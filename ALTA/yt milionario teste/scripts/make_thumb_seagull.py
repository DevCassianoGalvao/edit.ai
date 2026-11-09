"""Miniaturas "Engenheiros Americanos Desmontaram o BYD Mais Barato da China — O Preço no Brasil Vai Te Irritar" (pt).
Todo número é dito: R$ 119.990, 43 mil reais, quase 3 vezes, 400 quilos, um único limpador. Fotos do Commons."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_seagull"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "seagull_119990", "src": F / "BYD_DOLPHIN_MINI_BRAZIL_BYD_SEAGULL_6343e8.jpg", "num": "R$" + NB + "119.990", "word": "NO BRASIL", "size": 210},
    {"name": "seagull_43mil", "src": F / "2025_BYD_Seagull_EV_in_Sprout_Green_front_left_70f0c2.jpg", "num": "R$" + NB + "43" + NB + "MIL", "word": "NA CHINA", "size": 230},
    {"name": "seagull_3x", "src": F / "BYD_Seagull_Seashell_Pink_01_3e2e93.jpg", "num": "3X", "word": "MAIS CARO AQUI", "size": 300},
    {"name": "seagull_400kg", "src": F / "BYD_Seagull_EV_Sprout_Green_-_front_55d0da.jpg", "num": "400" + NB + "KG", "word": "MAIS LEVE", "size": 260},
    {"name": "seagull_1limpador", "src": F / "2023_BYD_Seagull_front__587566.jpg", "num": "1", "word": "LIMPADOR SÓ", "size": 320},
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
