"""Cinco miniaturas de "The nine vans that reach 300,000 miles" (en), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: as 300 mil milhas; as nove vans; 1965, quando o Transit apareceu;
1978, desde quando o Iveco Daily é feito; o 2.7 CDI de cinco cilindros do Sprinter.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_vans.py -> out/thumbnails/van_*.jpg + qa/thumbs_vans/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_vans"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "van_300k", "src": P / "Three_Rivers_M25_Motorway_-_geograph.org.uk_-_5733181.jpg",
     "num": "300,000", "word": "MILES", "size": 215},
    {"name": "van_nine", "src": P / "Mercedes-Benz_Sprinter.jpg",
     "num": "9", "word": "VANS THAT GET THERE", "size": 215},
    {"name": "van_1965", "src": P / "1980_Ford_Transit_Luton_box_van_.jpg",
     "num": "1965", "word": "THE FIRST TRANSIT", "size": 215},
    {"name": "van_1978", "src": P / "Iveco_Daily_4X4_double_cab_chassis.jpg",
     "num": "1978", "word": "STILL A TRUCK CHASSIS", "size": 200},
    {"name": "van_27cdi", "src": P / "Mercedes-Benz_Sprinter_2e_generatie.jpg",
     "num": "2.7 CDI", "word": "THE ONE TO LOOK FOR", "size": 195},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
