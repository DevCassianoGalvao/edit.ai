"""Miniaturas \"Des ingénieurs américains ont démonté la BYD à 10 000 €\" (fr). Todo número é dito: 18 990 €, 2 fois,
10 000 dollars, 5 étoiles, un seul essuie-glace. Fotos do Commons."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_seagullfr"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "sgfr_18990", "src": F / "BYD_Dolphin_Surf_IAA_2025_DSC_2032_105793.jpg", "num": "18" + NB + "990" + NB + "€", "word": "EN FRANCE", "size": 200},
    {"name": "sgfr_2x", "src": F / "2025_BYD_Seagull_EV_in_Sprout_Green_front_left_70f0c2.jpg", "num": "2X", "word": "PLUS CHÈRE ICI", "size": 300},
    {"name": "sgfr_10000", "src": F / "BYD_Seagull_EV_2025_4__0334f7.jpg", "num": "10" + NB + "000" + NB + "$", "word": "EN CHINE", "size": 210},
    {"name": "sgfr_5etoiles", "src": F / "BYD_Dolphin_Surf_IMG_3880_b9ed02.jpg", "num": "5", "word": "ÉTOILES EURO NCAP", "size": 320},
    {"name": "sgfr_1essuie", "src": F / "2023_BYD_Seagull_front__587566.jpg", "num": "1", "word": "SEUL ESSUIE-GLACE", "size": 320},
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
