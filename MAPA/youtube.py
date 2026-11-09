# -*- coding: utf-8 -*-
"""
youtube.py - camada de VIDEO DO YOUTUBE do THANOS 3.0, sem nenhuma API paga.

Tudo aqui roda em cima do yt-dlp (ja instalado como modulo do Python).
Duas operacoes, e so:

  1. buscar()   -> pesquisa no YouTube (ytsearch40), PONTUA e FILTRA os
                   resultados, e devolve so o que presta como b-roll.
                   NAO baixa nada. E rapido (~2s) e nao precisa de login.

  2. baixar_trecho() -> baixa APENAS UM PEDACO (padrao 20s) do video
                   escolhido, ja cortado no servidor do YouTube
                   (--download-sections). Nunca baixa o video inteiro.

A regra de ouro do modulo: video ruim nao chega na tela. O que o buscador de
imagens ja fazia com foto (jogar clipart/marca d'agua pro fim da fila) aqui e
feito com video - e mais duro, porque o lixo do YouTube e pior: gameplay,
clipe de musica, react, prank, desenho animado, live, aula, "top 10",
slideshow de foto parada... nada disso serve de imagem de apoio.
"""

import json
import os
import re
import subprocess
import sys
import time
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))

# yt-dlp esta instalado como modulo (pip install yt-dlp) -> chamamos pelo
# mesmo Python que esta rodando o servidor, assim nunca da "comando nao
# encontrado" nem pega uma versao velha que esteja no PATH.
YTDLP = [sys.executable, "-m", "yt_dlp"]


def _acha(prog):
    """Procura um executavel no PATH (equivalente ao 'which')."""
    import shutil
    return shutil.which(prog)


# O yt-dlp precisa de um motor JavaScript pra resolver o desafio do YouTube.
# Por padrao ele so aceita Deno; se a maquina tiver Node ou Bun instalado,
# avisamos - sem isso alguns formatos simplesmente nao aparecem.
def _args_motor():
    for runtime in ("deno", "node", "bun"):
        if _acha(runtime):
            return ["--js-runtimes", runtime]
    return []


# PO token: e o "carimbo" que o YouTube pede pra liberar o video sem login.
# Quando o plugin bgutil-ytdlp-pot-provider esta instalado, pedir o token
# sempre destrava boa parte dos bloqueios. Quando nao esta, esses argumentos
# sao inofensivos.
ARGS_EXTRA = ["--extractor-args", "youtube:fetch_pot=always"]

MOTOR = _args_motor()

# Windows: nao abrir janelinha preta de console a cada chamada
_NOWIN = {}
if os.name == "nt":
    _si = subprocess.STARTUPINFO()
    _si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _NOWIN = {"startupinfo": _si, "creationflags": 0x08000000}


# ===========================================================================
# COOKIES - o unico ponto em que o YouTube pode pedir "prove que voce nao e um
# robo". A BUSCA funciona sempre sem nada. O DOWNLOAD, dependendo do IP, pede
# cookie de uma sessao logada. Entao tentamos, em ordem:
#
#   1. cookies.txt na pasta do projeto (exportado por extensao do navegador)
#   2. cookies direto do navegador instalado (Firefox funciona ate aberto;
#      Chrome/Edge 127+ criptografam e normalmente falham)
#   3. sem cookie nenhum (funciona em muita rede domestica)
#
# A estrategia que der certo fica guardada, pra nao ficar testando de novo a
# cada download.
# ===========================================================================
COOKIES_TXT = os.path.join(ROOT, "cookies.txt")
# Firefox primeiro entre os navegadores: e o unico que entrega o cookie mesmo
# com o navegador aberto. Chrome e Edge da versao 127 pra frente criptografam
# (App-Bound Encryption) e quase sempre falham - ficam no fim da fila.
NAVEGADORES = ["firefox", "edge", "chrome", "brave", "vivaldi", "chromium", "opera"]

