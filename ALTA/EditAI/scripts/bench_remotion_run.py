"""Roda bench_remotion.mjs por variante medindo CPU do SISTEMA (Chrome + node + ffmpeg) e SSIM contra a base."""
import json, re, subprocess, sys, time
from pathlib import Path
import psutil

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "out" / "bench"
VARS = json.loads(sys.argv[1])
NQ = sys.argv[2] if len(sys.argv) > 2 else "1020"


def ssim(a, b):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(a), "-i", str(b), "-lavfi", "ssim", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"All:([\d.]+)", r.stderr)
    return float(m.group(1)) if m else -1


base = None
print(f"{'variante':22s} {'tempo':>7s} {'q/s':>6s} {'CPU sist méd':>12s} {'pico':>5s} {'RAM pico':>9s} {'SSIM':>7s}")
for nome, opts in VARS:
    psutil.cpu_percent(None)
    pr = subprocess.Popen(["node", "scripts/bench_remotion.mjs", nome, json.dumps(opts), NQ], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    am, pico, ram = [], 0, 0
    t0 = time.time()
    while pr.poll() is None:
        c = psutil.cpu_percent(interval=1)
        am.append(c); pico = max(pico, c)
        ram = max(ram, psutil.virtual_memory().used / 1e9)
    dt = time.time() - t0
    out = B / f"{nome}.mp4"
    if pr.returncode or not out.exists():
        print(nome, "FALHOU", (pr.stdout.read() or "")[-300:]); continue
    base = base or out
    s = 1.0 if out == base else ssim(base, out)
    print(f"{nome:22s} {dt:6.1f}s {int(NQ) / dt:6.1f} {sum(am) / len(am):11.0f}% {pico:4.0f}% {ram:8.1f}G {s:7.4f}",
          flush=True)
