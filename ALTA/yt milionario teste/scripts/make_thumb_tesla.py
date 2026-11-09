"""Miniaturas "Tesla Model 3 démontée" (fr). Todo número é dito: 6 ans d'avance, 6 000 heures, 70 pièces -> 1, 100 000 $."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_tesla"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "tesla_6ans", "src": S / "pfb6fb2ed.jpg", "num": "6" + NB + "ANS", "word": "D'AVANCE SUR TOYOTA", "size": 280},
    {"name": "tesla_6000h", "src": S / "p6b904bb4.jpg", "num": "6" + NB + "000" + NB + "H", "word": "POUR LA DÉMONTER", "size": 240},
    {"name": "tesla_70a1", "src": S / "p32f20452.jpg", "num": "70" + NB + "→" + NB + "1", "word": "CE QU'ILS ONT TROUVÉ", "size": 260},
    {"name": "tesla_100000", "src": S / "p75274b38.jpg", "num": "100" + NB + "000" + NB + "$", "word": "POUR UNE MODEL 3", "size": 220},
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