_estrategia_ok = None       # rotulo da que funcionou por ultimo -> tenta ela antes
_sem_cookie_ok = set()      # fontes de cookie quebradas: nao tenta de novo nesta sessao
_bloqueadas = set()         # estrategias que o YouTube recusou -> tenta so no fim


def _estrategias():
    """Todas as formas de autenticar, da mais barata/confiavel pra menos."""
    fora = []
    if os.path.isfile(COOKIES_TXT):
        fora.append(("cookies.txt", ["--cookies", COOKIES_TXT]))
    fora.append(("sem cookie", []))          # rapido de tentar, e as vezes basta
    for nav in NAVEGADORES:
        fora.append(("navegador:" + nav, ["--cookies-from-browser", nav]))
    return fora


def _ordem_tentativas():
    """
    Ordem de tentativa: a que funcionou por ultimo, depois as ainda nao
    reprovadas, depois as que o YouTube recusou (pode ter mudado). Fonte de
    cookie QUEBRADA (navegador nao instalado, banco travado) sai da lista de
    vez - nao adianta insistir.
    """
    todas = [e for e in _estrategias() if e[0] not in _sem_cookie_ok]
    def peso(e):
        if e[0] == _estrategia_ok: return 0
        return 2 if e[0] in _bloqueadas else 1
    return sorted(todas, key=peso)


# Os cookies que so existem quando a sessao esta LOGADA. Sem eles o arquivo
# ate parece um cookie valido (tem PREF, VISITOR_INFO1_LIVE, SOCS...), mas o
# YouTube trata a conexao como anonima e o download cai no "prove que voce nao
# e um robo". E o erro mais comum: exportar de uma aba deslogada, ou de uma
# janela anonima, ou de outro perfil do navegador.
COOKIES_DE_LOGIN = ["SID", "HSID", "SSID", "APISID", "SAPISID",
                    "__Secure-1PSID", "LOGIN_INFO"]


def conferir_cookies(caminho=None):
    """
    Le o cookies.txt e diz se ele tem login. Nao fala com o YouTube - so
    olha o arquivo, entao e instantaneo.
    """
    caminho = caminho or COOKIES_TXT
    if not os.path.isfile(caminho):
        return {"existe": False}

    nomes = set()
    total = 0
    try:
        with open(caminho, encoding="utf-8", errors="ignore") as f:
            for linha in f:
                if linha.startswith("#") or "\t" not in linha:
                    continue
                partes = linha.rstrip("\n").split("\t")
                if len(partes) >= 6 and "youtube.com" in partes[0]:
                    nomes.add(partes[5])
                    total += 1
    except Exception as e:
        return {"existe": True, "erro": str(e)}

    presentes = [c for c in COOKIES_DE_LOGIN if c in nomes]
    faltando = [c for c in COOKIES_DE_LOGIN if c not in nomes]
    # SID + SAPISID e o par que de fato autentica; sem eles nao ha sessao
    logado = ("SID" in nomes and "SAPISID" in nomes)
    return {"existe": True, "linhas": total, "logado": logado,
            "presentes": presentes, "faltando": faltando,
            "idade_h": round((time.time() - os.path.getmtime(caminho)) / 3600, 1)}


def _e_bloqueio(txt):
    """O YouTube recusou: 'prove que voce nao e um robo'."""
    baixo = (txt or "").lower()
    return ("not a bot" in baixo
            or "sign in to confirm" in baixo
            or "please sign in" in baixo
            or "confirm your age" in baixo
            or "--cookies" in baixo)


def _erro_de_cookie(txt):
    """
    Nao foi o YouTube que recusou: foi a FONTE do cookie que nao serviu
    (navegador nao instalado, arquivo travado porque o navegador esta aberto,
    cookie criptografado pelo Chrome novo, perfil vazio). Nesses casos tem que
    seguir pra proxima estrategia, nao parar.
    """
    baixo = (txt or "").lower()
    return any(x in baixo for x in (
        "could not find", "could not copy", "cookie database", "cookies database",
        "unsupported browser", "failed to decrypt", "no such file",
        "permission denied", "needs to be reloaded", "keyring", "profile"))


