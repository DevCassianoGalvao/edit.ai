"""Miniatura: o objeto do vídeo É a miniatura.

- quadro/foto em FORÇA TOTAL (sem escurecer), recortado para o objeto encher 1280x720
- no máximo DUAS palavras, numa linha, num canto vazio, sem faixa, sem sobretítulo
- gera também a prévia a 210 px de largura para o teste de leitura
Uso: python make_thumb.py SRC OUT.jpg "TEXTO" --crop x0 y0 x1 y1 --corner tl|tr|bl|br [--color #FFFFFF]
     (crop em pixels da imagem de origem; será ajustado para 16:9 em torno do centro do recorte)
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "C:/Windows/Fonts/impact.ttf"


def fit169(x0, y0, x1, y1, W, H):
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    if w / h > 16 / 9:
        h = w * 9 / 16
    else:
        w = h * 16 / 9
    w, h = min(w, W), min(h, H)
    x0 = min(max(0, cx - w / 2), W - w)
    y0 = min(max(0, cy - h / 2), H - h)
    return int(x0), int(y0), int(x0 + w), int(y0 + h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("text")
    ap.add_argument("--crop", nargs=4, type=int)
    ap.add_argument("--corner", default="tr", choices=["tl", "tr", "bl", "br"])
    ap.add_argument("--color", default="#FFFFFF")
    a = ap.parse_args()
    words = a.text.split()
    if len(words) > 2:
        raise SystemExit("no máximo DUAS palavras")
    im = Image.open(a.src).convert("RGB")
    box = fit169(*(a.crop or (0, 0, im.width, im.height)), im.width, im.height)
    im = im.crop(box).resize((1280, 720), Image.LANCZOS)
    size = 190
    font = ImageFont.truetype(FONT, size)
    dr = ImageDraw.Draw(im)
    tw = dr.textlength(a.text, font=font)
    while tw > 820 and size > 90:  # uma linha; teste a 210 px mostrou 640 px de largura pequeno demais
        size -= 6
        font = ImageFont.truetype(FONT, size)
        tw = dr.textlength(a.text, font=font)
    m = 40
    x = m if a.corner in ("tl", "bl") else 1280 - m - tw
    y = m - 10 if a.corner in ("tl", "tr") else 720 - m - size * 1.12
    # sombra suave só atrás das letras (legibilidade), a foto continua em força total
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 4, y + 6), a.text, font=font, fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(im.convert("RGBA"), shadow)
    ImageDraw.Draw(im).text((x, y), a.text, font=font, fill=a.color, stroke_width=5, stroke_fill="#000000")
    im = im.convert("RGB")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=92)
    im.resize((210, 118), Image.LANCZOS).save(out.with_name(out.stem + "_210px.png"))
    print("[thumb]", out, "crop", box)


if __name__ == "__main__":
    main()
