"""Miniaturas "A BYD Soltou uma BOMBA: Bateria Que Carrega em 5 Minutos Pode Acabar com o Posto" (pt). Todo número é
dito: 5 minutos, 1.500 kW, 44 mil postos, mil carregadores. Fotos do Wikimedia Commons (crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_bydflash"
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
    {"name": "bydflash_5min", "src": foto("File:BYD Zhengzhou All-Terrain Circuit Megawatt Charging 02.png"), "num": "5" + NB + "MINUTOS", "word": "E O POSTO?", "size": 240},
    {"name": "bydflash_1500kw", "src": foto("File:Denza Z9 GT IAA 2025 DSC 2034.jpg"), "num": "1.500" + NB + "kW", "word": "A BOMBA DA BYD", "size": 230},
    {"name": "bydflash_44mil", "src": foto("File:Posto Petrobras.jpg"), "num": "44" + NB + "MIL", "word": "POSTOS EM RISCO?", "size": 240},
    {"name": "bydflash_5min_b", "src": foto("File:BYD Zhengzhou All-Terrain Circuit Megawatt Charging 03.png"), "num": "5" + NB + "MIN", "word": "FIM DO POSTO?", "size": 250},
    {"name": "bydflash_mil", "src": foto("File:2025 Denza Z9 GT 1.jpg"), "num": "1.000", "word": "CARREGADORES NO BRASIL", "size": 230},
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
