"""Miniaturas 2 — ênfase no TRABALHO COM CARANGUEJO (pedido do usuário) para o título

    "Este trabalho com caranguejos no Alasca paga US$ 50.000 em 3 meses — se você sobreviver"

Os quadros saem dos ARQUIVOS ORIGINAIS em 1080p (nunca do filme renderizado) e mostram o que o título promete:
a tripulação despejando o caranguejo na mesa, cinco homens triando a captura e o homem com o caranguejo na mão.

Especificação fixa do usuário (16/09): foto real com água no quadro, 2 palavras (primeira BRANCA, segunda CIANO
#00D4FF ou VERMELHA #FF3B30), Anton em caixa alta com contorno escuro, terço inferior esquerdo (ou superior
quando o assunto está embaixo), sem seta/círculo/borda/emoji/faixa atrás do texto.

Texto EM INGLÊS (o filme é narrado em inglês), ancorado na narração: "$50,000 in three months"; "the word
survive in that headline is not a metaphor"; "twenty hour shifts on deck are standard".
Uso: python make_thumb_crab2.py -> out/thumbnails/crab2_*.jpg + qa/thumb_crab2/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma máquina de desenho)

Q = ROOT / "qa" / "thumb_crab2" / "orig"

SPECS = [
    # a tripulação despejando o caranguejo na mesa de triagem, gaivotas em volta
    {"name": "crab2_50k_3months", "src": Q / "Key_58.png",
     "w1": "$50,000", "w2": "3 MONTHS", "cor": VERMELHO, "pos": "baixo", "recorte": (0.82, 0.52, 0.43)},
    # cinco homens triando a captura, visto de cima: o trabalho inteiro num quadro
    {"name": "crab2_if_you_survive", "src": Q / "Silver_100.png",
     "w1": "IF YOU", "w2": "SURVIVE", "cor": CIANO, "pos": "cima"},
    # o caranguejo na mão, no costado, com a montanha atrás
    {"name": "crab2_20_hours", "src": Q / "Tanner_1047.png",
     "w1": "20 HOURS", "w2": "ON DECK", "cor": CIANO, "pos": "cima", "recorte": (0.9, 0.52, 0.55)},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumb_crab2" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=90)
    print("[review]", rev)


if __name__ == "__main__":
    main()
