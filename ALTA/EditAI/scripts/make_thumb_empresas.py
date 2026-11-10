"""Cinco miniaturas "9,1 milhões de empresas com o nome sujo" (pt, painel 20260929-185535). Todo número é dito na
narração: 9,1 milhões; 95%; 2.466 recuperações; 15% de Selic; 82% das famílias."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_empresas"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "empresas_91", "src": S / "pdce079b8.jpg", "num": "9,1 MILHÕES", "word": "DE EMPRESAS NO VERMELHO", "size": 210},
    {"name": "empresas_95", "src": S / "p56fd9ea6.jpg", "num": "95%", "word": "SÃO PEQUENAS", "size": 330},
    {"name": "empresas_2466", "src": S / "pa9f2b41c.jpg", "num": "2.466", "word": "PEDIRAM SOCORRO NA JUSTIÇA", "size": 280},
    {"name": "empresas_15", "src": S / "p0a217f4c.jpg", "num": "15%", "word": "O JURO QUE QUEBRA", "size": 330},
    {"name": "empresas_82", "src": S / "p174523be.jpg", "num": "82%", "word": "DAS FAMÍLIAS ENDIVIDADAS", "size": 330},
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
