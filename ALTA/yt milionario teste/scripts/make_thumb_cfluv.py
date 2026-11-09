"""Miniaturas maior comboio fluvial (pt, 05/11). Números ditos: 35 barcaças, 346 metros, 70 mil toneladas, 1.666 caminhões."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public"
QA = ROOT / "qa" / "thumbs_cfluv"
QA.mkdir(parents=True, exist_ok=True)
C = json.loads((ROOT / "data" / "clips.json").read_text("utf-8"))["clips"]


def foto(tag, i):
    l = [x["file"] for x in C if x.get("kind") == "photo" and x.get("tags") and x["tags"][0] == tag]
    return F / l[min(i, len(l) - 1)]


SPECS = [
    {"name": "cfluv_35", "src": foto("comboio", 5), "num": "35", "word": "BARCAÇAS, UM SÓ EMPURRADOR", "size": 260},
    {"name": "cfluv_70mil", "src": foto("comboio", 3), "num": "70 MIL", "word": "TONELADAS NO RIO AMAZONAS", "size": 200},
    {"name": "cfluv_346", "src": foto("comboio", 7), "num": "346", "word": "METROS: UMA CIDADE DE BARCOS", "size": 230},
    {"name": "cfluv_1666", "src": foto("empurrador", 0), "num": "1.666", "word": "CAMINHÕES A MENOS POR VIAGEM", "size": 200},
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
