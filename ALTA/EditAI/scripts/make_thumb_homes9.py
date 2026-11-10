"""Miniaturas "9 Strange Features in Old American Homes" (en, 02/11). Números ditos: nine, 1908, 75 percent, 1878."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_homes9"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "homes9_9", "src": F / "paa2a57c1.jpg", "num": "9", "word": "STRANGE HOUSE FEATURES", "size": 330},
    {"name": "homes9_1908", "src": F / "p39b24080.jpg", "num": "1908", "word": "WHY THEY SLEPT OUTSIDE", "size": 230},
    {"name": "homes9_75", "src": F / "p34293c68.jpg", "num": "75%", "word": "HEATED WITH COAL OR WOOD", "size": 230},
    {"name": "homes9_1878", "src": F / "p2f2091e0.jpg", "num": "1878", "word": "THE MILK BOTTLE YEAR", "size": 230},
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
