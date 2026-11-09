"""Cinco miniaturas do filme "21 carros que saem de linha até 2027" (pt-BR), no estilo da referência
(número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton).
Todo número é dito na narração: 21 modelos; 2027; 5 dos 21 saem pelas regras de emissões; a Saveiro de 1982;
os 170 cavalos da nova picape da Renault.
Imagens: fotos do Wikimedia Commons em alta resolução (>= 3000 px) já baixadas em assets/photos.
Uso: python make_thumb_carros.py -> out/thumbnails/carros_*.jpg + qa/thumbs_carros/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_carros"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # um sedã zero na rua: os 21 modelos que saem da vitrine
    {"name": "carros_21_modelos", "src": P / "2021_Fiat_Cronos_1.8_16v_Precision_front_view_.jpg",
     "num": "21 CARROS", "word": "FORA ATÉ 2027", "size": 185},
    # o escapamento: os 5 que saem pela lei de emissões
    {"name": "carros_5_pela_lei", "src": P / "Car_exhaust_pipe.jpg",
     "num": "5 DE 21", "word": "SAEM PELA LEI", "size": 195},
    # a Saveiro: o nome que mais mexe com o brasileiro
    {"name": "carros_saveiro_1982", "src": P / "Saveiro_G6_Trend.jpg",
     "num": "1982", "word": "A SAVEIRO ACABA", "size": 195},
    # a picape que substitui a Oroch
    {"name": "carros_170_cavalos", "src": P / "Renault_Duster_Oroch.jpg",
     "num": "170 CV", "word": "A NOVA PICAPE", "size": 200},
    # o Jimny: o 4x4 mais barato que saiu de cena
    {"name": "carros_jimny_108", "src": P / "Suzuki_Jimny_4x4_GLX_2019.jpg",
     "num": "108 CV", "word": "REPROVADO NA LEI", "size": 190},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90); print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
