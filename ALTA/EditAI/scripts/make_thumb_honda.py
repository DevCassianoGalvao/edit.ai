"""Miniaturas "Honda Rzuca BOMBĘ — Nowa Hybryda od 2027" (pl, 22/10). Todo número é dito: 15, 2027, 30 %, 21 mld $, 15,7 mld $."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_honda"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(pat):
    return sorted(F.glob(pat))[0]


SPECS = [
    {"name": "honda_15", "src": g("2023_Honda_Accord_LX_front_left_dc0fce.jpg"), "num": "15", "word": "NOWYCH HYBRYD OD 2027", "size": 300},
    {"name": "honda_2027", "src": g("Honda_Civic_FE4_FL_2.0_RS_e-HEV_Ignite_Red_Metallic_02_4999e1.jpg"), "num": "2027", "word": "HONDA RZUCA BOMBĘ", "size": 280},
    {"name": "honda_30", "src": g("Honda_HR-V_eHEV_Advance_III_f_31122023_44f034.jpg"), "num": f"-30{NB}%", "word": "TAŃSZA HYBRYDA", "size": 260},
    {"name": "honda_21mld", "src": g("Honda_Marysville_Auto_Plant_Marysville_Ohio_-_Honda_0_Series_Saloon_concept_01_36a775.jpg"), "num": f"21{NB}MLD{NB}$", "word": "ELEKTRYKI SKASOWANE", "size": 230},
    {"name": "honda_157", "src": g("Honda_Marysville_Auto_Plant_Marysville_Ohio_-_Honda_0_Series_SUV_concept_02_76b0b5.jpg"), "num": f"15,7{NB}MLD{NB}$", "word": "PIERWSZA STRATA OD 70 LAT", "size": 210},
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
