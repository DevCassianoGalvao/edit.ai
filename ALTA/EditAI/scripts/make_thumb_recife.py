"""Miniaturas "Recife, 1950: como as famílias aguentavam o calor" (pt, 26/10). Todo número é dito: 1950, 30 graus.
Fotos do Commons (Recife antigo, redes, casarão)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_recife"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "recife1950_semgeladeira", "src": g("O_Recife_antigo*.jpg", "*Recife_antigo*.jpg"), "num": "RECIFE, 1950", "word": "SEM GELADEIRA", "size": 230},
    {"name": "recife1950_30graus", "src": g("Hammocks_brazil*.jpg", "*ammock*.jpg"), "num": "30 GRAUS", "word": "E NENHUM VENTILADOR", "size": 250},
    {"name": "recife1950_casa", "src": g("Casar*velha_Recife*.jpg", "*Veneza*.jpg"), "num": "1950", "word": "A CASA QUE RESPIRAVA", "size": 280},
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
