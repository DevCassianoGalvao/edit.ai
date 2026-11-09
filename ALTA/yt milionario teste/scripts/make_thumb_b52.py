"""Miniaturas "30 horas dentro de un B-52" (es). Todo número é dito: 30 horas, cinco aviadores, 35 horas (Secret Squirrel),
50 grados bajo cero, 45 horas (Power Flite). Fotos Wikimedia Commons (USAF/DoD, domínio público; créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_b52"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    f = POOL[titulo].get("file")
    p = Path(f) if f else None
    if not p or not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {titulo}")
    return p


SPECS = [
    {"name": "b52_30horas", "src": foto("File:20th BS flies over Vegas during Red Flag 130128-F-XF291-288.jpg"), "num": "30" + NB + "HORAS", "word": "DENTRO DEL B-52", "size": 230},
    {"name": "b52_5aviadores", "src": foto("File:28 days in Global Strike 140211-F-RH756-825.jpg"), "num": "5", "word": "AVIADORES ENCERRADOS", "size": 280},
    {"name": "b52_35horas", "src": foto("File:US Navy 100710-F-5964B-368 A KC-135 stratotanker assigned to the 465th Air Refueling Squadron refuels a B-52 stratofortress assigned to the Buccaneers of 20th Expeditionary Bomb Squadron during a sortie supporting Rim of the Pa.jpg"), "num": "35" + NB + "HORAS", "word": "SIN ATERRIZAR", "size": 230},
    {"name": "b52_menos50", "src": foto("File:B-52H Stratofortress (7414115180).jpg"), "num": "-50" + NB + "°C", "word": "AFUERA DEL AVIÓN", "size": 230},
    {"name": "b52_45horas", "src": foto("File:B-52 Stratofortresses conduct nighttime show of presence mission over USCENTCOM (8876018).jpg"), "num": "45" + NB + "HORAS", "word": "SIN DORMIR", "size": 230},
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
