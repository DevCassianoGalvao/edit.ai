"""Cinco miniaturas "Arqueólogos abrieron la tumba de Tutankamón — y algo dentro no debía estar ahí" (es, painel
20260928-130356). Todo número é dito na narração: 1922; cerca del 80 % (Reeves); más de 3.000 años; 70 días; 100 kilos."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_tut"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "tut_80", "src": S / "p7cb42e94.jpg", "num": "80%", "word": "NO ERA PARA ÉL", "size": 300},
    {"name": "tut_1922", "src": S / "p541251e2.jpg", "num": "1922", "word": "ALGUIEN ENTRÓ ANTES", "size": 300},
    {"name": "tut_hierro", "src": S / "p66e1b13a.jpg", "num": "3.000 AÑOS", "word": "HIERRO DEL ESPACIO", "size": 220},
    {"name": "tut_70", "src": S / "p04d70bc2.jpg", "num": "70 DÍAS", "word": "UN ENTIERRO A PRISA", "size": 260},
    {"name": "tut_100", "src": S / "pa47ea5b1.jpg", "num": "100 KG", "word": "DE ORO MACIZO", "size": 280},
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
