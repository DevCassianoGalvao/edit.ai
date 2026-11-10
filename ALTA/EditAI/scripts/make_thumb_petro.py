"""Miniaturas "Como é a Vida no Maior Petroleiro do Mundo?" (pt, 25/10). Todo número é dito: 380 metros, 3 milhões de barris,
40 pessoas, 11 meses, 6 horas. Fotos do Pexels (petroleiros)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_petro"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "petro_380", "src": g("Pexels_1036866_*.jpg", "Pexels_36563588_*.jpg"), "num": f"380{NB}METROS", "word": "E SÓ 40 PESSOAS", "size": 200},
    {"name": "petro_3mi", "src": g("Pexels_36563588_*.jpg"), "num": "3 MILHÕES", "word": "DE BARRIS A BORDO", "size": 210},
    {"name": "petro_40", "src": g("Pexels_18597927_*.jpg", "Pexels_1036866_*.jpg"), "num": "40 PESSOAS", "word": "NO MEIO DO OCEANO", "size": 210},
    {"name": "petro_11", "src": g("Pexels_36563592_*.jpg", "Pexels_36563588_*.jpg"), "num": "11 MESES", "word": "SEM PISAR EM TERRA", "size": 230},
    {"name": "petro_6h", "src": g("Pexels_19302826_*.jpg", "Pexels_1036866_*.jpg"), "num": "6 HORAS", "word": "EM TERRA, NO MÁXIMO", "size": 240},
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
