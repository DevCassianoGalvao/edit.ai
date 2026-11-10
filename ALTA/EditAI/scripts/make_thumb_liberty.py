"""Miniaturas "Every Job Aboard a WWII Liberty Ship" (en, 28/10). Todo número é dito: 2,700 ships, 1 in 26, 130 degrees,
56 days, number 12 (12 jobs). Fotos do Commons (Liberty ship at sea, Atlantic convoy 1942, Richmond shipyards, R. P. Resor burning)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_liberty"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "lib_2700", "src": g("Liberty_ship_at_sea*.jpg"), "num": f"2,700", "word": "LIBERTY SHIPS", "size": 230},
    {"name": "lib_1in26", "src": g("Atlantic_convoy_in_1942*.jpg"), "num": "1 IN 26", "word": "SEAMEN LOST", "size": 210},
    {"name": "lib_130", "src": g("US_Navy_090214-N-2636M-052*.jpg"), "num": "130°", "word": "IN THE BOILER ROOM", "size": 220},
    {"name": "lib_56days", "src": g("Wendy_Welder_Richmond_Shipyards*.jpg"), "num": "56", "word": "DAYS TO BUILD ONE", "size": 230},
    {"name": "lib_12jobs", "src": g("R._P._Resor_burning*.jpg"), "num": "12", "word": "JOBS RANKED", "size": 240},
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
