"""Miniaturas "12 cheap Harbor Freight items when the furnace dies" (en, 20/10). Todo número é dito: twelve items,
two in the morning, first 24 hours, number one (moving blankets). Fotos aprovadas do filme (Commons/Pexels)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_surv"
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
    {"name": "surv_12", "src": foto("snow", 2), "num": "12" + NB + "CHEAP ITEMS", "word": "WHEN THE FURNACE DIES", "size": 210},
    {"name": "surv_2am", "src": foto("candle", 0), "num": "2" + NB + "A.M.", "word": "NO HEAT UNTIL THURSDAY", "size": 280},
    {"name": "surv_24h", "src": foto("room", 0), "num": "24" + NB + "HOURS", "word": "WITHOUT A FURNACE", "size": 270},
    {"name": "surv_hf", "src": foto("store", 0, "harbor"), "num": "12" + NB + "ITEMS", "word": "HARBOR FREIGHT SURVIVAL KIT", "size": 250},
    {"name": "surv_cold", "src": foto("window", 0), "num": "A" + NB + "DEGREE", "word": "LOST EVERY HOUR", "size": 260},
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
