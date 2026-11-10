"""Cinco miniaturas "Fertilizantes sem caixa" (pt). Todo número é dito na narração: US$ 22 e US$ 69; 30 %; US$ 1.200; 60 dias; R$ 2 bilhões."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_fert"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "fert_22", "src": S / "pbbc193e5.jpg", "num": "US$ 22", "word": "POR TONELADA · ERAM US$ 69", "size": 240},
    {"name": "fert_30", "src": S / "pa8a97d47.jpg", "num": "30%", "word": "MENOS ADUBO NA LAVOURA", "size": 300},
    {"name": "fert_1200", "src": S / "p80c0255f.jpg", "num": "US$ 1.200", "word": "A TONELADA DE ENXOFRE", "size": 230},
    {"name": "fert_60", "src": S / "pb42c5e04.jpg", "num": "60", "word": "DIAS CONTRA OS CREDORES", "size": 320},
    {"name": "fert_2bi", "src": S / "pff1c805c.jpg", "num": "R$ 2 BI", "word": "PEDIDOS AO GOVERNO", "size": 260},
]


def main():
    for s in SPECS:
        make(s)
    outs = [ROOT / "out" / "thumbnails" / f"{s['name']}.jpg" for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
