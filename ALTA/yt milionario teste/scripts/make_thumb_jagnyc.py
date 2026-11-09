"""Miniaturas "Jaguar ROZWALA cały rynek" (pl, 20/10). Todo número é dito: 1015 KM, 130 000 £, 3,2 s, 50 000 zainteresowanych."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

S = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_jagnyc"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "jagnyc_1015km", "src": S / "Jaguar_Type_01_Front_at_London_Showroom_7c86b9.jpg", "num": "1015" + NB + "KM", "word": "JAGUAR IS BACK", "size": 230},
    {"name": "jagnyc_130tys", "src": S / "Jaguar_Type_01_Rear_at_London_Showroom_1b9e8e.jpg", "num": "130" + NB + "000" + NB + "£", "word": "BEZ TYLNEJ SZYBY", "size": 210},
    {"name": "jagnyc_type01", "src": S / "Jaguar_Type_00_Side_resized__ef88e9.jpg", "num": "2" + NB + "LATA", "word": "CZEKANIA", "size": 230},
    {"name": "jagnyc_32s", "src": S / "Jaguar_Type_01_Front_at_London_Showroom_7c86b9.jpg", "num": "3,2" + NB + "S", "word": "DO SETKI", "size": 260},
    {"name": "jagnyc_50tys", "src": S / "Jaguar_Type_00_1_bb9ea3.jpg", "num": "50" + NB + "000", "word": "CHĘTNYCH", "size": 260},
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
