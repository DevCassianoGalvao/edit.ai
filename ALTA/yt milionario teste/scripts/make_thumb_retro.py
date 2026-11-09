"""Miniatury "Chiny produkują klasyki z elektrykiem" (pl). Każda liczba pada w narracji: 2022 (Ballet Cat),
29 tysięcy juanów (Wuling), Tank 300, 35 procent cła."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_retro"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "retro_2022", "src": S / "p20990639.jpg", "num": "2022", "word": "CHIŃSKI GARBUS", "size": 300},
    {"name": "retro_29", "src": S / "p00907422.jpg", "num": "29" + NB + "TYS.", "word": "JUANÓW ZA ELEKTRYKA", "size": 260},
    {"name": "retro_300", "src": S / "p26c638b7.jpg", "num": "TANK" + NB + "300", "word": "CHIŃSKI DEFENDER?", "size": 240},
    {"name": "retro_35", "src": S / "p0cef651b.jpg", "num": "35%", "word": "CŁA NIE POMOGŁY", "size": 300},
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
