"""Miniaturas "Cheyenne Mountain (en, 05/11). Números ditos: 25 tons, 2,000 feet, 1,319 springs."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_cheyenne"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "cm_25", "src": F / "pb8d3c4af.jpg", "num": "25", "word": "TON DOORS · NUCLEAR BUNKER", "size": 230},
    {"name": "cm_2000", "src": F / "p73b639bb.jpg", "num": "2,000", "word": "FEET INSIDE A MOUNTAIN", "size": 220},
    {"name": "cm_1319", "src": F / "pe2a719bf.jpg", "num": "1,319", "word": "STEEL SPRINGS · ONE BUNKER", "size": 220},
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
