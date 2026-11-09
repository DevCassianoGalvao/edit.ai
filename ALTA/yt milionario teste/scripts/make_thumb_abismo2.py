"""Cinco miniaturas do filme dos predadores do abismo (pedido do usuário: "mostrar bem os predadores, imagens chamativas").
Título do vídeo: "Caçadores da Escuridão Absoluta: Os Predadores Mais Ferozes a 4 Mil Metros de Profundidade".

Mesma máquina de desenho (make_thumb_navio2.make): 2 palavras, branca + vermelha/ciano, Anton, sem faixa/seta/borda.
Foto ≥ 3 700 px (só reduz). Tudo dito na narração: "dentes longos demais para caber na própria boca",
"armadilhas de luz viva", "o peixe dragão negro produz luz vermelha", "cinquenta toneladas",
"mais de quatro anos consecutivos", "a quatro mil metros".
Uso: python make_thumb_abismo2.py -> out/thumbnails/abismo2_*.jpg + qa/thumbs_abismo2/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402

F = ROOT / "assets" / "photos"
OUT = ROOT / "out" / "thumbnails"
QA = ROOT / "qa" / "thumbs_abismo2"

SPECS = [
    # peixe-víbora de boca aberta, presas à mostra (Ifremer, 4608 px, CC BY 4.0)
    {"name": "abismo2_dentes_longos", "src": F / "thumb_viper2.jpg",
     "w1": "DENTES", "w2": "LONGOS", "cor": VERMELHO, "pos": "cima", "recorte": (0.85, 0.55, 0.5)},
    # peixe-pescador negro com a isca acesa (Hal, 3738 px, CC BY-SA 4.0)
    {"name": "abismo2_luz_viva", "src": F / "thumb_anglerfish.jpg",
     "w1": "LUZ", "w2": "VIVA", "cor": CIANO, "pos": "baixo", "recorte": (0.9, 0.5, 0.5)},
    # dragão-negro com o fotóforo vermelho sob o olho (Hal, 4325 px, CC BY-SA 4.0)
    {"name": "abismo2_luz_vermelha", "src": F / "thumb_dragonfish.jpg",
     "w1": "LUZ", "w2": "VERMELHA", "cor": VERMELHO, "pos": "baixo", "recorte": (0.8, 0.55, 0.5)},
    # isópode-gigante de frente (5472 px, CC BY-SA 2.0)
    {"name": "abismo2_quatro_anos", "src": F / "Giant_Isopod_18443864634_.jpg",
     "w1": "QUATRO", "w2": "ANOS", "cor": CIANO, "pos": "baixo", "recorte": (0.9, 0.5, 0.5)},
    # cachalote com filhote (5115 px, CC BY-SA 2.0)
    {"name": "abismo2_50_toneladas", "src": F / "thumb_spermwhale.jpg",
     "w1": "50", "w2": "TONELADAS", "cor": VERMELHO, "pos": "baixo", "recorte": (0.9, 0.5, 0.45)},
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    outs = []
    for s in SPECS:
        w = Image.open(s["src"]).size[0]
        assert w >= 3700, f"{s['src'].name}: {w} px"
        outs.append(make(s))
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("\n".join(str(p) for p in outs))


if __name__ == "__main__":
    main()
