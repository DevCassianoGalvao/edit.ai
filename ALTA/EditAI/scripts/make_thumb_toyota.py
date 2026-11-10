"""Miniaturas "A Toyota desmontou 4 carros da BYD" (pt). Todo número é dito: 4 carros, 8 em 1, 8 horas, 1995."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_toyota"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "toyota_4carros", "src": S / "p9b7a0a37.jpg", "num": "4" + NB + "CARROS", "word": "A TOYOTA DESMONTOU", "size": 260},
    {"name": "toyota_8em1", "src": S / "p12f4c0f6.jpg", "num": "8" + NB + "EM" + NB + "1", "word": "O QUE A TOYOTA ACHOU", "size": 260},
    {"name": "toyota_8horas", "src": S / "p48719a9b.jpg", "num": "8" + NB + "HORAS", "word": "PRA ABRIR A BATERIA", "size": 250},
    {"name": "toyota_1995", "src": S / "p7b6c981f.jpg", "num": "1995", "word": "O ALUNO VIROU MESTRE", "size": 300},
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
