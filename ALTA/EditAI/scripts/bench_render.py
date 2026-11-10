"""07/10/2026 — BANCO DE TESTE do render híbrido (não faz parte do pipeline). Usa um filme já entregue que ainda está
em APAGAR_<slug>/ (pacote do Remotion, public/ e plan.json) e mede: ffmpeg sozinho, Remotion sozinho, os dois juntos
(como o render faz hoje) e os dois juntos com o ffmpeg em prioridade abaixo do normal.
Uso: python scripts/bench_render.py <pasta APAGAR_...> <saida> <cenario: ff|remo|junto|junto_baixa> [quadros_ff]"""
import json, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AP, OUT, CEN = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
ALVO = int(sys.argv[4]) if len(sys.argv) > 4 else 6000
OUT.mkdir(parents=True, exist_ok=True)
B1 = Path(__file__).resolve().parent.parent
for rel in ("src/design/tokens.ts", "data/pipeline_config.json"):
    (AP / rel).parent.mkdir(parents=True, exist_ok=True)
    if not (AP / rel).exists():
        shutil.copy2(B1 / rel, AP / rel)
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(B1 / "scripts"))
import render_hybrid as R
R.ROOT, R.D, R.HY = AP, AP / "data", OUT
plan = json.loads((AP / "out/hybrid/plan.json").read_text("utf-8"))
ff, n = [], 0
for s in plan["segments"]:
    if s["engine"] == "ffmpeg" and n < ALVO:
        s = {**s, "file": str(OUT / Path(s["file"]).name)}
        Path(s["file"]).unlink(missing_ok=True)
        ff.append(s)
        n += s["end"] - s["start"]
R.LOW = subprocess.BELOW_NORMAL_PRIORITY_CLASS if CEN == "junto_baixa" else 0


def roda_ff():
    t = time.time()
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda s: R.render_ff(s, plan["videoDrift"]), ff))
    return time.time() - t


def roda_remo():
    r = subprocess.run(["node", str(B1 / "scripts/bench_remotion.mjs"), str(AP / "out/bundle"), "20000", str(20000 + int(__import__("os").environ.get("REMO_Q", "1500"))),
                        str(OUT / "remo.mp4"), "-", "3"], capture_output=True, text=True, cwd=B1)
    return json.loads(r.stdout.strip().splitlines()[-1])


if CEN == "ff":
    print(f"ffmpeg sozinho: {n} quadros em {roda_ff():.0f} s")
elif CEN == "remo":
    print("Remotion sozinho:", roda_remo())
else:
    with ThreadPoolExecutor(2) as ex:
        a = ex.submit(roda_remo)
        tff = roda_ff()
        print(f"[{CEN}] ffmpeg: {n} quadros em {tff:.0f} s | Remotion: {a.result()}")
