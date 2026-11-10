"""Piec miniatur "Trzy firmy, silniki odrzutowe" (pl). Kazda liczba pada w narracji:
3 firmy; 61 ton ciagu; 1300 stopni; 6 miliardow dolarow; 10 tysiecy obrotow.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_jet"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "jet_3firmy", "src": S / "p23d9657e.jpg", "num": "3 FIRMY", "word": "NA ŚWIECIE", "size": 250},
    {"name": "jet_61t", "src": S / "pf1d80fce.jpg", "num": "61 TON", "word": "CIĄGU", "size": 260},
    {"name": "jet_1300", "src": S / "pb3c08fc9.jpg", "num": "1300°C", "word": "METAL SIĘ TOPI", "size": 240},
    {"name": "jet_6mld", "src": S / "pc493ba31.jpg", "num": "6 MLD $", "word": "JEDNA DROBINKA", "size": 240},
    {"name": "jet_10000", "src": S / "pa95f6cd3.jpg", "num": "10 000", "word": "OBROTÓW NA MINUTĘ", "size": 240},
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
