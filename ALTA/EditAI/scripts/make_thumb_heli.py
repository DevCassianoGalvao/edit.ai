"""Miniaturas "Jak Startuje Helikopter Ważący 105 Ton?" (pl). Todo número é dito: 105 ton (W-12), 56 ton (Mi-26),
67 metrów (W-12), 35 metrów (wirnik Mi-6), 40 ton (CH-53K)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_heli"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "heli_105ton", "src": S / "Helicopter_Mi-12_-12_._27646422208__ab759e.jpg", "num": "105" + NB + "TON", "word": "JAK TO LATA?", "size": 270},
    {"name": "heli_56ton", "src": S / "Mi-26_-_MAKS-2013Firstpixflights18_85cd28.jpg", "num": "56" + NB + "TON", "word": "8 ŁOPAT", "size": 270},
    {"name": "heli_67metrow", "src": S / "Mil_V-12_CCCP-21142_27449882099__85d6c2.jpg", "num": "67" + NB + "METRÓW", "word": "DWA WIRNIKI", "size": 240},
    {"name": "heli_35metrow", "src": S / "Mil_Mi-6A_Kyiv_2019_05_253016.jpg", "num": "35" + NB + "METRÓW", "word": "WIRNIK Mi-6", "size": 240},
    {"name": "heli_40ton", "src": S / "Sikorsky_CH-53K_King_Stallion_hovering_in_West_Palm_Beach_on_22_March_2017_170322-M-VU801-_565348.jpg", "num": "40" + NB + "TON", "word": "KING STALLION", "size": 260},
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
