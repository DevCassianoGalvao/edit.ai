"""Cinco miniaturas "Australia's New Invention Could Replace Coal Forever" (en, pedido do painel 20260928-071851).
Todo número é dito na narração: 570 °C (vapor supercrítico, CSIRO 2014); mais de oito horas de armazenamento (Vast Solar
One); 30 MW; acima de 800 °C (partículas); cerca de US$ 1,3 bilhão cortado no orçamento de 2026."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_aus"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "aus_570", "src": S / "p06575d6e.jpg", "num": "570°C", "word": "FROM SUNLIGHT ALONE", "size": 300},
    {"name": "aus_8h", "src": S / "p64dbe8e6.jpg", "num": "8 HOURS", "word": "OF SUN AFTER DARK", "size": 260},
    {"name": "aus_30", "src": S / "p83db4404.jpg", "num": "30 MW", "word": "TO REPLACE COAL?", "size": 300},
    {"name": "aus_800", "src": S / "p43fe1cfa.jpg", "num": "800°C", "word": "WITHOUT BURNING COAL", "size": 300},
    {"name": "aus_13b", "src": S / "p959fd8d1.jpg", "num": "$1.3 BILLION", "word": "JUST GOT CUT", "size": 210},
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
