"""Miniaturas "Australia's New Invention Turns Old Mattresses and Glass Into Tiles" (en). Todo número é dito:
740,000 mattresses still buried, 67 million tonnes to landfill, 80 % recycled (tiles), 2 million tyres, 700 tonnes a year.
Fotos do Wikimedia Commons (licença livre, crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_veena"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    f = POOL[titulo].get("file")
    p = Path(f) if f else None
    if not p or not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {titulo}")
    return p


SPECS = [
    {"name": "veena_740k", "src": foto("File:28 May 2018. Dumped mattresses Park View Road (28554528668).jpg"), "num": "740,000", "word": "MATTRESSES BURIED", "size": 220},
    {"name": "veena_67mi", "src": foto("File:Tana E520 landfill compactor.jpg"), "num": "67" + NB + "MILLION", "word": "TONNES OF WASTE", "size": 200},
    {"name": "veena_80pct", "src": foto("File:Terrazzo Wernerit.jpeg"), "num": "80%", "word": "RECYCLED TILES", "size": 260},
    {"name": "veena_2mi", "src": foto("File:1993-06-19 - aerial - MIDDLETON - Tire Pile - 002.jpg"), "num": "2" + NB + "MILLION", "word": "TYRES INSTEAD OF COAL", "size": 210},
    {"name": "veena_700t", "src": foto("File:Crushed glass pieces for glass bead production.jpg"), "num": "700" + NB + "TONNES", "word": "GLASS AND MATTRESSES", "size": 200},
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
