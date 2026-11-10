"""TRAVA DA GPU/CPU pesada entre as BAIAS (28/09/2026, painel: vários filmes ao mesmo tempo).

O PC (16 GB, RTX 2050 4 GB) aguenta UM render por vez (Remotion + ffmpeg + acabamento). A trava é um arquivo em
<pasta ALTA PRODUÇÃO>/.trava_pesado com {pid, baia, etapa, desde}; quem chega depois ESPERA.
Trava de processo morto (PC reiniciou, janela fechada) é tomada sozinha.

04/10/2026 — TRAVA DA GPU separada (.trava_gpu) para a TRANSCRIÇÃO: o filme do crédito rural esperou ~40 min o render
do porta-aviões para uma transcrição de 4 min. Agora a transcrição pega só a trava da GPU e roda JUNTO com um render
quando há VRAM livre (>= VRAM_MIN MiB no nvidia-smi: large-v3 int8_float16 mediu 2,2 GB de pico). Sem VRAM, espera.
Junto com render ela roda com TRANSCRIBE_SEM_CPU=1 (nunca cai para a CPU, que derrubaria o render); se a GPU falhar,
o novo_filme espera a trava pesada e transcreve do jeito antigo. O render, ao começar, espera a trava da GPU soltar
(transcrição é curta), para o teste do NVENC não falhar por falta de VRAM e cair no x264 da CPU.

07/10/2026 — RENDER EXCLUSIVO (trava "média"): medido no filme da Toyota, o render levou 40 min com a outra baia
trabalhando ao lado (memória do PC estourava: o PC parado já usa ~8 dos 16 GB, o render ~7 GB) e ~10 min sozinho
(ffmpeg 35 mil quadros em 5,5 min + Remotion 9,5 mil em 9,8 min). Passos pesados de CPU/memória (preparar, make_clips,
prefilter, paralaxe, make_photos) usam `with media("..."):` — esperam o render de OUTRA baia acabar, e o render
espera eles acabarem antes de começar (até 40 min). Downloads (rede) não entram: rodam junto sem problema.

Uso no código:  from trava import pesado, gpu, media ;  with pesado("render"): ...  /  with gpu("transcrição") as junto: ...
Terminal:       python trava.py            # mostra quem está com cada trava
"""
import json, os, subprocess, sys, time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT.parent.parent if ROOT.parent.name == "baias" else ROOT.parent   # 28/09: a mesma trava para todas as baias
ARQ = BASE / ".trava_pesado"
ARQ_GPU = BASE / ".trava_gpu"
VRAM_MIN = 2400   # MiB livres: large-v3 int8_float16 mediu 2.235 MiB de pico (04/10, teste de 90 s) + folga


def _vivo(pid):
    try:
        r = subprocess.run(["tasklist", "/FI", f"PID eq {int(pid)}", "/NH"], capture_output=True, text=True)
        return str(int(pid)) in r.stdout
    except Exception:  # noqa: BLE001
        return True


def estado(arq=ARQ):
    try:
        e = json.loads(arq.read_text("utf-8"))
        return e if _vivo(e.get("pid", 0)) else None
    except Exception:  # noqa: BLE001
        return None


def vram_livre():
    """MiB livres na GPU (nvidia-smi); None se não der para medir."""
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=20)
        return int(r.stdout.strip().splitlines()[0])
    except Exception:  # noqa: BLE001
        return None


def _pega(arq, eu):
    try:
        fd = os.open(arq, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, json.dumps(eu, ensure_ascii=False).encode("utf-8"))
        os.close(fd)
        return True
    except FileExistsError:
        if estado(arq) is None:     # dono morreu: toma a trava
            arq.unlink(missing_ok=True)
            return _pega(arq, eu)
        return False


def _solta(arq):
    try:
        if json.loads(arq.read_text("utf-8")).get("pid") == os.getpid():
            arq.unlink()
    except Exception:  # noqa: BLE001
        pass


