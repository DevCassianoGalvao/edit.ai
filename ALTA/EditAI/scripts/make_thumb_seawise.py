"""Cinco miniaturas do filme do Seawise Giant, estilo da referência (número DOURADO + palavra BRANCA, Anton, alto à esquerda).
Todo número é dito na narração: 458 metros; mais de 657 mil toneladas; cerca de 10 km para parar; cinco nomes; 24,5 m de calado.
Fotos: quadros 1080p nativos (qa/thumbs_seawise/cand), recortados só para tirar a faixa de título do canal (sem ampliar abaixo de 1920 px de origem).
Uso: python make_thumb_seawise.py -> out/thumbnails/seawise_*.jpg + qa/thumbs_seawise/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
C = ROOT / "qa" / "thumbs_seawise" / "cand"
QA = ROOT / "qa" / "thumbs_seawise"


def sem_faixa(src, out, top=0.12, bottom=0.0):
    im = Image.open(src).convert("RGB"); w, h = im.size
    y0, y1 = int(h * top), int(h * (1 - bottom))
    nh = y1 - y0; nw = int(nh * 16 / 9); x0 = (w - nw) // 2
    im.crop((x0, y0, x0 + nw, y1)).save(out, quality=97)
    return out


SPECS = [
    {"name": "seawise_458m", "src": sem_faixa(C / "idjbwskrnKk_160.png", QA / "_t1.jpg", 0.12, 0.08), "num": "458 M", "word": "DE AÇO", "size": 220},
    {"name": "seawise_657mil", "src": sem_faixa(C / "3LaCyte3eaA_30.png", QA / "_t2.jpg", 0.0, 0.08), "num": "657 MIL T", "word": "FLUTUANDO", "size": 190},
    {"name": "seawise_10km", "src": sem_faixa(C / "3SB8BlJZmF0_70.png", QA / "_t3.jpg", 0.0, 0.0), "num": "10 KM", "word": "PARA PARAR", "size": 210},
    {"name": "seawise_5nomes", "src": sem_faixa(C / "5uzTMSg-oIQ_90.png", QA / "_t4.jpg", 0.12, 0.14), "num": "5 NOMES", "word": "1 GIGANTE", "size": 200},
    {"name": "seawise_24m", "src": sem_faixa(C / "15fME-J497k_30.png", QA / "_t5.jpg", 0.0, 0.08), "num": "24,5 M", "word": "SOB A ÁGUA", "size": 200},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372)); folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90); print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
