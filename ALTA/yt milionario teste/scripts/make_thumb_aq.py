"""Cinco miniaturas "Aquarius" (pt). Todo número é dito na narração: dez dias; 20 metros; 17 horas; seis pessoas; 31 dias."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_aq"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "aq_10", "src": S / "pd0acd054.jpg", "num": "10", "word": "DIAS SEM PODER SUBIR", "size": 320},
    {"name": "aq_20", "src": S / "p3ebeee21.jpg", "num": "20 METROS", "word": "UMA CASA NO FUNDO DO MAR", "size": 230},
    {"name": "aq_17", "src": S / "pc412a4f7.jpg", "num": "17 HORAS", "word": "PARA VOLTAR À SUPERFÍCIE", "size": 230},
    {"name": "aq_6", "src": S / "p9e37c011.jpg", "num": "6", "word": "PESSOAS · SEIS BELICHES", "size": 330},
    {"name": "aq_31", "src": S / "pe76829ac.jpg", "num": "31", "word": "DIAS DEBAIXO D'ÁGUA", "size": 320},
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
