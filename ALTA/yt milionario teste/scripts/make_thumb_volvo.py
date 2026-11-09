"""Miniaturas "Volvo Traci Wszystko" (pl, 27/10). Todo número é dito: 3000 zwolnień, 2500 (druga fala), 11,4 mld koron (odpis),
5500 (razem). Fotos do Commons (Volvo EX90 / EX30 / Samuelsson)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_volvo"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "volvo_3000", "src": g("Volvo_EX90_Auto_Zuerich_2024_DSC_6757*.jpg"), "num": f"3{NB}000", "word": "ZWOLNIEŃ W VOLVO", "size": 260},
    {"name": "volvo_2500", "src": g("Volvo_EX90_DSC_7859*.jpg"), "num": f"2{NB}500", "word": "KOLEJNYCH ZWOLNIEŃ", "size": 240},
    {"name": "volvo_11mld", "src": g("2024_Volvo_EX30_Front*.jpg"), "num": "11,4 MLD", "word": "ODPISU NA ELEKTRYKACH", "size": 190},
    {"name": "volvo_5500", "src": g("Volvo_EX90_autoMOBIL_T_bingen_2025_DSC_2740*.jpg"), "num": f"5{NB}500", "word": "LUDZI STRACIŁO PRACĘ", "size": 220},
    {"name": "volvo_prezes", "src": g("Hakan_Samuelsson_at_COTY_2018_Le_Grand-Saconnex_1X7A9423*.jpg"), "num": "3 000", "word": "TO TYLKO ROZGRZEWKA", "size": 200},
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
