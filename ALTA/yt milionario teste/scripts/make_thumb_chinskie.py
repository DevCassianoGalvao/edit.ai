"""Miniaturas "Tysiące Polaków Kupiło BYD lub MG" (pl, 28/10). Todo número é dito: 49 161 (chińskie marki), 8 lat (BYD),
15 229 (MG), 44,7 % (BYD po 4 latach), 98 900 zł (hybryda). Fotos do Commons (Seal U, MG HS, Dolphin Surf, Jaecoo)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_chinskie"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "chin_49161", "src": g("2024_MG_HS_5_*.jpg"), "num": f"49{NB}161", "word": "CHIŃSKICH AUT W POLSCE", "size": 230},
    {"name": "chin_8lat", "src": g("BYD_Seal_U_DM-i_2025_54522011110__*.jpg"), "num": "8 LAT", "word": "GWARANCJI. ALE NIE U WSZYSTKICH", "size": 230},
    {"name": "chin_15229", "src": g("2023_MG_HS_1X7A2509_*.jpg"), "num": f"15{NB}229", "word": "AUT MG W JEDEN ROK", "size": 230},
    {"name": "chin_447", "src": g("BYD_Dolphin_Surf_IAA_2025_DSC_2031_*.jpg"), "num": "44,7%", "word": "WARTOŚCI PO 4 LATACH", "size": 240},
    {"name": "chin_98900", "src": g("2024_MG_ZS_1.5_Alpha_in_Extreme_Speed_Red_front_left_*.jpg"), "num": f"98{NB}900 ZŁ", "word": "ZA HYBRYDĘ MG ZS", "size": 200},
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
