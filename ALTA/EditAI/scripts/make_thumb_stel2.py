"""Miniaturas "Stellantis Tonie" (pl, 11/10). Todo número é dito: 22,3 mld € de prejuízo, 430 000 carros sem comprador,
36,5 mln € do Tavares, 233 Chargers elétricos no 3º trimestre, ~740 empregos em Tychy."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_stel2"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "stel2_22mld", "src": S / "Carlos_Tavares_2_Genf_2018_3e28c4.jpg", "num": "22,3" + NB + "MLD" + NB + "€", "word": "STRATY", "size": 230},
    {"name": "stel2_430tys", "src": S / "Jeep_Grand_Cherokee_L_1X7A7469_61bf5d.jpg", "num": "430" + NB + "000", "word": "AUT BEZ KUPCA", "size": 250},
    {"name": "stel2_36mln", "src": S / "Carlos_Tavares_Stellantis_NAIAS_2022_c210f4.jpg", "num": "36,5" + NB + "MLN" + NB + "€", "word": "DLA PREZESA", "size": 220},
    {"name": "stel2_233", "src": S / "2024_Dodge_Charger_Daytona_RT_front_4.14.25_11a76e.jpg", "num": "233", "word": "ELEKTRYCZNE CHARGERY", "size": 270},
    {"name": "stel2_tychy", "src": S / "2023_Jeep_Avenger_First_Edition_Auto_1bb7ac.jpg", "num": "740", "word": "MIEJSC PRACY · TYCHY", "size": 250},
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
