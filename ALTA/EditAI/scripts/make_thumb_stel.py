"""Miniaturas "Stellantis Traci Wszystko" (pl). Todo número é dito: 22,3 mld € de prejuízo, 430 000 carros sem comprador,
80 Chargers elétricos em janeiro, 18,6 mld de lucro, ~740 empregos em Tychy."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_stel"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "stel_22mld", "src": S / "Carlos_Tavares_2_Genf_2018_3e28c4.jpg", "num": "22,3" + NB + "MLD" + NB + "€", "word": "STRATY", "size": 230},
    {"name": "stel_430tys", "src": S / "Jeep_Grand_Cherokee_L_1X7A7469_61bf5d.jpg", "num": "430" + NB + "000", "word": "BEZ KUPCA", "size": 250},
    {"name": "stel_80sztuk", "src": S / "2024_Dodge_Charger_Daytona_RT_front_4.14.25_11a76e.jpg", "num": "80" + NB + "SZTUK", "word": "W MIESIĄC", "size": 250},
    {"name": "stel_hemi", "src": S / "2023_Ram_1500_HEMI_05c353.jpg", "num": "18,6" + NB + "MLD", "word": "ZYSKU → STRATA", "size": 220},
    {"name": "stel_tychy", "src": S / "2023_Jeep_Avenger_First_Edition_Auto_1bb7ac.jpg", "num": "740", "word": "MIEJSC PRACY · TYCHY", "size": 250},
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
