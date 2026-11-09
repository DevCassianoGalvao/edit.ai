"""Miniaturas "Musk riu da BYD" (pt). Todo número é dito: 2011, 8 em 1,
US$ 10 mil, 4 milhões."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_bydpt"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "bydpt_2011", "src": S / "pacf21aff.jpg", "num": "2011", "word": "MUSK RIU DA BYD", "size": 300},
    {"name": "bydpt_8em1", "src": S / "p24e8f0a0.jpg", "num": "8" + NB + "EM" + NB + "1", "word": "O QUE ACHARAM DENTRO", "size": 260},
    {"name": "bydpt_10mil", "src": S / "pb82c4b4f.jpg", "num": "US$" + NB + "10" + NB + "MIL", "word": "UM ELÉTRICO NOVO", "size": 230},
    {"name": "bydpt_4mi", "src": S / "p07ac7685.jpg", "num": "4" + NB + "MILHÕES", "word": "A TESLA FICOU PRA TRÁS", "size": 240},
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
