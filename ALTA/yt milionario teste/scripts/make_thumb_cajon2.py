"""Mais 3 miniaturas do filme do Cajon Pass (pedido do usuário), agora com FOTO de alta resolução
do Wikimedia Commons (3840 px) em vez de quadro de vídeo. Mesmo estilo: número DOURADO + palavra BRANCA, Anton.
Números ditos na narração: around two percent; twelve thousand tons; well over a hundred trains a day;
four thousand four hundred horsepower.
Uso: python make_thumb_cajon2.py -> out/thumbnails/cajon_*.jpg + qa/thumbs_cajon/review2.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_cajon"

SPECS = [
    # a fila de locomotivas da Union Pacific subindo o corte do passo (Commons, 3840x2560)
    {"name": "cajon_2_percent", "src": P / "UnionPacificcajonpass.jpg", "num": "2% GRADE", "word": "12,000 TONS", "size": 190},
    # o BNSF laranja com o passo coberto de neve (Commons, 3840x2560)
    {"name": "cajon_100_trains", "src": P / "BNSFcajonpass.jpg", "num": "100 TRAINS", "word": "A DAY", "size": 200},
    # a locomotiva de frente no pôr do sol (Commons, 3840x2560)
    {"name": "cajon_4400_hp", "src": P / "Autorack.jpg", "num": "4,400 HP", "word": "PER ENGINE", "size": 200},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372)); folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review2.jpg", quality=90); print("->", QA / "review2.jpg")


if __name__ == "__main__":
    main()
