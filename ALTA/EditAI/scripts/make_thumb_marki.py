"""Miniaturas "10 Nowych Aut, Których w Polsce Nikt Nie Chce" (pl, 04/11). Todo número é dito: 10 marek, −35,5 %, −61 %, −52,9 %."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_marki"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "marki_10", "src": g("2023_Mitsubishi_ASX_1.3_DI-T_front_*.jpg"), "num": "10", "word": "MAREK, KTÓRYCH POLACY NIE CHCĄ", "size": 300},
    {"name": "marki_355", "src": g("Mitsubishi_ASX_2nd_generation_1X7A6891_*.jpg"), "num": f"−35,5{NB}%", "word": "MITSUBISHI W POLSCE", "size": 250},
    {"name": "marki_61", "src": g("Mitsubishi_ASX_Hybrid_1X7A7176_*.jpg"), "num": f"−61{NB}%", "word": "W JEDNYM MIESIĄCU", "size": 280},
    {"name": "marki_529", "src": g("Porsche_Macan_4_IMG_2153_*.jpg"), "num": f"−52,9{NB}%", "word": "PORSCHE WE WRZEŚNIU", "size": 250},
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
