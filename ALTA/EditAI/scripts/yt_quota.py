"""Cota COMPARTILHADA de extrações do YouTube (todas as sessões/cópias do pipeline nesta máquina).

O bloqueio "confirm you're not a bot" vem de VOLUME por IP. Em vez de contornar, fica abaixo do limite:
  - no máximo 1 extração a cada MIN_GAP s e DAY_MAX por 24 h (janela móvel), somando todas as sessões;
  - quando uma extração recebe o aviso de robô, TODAS as sessões param por COOLDOWN (não insistem).
Estado em %USERPROFILE%\\.yt_quota.json (trava por arquivo .lock).
"""
import json, os, time
from pathlib import Path

COOKIES = Path(__file__).resolve().parent.parent / "cookies.txt"  # só youtube.com/google.com, sessão logada


def ytdlp(*args):
    """Linha de comando do yt-dlp com uma CÓPIA do cookies.txt do projeto (quando existe).
    O yt-dlp regrava o arquivo de cookies ao sair: quando o YouTube derruba a sessão, ele gravou por cima
    a versão deslogada (14/09 17:39). A cópia por processo protege o original."""
    # 25/09/2026: com os clientes padrão o YouTube passou a devolver SÓ o formato 18 (360p) — 4 filmes seguidos
    # sem vídeo do YouTube. O cliente web_safari volta a listar até 1080p (testado no pOkLMp8iEX0).
    # 26/09/2026: COM o cookie da conta até o web_safari voltou a dar só o formato 18 (SunCable: 20 de 26 vídeos em
    # 360p). SEM cookie, o cliente mweb lista 1080p avc1. Padrão agora: sem cookie + mweb; YT_COOKIES=1 volta ao antigo.
    usa_cookie = os.environ.get("YT_COOKIES") == "1"
    ea = [] if any(str(a).startswith("youtube:player_client") for a in args) else         ["--extractor-args", "youtube:player_client=" + ("web_safari,default" if usa_cookie else "mweb,web_safari,default")]
    args = (*ea, *args)
    if not COOKIES.exists() or not usa_cookie:
        return ["yt-dlp", *args]
    import shutil, tempfile
    tmp = Path(tempfile.gettempdir()) / f"yt_cookies_{os.getpid()}.txt"
    shutil.copyfile(COOKIES, tmp)
    return ["yt-dlp", "--cookies", str(tmp), *args]


STATE = Path.home() / ".yt_quota.json"
LOCK = Path.home() / ".yt_quota.lock"
MIN_GAP = 45          # s entre extrações (com 20 s a sessão do cookie caiu após ~33 extrações em 10 min)
DAY_MAX = 160   # 04/10/2026: o aviso de robô veio com 169 extrações/24 h (4 filmes seguidos) — teto real ~170; antes: 400         # extrações por 24 h — o usuário subiu de 280 para 400 em 22/09/2026, depois que a
                      # busca passou para a API e o download passou a usar --load-info-json (filme caiu de
                      # ~140 para ~52 extrações). Histórico: 150 sem cookie, 200 no CN, 280 até 21/09.
                      # MIN_GAP de 45 s e a pausa de 3 h no aviso de robô continuam valendo — são elas que
                      # seguram o ritmo; se o aviso aparecer, BAIXAR de volta para 280.
COOLDOWN = 3 * 3600   # s parado depois de um aviso de robô
BOT_MARK = "confirm you"  # "Sign in to confirm you're not a bot"


class Blocked(RuntimeError):
    pass


class SemOrcamento(Blocked):
    """07/10/2026: o FILME gastou o orçamento dele (não é a cota do dia) — não esperar: completar com Pexels/foto."""
    pass


# 07/10/2026 (pedido do usuário: "tá demorando muito"): 2 filmes juntos gastaram ~120 das 160 extrações numa tarde e
# os dois ficaram ~2 h baixando 1 vídeo a cada 5 min. Cada filme agora tem um orçamento (data/yt_orcamento.json,
# zerado pelo novo_filme.py): padrão 40 se o filme é ≥70 % foto, 60 se não; pipeline_config "yt_max" muda.
RAIZ = Path(__file__).resolve().parent.parent
ORC = RAIZ / "data" / "yt_orcamento.json"


