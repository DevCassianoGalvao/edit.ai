"""Miniaturas "7 Samochodów Elektrycznych" (pl, 27/10). Todo número é dito: 2760, 15 lat, 11 201, 3 akcje."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_ev"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "ev_2760", "src": g("2018_Jaguar_I-Pace_EV400_AWD_Front_*.jpg"), "num": f"2{NB}760", "word": "AUT ODKUPIONYCH PRZEZ JAGUARA", "size": 270},
    {"name": "ev_15", "src": g("2021_Hyundai_Ioniq_5_Premium_Standard_Range_2WD_Front__*.jpg"), "num": f"15{NB}LAT", "word": "GWARANCJI NA JEDEN ELEMENT", "size": 250},
    {"name": "ev_11201", "src": g("2023_Fisker_Ocean_a2b5dd.jpg"), "num": f"11{NB}201", "word": "AUT BEZ PRODUCENTA", "size": 260},
    {"name": "ev_3", "src": g("2021_Ford_Mustang_Mach-E_GT_22d273.jpg"), "num": "3", "word": "AKCJE NA TEN SAM PODZESPÓŁ", "size": 300},
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
