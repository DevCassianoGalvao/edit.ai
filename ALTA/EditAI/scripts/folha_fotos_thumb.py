"""Folha de conferencia das fotos candidatas a miniatura (a folha e o juiz).
Uso: python folha_fotos_thumb.py [pasta] [saida.jpg]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "APAGAR_navio-2026-09-16" / "fotos_thumb"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "qa" / "thumbs_200t" / "candidatas.jpg"
fotos = sorted(p for p in src.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
COLS, CW, CH = 4, 470, 300
linhas = (len(fotos) + COLS - 1) // COLS
folha = Image.new("RGB", (COLS * CW, linhas * CH), (14, 16, 20))
d = ImageDraw.Draw(folha)
for i, p in enumerate(fotos):
    try:
        im = Image.open(p).convert("RGB")
    except Exception:
        continue
    im.thumbnail((CW - 10, CH - 34), Image.LANCZOS)
    x, y = (i % COLS) * CW + 5, (i // COLS) * CH + 5
    folha.paste(im, (x, y))
    d.text((x + 3, y + CH - 28), f"{i:02d} {p.stem[:44]}", fill=(235, 235, 235))
out.parent.mkdir(parents=True, exist_ok=True)
folha.save(out, quality=88)
print(out, len(fotos), "fotos")
