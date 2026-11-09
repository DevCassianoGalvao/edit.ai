"""Miniaturas "7 voitures électriques" (fr, 27/10). Todo número é dito: 80 %, 22 524, 72 668, 200 000."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_evfr"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "evfr_80", "src": g("2020_Volkswagen_ID.3_1st_Front_*.jpg"), "num": f"80{NB}%", "word": "DE BATTERIE SEULEMENT", "size": 290},
    {"name": "evfr_22524", "src": g("2020_Volkswagen_ID.4_Pro_Netherlands_front_view_*.jpg"), "num": f"22{NB}524", "word": "ID.4 RAPPELÉES AUX ÉTATS-UNIS", "size": 250},
    {"name": "evfr_72668", "src": g("VW_ID4_GTX_20210805_113252_*.jpg"), "num": f"72{NB}668", "word": "VOITURES VW RAPPELÉES", "size": 250},
    {"name": "evfr_200000", "src": g("2021_Hyundai_Ioniq_5_Premium_Standard_Range_2WD_Front__*.jpg"), "num": f"200{NB}000", "word": "HYUNDAI ET KIA RAPPELÉES", "size": 230},
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
