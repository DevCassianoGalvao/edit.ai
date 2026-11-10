"""Pięć miniatur "Jak wielki może być statek?" (pl). Liczby mówione w narracji: 458 m; ponad 40 lat; 650 tysięcy ton; 400 m; 488 m."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_stat"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "stat_458", "src": S / "p8c1bb398.jpg", "num": "458 M", "word": "NAJDŁUŻSZY STATEK W HISTORII", "size": 250},
    {"name": "stat_40", "src": S / "p5a6b4a53.jpg", "num": "40 LAT", "word": "NIKT NIE ZBUDOWAŁ WIĘKSZEGO", "size": 240},
    {"name": "stat_650", "src": S / "pa9e39766.jpg", "num": "650 TYS. TON", "word": "I JEDNA FALA", "size": 200},
    {"name": "stat_400", "src": S / "p7bbf4527.jpg", "num": "400 M", "word": "GRANICA KONTENEROWCÓW", "size": 260},
    {"name": "stat_124", "src": S / "p2c41a1be.jpg", "num": "124 M", "word": "SZEROKOŚCI · DWA KADŁUBY", "size": 260},
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
