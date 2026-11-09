"""Cinco miniaturas "O motor a água da Toyota" (pt, pedido do painel car-pt). Todo número é dito na narração:
quase 2.000 km (boato); 1.360 km com um único tanque (recorde Guinness); zero emissões; ~30 % da energia; 24 horas em Fuji."""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "public" / "stock"
QA = ROOT / "qa" / "thumbs_car"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "car_2000", "src": S / "p024dd36e.jpg", "num": "2.000 KM", "word": "COM ÁGUA DA TORNEIRA?", "size": 230},
    {"name": "car_1360", "src": S / "p565bf908.jpg", "num": "1.360 KM", "word": "COM UM ÚNICO TANQUE", "size": 230},
    {"name": "car_zero", "src": S / "p96bb631a.jpg", "num": "ZERO", "word": "O MOTOR A ÁGUA DA TOYOTA", "size": 300},
    {"name": "car_30", "src": S / "p8075f70e.jpg", "num": "30%", "word": "DA ENERGIA CHEGA À RODA", "size": 300},
    {"name": "car_24h", "src": S / "p147ef034.jpg", "num": "24 H", "word": "A HIDROGÊNIO EM FUJI", "size": 300},
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
