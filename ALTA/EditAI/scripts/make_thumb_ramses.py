"""Miniaturas "Hallaron 28 humanos en un pozo de 430.000 años" (es). Todo número é dito: 28 humanos, 430.000 años,
13 metros de caída libre, dos golpes (Cráneo 17), 80 por ciento. Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_ramses"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    for k, v in POOL.items():
        if k.startswith(titulo) and v.get("file") and Path(v["file"]).exists():
            return Path(v["file"])
    raise SystemExit(f"[thumb] sem arquivo: {titulo}")


SPECS = [
    {"name": "ramses_28", "src": foto("File:Papyrus judicial Turin.jpg"), "num": "28", "word": "EJECUTADOS POR EL COMPLOT", "size": 280},
    {"name": "ramses_7cm", "src": foto("File:Sarcophagus of Ramses III in Le Louvre.jpg"), "num": "7" + NB + "CM", "word": "EL CORTE QUE NADIE VIO", "size": 240},
    {"name": "ramses_3000", "src": foto("File:KV11 Tomb of Ramses III DSCF2941.jpg"), "num": "3.000", "word": "AÑOS DESPUÉS, LA PRUEBA", "size": 230},
    {"name": "ramses_1155", "src": foto("File:Medinet Habu Ramses III. Tempelrelief 06.JPG"), "num": "1155", "word": "A.C. · EL ASESINATO", "size": 230},
    {"name": "ramses_2012", "src": foto("File:Sarcophagus and mummy Egyptian Museum Cairo.jpg"), "num": "2012", "word": "LA TOMOGRAFÍA LO REVELÓ", "size": 230},
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
