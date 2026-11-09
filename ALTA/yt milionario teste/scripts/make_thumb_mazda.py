"""Miniaturas "Mazda Rzuca BOMBĘ — Nowy Silnik Skyactiv-Z" (pl, 24/10). Todo número é dito: 2027, 30 %, 2500, 56 %, 7 (Euro 7)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_mazda"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "mazda_2027", "src": g("2026_Mazda_CX-5_e-SKYACTIV_G_2.5_engine_*.jpg"), "num": "2027", "word": "MAZDA RZUCA BOMBĘ", "size": 280},
    {"name": "mazda_30", "src": g("Geneva_MotorShow_2013_-_Mazda_Skyactiv-G2.5L_engine_*.jpg"), "num": f"-30{NB}%", "word": "MOCY PRZEZ EURO 7", "size": 260},
    {"name": "mazda_2500", "src": g("Mazda_CX-5_KI_Auto_Zuerich_2025_DSC_3145_*.jpg"), "num": "2500", "word": "ZAMÓWIEŃ W CIEMNO", "size": 270},
    {"name": "mazda_56", "src": g("Mazda3_BP_X_E-Skyactiv-X_1X7A2480_*.jpg"), "num": f"56{NB}%", "word": "SPRAWNOŚCI — CEL MAZDY", "size": 260},
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
