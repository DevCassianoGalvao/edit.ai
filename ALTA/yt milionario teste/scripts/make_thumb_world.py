"""Miniaturas "Como Vivem os Milionários que Pagam US$ 15 Milhões para Morar em um Navio" (pt). Todo número é dito:
15 milhões de dólares (apartamento), 900 mil dólares por ano (taxa dos maiores), 165 casas, duas cartas de moradores,
280 tripulantes. Fotos do MS The World no Wikimedia Commons (licença livre, crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_world"
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
    {"name": "world_15mi", "src": foto("File:Residential yacht The World in Genoa, Italy.jpg"), "num": "US$" + NB + "15" + NB + "MI", "word": "POR UM APARTAMENTO", "size": 200},
    {"name": "world_900mil", "src": foto("File:Croisière THE WORLD.jpg"), "num": "900" + NB + "MIL", "word": "DÓLARES POR ANO", "size": 220},
    {"name": "world_165", "src": foto("File:Kobe port The World01n4272.jpg"), "num": "165", "word": "CASAS NUM NAVIO", "size": 260},
    {"name": "world_2cartas", "src": foto("File:Croisière THE WORLD au port.jpg"), "num": "2" + NB + "CARTAS", "word": "PARA PODER ENTRAR", "size": 220},
    {"name": "world_280", "src": foto("File:At Tenerife 2021 0033.jpg"), "num": "280", "word": "PESSOAS PARA SERVIR", "size": 260},
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
