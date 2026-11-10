"""Miniaturas "Como Vive a Tripulação do Avião de US$ 445 Milhões em 16 Horas Sem Pousar" (pt). Todo número é dito:
445 milhões de dólares, 16 horas, 4 pilotos, 5 minutos de água quente, 3 em 3 (beliches). Fotos do Emirates A380 no
Wikimedia Commons (licença livre, crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_a380"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    f = POOL[titulo].get("file")
    p = Path(f) if f else None
    if not p or not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {titulo}")
    return p


SPECS = [
    {"name": "a380_445mi", "src": foto("File:A6-EDK Emirates Airbus A380-861 - cn 030 takeoff from Schiphol runway 36C pic2.JPG"), "num": "US$" + NB + "445" + NB + "MI", "word": "16 HORAS SEM POUSAR", "size": 200},
    {"name": "a380_16h", "src": foto("File:Emirates Airbus A380-861 A6-EER MUC 2015 01.jpg"), "num": "16" + NB + "HORAS", "word": "SEM POUSAR", "size": 240},
    {"name": "a380_4pilotos", "src": foto("File:Airbus A380 cockpit.jpg"), "num": "4" + NB + "PILOTOS", "word": "E UMA CAMA ESCONDIDA", "size": 220},
    {"name": "a380_5min", "src": foto("File:Emirates A380 Shower SPA ITB2014.jpg"), "num": "5" + NB + "MINUTOS", "word": "DE BANHO NO CÉU", "size": 220},
    {"name": "a380_bar", "src": foto("File:Emirates A380 Onboard Lounge ITB 2017 (1).JPG"), "num": "445" + NB + "MI", "word": "O QUE FICA ESCONDIDO", "size": 240},
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
