"""Miniaturas "Os Maiores Navios Porta-Contêineres Feitos na China" (pt, 31/10). Todo número é dito: quase 400 metros,
24.346 TEU, 61 metros de largura, 58 caixas (Ideal X, 1956). Fotos do Commons (MSC Irina/Loreto/Tessa)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_msc"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "msc_24mil", "src": g("MSC_IRINA_TRIVANDRUM_PORT_HD*.jpg", "MSC_IRINA*.jpg"), "num": "24 MIL", "word": "CONTÊINERES", "size": 230},
    {"name": "msc_400", "src": g("MSC_IRINA_Trivandrum_Port*.jpg", "MSC_IRINA*.jpg"), "num": f"400{NB}M", "word": "DE AÇO", "size": 260},
    {"name": "msc_teu", "src": g("MSC_LORETO_52922252347*.jpg", "MSC_Loreto*.jpg"), "num": f"24.346{NB}TEU", "word": "EM UM NAVIO", "size": 200},
    {"name": "msc_61", "src": g("MSC_LORETO_52922990334*.jpg", "MSC_Loreto*.jpg"), "num": f"61{NB}M", "word": "DE LARGURA", "size": 260},
    {"name": "msc_china", "src": g("MSC_TESSA_24.116_TEU*.jpg", "ROTTERDAM_MSC_TESSA*.jpg"), "num": "FEITO", "word": "NA CHINA", "size": 230},
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
