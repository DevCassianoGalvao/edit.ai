"""Miniaturas "You Own the Home. Someone Else Controls the Repo." (en, 03/11). Números ditos: 99, 24 dollars, seven."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_repo"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "repo_13800", "src": F / "p533eb573.jpg", "num": "$13,800", "word": "STILL OWED. CAR GONE", "size": 230},
    {"name": "repo_18000", "src": F / "p2dc57fb6.jpg", "num": "$18,000", "word": "AUCTION. $12,000 GAP", "size": 230},
    {"name": "repo_10", "src": F / "p0ed0eb8f.jpg", "num": "10", "word": "STEPS AFTER REPOSSESSION", "size": 330},
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
