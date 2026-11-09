"""Miniaturas "Vigias de torres" (pt, 27/10). Números ditos: 646, 30, 45, 10 vezes."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_torres"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "torres_646", "src": g("Pexels_15104408_*.jpg"), "num": "646 M", "word": "A TORRE QUE CAIU", "size": 250},
    {"name": "torres_30dias", "src": g("KVRR-tower_*.jpg"), "num": "30 DIAS", "word": "NÃO EXISTE", "size": 240},
    {"name": "torres_45min", "src": g("Pexels_1126376_*.jpg"), "num": "45 MIN", "word": "SÓ PARA SUBIR", "size": 230},
    {"name": "torres_10x", "src": g("Guy_Anchor_Konstantynow_*.jpg"), "num": "10X", "word": "MAIS MORTES", "size": 290},
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