def _rodar(args, timeout=90):
    """Roda o yt-dlp e devolve (codigo, stdout, stderr)."""
    try:
        p = subprocess.run(YTDLP + MOTOR + args, capture_output=True,
                           timeout=timeout, **_NOWIN)
        return (p.returncode,
                p.stdout.decode("utf-8", "ignore"),
                p.stderr.decode("utf-8", "ignore"))
    except subprocess.TimeoutExpired:
        return (-1, "", "tempo esgotado (%ss)" % timeout)
    except Exception as e:
        return (-1, "", str(e))


# ===========================================================================
# NORMALIZACAO DE TEXTO (titulo e canal vem com acento, emoji, caixa alta...)
# ===========================================================================
def _limpo(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s.lower()).strip()


def _tokens(s):
    return [t for t in re.split(r"[^0-9a-z]+", _limpo(s)) if len(t) > 2]


# ===========================================================================
# LISTA NEGRA - o que NUNCA serve de imagem de apoio.
# Cada entrada e (regex, rotulo do motivo). O rotulo aparece na tela pro editor
# entender POR QUE aquele video sumiu.
# ===========================================================================
VETO = [
    (r"\b(gameplay|game play|lets play|let s play|walkthrough|speedrun|"
     r"minecraft|fortnite|roblox|gta ?[iv0-9]|free fire|valorant|"
     r"call of duty|fifa ?\d*|pes ?\d*|among us|brawl stars|clash royale|"
     r"jogo completo|zerando|mod pack|full game|speed run)\b", "jogo/gameplay"),

    (r"\b(official video|official music video|music video|lyrics|lyric video|letra|"
     r"karaoke|full album|album completo|audio oficial|clipe oficial|"
     r"dvd ao vivo|cover|remix|instrumental|playlist de musicas|"
     r"nightcore|slowed reverb|bass boosted)\b", "musica/clipe"),

    (r"\b(react|reacao|reagindo|reaction|reagi|first time hearing|"
     r"pegadinha|prank|troll|desafio|challenge|24 horas)\b", "react/pegadinha"),

    (r"\b(asmr|mukbang|unboxing|haul|vlog|vlogs|day in my life|rotina|"
     r"morning routine|grwm|storytime|story time)\b", "vlog/asmr"),

    (r"\b(podcast|cortes do|corte do|entrevista completa|ao vivo agora|"
     r"transmissao ao vivo|stream|streaming ao vivo|debate ao vivo)\b", "podcast/live"),

    (r"\b(tutorial|como fazer|how to|passo a passo|aula ?\d*|curso completo|"
     r"aprenda |dicas de |masterclass|webinar|after effects|premiere|photoshop|"
     r"canva|capcut|editar video)\b", "tutorial/aula"),

    (r"\b(top ?\d+|os \d+ maiores|ranking|tier list|compilation|"
     r"compilado|melhores momentos|best of|momentos engracados|fails|"
     r"tente nao rir|memes|meme )\b", "top10/compilado"),

    (r"\b(episodio|episode|ep ?\d+|cap ?\d+|capitulo|temporada|season ?\d+|"
     r"serie completa|filme completo|full movie|dublado completo|trailer oficial|"
     r"teaser|desenho animado|cartoon|anime |amv )\b", "episodio/filme"),

    (r"\b(slideshow|slide show|apresentacao de slides|imagens de fundo|"
     r"wallpaper|papel de parede|galeria de fotos|photo slideshow|"
     r"picture slideshow)\b", "slideshow/foto parada"),

    (r"(#shorts|\bshorts\b|\btiktok\b|\breels\b|status whatsapp|\bedits?\b)", "shorts/vertical"),

    (r"\b(sermao|culto|pregacao|missa|louvor|adoracao)\b", "culto/pregacao"),
]
VETO = [(re.compile(p), m) for p, m in VETO]

