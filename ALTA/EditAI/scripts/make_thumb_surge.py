"""Miniaturas "Your Surge Protector Still Works" (en, 03/11). Números ditos: three to five, seven, 120."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_surge"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "surge_35", "src": F / "ia_08.jpg", "num": "3-5", "word": "YEARS, THEN REPLACE IT", "size": 300},
    {"name": "surge_7", "src": F / "ia_03.jpg", "num": "7", "word": "STEPS TO CHECK YOUR STRIPS", "size": 330},
    {"name": "surge_120", "src": F / "ia_01.jpg", "num": "120", "word": "VOLTS AND ONE WORN-OUT PART", "size": 250},
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
