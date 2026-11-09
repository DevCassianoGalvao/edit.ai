"""Five thumbnails for "Night shift at minus 45" (en) — GOLD number glued to a WHITE word, one line, top left, Anton.
Commons photos >= 1080p from Yakutia and Russian railways.

Every number is SPOKEN in the narration: minus 45 tonight; the record minus 64.4 (1891); the minus 47 at the end
of the shift; the 350-meter Aldan bridge; the 40 minutes waiting at the frozen switch.
Use: python make_thumb_yakutsk.py -> out/thumbnails/yak_*.jpg + qa/thumbs_yakutsk/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_yakutsk"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "yak_minus45", "src": P / "Train_In_The_Snow_192702893_.jpeg",
     "num": "−45°C", "word": "NIGHT SHIFT", "size": 230},
    {"name": "yak_minus64", "src": P / "Yakutsk_-_190227_DSC_4907.jpg",
     "num": "−64°C", "word": "THE RECORD", "size": 235},
    {"name": "yak_minus47", "src": P / "Night_train_at_Golovanova_Dacha_Tumskaya_railway_10074709234_.jpg",
     "num": "−47°C", "word": "AT DAWN", "size": 235},
    {"name": "yak_350m", "src": P / "_02.JPG",
     "num": "350 M", "word": "OVER THE ALDAN", "size": 220},
    {"name": "yak_40min", "src": P / "Winter_station_Vodinskaya.jpg",
     "num": "40 MIN", "word": "FROZEN SWITCH", "size": 215},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
