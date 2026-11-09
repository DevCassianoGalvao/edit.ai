"""Miniaturas "Bis 1893 hatte jede deutsche Stadt ihre eigene Uhrzeit" (de, 29/10). Todo número é dito: 67 Minuten, 1893,
26 Minuten (Karlsruhe), 20 Minuten (zwischen den Bahnzeiten). Fotos já aprovadas (Commons/Pexels) em public/stock."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_uhr"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "uhr_67", "src": F / "pdbf4382b.jpg", "num": "67", "word": "MINUTEN UNTERSCHIED", "size": 250},
    {"name": "uhr_1893", "src": F / "p76258a79.jpg", "num": "1893", "word": "EINE UHR FÜRS REICH", "size": 220},
    {"name": "uhr_26", "src": F / "p1f17943d.jpg", "num": "26", "word": "MINUTEN VORAUS", "size": 250},
    {"name": "uhr_20", "src": F / "pf103c0fd.jpg", "num": "20", "word": "MINUTEN ZWISCHEN BAHNEN", "size": 250},
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