def _eu(etapa):
    return {"pid": os.getpid(), "baia": ROOT.name, "etapa": etapa, "desde": time.strftime("%Y-%m-%dT%H:%M:%S")}


@contextmanager
def pesado(etapa):
    eu = _eu(etapa)
    avisou = False
    while not _pega(ARQ, eu):
        e = estado(ARQ)
        if e and not avisou:
            print(f"[trava] esperando a vez: {e['baia']} está em '{e['etapa']}' desde {e['desde']}", flush=True)
            avisou = True
        time.sleep(15)
    avisou = False
    while estado(ARQ_GPU):          # 04/10: transcrição de outra baia na GPU -> o render espera ela acabar (minutos)
        if not avisou:
            g = estado(ARQ_GPU)
            print(f"[trava] esperando a GPU: {g['baia']} em '{g['etapa']}'", flush=True)
            avisou = True
        time.sleep(10)
    t0, avisou = time.time(), False
    while _medias_outras() and time.time() - t0 < 40 * 60:   # 07/10: render exclusivo — passos médios da outra baia acabam antes
        if not avisou:
            print(f"[trava] render esperando a outra baia terminar: {[m['etapa'] for m in _medias_outras()]}", flush=True)
            avisou = True
        time.sleep(10)
    try:
        yield
    finally:
        _solta(ARQ)


ARQ_MEDIA = BASE / ".trava_media"   # 07/10/2026: uma ficha por passo médio em andamento ({pid, baia, etapa, desde})


def _medias_outras():
    vivas = []
    for f in ARQ_MEDIA.glob("*.json") if ARQ_MEDIA.exists() else []:
        try:
            e = json.loads(f.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if not _vivo(e.get("pid", 0)):
            f.unlink(missing_ok=True)
        elif e.get("baia") != ROOT.name:
            vivas.append(e)
    return vivas


@contextmanager
def media(etapa):
    """Passo pesado de CPU/memória: não roda junto com o render de OUTRA baia (ver RENDER EXCLUSIVO no topo).
    Registra a ficha ANTES de olhar o render — assim ou ele vê o render e espera, ou o render vê a ficha e espera."""
    ARQ_MEDIA.mkdir(exist_ok=True)
    ficha = ARQ_MEDIA / f"{os.getpid()}.json"
    avisou = False
    while True:
        ficha.write_text(json.dumps(_eu(etapa), ensure_ascii=False), "utf-8")
        r = estado(ARQ)
        if r is None or r.get("baia") == ROOT.name:
            break
        ficha.unlink(missing_ok=True)
        if not avisou:
            print(f"[trava] {etapa} esperando o render de {r['baia']} acabar (render exclusivo)", flush=True)
            avisou = True
        time.sleep(15)
    try:
        yield
    finally:
        ficha.unlink(missing_ok=True)


@contextmanager
def gpu(etapa):
    """Trava só da GPU (transcrição). Rende `junto=True` quando roda ao lado de um render de outra baia."""
    eu = _eu(etapa)
    avisou = ""
    while True:
        render = estado(ARQ)
        livre = vram_livre()
        if render is None or (livre is not None and livre >= VRAM_MIN):
            if _pega(ARQ_GPU, eu):
                break
            msg = "outra transcrição na GPU"
        else:
            msg = f"render de {render['baia']} e só {livre} MiB de VRAM livres (precisa {VRAM_MIN})"
        if msg != avisou:
            print(f"[trava] transcrição esperando: {msg}", flush=True)
            avisou = msg
        time.sleep(15)
    junto = estado(ARQ) is not None
    if junto:
        print(f"[trava] transcrição JUNTO com o render ({vram_livre()} MiB livres)", flush=True)
    try:
        yield junto
    finally:
        _solta(ARQ_GPU)


if __name__ == "__main__":
    print("render:", estado(ARQ) or "livre")
    print("gpu:   ", estado(ARQ_GPU) or "livre", "| VRAM livre:", vram_livre(), "MiB")
