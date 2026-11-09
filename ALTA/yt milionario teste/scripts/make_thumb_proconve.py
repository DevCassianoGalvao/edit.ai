"""Miniaturas "A Regra Que Expulsou a Subaru do Brasil" (pt). Todo número é dito: R$ 253.900 no site, 34 anos,
janeiro de 2027, cinco cavalos a menos, teto de 50 para 40."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
A = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_proconve"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "pc_253", "src": S / "p576a6c46.jpg", "num": "R$" + NB + "253.900", "word": "SEM COMPRADOR", "size": 200},
    {"name": "pc_2027", "src": A / "2023_Hyundai_HB20_1.0_T-GDi_Platinum_Plus_Brazil_front_view_587090.png", "num": "JAN" + NB + "2027", "word": "A REGRA APERTA", "size": 215},
    {"name": "pc_34", "src": S / "p184316bd.jpg", "num": "34" + NB + "ANOS", "word": "ACABARAM", "size": 240},
    {"name": "pc_5cv", "src": A / "2023_Hyundai_HB20_1.0_T-GDi_Platinum_Plus_Brazil_rear_view_b5c260.png", "num": "5" + NB + "CV", "word": "A MENOS", "size": 260},
    {"name": "pc_50_40", "src": S / "p6ffe0bfe.jpg", "num": "50" + NB + "→" + NB + "40", "word": "TETO DE EMISSÃO", "size": 215},
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
