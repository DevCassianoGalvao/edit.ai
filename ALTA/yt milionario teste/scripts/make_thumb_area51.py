"""Miniaturas "What Lies Under Area 51" (en, 01/11). Números ditos: 2 miles, 828 tests, 58 years, 10,560 feet."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_area51"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "area51_2miles", "src": F / "p83031cfe.jpg", "num": f"2{NB}MILES", "word": "BENEATH AREA 51", "size": 230},
    {"name": "area51_828", "src": F / "p33c74cd9.jpg", "num": f"828{NB}TESTS", "word": "UNDER THE DESERT", "size": 230},
    {"name": "area51_58", "src": F / "pb8ddbc53.jpg", "num": f"58{NB}YEARS", "word": "OF SILENCE", "size": 230},
    {"name": "area51_10560", "src": F / "p4512a5b9.jpg", "num": f"10,560{NB}FEET", "word": "STRAIGHT DOWN", "size": 190},
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
