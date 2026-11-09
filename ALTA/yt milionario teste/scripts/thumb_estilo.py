"""MINIATURAS NO ESTILO DA REFERÊNCIA DE CADA NICHO (07/10/2026, pedido do usuário).

O usuário mandou 4 referências (painel/thumb_estilos/<nicho>/ref_1.webp) e pediu que toda miniatura copie a referência
"de cabo a rabo" — elementos, posições, fonte e jeito do texto — com uma imagem que tenha tudo a ver com o tema e uma
frase curta, impactante e provocativa no idioma do canal, em 16:9. Aqui é o MOLDE de cada referência (texto desenhado
por nós = sem erro de letra; as fotos vêm do material aprovado do filme / banco).

  noticia  (carros + indústria) — painel em diagonal à esquerda, foto principal à direita, etiquetas vermelhas com
           seta, quadro antes/depois com borda vermelha, selo do globo, faixa vermelha inclinada (linha 1, itálico) e
           caixa branca de borda vermelha com a linha 2 ENORME em preto
  trilho   (seu canal) — foto de fundo, recorte inclinado com borda amarela, seta vermelha, selo vermelho de pincel
           com termômetro no canto, texto embaixo: parte 1 branca + parte 2 amarela, contorno preto, textura gasta
  mumia    (seu canal) — 2 linhas no alto à esquerda (branca + vermelha), quadro de borda vermelha no
           alto à direita, seta vermelha curva do quadro até o assunto
  doc      (Documentários Extremos) — foto de fundo, recorte grande de cantos chanfrados com borda ciano, seta vermelha,
           texto embaixo à direita: parte 1 branca + parte 2 amarela

Uso: python thumb_estilo.py spec.json        (spec: {"estilo", "saida", "fundo", "lado"/"inset"/"inset2",
     "linha1", "linha2", "badge", "etiquetas": [{"txt", "x", "y", "alvo": [x, y]}], "foco": [fx, fy], "seta_alvo": [x, y]})
     Coordenadas na tela de 1920x1080.
"""
import json, math, random, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTES = ROOT / "public" / "fonts"
W, H = 1920, 1080
VERM, AMAR, CIANO, BRANCO, PRETO = (232, 22, 28), (255, 236, 30), (70, 220, 255), (255, 255, 255), (0, 0, 0)


def fonte(nome, tam):
    return ImageFont.truetype(str(FONTES / f"{nome}.ttf"), int(tam))


def cabe(txt, nome, max_w, max_h, ini=400):
    """Maior tamanho de fonte em que o texto cabe na caixa."""
    t = ini
    while t > 12:
        f = fonte(nome, t)
        x0, y0, x1, y1 = f.getbbox(txt)
        if x1 - x0 <= max_w and y1 - y0 <= max_h:
            return f
        t -= 4
    return fonte(nome, 12)


def look(im):
    """O "visual de miniatura" das referências: contraste, cor saturada, nitidez."""
    im = ImageEnhance.Contrast(im).enhance(1.22)
    im = ImageEnhance.Color(im).enhance(1.35)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    return im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=140, threshold=2))


def foto(caminho, w, h, foco=(0.5, 0.5), realce=True):
    im = Image.open(caminho).convert("RGB")
    k = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * k)), max(h, round(im.height * k))), Image.LANCZOS)
    x = int((im.width - w) * foco[0]); y = int((im.height - h) * foco[1])
    im = im.crop((x, y, x + w, y + h))
    return look(im) if realce else im


