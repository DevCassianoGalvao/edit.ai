"""Miniaturas "Os 5 frigoríficos mais expostos à China" (pt). Todo número é dito: 67 %, 70 %,
39 %, 6 plantas."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_carne"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "carne_67", "src": S / "p8a30e20e.jpg", "num": "67%", "word": "IMPOSTO DA CHINA", "size": 300},
    {"name": "carne_70", "src": S / "pf814370e.jpg", "num": "70%", "word": "IA PARA A CHINA", "size": 300},
    {"name": "carne_5", "src": S / "p00e09a52.jpg", "num": "5", "word": "FRIGORÍFICOS NA MIRA", "size": 300},
    {"name": "carne_39", "src": S / "p11716625.jpg", "num": "39%", "word": "DA CARNE DO MS", "size": 300},
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
