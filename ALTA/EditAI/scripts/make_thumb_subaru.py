"""Miniaturas "A virada da Subaru" (pt). Todo número é dito na narração: trezentos e setenta e cinco cavalos,
quatro elétricos, novecentos e trinta quilômetros, um vírgula cinco trilhão de ienes."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_subaru"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "subaru_375", "src": S / "pa4e88284.jpg", "num": "375" + NB + "CV", "word": "POR MENOS DE US$ 40 MIL", "size": 300},
    {"name": "subaru_4", "src": S / "p1179ee2f.jpg", "num": "4" + NB + "ELÉTRICOS", "word": "EM POUCO MAIS DE 1 ANO", "size": 230},
    {"name": "subaru_930", "src": S / "p2be27969.jpg", "num": "930" + NB + "KM", "word": "COM UM TANQUE", "size": 300},
    {"name": "subaru_trilhao", "src": S / "p0ca53226.jpg", "num": "1,5" + NB + "TRILHÃO", "word": "O PLANO QUE ELA ADIOU", "size": 230},
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
