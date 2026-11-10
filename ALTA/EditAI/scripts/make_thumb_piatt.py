"""Miniaturas "Cosa Mangiano gli Operai Chiusi 28 Giorni su una Piattaforma" (it, 22/10). Todo número é dito: 28 giorni,
600 pasti, 16.800 pasti, 99 chili, onde di 6 metri. Fotos do Commons/Pexels aprovadas no filme."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_piatt"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat)) or sorted((ROOT / "assets" / "banco").glob(pat)) or sorted((ROOT.parent / "banco").rglob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "piatt_28giorni", "src": g("Marco_Polo_at_Dusk*.jpg", "Holstein_at_Dusk*.jpg"), "num": "28 GIORNI", "word": "IN MEZZO AL MARE", "size": 230},
    {"name": "piatt_600pasti", "src": g("Pexels_12193823_*.jpg", "Cruise_Ship_Kitchen_*.jpg"), "num": "600 PASTI", "word": "OGNI GIORNO", "size": 240},
    {"name": "piatt_16800", "src": g("Hot_food_section_in_cruise_ship_buffet*.jpg", "Buffet_2973165044*.jpg"), "num": "16.800 PASTI", "word": "IN 28 GIORNI", "size": 210},
    {"name": "piatt_99kg", "src": g("Tomahawk_steaks_on_the_grill*.jpg", "Grilling_Steaks*.jpg"), "num": f"99{NB}KG", "word": "IL PREZZO DELLA MENSA", "size": 260},
    {"name": "piatt_6metri", "src": g("View_from_the_bow_of_the_Fugro_Discovery*.jpg", "Falami.jpg"), "num": f"6{NB}METRI", "word": "E LA DISPENSA SI SVUOTA", "size": 240},
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
