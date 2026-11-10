"""Miniaturas "Inside the Cab of Big Boy 4014" (en). Todo número é dito na narração: 1 de 25 (twenty-five built,
only one still breathes fire), 17 sucateadas, 8,013 ft (cume de Sherman Hill), 1,031,205 milhas, 4014.
Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_bigboy"
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
    {"name": "bb4014_1de25", "src": foto("File:UP 4014 Yoder Sub Egbert WY.jpg"), "num": "1" + NB + "OF" + NB + "25", "word": "STILL BREATHES FIRE", "size": 220},
    {"name": "bb4014_17", "src": foto("File:Union Pacific Big Boy 4014 Departs Granger, WY May 6th, 2019.jpg"), "num": "17", "word": "CUT FOR SCRAP", "size": 240},
    {"name": "bb4014_8013", "src": foto("File:UP 4014 Unassisted On Wasatch Grade.jpg"), "num": "8,013" + NB + "FT", "word": "THE CLIMB", "size": 220},
    {"name": "bb4014_milhas", "src": foto("File:4014 Accelerates East From Gering NE.jpg"), "num": "1,031,205", "word": "MILES", "size": 210},
    {"name": "bb4014_4014", "src": foto("File:Big Boy 4014 In Operation.jpg"), "num": "4014", "word": "THE LAST GIANT", "size": 240},
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