def vinheta(im, forca=0.55):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((-im.width * 0.15, -im.height * 0.2, im.width * 1.15, im.height * 1.2), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(im.width // 8))
    escuro = Image.new("RGB", im.size, (0, 0, 0))
    return Image.composite(im, Image.blend(im, escuro, forca), m)


def gasto(alpha, densidade=0.035, semente=7):
    """Textura gasta (grunge) das referências 2-4: pinta falhas no texto."""
    rnd = random.Random(semente)
    d = ImageDraw.Draw(alpha)
    w, h = alpha.size
    for _ in range(int(w * h * densidade / 140)):
        x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.choice((1, 1, 2, 2, 3, 4))
        d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice((0, 40, 90)))
    return alpha


def escreve(base, xy, txt, f, cor, contorno=10, cor_contorno=PRETO, sombra=12, grunge=False, ancora="la", italico=0.0):
    """Texto com contorno grosso + sombra (estilo das referências). italico = inclinação (0,18 = itálico)."""
    camada = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    if sombra:
        d.text((xy[0] + sombra * 0.6, xy[1] + sombra), txt, font=f, fill=(0, 0, 0, 170), anchor=ancora,
               stroke_width=contorno, stroke_fill=(0, 0, 0, 170))
        camada = camada.filter(ImageFilter.GaussianBlur(sombra * 0.6))
        d = ImageDraw.Draw(camada)
    letra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(letra)
    dl.text(xy, txt, font=f, fill=cor + (255,), anchor=ancora, stroke_width=contorno, stroke_fill=cor_contorno + (255,))
    if grunge:
        miolo = Image.new("L", base.size, 0)
        ImageDraw.Draw(miolo).text(xy, txt, font=f, fill=255, anchor=ancora)
        falhas = gasto(Image.new("L", base.size, 255))
        # as falhas só "comem" o miolo da letra, revelando uma cor um pouco mais escura (efeito tinta gasta)
        escura = tuple(int(c * 0.72) for c in cor) + (255,)
        manchas = Image.new("RGBA", base.size, escura)
        mascara = Image.composite(Image.new("L", base.size, 0), miolo, falhas)
        letra = Image.composite(manchas, letra, mascara)
    camada = Image.alpha_composite(camada, letra)
    if italico:
        camada = camada.transform(camada.size, Image.AFFINE, (1, italico, -italico * xy[1], 0, 1, 0), Image.BICUBIC)
    base.alpha_composite(camada)
    return base


def seta(base, ini, fim, largura=60, cor=VERM, contorno=7, curva=0.0):
    """Seta vermelha grossa com contorno preto; curva != 0 dobra o corpo (seta curva da referência 3)."""
    d = ImageDraw.Draw(base)
    (x0, y0), (x1, y1) = ini, fim
    ang = math.atan2(y1 - y0, x1 - x0)
    cab = largura * 1.9
    bx, by = x1 - math.cos(ang) * cab * 0.85, y1 - math.sin(ang) * cab * 0.85   # base da ponta
    if curva:
        mx, my = (x0 + bx) / 2 - math.sin(ang) * curva, (y0 + by) / 2 + math.cos(ang) * curva
        pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * bx, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * by)
               for t in [i / 40 for i in range(41)]]
        ang2 = math.atan2(by - pts[-3][1], bx - pts[-3][0])
    else:
        pts, ang2 = [(x0, y0), (bx, by)], ang
    ponta = [(x1, y1), (bx + math.cos(ang2 + math.pi / 2) * cab * 0.62, by + math.sin(ang2 + math.pi / 2) * cab * 0.62),
             (bx - math.cos(ang2 + math.pi / 2) * cab * 0.62, by - math.sin(ang2 + math.pi / 2) * cab * 0.62)]
    for c, w_extra in ((PRETO, contorno * 2), (cor, 0)):
        d.line(pts, fill=c + (255,), width=int(largura * 0.5) + w_extra, joint="curve")
        if w_extra:
            d.polygon(ponta, fill=c + (255,), outline=c + (255,), width=w_extra)
        else:
            d.polygon(ponta, fill=c + (255,))
    return base


