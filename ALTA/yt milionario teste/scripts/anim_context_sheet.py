"""Passada final das animações NO CONTEXTO REAL: renderiza pela composição Main (cues do Whisper
vindos da timeline), 4 quadros por animação longe dos fades: +30, cue do meio +20, último cue +45, fim -20.
Saída: qa/anim_context.jpg (13 linhas x 4 colunas, rótulo = cena e segundo do filme)."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"]
anims = [it for it in items if it["type"] == "animation"]
jobs, rows = [], []
for it in anims:
    a, d = it["from"], it["dur"]
    cues = sorted((it.get("cues") or {}).values())
    mid = cues[len(cues) // 2] + 20 if cues else d // 2
    last = cues[-1] + 45 if cues else int(d * 0.75)
    fr = [30, mid, last, d - 20]
    fr = [min(max(f, it["fadeIn"] + 6), d - 20) for f in fr]
    row = []
    for k, f in enumerate(fr):
        out = f"qa/_anim/{it['scene']}_{k}.jpg"
        jobs.append({"comp": "Main", "frame": a + f, "out": out, "scale": 0.25})
        row.append((out, (a + f) / 30))
    rows.append((it["scene"], row))
(ROOT / "qa/jobs_anim_ctx.json").write_text(json.dumps({"public": "audio", "jobs": jobs}), "utf-8")
subprocess.run(["node", str(ROOT / "scripts/stills.mjs"), str(ROOT / "qa/jobs_anim_ctx.json")], cwd=ROOT, check=True)
TW, TH = 480, 270
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
sheet = Image.new("RGB", (TW * 4, (TH + 22) * len(rows)), (18, 18, 18))
dr = ImageDraw.Draw(sheet)
for r, (scene, row) in enumerate(rows):
    for k, (p, sec) in enumerate(row):
        x, y = k * TW, r * (TH + 22)
        sheet.paste(Image.open(ROOT / p).resize((TW, TH)), (x, y + 22))
        dr.text((x + 4, y + 3), f"{scene}  {int(sec // 60)}:{sec % 60:04.1f}", fill=(255, 220, 0), font=font)
sheet.save(ROOT / "qa/anim_context.jpg", quality=82)
print("[anim] qa/anim_context.jpg", len(jobs), "quadros")
