"""Miniaturas "The Hidden World Inside a Mountain" (en, 05/11). Números ditos: 2,000 feet, 15 buildings, 110,000 rock bolts."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_hidden"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "hw_2000", "src": F / "p2c9a29a1.jpg", "num": "2,000", "word": "FEET OF GRANITE ABOVE IT", "size": 220},
    {"name": "hw_15", "src": F / "p8d4ba563.jpg", "num": "15", "word": "BUILDINGS ON GIANT SPRINGS", "size": 240},
    {"name": "hw_110000", "src": F / "p978afcf0.jpg", "num": "110,000", "word": "ROCK BOLTS · ONE MOUNTAIN", "size": 200},
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
