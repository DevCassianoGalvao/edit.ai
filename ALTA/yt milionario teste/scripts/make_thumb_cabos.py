"""Cinco miniaturas de "The forgotten network — submarine cables" (en), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: 1,4 milhão de km no fundo do mar; as 98 palavras da rainha Victoria;
os 12 cabos rompidos em 1929; as 36 ligações simultâneas do TAT-1; os 99 % de todo o tráfego intercontinental.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_cabos.py -> out/thumbnails/cabo_*.jpg + qa/thumbs_cabos/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_cabos"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "cabo_14m", "src": P / "A_steelworker_works_on_an_underwater_cable._14836087892_.jpg",
     "num": "1.4M KM", "word": "ON THE SEABED", "size": 190},
    {"name": "cabo_98", "src": P / "Telegraph_key_and_sounder_-_Bennington_Museum_-_Bennington_VT_-_DSC08644.JPG",
     "num": "98", "word": "WORDS IN 16 HOURS", "size": 235},
    {"name": "cabo_12", "src": P / "Submarine_telegraph_cable_in_the_early_1900s_2_.png",
     "num": "12", "word": "CABLES SNAPPED", "size": 240},
    {"name": "cabo_36", "src": P / "12_Optical_fibers_2_.jpg",
     "num": "36", "word": "CALLS AT A TIME", "size": 240},
    {"name": "cabo_99", "src": P / "Port_Side_of_CS_Cable_Innovator.jpg",
     "num": "99%", "word": "OF ALL DATA", "size": 225},
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
