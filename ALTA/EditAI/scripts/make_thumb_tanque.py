"""Miniaturas "Dentro de un tanque de guerra" (es). Todo número é dito: 50 grados, cinco hombres, 30 o 40 bajo cero,
tres días, 30 horas despierto. Fotos Wikimedia Commons (IWM, Bundesarchiv CC-BY-SA, SA-kuva; créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_tanque"
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
    {"name": "tq_50grados", "src": foto("File:Sergeant A G Williams of the 17th-21st Lancers in the turret of his Sherman tank at San Angelo in Italy, April 1944. TR1702.jpg"), "num": "50" + NB + "°C", "word": "DENTRO DEL TANQUE", "size": 240},
    {"name": "tq_5hombres", "src": foto("File:KV-1 tank crew (17th Tank Bridage).jpg"), "num": "5", "word": "HOMBRES ENCERRADOS", "size": 280},
    {"name": "tq_menos40", "src": foto("File:Bundesarchiv Bild 101I-689-0190-07, Russland, Panzer IV.jpg"), "num": "-40" + NB + "°C", "word": "DENTRO DEL ACERO", "size": 230},
    {"name": "tq_3dias", "src": foto("File:Sa-kuva-143774.jpg"), "num": "3" + NB + "DÍAS", "word": "SIN SALIR", "size": 250},
    {"name": "tq_30horas", "src": foto("File:Bundesarchiv Bild 101I-113-0029-13, Nordeuropa, Panzer IV.jpg"), "num": "30" + NB + "HORAS", "word": "SIN DORMIR", "size": 230},
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
