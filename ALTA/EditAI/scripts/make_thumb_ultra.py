"""Miniaturas do filme do Part 103 — especificação fixa do usuário (16/09), com foto GRANDE.

Fonte: só foto do acervo do filme com 3800 px+ de largura (o corte para 1920×1080 apenas reduz, nunca amplia
— foi o que resolveu a reclamação de qualidade no filme anterior).
Texto: 2 palavras, primeira BRANCA e segunda CIANO (#00D4FF) ou VERMELHA (#FF3B30), Anton em caixa alta com
contorno escuro; terço inferior esquerdo, ou superior quando a aeronave está embaixo.
Proibido: seta, círculo, borda, emoji e faixa/gradiente atrás do texto.
Tudo é dito na narração: "no pilot license"; "less than two hundred fifty-four pounds empty";
"you can fly a helicopter without a helicopter license".
Uso: python make_thumb_ultra.py -> out/thumbnails/ultra_*.jpg + qa/thumbs_ultra/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma máquina de desenho)

F = ROOT / "assets" / "photos"

SPECS = [
    # o Aerolite 103 do capítulo um, em 6000 px
    {"name": "ultra_no_license", "src": F / "Aero-Works_Aerolite_103_Alina_4-12-2024_.jpg",
     "w1": "NO", "w2": "LICENSE", "cor": VERMELHO, "pos": "baixo", "recorte": (0.82, 0.5, 0.5)},
    # o CGS Hawk Ultra, também em 6000 px
    {"name": "ultra_254_pounds", "src": F / "CGS_Hawk_Ultra_4-11-2024_.jpg",
     "w1": "254", "w2": "POUNDS", "cor": CIANO, "pos": "baixo", "recorte": (0.8, 0.5, 0.5)},
    # o Quicksilver MX clássico, 5184 px
    {"name": "ultra_ten_aircraft", "src": F / "Aerolite.jpg",
     "w1": "TEN", "w2": "AIRCRAFT", "cor": CIANO, "pos": "cima"},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumbs_ultra" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=92)
    print("[review]", rev)


if __name__ == "__main__":
    main()
