"""Three thumbnails for the Cajon Pass film (English), in the user's reference style (GOLD number + WHITE word,
Anton, top-left — make_thumb_solda.make).
Title: The Hardest 60 Miles in America: How 2 Engineers Take 12,000 Tons Over Cajon Pass.
Every number is spoken in the narration: twelve thousand tons; two people in a cab; the hardest sixty miles;
nearly three thousand feet.
Source: native 1080p frames from the railfan videos used in the film (qa/thumbs_cajon/cand).
Usage: python make_thumb_cajon.py -> out/thumbnails/cajon_*.jpg + qa/thumbs_cajon/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
C = ROOT / "qa" / "thumbs_cajon" / "cand"
QA = ROOT / "qa" / "thumbs_cajon"


def crop(src, out, top=0.0, bottom=0.0, left=0.5):
    im = Image.open(src).convert("RGB"); w, h = im.size
    y0, y1 = int(h * top), int(h * (1 - bottom)); nh = y1 - y0; nw = min(int(nh * 16 / 9), w)
    x0 = min(max(int((w - nw) * left), 0), w - nw)
    im.crop((x0, y0, x0 + nw, y1)).save(out, quality=97); return out


SPECS = [
    # a locomotiva de frente no passo: as 12 mil toneladas e os 2 na cabine
    {"name": "cajon_12000_tons", "src": C / "v0898b282_4.2.png", "num": "60 MILES", "word": "12,000 TONS", "size": 190},
    # o trem laranja fazendo a curva pela montanha: as 60 milhas
    {"name": "cajon_60_miles", "src": C / "v55cd8f3b_4.2.png", "num": "60 MILES", "word": "OF MOUNTAIN", "size": 200},
    # o drone colado na locomotiva descendo: os 3.000 pés
    {"name": "cajon_3000_ft", "src": C / "v152313cd_4.2.png", "num": "3,000 FT", "word": "STRAIGHT DOWN", "size": 195},
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
