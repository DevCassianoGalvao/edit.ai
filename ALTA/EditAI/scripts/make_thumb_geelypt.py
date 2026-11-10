"""Cinco miniaturas de "O motor a gasolina chinês que ameaça o carro elétrico" (pt). Todo número é DITO na narração:
48,41 %; 45 km/l; 2,22 litros (Guinness); 230 kW; 76,5 % ainda a combustão.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_geelypt"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "gpt_4841", "src": S / "p7387b6fa.jpg", "num": "48,41%", "word": "MOTOR CHINÊS", "size": 250},
    {"name": "gpt_45kml", "src": S / "p86422206.jpg", "num": "45 KM/L", "word": "GASOLINA", "size": 240},
    {"name": "gpt_222", "src": S / "pfd7e7284.jpg", "num": "2,22 L", "word": "RECORDE", "size": 260},
    {"name": "gpt_230kw", "src": S / "pc44a3798.jpg", "num": "230 KW", "word": "HÍBRIDO", "size": 250},
    {"name": "gpt_765", "src": S / "p7c58483d.jpg", "num": "76,5%", "word": "AINDA A GASOLINA", "size": 240},
]


def main():
    outs = [make(s) for s in SPECS]
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
