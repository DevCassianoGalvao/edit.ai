"""Miniaturas "36 000 Ton Stali nad Reaktorem" (pl). Todo número é dito: 36 000 ton, 108 m, 327 m, 12 minut, 100 lat.
Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_czarnobyl"
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
    {"name": "cz_36000", "src": foto("File:Chernobyl New Safe Confinement.jpg"), "num": "36" + NB + "000" + NB + "TON", "word": "STALI NAD REAKTOREM", "size": 200},
    {"name": "cz_108m", "src": foto("File:Chernobyl second sarcophacus 2018 hnapel 01.jpg"), "num": "108" + NB + "M", "word": "NAD REAKTOREM NR 4", "size": 250},
    {"name": "cz_327m", "src": foto("File:New Safe Confinement at Chernobyl Nuclear Power Plant October 2016 1.jpg"), "num": "327" + NB + "M", "word": "PRZESUNIĘTE W CAŁOŚCI", "size": 250},
    {"name": "cz_12min", "src": foto("File:Chernobyl reactor 4.jpg"), "num": "12" + NB + "MINUT", "word": "I ROCZNA DAWKA", "size": 220},
    {"name": "cz_100lat", "src": foto("File:Chernobyl second sarcophacus 2018 hnapel 05.jpg"), "num": "100" + NB + "LAT", "word": "POD STALOWYM ŁUKIEM", "size": 240},
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
