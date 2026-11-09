"""Miniaturas da draga Cristóbal Colón (fr, 19/10/2026). Todo número é dito: quarante-six personnes, 223 mètres,
46 000 m3, 12 heures par jour. Fotos Wikimedia Commons (licença livre; créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_colon"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(*titulos):
    for titulo in titulos:
        f = (POOL.get(titulo) or {}).get("file")
        p = Path(f) if f else None
        if p and p.exists():
            return p
    raise SystemExit(f"[thumb] sem arquivo: {titulos}")


SPECS = [
    {"name": "colon_46", "src": foto("File:Cristóbal Colón photo1.JPG", "File:Cristóbal Colón photo2.JPG"),
     "num": "46", "word": "PERSONNES À BORD", "size": 300},
    {"name": "colon_223m", "src": foto("File:Cristóbal Colón astern.JPG", "File:Cristóbal Colón photo2.JPG"),
     "num": "223" + NB + "M", "word": "D'ACIER", "size": 260},
    {"name": "colon_12h", "src": foto("File:SleephopperzuigerRainbow.JPG", "File:Cristóbal Colón photo2.JPG"),
     "num": "12" + NB + "H", "word": "PAR JOUR, 7 JOURS SUR 7", "size": 280},
    {"name": "colon_46b", "src": foto("File:Cristóbal Colón photo2.JPG", "File:Cristóbal Colón photo1.JPG"),
     "num": "46", "word": "MARINS, UN GÉANT", "size": 300},
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
