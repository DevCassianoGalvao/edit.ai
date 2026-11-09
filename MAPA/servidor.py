# -*- coding: utf-8 -*-
"""
Servidor local do THANOS 3.0.
Rode este arquivo na MESMA pasta do buscador-imagens.html e abra:

    http://localhost:8000/

O que ele faz:
  - Serve a página buscador-imagens.html
  - /api/serper    -> Google Imagens (via sua chave Serper.dev)   [PRINCIPAL]
  - /api/bing      -> DESATIVADO (Bing saiu; rota devolve vazio)
  - /api/ddg       -> DuckDuckGo      (sem chave, complementa)
  - /api/openverse -> Openverse       (banco grátis, SEM chave)
  - /api/wikimedia -> Wikimedia Commons (SEM chave; guarda NOME PRÓPRIO)
  - /api/nasa      -> NASA Image Library (SEM chave; espaço/Terra/tecnologia)
  - /api/archive   -> Internet Archive   (SEM chave; registro de época)
  - /api/pexels    -> Pexels FOTO     (banco grátis, chave no header X-PEXELS-KEY)
  - /api/pixabay   -> Pixabay FOTO    (banco grátis, chave no header X-PIXABAY-KEY)
  - /api/pexels_video  -> Pexels VÍDEO   (mesma chave do X-PEXELS-KEY)
  - /api/pixabay_video -> Pixabay VÍDEO  (mesma chave do X-PIXABAY-KEY)
  - /api/youtube        -> busca no YouTube via yt-dlp, SEM API e SEM chave;
                           já devolve filtrado (fora: gameplay, clipe, react,
                           live, tutorial, slideshow de foto parada, Shorts...)
  - /api/youtube_save   -> baixa APENAS UM TRECHO (~20s) do vídeo do YouTube,
                           cortado no próprio download (--download-sections)
  - /api/youtube_status -> diagnóstico da camada YouTube (o botão "testar")
  - /api/save      -> baixa a imagem OU o vídeo e salva em downloads/paragrafo NN/
  - /api/partes    -> grava downloads/partes.json (a divisão do roteiro)

  Observação sobre "Canva": a Canva não tem API pública de busca de vídeos
  de banco - o banco de vídeos que a própria Canva usa internamente É o
  Pexels (a Canva comprou o Pexels em 2021). Então buscar no Pexels aqui
  já cobre o mesmo acervo que apareceria dentro da Canva.

Precisa só de Python 3 (nada de instalar pacote).
    Windows:  py servidor.py
    Mac/Linux: python3 servidor.py
"""

import json
import os
import re
import html
import mimetypes
import sys
import urllib.request
import urllib.parse
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Camada YouTube (yt-dlp). Fica num arquivo à parte porque tem regra de filtro
# demais pra caber aqui. Se o yt-dlp não estiver instalado, o servidor sobe do
# mesmo jeito - só as rotas /api/youtube* respondem avisando o que falta.
try:
    import youtube as yt
    YT_ERRO = ""
except Exception as _e:                                    # pragma: no cover
    yt = None
    YT_ERRO = str(_e)

# Bancos de imagem PUBLICOS que nao pedem chave (Wikimedia Commons, NASA,
# Internet Archive). Modulo leve, so stdlib - se faltar, o servidor sobe igual
# e as rotas /api/wikimedia etc. respondem [] avisando.
try:
    import bancos as bancos_publicos
    BANCOS_ERRO = ""
except Exception as _e:                                    # pragma: no cover
    bancos_publicos = None
    BANCOS_ERRO = str(_e)

# Camada de ÁUDIO/SINCRONIA (faster-whisper). Pesada de importar, então só
# entra quando a página realmente pedir - subir o servidor continua instantâneo.
audio = None
AUDIO_ERRO = ""


def _audio():
    """Importa a camada de áudio na primeira vez que alguém precisa dela."""
    global audio, AUDIO_ERRO
    if audio is None and not AUDIO_ERRO:
        try:
            import audio as _a
            audio = _a
        except Exception as e:
            AUDIO_ERRO = str(e)
    return audio


# Camada de MOTION GRAPHICS (só ffmpeg, importa na hora)
try:
    import motion as mg
    MG_ERRO = ""
except Exception as _e:                                    # pragma: no cover
    mg = None
    MG_ERRO = str(_e)

# A 3.0 sobe numa porta DIFERENTE da 2.0 de proposito: assim da pra deixar as
# duas ferramentas rodando ao mesmo tempo e comparar o resultado sem uma
# derrubar a outra. Da pra forcar outra porta:  py servidor.py 8010
PORT = 8877
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(ROOT, "downloads")
PAGE = "buscador-imagens.html"

