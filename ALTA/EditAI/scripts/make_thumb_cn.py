"""Miniaturas do filme CN (texto na tela em INGLÊS) — regra do PROMPT_v:
- o objeto do vídeo É a miniatura: quadro do próprio filme em força total (nada escurecido), recortado para encher o quadro
- no máximo DUAS palavras, numa linha, num canto vazio da foto, sem cobrir o objeto; sem faixa, sem sobretítulo, sem selo
- testada a 210 px de largura (qa/thumbs_cn/review.jpg mostra 1280 px e 210 px lado a lado)
Uso: python make_thumb_cn.py -> out/thumbnails/cn_*.jpg + qa/thumbs_cn/review.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 720
F_BIG = "C:/Windows/Fonts/seguibl.ttf"

# crop = janela 16:9 no quadro 1920x1080; pos = canto do texto; ink = cor do texto (sombra na cor oposta)
SPECS = [
    # 1ª versão: texto à esquerda encostava no topo da locomotiva → quadro inteiro, texto na fumaça escura à direita
    {"name": "cn_minus40", "src": "qa/thumbs_cn/c052441_cn5423_headlight.jpg", "crop": [0, 0, 1920, 1080],
     "text": "-40°", "pos": "top-right", "ink": (255, 255, 255), "size": 190},
    {"name": "cn_deep_freeze", "src": "qa/thumbs_cn/c000000_cnca_blizzard.jpg", "crop": [0, 0, 1920, 1080],
     "text": "DEEP FREEZE", "pos": "top-right", "ink": (255, 255, 255), "size": 150},
    # 1ª versão: trem pequeno demais para ser o objeto → recorte apertado no trem abrindo a neve
    {"name": "cn_whiteout", "src": "qa/thumbs_cn/c001848_plow_drift.jpg", "crop": [580, 300, 1540, 840],
     "text": "WHITEOUT", "pos": "top-left", "ink": (18, 28, 48), "size": 150},
    # 2ª leva (5 miniaturas): CN 2270 com neve caindo — texto no céu à esquerda, acima da locomotiva (topo em y≈300)
    {"name": "cn_snowstorm", "src": "qa/thumbs5/h_c019483_cn_vermelha_neve.jpg", "crop": [0, 0, 1920, 1080],
     "text": "SNOWSTORM", "pos": "top-left", "ink": (18, 28, 48), "size": 130},  # branco sumia no céu cinza a 210 px
    # CN 3884 na curva vista do alto — texto sobre o barranco à direita, longe da cauda do trem (x≈600–840)
    {"name": "cn_survival", "src": "qa/thumbs5/c_c054415_cn3084_curva.jpg", "crop": [0, 0, 1920, 1080],
     "text": "SURVIVAL", "pos": "top-right", "ink": (255, 255, 255), "size": 130},
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
    shade = (0, 0, 0, 190) if sum(ink) > 380 else (255, 255, 255, 200)
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
    review = ROOT / "qa" / "thumbs_cn" / "review.jpg"
    sheet.save(review, quality=90)
    print("[review]", review)


if __name__ == "__main__":
    main()
