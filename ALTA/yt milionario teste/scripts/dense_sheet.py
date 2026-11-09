"""Folha DENSA de uma fonte do YouTube (arquivo local): N quadros com o SEGUNDO impresso, para escolher
janelas extras (data/extra_windows.json {key: [[s, e, [tags]], ...]}) de fontes já aprovadas.
Uso: python dense_sheet.py yt:ID N  -> qa/dense/ID.jpg (6 colunas, 480x270)"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from local_yt import local_yt

ROOT = Path(__file__).resolve().parent.parent
key, N = sys.argv[1], int(sys.argv[2])
vid = key[3:]
src = local_yt(vid)
pool = json.loads((ROOT / "data/yt_pool.json").read_text("utf-8"))
dur = float(pool[vid]["duration"])
out = ROOT / "qa/dense"; out.mkdir(parents=True, exist_ok=True)
tmp = out / "_tmp.jpg"
F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
COLS, TW, TH = 6, 480, 270
rows = (N + COLS - 1) // COLS
W = Image.new("RGB", (COLS * TW, rows * (TH + 26)), "black")
d = ImageDraw.Draw(W)
for i in range(N):
    t = dur * 0.03 + (dur * 0.87) * i / (N - 1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", f"scale={TW}:{TH}", str(tmp)])
    im = Image.open(tmp)
    x, y = (i % COLS) * TW, (i // COLS) * (TH + 26)
    d.text((x + 4, y + 2), f"#{i}  {t:.0f}s", fill="yellow", font=F)
    W.paste(im, (x, y + 26))
tmp.unlink(missing_ok=True)
W.save(out / f"{vid}.jpg", quality=82)
print(f"[dense] {vid} {N} quadros, {dur:.0f}s -> qa/dense/{vid}.jpg")
