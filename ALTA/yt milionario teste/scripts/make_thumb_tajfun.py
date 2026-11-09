"""Miniaturas "Tajfun" (pl, painel 20260930-092613). Todo número é dito na narração:
czterdzieści osiem tysięcy ton, sto siedemdziesiąt pięć metrów, dwadzieścia rakiet, dwieście głowic, sto dwadzieścia dni."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_tajfun"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "tajfun_48000", "src": S / "p50cd3da9.jpg", "num": "48 000 TON", "word": "NAJWIĘKSZY OKRĘT PODWODNY", "size": 200},
    {"name": "tajfun_175", "src": S / "p7928bb34.jpg", "num": "175 M", "word": "PODWODNE MIASTO", "size": 280},
    {"name": "tajfun_200", "src": S / "p02a615ac.jpg", "num": "200", "word": "GŁOWIC W JEDNYM OKRĘCIE", "size": 320},
    {"name": "tajfun_120", "src": S / "p39a46e43.jpg", "num": "120 DNI", "word": "POD LODEM ARKTYKI", "size": 260},
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
