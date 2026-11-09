"""Mais 5 miniaturas para "Por Que um Navio de Aco de 200 Mil Toneladas Nao Afunda | Documentario".

Mesma especificacao fixa (16/09) e a mesma enfase pedida pelo usuario: o NAVIO grande no quadro, foto podendo
vir de fora dos videos do filme. Cinco navios diferentes, fotos do Commons em 3000 px+ (licenca livre).

Cada frase esta no roteiro:
  "NAO AFUNDA"       -> "duzentas mil toneladas de aco nao afundam..." (e o proprio titulo)
  "200 MIL TONELADAS"-> "o navio desloca duzentas mil toneladas"
  "80 PISCINAS"      -> "mais do que oitenta piscinas olimpicas removidas do oceano"
  "PURO ACO"         -> "ele e feito de aco, um material cerca de oito vezes mais denso que a agua"
  "O MAR SEGURA"     -> "o mar sempre esteve disposto a segurar duzentas mil toneladas de aco"
Uso: python make_thumb_navio4.py -> out/thumbnails/navio4_*.jpg + qa/thumbs_navio4/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402

FOTOS = ROOT / "APAGAR_navio-2026-09-16" / "fotos_thumb"

SPECS = [
    {"name": "navio4_nao_afunda", "src": FOTOS / "Container_ship_Emma_Maersk_with_Destination_Port_of_Hamburg.jpg",
     "w1": "NÃO", "w2": "AFUNDA", "cor": CIANO, "pos": "baixo", "recorte": (0.86, 0.50, 0.50)},
    {"name": "navio4_200mil_julesverne", "src": FOTOS / "Container_ship_CMA_CGM_Jules_Verne_income_Hamburg_on_12_June_2013.jpg",
     "w1": "200 MIL", "w2": "TONELADAS", "cor": CIANO, "pos": "baixo", "recorte": (0.70, 0.56, 0.52)},
    {"name": "navio4_80_piscinas", "src": FOTOS / "Container_ship_CMA_CGM_Margrit_on_the_Elbe_with_Destination_Hamburg.jpg",
     "w1": "80", "w2": "PISCINAS", "cor": VERMELHO, "pos": "baixo", "recorte": (0.74, 0.52, 0.56)},
    {"name": "navio4_puro_aco", "src": FOTOS / "IMO_9811000_EVER_GIVEN_03_.jpg",
     "w1": "PURO", "w2": "AÇO", "cor": CIANO, "pos": "baixo"},
    {"name": "navio4_o_mar_segura", "src": FOTOS / "Container_ship_CMA_CGM_Vasco_da_Gama_in_the_port_of_Hamburg_in_Septemb.jpg",
     "w1": "O MAR", "w2": "SEGURA", "cor": VERMELHO, "pos": "baixo", "recorte": (0.84, 0.52, 0.56)},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumbs_navio4" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=90)
    print("[review]", rev)


if __name__ == "__main__":
    main()
