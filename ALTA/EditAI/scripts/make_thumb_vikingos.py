"""Cinco miniaturas "La granja vikinga bajo la arena" (es, painel 20260929-231437). Todo número é dito na narração:
1990 (mil novecientos noventa), más de seiscientos años, trescientos años, 25 barcos / 14 llegaron, 1408."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_vikingos"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "vikingos_600", "src": S / "p3a8fb3c5.jpg", "num": "600 AÑOS", "word": "BAJO LA ARENA", "size": 250},
    {"name": "vikingos_1990", "src": S / "p2904b8e5.jpg", "num": "1990", "word": "LA GRANJA QUE NO DEBÍA EXISTIR", "size": 300},
    {"name": "vikingos_300", "src": S / "pb754b875.jpg", "num": "300 AÑOS", "word": "AL BORDE DEL HIELO", "size": 250},
    {"name": "vikingos_14", "src": S / "p37bc1df2.jpg", "num": "14 DE 25", "word": "BARCOS LLEGARON", "size": 250},
    {"name": "vikingos_1408", "src": S / "p477b0b43.jpg", "num": "1408", "word": "LA ÚLTIMA NOTICIA", "size": 300},
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
