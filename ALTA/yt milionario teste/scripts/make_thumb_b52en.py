"""Miniaturas "B-52D — six seats ranked" (en, 19/10). Todo número é dito: six seats, 108 bombs, 164 missiles,
15 Stratofortresses lost, 250 feet. Fotos Wikimedia Commons (USAF/DoD e CC; créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_b52en"
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
    {"name": "b52en_6seats", "src": foto("File:B-52D dropping bombs.jpg"), "num": "6" + NB + "SEATS", "word": "RANKED BY RISK", "size": 250},
    {"name": "b52en_tail", "src": foto("File:B-52 tail turret.jpg"), "num": "SEAT" + NB + "6", "word": "THE DEADLIEST SEAT", "size": 250},
    {"name": "b52en_164", "src": foto("File:S-75 Desna (SA-2B Guideline) missile – NASM Udvar Hazy Center.jpg"), "num": "164", "word": "MISSILES IN ONE NIGHT", "size": 280},
    {"name": "b52en_108", "src": foto("File:B-52D. Wpn loading(USAF) copy (7257085108).jpg"), "num": "108", "word": "BOMBS PER B-52D", "size": 280},
    {"name": "b52en_250ft", "src": foto("File:B-52 cockpit.jpg"), "num": "250" + NB + "FT", "word": "OR YOU HIT THE GROUND", "size": 250},
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
