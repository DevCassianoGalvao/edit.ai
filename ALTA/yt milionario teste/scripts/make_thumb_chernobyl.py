"""Five thumbnails for "The People Who Still Work Inside Chernobyl" (en). Every number is spoken in the narration:
3,000 people; 40 years; 36,000 tonnes (the arch); 15 days inside / 15 outside; more than 160 villages.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_chernobyl"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "cz_3000", "src": S / "pf58d488a.jpg", "num": "3,000", "word": "STILL WORK HERE", "size": 250},
    {"name": "cz_40years", "src": S / "p38d0ff7b.jpg", "num": "40 YEARS", "word": "NOT EMPTY", "size": 240},
    {"name": "cz_36000t", "src": S / "pb6b78d92.jpg", "num": "36,000 T", "word": "STEEL ARCH", "size": 230},
    {"name": "cz_1515", "src": S / "pc1f06d5a.jpg", "num": "15 DAYS", "word": "INSIDE", "size": 250},
    {"name": "cz_160", "src": S / "pdc948ee1.jpg", "num": "160", "word": "VILLAGES GONE", "size": 260},
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
