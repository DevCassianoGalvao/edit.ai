"""Miniaturas "Ninguém Viu o Dolphin Mini Chegando" (pt). Todo número é dito: 4º, 8.299, 3.343 num dia, carro 100 mil,
1º no varejo. Fotos do Commons / banco."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
BA = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_dolphin"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "dm_4lugar", "src": BA / "BYD_DOLPHIN_MINI_BRAZIL_BYD_SEAGULL_6343e8.jpg", "num": "4º", "word": "CARRO MAIS VENDIDO", "size": 330},
    {"name": "dm_8299", "src": F / "BYD_Seagull_EV_Sprout_Green_-_front_55d0da.jpg", "num": "8.299", "word": "DOLPHIN MINI EM AGOSTO", "size": 250},
    {"name": "dm_3343", "src": F / "BYD_Seagull_Seashell_Pink_02_ac666f.jpg", "num": "3.343", "word": "VENDAS NUM ÚNICO DIA", "size": 250},
    {"name": "dm_100mil", "src": F / "09.10.2025_Visita_linha_de_montagem_de_ve_culos_da_BYD_54842306552__a7d6e0.jpg", "num": "100" + NB + "MIL", "word": "CARROS NA BAHIA", "size": 230},
    {"name": "dm_1varejo", "src": F / "BYD_Seagull_EV_2025_757685.jpg", "num": "1º", "word": "NO VAREJO DO BRASIL", "size": 330},
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
