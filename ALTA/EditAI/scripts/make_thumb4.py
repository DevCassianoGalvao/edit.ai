"""Miniaturas no estilo da referência "LIVING IN CANADA" (usuário, 14/09/2026).

- cena do filme em tela cheia, viva (contraste/saturação leves)
- canto superior direito: linha pequena espaçada ("VIVIR EN") + palavra grande em caixa alta ("NORUEGA"),
  branco com sombra suave, alinhadas pela direita
- canto inferior esquerdo: círculo azul com número/gancho curto em serifa branca
Uso: python make_thumb4.py spec.json -> out/thumbnails/<name>.jpg + qa/thumbs4/review.jpg
spec = [{"name","src","crop":[x0,y0,x1,y1]?,"small","big","badge"}]
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 720
BLUE = (22, 88, 196)
WHITE = (250, 250, 250)
F_BIG = "C:/Windows/Fonts/seguibl.ttf"
F_SMALL = "C:/Windows/Fonts/segoeuib.ttf"
F_BADGE = "C:/Windows/Fonts/timesbd.ttf"  # algarismos alinhados (Georgia tem algarismos de texto: "60%" ficava desnivelado)


def fit169(im, crop=None):
    if crop:
        im = im.crop(tuple(crop))
    iw, ih = im.size
    if iw / ih > 16 / 9:
        nw = int(ih * 16 / 9); x = (iw - nw) // 2; im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw * 9 / 16); y = (ih - nh) // 2; im = im.crop((0, y, iw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def spaced(draw, xy_right, text, font, spacing, fill):
    """texto com espaçamento entre letras, alinhado pela direita em xy_right=(x_dir, y)."""
    widths = [draw.textlength(c, font=font) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy_right[0] - total
    for c, w in zip(text, widths):
        draw.text((x, xy_right[1]), c, font=font, fill=fill)
        x += w + spacing
    return total


def make(spec):
    im = Image.open(ROOT / spec["src"]).convert("RGB")
    im = fit169(im, spec.get("crop"))
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.12)
    # sombra do título numa camada separada, desfocada
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    text = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds, dt = ImageDraw.Draw(shadow), ImageDraw.Draw(text)
    right = W - 58
    big = ImageFont.truetype(F_BIG, 118)
    small = ImageFont.truetype(F_SMALL, 40)
    bw = dt.textlength(spec["big"], font=big)
    while bw > W * 0.62:  # palavra grande nunca passa de ~62% da largura
        big = ImageFont.truetype(F_BIG, big.size - 4); bw = dt.textlength(spec["big"], font=big)
    y_small, y_big = 14, 58
    for d, fill, off in ((ds, (0, 0, 0, 200), 4), (dt, WHITE, 0)):
        spaced(d, (right + off - (bw - dt.textlength(spec["big"], font=big)) , y_small + off), spec["small"], small, 14, fill)
        d.text((right - bw + off, y_big + off), spec["big"], font=big, fill=fill)
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(im.convert("RGBA"), shadow)
    im = Image.alpha_composite(im, text)
    # selo azul com número
    badge = spec.get("badge")
    if badge:
        d = ImageDraw.Draw(im)
        cx, cy, r = 100, H - 100, 78
        d.ellipse((cx - r + 3, cy - r + 5, cx + r + 3, cy + r + 5), fill=(0, 0, 0, 90))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BLUE)
        size = 72 if len(badge) <= 2 else 56 if len(badge) <= 3 else 44
        fb = ImageFont.truetype(F_BADGE, size)
        tw = d.textlength(badge, font=fb)
        bb = d.textbbox((0, 0), badge, font=fb)
        d.text((cx - tw / 2, cy - (bb[3] + bb[1]) / 2), badge, font=fb, fill=WHITE)
    out = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(out, quality=92)
    print("[thumb4]", out)
    return out


def main():
    specs = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    outs = [make(s) for s in specs]
    cols = 2
    rows = (len(outs) + 1) // 2
    sheet = Image.new("RGB", (cols * 640, rows * 360), (20, 20, 20))
    for i, p in enumerate(outs):
        sheet.paste(Image.open(p).resize((640, 360)), ((i % cols) * 640, (i // cols) * 360))
    (ROOT / "qa" / "thumbs4").mkdir(parents=True, exist_ok=True)
    sheet.save(ROOT / "qa" / "thumbs4" / "review.jpg", quality=88)


if __name__ == "__main__":
    main()
