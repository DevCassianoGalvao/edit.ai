"""Miniaturas "Japońscy inżynierowie sprawdzili chińskie auto" (pl, 01/11). Todo número é dito: 25 % (UBS: Seal taniej),
75 % (komponentów własnych), 350 stron (podręcznik), 6 340 USD (cena), 15 % (taniej niż Tesla Model 3).
Fotos do Commons (BYD Seal)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_sealjp"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "seal_25", "src": g("2024_BYD_Seal_Performance_AWD_in_Aurora_White_01_*.jpg"), "num": f"25{NB}%", "word": "TAŃSZY OD EUROPEJSKICH", "size": 230},
    {"name": "seal_75", "src": g("BYD_Seal_IAA_2023_1X7A0502_*.jpg"), "num": f"75{NB}%", "word": "CZĘŚCI ROBI SAM", "size": 230},
    {"name": "seal_350", "src": g("BYD_SEAL_white_20240303_*.jpg"), "num": f"350{NB}STRON", "word": "O JEDNYM AUCIE", "size": 200},
    {"name": "seal_6340", "src": g("BYD_Seal_005_*.jpg"), "num": f"6{NB}340{NB}$", "word": "ZA PODRĘCZNIK", "size": 210},
    {"name": "seal_15", "src": g("BYD_Seal_EV_03_2023_5874_*.jpg"), "num": f"15{NB}%", "word": "TAŃSZY OD TESLI", "size": 230},
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
