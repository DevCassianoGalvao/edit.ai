"""Cinco miniaturas do filme do calor no Mojave (inglês), no estilo da referência
(número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton).
Todo número é dito na narração: 118 °F na cabine; duas pessoas; 12 horas de jornada; o trilho a 140 °F;
a linha concluída em janeiro de 1905.
Imagens: fotos do Wikimedia Commons em alta resolução (>= 2400 px) já baixadas em assets/photos.
Uso: python make_thumb_mojave.py -> out/thumbnails/mj_*.jpg + qa/thumbs_mj/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_mj"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # o trem no deserto aberto: a promessa do título
    {"name": "mj_118", "src": P / "A_long_freight_train_approaches_between_a_wind-turbine_farm_and_desert_land_outside_the_town_of_Caba.jpg",
     "num": "118 °F", "word": "INSIDE THE CAB", "size": 195},
    # o UP passando pela estação no deserto: os dois da tripulação
    {"name": "mj_2people", "src": P / "Union_Pacific_Passing_Through_Desert_Station_-_panoramio.jpg",
     "num": "2 PEOPLE", "word": "NO SHADE, NO EXIT", "size": 185},
    # a cabine velha e suja: as 12 horas de lei
    {"name": "mj_12horas", "src": P / "SWB_A_101_cab_interior_2.jpg",
     "num": "12 HOURS", "word": "THEN THEY STOP", "size": 195},
    # as dunas de Kelso: o calor do chão
    {"name": "mj_140", "src": P / "KelsoDunesMarch2010.JPG",
     "num": "140 °F", "word": "THE RAIL ITSELF", "size": 200},
    # a estação de Kelso: a linha de 1905
    {"name": "mj_1905", "src": P / "Union_Pacific_Railroad_Station_Kelso_California.JPG",
     "num": "1905", "word": "THE LINE THEY BUILT", "size": 190},
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
