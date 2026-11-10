"""Miniaturas "18 Tage unter Wasser ohne Tageslicht — Wie leben 28 Soldaten in einem deutschen U-Boot?" (de). Todo número
é dito: 18 Tage, 28 Soldaten, 24 Kojen, 700 Meter (Zerstörungstiefe), 60 Zentimeter (Koje)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_uboot"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "uboot_18tage", "src": S / "pf338b2d0.jpg", "num": "18" + NB + "TAGE", "word": "UNTER WASSER", "size": 270},
    {"name": "uboot_28soldaten", "src": S / "p7db5486e.jpg", "num": "28" + NB + "SOLDATEN", "word": "IN EINER STAHLRÖHRE", "size": 230},
    {"name": "uboot_24kojen", "src": S / "p9cf92690.jpg", "num": "24" + NB + "KOJEN", "word": "FÜR 28 MANN", "size": 250},
    {"name": "uboot_700meter", "src": S / "p2915f8cf.jpg", "num": "700" + NB + "METER", "word": "ZERSTÖRUNGSTIEFE", "size": 250},
    {"name": "uboot_ohnelicht", "src": S / "p5223cd0f.jpg", "num": "18" + NB + "TAGE", "word": "OHNE TAGESLICHT", "size": 270},
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
