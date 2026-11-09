"""Miniaturas "Icon of the Seas — pływające miasto" (pl, painel 20261004-153813). Todo número é dito na narração:
dziesięć tysięcy ludzi, trzysta sześćdziesiąt pięć metrów, dwa miliardy dolarów, dwadzieścia pokładów."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_icon"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "icon_10tys", "src": S / "p0784d5f3.jpg", "num": "10" + NB + "000", "word": "LUDZI W" + NB + "JEDNYM KADŁUBIE", "size": 300},
    {"name": "icon_365m", "src": S / "p256f44b0.jpg", "num": "365" + NB + "M", "word": "PŁYWAJĄCE MIASTO", "size": 300},
    {"name": "icon_2mld", "src": S / "p39d943f3.jpg", "num": "2" + NB + "MLD" + NB + "$", "word": "ILE KOSZTUJE TO MIASTO", "size": 260},
    {"name": "icon_20", "src": S / "p0759f012.jpg", "num": "20" + NB + "POKŁADÓW", "word": "I" + NB + "ŻADNEGO LĄDU", "size": 230},
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
