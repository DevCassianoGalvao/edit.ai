"""Cinco miniaturas de "Chiński silnik rekordowy" (pl) — número dourado + palavra branca. Todo número é dito na narração:
48,41 % de eficiência; 2,22 l/100 km; 12 % melhor que o Prius; 450 litros a menos por ano; injeção a 500 bar.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
B = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_silnik"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "pl_4841", "src": P / "Geely_Emgrand_IV_007_12fe46.jpg", "num": "48,41%", "word": "REKORD", "size": 240},
    {"name": "pl_222l", "src": P / "Geely_Emgrand_IV_012_0e6bde.jpg", "num": "2,22 L", "word": "NA 100 KM", "size": 240},
    {"name": "pl_12proc", "src": P / "Prius_on_the_Blue_Carpet_53518912307__428e09.jpg", "num": "12%", "word": "LEPSZY OD PRIUSA", "size": 250},
    {"name": "pl_450l", "src": P / "Shanghai_stau_5d657f.jpg", "num": "450 L", "word": "MNIEJ ROCZNIE", "size": 240},
    {"name": "pl_500bar", "src": P / "VCR-engine_dyno_testing_P1505_Heilbronn_University_3f84d3.jpg", "num": "500 BAR", "word": "WTRYSK", "size": 225},
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
