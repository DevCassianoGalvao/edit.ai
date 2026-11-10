"""Miniaturas "Antes do SUS (1988)" (pt, 31/10). Todo número é dito: quase 400 metros,
24.346 TEU, 61 metros de largura, 58 caixas (Ideal X, 1956). Fotos do Commons (MSC Irina/Loreto/Tessa)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_sus"
QA.mkdir(parents=True, exist_ok=True)
NB = " "


def g(*pats):
    for pat in pats:
        r = sorted(F.glob(pat))
        if r:
            return r[0]
    raise SystemExit(f"sem foto: {pats}")


SPECS = [
    {"name": "sus_1988", "src": g("Ulyssesguimaraesconstituicao*.jpg"), "num": "1988", "word": "FIM DO FAVOR", "size": 260},
    {"name": "sus_196", "src": g("Promulga_o-Constitui_o-1988*.jpg", "Constituinte_4987466247*.jpg"), "num": "ARTIGO 196", "word": "SAÚDE É DIREITO", "size": 200},
    {"name": "sus_97", "src": g("Pixabay_5185845*.jpg"), "num": "97,1", "word": "ÓBITOS POR MIL", "size": 230},
    {"name": "sus_1993", "src": g("Fachada_principal_do_Hospital_da_Santa_Casa*.jpg"), "num": "1993", "word": "FIM DO INAMPS", "size": 230},
    {"name": "sus_indigente", "src": g("Santa_Casa_de_Fortaleza_01*.jpg"), "num": "SEM", "word": "CARTEIRA", "size": 260},
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
