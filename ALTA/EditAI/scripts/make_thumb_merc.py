"""Miniaturas "Mercedes Rzuca BOMBĘ — Nowy Silnik z Berlina" (pl). Todo número é dito: 1169 KM, 3 razy, 2,1 s, 600 kW,
42 kW/kg. Fotos do Commons (AMG GT 4 portas X290 / Concept GT XX)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_merc"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "merc_1169", "src": g("Mercedes-AMG_GT_63_S_E_Performance_IAA_2021_1X7A0201*.jpg"), "num": f"1169{NB}KM", "word": "SILNIK Z BERLINA", "size": 220},
    {"name": "merc_3x", "src": g("Mercedes-AMG_Concept_GT_XX_IAA_2025_DSC_1447*.jpg"), "num": "3× LŻEJSZY", "word": "NOWY SILNIK MERCEDESA", "size": 200},
    {"name": "merc_21", "src": g("Mercedes-AMG_Concept_AMG_GT_XX_JMS_2025_*.jpg"), "num": "2,1 S", "word": "DO SETKI · 4 DRZWI", "size": 260},
    {"name": "merc_600", "src": g("Mercedes-AMG_Concept_GT_XX_IAA_2025_DSC_2085*.jpg"), "num": f"600{NB}KW", "word": "ŁADOWANIA", "size": 240},
    {"name": "merc_42", "src": g("Mercedes-AMG_Concept_GT_XX_IAA_2025_DSC_1872*.jpg"), "num": "42 KW/KG", "word": "MERCEDES RZUCA BOMBĘ", "size": 200},
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
