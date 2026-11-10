"""Cinco miniaturas do filme da Pif Paf (português), no estilo da referência: número DOURADO colado à
palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: os 4 bilhões de faturamento; a alavancagem de 40 vezes; os 80 milhões de aves
por ano; os 8.500 funcionários; os 50 anos de construção.
Imagens: Wikimedia Commons em alta resolução (>= 2200 px), já aprovadas na folha.
Uso: python make_thumb_pifpaf.py -> out/thumbnails/pp_*.jpg + qa/thumbs_pp/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_pp"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # a planta de frango: a máquina que a dívida quase parou
    {"name": "pp_40x", "src": P / "Inside_slaughterhouse_4186777549_.jpg",
     "num": "40×", "word": "A DÍVIDA QUE ENGOLIU", "size": 215},
    # o galpão cheio: os 80 milhões de aves por ano
    {"name": "pp_80mi", "src": P / "Bobby_Morgan_Poultry_Farm_Agriculture_in_the_United_States.jpg",
     "num": "80 MI", "word": "DE AVES POR ANO", "size": 200},
    # a linha de produção: os 8.500 empregos
    {"name": "pp_8500", "src": P / "Bari_Samaratsi_Meat_Plant_2195.jpg",
     "num": "8.500", "word": "EMPREGOS EM RISCO", "size": 195},
    # o frango embalado no mercado: os 4 bilhões de faturamento
    {"name": "pp_4bi", "src": P / "SelectionOfPackageMeats.jpg",
     "num": "R$ 4 BI", "word": "E QUASE QUEBROU", "size": 190},
    # o galpão de criação: os 50 anos construindo
    {"name": "pp_50anos", "src": P / "Fazenda_em_Formiga-MG.jpg",
     "num": "50 ANOS", "word": "PARA QUASE PERDER TUDO", "size": 185},
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
