"""Miniaturas "Największy na świecie statek 382 m: Jak Pioneering Spirit podnosi 48 000 ton bez dźwigu?" (pl). Todo número
é dito: 48 000 ton, 382 metry, 31 000 ton, 9 sekund, 124 metry. Fotos do Commons (licença no attribution)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_pioneer"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "pioneer_48000ton", "src": F / "Pioneering_Spirit_-_Biggest_ship_of_the_world_-_Port_of_Rotterdam_28205610483__9ac6a8.jpg", "num": "48" + NB + "000" + NB + "TON", "word": "BEZ DŹWIGU", "size": 230},
    {"name": "pioneer_382m", "src": F / "Pioneering_Spirit_ship_2014_002_70315f.jpg", "num": "382" + NB + "M", "word": "NAJWIĘKSZY STATEK ŚWIATA", "size": 270},
    {"name": "pioneer_31000ton", "src": F / "Pioneering_Spirit_28146160733__62d579.jpg", "num": "31" + NB + "000" + NB + "TON", "word": "W JEDNYM KAWAŁKU", "size": 230},
    {"name": "pioneer_9sekund", "src": F / "PIONEERING_SPIRIT_50291262853__2dda0b.jpg", "num": "9" + NB + "SEKUND", "word": "I PLATFORMA ZNIKA", "size": 260},
    {"name": "pioneer_124m", "src": F / "Pieter_Schelte_IMO_9593505_at_the_Tweede_Maasvlakte_Port_of_Rotterdam_pic_282852.jpg", "num": "124" + NB + "M", "word": "SZEROKOŚCI", "size": 270},
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
