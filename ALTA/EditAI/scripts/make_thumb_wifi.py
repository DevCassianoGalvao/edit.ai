"""Five thumbnails "How Australia invented Wi-Fi" (en). Every number is spoken in the narration:
A$430 million; 23 companies; 1996; 90 percent of the industry; 36 dishes.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_wifi"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "wifi_430", "src": S / "pd18aeb20.jpg", "num": "A$430 MILLION", "word": "FOR ONE PATENT", "size": 200},
    {"name": "wifi_23", "src": S / "pebf44f28.jpg", "num": "23", "word": "COMPANIES PAID UP", "size": 320},
    {"name": "wifi_1996", "src": S / "peab23fca.jpg", "num": "1996", "word": "THE AUSTRALIAN PATENT", "size": 270},
    {"name": "wifi_90", "src": S / "p2386e887.jpg", "num": "90%", "word": "OF THE INDUSTRY PAID", "size": 300},
    {"name": "wifi_36", "src": S / "p8c6f500d.jpg", "num": "36", "word": "DISHES · DOING IT AGAIN", "size": 300},
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
