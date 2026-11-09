"""Miniaturas "La Ville Cachée Que Personne Ne Voit" (fr). Todo número é dito: 2 350 marins, quatre ponts,
1 175 cabines, 72 heures par semaine, 83 pays."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_iconfr"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "iconfr_2350marins", "src": S / "Icon_of_the_Seas_0784d5.jpg", "num": "2" + NB + "350" + NB + "MARINS", "word": "LA VILLE CACHÉE", "size": 220},
    {"name": "iconfr_4ponts", "src": S / "Lower_Aft_Icon_of_the_Seas_2024_39d943.jpg", "num": "4" + NB + "PONTS", "word": "INTERDITS AUX PASSAGERS", "size": 270},
    {"name": "iconfr_1175cabines", "src": S / "Britannia_-_Mannschafts-Schlafraum_a7ed88.jpg", "num": "1" + NB + "175" + NB + "CABINES", "word": "SANS HUBLOT", "size": 220},
    {"name": "iconfr_72heures", "src": S / "Britannia_s_soldiers_cabin_6213609295__030390.jpg", "num": "72" + NB + "HEURES", "word": "PAR SEMAINE · LÉGAL", "size": 260},
    {"name": "iconfr_83pays", "src": S / "Thrill_Island_Icon_of_the_Seas_2024_873bec.jpg", "num": "83" + NB + "PAYS", "word": "SOUS LES TOBOGGANS", "size": 270},
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
