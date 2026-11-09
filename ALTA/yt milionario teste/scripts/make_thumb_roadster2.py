"""Miniaturas "Tesla Rzuca BOMBĘ — Nowy Roadster z Napędem SpaceX" (pl). Todo número é dito: 600 litrów, 10 dysz,
0,81 s, 250 000 $, 2028. Fotos do Commons (Roadster 2a geração)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_roadster2"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "rs2_600", "src": F / "NextGenTeslaRoadster_4ba435.jpg", "num": f"600{NB}LITRÓW", "word": "GAZU ZAMIAST SILNIKA", "size": 200},
    {"name": "rs2_10", "src": F / "Tesla_roadster_2020_prototype_bddc7d.jpg", "num": "10 DYSZ", "word": "Z TECHNOLOGII SPACEX", "size": 240},
    {"name": "rs2_081", "src": F / "The_Wicked-Fast_Next_Gen_Roadster_ac1b01.jpg", "num": "0,81 S", "word": "FAKT CZY OBIETNICA?", "size": 260},
    {"name": "rs2_250", "src": F / "Tesla_Roadster_2.0_47619421652__e0ba7f.jpg", "num": f"250{NB}000{NB}$", "word": "SAMA ZALICZKA", "size": 200},
    {"name": "rs2_2028", "src": F / "Roadster-2020-shareholder-meeting_cd920c.jpg", "num": "2028", "word": "TESLA RZUCA BOMBĘ", "size": 300},
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
