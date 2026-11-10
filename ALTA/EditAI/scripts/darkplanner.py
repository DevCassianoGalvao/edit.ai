"""LOCUÇÃO pela API da DarkPlanner (07/10/2026, pedido do usuário: "interligar a minha API de áudio no pipeline").

Chave em <ALTA PRODUÇÃO>/chaves/darkplanner.txt (NUNCA imprimir nem gravar em log). Base: app.darkplanner.com.br/api/v1/audio
Regras da API (doc oficial /docs, conferida em 07/10): gerar 10/min; status/usage/history no máx. 1/s (acima = 429 com
Retry-After); links de download valem 24 h -> baixar na hora; estados processing|completed|failed|blocked|not_found.

  python darkplanner.py uso                         # uso do dia / limite / máx. de caracteres por áudio
  python darkplanner.py vozes [--json saida.json]   # lista as vozes (id, nome, gênero, amostra)
  python darkplanner.py gerar roteiro.txt saida.mp3 --voz ID [--vel 1.0] [--titulo nome]
                                                    # gera, espera, baixa mp3 + legenda.srt ao lado
"""
import json, sys, time, urllib.error, urllib.request
from pathlib import Path

BASE = "https://app.darkplanner.com.br/api/v1/audio"
CHAVE = Path(__file__).resolve().parents[2] / "chaves" / "darkplanner.txt"
if not CHAVE.exists():   # baias/bN/scripts -> a pasta ALTA PRODUÇÃO fica 3 níveis acima
    CHAVE = Path(__file__).resolve().parents[3] / "chaves" / "darkplanner.txt"


def _chave():
    k = CHAVE.read_text("utf-8").strip()
    if not k.startswith("dpk_"):
        sys.exit(f"[darkplanner] chave inválida em {CHAVE}")
    return k


def api(metodo, rota, corpo=None, tentativas=6):
    for i in range(tentativas):
        req = urllib.request.Request(BASE + rota, method=metodo,
                                     data=json.dumps(corpo).encode("utf-8") if corpo is not None else None,
                                     headers={"X-API-Key": _chave(), "Content-Type": "application/json",
                                              "User-Agent": "sala-de-montagem/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if e.code == 429 and i < tentativas - 1:
                espera = int(e.headers.get("Retry-After") or 10)
                print(f"[darkplanner] 429 (limite) — esperando {espera} s", flush=True)
                time.sleep(espera)
                continue
            if e.code >= 500 and i < tentativas - 1:
                time.sleep(10 * (i + 1))
                continue
            sys.exit(f"[darkplanner] ERRO {e.code} em {rota}: {msg}")
        except urllib.error.URLError as e:
            if i < tentativas - 1:
                time.sleep(10 * (i + 1))
                continue
            sys.exit(f"[darkplanner] sem conexão: {e}")


def voz_por_nome(nome, reserva=None):
    """20/10/2026 (pedido do usuário, conta nova): a voz de cada canal é achada PELO NOME na conta atual da DarkPlanner,
    porque o id pode mudar quando a conta muda. Nome igual (sem caixa) primeiro; senão o id de reserva do canais.json."""
    alvo = (nome or "").strip().lower()
    vozes = api("GET", "/voices").get("voices", [])
    for x in vozes:
        if (x.get("name") or "").strip().lower() == alvo:
            return x["id"]
    if reserva and any(x.get("id") == reserva for x in vozes):
        print(f"[darkplanner] voz '{nome}' não achada pelo nome — usando o id salvo", flush=True)
        return reserva
    sys.exit(f"[darkplanner] a voz '{nome}' não existe na conta atual (procure o nome certo em: darkplanner.py vozes)")


def baixa(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "sala-de-montagem/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        Path(destino).write_bytes(r.read())


def gerar(texto, saida, voz, vel=1.0, titulo=None, espera_max=3600):
    saida = Path(saida)
    uso = api("GET", "/usage")
    if not uso.get("can_generate", True):
        sys.exit(f"[darkplanner] limite do dia atingido: {uso.get('used_today')}/{uso.get('limit')}")
    if len(texto) > int(uso.get("max_characters_per_audio") or 10 ** 9):
        sys.exit(f"[darkplanner] roteiro com {len(texto)} caracteres; o plano aceita {uso['max_characters_per_audio']}")
    corpo = {"text": texto, "voice_id": voz, "speed": vel, "title": titulo or saida.stem}
    job = api("POST", "/generate", corpo)
    jid = job.get("job_id")
    if not jid:
        sys.exit(f"[darkplanner] sem job_id: {json.dumps(job, ensure_ascii=False)[:300]}")
    print(f"[darkplanner] job {jid} na fila ({len(texto)} caracteres)", flush=True)
    t0 = time.time()
    while True:
        time.sleep(5)
        st = api("GET", f"/status/{jid}").get("status")
        if st == "completed":
            break
        if st in ("failed", "blocked", "not_found", "expired"):
            sys.exit(f"[darkplanner] job {jid} terminou como {st}")
        if time.time() - t0 > espera_max:
            sys.exit(f"[darkplanner] job {jid} passou de {espera_max // 60} min em {st}")
    d = api("GET", f"/download/{jid}")
    saida.parent.mkdir(parents=True, exist_ok=True)
    baixa(d["audio_url"], saida)
    if d.get("srt_url"):
        baixa(d["srt_url"], saida.with_suffix(".srt"))
    print(f"[darkplanner] pronto em {time.time() - t0:.0f} s -> {saida} ({saida.stat().st_size / 1e6:.1f} MB)", flush=True)
    return saida


if __name__ == "__main__":
    a = sys.argv[1:]
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if not a or a[0] == "uso":
        print(json.dumps(api("GET", "/usage"), ensure_ascii=False, indent=1))
    elif a[0] == "vozes":
        v = api("GET", "/voices")
        if op("--json"):
            Path(op("--json")).write_text(json.dumps(v, ensure_ascii=False, indent=1), "utf-8")
        for x in v.get("voices", []):
            print(f"{x.get('id')}\t{x.get('name')}\t{x.get('gender')}\t{x.get('preview_url') or ''}")
        print(f"total: {v.get('total', len(v.get('voices', [])))}")
    elif a[0] == "gerar":
        gerar(Path(a[1]).read_text("utf-8"), a[2], op("--voz"), float(op("--vel", 1.0)), op("--titulo"))
    else:
        sys.exit(__doc__)
