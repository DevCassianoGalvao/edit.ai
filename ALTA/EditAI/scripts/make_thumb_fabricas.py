"""Miniaturas "7 Fábricas de Carro Que Fecharam no Brasil" (pt). Todo número é dito: 7 fábricas, 6 de 7 com montadora
chinesa por perto, 757 carros num ano (JLR), 2 só em 2026."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_fabricas"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "fab_7", "src": S / "p33fe28ef.jpg", "num": "7", "word": "FÁBRICAS FECHADAS", "size": 320},
    {"name": "fab_6de7", "src": S / "p55d0da12.jpg", "num": "6" + NB + "DE" + NB + "7", "word": "COM SOMBRA CHINESA", "size": 260},
    {"name": "fab_757", "src": S / "p1589399c.jpg", "num": "757", "word": "CARROS NUM ANO", "size": 300},
    {"name": "fab_2em2026", "src": S / "pb0e2054f.jpg", "num": "2", "word": "SÓ EM 2026", "size": 320},
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
