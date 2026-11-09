"""Miniaturas "SUVs 2026 Novos Já Estão Caindo aos Pedaços" (pt). Todo número é dito: nota 14, 12 piores, 380 mil,
750 mil reais, número 12. Fotos do Wikimedia Commons (crédito no LEIA-ME)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_suvs"
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
    {"name": "suvs_nota14", "src": foto("File:GMC Acadia in Volcanic Red Tintcoat.jpg"), "num": "NOTA" + NB + "14", "word": "O PIOR SUV DE 2026", "size": 230},
    {"name": "suvs_12piores", "src": foto("File:2025 Chevrolet Equinox LT AWD Convenience Package II in Cacti Green, front right, 2025-05-06.jpg"), "num": "12" + NB + "SUVs", "word": "JÁ CAINDO AOS PEDAÇOS", "size": 240},
    {"name": "suvs_380mil", "src": foto("File:24 GMC Acadia Denali.jpg"), "num": "380" + NB + "MIL", "word": "DONOS RECLAMARAM", "size": 230},
    {"name": "suvs_750mil", "src": foto("File:2024 Kia EV9 GT-Line AWD 2.jpg"), "num": "R$" + NB + "750" + NB + "MIL", "word": "E A BATERIA FALHA", "size": 190},
    {"name": "suvs_jeep", "src": foto("File:2023 Jeep Grand Cherokee 4xe Summit Reserve.jpg"), "num": "Nº" + NB + "12", "word": "VENDIDO NO BRASIL", "size": 230},
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
