"""Cinco miniaturas de "A vida a bordo de um porta-contêineres gigante" (pt), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: os onze meses sem pisar em terra; os quatrocentos metros de comprimento;
as vinte e cinco pessoas a bordo; os cem decibéis da casa de máquinas; os vinte e quatro mil contêineres.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_navio.py -> out/thumbnails/navio_*.jpg + qa/thumbs_navio/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_navio"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "navio_11meses", "src": P / "Cargo_naviguant_par_temp_te_en_mer_M_diterran_e_Ifremer_00766-87770_-_46843_.jpg", "num": "11", "word": "MESES SEM DESCER", "size": 240},
    {"name": "navio_400m", "src": P / "Aankomst_Ever_Glory_groen_gestuwd_20.000_TEU_containerschip_48060357263_.jpg", "num": "400 M", "word": "DE AÇO", "size": 210},
    {"name": "navio_25", "src": P / "Anchors_Away_9552661_.jpg", "num": "25", "word": "PESSOAS A BORDO", "size": 240},
    {"name": "navio_100db", "src": P / "Main_engine_of_Hakkoda_Maru.jpg", "num": "100 DB", "word": "NA CASA DE MÁQUINAS", "size": 190},
    {"name": "navio_24mil", "src": P / "Container_ship_OOCL_Malaysia_at_Skandiahamnen_4.jpg", "num": "24.000", "word": "CONTÊINERES", "size": 200},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