def cola_poligono(base, im, pts, borda=None, esp=8):
    """Cola a foto `im` (já no tamanho da caixa do polígono) recortada pelo polígono, com borda colorida."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0 = int(min(xs)), int(min(ys))
    im = im.resize((int(max(xs)) - x0, int(max(ys)) - y0), Image.LANCZOS)
    m = Image.new("L", base.size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    camada = Image.new("RGBA", base.size, (0, 0, 0, 0))
    camada.paste(im.convert("RGBA"), (x0, y0))
    sombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).polygon([(x + 10, y + 14) for x, y in pts], fill=(0, 0, 0, 150))
    base.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(14)))
    base.paste(camada, (0, 0), m)
    if borda:
        ImageDraw.Draw(base).line(pts + [pts[0]], fill=borda + (255,), width=esp, joint="curve")
    return base


def chanfro(x0, y0, x1, y1, c):
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


# ------------------------------------------------------------------ estilos
def noticia(s):
    base = foto(s["fundo"], W, H, tuple(s.get("foco", (0.5, 0.5)))).convert("RGBA")
    base = vinheta(base.convert("RGB"), 0.35).convert("RGBA")
    # painel da esquerda em diagonal (na referência é a apresentadora no estúdio azul)
    if s.get("lado"):
        lado = foto(s["lado"], 720, H, tuple(s.get("foco_lado", (0.5, 0.35))))
        azul = Image.new("RGB", lado.size, (20, 70, 200))
        lado = Image.blend(lado, azul, 0.18)
        diag = [(0, 0), (665, 0), (505, H), (0, H)]
        cola_poligono(base, lado, diag)
        ImageDraw.Draw(base).line([(665, 0), (505, H)], fill=(235, 245, 255, 255), width=7)
    # etiquetas vermelhas com seta
    for e in s.get("etiquetas", []):
        f = fonte("Anton", 52)
        x0, y0, x1, y1 = f.getbbox(e["txt"])
        bw, bh = x1 - x0 + 34, y1 - y0 + 26
        d = ImageDraw.Draw(base)
        d.rectangle((e["x"], e["y"], e["x"] + bw, e["y"] + bh), fill=VERM + (255,), outline=BRANCO + (255,), width=3)
        d.text((e["x"] + 17 - x0, e["y"] + 13 - y0), e["txt"], font=f, fill=BRANCO + (255,))
        if e.get("alvo"):
            seta(base, (e["x"] + bw * 0.55, e["y"] + bh), tuple(e["alvo"]), largura=26, contorno=3)
    # quadro antes/depois (borda vermelha)
    if s.get("inset"):
        bx0, by0, bx1, by1 = 1440, 370, 1900, 700
        ImageDraw.Draw(base).rectangle((bx0 - 7, by0 - 7, bx1 + 7, by1 + 7), fill=VERM + (255,))
        if s.get("inset2"):
            a = foto(s["inset"], (bx1 - bx0) // 2 - 3, by1 - by0); b = foto(s["inset2"], (bx1 - bx0) // 2 - 3, by1 - by0)
            base.paste(a, (bx0, by0)); base.paste(b, (bx0 + a.width + 6, by0))
            ImageDraw.Draw(base).rectangle((bx0 + a.width, by0, bx0 + a.width + 5, by1), fill=BRANCO + (255,))
            seta(base, (bx0 + 170, by0 + 150), (bx0 + 300, by0 + 150), largura=30, contorno=3, curva=-55)
        else:
            base.paste(foto(s["inset"], bx1 - bx0, by1 - by0), (bx0, by0))
    # selo do globo (canto inferior esquerdo)
    g = Image.new("RGBA", (260, 290), (0, 0, 0, 0))
    dg = ImageDraw.Draw(g)
    dg.rounded_rectangle((0, 0, 259, 289), 14, fill=(8, 18, 48, 255), outline=(60, 140, 255, 255), width=3)
    for r, a in ((118, 40), (98, 90), (82, 255)):
        dg.ellipse((130 - r, 140 - r, 130 + r, 140 + r), fill=(40, 120, 255, a))
    for k in range(-2, 3):
        dg.ellipse((130 - 82 + abs(k) * 22, 58, 130 + 82 - abs(k) * 22, 222), outline=(170, 220, 255, 160), width=3)
        dg.line((52, 140 + k * 30, 208, 140 + k * 30), fill=(170, 220, 255, 140), width=3)
    dg.ellipse((22, 210, 238, 262), outline=(110, 190, 255, 220), width=6)
    g = g.filter(ImageFilter.GaussianBlur(0.6))
    base.alpha_composite(g, (12, 770))
    # faixa vermelha inclinada (linha 1, itálico) + caixa branca com a linha 2 enorme
    d = ImageDraw.Draw(base)
    f1 = cabe(s["linha1"], "Anton", 760, 92, 150)
    x0, y0, x1, y1 = f1.getbbox(s["linha1"])
    fw = x1 - x0 + 90
    d.polygon([(300, 742), (300 + fw + 40, 742), (300 + fw, 836), (276, 836)], fill=VERM + (255,))
    escreve(base, (330 - x0 + 16, 789), s["linha1"], f1, BRANCO, contorno=0, sombra=4, ancora="lm", italico=-0.2)
    d = ImageDraw.Draw(base)
    d.rectangle((262, 838, 1906, 1052), fill=VERM + (255,))
    d.rectangle((272, 848, 1896, 1042), fill=BRANCO + (255,))
    f2 = cabe(s["linha2"], "Anton", 1590, 200, 320)   # na referência a linha 2 enche a caixa
    escreve(base, (1084, 948), s["linha2"], f2, PRETO, contorno=0, sombra=0, ancora="mm")
    return base


def trilho(s):
    base = foto(s["fundo"], W, H, tuple(s.get("foco", (0.5, 0.5)))).convert("RGBA")
    if s.get("inset"):
        pts = [(0, 34), (860, 40), (1035, 310), (980, 690), (40, 720), (0, 700)]
        cola_poligono(base, foto(s["inset"], 1040, 690), pts, borda=AMAR, esp=9)
        seta(base, tuple(s.get("seta_ini", (1135, 785))), tuple(s.get("seta_alvo", (975, 645))), largura=66)
    if s.get("badge"):   # selo vermelho de pincel com termômetro
        sel = Image.new("RGBA", (560, 200), (0, 0, 0, 0))
        ds = ImageDraw.Draw(sel)
        rnd = random.Random(3)
        # pincelada: borda irregular (não pontilhada) — contorno em zigue-zague fino
        topo = [(x, 22 + rnd.uniform(-9, 9) - x * 0.02) for x in range(14, 556, 18)]
        base_ = [(x, 176 + rnd.uniform(-10, 10) - x * 0.02) for x in range(556, 10, -18)]
        ds.polygon([(6, 60)] + topo + [(558, 100)] + base_ + [(4, 150)], fill=VERM + (255,))
        ds.rounded_rectangle((52, 30, 92, 140), 20, fill=BRANCO + (255,)); ds.ellipse((40, 118, 104, 182), fill=BRANCO + (255,))
        ds.rounded_rectangle((63, 60, 81, 140), 9, fill=VERM + (255,)); ds.ellipse((52, 130, 92, 170), fill=VERM + (255,))
        ft = cabe(s["badge"], "Anton", 400, 128, 170)
        ds.text((118, 98), s["badge"], font=ft, fill=BRANCO + (255,), anchor="lm", stroke_width=4, stroke_fill=(120, 0, 0, 255))
        sel = sel.rotate(8, resample=Image.BICUBIC, expand=True)
        base.alpha_composite(sel, (W - sel.width - 10, 20))
    f = cabe(s["linha1"] + " " + s["linha2"], "Anton", 1800, 230, 320)
    larg1 = f.getlength(s["linha1"] + " ")
    total = f.getlength(s["linha1"] + " " + s["linha2"])
    x = (W - total) / 2
    escreve(base, (x, 1035), s["linha1"], f, BRANCO, contorno=12, grunge=True, ancora="ls")
    escreve(base, (x + larg1, 1035), s["linha2"], f, AMAR, contorno=12, grunge=True, ancora="ls")
    return base


def mumia(s):
    base = foto(s["fundo"], W, H, tuple(s.get("foco", (0.5, 0.6)))).convert("RGBA")
    base = vinheta(base.convert("RGB"), 0.45).convert("RGBA")
    if s.get("inset"):
        bx0, by0, bx1, by1 = 1262, 22, 1895, 445
        ImageDraw.Draw(base).rectangle((bx0 - 8, by0 - 8, bx1 + 8, by1 + 8), fill=VERM + (255,))
        base.paste(foto(s["inset"], bx1 - bx0, by1 - by0), (bx0, by0))
        seta(base, (bx0 - 20, by1 - 40), tuple(s.get("seta_alvo", (930, 560))), largura=46, curva=-90)
    f1 = cabe(s["linha1"], "Anton", 1190, 175, 260)
    f2 = cabe(s["linha2"], "Anton", 1190, 190, 270)
    t = min(f1.size, f2.size)
    f1, f2 = fonte("Anton", t), fonte("Anton", t)
    escreve(base, (30, 32), s["linha1"], f1, BRANCO, contorno=12, grunge=True, ancora="la")
    escreve(base, (30, 32 + t * 1.12), s["linha2"], f2, VERM, contorno=12, grunge=True, ancora="la")
    return base


def doc(s):
    base = foto(s["fundo"], W, H, tuple(s.get("foco", (0.5, 0.5)))).convert("RGBA")
    if s.get("inset"):
        pts = chanfro(18, 128, 1440, 792, 85)
        cola_poligono(base, foto(s["inset"], 1422, 664), pts, borda=CIANO, esp=6)
        seta(base, tuple(s.get("seta_ini", (1365, 770))), tuple(s.get("seta_alvo", (1175, 560))), largura=70)
    f = cabe(s["linha1"] + " " + s["linha2"], "Anton", 1600, 215, 320)
    larg2 = f.getlength(s["linha2"])
    xr = W - 45
    escreve(base, (xr - larg2, 1040), s["linha2"], f, AMAR, contorno=12, grunge=True, ancora="ls")
    escreve(base, (xr - larg2 - f.getlength(" "), 1040), s["linha1"], f, BRANCO, contorno=12, grunge=True, ancora="rs")
    return base


ESTILOS = {"noticia": noticia, "trilho": trilho, "mumia": mumia, "doc": doc}
NICHO_ESTILO = {"carros": "noticia", "industria": "noticia", "trens": "trilho", "historia": "mumia", "documentario": "doc"}


def gera(spec):
    im = ESTILOS[spec["estilo"]](spec).convert("RGB")
    saida = Path(spec["saida"]); saida.parent.mkdir(parents=True, exist_ok=True)
    im.save(saida, quality=93)
    im.resize((210, 118), Image.LANCZOS).save(saida.with_name(saida.stem + "_210px.jpg"), quality=90)   # conferir pequeno
    return saida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s in (lambda x: x if isinstance(x, list) else [x])(json.loads(Path(sys.argv[1]).read_text("utf-8"))):
        print("[thumb]", gera(s))
