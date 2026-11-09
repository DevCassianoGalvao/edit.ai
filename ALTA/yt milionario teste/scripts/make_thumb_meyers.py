"""Miniaturas "Meyers Hof" (de, 01/11). Números ditos: 2100 Menschen, 257 Wohnungen, 1972 gesprengt, sechs Höfe."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_meyers"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "meyers_2100", "src": F / "p04ad7d09.jpg", "num": "2.100", "word": "MENSCHEN · EIN HAUS", "size": 220},
    {"name": "meyers_257", "src": F / "pa75a4f27.jpg", "num": "257", "word": "WOHNUNGEN", "size": 250},
    {"name": "meyers_1972", "src": F / "p6e20a79c.jpg", "num": "1972", "word": "GESPRENGT", "size": 230},
    {"name": "meyers_6", "src": F / "p0f518637.jpg", "num": "6", "word": "HÖFE · EIN GRUNDSTÜCK", "size": 260},
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
