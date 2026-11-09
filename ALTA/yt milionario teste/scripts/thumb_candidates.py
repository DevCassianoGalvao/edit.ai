"""Pré-seleção de MINIATURA: quadros em 1080p dos clipes que mostram o próprio Ford por fora
(tag ford_ext) E que estão na timeline atual (a foto da miniatura tem que estar no filme).
Saída: qa/thumbs/cand_<clip>_<k>.png (1920x1080) + qa/thumbs/candidates.jpg (grade rotulada)."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "qa" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)
clips = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
used = {it["clip"] for it in json.loads((D / "timeline.json").read_text("utf-8"))["items"] if it.get("clip")}
cands = [c for c in clips.values() if c["kind"] == "video" and "ford_ext" in c["tags"] and c["id"] in used]
tiles = []
for c in sorted(cands, key=lambda c: c["id"]):
    src = ROOT / "public" / c["file"]
    dur = c["dur"] / 30
    for k, frac in enumerate((0.2, 0.5, 0.8)):
        png = OUT / f"cand_{c['id']}_{k}.png"
        if not png.exists():
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{dur * frac:.2f}", "-i", str(src),
                            "-frames:v", "1", str(png)], check=False)
        if png.exists():
            tiles.append((png, f"{c['id']}_{k}  {(c.get('channel') or c.get('title') or '')[:40]}"))
TW, TH, COLS = 480, 270, 6
rows = (len(tiles) + COLS - 1) // COLS
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
sheet = Image.new("RGB", (TW * COLS, max(1, rows) * (TH + 22)), (18, 18, 18))
dr = ImageDraw.Draw(sheet)
for n, (p, label) in enumerate(tiles):
    x, y = (n % COLS) * TW, (n // COLS) * (TH + 22)
    sheet.paste(Image.open(p).convert("RGB").resize((TW, TH)), (x, y + 22))
    dr.text((x + 4, y + 3), label, fill=(255, 220, 0), font=font)
sheet.save(OUT / "candidates.jpg", quality=82)
print(f"[thumbs] {len(cands)} clipes ford_ext no filme, {len(tiles)} quadros -> qa/thumbs/candidates.jpg")
