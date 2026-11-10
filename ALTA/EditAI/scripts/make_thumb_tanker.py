"""Miniaturas "Tak Żyją Marynarze na Supertankowcu" (pl). Todo número é dito: 2 milhões de barris, 330 m, 25 osób,
zero ognia, 53 dni. Fotos Wikimedia Commons / Pexels (licença livre)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_tanker"
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
    {"name": "tk_2mln", "src": foto("File:MT Alaskan Navigator at Valdez Marine Terminal (Bow).jpg"), "num": "2 MLN", "word": "BARYŁEK POD STOPAMI", "size": 230},
    {"name": "tk_330", "src": foto('File:Pexels 1036866 Aerial shot of an oil tanker cruising through the ocean, emphasizing maritime tr.jpg'), "num": "330" + NB + "M", "word": "JEDEN BŁĄD I KONIEC", "size": 230},
    {"name": "tk_25", "src": foto("File:MT Alaskan Navigator at Valdez Marine Terminal (Deck).jpg"), "num": "25 OSÓB", "word": "NA CAŁY STATEK", "size": 200},
    {"name": "tk_zero", "src": foto("File:Match flame.jpg"), "num": "ZERO", "word": "OGNIA NA POKŁADZIE", "size": 230},
    {"name": "tk_53", "src": foto('File:Pexels 36563588 A large oil tanker sailing on the ocean with a sunset view..jpg'), "num": "53 DNI", "word": "BEZ PORTU", "size": 220},
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
