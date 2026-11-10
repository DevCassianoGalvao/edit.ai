"""Miniaturas "12 Small Problems in Older Homes That Can Turn Into Expensive Repairs" (en, 02/11). Números ditos: twelve,
$25,000 (rewire), $210 (GFCI outlets), 1978 (lead paint), $8,000."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_homes"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "homes_12", "src": F / "pa937f007.jpg", "num": f"12{NB}SMALL", "word": "PROBLEMS · BIG BILLS", "size": 230},
    {"name": "homes_25000", "src": F / "p21bb21d2.jpg", "num": f"$25,000", "word": "FOR OLD WIRING", "size": 200},
    {"name": "homes_1978", "src": F / "p13e51792.jpg", "num": "1978", "word": "LEAD PAINT YEAR", "size": 230},
    {"name": "homes_210", "src": F / "pb9c6cbac.jpg", "num": f"$210", "word": "VS A $25,000 REWIRE", "size": 230},
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
