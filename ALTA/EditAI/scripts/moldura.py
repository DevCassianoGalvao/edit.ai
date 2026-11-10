"""MOLDURA — fotos de arquivo IMPRESSAS sobre a mesa (estilo "Arquivo Colorizado", 04/11/2026, vídeo de referência
painel/referencias/20261104-*-okeanos-cuba).

O que o estilo faz com a foto de arquivo (medido no vídeo de referência):
  - a foto NÃO enche a tela: vira uma cópia impressa (borda creme fina, sombra) no centro, ~78 % da altura;
  - o fundo é escuro esfumaçado (marrom quase preto, vinheta forte) ou papel creme quadriculado (~1 em 3);
  - foto P&B ganha um tom sépia leve (cópia antiga), colorida fica como está;
  - etiqueta LARANJA no canto superior esquerdo: "LUGAR · DATA" em versalete serifado (ex.: USS MAINE IN HAVANA HARBOR · 1898);
  - retrato de pessoa: nome numa tarja laranja + cargo numa tarja escura, à esquerda da foto;
  - virada de capítulo (foto em tela cheia): caixinha laranja com o ANO + tarja escura com o TÍTULO, no topo à esquerda.
O Remotion depois faz o push lento em cima da imagem pronta (igual ao vídeo de referência).

Rótulos por foto (o Diretor escreve; chave = título da foto no photo_side.json): data/moldura_rotulos.json
  {"File:USS Maine.jpg": {"etiqueta": "USS MAINE IN HAVANA HARBOR · 1898"},
   "File:Shafter.jpg": {"nome": "WILLIAM SHAFTER", "cargo": "U.S. Army general"},
   "File:Senado.jpg": {"capitulo": ["1898", "THE FRUIT FALLS"], "moldura": false},
   "File:X.jpg": {"moldura": "papel"}}          # força papel quadriculado / "escura" / false = tela cheia
Sem rótulo, a foto entra na moldura se for de arquivo (P&B/pouca cor ou formato fora de 16:9) e a fração do
pipeline_config "moldura_fotos": {"ligado": true, "fracao": 0.45} ainda não foi atingida (sorteio fixo por título).
Teste: python scripts/moldura.py FOTO SAIDA.jpg [escura|papel] ["ETIQUETA"]
"""
import hashlib, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FX = ROOT / "assets" / "fx"
FONTE = ROOT / "public" / "fonts" / "Garamond.ttf"
FONTE_B = ROOT / "public" / "fonts" / "Garamond-Bold.ttf"
W, H = 1920, 1080
LARANJA = (196, 86, 52)
CREME = (236, 226, 204)


