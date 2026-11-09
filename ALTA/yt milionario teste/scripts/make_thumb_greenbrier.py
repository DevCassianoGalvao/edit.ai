"""Miniaturas "Inside the Greenbrier" (en, 02/11). Números ditos: thirty years, 535 lawmakers, 25 tons."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_greenbrier"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "gb_30", "src": F / "p6f0c4e18.jpg", "num": "30", "word": "YEARS · UNDER A RESORT", "size": 260},
    {"name": "gb_535", "src": F / "p08b3835e.jpg", "num": "535", "word": "LAWMAKERS · ONE BUNKER", "size": 230},
    {"name": "gb_25", "src": F / "p07e0927c.jpg", "num": "25", "word": "TON DOOR · HIDDEN BUNKER", "size": 230},
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
