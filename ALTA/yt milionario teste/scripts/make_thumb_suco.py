"""Miniaturas "Como um Único Navio Leva 32 Mil Toneladas de Suco de Laranja" (pt, 21/10). Todo número é dito: 32 mil
toneladas, 16 tanques, 10 graus negativos, 30 pessoas, 205 metros. Fotos do Commons (Carlos Fischer, navios de suco) e Pexels."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_suco"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "suco_32mil", "src": g("Fruit_juice_carrier_Carlos_Fischer_d*.jpg", "Fruit_juice_carrier_Carlos_Fischer*.jpg"), "num": f"32{NB}MIL{NB}T", "word": "DE SUCO DE LARANJA", "size": 230},
    {"name": "suco_16", "src": g("Fruit_juice_carrier_Carlos_Fischer_2*.jpg", "Fruit_juice_carrier_Carlos_Fischer*.jpg"), "num": "16 TANQUES", "word": "SEM ESTRAGAR", "size": 220},
    {"name": "suco_menos10", "src": g("Orange-Fruit-Pieces*.jpg", "*orange*.jpg"), "num": f"−10{NB}°C", "word": "NO MEIO DO ATLÂNTICO", "size": 260},
    {"name": "suco_30", "src": g("Fruit_juice_carrier_Carlos_Fischer_d*.jpg"), "num": "30 PESSOAS", "word": "E UM MAR DE SUCO", "size": 220},
    {"name": "suco_205", "src": g("Fruit_juice_carrier_Carlos_Fischer_2*.jpg", "Fruit_juice_carrier_Carlos_Fischer*.jpg"), "num": f"205{NB}M", "word": "DE SUCO DO BRASIL", "size": 260},
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
