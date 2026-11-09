"""Miniaturas "Mercury x Jing-Jin" (pt, 27/10). Todo número é dito: 4.930, 3.700, 4.000, 2023."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_mercury"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "mercury_4930", "src": g("Pexels_13993920_*.jpg"), "num": f"US${NB}4.930", "word": "O MOTOR ELÉTRICO DE POPA", "size": 230},
    {"name": "mercury_3700", "src": g("Pexels_35652157_*.jpg"), "num": f"3.700{NB}W", "word": "AVATOR 35e ELÉTRICO", "size": 260},
    {"name": "mercury_4000", "src": g("Compression_Testing_*.jpg"), "num": f"US${NB}4.000", "word": "NA VITRINE DOS EUA", "size": 230},
    {"name": "mercury_2023", "src": g("Pudong_Shanghai_November_2017_*.jpg"), "num": "2023", "word": "MERCURY + CHINA", "size": 290},
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
