"""Miniaturas "Os 5 Submarinos Mais Pesados da História" (pt). Todo número é dito na narração: 48 mil toneladas
(Typhoon), 118 homens (Kursk), 108 metros (Kursk), 25 mil toneladas de água (Typhoon), 24 tubos de mísseis (Ohio).
Fotos Wikimedia Commons (licença livre, créditos no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_sub"
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
    {"name": "sub5_48mil", "src": foto("File:Akula (Typhoon) class submarine DD-ST-85-06625.jpg"), "num": "48.000" + NB + "T", "word": "E ELE SOBE", "size": 210},
    {"name": "sub5_118", "src": foto("File:Рубка Курска.jpg"), "num": "118", "word": "HOMENS NO FUNDO", "size": 240},
    {"name": "sub5_108m", "src": foto("File:Прибытие атомного подводного ракетного крейсера Северного флота «Орёл» в пункт постоянного базирования 08.jpg"), "num": "108" + NB + "M", "word": "E NÃO SUBIU", "size": 230},
    {"name": "sub5_25mil", "src": foto("File:Russian Typhoon-class submarine.jpg"), "num": "25.000" + NB + "T", "word": "DE ÁGUA", "size": 210},
    {"name": "sub5_24", "src": foto("File:USS Ohio (SSGN 726) arrives in Brisbane, Australia (9221486).jpg"), "num": "24", "word": "MÍSSEIS NAS COSTAS", "size": 240},
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
