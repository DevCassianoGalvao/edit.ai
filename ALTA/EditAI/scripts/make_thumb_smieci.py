"""Miniaturas "Gdzie Trafiają Śmieci 10 Tysięcy Ludzi" (pl). Todo número é dito: 10 000 ludzi, 222 palety, 90 %, 7 etapów.
Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_smieci"
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
    {"name": "sm_10000", "src": foto("File:Icon of the Seas (kahunapulej).jpg"), "num": "10" + NB + "000" + NB + "LUDZI", "word": "GDZIE TRAFIAJĄ ŚMIECI?", "size": 200},
    {"name": "sm_222", "src": foto("File:Lower Aft Icon of the Seas 2024.jpg"), "num": "222" + NB + "PALETY", "word": "ŚMIECI CO TYDZIEŃ", "size": 220},
    {"name": "sm_90", "src": foto("File:Icon of the Seas (cropped).jpg"), "num": "90%", "word": "NIGDY NA WYSYPISKO", "size": 260},
    {"name": "sm_7etapow", "src": foto("File:Biochar pile.jpg"), "num": "7" + NB + "ETAPÓW", "word": "OD TALERZA DO ENERGII", "size": 240},
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
