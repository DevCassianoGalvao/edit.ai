"""Five thumbnails for the CP winter-crew film (English), in the user's reference style (GOLD number + WHITE word,
Anton, top-left — make_thumb_solda.make). Every number is spoken in the narration: forty below; ten days; two people;
a mile and a half of steel; forty-four below.
Sources: native 1080p frames from the downloaded railfan videos (qa/thumbs_cp/cand), cropped to remove channel marks.
Usage: python make_thumb_cp.py -> out/thumbnails/cp_*.jpg + qa/thumbs_cp/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
C = ROOT / "qa" / "thumbs_cp" / "cand"
QA = ROOT / "qa" / "thumbs_cp"


def crop(src, out, top=0.0, bottom=0.0, left=0.0):
    im = Image.open(src).convert("RGB"); w, h = im.size
    y0, y1 = int(h * top), int(h * (1 - bottom)); nh = y1 - y0; nw = int(nh * 16 / 9)
    x0 = min(max(int(w * left), 0), w - nw)
    im.crop((x0, y0, x0 + nw, y1)).save(out, quality=97); return out


SPECS = [
    {"name": "cp_40below", "src": C / "7hBYOZEUoIw_84.6.png", "num": "-40°", "word": "10 DAYS", "size": 220},
    {"name": "cp_10days", "src": crop(C / "wccRg3i-f7U_143.0.png", QA / "_t2.jpg"), "num": "10 DAYS", "word": "AT -40°", "size": 210},
    {"name": "cp_2people", "src": crop(C / "RpS775SpawI_123.9.png", QA / "_t3.jpg"), "num": "2 PEOPLE", "word": "1 LOCOMOTIVE", "size": 190},
    {"name": "cp_mile", "src": crop(C / "HHH4A9FmuD0_205.0.png", QA / "_t4.jpg", 0.0, 0.12, 0.0), "num": "1.5 MILES", "word": "OF STEEL", "size": 200},
    {"name": "cp_44below", "src": crop(C / "XqQiYyjUvls_160.6.png", QA / "_t5.jpg"), "num": "-44°", "word": "AND STILL MOVING", "size": 210},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372)); folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90); print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