# ===========================================================================
# LISTA VERDE - sinais de que o video E imagem de apoio limpa
# ===========================================================================
BONUS_PALAVRA = [
    (r"\b(stock footage|stock video|free footage|free stock|no copyright|"
     r"royalty free|copyright free|creative commons)\b", 40, "banco de imagem"),
    (r"\b(b ?roll|broll|footage|imagens de arquivo|archive footage|"
     r"file footage|raw footage|no talking|sem narracao)\b", 32, "b-roll"),
    (r"\b(drone|aerial|aereo|vista aerea|timelapse|time lapse|hyperlapse|"
     r"slow motion|camera lenta|close up|macro)\b", 26, "plano cinematografico"),
    (r"\b(cinematic|cinematografico|documentario|documentary|reportagem|"
     r"walking tour|city walk|street view|caminhando por)\b", 20, "documental"),
    (r"\b(4k|uhd|2160p|1080p|full hd)\b", 14, "alta resolucao"),
]
BONUS_PALAVRA = [(re.compile(p), v, m) for p, v, m in BONUS_PALAVRA]

# Nao chega a ser veto (as vezes e a unica coisa que existe do assunto), mas
# derruba a nota: video de alguem falando pra camera, com corte de estudio,
# logo do canal e legenda queimada.
FALANTE = re.compile(
    r"\b(vem com a gente|um dia (de|com)|fui (ate|para|no|na)|visita (na|ao|a)|"
    r"conheci|mostrando|te mostro|eu (fui|comprei|testei)|minha |meu |nosso |"
    r"conta tudo|explica|entenda|analise|opiniao|comentario|resposta a|"
    r"antes de comprar|vale a pena|o que eu|primeira vez|"
    r"interview|entrevista|talks?|conversa com|bate.?papo)\b", re.I)

# Preview de banco PAGO: a imagem vem com marca d'agua queimada no meio.
MARCA_DAGUA = re.compile(
    r"\b(shutterstock|getty ?images|istock|adobe stock|alamy|depositphotos|"
    r"dreamstime|123rf|envato|videohive|pond5|artgrid|filmsupply)\b", re.I)

# Canais institucionais / de arquivo: imagem limpa, sem marca d'agua, sem
# apresentador falando pra camera.
CANAIS_BONS = [
    "reuters", "ap archive", "associated press", "afp", "agence france",
    "bloomberg", "cnbc", "bbc", "deutsche welle", "euronews", "ruptly",
    "guardian", "nytimes", "new york times", "washington post",
    "nasa", "european space", "united nations", "world bank",
    "world economic forum",
    "pexels", "pixabay", "videvo", "mixkit", "coverr", "storyblocks",
    "mazwai", "vidsplay", "life of vids", "free stock",
    "national geographic", "discovery", "smithsonian",
    "agencia brasil", "senado", "camara dos deputados", "tv brasil",
]

# Canais que so produzem lixo pro nosso uso
CANAIS_RUINS = ["kids", "infantil", "criancas", "nursery", "cocomelon",
                "gameplay", "gamer", "jogos", "clipe oficial", "musica"]


def _thumb(item):
    """Melhor thumbnail que o YouTube ja entrega direto no navegador."""
    vid = item.get("id") or ""
    if vid:
        return "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid
    thumbs = item.get("thumbnails") or []
    return thumbs[-1].get("url", "") if thumbs else ""


