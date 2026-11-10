"""Miniaturas "Catar: 99 % del agua potable sale del mar" (es, 26/10). Todo número é dito: 99 %, 5 días, 48 horas,
3 millones, 540 millones de galones. Fotos do Commons/Pixabay aprovadas."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_catar"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "catar_99", "src": g("Doha_Skyline_12_*.jpg", "Doha_Skyline_10_*.jpg"), "num": f"99{NB}%", "word": "DEL AGUA SALE DEL MAR", "size": 230},
    {"name": "catar_5dias", "src": g("Multi_Stage_Flash_Desalination_*.jpg"), "num": f"5{NB}DÍAS", "word": "DE AGUA GUARDADA", "size": 230},
    {"name": "catar_48h", "src": g("Qatar_Zekreet_Bir_Zekrit_10_*.jpg", "Desert_of_Qatar_*.jpg"), "num": f"48{NB}HORAS", "word": "SIN AGUA", "size": 220},
    {"name": "catar_3mill", "src": g("Pixabay_10197389_*.jpg"), "num": f"3{NB}MILLONES", "word": "BEBEN DEL MAR", "size": 210},
    {"name": "catar_540", "src": g("Doha_Corniche_Skyline_View_1_*.jpg", "Doha_Skyline_11_*.jpg"), "num": "540 MILLONES", "word": "DE GALONES AL DÍA", "size": 190},
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
