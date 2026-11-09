"""Miniaturas "Rio de Janeiro, 1950: como se vivia sem geladeira" (pt, 24/10). Todo número é dito: 1950, 40 graus.
Fotos do Commons/IMS (Copacabana, banhistas, iceman)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_rio"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "rio1950_semgeladeira", "src": g("Vista_a_rea_da_praia_de_Copacabana*.jpg"), "num": "RIO, 1950", "word": "SEM GELADEIRA", "size": 230},
    {"name": "rio1950_40graus", "src": g("Banhistas_na_praia_de_Copacabana*.jpg"), "num": "40 GRAUS", "word": "E NENHUMA GELADEIRA", "size": 250},
    {"name": "rio1950_avenida", "src": g("Avenida_Central_atual_Rio_Branco*.jpg", "Brazil._Ave._Rio_Branco*.jpg"), "num": "1950", "word": "COMO O RIO COMIA", "size": 280},
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
