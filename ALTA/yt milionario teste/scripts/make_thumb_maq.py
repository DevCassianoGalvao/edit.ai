"""Miniaturas do filme das 15 máquinas (texto na tela em PORTUGUÊS) — regra do PROMPT_v:
- o objeto do vídeo É a miniatura: quadro do próprio filme em força total (nada escurecido), recortado para encher o quadro
- no máximo DUAS palavras, numa linha, num canto vazio da foto, sem cobrir o objeto; sem faixa, sem sobretítulo, sem selo
- testada a 210 px de largura (qa/thumbs_maq/review.jpg mostra 640 px e 210 px lado a lado)
Uso: python make_thumb_maq.py -> out/thumbnails/maq_*.jpg + qa/thumbs_maq/review.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 720
F_BIG = "C:/Windows/Fonts/seguibl.ttf"

# crop = janela no quadro 1920x1080 (ajustada para 16:9); pos = canto do texto; ink = cor do texto
SPECS = [
    # 1ª versão: "200 HOMENS" sobre a estrutura da escavadeira sumia a 210 px → céu vazio do porto ao entardecer
    {"name": "maq_200_homens", "src": "qa/thumbs_maq/g_container.jpg", "crop": [0, 0, 1920, 1080],
     "text": "200 HOMENS", "pos": "top-left", "ink": (255, 255, 255), "size": 150},
    # escavadeira de caçambas: carvão escuro e liso no canto inferior esquerdo
    {"name": "maq_gigante", "src": "qa/thumbs_maq/b_bucketwheel2.jpg", "crop": [0, 0, 1920, 1080],
     "text": "GIGANTE", "pos": "bottom-left", "ink": (255, 214, 0), "size": 160},
    # cabeça da tuneladora rompendo a rocha: parede lisa à direita/topo
    {"name": "maq_1_minuto", "src": "qa/thumbs_maq/c_tbm.jpg", "crop": [0, 0, 1920, 1080],
     "text": "1 MINUTO", "pos": "bottom-left", "ink": (255, 214, 0), "size": 160},
    # 1ª versão: "SEM PARAR" cobria a capota da colhedora de batata → colheitadeira de cima, palha lisa no topo
    {"name": "maq_sem_parar", "src": "qa/thumbs_maq/h_combine.jpg", "crop": [0, 0, 1920, 1080],
     "text": "SEM PARAR", "pos": "top-left", "ink": (255, 255, 255), "size": 150},
    # feller buncher Tigercat abraçando a árvore: mato claro no topo esquerdo
    {"name": "maq_sozinha", "src": "qa/thumbs_maq/e_feller.jpg", "crop": [0, 0, 1920, 1080],
     "text": "SOZINHA", "pos": "top-left", "ink": (255, 255, 255), "size": 150},
]


def fit169(im, crop):
    im = im.crop(tuple(crop))
    iw, ih = im.size
    if iw / ih > 16 / 9:
        nw = int(ih * 16 / 9); x = (iw - nw) // 2; im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw * 9 / 16); y = (ih - nh) // 2; im = im.crop((0, y, iw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def make(spec):
    im = fit169(Image.open(ROOT / spec["src"]).convert("RGB"), spec["crop"])
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.15)
    font = ImageFont.truetype(F_BIG, spec["size"])
    probe = ImageDraw.Draw(im)
    while probe.textlength(spec["text"], font=font) > W * 0.60:  # uma linha, nunca mais que 60% da largura
        font = ImageFont.truetype(F_BIG, font.size - 6)
    tw = probe.textlength(spec["text"], font=font)
    bb = probe.textbbox((0, 0), spec["text"], font=font)
    margin = 48
    x = margin if spec["pos"].endswith("left") else W - margin - tw
    y = margin - bb[1] if spec["pos"].startswith("top") else H - margin - bb[3]
    ink = spec["ink"]
    shade = (0, 0, 0, 200) if sum(ink) > 380 else (255, 255, 255, 200)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 5, y + 6), spec["text"], font=font, fill=shade)
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    out_im = Image.alpha_composite(im.convert("RGBA"), shadow)
    ImageDraw.Draw(out_im).text((x, y), spec["text"], font=font, fill=ink + (255,))
    out = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out_im.convert("RGB").save(out, quality=92)
    print("[thumb]", out.name, f"texto {font.size}px")
    return out


def main():
    outs = [make(s) for s in SPECS]
    small_w, small_h = 210, 118
    sheet = Image.new("RGB", (640 + 24 + small_w, len(outs) * 360), (20, 20, 20))
    for i, p in enumerate(outs):
        im = Image.open(p)
        sheet.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        sheet.paste(im.resize((small_w, small_h), Image.LANCZOS), (640 + 24, i * 360 + (360 - small_h) // 2))
    review = ROOT / "qa" / "thumbs_maq" / "review.jpg"
    review.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(review, quality=90)
    print("[review]", review)


if __name__ == "__main__":
    main()
