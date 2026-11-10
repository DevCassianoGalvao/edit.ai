"""Cinco miniaturas de "Challenger and Appendix F" (en), no estilo da referência:
número DOURADO colado à palavra BRANCA, uma linha, no alto à esquerda, fonte Anton.

Todo número é DITO na narração: os 73 segundos até a perda; os 32 °F do copo de água gelada;
o um quarto de polegada do anel de vedação; as mil libras por polegada quadrada dentro do propulsor;
os 300 anos que a conta de "um em cem mil" implicava.
Imagens: Wikimedia Commons em alta resolução, já aprovadas na folha de contato.
Uso: python make_thumb_challenger.py -> out/thumbnails/chl_*.jpg + qa/thumbs_challenger/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_challenger"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "chl_73s", "src": P / "Brightly_lit_STS-135_on_launch_pad_39a.jpg",
     "num": "73", "word": "SECONDS", "size": 250},
    {"name": "chl_32f", "src": P / "Ice_Ice_Baby_152310615_.jpeg",
     "num": "32 °F", "word": "IN A GLASS OF WATER", "size": 195},
    {"name": "chl_quarter", "src": P / "Bialetti-Dichtungsring_verschmort_03_fcm_.jpg",
     "num": "1/4 IN", "word": "OF RUBBER", "size": 205},
    {"name": "chl_1000psi", "src": P / "186484-01_Nozzle_Assemblies_Complete_for_Exploration_Mission-1_Solid_Rocket_Boosters.jpg",
     "num": "1,000", "word": "PSI IN A HEARTBEAT", "size": 195},
    {"name": "chl_300y", "src": P / "Foggy_Rollout_for_Space_Shuttle_Challenger.jpg",
     "num": "300", "word": "YEARS OF LAUNCHES", "size": 235},
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
