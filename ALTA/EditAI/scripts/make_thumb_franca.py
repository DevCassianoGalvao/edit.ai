"""Miniatures "La France Ouvre ses Portes à BYD" (fr). Todo número é dito: huit pour cent, 19 990 euros, 400 kilos,
un seul essuie-glace, +136 %. Fotos do Commons."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_franca"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "frbyd_8pc", "src": F / "BYD_Dolphin_Surf_IAA_2025_DSC_2032_105793.jpg", "num": "8" + NB + "%", "word": "DU MARCHÉ FRANÇAIS", "size": 300},
    {"name": "frbyd_19990", "src": F / "BYD_Dolphin_Surf_IMG_3802_f951c5.jpg", "num": "19" + NB + "990" + NB + "€", "word": "LA BYD DÉMONTÉE", "size": 200},
    {"name": "frbyd_400kg", "src": F / "2023_BYD_Seagull_front__587566.jpg", "num": "−400" + NB + "KG", "word": "ILS L'ONT DÉMONTÉE", "size": 230},
    {"name": "frbyd_1essuie", "src": F / "BYD_Dolphin_Surf_IMG_3880_b9ed02.jpg", "num": "1", "word": "SEUL ESSUIE-GLACE", "size": 320},
    {"name": "frbyd_136", "src": F / "2025_BYD_Seagull_EV_in_Sprout_Green_front_left_70f0c2.jpg", "num": "+136" + NB + "%", "word": "BYD EN FRANCE", "size": 230},
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
