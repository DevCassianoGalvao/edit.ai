"""Miniaturas dresser (en, 05/11). Número dito: thirty-five dollars ($35). Fotos = cenas IA do seu canal."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_dresser"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "dr_35", "src": F / "ia_06.jpg", "num": "$35", "word": "OLD DRESSER · NO ELECTRICITY", "size": 230},
    {"name": "dr_35b", "src": F / "ia_02.jpg", "num": "$35", "word": "DRESSER DRIES YOUR HARVEST", "size": 230},
    {"name": "dr_35c", "src": F / "ia_08.jpg", "num": "$35", "word": "NO PLUG · NO BILL · NO NOISE", "size": 230},
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
