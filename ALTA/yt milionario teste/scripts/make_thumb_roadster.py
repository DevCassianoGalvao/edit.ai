"""Miniaturas "Musk Rzuca BOMBĘ — Latający Roadster" (pl). Todo número é dito: 0,81 s, 10 dysz, 9 lat, 250 000 $, 2028.
Fotos do Commons (Roadster 2a geração)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
BA = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_roadster"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "rd_081", "src": F / "Tesla_roadster_2020_prototype_bddc7d.jpg", "num": "0,81 S", "word": "I JEDEN HACZYK", "size": 260},
    {"name": "rd_10", "src": F / "NextGenTeslaRoadster_4ba435.jpg", "num": "10 DYSZ", "word": "ZAMIAST LOTU", "size": 240},
    {"name": "rd_9", "src": F / "The_Wicked-Fast_Next_Gen_Roadster_ac1b01.jpg", "num": "9 LAT", "word": "PUSTYCH OBIETNIC", "size": 300},
    {"name": "rd_250", "src": F / "Tesla_Roadster_2.0_47619421652__e0ba7f.jpg", "num": f"250{NB}000{NB}$", "word": "SAMA REZERWACJA", "size": 200},
    {"name": "rd_2028", "src": F / "Roadster-2020-shareholder-meeting_cd920c.jpg", "num": "2028", "word": "NAPRAWDĘ?", "size": 300},
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
