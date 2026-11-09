"""Miniaturas "Brise-glace nucléaire à 1 milliard $" (fr). Todo número é dito: un milliard de dollars, trois mètres,
trente-trois mille tonnes, deux réacteurs / sept ans, moteur de trois cents tonnes. Fotos do Wikimedia Commons (crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_glace"
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
    {"name": "glace_1milliard", "src": foto("File:Арктика в доке им. Велещинского.jpg"), "num": "1" + NB + "MILLIARD" + NB + "$", "word": "BRISE-GLACE NUCLÉAIRE", "size": 190},
    {"name": "glace_3metres", "src": foto("File:50letPob pole.JPG"), "num": "3" + NB + "MÈTRES", "word": "DE GLACE DEVANT LUI", "size": 250},
    {"name": "glace_33000t", "src": foto('File:Rosatomflot icebreaker "50 Years of Victory".jpg'), "num": "33" + NB + "000" + NB + "T", "word": "IL MONTE SUR LA GLACE", "size": 230},
    {"name": "glace_2reacteurs", "src": foto('File:Ледокол "Урал" (проект 22220).jpg'), "num": "2" + NB + "RÉACTEURS", "word": "7 ANS SANS LE PLEIN", "size": 210},
    {"name": "glace_300t", "src": foto("File:С вертолета-2.JPG"), "num": "300" + NB + "TONNES", "word": "LE MOTEUR A GRILLÉ", "size": 220},
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
