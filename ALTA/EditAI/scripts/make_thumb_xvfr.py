"""Miniaturas "Xiaomi vient de dévoiler un moteur à 28 000 tr/min" (fr, 21/10). Todo número é dito: 28 000, 27 200,
0,15 mm, 1548 ch, 7:04 (Nürburgring). Fotos do Commons (Xiaomi SU7 / SU7 Ultra / YU7)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_xvfr"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "xvfr_28000", "src": g("Xiaomi_SU7_Ultra_yellow_showroom_side_view_2026*.jpg"), "num": f"28{NB}000", "word": "TOURS/MIN. L'EUROPE SOUS LE CHOC", "size": 240},
    {"name": "xvfr_27200", "src": g("Xiaomi_SU7_Ultra_Aqua_Green_front*.jpg"), "num": f"27{NB}200", "word": "TOURS PAR MINUTE", "size": 240},
    {"name": "xvfr_015", "src": g("2025_Xiaomi_YU7_green_*.jpg"), "num": "0,15 mm", "word": "SANS FIBRE DE CARBONE", "size": 240},
    {"name": "xvfr_1548", "src": g("_-_SU7_Ultra_-_2025-05-17*.jpg"), "num": f"1548{NB}CH", "word": "UNE MARQUE DE TÉLÉPHONES", "size": 220},
    {"name": "xvfr_704", "src": g("Xiaomi_SU7_Max_grey_front_view*.jpg"), "num": "7:04", "word": "PORSCHE BATTU AU NÜRBURGRING", "size": 260},
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
