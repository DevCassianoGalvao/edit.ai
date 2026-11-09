"""Pré-seleção de quadros para MINIATURA chamativa (só clipes que estão no filme).
Tags de impacto: ford_ext, launch, landing, night, sunset_sea, carrier_ext, hornet, flightdeck.
6 quadros por clipe; nota = nitidez (variância de bordas) x colorido (Hasler-Süsstrunk) x brilho ok.
Saída: qa/thumbs2/c_<clip>_<k>.png (1920x1080) + qa/thumbs2/top.jpg (48 melhores, rotulados)."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "qa" / "thumbs2"
OUT.mkdir(parents=True, exist_ok=True)
clips = {c["id"]: c for c in json.loads((ROOT / "data/clips.json").read_text("utf-8"))["clips"]}
used = {it["clip"] for it in json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"] if it.get("clip")}
IMPACT = {"submarine_surface", "submarine_underwater", "arctic_ice", "missile", "periscope", "berthing",
          "control_room"}  # vida dentro de um submarino nuclear
cands = [c for cid, c in clips.items() if cid in used and c["kind"] == "video" and IMPACT & set(c["tags"])]


def score(im):
    small = im.resize((480, 270))
    a = np.asarray(small).astype(float)
    rg, yb = a[..., 0] - a[..., 1], 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
    color = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    edges = ImageStat.Stat(small.convert("L").filter(ImageFilter.FIND_EDGES)).var[0]
    bright = ImageStat.Stat(small.convert("L")).mean[0]
    bpen = 1.0 if 60 < bright < 200 else 0.5
    return (edges ** 0.5) * (color + 10) * bpen


rows = []
for c in cands:
    src = ROOT / "public" / c["file"]
    dur = c["dur"] / 30
    for k in range(6):
        png = OUT / f"c_{c['id']}_{k}.png"
        if not png.exists():
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{dur * (0.08 + 0.84 * k / 5):.2f}",
                            "-i", str(src), "-frames:v", "1", str(png)])
        if png.exists():
            rows.append((score(Image.open(png).convert("RGB")), png, c))
rows.sort(key=lambda r: -r[0])
# no máximo 2 quadros por clipe no topo
top, per = [], {}
for s, p, c in rows:
    if per.get(c["id"], 0) >= 2:
        continue
    per[c["id"]] = per.get(c["id"], 0) + 1
    top.append((s, p, c))
    if len(top) >= 48:
        break
TW, TH, COLS = 480, 270, 6
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
sheet = Image.new("RGB", (TW * COLS, 8 * (TH + 22)), (18, 18, 18))
dr = ImageDraw.Draw(sheet)
for n, (s, p, c) in enumerate(top):
    x, y = (n % COLS) * TW, (n // COLS) * (TH + 22)
    sheet.paste(Image.open(p).convert("RGB").resize((TW, TH)), (x, y + 22))
    dr.text((x + 4, y + 3), f"#{n} {p.stem[2:]} {','.join(c['tags'][:2])}", fill=(255, 220, 0), font=font)
sheet.save(OUT / "top.jpg", quality=85)
(OUT / "top.json").write_text(json.dumps([str(p) for _, p, _ in top], indent=1), "utf-8")
print(f"[thumbs2] {len(cands)} clipes, {len(rows)} quadros -> qa/thumbs2/top.jpg")
