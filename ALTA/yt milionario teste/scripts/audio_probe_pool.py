"""Mede cada faixa/efeito do pool (duração, LUFS integrado, LRA, pico) -> data/music_probe.json e data/sfx_probe.json.
Serve para classificar clima (cama/tensão/reveal) sem ouvir: LRA alto e variação de energia = tensão; LRA baixo = cama."""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

def medir(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, errors="replace")
    txt = r.stderr
    def g(pat):
        m = re.findall(pat, txt)
        return float(m[-1]) if m else None
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return {"dur_s": float(dur or 0), "lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "lra": g(r"LRA:\s+([\d.]+) LU"),
            "peak_dbtp": g(r"Peak:\s+(-?[\d.]+) dBFS")}

for nome, pool in (("music", "music_pool.json"), ("sfx", "sfx_pool.json")):
    if len(sys.argv) > 1 and sys.argv[1] != nome:
        continue
    p = json.loads((D / pool).read_text("utf-8"))
    out = {}
    for k, v in p.items():
        f = ROOT / v["file"]
        if f.exists():
            out[k] = medir(f); print(f"[{nome}] {k} {out[k]}", flush=True)
    (D / f"{nome}_probe.json").write_text(json.dumps(out, indent=1), "utf-8")
    print(f"[{nome}] {len(out)} medidos -> data/{nome}_probe.json")
