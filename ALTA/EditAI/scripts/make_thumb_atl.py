"""Piec miniatur "Dlaczego samoloty leca nad Atlantykiem w nocy" (pl). Kazda liczba pada w narracji:
1200 km/h; 4 h 56 min; ponad 2000 samolotow; 6 stref; 400 km/h.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_atl"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "atl_1200", "src": S / "p1ed3d202.jpg", "num": "1200 KM/H", "word": "NAD OCEANEM", "size": 240},
    {"name": "atl_456", "src": S / "p99318fbf.jpg", "num": "4:56", "word": "NOWY JORK–LONDYN", "size": 260},
    {"name": "atl_2000", "src": S / "p385d096f.jpg", "num": "2000", "word": "SAMOLOTÓW NOCĄ", "size": 260},
    {"name": "atl_6stref", "src": S / "p920a8461.jpg", "num": "6 STREF", "word": "W JEDNĄ NOC", "size": 250},
    {"name": "atl_400", "src": S / "p10114f84.jpg", "num": "400 KM/H", "word": "WIATRU", "size": 250},
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