def _avaliar(item, tokens_busca, minimo, maximo):
    """
    Devolve (nota, motivos_bons, motivo_veto).
    motivo_veto != None  ->  o video foi DESCARTADO e nao vai pra tela.
    """
    titulo = item.get("title") or ""
    canal = item.get("channel") or item.get("uploader") or ""
    desc = item.get("description") or ""
    dur = item.get("duration")
    vistas = item.get("view_count") or 0
    alvo = _limpo(titulo + " | " + canal + " | " + desc)
    alvo_curto = _limpo(titulo + " | " + canal)

    # ---- VETOS (descarte na hora) ----------------------------------------
    if (item.get("live_status") or "") in ("is_live", "is_upcoming", "post_live"):
        return 0, [], "transmissao ao vivo"
    if "/shorts/" in (item.get("url") or ""):
        return 0, [], "shorts/vertical"
    if dur is None:
        return 0, [], "sem duracao (indisponivel)"
    if dur < minimo:
        return 0, [], "curto demais (%ss)" % int(dur)
    if dur > maximo:
        return 0, [], "longo demais (%smin)" % int(dur / 60)
    for rx, motivo in VETO:
        if rx.search(alvo_curto):
            return 0, [], motivo
    canal_limpo = _limpo(canal)
    for ruim in CANAIS_RUINS:
        if ruim in canal_limpo:
            return 0, [], "canal fora do perfil"
    # Audiencia baixa NAO descarta sozinha: clipe de banco de imagem limpo
    # costuma ter poucas visualizacoes justamente por nao ser video de canal.
    # So cai fora o que e claramente upload morto.
    if vistas and vistas < 30:
        return 0, [], "upload sem audiencia"

    # ---- NOTA -------------------------------------------------------------
    nota = 0.0
    bons = []

    # relevancia: quantas palavras da busca aparecem no titulo/canal/descricao
    if tokens_busca:
        no_titulo = sum(1 for t in tokens_busca if t in _limpo(titulo))
        no_resto = sum(1 for t in tokens_busca if t in alvo)
        nota += 100.0 * (no_titulo / len(tokens_busca))   # peso maior no titulo
        nota += 40.0 * (no_resto / len(tokens_busca))
        if no_resto == 0:
            nota -= 45                                    # nao tem nada a ver

    for rx, valor, rotulo in BONUS_PALAVRA:
        if rx.search(alvo):
            nota += valor
            bons.append(rotulo)

    if any(c in canal_limpo for c in CANAIS_BONS):
        nota += 45
        bons.append("canal de arquivo")

    if item.get("channel_is_verified"):
        nota += 8

    # duracao boa pra recortar: nem 40s (pouca margem) nem 3h (video-paisagem)
    if 10 <= dur <= 1500:
        nota += 18
        bons.append("duracao boa")
    elif dur > 3600:
        nota -= 12

    # audiencia pesa um pouco, saturando (video viral nao e melhor b-roll)
    if vistas:
        nota += min(18.0, (vistas ** 0.28) / 4.0)
    if vistas and vistas < 500 and not bons:
        nota -= 12          # pouca gente viu E nenhum sinal de b-roll

    # cara falando pra camera: nao e imagem de apoio, e um video de canal
    if FALANTE.search(alvo_curto):
        nota -= 55
    # marca d'agua / preview de banco pago aparece queimada na imagem
    if MARCA_DAGUA.search(alvo_curto):
        nota -= 40

    # titulo em CAIXA ALTA com muito ponto de exclamacao = clickbait
    if titulo and sum(1 for c in titulo if c.isupper()) > len(titulo) * 0.6:
        nota -= 15
    nota -= 6 * titulo.count("!")

    return nota, bons, None


def _melhor_inicio(duracao):
    """
    Onde comecar o recorte. Comeco de video no YouTube quase sempre e vinheta,
    logo, ou o apresentador dando bom dia - entao entramos DEPOIS disso.
    """
    if duracao <= 0:
        return 10
    if duracao <= 35:
        return 0                       # clipe de banco: ja comeca na imagem
    if duracao < 90:
        return max(2, int(duracao * 0.10))
    return int(min(max(duracao * 0.15, 20), 180))


