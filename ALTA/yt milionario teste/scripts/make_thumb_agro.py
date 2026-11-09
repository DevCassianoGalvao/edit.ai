"""Cinco miniaturas de "Os três golpes do agro" (pt) — número DOURADO colado à palavra BRANCA, uma linha,
no alto à esquerda, fonte Anton. Fotos brasileiras >= 1080p do Wikimedia Commons.

Todo número é DITO na narração: os 361 milhões de toneladas da safra recorde; os 1.990 pedidos de recuperação
judicial de 2025; a Selic de 15 %; o prejuízo de R$ 630 por hectare em Sorriso; os 3 golpes.
Uso: python make_thumb_agro.py -> out/thumbnails/agro_*.jpg + qa/thumbs_agro/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_agro"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "agro_361mi", "src": P / "Ronodon_polis_colheita_soja_Roosevelt_Pinheiro_28mar09.jpg",
     "num": "361 MI", "word": "DE TONELADAS", "size": 215},
    {"name": "agro_1990", "src": P / "Antigo_F_rum_de_Passos.jpg",
     "num": "1.990", "word": "PEDIDOS NA JUSTIÇA", "size": 215},
    {"name": "agro_15", "src": P / "Edif_cio_sede_do_Banco_Central_do_Brasil_16011634694_.jpg",
     "num": "15%", "word": "DE JUROS NA SELIC", "size": 240},
    {"name": "agro_630", "src": P / "Planta_o_de_Soja_em_Novo_Barreiro.jpg",
     "num": "R$ 630", "word": "DE PREJUÍZO", "size": 220},
    {"name": "agro_3golpes", "src": P / "Agricultores_podem_voltar_a_plantar_feij_o_a_partir_desta_quarta_21720304904_.jpg",
     "num": "3", "word": "GOLPES NO AGRO", "size": 260},
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
