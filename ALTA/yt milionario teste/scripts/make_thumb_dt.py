"""Miniaturas "10 cheap Dollar Tree items when the furnace dies" (en, 20/10). Todo número é dito: ten items,
one dollar and twenty-five cents, three in the morning. Fotos aprovadas do filme (Commons/Pexels/reuso surv)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_dt"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
SIDE = json.loads((ROOT / "data" / "photo_side.json").read_text("utf-8"))
NB = " "


def foto(tag, n=0, contem=None):
    achadas = []
    for t, v in SIDE.items():
        if v.get("verdict") != "ok" or (v.get("tags") or [""])[0] != tag:
            continue
        if contem and contem.lower() not in t.lower():
            continue
        f = POOL.get(t, {}).get("file")
        if f and Path(f).exists() and (POOL[t].get("width") or 0) >= 1600:
            achadas.append(Path(f))
    if not achadas:
        raise SystemExit(f"[thumb] sem foto da tag {tag}")
    return achadas[min(n, len(achadas) - 1)]


SPECS = [
    {"name": "dt_10", "src": foto("snow", 2), "num": "10" + NB + "CHEAP ITEMS", "word": "WHEN THE FURNACE DIES", "size": 210},
    {"name": "dt_store", "src": foto("store", 0, "dollar"), "num": "10" + NB + "ITEMS", "word": "DOLLAR TREE SURVIVAL KIT", "size": 250},
    {"name": "dt_125", "src": foto("mylar", 0), "num": "$1.25", "word": "THE CHEAPEST WARMTH", "size": 270},
    {"name": "dt_3am", "src": foto("candle", 0), "num": "3" + NB + "A.M.", "word": "AND THE FURNACE IS DEAD", "size": 260},
    {"name": "dt_room", "src": foto("room", 0), "num": "10" + NB + "ITEMS", "word": "FOR A FEW DOLLARS", "size": 250},
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
