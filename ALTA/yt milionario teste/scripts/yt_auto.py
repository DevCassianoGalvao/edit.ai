"""Tenta o YouTube sozinho até conseguir, SEM contornar a verificação anti-robô.

Loop (até 72 h):
  1. respeita a pausa geral da cota (scripts/yt_quota.py) — nunca bate no YouTube durante a pausa;
  2. testa UMA extração (conta na cota); se o YouTube pedir verificação, a cota liga nova pausa e o loop volta a esperar;
  3. liberado: busca (fetch_video.py queries/cn_youtube.txt) → seleção (select_probe 0 N data/probe_round3.json)
     → folha de sondagem (probe_sheet.py → qa/probe3) → grava data/yt_auto_done.txt e sai.
Log: data/yt_auto.log
"""
import json, subprocess, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_quota

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "scripts"
LOG = ROOT / "data" / "yt_auto.log"
TEST_URL = "https://www.youtube.com/watch?v=n8TvEzUV_C4"
# uso: python yt_auto.py [queries.txt] [N]  (padrão: filme CN)
QUERIES = Path(sys.argv[1]) if len(sys.argv) > 1 else S / "queries" / "cn_youtube.txt"
N_YT = int(sys.argv[2]) if len(sys.argv) > 2 else 30
DEADLINE = time.time() + 72 * 3600


def log(msg):
    line = f"{datetime.now():%d/%m %H:%M} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args, timeout=None):
    p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    yt_quota.report(p.stderr + p.stdout)  # aviso de robô em qualquer etapa liga a pausa geral
    return p


def pause_left():
    st = json.loads(yt_quota.STATE.read_text("utf-8")) if yt_quota.STATE.exists() else {}
    return max(0.0, yt_quota.COOLDOWN - (time.time() - st.get("blocked_at", 0)))


def main():
    log("iniciado")
    while time.time() < DEADLINE:
        left = pause_left()
        if left > 0:
            log(f"pausa da cota: esperando {left / 60:.0f} min")
            time.sleep(min(left + 30, 1800))
            continue
        try:
            yt_quota.acquire("yt_auto teste")
            p = subprocess.run(yt_quota.ytdlp("-F", "--no-warnings", TEST_URL), capture_output=True, text=True, timeout=120)
            yt_quota.report(p.stderr)
            if p.returncode != 0:
                log(f"teste falhou sem aviso de robô: {(p.stderr.strip().splitlines() or [''])[-1][:120]}")
                time.sleep(900)
                continue
            log("YouTube LIBERADO — buscando")
            r = run([str(S / "fetch_video.py"), str(QUERIES)], timeout=6 * 3600)
            log(f"busca: {(r.stdout.strip().splitlines() or [''])[-1][:160]}")
            r = run([str(S / "select_probe.py"), "0", str(N_YT), "data/probe_round3.json", "--skip", "data/source_side.json"])
            log(f"seleção: {r.stdout.strip()[-160:]}")
            r = run([str(S / "probe_sheet.py"), "data/probe_round3.json", "qa/probe3"], timeout=3 * 3600)
            sheets = len(list((ROOT / "qa" / "probe3").glob("sheet_*.jpg")))
            fails = r.stdout.count("[grab] falhou")
            (ROOT / "data" / "yt_auto_done.txt").write_text(f"{datetime.now():%d/%m %H:%M} folhas {sheets} falhas {fails}\n", "utf-8")
            log(f"PRONTO: qa/probe3 com {sheets} folhas ({fails} quadros falhos)")
            return
        except yt_quota.Blocked as e:
            log(f"bloqueado: {e}")
        except subprocess.TimeoutExpired as e:
            log(f"timeout: {e}")
            time.sleep(600)
    log("prazo de 72 h esgotado sem liberar")


if __name__ == "__main__":
    main()
