"""Miniaturas "A JAC do Faustão pediu recuperação judicial" (pt). Todo número é dito: R$ 239 milhões, 988 carros em
2025, 50 lojas num único dia, 3 vezes George Clooney."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_jac"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "jac_239mi", "src": S / "p32d922c7.jpg", "num": "R$" + NB + "239" + NB + "MI", "word": "EM DÍVIDAS", "size": 230},
    {"name": "jac_988", "src": S / "p333b979d.jpg", "num": "988", "word": "CARROS EM 2025", "size": 300},
    {"name": "jac_50lojas", "src": S / "p2f26e5d0.jpg", "num": "50" + NB + "LOJAS", "word": "NUM ÚNICO DIA", "size": 240},
    {"name": "jac_3x", "src": S / "p32d922c7.jpg", "num": "3X", "word": "MAIS CARO QUE CLOONEY", "size": 300},
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
