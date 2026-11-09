"""Miniaturas "What Lies Under Loch Ness" (en, 31/10). Números ditos: 230 m, 160 km, 250 lugares, 10,000 anos."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_loch"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "loch_230", "src": F / "p0413463f.jpg", "num": f"230{NB}METERS", "word": "DOWN IN LOCH NESS", "size": 230},
    {"name": "loch_160", "src": F / "p500f7b10.jpg", "num": f"160{NB}KM", "word": "SCOTLAND TORN IN TWO", "size": 230},
    {"name": "loch_250", "src": F / "p07ed7ff3.jpg", "num": f"250{NB}PLACES", "word": "NO MONSTER FOUND", "size": 230},
    {"name": "loch_10000", "src": F / "p2d361230.jpg", "num": f"10,000{NB}YEARS", "word": "THE REAL MONSTER", "size": 190},
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
