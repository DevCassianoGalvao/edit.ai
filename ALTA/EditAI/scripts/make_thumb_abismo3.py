"""Cinco miniaturas do filme dos predadores do abismo NO ESTILO DA REFERÊNCIA do usuário (18/09): número DOURADO
colado à palavra BRANCA, uma linha, no alto à esquerda, Anton pesada com sombra curta (mesma máquina do filme
da solda: make_thumb_solda.make).

Título: "Caçadores da Escuridão Absoluta: Os Predadores Mais Ferozes a 4 Mil Metros de Profundidade".
Todo número é dito na narração: "a quatro mil metros"; "quatrocentos quilos" por centímetro quadrado; "quase dez
por cento do comprimento total do corpo" (mandíbula do duende); "mais de quatro anos consecutivos" sem comer;
"cinquenta toneladas" (cachalote).
Fotos: Commons ≥ 3 700 px (só reduz) e dois quadros 1080p nativos dos vídeos de pesquisa (sem ampliação).
Uso: python make_thumb_abismo3.py -> out/thumbnails/ab3_*.jpg + qa/thumbs_abismo3/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

F = ROOT / "assets" / "photos"
QA = ROOT / "qa" / "thumbs_abismo3"


def recorta(src, rec, out):
    """rec = (zoom, cx, cy): aproxima no bicho antes do corte 16:9 (nunca amplia: o arquivo tem 3 700 px+)."""
    im = Image.open(src).convert("RGB")
    z, cx, cy = rec
    iw, ih = im.size
    nw, nh = int(iw * z), int(ih * z)
    x = min(max(int(iw * cx - nw / 2), 0), iw - nw)
    y = min(max(int(ih * cy - nh / 2), 0), ih - nh)
    im.crop((x, y, x + nw, y + nh)).save(out, quality=97)
    return out


SPECS = [
    # peixe-víbora de boca aberta (Ifremer, 4608 px, CC BY 4.0)
    {"name": "ab3_4mil_metros", "src": recorta(F / "Grand_croc_petit_fil_Chauliodus_sloani_de_M_diterran_e_Ifremer_00676-78846_-_31646_.jpg", (1.0, 0.5, 0.5), F / "_t_viper.jpg"),
     "num": "4 MIL", "word": "METROS", "size": 210},
    # tubarão-duende com a mandíbula projetada (Pengo, 2560 px, CC BY-SA 3.0 — reduz para 1920, não amplia)
    {"name": "ab3_10pct_corpo", "src": recorta(F / "thumb_goblin.jpg", (0.92, 0.5, 0.5), F / "_t_goblin.jpg"),
     "num": "10%", "word": "DO CORPO", "size": 200},
    # peixe-pescador Sladenia sobre a rocha (quadro 1080p nativo, GFOE — sem texto)
    {"name": "ab3_400kg", "src": F / "frame_angler_front.png",
     "num": "400 KG", "word": "POR CM²", "size": 200},
    # isópode-gigante (5472 px, CC BY-SA 2.0)
    {"name": "ab3_4anos", "src": recorta(F / "Giant_Isopod_18443864634_.jpg", (0.9, 0.5, 0.5), F / "_t_isopod.jpg"),
     "num": "4 ANOS", "word": "SEM COMER", "size": 200},
    # cachalote com filhote (5115 px, CC BY-SA 2.0)
    {"name": "ab3_50_toneladas", "src": recorta(F / "thumb_spermwhale.jpg", (0.9, 0.5, 0.45), F / "_t_whale.jpg"),
     "num": "50", "word": "TONELADAS", "size": 210},
]


def main():
    QA.mkdir(parents=True, exist_ok=True)
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
