"""Five thumbnails "SunCable - the solar cable to Singapore" (en). Every number is spoken in the narration:
4,300 km cable; 20 gigawatts; 95% imported gas; 1.75 gigawatts; 30 to 35 billion Australian dollars.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_sun"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "sun_4300", "src": S / "pa52e7657.jpg", "num": "4,300 KM", "word": "SOLAR CABLE", "size": 230},
    {"name": "sun_20gw", "src": S / "p65afbf5a.jpg", "num": "20 GW", "word": "IN THE OUTBACK", "size": 260},
    {"name": "sun_95", "src": S / "pe1bfa487.jpg", "num": "95%", "word": "IMPORTED GAS", "size": 270},
    {"name": "sun_175", "src": S / "p5042225d.jpg", "num": "1.75 GW", "word": "TO SINGAPORE", "size": 240},
    {"name": "sun_30b", "src": S / "p3ef59f2b.jpg", "num": "$30 BILLION", "word": "SOLAR BET", "size": 210},
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
