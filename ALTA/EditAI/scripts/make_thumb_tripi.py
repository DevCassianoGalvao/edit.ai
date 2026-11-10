"""Miniaturas "Como Vivem os Marinheiros do Maior Porta-Contêineres do Mundo" (pt, 04/11). Todo número é dito: quase 400 metros,
24 mil contêineres, 11 meses, 500 metros de ponto cego, 342 contêineres (MSC Zoe). Fotos do Commons (MSC Irina/Loreto/Tessa)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_tripi"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "tripi_400", "src": g("MSC_IRINA_TRIVANDRUM_PORT_HD*.jpg", "MSC_IRINA*.jpg"), "num": f"400{NB}M", "word": "E POUCOS HOMENS", "size": 250},
    {"name": "tripi_24mil", "src": g("MSC_IRINA_Trivandrum_Port*.jpg", "MSC_IRINA*.jpg"), "num": "24 MIL", "word": "CAIXAS A BORDO", "size": 230},
    {"name": "tripi_11meses", "src": g("MSC_LORETO_52922252347*.jpg", "MSC_Loreto*.jpg"), "num": "11 MESES", "word": "LONGE DE CASA", "size": 210},
    {"name": "tripi_500", "src": g("MSC_LORETO_52922990334*.jpg", "MSC_Loreto*.jpg"), "num": f"500{NB}M", "word": "SEM VER O MAR", "size": 250},
    {"name": "tripi_342", "src": g("Cleaning_up_Terschelling_after_MSC_Zoe_lost_281_containers_31641937427*.jpg", "MSC_TESSA_24.116_TEU*.jpg"), "num": "342", "word": "CAIXAS NO MAR", "size": 260},
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
