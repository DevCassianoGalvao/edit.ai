"""Cinco miniaturas de "A crise da Camil" (pt) — número dourado + palavra branca. Todo número é dito na narração:
alta de 49 % da saca; dívida de mais de R$ 4 bilhões; ações -18 % num pregão; safra gaúcha -13 %; 1 real de lucro a cada 100.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
B = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_camil"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "cam_49", "src": P / "Handful_of_rice_d045e6.jpg", "num": "+49%", "word": "NO ARROZ", "size": 250},
    {"name": "cam_4bi", "src": P / "Harvested_rice_in_Doho_Rice_Scheme_7cb440.jpg", "num": "R$ 4 BI", "word": "EM DÍVIDAS", "size": 225},
    {"name": "cam_18", "src": P / "Bovespa_S_o_Paulo_city_downtown_a6ab79.jpg", "num": "-18%", "word": "EM UM DIA", "size": 250},
    {"name": "cam_13", "src": P / "Arroz_irrigado_Irrigated_rice_plantation_2456055347__4d61a4.jpg", "num": "-13%", "word": "NA SAFRA", "size": 250},
    {"name": "cam_1real", "src": P / "Supermercado_Talevi_45c432.jpg", "num": "R$ 1", "word": "DE LUCRO A CADA 100", "size": 240},
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
