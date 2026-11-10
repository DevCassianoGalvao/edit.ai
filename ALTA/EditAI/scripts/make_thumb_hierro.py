"""Cinco miniaturas "El Hierro, la isla que vive del viento y del agua" (es, painel 20260929-091358). Todo número é dito
na narração: 24 días seguidos; 11.000 habitantes; 6.000 toneladas de gasóleo; 5 aerogeneradores; 2011 (erupción)."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_hierro"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "hierro_24", "src": S / "p5aab1569.jpg", "num": "24 DÍAS", "word": "SIN PETRÓLEO", "size": 270},
    {"name": "hierro_11000", "src": S / "pa8c4f7cf.jpg", "num": "11.000", "word": "VIVEN DEL VIENTO", "size": 280},
    {"name": "hierro_6000", "src": S / "p35e46943.jpg", "num": "6.000 T", "word": "DE GASÓLEO AL AÑO", "size": 270},
    {"name": "hierro_5", "src": S / "p52c9ea83.jpg", "num": "5", "word": "MOLINOS PARA UNA ISLA", "size": 330},
    {"name": "hierro_2011", "src": S / "p5857fdff.jpg", "num": "2011", "word": "EL VOLCÁN BAJO EL MAR", "size": 300},
]


def main():
    for s in SPECS:
        make(s)
    outs = [ROOT / "out" / "thumbnails" / f"{s['name']}.jpg" for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
