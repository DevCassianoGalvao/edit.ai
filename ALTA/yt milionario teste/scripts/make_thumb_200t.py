"""Duas miniaturas para o titulo "Por Que um Navio de Aco de 200 Mil Toneladas Nao Afunda | Documentario".

Pedido do usuario: ENFASE NO NAVIO, e a foto nao precisa sair dos videos do filme.
As duas usam o HMM ALGECIRAS (porta-conteineres de ~228 mil toneladas de porte bruto) em foto de 3400 px do
Commons, CC BY-SA 2.0 de kees torn — cabe no numero do titulo sem exagerar.

O texto e "200 MIL" + "TONELADAS", e nao "200 TONELADAS": 200 toneladas seria uma barcaca, nao o navio do filme.
Resto da especificacao fixa (16/09): agua sempre no quadro, plano aberto, duas palavras (branca + ciano/vermelha),
Anton caixa alta, terco inferior esquerdo (ou superior se o assunto estiver embaixo), paleta fria,
sem seta/circulo/borda/rosto em close/emoji/faixa atras do texto.
Uso: python make_thumb_200t.py -> out/thumbnails/navio3_*.jpg + qa/thumbs_200t/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_navio2 import CIANO, VERMELHO, make  # noqa: E402  (mesma maquina de desenho)

FOTOS = ROOT / "APAGAR_navio-2026-09-16" / "fotos_thumb"

SPECS = [
    # A: navio carregado passando, rebocador ao lado dando a escala; agua no terco inferior -> texto embaixo
    {"name": "navio3_200mil_carregado", "src": FOTOS / "HMM_ALGECIRAS_49969576408_.jpg",
     "w1": "200 MIL", "w2": "TONELADAS", "cor": CIANO, "pos": "baixo"},
    # B: proa de frente, rebocador minusculo colado no bulbo -> mesma ideia, outro enquadramento, em vermelho
    {"name": "navio3_200mil_proa", "src": FOTOS / "HMM_ALGECIRAS_ROTTERDAM_49970357237_.jpg",
     "w1": "200 MIL", "w2": "TONELADAS", "cor": VERMELHO, "pos": "baixo", "empilhar": True},
]


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumbs_200t" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=90)
    print("[review]", rev)


if __name__ == "__main__":
    main()
