"""Miniaturas "Como o Capitão de um Navio de 400 Metros Come, Toma Banho e Dorme" (pt). Todo número é dito: 400 metros,
4 meses de contrato, 10 horas de descanso, 35 tripulantes, 24 mil contêineres. Fotos Wikimedia Commons (licença livre)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_cap400"
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
    {"name": "cap400_400m", "src": foto("File:MSC IRINA Trivandrum Port.jpg"), "num": "400" + NB + "M", "word": "UM SÓ CAPITÃO", "size": 230},
    {"name": "cap400_4meses", "src": foto("File:Hamburg-Express (2012)-Owners-Bedroom.JPG"), "num": "4 MESES", "word": "DORMINDO AQUI", "size": 200},
    {"name": "cap400_10h", "src": foto("File:6 MV Pollux bridge 220918.jpg"), "num": "10 HORAS", "word": "DE DESCANSO", "size": 200},
    {"name": "cap400_35", "src": foto("File:MSC TESSA (24.116 TEU) (53240860255).jpg"), "num": "35", "word": "PESSOAS A BORDO", "size": 240},
    {"name": "cap400_24mil", "src": foto("File:Vizhinjam Port 2024.jpg"), "num": "24 MIL", "word": "CONTÊINERES", "size": 220},
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
