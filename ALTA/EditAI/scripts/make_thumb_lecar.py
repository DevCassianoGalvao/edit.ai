"""Cinco miniaturas de "O carro elétrico brasileiro que a China não esperava" (pt) — número DOURADO + palavra BRANCA,
uma linha, fonte Anton. Todo número é dito na narração: 1.000 km de autonomia; 30 litros de etanol; os mais de
40 mil veículos da Gurgel; o imposto de 35 %; os R$ 5,5 bilhões da BYD em Camaçari.
Uso: python make_thumb_lecar.py -> out/thumbnails/br_*.jpg + qa/thumbs_lecar/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_lecar"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "br_1000km", "src": P / "Posto_de_Combust_vel_Paju_ara_-_Natal_-_RN_0502e8.jpg",
     "num": "1.000 KM", "word": "COM ETANOL", "size": 215},
    {"name": "br_30litros", "src": P / "Cana-de-a_car_-_Colheita_Mecanizada_-_Santo_In_cio_PR._-_panoramio_097671.jpg",
     "num": "30 LITROS", "word": "DE ETANOL", "size": 215},
    {"name": "br_40mil", "src": P / "Gurgel_em_S_o_Paulo._b7d532.jpg",
     "num": "40 MIL", "word": "GURGEL VENDIDOS", "size": 225},
    {"name": "br_35", "src": P / "Car_carrier_NEPTUNE_KEFALONIA_en_mer_7b1bce.jpg",
     "num": "35%", "word": "DE IMPOSTO", "size": 250},
    {"name": "br_55bi", "src": P / "BYD_DOLPHIN_MINI_BRAZIL_BYD_SEAGULL_6343e8.jpg",
     "num": "R$ 5,5 BI", "word": "DA BYD", "size": 215},
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
