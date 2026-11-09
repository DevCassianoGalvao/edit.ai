"""Miniaturas "10 cheap Walmart foods ... can't cook for three days" (en, 20/10). Todo número é dito: ten foods,
three days, just under four dollars (peanut butter). Fotos aprovadas do filme."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_wm"
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
    {"name": "wm_10", "src": foto("trailmix", 0), "num": "10" + NB + "CHEAP FOODS", "word": "3 DAYS WITHOUT COOKING", "size": 210},
    {"name": "wm_walmart", "src": foto("walmart", 0, "walmart"), "num": "10" + NB + "WALMART FOODS", "word": "NO STOVE · NO FRIDGE", "size": 200},
    {"name": "wm_pb", "src": foto("pb", 0), "num": "$4", "word": "THE JAR THAT FEEDS A FAMILY", "size": 300},
    {"name": "wm_3days", "src": foto("powerout", 0), "num": "3" + NB + "DAYS", "word": "WHEN THE POWER IS GONE", "size": 270},
    {"name": "wm_cans", "src": foto("cans", 0), "num": "10" + NB + "ITEMS", "word": "PRICELESS IN A BLACKOUT", "size": 250},
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
