"""Pięć miniaturek "Polski samochód elektryczny" (pl) — ZŁOTA liczba przy BIAŁYM słowie, jedna linia, Anton.
Każda liczba pada w narracji: 450 tysięcy aut rocznie w Jaworznie; 4,5 mld zł z KPO; 70% polskich komponentów;
35 tysięcy miejsc pracy w Volkswagenie; auta z linii w 2029.
Użycie: python make_thumb_izera.py -> out/thumbnails/pl_*.jpg + qa/thumbs_izera/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_izera"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "pl_450tys", "src": P / "BMW_Leipzig_MEDIA_050719_Download_Karosseriebau_max_5ed649.jpg",
     "num": "450 000", "word": "AUT ROCZNIE", "size": 215},
    {"name": "pl_45mld", "src": P / "Jaworzno_miejsce_pod_budow_fabryki_samochod_w_elektrycznych_Izera_01_6efaa6.jpg",
     "num": "4,5 MLD ZŁ", "word": "NA FABRYKĘ", "size": 200},
    {"name": "pl_70proc", "src": P / "Manufacturing_equipment_116_c6126a.jpg",
     "num": "70%", "word": "Z POLSKI", "size": 250},
    {"name": "pl_35tys", "src": P / "Wolfsburg_Volkswagenwerk3_de4a4f.jpg",
     "num": "35 000", "word": "ZWOLNIEŃ W VW", "size": 215},
    {"name": "pl_2029", "src": P / "Autostrada_A4_w_Polsce_w_okolicy_Jaworzna_czerwiec_2022_554_b7a5a8.jpg",
     "num": "2029", "word": "POLSKIE AUTO", "size": 240},
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
