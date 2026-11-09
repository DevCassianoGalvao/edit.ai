# -*- coding: utf-8 -*-
"""
bancos.py - bancos de imagem PUBLICOS que nao pedem chave nenhuma.

Sao acervos "tier 0" (foto crua, sem manchete/tarja/logo por cima), do mesmo
nivel do Pexels/Pixabay/Openverse, mas com uma vantagem que aqueles nao tem:
guardam NOME PROPRIO. Nenhum banco de stock tem "Sevmorput", "Grupo Jiangnan"
ou "NS Savannah" - o Wikimedia Commons tem. Era esse buraco que obrigava a
puxar o assunto especifico so do Google (e vir com tarja de site de noticia).

  - Wikimedia Commons  -> foto/arquivo de quase tudo que tem nome
  - NASA Image Library -> espaco, Terra, foguete, satelite, tecnologia
  - Internet Archive    -> registro de epoca, cinejornal, foto historica

Todos devolvem a MESMA forma dos outros bancos do servidor:
    {"imageUrl", "title", "source", "width", "height"}
e, em falha de rede/parse, devolvem [] sem levantar excecao - o servidor segue
com as fontes que tiver.
"""

import json
import os as _os
import re as _re
import time as _time
import urllib.error
import urllib.parse
import urllib.request

_AQUI = _os.path.dirname(_os.path.abspath(__file__))

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


def _config(nome, arquivo):
    """Le uma chave/token do ambiente OU de um .txt na pasta (1a linha)."""
    v = (_os.environ.get(nome) or "").strip()
    if v:
        return v
    try:
        p = _os.path.join(_AQUI, arquivo)
        if _os.path.isfile(p):
            return open(p, encoding="utf-8").read().strip().splitlines()[0].strip()
    except Exception:
        pass
    return ""


# --- Wikimedia: token OAuth pessoal (GRATIS) tira o limite por IP -------------
# Sem token: ~500 req/h anonimo, e o 429 chega rapido num roteiro de 40 partes.
# Com token: 5000 req/h. Registre um consumidor "owner-only" em
#   https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose/oauth2
#   (marque "for use only by voce", "Applicable project" = *, grant "Basic rights")
# e ponha o Access token em WIKIMEDIA_TOKEN (ambiente) ou num wikimedia_token.txt.
WIKIMEDIA_TOKEN = _config("WIKIMEDIA_TOKEN", "wikimedia_token.txt")
_WM_CONTATO = _config("WIKIMEDIA_CONTACT", "wikimedia_contact.txt") or "https://localhost/thanos"
UA_WIKI = "THANOS-buscador/3.0 (%s)" % _WM_CONTATO

# Extensoes que servem para um video (o resto - SVG, PDF, TIFF gigante - o
# CapCut/ffmpeg trata mal, entao nem oferecemos).
_EXT_OK = (".jpg", ".jpeg", ".png", ".webp")

# Cache: memoria + DISCO. A mesma consulta feita por duas partes nao vai duas
# vezes a rede; e um vídeo re-buscado no dia seguinte reaproveita tudo. E o que
# mantem a ferramenta abaixo do limite da Wikimedia num roteiro de 40 partes.
_CACHE_DISCO = _os.path.join(_AQUI, "downloads", "_cache_bancos.json")
try:
    _os.makedirs(_os.path.dirname(_CACHE_DISCO), exist_ok=True)
    _CACHE = json.load(open(_CACHE_DISCO, encoding="utf-8")) if _os.path.isfile(_CACHE_DISCO) else {}
except Exception:
    _CACHE = {}
_CACHE_MAX = 3000
_cache_sujo = [0]


