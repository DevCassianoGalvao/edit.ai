"""Miniaturas "Czterdziestka Ptolemeusza" (pl, 20/10). Todo número é dito: 4000 wioślarzy, 7250 ludzi, 130 m, 40, 17 m."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_polo"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "polo_4000", "src": S / "Trireme_Olympias_ac152e.jpg", "num": "4" + NB + "000", "word": "WIOŚLARZY", "size": 260},
    {"name": "polo_7250", "src": S / "The_trireme_Olympias_on_23_February_2019_30a0fc.jpg", "num": "7" + NB + "250", "word": "LUDZI NA OKRĘCIE", "size": 250},
    {"name": "polo_130m", "src": S / "Tessarakonteres_ee1453.jpg", "num": "130" + NB + "M", "word": "Z DREWNA", "size": 260},
    {"name": "polo_40", "src": S / "Model_of_ancient_Athenian_trireme_Museum_of_ancient_Greek_technology_04_a4a4ea.jpg", "num": "40", "word": "CZTERDZIESTKA", "size": 300},
    {"name": "polo_17m", "src": S / "Replica_of_Athenian_trireme_trieres_._Athens_War_Museum_26147f.jpg", "num": "17" + NB + "M", "word": "JEDNO WIOSŁO", "size": 280},
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
