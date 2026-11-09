"""Cinco miniaturas de "O trator parado no pátio" (pt) — número dourado + palavra branca. Todo número é dito na narração:
2 % do crédito para investimento; -22 % em máquinas vendidas; 1.263 produtores em recuperação judicial;
mais de R$ 400 mil de juros por colheitadeira parada; Selic de 15 %.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
B = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_trator"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "trat_2", "src": P / "Pexels_29934104_Line_of_blue_tractors_parked_on_a_farm_during_winter._17ce8e.jpg", "num": "2%", "word": "PARA MÁQUINAS", "size": 260},
    {"name": "trat_22", "src": P / "Valtra_S416_Agritechnica_2025_DSC09492__125c65.jpg", "num": "-22%", "word": "TRATORES VENDIDOS", "size": 240},
    {"name": "trat_1263", "src": B / "Farmer_in_Field_48750760032_.jpg", "num": "1.263", "word": "PRODUTORES NA JUSTIÇA", "size": 230},
    {"name": "trat_400mil", "src": B / "Mike_Starkey_Soybean_Harvest_52490323937_.jpg", "num": "R$ 400 MIL", "word": "EM JUROS", "size": 225},
    {"name": "trat_15", "src": P / "Ag_ncia_do_Banco_do_Brasil_em_Coronel_Fabriciano_MG_38600d.jpg", "num": "15%", "word": "DE JUROS", "size": 260},
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
