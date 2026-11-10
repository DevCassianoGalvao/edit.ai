"""Cinco miniaturas de "Solo tre aziende al mondo" (it) — numero DORATO attaccato alla parola BIANCA, una riga,
in alto a sinistra, font Anton. Foto del Commons >= 1080p sul tema.

Ogni numero è DETTO nella narrazione: le 2.300 tonnellate del motore della Emma Mærsk; le 3 aziende; i 96 cm
di ogni cilindro; gli oltre 100.000 cavalli; l'elica che può superare i 10 metri di diametro.
Uso: python make_thumb_motori.py -> out/thumbnails/mot_*.jpg + qa/thumbs_motori/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_motori"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "mot_2300t", "src": P / "Emma_Maersk_in_Palermo.jpg",
     "num": "2.300 T", "word": "DI MOTORE", "size": 220},
    {"name": "mot_3aziende", "src": P / "Emma_Maersk_ship_2006_IMO_9321483_Schelde_Port_of_Antwerp_pic4.JPG",
     "num": "3", "word": "AZIENDE AL MONDO", "size": 260},
    {"name": "mot_96cm", "src": P / "MS_Bleichen_Maschinenraum_Zylinderk_pfe_mit_Kipphebeln.jpg",
     "num": "96 CM", "word": "PER CILINDRO", "size": 225},
    {"name": "mot_100mila", "src": P / "Cuxhaven_Elbm_ndung_Containerschiff_Ever_Genius_--_2024_--_6169.jpg",
     "num": "100.000", "word": "CAVALLI", "size": 220},
    {"name": "mot_10m", "src": P / "Ship-propeller_2000.jpg",
     "num": "10 M", "word": "DI ELICA", "size": 250},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
