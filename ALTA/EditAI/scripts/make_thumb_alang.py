"""Piec miniatur "Alang - najwiekszy cmentarz statkow" (pl). Kazda liczba pada w narracji:
ponad 150 dzialek; 26 zabitych; 16 procent; 10 metrow przyplywu; 1983.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_alang"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "alg_150", "src": S / "p3e8218d2.jpg", "num": "150", "word": "STOCZNI NA PLAŻY", "size": 260},
    {"name": "alg_26", "src": S / "pdfc4a193.jpg", "num": "26", "word": "ZABITYCH", "size": 270},
    {"name": "alg_16", "src": S / "p2dfc11e0.jpg", "num": "16%", "word": "AZBEST W PŁUCACH", "size": 250},
    {"name": "alg_10m", "src": S / "p709f3148.jpg", "num": "10 M", "word": "PRZYPŁYWU", "size": 260},
    {"name": "alg_1983", "src": S / "pa540a7d7.jpg", "num": "1983", "word": "CMENTARZ STATKÓW", "size": 250},
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
