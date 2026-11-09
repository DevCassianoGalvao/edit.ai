"""Cinco miniaturas de "A rota dos piratas" (pt) — número DOURADO + palavra BRANCA, uma linha, fonte Anton.
Todo número é dito na narração: o navio de 1 bilhão de reais; os mais de 400 dias de cativeiro do Galaxy Leader;
os mais de 230 ataques de 2011; 20 a 25 pessoas a bordo; mais de 18 nós para fugir das lanchas.
Uso: python make_thumb_piratas.py -> out/thumbnails/pir_*.jpg + qa/thumbs_piratas/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
B = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_piratas"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "pir_1bilhao", "src": B / "The_container_ship_Ever_Forward_-_220420-A-OX377-2006.jpg",
     "num": "R$ 1 BILHÃO", "word": "NA MIRA", "size": 205},
    {"name": "pir_400dias", "src": P / "Car_carrier_Galaxy_Leader_6cd980.jpg",
     "num": "400 DIAS", "word": "REFÉNS", "size": 225},
    {"name": "pir_230", "src": P / "Gulf_of_Aden_-_disabled_pirate_boat_b31c03.jpg",
     "num": "230", "word": "ATAQUES", "size": 260},
    {"name": "pir_20pessoas", "src": B / "Ever_Smart_2012_vor_Cuxhaven.jpg",
     "num": "20 PESSOAS", "word": "400 METROS", "size": 200},
    {"name": "pir_18nos", "src": P / "US_Navy_100410-N-1082Z-119_A_visit_board_search_and_seizure_VBSS_team_pulls_suspected_pira_74f1d1.jpg",
     "num": "18 NÓS", "word": "PARA FUGIR", "size": 225},
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
