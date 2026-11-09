"""Cinco miniaturas de "O vibrador do radio de carro" (pt). Todo numero e dito na narracao:
115 vezes por segundo; 6 volts; 30 anos; 1947; 12 volts.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_vib"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "vib_115", "src": S / "pc252074b.jpg", "num": "115x", "word": "POR SEGUNDO", "size": 260},
    {"name": "vib_6v", "src": S / "pb43b3ade.jpg", "num": "6 VOLTS", "word": "O ZUMBIDO", "size": 250},
    {"name": "vib_30anos", "src": S / "p4d3736d9.jpg", "num": "30 ANOS", "word": "E SUMIU", "size": 250},
    {"name": "vib_1947", "src": S / "pe141cc64.jpg", "num": "1947", "word": "O FIM DO VIBRADOR", "size": 260},
    {"name": "vib_12v", "src": S / "p2c9890df.jpg", "num": "12 VOLTS", "word": "MUDOU TUDO", "size": 240},
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
