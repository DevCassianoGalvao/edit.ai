"""Miniaturas "Navio-cegonha: 8 mil carros sem arranhar" (pt). Todo número é dito: 8 mil, 10 centímetros,
60 graus (Cougar Ace), 4.200 veículos (Golden Ray)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_cegonha"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "cegonha_8mil", "src": S / "p11a9b6a2.jpg", "num": "8" + NB + "MIL", "word": "CARROS SEM UM RISCO", "size": 300},
    {"name": "cegonha_10cm", "src": S / "p6016e325.jpg", "num": "10" + NB + "CM", "word": "ENTRE UM CARRO E OUTRO", "size": 300},
    {"name": "cegonha_60graus", "src": S / "p20ea177b.jpg", "num": "60°", "word": "E AS CINTAS SEGURARAM", "size": 300},
    {"name": "cegonha_4200", "src": S / "p3e69b7e2.jpg", "num": "4.200", "word": "VEÍCULOS NUM NAVIO TOMBADO", "size": 280},
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
