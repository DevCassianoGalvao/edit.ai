"""Miniaturas 3 — QUALIDADE: só FOTO grande (2816–3840 px), nunca quadro de vídeo.

O usuário reclamou que as miniaturas anteriores estavam moles: elas saíam de quadro de vídeo 1080p comprimido e
ainda ampliado pelo recorte. Aqui toda fonte tem pelo menos 2816 px de largura, então o corte para 1920×1080 só
REDUZ a imagem — é o caminho que dá miniatura nítida.

Fontes (licença livre, crédito anotado em qa/thumb_crab3/fotos/ficha.json):
  - Red king crab na arrumação do convés (Commons)         - 3000 x 2003
  - gelo acumulado no barco e nos covos (Commons)          - 3504 x 2336
  - F/V Cornelia Marie navegando com a pilha de covos      - 2816 x 2112
  - king crab de frente, foto de acervo                     - 3840 x 2880

Especificação fixa do usuário (16/09): água no quadro, 2 palavras (primeira BRANCA, segunda CIANO #00D4FF ou
VERMELHA #FF3B30), Anton caixa alta com contorno escuro, terço inferior esquerdo ou superior, sem seta/círculo/
borda/emoji/faixa. Texto em INGLÊS, como o filme, e ancorado na narração.
Uso: python make_thumb_crab3.py -> out/thumbnails/crab3_*.jpg + qa/thumb_crab3/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma máquina de desenho)

F = ROOT / "qa" / "thumb_crab3" / "fotos"

SPECS = [
    # o caranguejo real no meio da arrumação do convés — o que o título promete
    {"name": "crab3_50k_3months", "src": F / "filme_Red_king_crab_paralithodes_camtschaticus.jpg",
     "w1": "$50,000", "w2": "3 MONTHS", "cor": VERMELHO, "pos": "baixo"},
    # gelo acumulado no barco: o "se você sobreviver" do título
    {"name": "crab3_if_you_survive", "src": F / "Ice_Buildup_8743424319_.jpg",
     "w1": "IF YOU", "w2": "SURVIVE", "cor": CIANO, "pos": "cima"},
    # barco de caranguejo navegando com a pilha de covos no convés
    {"name": "crab3_800lb_per_pot", "src": F / "FV_Cornelia_Marie.jpg",
     "w1": "800 LB", "w2": "PER POT", "cor": CIANO, "pos": "baixo", "recorte": (0.72, 0.5, 0.55)},
    # descarga em Dutch Harbor: a hora em que o caranguejo vira dinheiro (a foto do caranguejo de frente,
    # apesar de 3840 px, e uma foto submarina MOLE — nao serve para miniatura)
    {"name": "crab3_sold_by_pound", "src": F / "Offloading_crab_in_Dutch_Harbor.jpg",
     "w1": "SOLD", "w2": "BY POUND", "cor": CIANO, "pos": "cima", "recorte": (0.72, 0.58, 0.5)},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumb_crab3" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=92)
    print("[review]", rev)


if __name__ == "__main__":
    main()
