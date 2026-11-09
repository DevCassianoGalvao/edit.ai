"""Cinco miniaturas de "25 carros proibidos — 2ª lista" (português), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: os 25 carros da lista; 2027, o ano que aparece em Bruxelas e no PROCONVE;
os 10 anos de Délhi e de Singapura; os quase 50 anos da proibição do diesel de passeio no Brasil; 2035 na Europa.
Imagens: Wikimedia Commons em alta resolução (>= 2400 px), já aprovadas na folha (assets/photos).
Uso: python make_thumb_carros2.py -> out/thumbnails/cr2_*.jpg + qa/thumbs_cr2/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
F = ROOT / "qa" / "thumbs_cr2" / "fotos"   # recortes feitos para a miniatura (o texto precisa de canto vazio)
QA = ROOT / "qa" / "thumbs_cr2"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # o ferro-velho: o destino de quem fica fora da regra — a imagem mais forte da lista
    {"name": "cr2_25_carros", "src": P / "Old_cars_are_stacked_in_a_junkyard_during_a_cloudy_day_in_an_urban_area_with_trees_in_the_background.jpg",
     "num": "25", "word": "CARROS PROIBIDOS", "size": 240},
    # a placa da zona de emissão de Londres: a regra que expulsa o carro da cidade
    {"name": "cr2_2027", "src": F / "ulez.jpg",
     "num": "2027", "word": "O ANO DA VIRADA", "size": 200},
    # Délhi: idade virou lei
    {"name": "cr2_10_anos", "src": F / "delhi.jpg",
     "num": "10 ANOS", "word": "E O CARRO MORRE", "size": 195},
    # São Paulo: a proibição brasileira de quase meio século
    {"name": "cr2_50_anos", "src": P / "At_S_o_Paulo_2018_151.jpg",
     "num": "50 ANOS", "word": "PROIBIDO NO BRASIL", "size": 185},
    # a Comissão Europeia: o item nº 1 da lista, a data que fecha a venda do carro a combustão
    {"name": "cr2_2035", "src": F / "eu.jpg",
     "num": "2035", "word": "O FIM DA GASOLINA", "size": 200},
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
