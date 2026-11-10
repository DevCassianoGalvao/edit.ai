"""Miniaturas "Como Vivem os Marinheiros do Navio que Conserta a Internet" (pt, 02/11). Números ditos: 60, 99, 120 mil, 12 horas."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_marin"
QA.mkdir(parents=True, exist_ok=True)
NB = "\u00a0"

SPECS = [
    {"name": "marin_60", "src": F / "p468b5e5a.jpg", "num": "60", "word": "PESSOAS NO NAVIO DA INTERNET", "size": 330},
    {"name": "marin_99", "src": F / "pf29484fc.jpg", "num": "99%", "word": "DA INTERNET PASSA PELO MAR", "size": 230},
    {"name": "marin_120", "src": F / "p94d41812.jpg", "num": "120 MIL", "word": "DÓLARES POR DIA NO MAR", "size": 200},
    {"name": "marin_12h", "src": F / "p9e54efbe.jpg", "num": "12 H", "word": "DE TURNO EM ALTO-MAR", "size": 230},
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
