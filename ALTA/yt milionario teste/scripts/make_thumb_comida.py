"""Miniaturas "O Que Acontece com a Comida que Ninguém Come no Maior Navio do Mundo" (pt). Todo número é dito: 10 mil pessoas,
4 horas, 40 mil sobremesas, 14 piscinas olímpicas.
Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_comida"
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
    {"name": "cm_4horas", "src": foto("File:Icon of the Seas (kahunapulej).jpg"), "num": "4" + NB + "HORAS", "word": "DEPOIS VIRA LIXO", "size": 240},
    {"name": "cm_10mil", "src": foto("File:Icon of the Seas (cropped).jpg"), "num": "10" + NB + "MIL", "word": "PESSOAS · E A SOBRA?", "size": 260},
    {"name": "cm_40mil", "src": foto("File:Lower Aft Icon of the Seas 2024.jpg"), "num": "40" + NB + "MIL", "word": "SOBREMESAS POR DIA", "size": 260},
    {"name": "cm_14", "src": foto("File:Biochar pile.jpg"), "num": "14" + NB + "PISCINAS", "word": "DE COMIDA JOGADA FORA", "size": 220},
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
