"""Miniaturas "Jaguar Chce 650 Tysięcy Złotych" (pl, 12/10). Todo número é dito: 650 tys. zł, 6 rejestracji (sześć),
783 -> 6, 1030 KM, 130 000 £."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_jaguar"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "jag_650tys", "src": S / "Jaguar_Type_00_12_d8020a.jpg", "num": "650" + NB + "000" + NB + "ZŁ", "word": "ZA TO AUTO?", "size": 210},
    {"name": "jag_6aut", "src": S / "Jaguar_Dealership_being_demolished_-_geograph.org.uk_-_4831053_eba4e3.jpg", "num": "6", "word": "SPRZEDANYCH JAGUARÓW", "size": 300},
    {"name": "jag_783do6", "src": S / "Jaguar_Type_00_1_bb9ea3.jpg", "num": "783" + NB + "→" + NB + "6", "word": "JAGUAR ZNIKA", "size": 230},
    {"name": "jag_1030km", "src": S / "Jaguar_Type_00_Side_resized__ef88e9.jpg", "num": "1030" + NB + "KM", "word": "ZA 130 000 FUNTÓW", "size": 230},
    {"name": "jag_130tys", "src": S / "Jaguar_Type_00_5_713771.jpg", "num": "130" + NB + "000" + NB + "£", "word": "PO 6 SPRZEDANYCH", "size": 210},
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
