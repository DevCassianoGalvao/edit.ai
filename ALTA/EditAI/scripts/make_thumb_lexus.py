"""Miniaturas "Lexus Rzuca BOMBĘ — Elektryczne LFA Może Zagrozić BMW" (pl, 02/11). Todo número é dito: V10, 500 egz.,
1000 km, 805 km, 691 szt. Fotos do Commons (Lexus LFA, Sport Concept, LS 500h, BMW iX3)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_lexus"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "lexus_v10", "src": g("Lexus_Sport_Concept_front_left_*.jpg"), "num": "V10", "word": "ZNIKA. LEXUS RZUCA BOMBĘ", "size": 260},
    {"name": "lexus_1000", "src": g("Lexus_LF-ZC_37313e.jpg"), "num": f"1000{NB}KM", "word": "OBIETNICA TOYOTY", "size": 230},
    {"name": "lexus_805", "src": g("BMW_iX3_50L_001_*.jpg"), "num": f"805{NB}KM", "word": "BMW JUŻ TO MA", "size": 240},
    {"name": "lexus_500", "src": g("2011_Lexus_LFA_White_*.jpg"), "num": f"500{NB}SZTUK", "word": "LEGENDA ZNIKA", "size": 200},
    {"name": "lexus_691", "src": g("0_Lexus_LS_500h_GVF50_1_*.jpg"), "num": f"691{NB}SZT.", "word": "LS KOŃCZY W USA", "size": 220},
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
