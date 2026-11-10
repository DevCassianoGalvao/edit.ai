"""Miniaturas "Motor de Popa Elétrico Dá Conta de Pescaria?" (pt, 29/10). Todo número é dito:
3 vezes, 4.200 dólares, 12 horas, 57 kg. Fotos de public/stock (Pexels/Commons)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_popa"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "popa_3x", "src": F / "p43bd0552.jpg", "num": "3X", "word": "MAIS CARO QUE A GASOLINA", "size": 260},
    {"name": "popa_4200", "src": F / "p3a735e72.jpg", "num": f"4.200{NB}US$", "word": "SÓ DE DIFERENÇA", "size": 210},
    {"name": "popa_12h", "src": F / "ped8490c7.jpg", "num": f"12{NB}HORAS", "word": "PARA CARREGAR", "size": 220},
    {"name": "popa_57", "src": F / "p533bb0ca.jpg", "num": f"57{NB}KG", "word": "COM A BATERIA", "size": 230},
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
