"""Miniaturas no estilo de referência do usuário (porta-aviões "R$ 70 BILHÕES" / plataforma "14 DIAS").

- foto do filme em tela cheia, cor viva (contraste/saturação leves), SEM escurecer a imagem inteira
- só uma sombra suave e local atrás do texto para leitura
- layout "stack": linha 1 branca menor + linha 2 âmbar grande, barrinha âmbar acima (ref. 1)
- layout "inline": número gigante laranja + palavra branca menor na mesma linha de base (ref. 2)
Uso: python make_thumb3.py spec.json -> out/thumbnails/<name>.jpg + _210px.png + qa/thumbs3/review.jpg
spec = [{"name","src","crop":[x0,y0,x1,y1]?,"layout":"stack"|"inline","l1","l2","corner":"tl"|"bl","x":px?,"y":px?}]
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 720
AMBER = (240, 180, 30)
ORANGE = (242, 140, 40)
WHITE = (245, 242, 235)


def font_heavy(size):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)


def font_condensed(size):
    f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", size)
    try:
        f.set_variation_by_name("Bold Condensed")
    except Exception:  # noqa: BLE001
        return ImageFont.truetype("C:/Windows/Fonts/impact.ttf", size)
    return f


def fit169(box, iw, ih):
    x0, y0, x1, y1 = box
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
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.25)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))


def text_shadow(base, draws):
    """draws: [(xy, text, font)] -> sombra macia só atrás das letras."""
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    for (x, y), t, f in draws:
        d.text((x + 4, y + 6), t, font=f, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    return Image.alpha_composite(base, sh)


def local_glow(base, rect):
    """escurecimento radial suave só na região do texto (não na foto toda)."""
    x0, y0, x1, y1 = rect
    m = Image.new("L", base.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([x0 - 60, y0 - 50, x1 + 80, y1 + 50], radius=80, fill=95)
    m = m.filter(ImageFilter.GaussianBlur(70))
    dark = Image.new("RGBA", base.size, (0, 0, 0, 255))
    dark.putalpha(m)
    return Image.alpha_composite(base, dark)


def render(s):
    src = Image.open(ROOT / s["src"]).convert("RGB")
    box = fit169(s.get("crop") or (0, 0, src.width, src.height), src.width, src.height)
    im = grade(src.crop(box).resize((W, H), Image.LANCZOS)).convert("RGBA")
    m = 58
    if s["layout"] == "stack":
        f1, f2 = font_heavy(s.get("s1", 118)), font_heavy(s.get("s2", 128))
        d = ImageDraw.Draw(im)
        w1 = d.textlength(s["l1"], font=f1)
        w2 = d.textlength(s["l2"], font=f2)
        while max(w1, w2) > W - 2 * m:
            f2 = font_heavy(f2.size - 6); w2 = d.textlength(s["l2"], font=f2)
        h1, h2 = f1.size * 1.0, f2.size * 1.0
        x = s.get("x", m)
        y0 = s.get("y", H - m - h1 - h2 + 8 if s.get("corner", "bl") == "bl" else m + 30)
        im = local_glow(im, (x, y0, x + max(w1, w2), y0 + h1 + h2))
        im = text_shadow(im, [((x, y0), s["l1"], f1), ((x, y0 + h1 * 0.98), s["l2"], f2)])
        d = ImageDraw.Draw(im)
        d.rectangle([x + 4, y0 - 22, x + 4 + 150, y0 - 14], fill=AMBER)
        d.text((x, y0), s["l1"], font=f1, fill=WHITE)
        d.text((x, y0 + h1 * 0.98), s["l2"], font=f2, fill=AMBER)
    else:  # inline
        fn, fw = font_condensed(s.get("s1", 230)), font_condensed(s.get("s2", 120))
        d = ImageDraw.Draw(im)
        x = s.get("x", m)
        y = s.get("y", m + 10 if s.get("corner", "tl") == "tl" else H - m - fn.size)
        wn = d.textlength(s["l1"], font=fn)
        bn = fn.getbbox(s["l1"]); bw = fw.getbbox(s["l2"])
        base = y + bn[3]  # linha de base visual do número
        yw = base - bw[3]
        xw = x + wn + 26
        ww = d.textlength(s["l2"], font=fw)
        im = local_glow(im, (x, y + bn[1], xw + ww, base))
        im = text_shadow(im, [((x, y), s["l1"], fn), ((xw, yw), s["l2"], fw)])
        d = ImageDraw.Draw(im)
        d.text((x, y), s["l1"], font=fn, fill=ORANGE)
        d.text((xw, yw), s["l2"], font=fw, fill=WHITE)
    return im.convert("RGB")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    od = ROOT / "out" / "thumbnails"; od.mkdir(parents=True, exist_ok=True)
    tiles = []
    for s in spec:
        im = render(s)
        p = od / f"{s['name']}.jpg"
        im.save(p, quality=93)
        sm = im.resize((210, 118), Image.LANCZOS); sm.save(od / f"{s['name']}_210px.png")
        tiles.append((im, sm)); print("[thumb3]", p)
    cols = 2; rows = (len(tiles) + 1) // 2
    rev = Image.new("RGB", (cols * 650, rows * 370), (28, 28, 28))
    for i, (im, sm) in enumerate(tiles):
        x, y = (i % 2) * 650, (i // 2) * 370
        rev.paste(im.resize((640, 360)), (x, y)); rev.paste(sm, (x + 640 - 215, y + 360 - 123))
    (ROOT / "qa" / "thumbs3").mkdir(parents=True, exist_ok=True)
    rev.save(ROOT / "qa" / "thumbs3" / "review.jpg", quality=85)


if __name__ == "__main__":
    main()
