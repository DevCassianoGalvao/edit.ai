"""Miniaturas "Como Vivem os Técnicos que Cuidam das Torres de Energia no Meio da Floresta" (pt, 29/10). Todo número é dito:
1.800 km, 3.600 torres, 500 kV, 295 m, 721 km. Fotos de public/stock (Pexels/Commons)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_tecnicos"
QA.mkdir(parents=True, exist_ok=True)
NB = " "

SPECS = [
    {"name": "tec_3600", "src": F / "p6526da29.jpg", "num": f"3.600", "word": "TORRES NA FLORESTA", "size": 250},
    {"name": "tec_1800", "src": F / "p258e5408.jpg", "num": f"1.800{NB}KM", "word": "DE CABOS NA AMAZÔNIA", "size": 220},
    {"name": "tec_500", "src": F / "p3bab44b9.jpg", "num": f"500{NB}KV", "word": "NO MEIO DA MATA", "size": 230},
    {"name": "tec_295", "src": F / "pc80b51e0.jpg", "num": f"295{NB}M", "word": "TORRES SOBRE O AMAZONAS", "size": 230},
    {"name": "tec_721", "src": F / "p4779f60b.jpg", "num": f"721{NB}KM", "word": "ATÉ BOA VISTA", "size": 230},
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