def _ruido(seed, escalas=(6, 18, 60, 180)):
    """fumaça: soma de ruídos suaves em várias escalas (determinístico)."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((H, W), np.float32)
    for k, e in enumerate(escalas):
        a = rng.random((max(2, H // e), max(2, W // e))).astype(np.float32)
        im = Image.fromarray((a * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(e / 3))
        acc += np.asarray(im, np.float32) / 255 * (0.5 ** (len(escalas) - 1 - k))
    acc -= acc.min()
    return acc / max(acc.max(), 1e-6)


def _vinheta(forca):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1 - forca * (r ** 1.8) / 2.2, 0, 1)


def fundo(variante):
    FX.mkdir(parents=True, exist_ok=True)
    p = FX / f"moldura_{variante}.jpg"
    if p.exists():
        return Image.open(p).convert("RGB")
    if variante == "papel":
        n = _ruido(7, (3, 12, 90))
        base = np.array([226, 212, 182], np.float32)[None, None] * (0.94 + 0.06 * n[..., None])
        im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        for x in range(0, W, 48):   # papel quadriculado bem fraco
            d.line([(x, 0), (x, H)], fill=(208, 194, 166), width=1)
        for y in range(0, H, 48):
            d.line([(0, y), (W, y)], fill=(208, 194, 166), width=1)
        a = np.asarray(im, np.float32) * (0.35 + 0.65 * _vinheta(0.75))[..., None]
    else:
        n = _ruido(3)
        cor = np.array([34, 28, 22], np.float32)[None, None]
        a = cor * (0.45 + 1.25 * n[..., None] ** 1.4) * _vinheta(1.0)[..., None]
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    out.save(p, quality=94)
    return out


def e_arquivo(im):
    a = np.asarray(im.convert("RGB").resize((96, 64)), np.float32)
    sat = (a.max(-1) - a.min(-1)).mean()
    return sat < 28 or not (1.55 < im.width / im.height < 1.9)


def sepia(im):
    g = ImageOps.grayscale(im)
    return ImageOps.colorize(g, (30, 24, 18), (236, 222, 196), mid=(140, 122, 96))


def _fonte(tam, negrito=False):
    return ImageFont.truetype(str(FONTE_B if negrito else FONTE), tam)


def _tarja(d, x, y, texto, tam, fundo_cor, cor=(250, 240, 228), pad=(14, 7), negrito=True, espaco=2):
    f = _fonte(tam, negrito)
    texto = texto.upper()
    larg = sum(f.getlength(c) + espaco for c in texto) - espaco
    alt = f.getbbox("HÁg")[3]
    d.rectangle([x, y, x + larg + 2 * pad[0], y + alt + 2 * pad[1]], fill=fundo_cor)
    cx = x + pad[0]
    for c in texto:
        d.text((cx, y + pad[1] - 2), c, font=f, fill=cor)
        cx += f.getlength(c) + espaco
    return x + larg + 2 * pad[0], y + alt + 2 * pad[1]


def capitulo(im, ano, titulo):
    """tag de capítulo no topo à esquerda: [ANO] laranja + [TÍTULO] escuro (foto já em 1920x1080)."""
    im = im.copy()
    d = ImageDraw.Draw(im)
    x1, _ = _tarja(d, 60, 56, ano, 30, LARANJA)
    _tarja(d, x1 + 6, 56, titulo, 30, (16, 14, 12))
    return im


def emoldura(foto, variante="escura", etiqueta=None, nome=None, cargo=None):
    base = fundo(variante).copy()
    foto = foto.convert("RGB")
    if e_arquivo(foto) and (np.asarray(foto.resize((64, 48)), np.float32).std(-1).mean() < 10):
        foto = sepia(foto)
    alt_max, larg_max = int(H * 0.78), int(W * 0.66)
    s = min(alt_max / foto.height, larg_max / foto.width)
    foto = foto.resize((max(1, round(foto.width * s)), max(1, round(foto.height * s))), Image.LANCZOS)
    borda = 10
    cp = Image.new("RGB", (foto.width + 2 * borda, foto.height + 2 * borda), CREME)
    cp.paste(foto, (borda, borda))
    ImageDraw.Draw(cp).rectangle([0, 0, cp.width - 1, cp.height - 1], outline=(180, 168, 146), width=2)
    x, y = (W - cp.width) // 2, (H - cp.height) // 2 - 8
    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).rectangle([x + 14, y + 22, x + cp.width + 14, y + cp.height + 22], fill=200)
    sombra = sombra.filter(ImageFilter.GaussianBlur(26))
    base.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sombra)
    base.paste(cp, (x, y))
    d = ImageDraw.Draw(base)
    if etiqueta:
        _tarja(d, 60, 52, etiqueta, 24, LARANJA, pad=(12, 6))
    if nome:
        bx, by = max(40, x - 120), y + int(cp.height * 0.62)
        _, b2 = _tarja(d, bx, by, nome, 30, LARANJA)
        if cargo:
            f = _fonte(22)
            larg = f.getlength(cargo)
            d.rectangle([bx, b2 + 4, bx + larg + 24, b2 + 40], fill=(30, 26, 22))
            d.text((bx + 12, b2 + 9), cargo, font=f, fill=(222, 212, 196))
    return base


def rotulos():
    p = ROOT / "data" / "moldura_rotulos.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def decide(titulo, im, rot, fracao):
    """-> None (tela cheia) | 'escura' | 'papel'"""
    m = rot.get("moldura")
    if m is False:
        return None
    if m in ("escura", "papel"):
        return m
    h = int(hashlib.md5(titulo.encode()).hexdigest()[:6], 16) / 0xFFFFFF
    if m is True or rot.get("etiqueta") or rot.get("nome") or (e_arquivo(im) and h < max(fracao, 0.0) / 0.6):
        return "papel" if h > 0.66 else "escura"
    return None


if __name__ == "__main__":
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    var = a[2] if len(a) > 2 else "escura"
    et = a[3] if len(a) > 3 else None
    if var == "capitulo":
        from make_photos import cover
        capitulo(cover(Image.open(src).convert("RGB"), 0.5, 0.5), *et.split("|")).save(dst, quality=92)
    elif var == "nome":
        n, c = et.split("|")
        emoldura(Image.open(src), "escura", nome=n, cargo=c).save(dst, quality=92)
    else:
        emoldura(Image.open(src), var, etiqueta=et).save(dst, quality=92)
    print(dst)