# Um User-Agent de navegador ajuda MUITO: muitos sites bloqueiam downloads sem ele.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Mapeia idioma da página -> mercado/região das buscas
BING_MKT = {"pt": "pt-BR", "en": "en-US", "es": "es-ES"}
DDG_REGION = {"pt": "br-pt", "en": "us-en", "es": "es-es"}

EXT_BY_CT = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/pjpeg": ".jpg",
    "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif",
    "image/avif": ".avif", "image/svg+xml": ".svg", "image/bmp": ".bmp",
    "image/tiff": ".tif",
    # vídeo (bancos Pexels Vídeo / Pixabay Vídeo)
    "video/mp4": ".mp4", "video/webm": ".webm", "video/quicktime": ".mov",
    "video/x-matroska": ".mkv", "video/x-msvideo": ".avi",
    "video/mpeg": ".mpeg", "video/3gpp": ".3gp",
}
VIDEO_EXTS = (".mp4", ".webm", ".mov", ".mkv", ".avi", ".mpeg", ".3gp", ".m4v")


def _http_get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers, r.geturl()


# ---------------------------------------------------------------------------
# FONTE PRINCIPAL: Serper.dev (Google Imagens)
# ---------------------------------------------------------------------------
def serper_images(api_key, body):
    dados = {
        "q": body.get("q", ""),
        "num": int(body.get("num", 8)),
        "hl": body.get("hl", "pt"),
        "gl": body.get("gl", "br"),
    }
    # "tbs" e o filtro do proprio Google Imagens (ex.: "itp:photo" = so
    # fotografia, sem clipart/vetor/PNG). So vai quando a pagina pede.
    tbs = str(body.get("tbs", "") or "").strip()
    if tbs:
        dados["tbs"] = tbs
    payload = json.dumps(dados).encode("utf-8")
    req = urllib.request.Request(
        "https://google.serper.dev/images",
        data=payload,
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# FONTE 2: Bing Imagens (scraping simples, sem chave)
# ---------------------------------------------------------------------------
def bing_images(q, num, lang):
    mkt = BING_MKT.get(lang, "pt-BR")
    url = ("https://www.bing.com/images/async?q=%s&first=1&count=%d&mkt=%s&adlt=moderate"
           % (urllib.parse.quote(q), max(num, 12), mkt))
    headers = {"User-Agent": UA, "Accept-Language": mkt + ",en;q=0.8"}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
    except Exception:
        return []
    body = raw.decode("utf-8", "ignore")
    out, seen = [], set()
    # cada resultado tem um atributo m="{...json escapado...}" com murl (imagem real)
    for m in re.finditer(r'class="iusc"[^>]*?\sm="([^"]+)"', body):
        try:
            meta = json.loads(html.unescape(m.group(1)))
        except Exception:
            continue
        murl = meta.get("murl")
        if not murl or murl in seen:
            continue
        seen.add(murl)
        out.append({
            "imageUrl": murl,
            "title": meta.get("t", "") or q,
            "source": (meta.get("purl") or "").split("/")[2] if meta.get("purl", "").count("/") >= 2 else "bing.com",
            # resolução original da imagem, se o Bing informar (usada só pra
            # priorizar qualidade no app, nunca pra excluir)
            "width": meta.get("ow") or 0,
            "height": meta.get("oh") or 0,
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# FONTE 3: DuckDuckGo Imagens (sem chave: pega o token vqd e chama i.js)
# ---------------------------------------------------------------------------
def ddg_images(q, num, lang):
    region = DDG_REGION.get(lang, "br-pt")
    headers = {"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"}
    try:
        page, _, _ = _http_get(
            "https://duckduckgo.com/?q=%s&iax=images&ia=images" % urllib.parse.quote(q),
            headers=headers, timeout=20)
        txt = page.decode("utf-8", "ignore")
    except Exception:
        return []
    vqd = None
    for pat in (r'vqd="([\d-]+)"', r'vqd=([\d-]+)\&', r'"vqd":"([\d-]+)"'):
        mm = re.search(pat, txt)
        if mm:
            vqd = mm.group(1)
            break
    if not vqd:
        return []
    api = ("https://duckduckgo.com/i.js?l=%s&o=json&q=%s&vqd=%s&f=,,,&p=1&v7exp=a"
           % (region, urllib.parse.quote(q), vqd))
    h2 = dict(headers)
    h2["Referer"] = "https://duckduckgo.com/"
    h2["X-Requested-With"] = "XMLHttpRequest"
    try:
        raw, _, _ = _http_get(api, headers=h2, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("results") or []):
        img = it.get("image")
        if not img:
            continue
        out.append({
            "imageUrl": img,
            "title": it.get("title", "") or q,
            "source": it.get("source", "") or "duckduckgo",
            "width": it.get("width") or 0,
            "height": it.get("height") or 0,
        })
        if len(out) >= num:
            break
    return out


PEXELS_LOCALE = {"pt": "pt-BR", "en": "en-US", "es": "es-ES"}
PIXABAY_LANG = {"pt": "pt", "en": "en", "es": "es"}


# ---------------------------------------------------------------------------
# BANCO GRÁTIS 1: Openverse (Creative Commons, SEM chave) -> sempre disponível
# ---------------------------------------------------------------------------
def openverse_images(q, num, lang):
    url = ("https://api.openverse.org/v1/images/?q=%s&page_size=%d"
           "&mature=false&license_type=commercial,modification"
           % (urllib.parse.quote(q), max(min(num, 30), 3)))
    headers = {"User-Agent": UA, "Accept": "application/json"}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("results") or []):
        img = it.get("url")
        if not img:
            continue
        w, h = it.get("width") or 0, it.get("height") or 0
        # lado maior < 1600 px nao enche a tela com movimento (0 = desconhecido,
        # conferido depois do download)
        if (w or h) and max(w, h) < 1600:
            continue
        lic = ("%s %s" % (it.get("license") or "", it.get("license_version") or "")).strip()
        out.append({
            "imageUrl": img,
            "title": it.get("title", "") or q,
            "source": it.get("source", "") or "openverse",
            "width": w,
            "height": h,
            "license": ("CC " + lic.upper()) if lic and not lic.lower().startswith(("cc0", "pdm")) else (lic.upper() or "unverified"),
            "author": it.get("creator") or "",
            "page": it.get("foreign_landing_url") or "",
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# BANCO GRÁTIS 2: Pexels (chave grátis; ótimo b-roll de conceito)
# ---------------------------------------------------------------------------
def pexels_images(q, num, lang, key):
    if not key:
        return []
    loc = PEXELS_LOCALE.get(lang, "pt-BR")
    url = ("https://api.pexels.com/v1/search?query=%s&per_page=%d&locale=%s"
           % (urllib.parse.quote(q), max(min(num, 30), 1), loc))
    headers = {"User-Agent": UA, "Authorization": key}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("photos") or []):
        src = it.get("src") or {}
        img = src.get("large2x") or src.get("large") or src.get("original") or src.get("medium")
        if not img:
            continue
        out.append({
            "imageUrl": img,
            "title": it.get("alt", "") or q,
            "source": "pexels.com",
            "width": it.get("width") or 0,
            "height": it.get("height") or 0,
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# BANCO GRÁTIS 3: Pixabay (chave grátis; muito gráfico/negócios/conceito)
# ---------------------------------------------------------------------------
def pixabay_images(q, num, lang, key):
    if not key:
        return []
    lg = PIXABAY_LANG.get(lang, "pt")
    url = ("https://pixabay.com/api/?key=%s&q=%s&per_page=%d&image_type=photo"
           "&safesearch=true&lang=%s"
           % (urllib.parse.quote(key), urllib.parse.quote(q), max(min(num, 30), 3), lg))
    headers = {"User-Agent": UA, "Accept": "application/json"}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("hits") or []):
        img = it.get("largeImageURL") or it.get("webformatURL")
        if not img:
            continue
        out.append({
            "imageUrl": img,
            "title": it.get("tags", "") or q,
            "source": "pixabay.com",
            "width": it.get("imageWidth") or it.get("webformatWidth") or 0,
            "height": it.get("imageHeight") or it.get("webformatHeight") or 0,
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# BANCO DE VÍDEO 1: Pexels Vídeo (mesma chave grátis do Pexels de foto)
# Esse é também o banco que a própria Canva usa por baixo dos panos (a Canva
# comprou o Pexels em 2021) - então isso já cobre o "banco de vídeo da Canva".
# ---------------------------------------------------------------------------
def _melhor_arquivo_pexels(video):
    """Escolhe o arquivo de vídeo com melhor qualidade até full HD (arquivos
    4K deixam o download e a montagem desnecessariamente pesados)."""
    arquivos = video.get("video_files") or []
    candidatos = [a for a in arquivos if (a.get("width") or 0) <= 1920 and a.get("link")]
    pool = candidatos or arquivos
    if not pool:
        return None
    pool = sorted(pool, key=lambda a: (a.get("width") or 0), reverse=True)
    return pool[0]


def pexels_videos(q, num, lang, key, orientacao=""):
    if not key:
        return []
    loc = PEXELS_LOCALE.get(lang, "pt-BR")
    url = ("https://api.pexels.com/videos/search?query=%s&per_page=%d&locale=%s"
           % (urllib.parse.quote(q), max(min(num, 30), 1), loc))
    # a API do Pexels já filtra por formato direto na busca (landscape/portrait)
    orient_pexels = {"horizontal": "landscape", "vertical": "portrait"}.get(orientacao)
    if orient_pexels:
        url += "&orientation=%s" % orient_pexels
    headers = {"User-Agent": UA, "Authorization": key}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("videos") or []):
        arq = _melhor_arquivo_pexels(it)
        if not arq or not arq.get("link"):
            continue
        pics = it.get("video_pictures") or []
        out.append({
            "videoUrl": arq["link"],
            "thumbUrl": (pics[0].get("picture") if pics else None) or it.get("image") or "",
            "title": (it.get("user") or {}).get("name", "") or q,
            "source": "pexels.com",
            "width": arq.get("width") or it.get("width") or 0,
            "height": arq.get("height") or it.get("height") or 0,
            "duration": it.get("duration") or 0,
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# BANCO DE VÍDEO 2: Pixabay Vídeo (mesma chave grátis do Pixabay de foto)
# A API de vídeo do Pixabay NÃO tem parâmetro de orientação (só a de foto
# tem) - então, quando o usuário pede um formato específico, pedimos um lote
# maior de resultados e filtramos aqui mesmo pela largura/altura do próprio
# vídeo devolvido, descartando quem não bate.
# ---------------------------------------------------------------------------
def pixabay_videos(q, num, lang, key, orientacao=""):
    if not key:
        return []
    lg = PIXABAY_LANG.get(lang, "pt")
    # sem filtro nativo de orientação -> pede um lote maior pra sobrar depois
    # de descartar quem não bate com o formato pedido
    pedir = max(min(num, 30), 3)
    if orientacao in ("horizontal", "vertical"):
        pedir = max(min(pedir * 4, 100), 20)
    url = ("https://pixabay.com/api/videos/?key=%s&q=%s&per_page=%d"
           "&video_type=all&safesearch=true&lang=%s"
           % (urllib.parse.quote(key), urllib.parse.quote(q), pedir, lg))
    headers = {"User-Agent": UA, "Accept": "application/json"}
    try:
        raw, _, _ = _http_get(url, headers=headers, timeout=20)
        data = json.loads(raw.decode("utf-8", "ignore"))
    except Exception:
        return []
    out = []
    for it in (data.get("hits") or []):
        videos = it.get("videos") or {}
        # prioriza qualidade até full HD: large -> medium -> small -> tiny
        escolhido = None
        for tam in ("large", "medium", "small", "tiny"):
            v = videos.get(tam)
            if v and v.get("url"):
                escolhido = v
                break
        if not escolhido:
            continue

        w, h = escolhido.get("width") or 0, escolhido.get("height") or 0
        if orientacao == "horizontal" and not (w and h and w >= h):
            continue
        if orientacao == "vertical" and not (w and h and h > w):
            continue

        out.append({
            "videoUrl": escolhido["url"],
            "thumbUrl": escolhido.get("thumbnail") or "",
            "title": it.get("tags", "") or q,
            "source": "pixabay.com",
            "width": w,
            "height": h,
            "duration": it.get("duration") or 0,
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# SALVAR imagem OU vídeo no disco (com cara de navegador -> baixa muito mais)
# ---------------------------------------------------------------------------
def _safe(name, fallback):
    name = re.sub(r"[^\w\- ]+", "_", str(name or "")).strip().strip(".")
    return name or fallback


def _safe_arquivo(nome, padrao):
    """
    Igual ao _safe, mas para NOME DE ARQUIVO: preserva o ponto da extensao.
    O _safe foi feito pra nome de PASTA ("paragrafo 01") e troca o ponto por
    "_", o que transformava "narracao.mp3" em "narracao_mp3" e o arquivo nunca
    era encontrado. Continua barrando barra e ".." (nada de sair da pasta).
    """
    nome = os.path.basename(str(nome or "").replace("\\", "/"))
    nome = re.sub(r"[^\w\-. ]+", "_", nome).strip().lstrip(".")
    return nome or padrao


def save_image(folder, filename, url):
    folder = _safe(folder, "paragrafo 01")
    base = _safe(filename, "imagem")[:60]
    dest_dir = os.path.join(DOWNLOADS, folder)
    os.makedirs(dest_dir, exist_ok=True)

    referer = ""
    try:
        p = urllib.parse.urlparse(url)
        referer = "%s://%s/" % (p.scheme, p.netloc)
    except Exception:
        pass
    headers = {
        "User-Agent": UA,
        "Accept": "video/mp4,video/webm,video/*,image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": referer,
    }
    # A Wikimedia limita duro quem baixa em volume com User-Agent de navegador:
    # para ela isso e trafego automatizado anonimo. O `bancos.py` ja resolveu
    # isso para a BUSCA (UA que identifica a ferramenta + token OAuth), mas o
    # DOWNLOAD continuava saindo com cara de Chrome - e 52 de 252 imagens
    # levaram "429 Too many requests" depois de a curadoria ja te-las aprovado.
    # Mesma credencial, mesma politica, os dois caminhos.
    if "wikimedia.org" in referer or "wikipedia.org" in referer:
        try:
            import bancos as _b
            headers["User-Agent"] = _b.UA_WIKI
            if getattr(_b, "WIKIMEDIA_TOKEN", ""):
                headers["Authorization"] = "Bearer " + _b.WIKIMEDIA_TOKEN
        except Exception:
            pass
    # vídeo pesa mais e demora mais pra baixar que imagem -> timeout maior
    provavel_video = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() in VIDEO_EXTS
    data, resp_headers, _ = _http_get(url, headers=headers, timeout=90 if provavel_video else 25)

    ctype = (resp_headers.get("Content-Type") or "").split(";")[0].strip().lower()
    # se veio uma página HTML no lugar do arquivo, é link protegido/quebrado
    if ctype.startswith("text/") or data[:15].lstrip().lower().startswith(b"<!doctype") or data[:6].lower() == b"<html>":
        raise ValueError("o link não entrega o arquivo direto (página protegida)")
    tamanho_minimo = 4000 if (ctype.startswith("video/") or provavel_video) else 400
    if not data or len(data) < tamanho_minimo:
        raise ValueError("arquivo vazio ou muito pequeno")

    ext = EXT_BY_CT.get(ctype, "")
    if not ext:
        url_ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
        exts_validas = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".bmp", ".svg") + VIDEO_EXTS
        ext = url_ext if url_ext in exts_validas else ".jpg"

    if os.path.splitext(base)[1].lower() != ext:
        base = base + ext
    path = os.path.join(dest_dir, base)
    with open(path, "wb") as f:
        f.write(data)
    return os.path.relpath(path, ROOT)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silencioso
        pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-KEY")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _read_bytes(self):
        """Corpo cru, sem tentar interpretar como JSON (áudio e quadro JPEG)."""
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return b""
        lidos = b""
        while len(lidos) < n:
            pedaco = self.rfile.read(min(n - len(lidos), 1 << 20))
            if not pedaco:
                break
            lidos += pedaco
        return lidos

    def _read_body(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    # ---- GET: serve arquivos estáticos --------------------------------------
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            path = "/" + PAGE
        rel = path.lstrip("/")
        full = os.path.normpath(os.path.join(ROOT, rel))
        if not full.startswith(ROOT) or not os.path.isfile(full):
            self.send_error(404, "arquivo não encontrado")
            return
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        try:
            with open(full, "rb") as f:
                data = f.read()
        except Exception:
            self.send_error(500)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ---- POST: as APIs ------------------------------------------------------
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/api/serper":
            key = self.headers.get("X-API-KEY", "")
            if not key:
                return self._json(400, {"message": "Falta a chave da Serper.dev."})
            body = self._read_body()
            try:
                return self._json(200, serper_images(key, body))
            except urllib.error.HTTPError as e:
                msg = "Erro Serper.dev (%s). Verifique sua chave." % e.code
                return self._json(e.code if 400 <= e.code < 600 else 502, {"message": msg})
            except Exception as e:
                return self._json(502, {"message": "Falha ao consultar a Serper.dev: %s" % e})

        if path == "/api/bing":
            # Bing saiu: imagem pequena, com marca d'agua e fora do assunto com
            # frequencia alta demais. Rota mantida so para nao dar 404 em
            # pagina antiga; devolve vazio.
            return self._json(200, {"images": []})

        if path == "/api/ddg":
            b = self._read_body()
            imgs = ddg_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"))
            return self._json(200, {"images": imgs})

        if path == "/api/openverse":
            b = self._read_body()
            imgs = openverse_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"))
            return self._json(200, {"images": imgs})

        # ---- BANCOS PUBLICOS SEM CHAVE (Wikimedia / NASA / Internet Archive) --
        if path in ("/api/wikimedia", "/api/nasa", "/api/archive"):
            b = self._read_body()
            nome = path.rsplit("/", 1)[1]
            if bancos_publicos is None:
                return self._json(200, {"images": [], "erro":
                    "bancos.py nao carregou (%s)" % BANCOS_ERRO})
            fn = bancos_publicos.BANCOS.get(nome)
            try:
                imgs = fn(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"),
                          offset=int(b.get("offset", 0) or 0))
            except Exception as e:
                return self._json(200, {"images": [], "erro": str(e)})
            return self._json(200, {"images": imgs})

        # ---- VIDEO dos bancos publicos sem chave (download direto) ------------
        if path in ("/api/wikimedia_video", "/api/nasa_video"):
            b = self._read_body()
            nome = path.rsplit("/", 1)[1].replace("_video", "")
            if bancos_publicos is None:
                return self._json(200, {"videos": [], "erro":
                    "bancos.py nao carregou (%s)" % BANCOS_ERRO})
            fn = bancos_publicos.BANCOS_VIDEO.get(nome)
            try:
                vids = fn(b.get("q", ""), int(b.get("num", 4)), b.get("lang", "pt"),
                          offset=int(b.get("offset", 0) or 0))
            except Exception as e:
                return self._json(200, {"videos": [], "erro": str(e)})
            return self._json(200, {"videos": vids})

        if path == "/api/pexels":
            b = self._read_body()
            key = self.headers.get("X-PEXELS-KEY", "")
            imgs = pexels_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"), key)
            return self._json(200, {"images": imgs})

        if path == "/api/pixabay":
            b = self._read_body()
            key = self.headers.get("X-PIXABAY-KEY", "")
            imgs = pixabay_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"), key)
            return self._json(200, {"images": imgs})

        if path == "/api/pexels_video":
            b = self._read_body()
            key = self.headers.get("X-PEXELS-KEY", "")
            vids = pexels_videos(b.get("q", ""), int(b.get("num", 4)), b.get("lang", "pt"), key,
                                  b.get("orientacao", ""))
            return self._json(200, {"videos": vids})

        if path == "/api/pixabay_video":
            b = self._read_body()
            key = self.headers.get("X-PIXABAY-KEY", "")
            vids = pixabay_videos(b.get("q", ""), int(b.get("num", 4)), b.get("lang", "pt"), key,
                                   b.get("orientacao", ""))
            return self._json(200, {"videos": vids})

        # ---- YOUTUBE (sem API, sem chave) ----------------------------------
        if path.startswith("/api/youtube"):
            if yt is None:
                return self._json(200, {"videos": [], "erro":
                    "yt-dlp não está instalado neste Python (%s). "
                    "Rode:  py -m pip install -U yt-dlp" % YT_ERRO})
            b = self._read_body()

            if path == "/api/youtube":
                try:
                    r = yt.buscar(b.get("q", ""),
                                  num=int(b.get("num", 6)),
                                  minimo=int(b.get("minimo", 8)),
                                  maximo=int(b.get("maximo", 14400)),
                                  pool=int(b.get("pool", 40)))
                    return self._json(200, r)
                except Exception as e:
                    return self._json(200, {"videos": [], "erro": str(e)})

            if path == "/api/youtube_save":
                pasta = os.path.join(DOWNLOADS, _safe(b.get("folder", ""), "paragrafo 01"))
                try:
                    r = yt.baixar_trecho(
                        b.get("ytId", ""), pasta,
                        _safe(b.get("filename", ""), "youtube"),
                        inicio=b.get("inicio"),
                        segundos=int(b.get("segundos", 20)),
                        duracao_fonte=int(b.get("duracao", 0)))
                    if r.get("ok"):
                        r["path"] = os.path.relpath(r["path"], ROOT)
                    return self._json(200, r)
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

            if path == "/api/youtube_status":
                try:
                    return self._json(200, yt.diagnostico())
                except Exception as e:
                    return self._json(200, {"detalhe": str(e)})

        # ---- ÁUDIO E SINCRONIA ----------------------------------------------
        if path.startswith("/api/audio") or path.startswith("/api/transcrever") \
                or path in ("/api/alinhar", "/api/linha_do_tempo",
                            "/api/preparar_montagem"):

            # Enviar arquivo é a única rota de áudio que não precisa do whisper
            if path == "/api/audio_enviar":
                nome = _safe_arquivo(urllib.parse.unquote(self.headers.get("X-Nome-Arquivo", "")), "narracao")
                if not nome.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".opus")):
                    nome += ".mp3"
                dados = self._read_bytes()
                if len(dados) < 2000:
                    return self._json(200, {"ok": False, "message": "arquivo vazio ou pequeno demais"})
                try:
                    with open(os.path.join(ROOT, nome), "wb") as f:
                        f.write(dados)
                    return self._json(200, {"ok": True, "nome": nome, "tamanho": len(dados)})
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

            a = _audio()
            if a is None:
                return self._json(200, {"erro":
                    "faster-whisper não está instalado neste Python (%s). "
                    "Rode:  py -m pip install -U faster-whisper" % AUDIO_ERRO})
            b = self._read_body()

            if path == "/api/audio_listar":
                try:
                    return self._json(200, {"audios": a.listar_audios()})
                except Exception as e:
                    return self._json(200, {"audios": [], "erro": str(e)})

            if path == "/api/transcrever":
                nome = _safe_arquivo(b.get("arquivo", ""), "")
                caminho = os.path.join(ROOT, nome)
                if not nome or not os.path.isfile(caminho):
                    return self._json(200, {"erro": "áudio não encontrado: %s" % nome})
                tid = a.iniciar_transcricao(caminho,
                                            modelo=b.get("modelo", "small"),
                                            idioma=b.get("idioma") or None,
                                            forcar=bool(b.get("forcar")))
                return self._json(200, {"ok": True, "tarefa": tid,
                                        "duracao": a.duracao_audio(caminho)})

            if path == "/api/transcrever_status":
                return self._json(200, a.status_transcricao(
                    b.get("tarefa", ""), com_resultado=bool(b.get("resultado"))))

            if path == "/api/alinhar":
                try:
                    r = a.alinhar_partes(b.get("partes") or [],
                                         b.get("palavras") or [],
                                         float(b.get("duracao") or 0))
                    r["plano"] = a.plano_de_midia(
                        r, seg_por_item=float(b.get("seg_por_item") or 5),
                        minimo=int(b.get("minimo") or 2),
                        maximo=int(b.get("maximo") or 12))
                    return self._json(200, r)
                except Exception as e:
                    return self._json(200, {"erro": str(e)})

            # Escreve de uma vez tudo que o sincronizar.py precisa achar na
            # pasta: a legenda, o roteiro e a divisao exata das partes.
            if path == "/api/preparar_montagem":
                try:
                    escritos = []
                    dados = b.get("transcricao") or {}
                    if dados.get("palavras") or dados.get("frases"):
                        r = a.gerar_srt(dados, os.path.join(ROOT, "legenda.srt"))
                        escritos.append("legenda.srt (%d blocos)" % r["blocos"])
                    if b.get("roteiro"):
                        with open(os.path.join(ROOT, "roteiro.txt"), "w",
                                  encoding="utf-8") as f:
                            f.write(b["roteiro"])
                        escritos.append("roteiro.txt")
                    if b.get("partes"):
                        os.makedirs(DOWNLOADS, exist_ok=True)
                        with open(os.path.join(DOWNLOADS, "partes.json"), "w",
                                  encoding="utf-8") as f:
                            # a chave e "charsPer": e o nome que o
                            # sincronizar.py procura ao ler este arquivo
                            json.dump({"charsPer": b.get("chars"), "partes": b["partes"]},
                                      f, ensure_ascii=False, indent=2)
                        escritos.append("downloads/partes.json (%d partes)" % len(b["partes"]))
                    return self._json(200, {"ok": True, "escritos": escritos})
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

            if path == "/api/linha_do_tempo":
                try:
                    destino = a.salvar_linha_do_tempo(
                        os.path.join(ROOT, _safe_arquivo(b.get("audio", ""), "")) if b.get("audio") else "",
                        b.get("plano") or [], b.get("midias") or [])
                    return self._json(200, {"ok": True, "path": os.path.relpath(destino, ROOT)})
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

        # ---- COMECAR UM VIDEO NOVO -------------------------------------------
        # Sem "confirmar", so LISTA o que seria apagado - assim da pra conferir
        # antes, e ninguem perde trabalho por clicar errado.
        if path == "/api/novo_video":
            b = self._read_body()
            confirmar = bool(b.get("confirmar"))
            alvos = []

            if os.path.isdir(DOWNLOADS):
                for nome in sorted(os.listdir(DOWNLOADS)):
                    caminho = os.path.join(DOWNLOADS, nome)
                    if re.fullmatch(r"par[a\u00e1]grafo[\s_-]*\d+", nome.strip(), re.I) \
                            or nome in ("motion", "_motion_tmp", "_teste_youtube", "_exemplos"):
                        alvos.append(("pasta", caminho, "downloads/" + nome))
                    elif nome == "partes.json":
                        alvos.append(("arquivo", caminho, "downloads/partes.json"))

            if os.path.isdir(os.path.join(ROOT, "capcut")):
                alvos.append(("pasta", os.path.join(ROOT, "capcut"), "capcut/"))

            for nome in ("legenda.srt", "roteiro.txt", "linha_do_tempo.json",
                         "mapa.csv", "mapa.json", "concat.txt", "comando.txt"):
                caminho = os.path.join(ROOT, nome)
                if os.path.isfile(caminho):
                    alvos.append(("arquivo", caminho, nome))

            # o que fica, e por que - a pessoa precisa saber que nao vai perder
            mantidos = []
            if os.path.isfile(os.path.join(ROOT, "cookies.txt")):
                mantidos.append("cookies.txt (o acesso ao YouTube)")
            cache = os.path.join(DOWNLOADS, "_transcricoes")
            if os.path.isdir(cache):
                n_cache = len([x for x in os.listdir(cache) if x.endswith(".json")])
                mantidos.append("downloads/_transcricoes (%d transcricao(oes) em cache)" % n_cache)
            audios = [x for x in os.listdir(ROOT)
                      if x.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"))]
            # O audio e material de ORIGEM, nao subproduto: so entra na lista de
            # apagar se a pessoa pedir explicitamente.
            if audios and b.get("apagar_audio"):
                for nome in audios:
                    alvos.append(("arquivo", os.path.join(ROOT, nome), nome))
            elif audios:
                mantidos.append("%d audio(s): %s" % (len(audios), ", ".join(audios[:3])))
            if os.path.isfile(os.path.join(ROOT, "video.mp4")):
                mantidos.append("video.mp4 (o video que voce ja exportou)")

            if not confirmar:
                return self._json(200, {"ok": True, "simulacao": True,
                                        "apagar": [r for _, _, r in alvos],
                                        "manter": mantidos,
                                        "audios": [{"nome": x,
                                                    "mb": round(os.path.getsize(os.path.join(ROOT, x)) / 1e6, 1)}
                                                   for x in audios]})

            import shutil
            apagados, erros = [], []
            for tipo, caminho, rotulo in alvos:
                try:
                    if tipo == "pasta":
                        shutil.rmtree(caminho, ignore_errors=False)
                    else:
                        os.remove(caminho)
                    apagados.append(rotulo)
                except Exception as e:
                    erros.append("%s: %s" % (rotulo, e))
            return self._json(200, {"ok": True, "apagados": apagados,
                                    "erros": erros, "manter": mantidos})

        # ---- CURADORIA VISUAL (Gemini olha a imagem) -------------------------
        if path == "/api/ver_imagens":
            b = self._read_body()
            try:
                import visao
            except Exception as e:
                return self._json(200, {"erro": "visao.py nao carregou: %s" % e, "itens": []})
            try:
                return self._json(200, visao.avaliar(
                    b.get("chave", ""), b.get("texto", ""), b.get("urls") or [],
                    idioma=b.get("idioma", "pt"),
                    provedor=b.get("provedor", "gemini"),
                    assunto=b.get("assunto", "")))
            except Exception as e:
                return self._json(200, {"erro": str(e), "itens": []})

        # ---- MOTION GRAPHICS -------------------------------------------------
        if path.startswith("/api/mg_"):
            if mg is None:
                return self._json(200, {"ok": False, "message": MG_ERRO or "motion.py não carregou"})

            if path == "/api/mg_frame":
                try:
                    n = mg.receber_quadro(self.headers.get("X-MG-Job", ""),
                                          self.headers.get("X-MG-Frame", "0"),
                                          self._read_bytes())
                    return self._json(200, {"ok": True, "quadro": n})
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

            if path == "/api/mg_render":
                b = self._read_body()
                try:
                    return self._json(200, mg.montar(b.get("job", ""),
                                                     fps=int(b.get("fps", 30)),
                                                     folder=b.get("folder", ""),
                                                     filename=b.get("filename", "motion")))
                except Exception as e:
                    return self._json(200, {"ok": False, "message": str(e)})

            if path == "/api/mg_limpar":
                return self._json(200, {"ok": True, "removidos": mg.limpar_temporarios()})

        if path == "/api/save":
            b = self._read_body()
            try:
                rel = save_image(b.get("folder", ""), b.get("filename", ""), b.get("url", ""))
                return self._json(200, {"ok": True, "path": rel})
            except Exception as e:
                return self._json(200, {"ok": False, "message": str(e)})

        if path == "/api/partes":
            b = self._read_body()
            try:
                os.makedirs(DOWNLOADS, exist_ok=True)
                with open(os.path.join(DOWNLOADS, "partes.json"), "w", encoding="utf-8") as f:
                    json.dump(b, f, ensure_ascii=False, indent=2)
                return self._json(200, {"ok": True})
            except Exception as e:
                return self._json(200, {"ok": False, "message": str(e)})

        self._json(404, {"message": "rota desconhecida"})


def main():
    os.makedirs(DOWNLOADS, exist_ok=True)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("=" * 60)
    print("  THANOS 3.0 rodando!")
    print("  Abra no navegador:  http://localhost:%d/" % PORT)
    print("  Imagens salvas em:  %s" % DOWNLOADS)
    print("  Camadas: YouTube %s | Áudio/sincronia %s | Motion graphics %s"
          % ("ok" if yt else "OFF", "sob demanda", "ok" if mg else "OFF"))
    if mg:
        mg.limpar_temporarios()
    print("  (Ctrl+C para parar)")
    print("=" * 60)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        srv.server_close()


if __name__ == "__main__":
    main()
