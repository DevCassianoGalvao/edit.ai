"""Five thumbnails "Canada's German submarines" (en). Every number is spoken in the narration:
up to 12 submarines; 60 billion Canadian dollars; 1985 Polar Sea; 14,000 km voyage; a single working submarine ("one").
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_subca"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "subca_12", "src": S / "p7db5486e.jpg", "num": "12", "word": "GERMAN SUBMARINES", "size": 300},
    {"name": "subca_60b", "src": S / "pf1f87943.jpg", "num": "$60 BILLION", "word": "SUBMARINE DEAL", "size": 210},
    {"name": "subca_1985", "src": S / "p1e9c7c1b.jpg", "num": "1985", "word": "THE ARCTIC INSULT", "size": 260},
    {"name": "subca_14000", "src": S / "p8799a6d6.jpg", "num": "14,000 KM", "word": "TO LOSE", "size": 220},
    {"name": "subca_1", "src": S / "p201f9481.jpg", "num": "1", "word": "WORKING SUBMARINE", "size": 320},
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
