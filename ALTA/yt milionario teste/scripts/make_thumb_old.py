"""Miniaturas "7 Old-House Features Worth Keeping Before You Start Remodeling" (en, 02/11). Números ditos: seven, 1978
(lead paint), 150 (anos da janela de madeira), twelve by twelve / 10 ft."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_old"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "old_7", "src": F / "p26eb6ac2.jpg", "num": "7", "word": "FEATURES WORTH KEEPING", "size": 260},
    {"name": "old_150", "src": F / "p0addea59.jpg", "num": "150", "word": "YEARS · WOOD WINDOWS", "size": 230},
    {"name": "old_1978", "src": F / "p13e51792.jpg", "num": "1978", "word": "LEAD PAINT YEAR", "size": 230},
    {"name": "old_46", "src": F / "p3b19c35a.jpg", "num": "4-6", "word": "REFINISHES · SOLID FLOORS", "size": 230},
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
