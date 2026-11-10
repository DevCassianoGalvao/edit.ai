"""Miniaturas "Ryzykują Życie dla Fortuny: Łowcy Krabów na Morzu Beringa" (pl). Todo número é dito:
ponad 300 kg (klatka pusta), 10 miliardów (kraby śnieżne), 150 ton lodu (Destination), 770 zgonów (lata 90.),
sześciu mężczyzn (Destination, nikt nie wrócił)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_kraby"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "kraby_300kg", "src": S / "Odin_King_Crab_Pots_11_6cc3dd.jpg", "num": "300" + NB + "KG", "word": "STALI W JEDNEJ KLATCE", "size": 250},
    {"name": "kraby_10mld", "src": S / "Blue_Chionoecetes_opilio_5a545f.jpg", "num": "10" + NB + "MLD", "word": "KRABÓW ZNIKNĘŁO", "size": 250},
    {"name": "kraby_150ton", "src": S / "Steamer_Resolute_coated_with_ice_64f3a1.jpg", "num": "150" + NB + "TON", "word": "LODU NA STATKU", "size": 250},
    {"name": "kraby_770", "src": ROOT.parent / "banco" / "ak_welle" / "US_Navy_061201-N-6423H-005_The_crew_of_the_fishing_vessel_Miss_Melissa_await_rescue_from_a_70c426.jpg", "num": "770", "word": "ZGONÓW · LATA 90.", "size": 270},
    {"name": "kraby_6", "src": S / "Dutch_harbor_crab_boats_56bd9c.jpg", "num": "6", "word": "NIGDY NIE WRÓCIŁO", "size": 290},
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
