"""Miniaturas do filme do caranguejo do Bering — mesma especificação que o usuário fixou em 16/09.

Imagem:      foto real que ESTÁ no filme, em força total (arquivo original do Commons, nunca o filme renderizado).
Enquadramento: o objeto do vídeo enchendo o quadro, água sempre presente.
Texto:       2 palavras. Primeira BRANCA, segunda CIANO (#00D4FF) ou VERMELHA (#FF3B30).
Fonte:       Anton em caixa alta, com contorno escuro (o vermelho sumia sobre casco azul sem ele).
Posição:     terço inferior esquerdo; terço SUPERIOR quando o assunto está embaixo.
Proibido:    seta, círculo, borda, emoji e faixa/gradiente atrás do texto.

Todo texto é dito na narração: "$50,000 ... is a gross figure"; "It is cold shock"; "600 to 800 pounds".
Uso: python make_thumb_crab.py -> out/thumbnails/crab_*.jpg + qa/thumbs_crab/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma máquina de desenho)

F = ROOT / "assets" / "photos"

SPECS = [
    # covos empilhados em Dutch Harbor com o vulcão nevado — o objeto do filme, com água no quadro
    {"name": "crab_800_pounds", "src": F / "Crab_Pots_in_Dutch_Harbor_Alaska_2190327867_.jpg",
     "w1": "800", "w2": "POUNDS", "cor": CIANO, "pos": "baixo"},
    # barco de pesca no mar grosso, tripulação esperando resgate (US Navy, domínio público)
    {"name": "crab_cold_shock", "src": F / "US_Navy_061201-N-6423H-006_The_crew_of_the_fishing_vessel_Miss_Melissa_await_rescue_from_a_boat_crew.jpg",
     "w1": "COLD", "w2": "SHOCK", "cor": CIANO, "pos": "cima"},
    # frota de caranguejo em Dutch Harbor, covos no cais e neve no vulcão
    {"name": "crab_50k_gross", "src": F / "Dutch_harbor_crab_boats.jpg",
     "w1": "$50,000", "w2": "GROSS", "cor": VERMELHO, "pos": "baixo"},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumbs_crab" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=90)
    print("[review]", rev)


if __name__ == "__main__":
    main()
