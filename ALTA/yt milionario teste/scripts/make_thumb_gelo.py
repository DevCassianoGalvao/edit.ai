"""Miniaturas "Quebra-Gelo Nuclear de US$ 1 Bilhão" (pt). Todo número é dito: 1 bilhão de dólares, 3 metros, 33 mil
toneladas, 2 reatores / 7 anos, motor de 300 toneladas. Fotos do Wikimedia Commons (crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_gelo"
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
    {"name": "gelo_1bilhao", "src": foto("File:Арктика в доке им. Велещинского.jpg"), "num": "US$" + NB + "1" + NB + "BILHÃO", "word": "QUEBRA-GELO NUCLEAR", "size": 200},
    {"name": "gelo_3metros", "src": foto("File:50letPob pole.JPG"), "num": "3" + NB + "METROS", "word": "DE GELO NO CAMINHO", "size": 250},
    {"name": "gelo_33mil", "src": foto('File:Rosatomflot icebreaker "50 Years of Victory".jpg'), "num": "33" + NB + "MIL" + NB + "T", "word": "SOBEM NO GELO", "size": 240},
    {"name": "gelo_2reatores", "src": foto('File:Ледокол "Урал" (проект 22220).jpg'), "num": "2" + NB + "REATORES", "word": "7 ANOS SEM REABASTECER", "size": 220},
    {"name": "gelo_300t", "src": foto("File:С вертолета-2.JPG"), "num": "300" + NB + "TONELADAS", "word": "O MOTOR QUEIMOU", "size": 200},
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
