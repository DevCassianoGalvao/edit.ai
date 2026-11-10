"""Miniaturas "BMW contre Zeekr 001" (fr, 04/11). Todo número é dito: 001, -40 %, 7 terres rares, 200 kW, 2035.
Fotos do Commons (Zeekr 001, BMW iX, BMW iX3 NA5, moteur coupé, terres rares)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_bmwz"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "bmwz_001", "src": g("Zeekr_001_004_*.jpg"), "num": "001", "word": "BMW CONTRE ZEEKR", "size": 300},
    {"name": "bmwz_40", "src": g("BMW_I20_iX_xDrive50_Sport_Mineral_White_Metallic_2__*.jpg"), "num": f"−40{NB}%", "word": "LE MOTEUR SANS AIMANTS", "size": 260},
    {"name": "bmwz_7", "src": g("Rare_earth_minerals_1_*.jpg"), "num": "7", "word": "TERRES RARES BLOQUÉES", "size": 320},
    {"name": "bmwz_200", "src": g("Cut-away_version_of_an_electric_motor_1__*.jpg"), "num": f"200{NB}KW", "word": "UN CŒUR JAPONAIS", "size": 240},
    {"name": "bmwz_2035", "src": g("BMW_iX3_50_IAA_Summit_2025_Munich_P1049826_*.jpg"), "num": "2035", "word": "L'EUROPE SANS AIMANTS ?", "size": 260},
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
