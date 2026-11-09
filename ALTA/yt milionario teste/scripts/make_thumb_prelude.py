"""Miniaturas "Encerrados en la Fábrica Flotante Más Grande del Mundo: Prelude, 488 Metros" (es). Todo número é dito:
488 metros, −162 grados, 600.000 toneladas, 200 personas, 19.000 millones. Fotos do Commons (licença no attribution)."""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_prelude"
QA.mkdir(parents=True, exist_ok=True)
NB = " "
SPECS = [
    {"name": "prelude_488metros", "src": F / "Morecambe_North_gas_platform_DPPA__9441c0.jpg", "num": "488" + NB + "METROS", "word": "ENCERRADOS EN EL MAR", "size": 250},
    {"name": "prelude_162grados", "src": F / "Frosty_cross_40574248682__09b296.jpg", "num": "−162" + NB + "°C", "word": "GAS CONVERTIDO EN LÍQUIDO", "size": 270},
    {"name": "prelude_600mil", "src": F / "North_Sea_Oil_Rig_7573694644__545068.jpg", "num": "600.000" + NB + "TONELADAS", "word": "FLOTANDO", "size": 210},
    {"name": "prelude_200personas", "src": F / "Hemmingsedt_raffinerie_turm_ganz_nah_bfa923.jpg", "num": "200" + NB + "PERSONAS", "word": "SIN PODER SALIR", "size": 250},
    {"name": "prelude_19mil", "src": F / "Offshore_oil_and_gas_production_contributes_to_America_s_Energy_Future_35440893341__5a2b64.jpg", "num": "19.000" + NB + "MILLONES", "word": "LA FÁBRICA PARADA", "size": 220},
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
