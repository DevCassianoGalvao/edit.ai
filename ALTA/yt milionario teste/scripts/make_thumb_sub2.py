"""Miniaturas do filme do submarino no MODELO pedido pelo usuário (16/09): foto do filme ocupando todo o quadro,
texto no alto à esquerda em UMA linha, NÚMERO em dourado colado à PALAVRA em branco, fonte pesada e sombra.

Os quadros saem do próprio filme entregue (o material bruto já foi apagado).
Uso: python make_thumb_sub2.py -> out/thumbnails/sub2_*.jpg + qa/thumbs_sub2/review.jpg (640 px e 210 px lado a lado)
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FILM = ROOT / "entregas" / "submarino-2026-09-16" / "La vida dentro de un submarino nuclear.mp4"
FRAMES = ROOT / "qa" / "thumbs_sub2" / "full"
W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/seguibl.ttf"
GOLD, WHITE = (232, 163, 45), (255, 255, 255)

# t = segundo do filme; num + word = as duas partes do texto (dourado + branco); crop = janela no quadro 1920x1080.
# Todo número tem que estar DITO na narração: 160 hombres, 90 días, 18 horas, "dos o incluso tres marineros" por litera.
# A narração nunca diz quantos mísseis o submarino leva -> nada de número aí; usa as palavras do próprio roteiro.
SPECS = [
    {"name": "sub2_160_militares", "t": 1780, "num": "160", "word": "MILITARES", "size": 132},
    {"name": "sub2_90_dias", "t": 152, "num": "90", "word": "DÍAS", "size": 150},
    {"name": "sub2_misiles_ocultos", "t": 2193, "num": "MISILES", "word": "OCULTOS", "size": 118},
    # crop tira a faixa de cima: a placa em inglês do beliche ficava colada no texto
    {"name": "sub2_3_turnos", "t": 618, "num": "3", "word": "TURNOS", "size": 145, "crop": [0, 300, 1920, 1080]},
    {"name": "sub2_18_horas", "t": 267, "num": "18", "word": "HORAS", "size": 145},
]


def frame(t):
    FRAMES.mkdir(parents=True, exist_ok=True)
    p = FRAMES / f"f{t:05d}.png"
    if not p.exists():
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(FILM),
                        "-frames:v", "1", str(p)], check=True)
    return Image.open(p).convert("RGB")


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
    im = fit169(frame(spec["t"]), spec.get("crop"))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.15)
    size = spec["size"]
    probe = ImageDraw.Draw(im)
    while True:  # número + palavra numa linha só, nunca mais que 62% da largura
        fnum = ImageFont.truetype(FONT_PATH, size)
        fword = ImageFont.truetype(FONT_PATH, int(size * 0.62))
        wn = probe.textlength(spec["num"], font=fnum)
        ww = probe.textlength(spec["word"], font=fword)
        if wn + 10 + ww <= W * 0.62 or size < 70:
            break
        size -= 6
    x, margin = 56, 52
    bn = probe.textbbox((0, 0), spec["num"], font=fnum)
    bw = probe.textbbox((0, 0), spec["word"], font=fword)
    base = margin + (bn[3] - bn[1])           # linha de base comum às duas partes
    y_num = base - bn[3]
    y_word = base - bw[3]
    x_word = x + wn + 10
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    ds.text((x + 5, y_num + 7), spec["num"], font=fnum, fill=(0, 0, 0, 205))
    ds.text((x_word + 5, y_word + 7), spec["word"], font=fword, fill=(0, 0, 0, 205))
    out_im = Image.alpha_composite(im.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(out_im)
    d.text((x, y_num), spec["num"], font=fnum, fill=GOLD + (255,))
    d.text((x_word, y_word), spec["word"], font=fword, fill=WHITE + (255,))
    out = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out_im.convert("RGB").save(out, quality=92)
    print("[thumb]", out.name, f"{spec['num']} {spec['word']} — {size}px")
    return out


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    sheet = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (20, 20, 20))
    for i, p in enumerate(outs):
        im = Image.open(p)
        sheet.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        sheet.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    review = ROOT / "qa" / "thumbs_sub2" / "review.jpg"
    review.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(review, quality=90)
    print("[review]", review)


if __name__ == "__main__":
    main()
