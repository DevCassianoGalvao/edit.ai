"""Miniaturas pescadores de lagosta do Ceará (pt, 06/11). Números ditos: 300 metros de mangueira, 7 de 28 morreram, 98 por cento ilegal, 130 metros."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public"
QA = ROOT / "qa" / "thumbs_lag"
QA.mkdir(parents=True, exist_ok=True)
C = json.loads((ROOT / "data" / "clips.json").read_text("utf-8"))["clips"]


def foto(tag, i):
    l = [x["file"] for x in C if x.get("kind") == "photo" and x.get("tags") and x["tags"][0] == tag]
    return F / l[min(i, len(l) - 1)]


SPECS = [
    {"name": "lag_300m", "src": foto("mergulho", 0), "num": "300 M", "word": "DE MANGUEIRA ATÉ A BOCA", "size": 230},
    {"name": "lag_7de28", "src": foto("camara", 0), "num": "7 DE 28", "word": "NÃO SOBREVIVERAM", "size": 210},
    {"name": "lag_98", "src": foto("lagosta", 0), "num": "98%", "word": "DA LAGOSTA É ILEGAL", "size": 260},
    {"name": "lag_130m", "src": foto("jangada", 2), "num": "130 M", "word": "COM AR DE BOTIJÃO", "size": 230},
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
