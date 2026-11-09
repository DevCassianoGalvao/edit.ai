"""Miniaturas do filme do trem no modelo aprovado pelo usuario (16/09): quadro do proprio filme ocupando tudo,
texto no alto a esquerda em UMA linha, NUMERO em dourado colado a PALAVRA em branco, fonte pesada e sombra.

Todo numero tem que estar DITO na narracao (roteiro: two miles, 180 cars, 19,000 tons, 4,400 hp, 660,000 lb, two people).
Uso: python make_thumb_tren.py -> out/thumbnails/tren_*.jpg + qa/thumbs_tren/review.jpg (640 px e 210 px lado a lado)
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "qa" / "thumbs_tren" / "orig"   # quadros tirados do ARQUIVO ORIGINAL baixado (qualidade cheia)
FRAMES = ROOT / "qa" / "thumbs_tren" / "full"
W, H = 1920, 1080   # 16/09: as 1as saiam de quadro do filme ja renderizado (comprimido 2x) e ficavam moles
FONT_PATH = "C:/Windows/Fonts/seguibl.ttf"
GOLD, WHITE = (232, 163, 45), (255, 255, 255)

SPECS = [
    # quadro = arquivo PNG extraido do original em resolucao cheia; escolhidos onde o TREM domina a tela
    {"name": "tren_2_miles", "src": "-bZtCNGaDQU_3.png", "num": "2", "word": "MILES OF TRAIN", "size": 200},
    {"name": "tren_19000_tons", "src": "N3VjUp9oz8o_2.png", "num": "19,000", "word": "TONS", "size": 200},
    {"name": "tren_660000_lb", "src": "N3VjUp9oz8o_3.png", "num": "660,000", "word": "LB", "size": 205},
    {"name": "tren_2_people", "src": "N3VjUp9oz8o_4.png", "num": "2", "word": "PEOPLE", "size": 215},
    {"name": "tren_180_cars", "src": "-bZtCNGaDQU_0.png", "num": "180", "word": "CARS", "size": 210},
]


def frame(spec):
    return Image.open(ORIG / spec["src"]).convert("RGB")


def fit169(im, crop=None):
    if crop:
        im = im.crop(tuple(crop))
    iw, ih = im.size
    if iw / ih > 16 / 9:
        nw = int(ih * 16 / 9); x = (iw - nw) // 2; im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw * 9 / 16); y = (ih - nh) // 2; im = im.crop((0, y, iw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def make(spec):
    im = fit169(frame(spec), spec.get("crop"))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.15)
    size = spec["size"]
    probe = ImageDraw.Draw(im)
    while True:
        fnum = ImageFont.truetype(FONT_PATH, size)
        fword = ImageFont.truetype(FONT_PATH, int(size * 0.62))
        wn = probe.textlength(spec["num"], font=fnum)
        ww = probe.textlength(spec["word"], font=fword)
        if wn + 14 + ww <= W * 0.66 or size < 60:
            break
        size -= 6
    x, margin = 84, 78
    bn = probe.textbbox((0, 0), spec["num"], font=fnum)
    bw = probe.textbbox((0, 0), spec["word"], font=fword)
    base = margin + (bn[3] - bn[1])
    y_num, y_word = base - bn[3], base - bw[3]
    x_word = x + wn + 14
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    ds.text((x + 7, y_num + 10), spec["num"], font=fnum, fill=(0, 0, 0, 205))
    ds.text((x_word + 7, y_word + 10), spec["word"], font=fword, fill=(0, 0, 0, 205))
    out_im = Image.alpha_composite(im.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(out_im)
    d.text((x, y_num), spec["num"], font=fnum, fill=GOLD + (255,))
    d.text((x_word, y_word), spec["word"], font=fword, fill=WHITE + (255,))
    out = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out_im.convert("RGB").save(out, quality=95, subsampling=0)
    print("[thumb]", out.name, f"{spec['num']} {spec['word']} - {size}px")
    return out


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    sheet = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (20, 20, 20))
    for i, p in enumerate(outs):
        im = Image.open(p)
        sheet.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        sheet.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    review = ROOT / "qa" / "thumbs_tren" / "review.jpg"
    review.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(review, quality=90)
    print("[review]", review)


if __name__ == "__main__":
    main()
