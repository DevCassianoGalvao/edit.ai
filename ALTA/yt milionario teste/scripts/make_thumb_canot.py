"""Miniatures "Ce qu'il y a dans le canot de sauvetage d'un cargo" (fr). Chaque nombre est dit dans la narration :
3 litres par personne, 55 mètres (record), 133 jours (Poon Lim), 7 coups brefs, 3 minutes.
Photos Wikimedia Commons (licence libre, crédits dans le LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_canot"
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
    {"name": "canot_3litres", "src": foto("File:Freefall lifeboat 1.JPG"), "num": "3" + NB + "LITRES", "word": "PAR MARIN. C'EST TOUT.", "size": 230},
    {"name": "canot_55m", "src": foto("File:Canot de sauvetage à chute libre.jpg"), "num": "55" + NB + "MÈTRES", "word": "DE CHUTE LIBRE", "size": 220},
    {"name": "canot_133j", "src": foto("File:Survival Craft. (16376708897).jpg"), "num": "133" + NB + "JOURS", "word": "À LA DÉRIVE", "size": 220},
    {"name": "canot_7coups", "src": foto("File:Freefall lifeboat of the Bulk carrier W-Smash, August 2021 02.jpg"), "num": "7" + NB + "COUPS", "word": "PUIS ON TOMBE", "size": 230},
    {"name": "canot_3min", "src": foto("File:2016-08 Frachtschiffreise MS Dornbusch Rettungsboot 0409.jpg"), "num": "3" + NB + "MINUTES", "word": "POUR EMBARQUER", "size": 220},
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
