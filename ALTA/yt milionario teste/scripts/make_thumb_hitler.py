"""Miniaturas "La verdadera razón por la que Hitler nunca invadió Turquía" (es). Todo número é dito:
1941, 90.000 toneladas de cromita, 5,6 meses (Speer), tres bandas. Fotos Wikimedia Commons (créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_hitler"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))


def foto(ini):
    t = next(t for t in POOL if t.startswith("File:" + ini) and POOL[t].get("file") and Path(POOL[t]["file"]).exists())
    return Path(POOL[t]["file"])


SPECS = [
    {"name": "ht_1941", "src": foto("Adolf-Hitler-greets-King-Boris-III"), "num": "1941", "word": "¿POR QUÉ NO INVADIÓ TURQUÍA?", "size": 260},
    {"name": "ht_90mil", "src": foto("Bundesarchiv Bild 101I-635-3965-17"), "num": "90.000 T", "word": "DE CROMO TURCO", "size": 230},
    {"name": "ht_56", "src": foto("Speer Speech 1943"), "num": "5,6 MESES", "word": "SIN CROMO TURCO", "size": 220},
    {"name": "ht_3bandas", "src": foto("Atatürk, İnönü, Bayar"), "num": "3 BANDAS", "word": "EL JUEGO DE İNÖNÜ", "size": 230},
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
