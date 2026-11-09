"""Miniaturas "The Day the Gauge Changed" (en). Todo número é dito na narração: 11,500 miles, 36 hours, 3 inches,
8,000 men (L&N), 1886. Fotos Wikimedia Commons/LOC (licença livre, créditos no LEIA-ME)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_gauge"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def foto(cid):
    p = ROOT / "public" / "stock" / f"{cid}.jpg"
    if not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {p}")
    return p


SPECS = [
    {"name": "gauge_11500", "src": foto("p018747cf"), "num": "11,500" + NB + "MILES", "word": "IN 36 HOURS", "size": 200},
    {"name": "gauge_36h", "src": foto("p09c9ac87"), "num": "36" + NB + "HOURS", "word": "THE GAUGE CHANGED", "size": 230},
    {"name": "gauge_3in", "src": foto("p0fa95be7"), "num": "3" + NB + "INCHES", "word": "ONE RAIL MOVED", "size": 230},
    {"name": "gauge_8000", "src": foto("p16dd2097"), "num": "8,000" + NB + "MEN", "word": "ONE DAY", "size": 220},
    {"name": "gauge_1886", "src": foto("p5bb6c78b"), "num": "1886", "word": "THE SOUTH CHANGED GAUGE", "size": 240},
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
