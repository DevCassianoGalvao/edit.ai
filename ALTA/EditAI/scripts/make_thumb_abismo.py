"""Miniaturas do filme dos predadores do abismo — especificação fixa do usuário (16/09), com foto GRANDE.

Fonte: só foto aprovada do acervo com 3800 px+ de largura (o corte para 1920×1080 apenas reduz, nunca amplia).
Texto: 2 palavras, primeira BRANCA e segunda CIANO (#00D4FF) ou VERMELHA (#FF3B30), Anton em caixa alta com
contorno escuro; terço inferior esquerdo, ou superior quando o bicho está embaixo.
Proibido: seta, círculo, borda, emoji e faixa/gradiente atrás do texto.
Tudo é dito na narração: "a quatro mil metros de profundidade"; "dentes longos demais para caber na própria
boca"; "a escuridão absoluta produziu os monstros mais eficientes"; "mais de quatro anos consecutivos".
Uso: python make_thumb_abismo.py -> out/thumbnails/abismo_*.jpg + qa/thumbs_abismo/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma máquina de desenho)

F = ROOT / "assets" / "photos"
OUT = ROOT / "out" / "thumbnails"
QA = ROOT / "qa" / "thumbs_abismo"

SPECS = [
    # peixe-víbora de boca aberta, 4608 px (Ifremer, CC BY 4.0)
    {"name": "abismo_dentes_longos", "src": F / "Grand_croc_petit_fil_Chauliodus_sloani_de_M_diterran_e_Ifremer_00676-78846_-_31646_.jpg",
     "w1": "DENTES", "w2": "LONGOS", "cor": VERMELHO, "pos": "baixo", "recorte": (0.9, 0.5, 0.45)},
    # (o peixe-pescador Gigantactis saiu: a foto é prateleira de museu com caixas brancas — não vende abismo)
    # isópode-gigante, 5472 px (CC BY-SA 2.0)
    {"name": "abismo_quatro_anos", "src": F / "Giant_Isopod_18443864634_.jpg",
     "w1": "QUATRO", "w2": "ANOS", "cor": CIANO, "pos": "baixo", "recorte": (0.9, 0.5, 0.5)},
    # mandíbula do peixe-víbora, 4608 px
    {"name": "abismo_escuridao_absoluta", "src": F / "Grand_croc_petit_fil_Chauliodus_sloani_de_M_diterran_e_Ifremer_00676-78846_-_31643_.jpg",
     "w1": "ESCURIDÃO", "w2": "ABSOLUTA", "cor": CIANO, "pos": "baixo", "recorte": (0.9, 0.5, 0.45)},
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    outs = []
    for s in SPECS:
        im = Image.open(s["src"])
        assert im.size[0] >= 3800, f"{s['src'].name}: {im.size[0]} px (mínimo 3800)"
        p = make(s)
        outs.append(p)
    # folha de revisão: grande + no tamanho da listagem do YouTube (210 px), que é onde a legibilidade se decide
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("\n".join(str(p) for p in outs))
    print(f"-> {QA / 'review.jpg'}")


if __name__ == "__main__":
    main()
