"""Miniaturas "7 Carros Chineses Que os Brasileiros SE RECUSAM a Comprar" (pt). Todo número é dito: 7 carros, 4 unidades
(Tan), 5 (E-JS1), 39 (Zeekr 7X), 12 (Cyberster). Fotos do Commons."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
BA = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_chineses"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "ch_7", "src": F / "BYD_Tang_II_EV_facelift_001_5db17f.jpg", "num": "7", "word": "CHINESES ENCALHADOS", "size": 330},
    {"name": "ch_4", "src": F / "BYD_Tang_II_EV_facelift_003_2c6ce8.jpg", "num": "4", "word": "UNIDADES NO MÊS", "size": 330},
    {"name": "ch_5", "src": F / "Sehol_E10X_007_e780c2.jpg", "num": "5", "word": "VENDIDOS EM SETEMBRO", "size": 330},
    {"name": "ch_39", "src": F / "Zeekr_7X_007_d045be.jpg", "num": "39", "word": "NO PAÍS INTEIRO", "size": 300},
    {"name": "ch_12", "src": F / "MG_Cyberster_005_895b40.jpg", "num": "12", "word": "CYBERSTER NO MÊS", "size": 300},
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