def _cache_salvar():
    try:
        json.dump(_CACHE, open(_CACHE_DISCO, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception:
        pass


# Freio adaptativo pro Commons: sem token o 429 vem rapido. O intervalo entre
# chamadas cresce a cada 429 e diminui quando da certo.
_wm_intervalo = [0.4 if WIKIMEDIA_TOKEN else 2.0]
_wm_ultimo = [0.0]


def _wm_freio(ok=None):
    if ok is None:  # antes da chamada
        gap = _time.monotonic() - _wm_ultimo[0]
        if gap < _wm_intervalo[0]:
            _time.sleep(_wm_intervalo[0] - gap)
        _wm_ultimo[0] = _time.monotonic()
    elif ok:
        _wm_intervalo[0] = max(0.4 if WIKIMEDIA_TOKEN else 1.0, _wm_intervalo[0] * 0.9)
    else:
        _wm_intervalo[0] = min(20.0, max(_wm_intervalo[0] * 1.7, 4.0))


def _get_json(url, headers=None, timeout=20, tentativas=2):
    """GET com cache (memoria+disco) e nova tentativa em 429/erro momentaneo."""
    if url in _CACHE:
        return _CACHE[url]
    hdr = headers or {"User-Agent": UA, "Accept": "application/json"}
    ehwiki = "commons.wikimedia.org" in url or "api.wikimedia.org" in url
    if ehwiki and WIKIMEDIA_TOKEN:
        hdr = dict(hdr)
        hdr["Authorization"] = "Bearer " + WIKIMEDIA_TOKEN

    erro = None
    for n in range(max(tentativas, 1)):
        if ehwiki:
            _wm_freio()
        req = urllib.request.Request(url, headers=hdr)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                dados = json.loads(r.read().decode("utf-8", "ignore"))
            if ehwiki:
                _wm_freio(True)
            if len(_CACHE) >= _CACHE_MAX:
                _CACHE.clear()
            _CACHE[url] = dados
            _cache_sujo[0] += 1
            if _cache_sujo[0] % 20 == 0:
                _cache_salvar()
            return dados
        except urllib.error.HTTPError as e:
            erro = e
            if ehwiki and e.code == 429:
                _wm_freio(False)
            if e.code in (429, 503) and n + 1 < tentativas:
                _time.sleep(2.0 * (n + 1))
                continue
            raise
        except Exception as e:
            erro = e
            if n + 1 < tentativas:
                _time.sleep(0.6)
                continue
            raise
    if erro:
        raise erro
    return {}


def _palavras_chave(q):
    """Versoes progressivamente mais curtas da consulta.

    A busca do Commons e conjuntiva: TODAS as palavras precisam aparecer. Uma
    frase como `merchant ship cargo ocean smokestack 1940s` nao tem um unico
    arquivo que satisfaca as seis - e o retorno e zero, calado. Era a metade
    silenciosa do problema de "busca fraca": nao vinha material errado, nao
    vinha material NENHUM.

    Um pesquisador humano faz o obvio: tira palavra do fim ate achar. Aqui a
    ordem importa - as primeiras palavras da frase sao as que descrevem a coisa
    ("merchant ship"), as ultimas sao qualificadores ("smokestack 1940s").
    """
    toks = [t for t in _re.split(r"[^\wÀ-ɏ]+", str(q or "")) if len(t) > 1]
    if not toks:
        return []
    versoes = []
    for corte in (len(toks), 3, 2, 1):
        if corte < 1 or corte > len(toks):
            continue
        v = " ".join(toks[:corte])
        if v and v not in versoes:
            versoes.append(v)
    return versoes


def _limite(num, teto=40):
    try:
        return max(min(int(num), teto), 3)
    except (TypeError, ValueError):
        return 8


def _offset(v):
    """Deslocamento na lista de resultados. E o que permite a MESMA frase
    devolver material DIFERENTE quando a mesma busca e repetida - sem isso,
    duas partes que caem na mesma consulta recebem exatamente as mesmas fotos."""
    try:
        return max(min(int(v), 400), 0)
    except (TypeError, ValueError):
        return 0


# ---------------------------------------------------------------------------
# O que o Commons tem de sobra e NAO serve de imagem de apoio.
#
# Todos sao a mesma coisa por baixo: DOCUMENTO PLANO FOTOGRAFADO - brasao,
# bandeira, mapa, logotipo, assinatura, medalha, cedula, cartaz, capa de
# revista, distintivo, diagrama, partitura, pagina digitalizada. Passam em todos
# os testes automaticos (sao JPG grandes, nitidos, sem marca d'agua) e chegam na
# tela como "imagem" - mas nenhum editor poe um brasao no meio de uma narracao.
#
# Foi o que apareceu ao medir: numa busca por "Kriegsmarine" o Commons devolveu
# capa de revista, cartaz de recrutamento e divisa de patente; em "Japan empire",
# uma cedula de 10 rupias e o texto da constituicao Meiji.
#
# Duas listas de proposito. Palavra INTEIRA para o que so e lixo quando e o
# assunto da foto ("map", "medal"); e trecho literal para o que so faz sentido
# em conjunto ("title page", "coat of arms").
# ---------------------------------------------------------------------------
_LIXO_PALAVRA = (
    "map mapa mapas karte carte kaart locator "
    "flag flagge bandera bandeira drapeau "
    "logo logotipo wordmark emblem emblema insignia distintivo "
    "signature assinatura autograph unterschrift "
    "stamp postage selo banknote cedula coin moeda currency rupees reichsmark "
    "medal medalha medaille orden ribbon barrette "
    "poster cartaz plakat affiche leaflet flyer panfleto "
    "diagram diagrama schematic esquema chart graph grafico graphique "
    "partitura score sheetmusic "
    "constitution constituicao certificate certificado diploma "
    "letterhead envelope postcard postal ephemera "
    "seal sello siegel crest heraldry heraldica wappen escudo brasao "
    "titelblatt titlepage frontispiece colophon "
    "timeline organigram organogram cladogram "
    "icon icone favicon sprite mockup template "
    "spectrum periodic"
).split()

_LIXO_TRECHO = (
    "coat of arms", "coat_of_arms", "title page", "cover of", "front cover",
    "sheet music", "family tree", "order of battle", "table of",
    "list of", "page from", "scan of", "excerpt from", "transcript",
    "rank insignia", "shoulder board", "collar patch", "cap badge",
    # divisa de patente: fundo chapado com um galao, catalogada aos milhares
    "-maate", "-gefreiter", "col, sleeve", "sleeve 19", "epaulette",
)

_LIXO_RE = _re.compile(r"(?<![a-z])(" + "|".join(_LIXO_PALAVRA) + r")(?![a-z])", _re.I)


LADO_MINIMO = 1600

# CC NonCommercial e NoDerivatives nao entram: canal monetizado e uso
# comercial, e um push-in dentro de um filme montado e obra derivada.
_LICENCA_PROIBIDA = _re.compile(r"(?<![a-z])(nc|nd|noncommercial|non-commercial|noderiv\w*)(?![a-z])", _re.I)


def licenca_proibida(licenca):
    return bool(licenca) and bool(_LICENCA_PROIBIDA.search(str(licenca).replace("-", " ")))


def _limpa_html(v):
    v = _re.sub(r"<[^>]+>", " ", str(v or ""))
    return _re.sub(r"\s+", " ", v).strip()[:160]


def _lixo_para_broll(titulo, arquivo=""):
    alvo = (str(titulo or "") + " " + str(arquivo or "").replace("_", " ")).lower()
    if any(m in alvo for m in _LIXO_TRECHO):
        return True
    return bool(_LIXO_RE.search(alvo))


# ---------------------------------------------------------------------------
# WIKIMEDIA COMMONS (sem chave) - o acervo de NOME PROPRIO
# ---------------------------------------------------------------------------
def _wikimedia_lote(consulta, pedir, off, lang):
    """UMA consulta ao Commons. Devolve a lista ja limpa (pode vir vazia)."""
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=%d&gsroffset=%d&gsrsearch=%s"
           "&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiurlwidth=1920"
           % (pedir, off, urllib.parse.quote(consulta)))
    headers = {"User-Agent": UA_WIKI, "Accept": "application/json",
               "Accept-Language": (lang or "pt") + ",en;q=0.8"}
    try:
        data = _get_json(url, headers=headers)
    except Exception:
        return []

    paginas = ((data.get("query") or {}).get("pages") or {})
    out = []
    # generator nao garante ordem; 'index' e a posicao do resultado da busca
    for _, pg in sorted(paginas.items(), key=lambda kv: (kv[1].get("index", 999))):
        info = (pg.get("imageinfo") or [{}])[0]
        mime = (info.get("mime") or "").lower()
        arquivo = pg.get("title", "").replace("File:", "")
        # SVG e desenho vetorial - bandeira, brasao, diagrama. O Commons entrega
        # um PNG renderizado no thumburl, entao o teste de extensao da URL nao
        # pega: tem que olhar o mime E o nome do arquivo original.
        if "image" not in mime or "svg" in mime or arquivo.lower().endswith(".svg"):
            continue
        img = info.get("thumburl") or info.get("url")
        if not img or not img.lower().split("?")[0].endswith(_EXT_OK):
            continue
        meta = info.get("extmetadata") or {}
        titulo = ((meta.get("ObjectName") or {}).get("value")
                  or (meta.get("ImageDescription") or {}).get("value")
                  or arquivo)
        # extmetadata devolve HTML as vezes - tira as tags mais grosseiras
        titulo = urllib.parse.unquote(str(titulo))
        titulo = titulo.replace("<p>", " ").replace("</p>", " ")
        titulo = _re.sub(r"<[^>]+>", " ", titulo)
        # Metadado do Wikidata vazado para dentro da legenda. O Commons devolve
        # coisas como `Panorama of Ships title QS:P1476,en:"Panorama of Ships"
        # label QS:...` - o titulo de verdade esta ali, mas afogado em ruido
        # que conta como palavra e estraga o calculo de relevancia (o
        # denominador cresce e a nota da imagem certa cai).
        # A ordem importa: o rotulo ("title", "label") sai JUNTO com o QS: que
        # ele anuncia. Tirar o QS: primeiro deixava "title ," orfao no meio da
        # frase, e "title" e uma palavra que conta no denominador.
        titulo = _re.sub(r"\b(title|label|caption|description)\s+QS:[^\s,]*", " ", titulo)
        titulo = _re.sub(r"\bQS:[^\s,]*", " ", titulo)
        titulo = _re.sub(r",?\s*\b[a-z]{2}:\"([^\"]*)\"", r" \1 ", titulo)
        titulo = _re.sub(r"[\"]", " ", titulo)
        titulo = _re.sub(r"\s*,\s*(?=[,\s]|$)", " ", titulo)
        titulo = _re.sub(r"\s+", " ", titulo).strip(" ,;-")
        # O Commons repete o titulo em cada idioma catalogado, e o que sobra
        # depois da limpeza e a mesma frase duas ou tres vezes seguidas. Isso
        # NAO e inofensivo: cada repeticao infla o denominador da relevancia,
        # entao a imagem certa termina com nota mais baixa que uma generica de
        # titulo curto.
        titulo = _re.sub(r"\b(.{6,60}?)\s+\1\b", r"\1", titulo, flags=_re.I)
        titulo = _re.sub(r"\s+", " ", titulo).strip(" ,;-")[:180] or consulta
        if _lixo_para_broll(titulo, arquivo):
            continue
        # Foto pequena nao enche uma tela de 1920x1080 com movimento por cima.
        # O piso era 640 px (servia para o CapCut); o filme so de fotos nao
        # amplia mais que 1,3x, entao o lado maior precisa de 1600 px.
        larg = info.get("width") or 0
        alt = info.get("height") or 0
        if max(larg, alt) < LADO_MINIMO:
            continue
        # Licenca como regra de POOL: NC e ND nunca chegam a curadoria. Rejeitar
        # arquivo por arquivo deixava o proximo NC entrar na rodada seguinte.
        licenca = _limpa_html((meta.get("LicenseShortName") or {}).get("value"))
        if licenca_proibida(licenca):
            continue
        out.append({
            "imageUrl": img,
            "title": titulo,
            "source": "commons.wikimedia.org",
            "width": info.get("thumbwidth") or info.get("width") or 0,
            "height": info.get("thumbheight") or info.get("height") or 0,
            "license": licenca or "unverified",
            "author": _limpa_html((meta.get("Artist") or {}).get("value")),
            "page": info.get("descriptionurl") or "",
            "origWidth": larg,
            "origHeight": alt,
        })
    return out


def wikimedia_images(q, num, lang="pt", offset=0):
    if not q or not q.strip():
        return []
    n = _limite(num)
    off = _offset(offset)
    # Pede MAIS do que vai devolver: o filtro de lixo corta brasao, mapa, logo
    # e assinatura, e sem folga a parte terminaria vazia por causa do proprio
    # filtro.
    pedir = min(n * 3, 50)

    # Cascata de encurtamento. A busca do Commons e conjuntiva, entao a frase
    # inteira quase sempre devolve zero; encurtar e o que faz a fonte responder.
    vistos, out = set(), []
    for consulta in _palavras_chave(q):
        for item in _wikimedia_lote(consulta, pedir, off, lang):
            if item["imageUrl"] in vistos:
                continue
            vistos.add(item["imageUrl"])
            out.append(item)
        if len(out) >= n:
            break
    return out[:n]


# ---------------------------------------------------------------------------
# NASA IMAGE LIBRARY (sem chave)
# ---------------------------------------------------------------------------
def nasa_images(q, num, lang="pt", offset=0):
    if not q or not q.strip():
        return []
    n = _limite(num, teto=30)
    # a API da NASA pagina de 100 em 100; o deslocamento vira pagina + corte
    off = _offset(offset)
    pagina = 1 + off // 100
    url = ("https://images-api.nasa.gov/search?media_type=image&q=%s&page=%d"
           % (urllib.parse.quote(q), pagina))
    try:
        data = _get_json(url, headers={"User-Agent": UA})
    except Exception:
        return []

    itens = ((data.get("collection") or {}).get("items") or [])[off % 100:]
    out = []
    for it in itens:
        dados = (it.get("data") or [{}])[0]
        links = it.get("links") or []
        thumb = next((l.get("href") for l in links if l.get("href")), "")
        if not thumb:
            continue
        # o link vem como ..._id/<id>~thumb.jpg. ~large.jpg e a versao de tela e
        # existe SEMPRE que a original e imagem (o ~orig as vezes e .tif e ai o
        # ~orig.jpg nao existe - ~large e o alvo seguro).
        cheia = thumb
        for marca in ("~thumb.jpg", "~thumb.png", "~small.jpg", "~medium.jpg"):
            if thumb.endswith(marca):
                cheia = thumb[: -len(marca)] + "~large.jpg"
                break
        titulo = (dados.get("title") or dados.get("description_508")
                  or dados.get("description") or q)
        out.append({
            "imageUrl": cheia,
            "title": str(titulo)[:180],
            "source": "images.nasa.gov",
            "width": 0, "height": 0,
        })
        if len(out) >= n:
            break
    return out


# ---------------------------------------------------------------------------
# INTERNET ARCHIVE (sem chave) - registro de epoca / dominio publico
# ---------------------------------------------------------------------------
def archive_images(q, num, lang="pt", offset=0):
    if not q or not q.strip():
        return []
    n = _limite(num, teto=30)
    off = _offset(offset)
    pagina = 1 + off // max(n, 1)
    consulta = '(%s) AND mediatype:image' % q
    url = ("https://archive.org/advancedsearch.php?q=%s"
           "&fl[]=identifier&fl[]=title&rows=%d&page=%d&output=json"
           % (urllib.parse.quote(consulta), n, pagina))
    try:
        data = _get_json(url, headers={"User-Agent": UA})
    except Exception:
        return []

    docs = (((data.get("response") or {}).get("docs")) or [])
    out = []
    for d in docs:
        ident = d.get("identifier")
        if not ident:
            continue
        # /services/img/<id> redireciona para a imagem representativa do item -
        # sempre existe e ja vem em tamanho de tela.
        out.append({
            "imageUrl": "https://archive.org/services/img/%s" % urllib.parse.quote(ident),
            "title": str(d.get("title") or q)[:180],
            "source": "archive.org",
            "width": 0, "height": 0,
        })
        if len(out) >= n:
            break
    return out


# ===========================================================================
# VIDEO - bancos publicos sem chave, com DOWNLOAD DIRETO (nao passam pelo
# "confirme que voce nao e um robo" do YouTube). Devolvem a mesma forma que o
# Pexels Video / Pixabay Video do servidor:
#     {"videoUrl", "thumbUrl", "title", "source", "width", "height", "duration"}
# ===========================================================================

def wikimedia_videos(q, num, lang="pt", offset=0):
    if not q or not q.strip():
        return []
    n = _limite(num, teto=25)
    off = _offset(offset)
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=%d&gsroffset=%d&gsrsearch=%s"
           "&prop=imageinfo&iiprop=url|size|mime|duration&iiurlwidth=640"
           % (n, off, urllib.parse.quote(q + " filetype:video")))
    headers = {"User-Agent": UA, "Accept": "application/json"}
    try:
        data = _get_json(url, headers=headers)
    except Exception:
        return []
    paginas = ((data.get("query") or {}).get("pages") or {})
    out = []
    for _, pg in sorted(paginas.items(), key=lambda kv: kv[1].get("index", 999)):
        info = (pg.get("imageinfo") or [{}])[0]
        mime = (info.get("mime") or "").lower()
        vurl = info.get("url")
        if "video" not in mime or not vurl:
            continue
        dur = info.get("duration") or 0
        # clipe curto demais nao serve de b-roll; longo demais vira download
        # pesado (o corte para o trecho e feito depois, no sincronizar.py).
        if dur and (dur < 2 or dur > 1200):
            continue
        out.append({
            "videoUrl": vurl,
            "thumbUrl": info.get("thumburl") or "",
            "title": pg.get("title", "").replace("File:", "")[:180] or q,
            "source": "commons.wikimedia.org",
            "width": info.get("width") or 0,
            "height": info.get("height") or 0,
            "duration": round(float(dur), 1) if dur else 0,
        })
        if len(out) >= n:
            break
    return out


