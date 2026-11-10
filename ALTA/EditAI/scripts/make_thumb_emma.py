"""Miniaturas "Enfermés des Mois Avec le Plus Gros Moteur du Monde" (fr, 21/10). Todo número é dito: 2 300 tonnes,
14 cylindres, 13 personnes, 110 décibels, 397 mètres. Fotos do Commons (Emma Mærsk, motor naval)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_emma"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "emma_2300", "src": g("M_V_AGELOS_PROTOSTATIS_Main_Engine*.jpg", "Hyundai_ship_engine_crankshaft*.jpg"), "num": f"2{NB}300{NB}T", "word": "D'ACIER", "size": 240},
    {"name": "emma_14", "src": g("Hyundai_ship_engine_crankshaft*.jpg"), "num": "14 CYLINDRES", "word": "UN HOMME DEBOUT DEDANS", "size": 200},
    {"name": "emma_13", "src": g("Emma_Maersk_ship_2006_IMO_9321483_Schelde_Port_of_Antwerp_pic1*.jpg", "Emma_M_rsk_2*.jpg"), "num": "13 HOMMES", "word": "ENFERMÉS DES MOIS", "size": 230},
    {"name": "emma_110", "src": g("Engine_Control_Room_3331126962*.jpg", "M_V_AGELOS_PROTOSTATIS_Main_Engine*.jpg"), "num": f"110{NB}dB", "word": "PENDANT DES MOIS", "size": 260},
    {"name": "emma_397", "src": g("Emma_Maersk_IMO_9321483_C_Hamburg_28-09-2023_1*.jpg", "Emma_M_rsk_3*.jpg"), "num": f"397{NB}M", "word": "LE GÉANT DE MAERSK", "size": 260},
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
