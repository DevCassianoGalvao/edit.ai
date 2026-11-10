"""Miniaturas "Como é a Vida num Submarino de Cocaína?" (pt, 22/10). Todo número é dito: 27 dias, 3 toneladas, 2 metros
quadrados, 3 homens, 3.068 kg, 11 anos. Fotos do Commons (Narcosubmarino en Aldán, Submarino requisado de Ávila)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_coca"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "coca_27dias", "src": g("Narcosubmarino_en_Ald_n_Cangas_1*.jpg", "Narcosubmarino*.jpg"), "num": "27 DIAS", "word": "DENTRO DESTE CASCO", "size": 250},
    {"name": "coca_3t", "src": g("Narcosubmarino_en_Ald_n_Cangas_3*.jpg", "Narcosubmarino*.jpg"), "num": "3 TONELADAS", "word": "DE COCAÍNA DO BRASIL", "size": 210},
    {"name": "coca_2m2", "src": g("Submarino_requisado*.jpg", "Narcosubmarino*.jpg"), "num": f"2{NB}M²", "word": "PARA 3 HOMENS", "size": 270},
    {"name": "coca_3068", "src": g("Narcosubmarino_en_Ald_n_Cangas_5*.jpg", "Narcosubmarino*.jpg"), "num": f"3.068{NB}KG", "word": "SEM BANHEIRO", "size": 230},
    {"name": "coca_11anos", "src": g("Narcosubmarino_en_Ald_n_Cangas_2*.jpg", "Narcosubmarino*.jpg"), "num": "11 ANOS", "word": "PARA CADA TRIPULANTE", "size": 240},
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
