"""Miniaturas "That Beeping May Not Be the Battery" (en, 03/11). Números ditos: five to seven, seven steps, thirty seconds."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_co"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "co_57", "src": F / "ia_04.jpg", "num": "5-7", "word": "YEARS, THEN IT EXPIRES", "size": 300},
    {"name": "co_7", "src": F / "ia_09.jpg", "num": "7", "word": "STEPS TO CHECK YOUR ALARM", "size": 330},
    {"name": "co_30", "src": F / "ia_02.jpg", "num": "30", "word": "SECONDS BETWEEN BEEPS", "size": 300},
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
