"""Cinco miniaturas "El caza soviético cancelado que nunca llegó a volar" (es, painel 20260928-230303). Todo número é
dito na narração: 3.000 km/h; 27 km de altitud; 1960 (desguace); Mach 3; T-37."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_caza"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "caza_3000", "src": S / "pd7da4dde.jpg", "num": "3.000 KM/H", "word": "Y NUNCA VOLÓ", "size": 230},
    {"name": "caza_1960", "src": S / "pbb404220.jpg", "num": "1960", "word": "ORDEN: DESGUAZARLO", "size": 300},
    {"name": "caza_mach3", "src": S / "p61d0da40.jpg", "num": "MACH 3", "word": "EL CAZA PROHIBIDO", "size": 280},
    {"name": "caza_27km", "src": S / "p1d87479f.jpg", "num": "27 KM", "word": "DE ALTURA", "size": 300},
    {"name": "caza_t37", "src": S / "pd0246be1.jpg", "num": "T-37", "word": "EL AVIÓN DESTRUIDO", "size": 300},
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