def orcamento():
    try:
        o = json.loads(ORC.read_text("utf-8"))
    except Exception:  # noqa: BLE001
        o = {}
    if "inicio" not in o:
        o = {"inicio": time.time()}
        try:
            ORC.parent.mkdir(parents=True, exist_ok=True)
            ORC.write_text(json.dumps(o), "utf-8")
        except OSError:
            pass
    try:
        cfg = json.loads((RAIZ / "data" / "pipeline_config.json").read_text("utf-8"))
    except Exception:  # noqa: BLE001
        cfg = {}
    # 10/10/2026 (meta de 2 h por vídeo): 25/35 — o resto do vídeo vem do DVIDS e do Pexels/Pixabay, buscados em paralelo
    # 12/10/2026 (regra do usuário: sempre 80 % foto / 20 % vídeo, meta de 1 vídeo por hora): teto 15 por filme
    padrao = 15
    return o["inicio"], int(o.get("max") or cfg.get("yt_max") or padrao)


def _locked(fn):
    t0 = time.time()
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:   # 29/09/2026: 3 baias sondando juntas — a trava some entre o open e o stat
                idade = time.time() - LOCK.stat().st_mtime
            except FileNotFoundError:
                continue
            if idade > 60:  # trava órfã
                LOCK.unlink(missing_ok=True)
            elif time.time() - t0 > 120:
                raise TimeoutError("trava da cota do YouTube presa")
            time.sleep(0.5)
    try:
        st = json.loads(STATE.read_text("utf-8")) if STATE.exists() else {}
        out = fn(st)
        STATE.write_text(json.dumps(st), "utf-8")
        return out
    finally:
        os.close(fd)
        LOCK.unlink(missing_ok=True)


def acquire(label="", wait=True):
    """Reserva uma extração. Espera o intervalo; levanta Blocked se houver aviso de robô recente ou cota do dia cheia."""
    inicio, teto = orcamento()
    while True:
        def step(st):
            now = time.time()
            st["calls"] = [t for t in st.get("calls", []) if now - t < 86400]
            if now - st.get("blocked_at", 0) < COOLDOWN:
                return ("blocked", COOLDOWN - (now - st["blocked_at"]))
            if len(st["calls"]) >= DAY_MAX:
                return ("day", 86400 - (now - st["calls"][0]))
            gap = MIN_GAP - (now - (st["calls"][-1] if st["calls"] else 0))
            pb = st.setdefault("por_baia", {})
            minhas = [t for t in pb.get(str(RAIZ), []) if now - t < 2 * 86400]
            if len([t for t in minhas if t >= inicio]) >= teto:
                return ("orcamento", 0)
            if gap > 0:
                return ("gap", gap)
            st["calls"].append(now)
            pb[str(RAIZ)] = minhas + [now]
            return ("ok", 0)
        kind, secs = _locked(step)
        if kind == "ok":
            return
        if kind == "orcamento":
            raise SemOrcamento(f"ORCAMENTO_ESGOTADO: este filme já usou as {teto} extrações do YouTube dele — "
                               f"complete com Pexels/Commons/foto (não espere) [{label}]")
        # YT_WAIT_DAY=1: cota do dia cheia ESPERA a janela móvel liberar (a janela solta aos poucos, não de uma vez —
        # 15/09 17:15 a busca parou após 1 consulta). O aviso de robô continua levantando Blocked.
        day_wait = kind == "day" and os.environ.get("YT_WAIT_DAY") == "1" and wait
        if kind == "blocked" or (kind == "day" and not day_wait) or not wait:
            raise Blocked(f"YouTube em pausa ({kind}) por mais {secs / 60:.0f} min [{label}]")
        time.sleep(min(secs + 1, 300) if day_wait else min(secs, MIN_GAP))


def report(output_text):
    """Chamar com stdout+stderr do yt-dlp: se houver aviso de robô, liga a pausa geral."""
    if BOT_MARK in (output_text or "").lower():
        def step(st):
            st["blocked_at"] = time.time()
        _locked(step)
        raise Blocked("YouTube pediu verificação de robô: pausa geral de "
                      f"{COOLDOWN // 3600} h para todas as sessões")


def status():
    def step(st):
        now = time.time()
        st["calls"] = [t for t in st.get("calls", []) if now - t < 86400]
        return len(st["calls"]), max(0, COOLDOWN - (now - st.get("blocked_at", 0)))
    n, cool = _locked(step)
    inicio, teto = orcamento()
    meu = _locked(lambda st: len([t for t in st.get("por_baia", {}).get(str(RAIZ), []) if t >= inicio]))
    return f"extrações 24h: {n}/{DAY_MAX} | este filme: {meu}/{teto} | pausa restante: {cool / 60:.0f} min"


if __name__ == "__main__":
    print(status())