def nasa_videos(q, num, lang="pt", offset=0):
    if not q or not q.strip():
        return []
    n = _limite(num, teto=12)
    off = _offset(offset)
    url = ("https://images-api.nasa.gov/search?media_type=video&q=%s&page=%d"
           % (urllib.parse.quote(q), 1 + off // 100))
    try:
        data = _get_json(url, headers={"User-Agent": UA})
    except Exception:
        return []
    itens = ((data.get("collection") or {}).get("items") or [])[off % 100:]
    out = []
    for it in itens:
        col = it.get("href")
        if not col:
            continue
        dados = (it.get("data") or [{}])[0]
        links = it.get("links") or []
        thumb = next((l.get("href") for l in links if l.get("href")), "")
        try:
            assets = _get_json(col, headers={"User-Agent": UA})
        except Exception:
            continue
        mp4s = [a for a in assets if isinstance(a, str) and a.lower().endswith(".mp4")]
        # ~medium e o equilibrio: ~orig as vezes tem 1-2 GB, ~preview e curto.
        escolhido = ""
        for marca in ("~medium.mp4", "~small.mp4", "~mobile.mp4", "~large.mp4"):
            escolhido = next((a for a in mp4s if a.endswith(marca)), "")
            if escolhido:
                break
        if not escolhido and mp4s:
            escolhido = mp4s[0]
        if not escolhido:
            continue
        out.append({
            "videoUrl": escolhido.replace("http://", "https://"),
            "thumbUrl": thumb,
            "title": str(dados.get("title") or q)[:180],
            "source": "images.nasa.gov",
            "width": 0, "height": 0, "duration": 0,
        })
        if len(out) >= n:
            break
    return out


BANCOS = {
    "wikimedia": wikimedia_images,
    "nasa": nasa_images,
    "archive": archive_images,
}

BANCOS_VIDEO = {
    "wikimedia": wikimedia_videos,
    "nasa": nasa_videos,
}
