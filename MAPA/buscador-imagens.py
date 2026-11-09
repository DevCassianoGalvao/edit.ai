# -*- coding: utf-8 -*-
"""
Servidor local do ImageFinder.
Rode este arquivo na MESMA pasta do buscador-imagens.html e abra:

    http://localhost:8000/

O que ele faz:
  - Serve a página buscador-imagens.html
  - /api/serper    -> Google Imagens (via sua chave Serper.dev)   [PRINCIPAL]
  - /api/bing      -> Bing Imagens    (sem chave, complementa)
  - /api/ddg       -> DuckDuckGo      (sem chave, complementa)
  - /api/openverse -> Openverse       (banco grátis, SEM chave)
  - /api/pexels    -> Pexels          (banco grátis, chave no header X-PEXELS-KEY)
  - /api/pixabay   -> Pixabay         (banco grátis, chave no header X-PIXABAY-KEY)
  - /api/save      -> baixa a imagem e salva em downloads/paragrafo NN/
  - /api/partes    -> grava downloads/partes.json (a divisão do roteiro)

Precisa só de Python 3 (nada de instalar pacote).
    Windows:  py servidor.py
    Mac/Linux: python3 servidor.py
"""

import json
import os
import re
import html
import mimetypes
import urllib.request
import urllib.parse
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(ROOT, "downloads")
PAGE = "buscador-imagens.html"

# Um User-Agent de navegador ajuda MUITO: muitos sites bloqueiam downloads sem ele.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Mapeia idioma da página -> mercado/região das buscas
BING_MKT = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "ru": "ru-RU"}
DDG_REGION = {"pt": "br-pt", "en": "us-en", "es": "es-es", "ru": "ru-ru"}

EXT_BY_CT = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/pjpeg": ".jpg",
    "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif",
    "image/avif": ".avif", "image/svg+xml": ".svg", "image/bmp": ".bmp",
    "image/tiff": ".tif",
}


def _http_get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers, r.geturl()


# ---------------------------------------------------------------------------
# FONTE PRINCIPAL: Serper.dev (Google Imagens)
# ---------------------------------------------------------------------------
def serper_images(api_key, body):
    payload = json.dumps({
        "q": body.get("q", ""),
        "num": int(body.get("num", 8)),
        "hl": body.get("hl", "pt"),
        "gl": body.get("gl", "br"),
    }).encode("utf-8")
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
        })
        if len(out) >= num:
            break
    return out


PEXELS_LOCALE = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "ru": "ru-RU"}
PIXABAY_LANG = {"pt": "pt", "en": "en", "es": "es", "ru": "ru"}


# ---------------------------------------------------------------------------
# BANCO GRÁTIS 1: Openverse (Creative Commons, SEM chave) -> sempre disponível
# ---------------------------------------------------------------------------
def openverse_images(q, num, lang):
    url = ("https://api.openverse.org/v1/images/?q=%s&page_size=%d"
           "&mature=false&license_type=all"
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
        out.append({
            "imageUrl": img,
            "title": it.get("title", "") or q,
            "source": it.get("source", "") or "openverse",
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
        })
        if len(out) >= num:
            break
    return out


# ---------------------------------------------------------------------------
# SALVAR imagem no disco (com cara de navegador -> baixa muito mais)
# ---------------------------------------------------------------------------
def _safe(name, fallback):
    name = re.sub(r"[^\w\- ]+", "_", str(name or "")).strip().strip(".")
    return name or fallback


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
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": referer,
    }
    data, resp_headers, _ = _http_get(url, headers=headers, timeout=25)

    ctype = (resp_headers.get("Content-Type") or "").split(";")[0].strip().lower()
    # se veio uma página HTML no lugar da imagem, é link protegido/quebrado
    if ctype.startswith("text/") or data[:15].lstrip().lower().startswith(b"<!doctype") or data[:6].lower() == b"<html>":
        raise ValueError("o link não entrega a imagem direto (página protegida)")
    if not data or len(data) < 400:
        raise ValueError("imagem vazia ou muito pequena")

    ext = EXT_BY_CT.get(ctype, "")
    if not ext:
        url_ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
        ext = url_ext if url_ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".bmp", ".svg") else ".jpg"

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
            b = self._read_body()
            imgs = bing_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"))
            return self._json(200, {"images": imgs})

        if path == "/api/ddg":
            b = self._read_body()
            imgs = ddg_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"))
            return self._json(200, {"images": imgs})

        if path == "/api/openverse":
            b = self._read_body()
            imgs = openverse_images(b.get("q", ""), int(b.get("num", 8)), b.get("lang", "pt"))
            return self._json(200, {"images": imgs})

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
    print("  ImageFinder rodando!")
    print("  Abra no navegador:  http://localhost:%d/" % PORT)
    print("  Imagens salvas em:  %s" % DOWNLOADS)
    print("  (Ctrl+C para parar)")
    print("=" * 60)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        srv.server_close()


if __name__ == "__main__":
    main()