def buscar(q, num=8, minimo=8, maximo=3600, pool=40):
    """
    Pesquisa no YouTube e devolve so os videos aprovados, ja ordenados.

    q       - frase de busca (a mesma que o buscador ja monta pra imagem)
    num     - quantos videos aprovados devolver
    minimo  - duracao minima do video FONTE em segundos (8: clipe de banco
              de imagem e curto DE PROPOSITO; quem mata Short e a url /shorts/)
    maximo  - duracao maxima do video FONTE. O padrao caiu de 4h pra 1h porque
              video longo e duas vezes ruim aqui: raramente e imagem de apoio
              limpa (e documentario, live, compilado) e baixar um trecho dele
              trava a fila - medido, 176s num video de 11 horas, sem terminar.
    pool    - quantos resultados pedir ao YouTube antes de filtrar (sempre alto:
              e filtrando MUITO candidato que sobra coisa boa)

    Devolve {"videos": [...], "descartados": N, "motivos": {motivo: n}}
    """
    q = (q or "").strip()
    if not q:
        return {"videos": [], "descartados": 0, "motivos": {}}

    pool = max(min(int(pool or 40), 60), 10)
    cod, saida, erro = _rodar(
        ["ytsearch%d:%s" % (pool, q), "--dump-json", "--flat-playlist",
         "--no-warnings", "--ignore-errors", "--no-playlist"],
        timeout=70)
    if cod != 0 and not saida.strip():
        return {"videos": [], "descartados": 0, "motivos": {},
                "erro": (erro or "").strip()[:300] or "yt-dlp nao respondeu"}

    tokens_busca = _tokens(q)
    aprovados, motivos, descartados = [], {}, 0

    for linha in saida.splitlines():
        linha = linha.strip()
        if not linha.startswith("{"):
            continue
        try:
            item = json.loads(linha)
        except Exception:
            continue
        nota, bons, veto = _avaliar(item, tokens_busca, minimo, maximo)
        if veto:
            descartados += 1
            motivos[veto] = motivos.get(veto, 0) + 1
            continue
        dur = int(item.get("duration") or 0)
        aprovados.append({
            "ytId": item.get("id"),
            "videoUrl": item.get("url") or ("https://www.youtube.com/watch?v=%s" % item.get("id")),
            "thumbUrl": _thumb(item),
            "title": item.get("title") or q,
            "channel": item.get("channel") or item.get("uploader") or "",
            "source": "youtube.com",
            "duration": dur,
            "views": int(item.get("view_count") or 0),
            "nota": round(nota, 1),
            "sinais": bons,
            "inicio": _melhor_inicio(dur),
        })

    aprovados.sort(key=lambda v: v["nota"], reverse=True)
    return {"videos": aprovados[:max(int(num or 8), 1)],
            "descartados": descartados, "motivos": motivos}


# ===========================================================================
# DOWNLOAD - so o pedaco, cortado la no servidor do YouTube
# ===========================================================================
def _hhmmss(seg):
    seg = max(int(seg), 0)
    return "%02d:%02d:%02d" % (seg // 3600, (seg % 3600) // 60, seg % 60)


# Sempre mirando 1080p. 4K deixa o download e a montagem pesados a toa; abaixo
# de 720p a imagem estoura quando ocupa a tela inteira.
FORMATO = ("bv*[height=1080][ext=mp4]/"
           "bv*[height=1080]/"
           "b[height=1080]/"
           "bv*[height<=1080][height>=720]/"
           "b[height<=1080][height>=720]/"
           "b[height<=1080]")


def _ffprobe(caminho):
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-show_entries", "format=duration",
             "-of", "json", caminho],
            capture_output=True, timeout=30, **_NOWIN)
        d = json.loads(p.stdout.decode("utf-8", "ignore") or "{}")
        st = (d.get("streams") or [{}])[0]
        return (int(st.get("width") or 0), int(st.get("height") or 0),
                float((d.get("format") or {}).get("duration") or 0))
    except Exception:
        return (0, 0, 0.0)


