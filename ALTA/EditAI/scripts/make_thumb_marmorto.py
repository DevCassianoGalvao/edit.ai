"""Cinco miniaturas do filme do MAR MORTO, no modelo da referência (número DOURADO colado à palavra BRANCA,
uma linha, no alto à esquerda, fonte pesada e sombra curta).

Título do filme: "O Mar Morto: o que aquela água faz com um corpo vivo".
Todo número aqui é dito na narração: 34% de sal; 430 m abaixo do nível do mar; 25% mais pesado que água doce;
nenhum peixe sobrevive; o nível cai cerca de 1 metro por ano.

Fonte das imagens: Wikimedia Commons em 2400-3840 px (licença livre; crédito em qa/thumb_marmorto/fotos/ficha.json).
Uso: python make_thumb_marmorto.py -> out/thumbnails/mm_*.jpg + qa/thumb_marmorto/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "qa" / "thumb_marmorto" / "fotos"
W, H = 1920, 1080
FONT_PATH = str(ROOT / "public" / "fonts" / "Anton.ttf")
GOLD, WHITE = (232, 163, 45), (255, 255, 255)

SPECS = [
    # o homem boiando de braços abertos: a imagem-símbolo do lago (3840 px)
    {"name": "mm_25_pesado", "src": F / "Effortlessly_floating_on_the_Dead_Sea_11663842305_.jpg",
     "num": "25%", "word": "MAIS PESADO", "size": 190},
    # a torre de sal branca dentro da água turquesa
    {"name": "mm_34_sal", "src": F / "Salt_pillar_at_the_Dead_Sea_Israel_35253925685_.jpg",
     "num": "34%", "word": "DE SAL", "size": 210},
    # a crosta de sal na margem, do lado jordaniano
    {"name": "mm_0_peixes", "src": F / "Salt_Dead_Sea_Jordan.jpg",
     "num": "0", "word": "PEIXES", "size": 220},
    # a parede do vale caindo no lago: dá a ideia de profundidade que a vista de cima não dá
    {"name": "mm_430_abaixo", "src": F / "Dead_Sea_from_Jordan.jpg",
     "num": "430 m", "word": "ABAIXO", "size": 195},
    # o banho de lama, para o trecho do corpo
    {"name": "mm_5_regras", "src": F / "A_guy_enjoying_a_mud_bath_2957458381_.jpg",
     "num": "5", "word": "MECANISMOS", "size": 185},
    # a dolina: o chão que some quando o lago recua
    {"name": "mm_1_metro", "src": F / "Dead_Sea_sinkhole_by_David_Shankbone.jpg",
     "num": "1 METRO", "word": "POR ANO", "size": 175},
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
    rev = ROOT / "qa" / "thumb_marmorto" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=92)
    print("[review]", rev)


if __name__ == "__main__":
    main()
