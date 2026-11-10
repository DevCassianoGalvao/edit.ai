"""Miniaturas "5 Biggest Port Machines" (en, 30/10). Todo número é dito: 48,000 tonnes, 14,200 tonnes, 95 tonnes, 400 m."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_port"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "port_48000", "src": F / "p117f1aa5.jpg", "num": f"48,000{NB}TONNES", "word": "ONE SINGLE LIFT", "size": 190},
    {"name": "port_14200", "src": F / "p392e3bec.jpg", "num": f"14,200{NB}TONNES", "word": "TWO CRANES AT SEA", "size": 190},
    {"name": "port_95", "src": F / "p38b6ca32.jpg", "num": f"95{NB}TONNES", "word": "A TUG THAT PULLS A SHIP", "size": 230},
    {"name": "port_400", "src": F / "p061db4bb.jpg", "num": f"400{NB}METRES", "word": "LOOKS TINY", "size": 230},
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
