"""Miniaturas "Bateu de Leve e o Elétrico Virou Perda Total" (pt). Todo número é dito: 240 mil reais, 2 amassados,
75 %, 20 mil dólares, 25,5 %. Fotos do Wikimedia Commons (crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_seguroev"
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
    {"name": "seguroev_240mil", "src": foto("File:Fiat 500e (2020) Auto Zuerich 2021 IMG 0604.jpg"), "num": "R$" + NB + "240" + NB + "MIL", "word": "POR 2 AMASSADOS", "size": 190},
    {"name": "seguroev_75", "src": foto("File:Volkswagen ID.3 electric car chassis DSC 0060 (52146930872).jpg"), "num": "75" + NB + "%", "word": "E O CARRO JÁ ERA", "size": 250},
    {"name": "seguroev_2amassados", "src": foto("File:Fiat 500e.jpg"), "num": "2" + NB + "AMASSADOS", "word": "PERDA TOTAL", "size": 200},
    {"name": "seguroev_20mil", "src": foto("File:VOLKSWAGEN GROUP MEB PLATFORM DEMO.jpg"), "num": "US$" + NB + "20" + NB + "MIL", "word": "SÓ A BATERIA", "size": 190},
    {"name": "seguroev_255", "src": foto("File:Renault Kwid 1.0 Outsider 2022.jpg"), "num": "+25,5" + NB + "%", "word": "A SEGURADORA SABIA", "size": 220},
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
