"""Miniaturas calor a bordo (pt, 01/11). Números ditos: 45 graus, 28 graus, 17 minutos, 1.495 km."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_calor"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "calor_45", "src": F / "p09afc646.jpg", "num": "45°C", "word": "NA CASA DE MÁQUINAS", "size": 230},
    {"name": "calor_28", "src": F / "p1d8786cd.jpg", "num": "28°C", "word": "E O NAVIO PAROU", "size": 230},
    {"name": "calor_17", "src": F / "p13aaccf7.jpg", "num": "17", "word": "MINUTOS NA MÁQUINA", "size": 260},
    {"name": "calor_1495", "src": F / "p2d2c6027.jpg", "num": "1.495", "word": "KM DE RIO E CALOR", "size": 210},
]


def main():
    for s in SPECS:
        make(s)
    outs = [ROOT / "out" / "thumbnails" / f"{s['name']}.jpg" for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
