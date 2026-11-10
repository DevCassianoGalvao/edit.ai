"""Miniaturas "Bajaron una sonda a 700 metros bajo el desierto de Atacama" (es). Todo número é dito: 33 mineros,
700 metros, 17 días, 69 días, siete palabras. Fotos Wikimedia Commons (Gobierno de Chile, licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_mina"
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
    {"name": "mina_33", "src": foto("File:Mina San José -Piñera con mensaje de mineros atrapados(2).jpg"), "num": "33", "word": "ESTABAN VIVOS", "size": 280},
    {"name": "mina_700m", "src": foto("File:12.10.10 Descenso del primer rescatista (5076808127).jpg"), "num": "700" + NB + "M", "word": "BAJO EL DESIERTO", "size": 240},
    {"name": "mina_17dias", "src": foto("File:Pexels 32990236 A dimly lit tunnel in Hinterbrühl, Austria, showcasing an underground cavern..jpg"), "num": "17" + NB + "DÍAS", "word": "SIN SEÑALES", "size": 230},
    {"name": "mina_69dias", "src": foto("File:Final rescue (5080215020).jpg"), "num": "69" + NB + "DÍAS", "word": "BAJO TIERRA", "size": 230},
    {"name": "mina_7palabras", "src": foto("File:LOS 33.jpg"), "num": "7", "word": "PALABRAS ESCRITAS A MANO", "size": 280},
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
