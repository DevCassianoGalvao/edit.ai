"""Miniaturas \"La verdadera razón por la que Londres y París no declararon la guerra a Stalin en 1939\" (es). Todo número é dito:
1939, dos ejércitos, 17 de septiembre, 1940 (Bakú). Fotos Wikimedia Commons."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_londres"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))


def foto(ini):
    t = next(t for t in POOL if t.startswith("File:" + ini) and POOL[t].get("file") and Path(POOL[t]["file"]).exists())
    return Path(POOL[t]["file"])


SPECS = [
    {"name": "lp_1939", "src": foto("Bundesarchiv Bild 101I-121-0011A-23"), "num": "1939", "word": "¿POR QUÉ NO A STALIN?", "size": 260},
    {"name": "lp_2ejercitos", "src": foto("Bundesarchiv Bild 101I-121-0012-30"), "num": "2 EJÉRCITOS", "word": "UNA SOLA GUERRA", "size": 220},
    {"name": "lp_17sep", "src": foto("Wojska Armii Czerwonej na ulicach Lwowa"), "num": "17 DE SEPTIEMBRE", "word": "STALIN ENTRA EN POLONIA", "size": 170},
    {"name": "lp_baku", "src": foto("Baku-promyselraiway"), "num": "1940", "word": "BOMBAS SOBRE BAKÚ", "size": 260},
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
