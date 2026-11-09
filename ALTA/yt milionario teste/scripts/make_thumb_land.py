"""Miniaturas "You Own the Home. Someone Else Controls the Land." (en, 03/11). Números ditos: 99, 24 dollars, seven."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_land"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "land_99", "src": F / "p0dff9e19.jpg", "num": "99", "word": "YEAR LEASE ON YOUR LAND", "size": 330},
    {"name": "land_24", "src": F / "p22e9d9bb.jpg", "num": "$24", "word": "DEBT. YOUR HOUSE AT RISK", "size": 300},
    {"name": "land_7", "src": F / "pcd180356.jpg", "num": "7", "word": "STEPS BEFORE YOU SIGN", "size": 330},
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
