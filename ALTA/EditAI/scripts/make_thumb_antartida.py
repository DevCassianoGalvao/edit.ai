"""Cinco miniaturas de "Surviving the Southern Ocean — the icebreaker Nuyina" (en), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: a onda de 78 pés medida em 2018; os 160 metros do Nuyina; os menos dois
graus que disparam o choque térmico; os 18 milhões de km² de banquisa no fim do inverno; os 70 nós de vento.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_antartida.py -> out/thumbnails/gelo_*.jpg + qa/thumbs_antartida/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_antartida"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "gelo_78ft", "src": P / "View_from_the_bow_of_the_Fugro_Discovery_in_the_southern_Indian_Ocean_2_.jpg",
     "num": "78 FT", "word": "IN ONE WAVE", "size": 210},
    {"name": "gelo_160m", "src": P / "Polarstern_ESA20794325.jpeg",
     "num": "160 M", "word": "OF ICEBREAKER", "size": 205},
    {"name": "gelo_menos2", "src": P / "Post_card._S.S._Northwestern._On_the_Alaskan_coast_after_a_storm._Ship_covered_with_ice_and_snow.jpg",
     "num": "−2 °C", "word": "KILLS IN MINUTES", "size": 200},
    {"name": "gelo_18mi", "src": P / "CCGS_Amundsen_icebreaker_Trois-Rivi_res.jpg",
     "num": "18M KM²", "word": "OF SEA ICE", "size": 195},
    {"name": "gelo_70nos", "src": P / "Fugro_Equator_operating_in_the_search_area_in_the_southern_Indian_Ocean_2_.jpg",
     "num": "70", "word": "KNOTS OF WIND", "size": 240},
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
