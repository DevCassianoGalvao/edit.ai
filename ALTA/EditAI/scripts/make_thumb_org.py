"""Miniaturas "If You Can't Stop Organizing" (en, 20/10, b1). Todo número é dito: eleven at night, 43 percent. Fotos Wikimedia Commons / Pexels aprovadas no filme."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_org"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    f = POOL[titulo].get("file")
    p = Path(f) if f else None
    if not p or not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {titulo}")
    return p


SPECS = [
    {"name": "org_11pm", "src": foto("File:Pexels 6940372 Asian woman sitting on bed in pajamas writing in a journal, illuminated by lamp .jpg"), "num": "11" + NB + "PM", "word": "WHY YOU ORGANIZE", "size": 250},
    {"name": "org_brain", "src": foto("File:Pexels 8580763 A woman organizing a pantry shelf with various food jars in a modern kitchen..jpg"), "num": "NOT OCD", "word": "YOUR BRAIN WANTS ORDER", "size": 230},
    {"name": "org_43", "src": foto("File:Pexels 17301204 Top view of a neatly organized drawer filled with colorful containers holding va.jpg"), "num": "43%", "word": "SEE ORDER THAT ISN'T THERE", "size": 250},
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
