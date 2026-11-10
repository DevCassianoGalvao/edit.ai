"""Miniaturas "37.8 Million Fire Extinguishers Were Recalled" (en, 03/11). Números ditos: 37.8 million, seven, twenty minutes."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_ext"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "ext_378", "src": F / "ia_02.jpg", "num": "37.8M", "word": "EXTINGUISHERS RECALLED", "size": 260},
    {"name": "ext_7", "src": F / "ia_10.jpg", "num": "7", "word": "STEPS TO CHECK YOURS", "size": 330},
    {"name": "ext_20", "src": F / "ia_01.jpg", "num": "20", "word": "MINUTES TO CHECK THEM ALL", "size": 300},
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
