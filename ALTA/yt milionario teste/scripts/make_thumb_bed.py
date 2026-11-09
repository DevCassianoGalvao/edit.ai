"""Miniaturas "If You Make Your Bed Every Morning" (en, 24/10, b1). Todo número é dito: 19 percent, 71 percent, one and a half million. Fotos Wikimedia Commons / Pexels aprovadas no filme."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_bed"
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
    {"name": "bed_19", "src": foto("File:Pexels 4153153 A woman with curly hair making a bed in a modern, cozy bedroom with natural ligh.jpg"), "num": "19%", "word": "BETTER SLEEP?", "size": 250},
    {"name": "bed_71", "src": foto("File:Pexels 11899139 Modern bedroom interior with striped headboard and blue geometric pillows, creat.jpg"), "num": "71%", "word": "SAY THEY'RE HAPPY", "size": 250},
    {"name": "bed_unmade", "src": foto("File:Pexels 37073368 An unmade bed with crumpled linens and a striped shirt adding a cozy feel..jpg"), "num": "1.5 MILLION", "word": "MITES IN YOUR BED", "size": 190},
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
