"""Cinco miniaturas de "Toyota po cichu wróciła do V8" (pl), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: os 270 mil veículos das três chamadas; os 70 mil motores já trocados;
os 5,7 litros do V8 aposentado; os 3,5 litros do V6 que o substituiu; as 3 akcje serwisowe.
A Anton tem todos os diacríticos poloneses (Ę Ć Ł Ń Ó Ś Ź Ż Ą) — conferido antes de gerar.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_tundra.py -> out/thumbnails/tun_*.jpg + qa/thumbs_tundra/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_tundra"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "tun_270k", "src": P / "Toyota_Tundra_Limited_2023_53646536522_.jpg",
     "num": "270 000", "word": "AUT W AKCJI", "size": 200},
    {"name": "tun_70k", "src": P / "Engine_Unsplash_.jpg",
     "num": "70 000", "word": "WYMIENIONYCH SILNIKÓW", "size": 180},
    {"name": "tun_57", "src": P / "2021_Toyota_Tundra_SR5_Pro_Double_Cab_in_Lunar_Rock_front_left.jpg",
     "num": "5,7 L", "word": "V8, KTÓRY WYRZUCONO", "size": 195},
    {"name": "tun_35", "src": P / "2022_Toyota_Tundra_1794_Edition_TRD_Crew_Cab_4X4_in_Celestial_Silver_front_left.jpg",
     "num": "3,5 L", "word": "I DWIE TURBINY", "size": 210},
    {"name": "tun_3akcje", "src": P / "Metal_sparks.jpg",
     "num": "3", "word": "AKCJE SERWISOWE", "size": 240},
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
