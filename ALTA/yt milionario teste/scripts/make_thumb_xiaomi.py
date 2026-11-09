"""Miniaturas "Xiaomi a acheté 3 Tesla et les a démontées" (fr). Todo número é dito: 3 Tesla, 3 Model Y,
7 minutes 04 (Nürburgring), 240 000 commandes en 18 heures."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_xiaomi"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "xiaomi_3tesla", "src": S / "p5d85585a.jpg", "num": "3" + NB + "TESLA", "word": "DÉMONTÉES PAR XIAOMI", "size": 260},
    {"name": "xiaomi_3modely", "src": S / "p39fbd816.jpg", "num": "3" + NB + "MODEL" + NB + "Y", "word": "PIÈCE PAR PIÈCE", "size": 240},
    {"name": "xiaomi_leijun", "src": S / "pc42f19e9.jpg", "num": "3" + NB + "TESLA", "word": "IL L'A AVOUÉ SUR SCÈNE", "size": 260},
    {"name": "xiaomi_704", "src": S / "p555b578a.jpg", "num": "7:04", "word": "PLUS RAPIDE QUE PORSCHE", "size": 300},
    {"name": "xiaomi_240000", "src": S / "p0b42354f.jpg", "num": "240" + NB + "000", "word": "COMMANDES EN 18 HEURES", "size": 240},
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
