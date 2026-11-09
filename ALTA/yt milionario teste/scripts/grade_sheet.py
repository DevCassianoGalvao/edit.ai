"""qa/grade_sheet.jpg — porta de saída do grade do tema (PROMPT_v_ULTRA, seção 5).
Linhas: 4 cortes de vídeo (2 quentes, 2 frios) e 4 fotos; colunas: quadro cru | ffmpeg com grade | Remotion com grade.
O ffmpeg (cortes secos) e o Remotion (fotos, cortes com sobreposição) têm de parecer da mesma câmera.
Uso: python grade_sheet.py"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_hybrid import grade_filter  # noqa: E402
ROOT = Path(__file__).resolve().parent.parent
D, Q = ROOT / "data", ROOT / "qa" / "grade"
Q.mkdir(parents=True, exist_ok=True)
tl = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
cuts = [it for it in tl if it["type"] == "cut" and it.get("src")]
vid = [it for it in cuts if it["kind"] == "video"]
pick = ([it for it in vid if it.get("lado") == "quente"][::max(1, len(vid) // 8)][:2] +
        [it for it in vid if it.get("lado") == "frio"][::max(1, len(vid) // 8)][:2] +
        [it for it in cuts if it["kind"] == "photo"][::max(1, len(cuts) // 12)][:4])
jobs, rows = [], []
for it in pick:
    mid = it["from"] + it["dur"] // 2
    raw, ff = Q / f"{it['id']}_raw.jpg", Q / f"{it['id']}_ff.jpg"
    src = ROOT / "public" / it["src"]
    if it["kind"] == "video":
        f0 = it.get("trimBefore", 0) + it["dur"] // 2
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"select=eq(n\,{f0})", "-frames:v", "1", str(raw)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"select=eq(n\,{f0}),{grade_filter(it.get('lado', 'quente'))}", "-frames:v", "1", str(ff)], check=True)
    else:
        Image.open(src).convert("RGB").resize((1920, 1080)).save(raw, quality=90)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", grade_filter(it.get("lado", "quente")), "-frames:v", "1", str(ff)], check=True)
    rm = Q / f"{it['id']}_rm.jpg"
    jobs.append({"comp": "Main", "frame": mid, "out": str(rm.relative_to(ROOT)).replace("\\", "/"), "props": {}})
    rows.append((it, raw, ff, rm))
(Q / "jobs.json").write_text(json.dumps({"public": True, "jobs": jobs}), "utf-8")
subprocess.run(["node", "scripts/stills.mjs", str(Q / "jobs.json")], check=True)
W, H = 480, 270
sheet = Image.new("RGB", (3 * W, len(rows) * (H + 22)), "black")
d = ImageDraw.Draw(sheet)
for r, (it, raw, ff, rm) in enumerate(rows):
    y = r * (H + 22)
    for c, p in enumerate((raw, ff, rm)):
        try:
            sheet.paste(Image.open(p).convert("RGB").resize((W, H)), (c * W, y + 22))
        except Exception:
            d.rectangle((c * W, y + 22, c * W + W, y + 22 + H), fill="red")
    d.text((4, y + 5), f"{it['id']} {it['kind']} lado={it.get('lado')}   |   cru   |   ffmpeg+grade   |   Remotion+grade", fill="yellow")
sheet.save(ROOT / "qa" / "grade_sheet.jpg", quality=88)
# medida: luminância média (0-255) cru / ffmpeg / Remotion e diferença ffmpeg x Remotion — têm de ficar a < 6 pontos
import numpy as np
for it, raw, ff, rm in rows:
    L = [np.asarray(Image.open(p).convert("L").resize((480, 270)), dtype=float) for p in (raw, ff, rm)]
    print(f"  {it['id']} {it['kind']:5s} {it.get('lado')}: cru {L[0].mean():5.1f}  ffmpeg {L[1].mean():5.1f}  remotion {L[2].mean():5.1f}  |ff-rm| {np.abs(L[1] - L[2]).mean():4.1f}  bordas ff/rm {L[1][:30].mean():5.1f}/{L[2][:30].mean():5.1f}")
print("qa/grade_sheet.jpg", len(rows), "linhas")
