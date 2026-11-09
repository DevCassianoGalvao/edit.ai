"""Miniaturas CHAMATIVAS v2 (a v1 foi reprovada: "feia").

Regras mantidas do PROMPT_v: quadro do próprio filme, em força total (nada escurecido), objeto enchendo o quadro,
no máximo DUAS palavras numa linha, num canto vazio, sem faixa/sobretítulo.
O que muda: correção de cor (contraste, saturação, nitidez, leve calor), tipografia pesada gigante,
1ª palavra branca + 2ª âmbar, contorno grosso + sombra longa, teste a 210 px.
Uso: python make_thumb2.py spec.json   -> out/thumbnails/v2_<nome>.jpg + _210px.png + qa/thumbs2/review.jpg
spec = [{"name", "src", "crop": [x0,y0,x1,y1] (px da origem, ajustado a 16:9), "words": ["BRANCO", "AMBAR"],
         "corner": "tl|tr|bl|br", "size": 230, "font": "impact|ariblk|seguibl"}]
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = {"impact": "C:/Windows/Fonts/impact.ttf", "ariblk": "C:/Windows/Fonts/ariblk.ttf", "seguibl": "C:/Windows/Fonts/seguibl.ttf"}
AMBER, WHITE = (255, 184, 28), (255, 255, 255)
W, H = 1280, 720


def fit169(x0, y0, x1, y1, iw, ih):
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    if w / h > 16 / 9:
        h = w * 9 / 16
    else:
        w = h * 16 / 9
    w, h = min(w, iw), min(h, ih)
    x0 = min(max(0, cx - w / 2), iw - w)
    y0 = min(max(0, cy - h / 2), ih - h)
    return int(x0), int(y0), int(x0 + w), int(y0 + h)


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.35)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    r, g, b = im.split()  # leve aquecimento nos claros (céu/sol mais "vivo")
    r = r.point(lambda v: min(255, int(v * 1.04)))
    b = b.point(lambda v: int(v * 0.98))
    im = Image.merge("RGB", (r, g, b))
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=90, threshold=2))
    return im


def draw_title(im, words, corner, size, font_key):
    font = ImageFont.truetype(FONTS[font_key], size)
    gap = int(size * 0.22)
    dr = ImageDraw.Draw(im)
    widths = [dr.textlength(w, font=font) for w in words]
    total = sum(widths) + gap * (len(words) - 1)
    while total > W * 0.62 and size > 90:
        size -= 8
        font = ImageFont.truetype(FONTS[font_key], size)
        gap = int(size * 0.22)
        widths = [dr.textlength(w, font=font) for w in words]
        total = sum(widths) + gap * (len(words) - 1)
    m = 42
    asc, desc = font.getmetrics()
    x = m if corner in ("tl", "bl") else W - m - total
    y = m - int(size * 0.08) if corner in ("tl", "tr") else H - m - asc - int(size * 0.02)
    # sombra longa e suave (só atrás das letras)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    xx = x
    for wd, wdt in zip(words, widths):
        sd.text((xx + 10, y + 12), wd, font=font, fill=(0, 0, 0, 230), stroke_width=10, stroke_fill=(0, 0, 0, 230))
        xx += wdt + gap
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    im = Image.alpha_composite(im.convert("RGBA"), sh)
    dr = ImageDraw.Draw(im)
    xx = x
    for i, (wd, wdt) in enumerate(zip(words, widths)):
        fill = WHITE if (i == 0 and len(words) > 1) else AMBAR_OR(len(words))
        dr.text((xx, y), wd, font=font, fill=fill, stroke_width=max(6, size // 22), stroke_fill=(0, 0, 0))
        xx += wdt + gap
    return im.convert("RGB")


def AMBAR_OR(n):
    return AMBER


def main():
    spec = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    outdir = ROOT / "out" / "thumbnails"
    outdir.mkdir(parents=True, exist_ok=True)
    tiles = []
    for s in spec:
        src = Image.open(ROOT / s["src"]).convert("RGB")
        box = fit169(*(s.get("crop") or (0, 0, src.width, src.height)), src.width, src.height)
        im = grade(src.crop(box).resize((W, H), Image.LANCZOS))
        im = draw_title(im, s["words"], s.get("corner", "tr"), s.get("size", 230), s.get("font", "impact"))
        p = outdir / f"v2_{s['name']}.jpg"
        im.save(p, quality=93)
        small = im.resize((210, 118), Image.LANCZOS)
        small.save(outdir / f"v2_{s['name']}_210px.png")
        tiles.append((im, small, s["name"]))
        print("[thumb2]", p, "crop", box)
    rev = Image.new("RGB", (W // 2 * 2 + 20, (H // 2 + 20) * ((len(tiles) + 1) // 2) + 150), (28, 28, 28))
    for i, (im, small, n) in enumerate(tiles):
        x, y = (i % 2) * (W // 2 + 10), (i // 2) * (H // 2 + 20)
        rev.paste(im.resize((W // 2, H // 2)), (x, y))
        rev.paste(small, (x + W // 2 - 220, y + H // 2 - 128))
    rev.save(ROOT / "qa" / "thumbs2" / "review.jpg", quality=85)
    print("[thumb2] qa/thumbs2/review.jpg")


if __name__ == "__main__":
    main()
