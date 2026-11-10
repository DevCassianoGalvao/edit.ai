"""Cinco miniaturas do filme do cemitério de navios, no estilo da referência do usuário (número DOURADO colado à
palavra BRANCA, Anton, alto à esquerda — make_thumb_solda.make).
Todo número é dito na narração: "mais de um bilhão de reais", "trezentos metros" cortados a mão, "oito em cada dez"
toneladas desmanchadas no Sul da Ásia, "pelo menos vinte e seis trabalhadores morreram" em Gadani, "noventa por cento
ou mais" reaproveitado.
Fotos: quadro 1080p NATIVO dos vídeos baixados (qa/thumbs_navios/cand, sem logo no quadro) ou Commons >= 3 800 px.
Uso: python make_thumb_navios.py -> out/thumbnails/navios_*.jpg + qa/thumbs_navios/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

C = ROOT / "qa" / "thumbs_navios" / "cand"
P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_navios"

SPECS = [
    # o graneleiro enferrujado chegando à praia de Alang, botes em volta: a promessa do título
    {"name": "navios_1_bilhao", "src": C / "9iXVNeutzDY_40.png", "num": "R$ 1 BILHÃO", "word": "VIRA SUCATA", "size": 180},
    # o petroleiro inteiro encalhado, guindastes e guinchos na areia
    {"name": "navios_300_metros", "src": C / "DMOtqyU756Y_55.png", "num": "300 M", "word": "CORTADOS À MÃO", "size": 200},
    # a praia de Alang cheia de cascos
    {"name": "navios_8_em_10", "src": P / "ASIA_S_BIGGEST_SHIP_BREAKING_YARD_ALANG.jpg", "num": "8 EM 10", "word": "MORREM AQUI", "size": 200},
    # Gadani: cascos na praia do Baluchistão
    {"name": "navios_26_mortos", "src": P / "Gadani_Ship_Breaking_yard_-_panoramio.jpg", "num": "26", "word": "MORTOS EM GADANI", "size": 210},
    # casco aberto no estaleiro de reciclagem
    {"name": "navios_90", "src": P / "End_of_the_life_vessel_beached_in_ship_recycling_yard.jpg", "num": "90%", "word": "REAPROVEITADO", "size": 210},
]


def main():
    QA.mkdir(parents=True, exist_ok=True)
    outs = []
    for s in SPECS:
        assert Image.open(s["src"]).size[0] >= 1920, s["name"]  # nunca ampliar
        outs.append(make(s))
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
