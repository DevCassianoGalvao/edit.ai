"""Miniaturas "12 Meter hohe Wellen und eisige Stürme — Krabbenfischer im Beringmeer" (de). Todo número é dito:
12 Meter (Wellen), über 300 Kilo (Falle leer), minus 12 Grad (Silvester 2019), 50 Minuten (Cache Seel im Wasser),
23 Stunden (Eis auf der Destination)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_bering"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "bering_12meter", "src": S / "p70c426b0.jpg", "num": "12" + NB + "METER", "word": "WELLEN IM BERINGMEER", "size": 250},
    {"name": "bering_300kilo", "src": S / "p9886a63e.jpg", "num": "300" + NB + "KILO", "word": "JEDE FALLE — LEER", "size": 250},
    {"name": "bering_minus12", "src": S / "pf3386c95.jpg", "num": "−12" + NB + "°C", "word": "EIS AUF DEM KUTTER", "size": 270},
    {"name": "bering_50min", "src": S / "p44bd7e52.jpg", "num": "50" + NB + "MINUTEN", "word": "IM EISKALTEN WASSER", "size": 230},
    {"name": "bering_23std", "src": S / "p96bd4b9a.jpg", "num": "23" + NB + "STUNDEN", "word": "EIS SCHLAGEN ODER SINKEN", "size": 230},
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
