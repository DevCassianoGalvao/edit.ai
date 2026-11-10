"""Cinco miniaturas "Revendas de máquinas agrícolas no vermelho" (pt). Todo número é dito na narração:
dívida de 600 milhões; 1.263 produtores; 2 % do crédito; queda de 25,8 %; prejuízo de 87,5 milhões.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_rev"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "rev_600m", "src": S / "pd181f781.jpg", "num": "R$ 600 MI", "word": "DÍVIDA NA REVENDA", "size": 230},
    {"name": "rev_1263", "src": S / "pca21b11a.jpg", "num": "1.263", "word": "PRODUTORES NA JUSTIÇA", "size": 270},
    {"name": "rev_2pct", "src": S / "p7e4adbe8.jpg", "num": "2%", "word": "PARA COMPRAR MÁQUINA", "size": 320},
    {"name": "rev_25", "src": S / "pe6b0e6c5.jpg", "num": "-25,8%", "word": "MÁQUINAS AGRÍCOLAS", "size": 240},
    {"name": "rev_87m", "src": S / "p23c095b3.jpg", "num": "R$ 87 MI", "word": "DE PREJUÍZO", "size": 250},
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
