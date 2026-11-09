"""Miniaturas do filme do navio — ESPECIFICAÇÃO FIXA do usuário (16/09).

Imagem:      foto real, SEMPRE com água no enquadramento.
Enquadramento: objeto grande em plano aberto, ou um único elemento contra a imensidão vazia.
Texto:       2 palavras. Primeira BRANCA, segunda CIANO (#00D4FF) ou VERMELHA (#FF3B30).
Fonte:       condensada pesada em caixa alta (Anton; Bebas Neue e Archivo Black como reserva).
Posição:     terço inferior esquerdo; terço SUPERIOR quando o assunto está embaixo.
Paleta:      azul-marinho, preto-azulado, cinza-tempestade, branco de espuma (leve correção fria).
Proibido:    seta, círculo, borda, rosto em close, emoji e gradiente atrás do texto — só uma sombra curta
             para legibilidade sobre água clara.

Os quadros saem dos ARQUIVOS ORIGINAIS (vídeo 1080p do usuário e foto do Commons em alta), nunca do filme
já renderizado. Todo texto é ancorado no que a narração diz.
Uso: python make_thumb_navio2.py -> out/thumbnails/navio2_*.jpg + qa/thumbs_navio2/review.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
AP = ROOT / "APAGAR_navio-2026-09-16"
ORIG = AP / "folhas_de_conferencia" / "thumbs_navio" / "orig"
FOTOS = AP / "fotos_baixadas"
W, H = 1920, 1080
FONTS = [ROOT / "public" / "fonts" / n for n in ("Anton.ttf", "BebasNeue.ttf", "ArchivoBlack.ttf")]
FONT_PATH = str(next(f for f in FONTS if f.exists()))
WHITE = (255, 255, 255)
CIANO = (0, 212, 255)      # #00D4FF
VERMELHO = (255, 59, 48)   # #FF3B30

SPECS = [
    # "assunto embaixo" -> texto no terço superior; senão, terço inferior esquerdo
    {"name": "navio2_aco_flutua", "src": ORIG / "55_120.png", "w1": "AÇO", "w2": "FLUTUA", "cor": CIANO, "pos": "baixo"},
    {"name": "navio2_agua_ausente", "src": ORIG / "Ship_80.png", "w1": "ÁGUA", "w2": "AUSENTE", "cor": CIANO, "pos": "baixo"},
    {"name": "navio2_borda_livre", "src": ORIG / "Ship_115.png", "w1": "BORDA", "w2": "LIVRE", "cor": CIANO, "pos": "baixo"},
    {"name": "navio2_noventa_segundos", "src": ORIG / "Oil_30.png", "w1": "NOVENTA", "w2": "SEGUNDOS", "cor": VERMELHO, "pos": "cima"},
    # "CASCO PARTIDO" prometia casco partido em dois; a foto e de um navio encalhado inteiro -> "SEM VOLTA"
    {"name": "navio2_sem_volta", "src": FOTOS / "Edro_III_Shipwreck_LE.jpg", "w1": "SEM", "w2": "VOLTA", "cor": VERMELHO, "pos": "baixo"},
]


def fit169(im):
    iw, ih = im.size
    if iw / ih > 16 / 9:
        nw = int(ih * 16 / 9); x = (iw - nw) // 2; im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw * 9 / 16); y = (ih - nh) // 2; im = im.crop((0, y, iw, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def paleta_fria(im):
    """Puxa a imagem para azul-marinho / cinza-tempestade, sem lavar o branco da espuma."""
    im = ImageEnhance.Color(im).enhance(0.88)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    r, g, b = im.split()
    r = r.point(lambda v: max(0, int(v * 0.96)))
    b = b.point(lambda v: min(255, int(v * 1.06)))
    return Image.merge("RGB", (r, g, b))


def recorta(im, rec):
    """rec = (zoom, cx, cy) normalizado: aproxima o quadro no navio antes do corte 16:9."""
    z, cx, cy = rec
    iw, ih = im.size
    nw, nh = int(iw * z), int(ih * z)
    x = min(max(int(iw * cx - nw / 2), 0), iw - nw)
    y = min(max(int(ih * cy - nh / 2), 0), ih - nh)
    return im.crop((x, y, x + nw, y + nh))


def make(spec):
    im = Image.open(spec["src"]).convert("RGB")
    if spec.get("recorte"):
        im = recorta(im, spec["recorte"])
    im = paleta_fria(fit169(im))
    d = ImageDraw.Draw(im)
    size = 200
    if spec.get("empilhar"):   # duas linhas por escolha de composicao (texto so sobre a agua)
        f = ImageFont.truetype(FONT_PATH, size)
        linhas = [[(spec["w1"], WHITE)], [(spec["w2"], spec["cor"])]]
        while max(d.textlength(t, font=f) for l in linhas for t, _c in l) > W * 0.42 and size > 120:
            size -= 6
            f = ImageFont.truetype(FONT_PATH, size)
        return _desenha(im, d, spec, linhas, size)
    while True:  # duas palavras na mesma linha; se passar de 66% da largura, empilha
        f = ImageFont.truetype(FONT_PATH, size)
        w1 = d.textlength(spec["w1"] + " ", font=f)
        w2 = d.textlength(spec["w2"], font=f)
        if w1 + w2 <= W * 0.66:
            linhas = [[(spec["w1"], WHITE), (spec["w2"], spec["cor"])]]
            break
        if size <= 150:
            linhas = [[(spec["w1"], WHITE)], [(spec["w2"], spec["cor"])]]
            break
        size -= 8
    return _desenha(im, d, spec, linhas, size)


def _desenha(im, d, spec, linhas, size):
    f = ImageFont.truetype(FONT_PATH, size)
    alt = (f.getbbox("H")[3] - f.getbbox("H")[1]) * 1.18
    x0 = 92
    y0 = 84 if spec["pos"] == "cima" else H - 84 - alt * len(linhas)
    # LEGIBILIDADE (17/09): o vermelho sobre casco azul sumia no tamanho de listagem. Agora cada palavra leva
    # uma mancha escura desfocada colada nela + contorno preto-azulado. Continua sem faixa e sem gradiente.
    contorno = max(6, size // 16)
    mancha = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dm = ImageDraw.Draw(mancha)
    for i, linha in enumerate(linhas):
        x = x0
        for txt, _cor in linha:
            dm.text((x + 3, y0 + i * alt + 5), txt, font=f, fill=(0, 14, 28, 225),
                    stroke_width=contorno + 8, stroke_fill=(0, 14, 28, 225))
            x += d.textlength(txt + " ", font=f)
    out = Image.alpha_composite(im.convert("RGBA"), mancha.filter(ImageFilter.GaussianBlur(16)))
    dd = ImageDraw.Draw(out)
    for i, linha in enumerate(linhas):
        x = x0
        for txt, cor in linha:
            dd.text((x, y0 + i * alt), txt, font=f, fill=cor + (255,),
                    stroke_width=contorno, stroke_fill=(0, 12, 24, 255))
            x += d.textlength(txt + " ", font=f)
    dst = ROOT / "out" / "thumbnails" / f"{spec['name']}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(dst, quality=95, subsampling=0)
    print("[thumb]", dst.name, f"{spec['w1']} {spec['w2']} — {size}px, {len(linhas)} linha(s)")
    return dst


def main():
    outs = [make(s) for s in SPECS]
    sw, sh = 210, 118
    folha = Image.new("RGB", (640 + 24 + sw, len(outs) * 360), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p)
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 360))
        folha.paste(im.resize((sw, sh), Image.LANCZOS), (640 + 24, i * 360 + (360 - sh) // 2))
    rev = ROOT / "qa" / "thumbs_navio2" / "review.jpg"
    rev.parent.mkdir(parents=True, exist_ok=True)
    folha.save(rev, quality=90)
    print("[review]", rev)


if __name__ == "__main__":
    main()
