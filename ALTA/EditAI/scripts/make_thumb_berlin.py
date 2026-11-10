"""Miniaturas "Berliner Arbeiterfamilien vermieteten Betten stundenweise" (de, 29/10). Números ditos: mehr als 100.000 Schlafgänger, 1908, 17 Mark im Monat, 2.000 Bewohner (Meyers Hof)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_berlin"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "berlin_100000", "src": F / "p0d5dad77.jpg", "num": "100.000", "word": "FREMDE BETTEN", "size": 220},
    {"name": "berlin_1908", "src": F / "pf0df343f.jpg", "num": "1908", "word": "DAS ERSTE LEDIGENHEIM", "size": 220},
    {"name": "berlin_17", "src": F / "p542ff124.jpg", "num": "17", "word": "MARK IM MONAT", "size": 250},
    {"name": "berlin_2000", "src": F / "p602f66f2.jpg", "num": "2.000", "word": "MENSCHEN · EIN HAUS", "size": 220},
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
