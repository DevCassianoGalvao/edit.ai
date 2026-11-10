"""Miniaturas "Como 7 Homens Cruzam 360 km do Pantanal a Cavalo com 1.350 Bois" (pt, 23/10). Todo número é dito: 1.350 bois,
7 homens, 360 km, 46 dias, 4 milhões de reais. Fotos do Commons (Pantanal cowboys herding, Brangus, cheia)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_pantanal"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "pantanal_1350", "src": g("DSC00234_Brasil_Pantanal_Cowboys*.jpg"), "num": "1.350 BOIS", "word": "SÓ 7 HOMENS", "size": 230},
    {"name": "pantanal_360km", "src": g("Herd_of_Brahma_Cattle_led_by_Pantaneiro*.jpg"), "num": f"360{NB}KM", "word": "A CAVALO NO PANTANAL", "size": 270},
    {"name": "pantanal_46dias", "src": g("Cattle_being_herded_in_the_Parque*.jpg", "DSC00234*.jpg"), "num": "46 DIAS", "word": "ONDE CAMINHÃO NÃO PASSA", "size": 250},
    {"name": "pantanal_7homens", "src": g("Brangus_35896552563*.jpg"), "num": "7 HOMENS", "word": "1.350 BOIS BRANGUS", "size": 240},
    {"name": "pantanal_4milhoes", "src": g("Cheia_no_Pantanal*.jpg", "DSC00234*.jpg"), "num": "R$ 4 MILHÕES", "word": "ANDANDO A PÉ", "size": 200},
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
