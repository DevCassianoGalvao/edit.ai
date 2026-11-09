"""Cinco miniaturas de "Siete cosas extrañas del T-34" (español), en el estilo de la referencia:
número DORADO pegado a la palabra BLANCA, una línea, arriba a la izquierda, tipografía Anton.

Todo número se DICE en la narración: las siete cosas; los 90 mm de blindaje efectivo; los 88 mm que fueron
la única respuesta; los más de 12.000 T-34 de 1942; los dos hombres de la torre.
Imágenes: Wikimedia Commons en alta resolución, ya aprobadas en la hoja de contacto.
Uso: python make_thumb_t34.py -> out/thumbnails/t34_*.jpg + qa/thumbs_t34/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_t34"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # el T-34 capturado que los alemanes estudiaron: la imagen que promete el título
    {"name": "t34_siete", "src": P / "Zs_km_nyolt_szovjet_T-34-76_t_pus_harckocsi._Fortepan_12201.jpg",
     "num": "7", "word": "COSAS EXTRAÑAS", "size": 250},
    # el T-34 en marcha: el blindaje inclinado que rebotaba los proyectiles
    {"name": "t34_90mm", "src": P / "T-34_in_marcia.jpg",
     "num": "90 MM", "word": "DE BLINDAJE EFECTIVO", "size": 200},
    # los T-34 abandonados en el campo: la producción que no paraba
    {"name": "t34_12mil", "src": P / "T34_abbandonati_sul_campo_di_battaglia.jpg",
     "num": "12.000", "word": "EN UN SOLO AÑO", "size": 195},
    # el T-34 en Kursk con su tripulación: la torre de dos hombres
    {"name": "t34_dos", "src": P / "T34_Kursk.jpg",
     "num": "2", "word": "HOMBRES EN LA TORRE", "size": 245},
    # el propio 88: el cañón antiaéreo que tuvieron que bajar contra los tanques
    {"name": "t34_88mm", "src": P / "88mm_Flak_Gun_DSC_0019_11794615684_.jpg",
     "num": "88 MM", "word": "LA ÚNICA RESPUESTA", "size": 205},
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
