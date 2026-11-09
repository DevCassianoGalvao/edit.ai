"""Miniaturas "Hallaron 28 humanos en un pozo de 430.000 años" (es). Todo número é dito: 28 humanos, 430.000 años,
13 metros de caída libre, dos golpes (Cráneo 17), 80 por ciento. Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_sima"
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
    {"name": "sima_28", "src": foto("File:Em - European Homo heidelbergensis - 1.jpg"), "num": "28", "word": "HUMANOS EN UN POZO", "size": 260},
    {"name": "sima_430000", "src": foto("File:Miguelon - MCN 4149.jpg"), "num": "430.000", "word": "AÑOS", "size": 220},
    {"name": "sima_13m", "src": foto("File:Atapuerca, excavación Galería.jpg"), "num": "13" + NB + "M", "word": "DE CAÍDA LIBRE", "size": 240},
    {"name": "sima_2golpes", "src": foto("File:Homo heidelbergensis.004 - Domus (A Coruña).jpg"), "num": "2" + NB + "GOLPES", "word": "EL CRIMEN MÁS ANTIGUO", "size": 200},
    {"name": "sima_80", "src": foto("File:Homo heidelbergensis.502 - Domus (A Coruña).jpg"), "num": "80" + NB + "%", "word": "DE LOS FÓSILES DEL MUNDO", "size": 240},
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