def _achar_saida(pasta, base):
    for ext in (".mp4", ".mkv", ".webm", ".mov"):
        p = os.path.join(pasta, base + ext)
        if os.path.isfile(p) and os.path.getsize(p) > 20000:
            return p
    return None


def baixar_trecho(video_id, pasta_destino, nome_arquivo, inicio=None,
                  segundos=20, duracao_fonte=0):
    """
    Baixa SO o trecho pedido do video. Nunca o video inteiro.

    Devolve {"ok":bool, "path":..., "width":.., "height":.., "duration":..,
             "estrategia":.., "message":..}
    """
    global _estrategia_ok

    video_id = re.sub(r"[^A-Za-z0-9_\-]", "", str(video_id or ""))
    if len(video_id) < 6:
        return {"ok": False, "message": "id de video invalido"}

    # Video FONTE muito longo e o pior caso: o yt-dlp tem que varrer o fluxo ate
    # o ponto do corte. Um de 11 horas gastou 176s e falhou. Melhor recusar na
    # entrada e explicar do que segurar a fila inteira por um item.
    if duracao_fonte and duracao_fonte > 5400:
        return {"ok": False, "message":
                "video fonte longo demais (%dh%02dmin) - baixar um trecho dele "
                "trava a fila. Escolha outro resultado."
                % (int(duracao_fonte // 3600), int((duracao_fonte % 3600) // 60))}

    segundos = max(min(int(segundos or 20), 90), 4)
    if inicio is None:
        inicio = _melhor_inicio(int(duracao_fonte or 0))
    inicio = max(int(inicio or 0), 0)
    # Clipe de banco de imagem costuma ter 10-20s inteiros: nao adianta pedir
    # 20s de um video de 13s. Encurta o pedido pro que o video tem de verdade
    # (e so entao ajusta o ponto de entrada), pra conferencia de duracao la
    # embaixo comparar com o numero certo.
    if duracao_fonte and duracao_fonte > 0:
        segundos = max(min(segundos, int(duracao_fonte)), 4)
        if inicio + segundos > duracao_fonte:
            inicio = max(int(duracao_fonte - segundos), 0)

    os.makedirs(pasta_destino, exist_ok=True)
    base = re.sub(r"[^\w\-]+", "_", str(nome_arquivo or "youtube"))[:55] or "youtube"
    for ext in (".mp4", ".mkv", ".webm", ".mov"):
        velho = os.path.join(pasta_destino, base + ext)
        if os.path.isfile(velho):
            try:
                os.remove(velho)
            except Exception:
                pass

    secao = "*%s-%s" % (_hhmmss(inicio), _hhmmss(inicio + segundos))
    base_args = [
        "https://www.youtube.com/watch?v=" + video_id,
        "-f", FORMATO,
        "--download-sections", secao,   # <- o corte acontece NO DOWNLOAD
        # NAO usar --force-keyframes-at-cuts aqui. Ele recodifica o trecho pra
        # o corte cair no quadro exato: medido, 11,4s contra 2,7s no mesmo
        # clipe, e o dobro de arquivo. Pra imagem de apoio que fica 5s na tela,
        # cair no keyframe mais proximo e uma diferenca invisivel.
        "--merge-output-format", "mp4",
        "-o", os.path.join(pasta_destino, base + ".%(ext)s"),
        "--no-playlist", "--no-warnings", "--no-part",
        "--retries", "2", "--fragment-retries", "3",
        "--socket-timeout", "15",       # conexao que emudece nao segura a fila
        "-N", "4",
    ] + ARGS_EXTRA

    ultimo_erro = ""
    # No maximo 3 tentativas. Antes a cadeia podia percorrer as 9 estrategias de
    # cookie no mesmo video: com 150s cada, um unico item segurava a fila por
    # mais de 20 minutos, e era isso que dava a sensacao de travado.
    for rotulo, extra in _ordem_tentativas()[:3]:
        cod, saida, erro = _rodar(base_args + extra, timeout=150)
        gerado = _achar_saida(pasta_destino, base)
        if cod == 0 and gerado:
            larg, alt, dur = _ffprobe(gerado)
            if alt and alt < 640:
                os.remove(gerado)
                ultimo_erro = "so existe versao de baixa resolucao (%dp)" % alt
                break
            if dur and dur < segundos * 0.5:
                os.remove(gerado)
                ultimo_erro = "o trecho baixado veio truncado (%.1fs)" % dur
                break
            _estrategia_ok = rotulo
            _bloqueadas.discard(rotulo)
            return {"ok": True, "path": gerado, "width": larg, "height": alt,
                    "duration": round(dur, 2), "estrategia": rotulo,
                    "inicio": inicio, "segundos": segundos}

        if gerado and os.path.isfile(gerado):
            try:
                os.remove(gerado)
            except Exception:
                pass
        bruto = (erro or saida or "").strip()
        ultimo_erro = bruto.splitlines()[-1][:220] if bruto else "falhou"
        if _erro_de_cookie(bruto):
            _sem_cookie_ok.add(rotulo)      # essa fonte de cookie nao serve
            continue
        if _e_bloqueio(bruto):
            _bloqueadas.add(rotulo)         # o YouTube recusou: tenta a proxima
            continue
        # erro que nao e nem um nem outro (video removido, restricao de regiao,
        # idade): trocar de cookie nao resolve, para aqui
        break

    return {"ok": False, "message": ultimo_erro or "nao consegui baixar",
            "bloqueio": _e_bloqueio(ultimo_erro)}


# ===========================================================================
# DIAGNOSTICO - o botao "testar YouTube" da pagina cai aqui
# ===========================================================================
def diagnostico():
    fora = {"ytdlp": "", "busca": False, "download": None, "estrategia": "",
            "cookies_txt": os.path.isfile(COOKIES_TXT),
            "cookie": conferir_cookies(), "detalhe": "",
            "motor_js": (MOTOR[1] if MOTOR else ""),
            "navegadores": [n for n in NAVEGADORES if n not in _sem_cookie_ok]}

    cod, saida, _ = _rodar(["--version"], timeout=30)
    if cod != 0:
        fora["detalhe"] = "yt-dlp nao esta instalado neste Python. Rode: pip install -U yt-dlp"
        return fora
    fora["ytdlp"] = saida.strip().splitlines()[0] if saida.strip() else "?"

    r = buscar("aerial drone city skyline", num=1, pool=12)
    fora["busca"] = bool(r.get("videos"))
    if not fora["busca"]:
        fora["detalhe"] = r.get("erro") or "a busca nao devolveu nada"
        return fora

    alvo = r["videos"][0]
    teste_dir = os.path.join(ROOT, "downloads", "_teste_youtube")
    res = baixar_trecho(alvo["ytId"], teste_dir, "teste", inicio=alvo["inicio"],
                        segundos=5, duracao_fonte=alvo["duration"])
    fora["download"] = bool(res.get("ok"))
    fora["estrategia"] = res.get("estrategia", "")
    if not res.get("ok"):
        fora["detalhe"] = res.get("message", "")
    else:
        try:
            os.remove(res["path"])
            os.rmdir(teste_dir)
        except Exception:
            pass
    return fora


if __name__ == "__main__":
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        pprint.pprint(diagnostico())
    else:
        termo = " ".join(sys.argv[1:]) or "supermercado corredor compras"
        r = buscar(termo, num=8)
        print("descartados:", r["descartados"], r["motivos"])
        for v in r["videos"]:
            print("%6.1f  %5ss  %-26s %s" % (v["nota"], v["duration"],
                                             v["channel"][:26], v["title"][:58]))
