"""Cinco miniaturas do filme do MERGULHO DE SATURAÇÃO ($1,400 por dia), no estilo da referência
(número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton).
Todo número é dito na narração: fourteen hundred dollars a day; nine hundred feet; two men; twenty-eight days;
four divers died (North Sea, 1983).
Imagens: fotos do Wikimedia Commons em alta resolução (>= 3000 px) já baixadas em assets/photos.
Uso: python make_thumb_sat.py -> out/thumbnails/sat_*.jpg + qa/thumbs_sat/review.jpg"""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402
P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_sat"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    # o rosto no capacete amarelo: a promessa do título
    {"name": "sat_1400_day", "src": P / "US_Navy_091115-N-4154B-113_Navy_Diver_2nd_Class_Alfred_Pintor_prepares_to_dive_during_diving_operati.jpg",
     "num": "$1,400", "word": "A DAY", "size": 195},
    # dois homens vistos pela vigia da câmara: os 28 dias
    {"name": "sat_28_days", "src": P / "CTG_73_6-MDSU_1-3_Support_DPAA_recovery_Efforts_in_Subic_Bay_April_14_2026_9625754_.jpg",
     "num": "28 DAYS", "word": "SEALED IN", "size": 190},
    # o mergulhador emergindo: os 900 pés
    {"name": "sat_900_feet", "src": P / "US_Navy_110518-N-WL435-218_Chief_Navy_Diver_Ryan_Oakley_assigned_to_Commander_Task_Group_56.jpg",
     "num": "900 FEET", "word": "STRAIGHT DOWN", "size": 185},
    # o arco da solda submarina: os dois homens e a única linha de vida
    {"name": "sat_2_men", "src": P / "Sailor_performs_an_underwater_fillet_weld_in_a_training_pool_at_the_ROK_engineering_school_.jpg",
     "num": "2 MEN", "word": "ONE LIFELINE", "size": 200},
    # a câmara hiperbárica vazia: o acidente de 1983
    {"name": "sat_4_died", "src": P / "CFSSAT_Hyperbaric_Chamber.jpg",
     "num": "4 DIED", "word": "IN A SECOND", "size": 200},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90); print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
