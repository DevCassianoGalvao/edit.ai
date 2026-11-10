"""Miniaturas comboios de soja (pt, 04/11). Números ditos: 60 dias, 35 barcaças, 346 metros, 60 mil toneladas."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public"
QA = ROOT / "qa" / "thumbs_comboio"
QA.mkdir(parents=True, exist_ok=True)
C = json.loads((ROOT / "data" / "clips.json").read_text("utf-8"))["clips"]


def foto(tag, i):
    l = [x["file"] for x in C if x.get("kind") == "photo" and x.get("tags") and x["tags"][0] == tag]
    return F / l[min(i, len(l) - 1)]


SPECS = [
    {"name": "comboio_60", "src": foto("madeira", 6), "num": "60", "word": "DIAS SEM PISAR EM CASA", "size": 260},
    {"name": "comboio_35", "src": foto("empurrador", 0), "num": "35", "word": "BARCAÇAS, UM EMPURRADOR", "size": 260},
    {"name": "comboio_346", "src": foto("comboio", 7), "num": "346", "word": "METROS DE AÇO NO RIO", "size": 230},
    {"name": "comboio_60mil", "src": foto("madeira", 2), "num": "60 MIL", "word": "TONELADAS DE SOJA", "size": 200},
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
