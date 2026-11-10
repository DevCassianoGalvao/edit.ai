"""Miniaturas do filme da SOLDAGEM SUBAQUÁTICA, no modelo da referência (número DOURADO colado à palavra
BRANCA, uma linha, no alto à esquerda, fonte pesada e sombra curta).

Título do filme: os 2 mil dólares por dia e o mito de "1 em 5 morre".
Todo número aqui é dito na narração: $2,000 por dia; 1 em 5 (o mito); $68,000 de mediana; 39 mortes em
2011-2017; 50x a média de todas as indústrias; 28 dias em saturação; $15,000-$30,000 de escola.

Fonte das imagens: Wikimedia Commons em 2400-6000 px (licença livre; crédito em qa/thumb_solda/fotos/ficha.json).
Uso: python make_thumb_solda.py -> out/thumbnails/sw_*.jpg + qa/thumb_solda/review.jpg
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "qa" / "thumb_solda" / "fotos"
W, H = 1920, 1080
FONT_PATH = str(ROOT / "public" / "fonts" / "Anton.ttf")
GOLD, WHITE = (232, 163, 45), (255, 255, 255)

SPECS = [
    # o soldador com o arco aceso: a imagem que o título promete
    {"name": "sw_2000_day", "src": F / "A_Navy_diver_uses_an_underwater_welding_torch._8407482809_.jpg",
     "num": "$2,000", "word": "A DAY", "size": 180},
    # o mergulhador de capacete na água turquesa, para o mito
    {"name": "sw_1in5_myth", "src": F / "Flickr_-_Official_U.S.jpg",
     "num": "1 IN 5", "word": "IS A MYTH", "size": 195},
    # a equipe puxando o umbilical no convés: o salário real do dia a dia
    {"name": "sw_68k_real", "src": F / "US_Navy_100712-N-9769P-353_Navy_Diver_1st_Class_Joel_Sharp_left_assign.jpg",
     "num": "$68,000", "word": "REAL", "size": 175},
    # o homem dentro da câmara: os 28 dias
    {"name": "sw_28_days", "src": F / "Decompression_chamber.jpg",
     "num": "28", "word": "DAYS SEALED", "size": 195},
    # as plataformas do Mar do Norte: a comparação de risco
    {"name": "sw_50x", "src": F / "Oseberg_feltsenter_Nordsj_en_27945050314_.jpg",
     "num": "50×", "word": "THE AVERAGE", "size": 195},
    # o corte com maçarico e faísca embaixo d'água
    {"name": "sw_39_deaths", "src": F / "Navy_Diver_performs_underwater_cutting_operations_using_a_Broco_torch.jpg",
     "num": "39", "word": "DEATHS", "size": 210},
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
    rev = ROOT / "qa" / "thumb_solda" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=92)
    print("[review]", rev)


if __name__ == "__main__":
    main()
