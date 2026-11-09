"""Cinco miniaturas no MODELO DA REFERÊNCIA que o usuário mandou (o submarino com "160 MILITARES"):
número em DOURADO colado à palavra em BRANCO, uma linha, no alto à esquerda, fonte pesada e sombra curta.

Título do filme: "Aircraft You Can Legally Fly Without a Pilot License in America".
Ênfase pedida: as aeronaves de asa flexível/planador e foto de alta qualidade.

Fonte das imagens: Wikimedia Commons em 2400–6720 px (licença livre; crédito em qa/thumb_ultra2/fotos/ficha.json).
Todo número é dito na narração: dez aeronaves; 254 libras vazio; 55 nós no máximo; 5 galões de combustível;
"under nineteen thousand dollars" para o Quicksilver pronto para voar.
Uso: python make_thumb_ultra2.py -> out/thumbnails/ref_*.jpg + qa/thumb_ultra2/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "qa" / "thumb_ultra2" / "fotos"
W, H = 1920, 1080
FONT_PATH = str(ROOT / "public" / "fonts" / "Anton.ttf")
GOLD, WHITE = (232, 163, 45), (255, 255, 255)

SPECS = [
    # trike de asa flexível voando junto com um bando de gansos — a imagem mais forte do acervo
    {"name": "ref_10_aircraft", "src": F / "filme_Powered_hang_glider_Exxtacy_BI_Truster_in_Styria.JPG",
     "num": "10", "word": "AIRCRAFT", "size": 200},
    # o Aerolite 103, em 6000 px
    {"name": "ref_254_pounds", "src": F / "Aero-Works_Aerolite_103_Alina_4-12-2024_.jpg",
     "num": "254", "word": "POUNDS", "size": 190},
    # trike vermelho e amarelo em voo contra o céu limpo
    {"name": "ref_55_knots", "src": F / "filme_Ultralight_Trike_01.JPG",
     "num": "55", "word": "KNOTS", "size": 200},
    # CGS Hawk Ultra, em 6000 px
    {"name": "ref_5_gallons", "src": F / "filme_CGS_Hawk_Ultra_4-11-2024_.jpg",
     "num": "5", "word": "GALLONS", "size": 200},
    # Quicksilver no hangar: o "pronto para voar por menos de 19 mil"
    {"name": "ref_19k_ready", "src": F / "filme_2016-07-24_37_Powered_hang_glider_in_Jakabsz_ll_s.jpg",
     "num": "$19,000", "word": "READY", "size": 170},
]


def fit169(im):
    iw, ih = im.size
    if iw / ih > 16 / 9:
        nw = int(ih * 16 / 9); x = (iw - nw) // 2; im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw * 9 / 16); y = (ih - nh) // 2; im = im.crop((0, y, iw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def make(spec):
    im = fit169(Image.open(spec["src"]).convert("RGB"))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.12)
    size = spec["size"]
    probe = ImageDraw.Draw(im)
    while True:  # número + palavra na mesma linha, até 72% da largura
        fnum = ImageFont.truetype(FONT_PATH, size)
        fword = ImageFont.truetype(FONT_PATH, int(size * 0.66))
        wn = probe.textlength(spec["num"], font=fnum)
        ww = probe.textlength(spec["word"], font=fword)
        if wn + 16 + ww <= W * 0.72 or size < 70:
            break
        size -= 6
    x, margem = 86, 74
    bn = probe.textbbox((0, 0), spec["num"], font=fnum)
    bw = probe.textbbox((0, 0), spec["word"], font=fword)
    base = margem + (bn[3] - bn[1])
    y_num, y_word = base - bn[3], base - bw[3]
    x_word = x + wn + 16
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    ds.text((x + 6, y_num + 9), spec["num"], font=fnum, fill=(0, 0, 0, 210), stroke_width=10, stroke_fill=(0, 0, 0, 210))
    ds.text((x_word + 6, y_word + 9), spec["word"], font=fword, fill=(0, 0, 0, 210), stroke_width=10, stroke_fill=(0, 0, 0, 210))
    out = Image.alpha_composite(im.convert("RGBA"), sombra.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(out)
    d.text((x, y_num), spec["num"], font=fnum, fill=GOLD + (255,), stroke_width=3, stroke_fill=(20, 12, 0, 255))
    d.text((x_word, y_word), spec["word"], font=fword, fill=WHITE + (255,), stroke_width=3, stroke_fill=(10, 10, 12, 255))
    dst = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(dst, quality=95, subsampling=0)
    print("[thumb]", dst.name, f"{spec['num']} {spec['word']} - {size}px")
    return dst


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumb_ultra2" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=92)
    print("[review]", rev)


if __name__ == "__main__":
    main()
