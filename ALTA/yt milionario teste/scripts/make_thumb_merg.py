"""Cinco miniaturas "Os mergulhadores pagos para tirar corpos de navios naufragados" (pt). Todo número é dito na
narração: mil dólares por dia; 118 homens; 28 dias; 852 mortos; 304 mortos.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_merg"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "merg_1000", "src": S / "pf2cef94f.jpg", "num": "US$ 1.000", "word": "POR DIA PARA DESCER", "size": 230},
    {"name": "merg_118", "src": S / "p08f85749.jpg", "num": "118", "word": "HOMENS NO KURSK", "size": 320},
    {"name": "merg_28", "src": S / "pd5083ac8.jpg", "num": "28", "word": "DIAS SOB PRESSÃO", "size": 320},
    {"name": "merg_852", "src": S / "pcd115d50.jpg", "num": "852", "word": "NUNCA VOLTARAM", "size": 300},
    {"name": "merg_304", "src": S / "p4fc57e6d.jpg", "num": "304", "word": "MORTOS NO SEWOL", "size": 300},
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
