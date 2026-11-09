#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estudio.py - ferramenta unica: escolha MANUAL da midia + sincronia AUTOMATICA.

Substitui, num arquivo so:
    servidor.py + buscador-imagens.html + sincronizar.py + lote_finalizar.py

COMO USAR
---------
    1. Numa pasta, coloque:
           narracao.mp3   (ou qualquer audio: .wav .m4a .aac .ogg .opus .flac)
           legenda.srt    (a legenda dessa narracao)
           roteiro.txt    (OPCIONAL - so pra conferir o texto na tela)

    2. Rode:
           python estudio.py

       Abre sozinho no navegador. Cada CENA ja vem com o tempo exato
       tirado do .srt. Voce so escolhe a imagem/video de cada uma.

    3. Clique em "MONTAR VIDEO". Sai video.mp4 sincronizado ao quadro.

POR QUE FICA 100% SINCRONIZADO
------------------------------
A versao antiga cortava o ROTEIRO por numero de caracteres e depois tentava
readivinhar, com difflib, em que segundo cada pedaco era falado. Quando o
casamento de palavras falhava (idioma diferente, roteiro editado, palavra
comum casando com a ocorrencia errada), a imagem entrava no segundo errado.

Aqui a cena NASCE do proprio .srt: o corte so acontece numa fronteira de
fala que ja tem timestamp. Nao existe adivinhacao nenhuma pra dar errado.
E a duracao vira QUADRO INTEIRO por arredondamento acumulado
(quadros[i] = round(fim*fps) - round(ini*fps)), entao a soma dos clipes
bate exatamente com o audio - sem deriva de milesimo acumulando.

Precisa: Python 3.8+, ffmpeg/ffprobe no PATH.
Opcional: yt-dlp (pip install -U yt-dlp) pra buscar video no YouTube.
"""

import csv
import glob
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA = 8000
RAIZ = os.path.abspath(os.getcwd())
MIDIA = os.path.join(RAIZ, "midia")
CACHE = os.path.join(RAIZ, "_cache")
FPS = 30
LARGURA, ALTURA = 1920, 1080

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif", ".tif", ".tiff")
VID_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi", ".mpeg", ".3gp")
AUDIO_EXT = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


def eh_video(p):
    return os.path.splitext(p)[1].lower() in VID_EXT


def log(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


# ===========================================================================
# CHAVES
# ===========================================================================
def carregar_chaves():
    caminho = os.path.join(RAIZ, "chaves.json")
    if not os.path.exists(caminho):
        return {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            d = json.load(f)
        return {k: str(v or "") for k, v in d.items() if not k.startswith("_")}
    except Exception as e:
        log(" ! chaves.json invalido (%s) - seguindo sem chave." % e)
        return {}


CHAVES = carregar_chaves()


# ===========================================================================
# AUDIO / FFMPEG
# ===========================================================================
def tem(prog):
    return shutil.which(prog) is not None


def duracao_arquivo(caminho):
    """Duracao real em segundos via ffprobe. None se nao der."""
    if not caminho or not os.path.exists(caminho) or not tem("ffprobe"):
        return None
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", caminho],
            capture_output=True, text=True, timeout=30)
        v = float(r.stdout.strip())
        return v if v > 0 else None
    except Exception:
        return None


def achar_audio():
    """Acha a narracao. Ignora de proposito o video.mp4 gerado pela propria
    ferramenta - o script antigo listava .mp4 como audio e ordenava por
    tamanho, entao na segunda execucao ele pegava o PROPRIO video de saida
    como se fosse a narracao."""
    for nome in ("narracao.mp3", "narracao.wav", "narracao.m4a",
                 "audio.mp3", "audio.wav", "audio.m4a"):
        caminho = os.path.join(RAIZ, nome)
        if os.path.isfile(caminho):
            return caminho
    cands = []
    for nome in os.listdir(RAIZ):
        caminho = os.path.join(RAIZ, nome)
        if os.path.isfile(caminho) and nome.lower().endswith(AUDIO_EXT):
            cands.append((os.path.getsize(caminho), caminho))
    if not cands:
        return None
    cands.sort(reverse=True)
    return cands[0][1]


def achar_srt():
    for nome in ("legenda.srt", "legendas.srt", "subtitle.srt"):
        caminho = os.path.join(RAIZ, nome)
        if os.path.isfile(caminho):
            return caminho
    achados = sorted(glob.glob(os.path.join(RAIZ, "*.srt")))
    return achados[0] if achados else None


# ===========================================================================
# SRT -> CENAS  (o coracao da sincronia)
# ===========================================================================
def parse_tempo(s):
    s = s.strip().replace(".", ",")
    partes = s.split(":")
    if len(partes) == 2:
        partes = ["0"] + partes
    if len(partes) != 3:
        raise ValueError("timestamp invalido: %s" % s)
    h, m, resto = partes
    seg, ms = (resto.split(",", 1) + ["0"])[:2] if "," in resto else (resto, "0")
    ms = (ms + "000")[:3]
    return int(h) * 3600 + int(m) * 60 + int(seg) + int(ms) / 1000.0


def ler_srt(caminho):
    """Devolve [(inicio, fim, texto)] limpo, em ordem e sem sobreposicao."""
    with open(caminho, "r", encoding="utf-8-sig", errors="replace") as f:
        bruto = f.read()
    bruto = re.sub(r"\r\n?", "\n", bruto)

    cues = []
    for bloco in re.split(r"\n{2,}", bruto.strip()):
        linhas = [l for l in bloco.split("\n") if l.strip()]
        if not linhas:
            continue
        i = 1 if re.fullmatch(r"\d+", linhas[0].strip()) else 0
        if i >= len(linhas):
            continue
        m = re.search(r"([\d:,.]+)\s*-->\s*([\d:,.]+)", linhas[i])
        if not m:
            continue
        try:
            ini, fim = parse_tempo(m.group(1)), parse_tempo(m.group(2))
        except (ValueError, IndexError):
            continue
        texto = " ".join(linhas[i + 1:])
        texto = re.sub(r"<[^>]+>", "", texto)
        texto = re.sub(r"\{[^}]*\}", "", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        if fim <= ini:
            fim = ini + 0.5
        cues.append((ini, fim, texto))

    cues.sort(key=lambda c: c[0])
    # legenda com sobreposicao: encurta a anterior, senao a fronteira da cena
    # sai invertida e a duracao vira negativa
    for i in range(len(cues) - 1):
        if cues[i][1] > cues[i + 1][0]:
            cues[i] = (cues[i][0], cues[i + 1][0], cues[i][2])
    return [c for c in cues if c[1] > c[0]]


def montar_cenas(cues, fim_total, alvo=6.0):
    """Agrupa as legendas em CENAS de ~alvo segundos, cortando SOMENTE numa
    fronteira de fala (onde a proxima legenda comeca) - ou seja, numa pausa
    real da narracao, que ja vem com timestamp exato do .srt.

    A cena i termina exatamente onde a cena i+1 comeca, e a ultima vai ate o
    fim REAL do audio. A linha do tempo cobre [0, fim_total] sem buraco e sem
    sobreposicao, por construcao."""
    if not cues:
        return []

    cenas = []
    ini = 0.0
    i = 0
    n = len(cues)
    while i < n:
        if cues[i][0] >= fim_total:
            break
        j = i
        while j < n - 1:
            proximo = cues[j + 1][0]
            if proximo >= fim_total or proximo - ini >= alvo:
                break
            j += 1
        fim = min(cues[j + 1][0], fim_total) if j + 1 < n else fim_total
        texto = " ".join(c[2] for c in cues[i:j + 1] if c[2]).strip()
        if fim > ini:
            cenas.append({"ini": ini, "fim": fim, "texto": texto})
            ini = fim
        i = j + 1

    if not cenas:
        return []

    # cauda de silencio depois da ultima legenda entra na ultima cena
    if cenas[-1]["fim"] < fim_total:
        cenas[-1]["fim"] = fim_total

    # ultima cena curtissima e ruim de preencher a mao -> funde com a anterior
    if len(cenas) > 1 and cenas[-1]["fim"] - cenas[-1]["ini"] < 1.0:
        ult = cenas.pop()
        cenas[-1]["fim"] = ult["fim"]
        cenas[-1]["texto"] = (cenas[-1]["texto"] + " " + ult["texto"]).strip()

    # QUADRO INTEIRO por arredondamento acumulado: cada fronteira e
    # arredondada UMA vez e compartilhada pelos dois vizinhos, entao
    # sum(quadros) == round(fim_total*FPS) exato, sem deriva.
    for k, c in enumerate(cenas, 1):
        c["n"] = k
        c["q_ini"] = int(round(c["ini"] * FPS))
        c["q_fim"] = int(round(c["fim"] * FPS))
        c["quadros"] = max(c["q_fim"] - c["q_ini"], 1)
        c["dur"] = c["quadros"] / FPS
    return cenas


def hms(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    return "%02d:%02d:%06.3f" % (h, m, t % 60)


# ===========================================================================
# PROJETO (estado em disco)
# ===========================================================================
class Projeto(object):
    def __init__(self):
        self.recarregar()

    def recarregar(self, alvo=None):
        self.erro = ""
        self.audio = achar_audio()
        self.srt = achar_srt()
        self.roteiro = ""
        caminho_rot = os.path.join(RAIZ, "roteiro.txt")
        if os.path.isfile(caminho_rot):
            with open(caminho_rot, "r", encoding="utf-8-sig", errors="replace") as f:
                self.roteiro = f.read()

        self.alvo = float(alvo) if alvo else self._alvo_salvo()
        self.cenas = []
        self.dur_audio = None
        self.aviso = ""

        if not self.srt:
            self.erro = "Nao achei nenhum arquivo .srt nesta pasta."
            return
        if not self.audio:
            self.erro = "Nao achei o audio da narracao nesta pasta."
            return

        cues = ler_srt(self.srt)
        if not cues:
            self.erro = "O .srt esta vazio ou em formato nao reconhecido."
            return

        self.dur_audio = duracao_arquivo(self.audio)
        fim_srt = cues[-1][1]
        if self.dur_audio is None:
            fim_total = fim_srt
            self.aviso = ("Sem ffprobe nao consegui medir o audio; usei o fim "
                          "do .srt (%s)." % hms(fim_srt))
        elif self.dur_audio < fim_srt - 0.5:
            fim_total = self.dur_audio
            self.aviso = ("O .srt vai ate %s mas o audio so tem %s - o .srt "
                          "parece ser de outra versao da narracao. Cortei no "
                          "fim do audio." % (hms(fim_srt), hms(self.dur_audio)))
        else:
            fim_total = self.dur_audio
            if self.dur_audio > fim_srt + 0.5:
                self.aviso = ("O audio segue %.1fs depois da ultima legenda; a "
                              "ultima cena foi esticada pra cobrir tudo."
                              % (self.dur_audio - fim_srt))

        self.fim_total = fim_total
        self.cenas = montar_cenas(cues, fim_total, self.alvo)
        if not self.cenas:
            self.erro = "Nao consegui montar nenhuma cena a partir do .srt."
            return
        self._aplicar_midia()

    def _alvo_salvo(self):
        caminho = os.path.join(RAIZ, "projeto.json")
        if os.path.isfile(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    return float(json.load(f).get("alvo") or 6.0)
            except Exception:
                pass
        return 6.0

    def _aplicar_midia(self):
        """Liga cada cena ao arquivo midia/NNN.* que ja existe no disco.
        O disco e a fonte da verdade - nada de estado paralelo pra
        dessincronizar."""
        mapa = {}
        if os.path.isdir(MIDIA):
            for nome in os.listdir(MIDIA):
                m = re.match(r"^(\d{3,4})\b", nome)
                caminho = os.path.join(MIDIA, nome)
                if m and os.path.isfile(caminho):
                    ext = os.path.splitext(nome)[1].lower()
                    if ext in IMG_EXT + VID_EXT:
                        mapa[int(m.group(1))] = nome
        for c in self.cenas:
            nome = mapa.get(c["n"])
            c["midia"] = nome
            c["tipo"] = ("video" if nome and eh_video(nome) else
                         "imagem" if nome else "")

    def salvar(self):
        dados = {
            "alvo": self.alvo,
            "audio": self.audio,
            "srt": self.srt,
            "fps": FPS,
            "cenas": [{"n": c["n"], "ini": round(c["ini"], 3),
                       "fim": round(c["fim"], 3), "quadros": c["quadros"],
                       "midia": c.get("midia") or "", "texto": c["texto"]}
                      for c in self.cenas],
        }
        with open(os.path.join(RAIZ, "projeto.json"), "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=1)

    def para_json(self):
        return {
            "ok": not self.erro,
            "erro": self.erro,
            "aviso": self.aviso,
            "alvo": self.alvo,
            "audio": os.path.basename(self.audio) if self.audio else "",
            "srt": os.path.basename(self.srt) if self.srt else "",
            "dur": getattr(self, "fim_total", 0),
            "dur_txt": hms(getattr(self, "fim_total", 0)),
            "fps": FPS,
            # idioma tirado do que e FALADO de verdade (o proprio .srt): um
            # roteiro em ingles tem que buscar em ingles, senao o resultado
            # do YouTube e de outro mundo
            "lang": detectar_idioma(" ".join(c["texto"] for c in self.cenas[:40])),
            "ffmpeg": tem("ffmpeg"),
            "ytdlp": TEM_YTDLP,
            "chaves": {k: bool(v) for k, v in CHAVES.items()},
            "cenas": [{
                "n": c["n"], "ini": round(c["ini"], 3), "fim": round(c["fim"], 3),
                "dur": round(c["dur"], 2), "quadros": c["quadros"],
                "ini_txt": "%d:%05.2f" % (int(c["ini"] // 60), c["ini"] % 60),
                "texto": c["texto"], "midia": c.get("midia") or "",
                "tipo": c.get("tipo") or "",
                "busca": palavras_chave(c["texto"]),
            } for c in self.cenas],
        }


# ---------------------------------------------------------------- palavras --
STOP = set("""
a o e de da do das dos em um uma uns umas que se por para com no na nos nas
ao aos as os pelo pela como mas ou seu sua seus suas ele ela eles elas isso
este esta esse essa aquele aquela foi era sao ser ter tem tinha nao sim mais
menos muito pouco quando onde qual quais entao porque tambem ja ate depois
antes sobre entre sem sob apos cada todo toda todos todas outro outra
the of and to in a is it for on with as at by from that this was were be
are has have had not but or an his her they their you your we our
el la los las un una y de del que en por para con no se es son fue era como
il lo gli le di da in un una che e per con non si sono era come del della
der die das und ist zu den von mit auf als im fur ein eine nicht war sind
le les des du et est en un une que pour avec dans sur par ne pas au aux
""".split())


def palavras_chave(texto, quantas=6):
    """Sugestao de busca tirada do proprio texto falado: prioriza nome
    proprio (maiuscula no meio da frase) e numero, que sao o que realmente
    identifica a cena; o resto entra por tamanho."""
    if not texto:
        return ""
    palavras = re.findall(r"[0-9A-Za-zÀ-ÿ][0-9A-Za-zÀ-ÿ'-]*", texto)
    proprios, comuns = [], []
    for i, p in enumerate(palavras):
        base = p.lower().strip("'-")
        if len(base) < 3 or base in STOP:
            continue
        if (p[0].isupper() and i > 0) or any(ch.isdigit() for ch in p):
            if base not in [x.lower() for x in proprios]:
                proprios.append(p)
        elif base not in comuns:
            comuns.append(base)
    comuns.sort(key=len, reverse=True)
    escolhidas = proprios[:4] + comuns[:max(quantas - len(proprios[:4]), 0)]
    return " ".join(escolhidas[:quantas])


MARCAS = {
    "pt": "o a e de do da dos das em no na um uma que nao não para com por os "
          "as se mais como mas foi ele ela dele dela seu sua isso muito "
          "depois ainda quando porque tambem também voce você entao então",
    "es": "el la los las de en un una que no para con por se mas más como pero "
          "fue su sus cuando porque muy tambien también desde hasta aunque "
          "donde habia había ellos ella esta este",
    "en": "the and of to in a is it for on with as at by from that this was "
          "were be are has have they their when where because about would "
          "could into over after been",
    "it": "il lo la gli le di che e per con non si un una sono era come della "
          "nel nella dal anche quando perche perché questo questa molto dei "
          "delle sul suo",
    "de": "der die das und ist zu den von mit auf als im fur für ein eine "
          "nicht war sind sich auch aber nach uber über wurde werden diese "
          "wenn schon dann noch",
    "fr": "le la les des un une et est dans pour avec qui que plus comme cette "
          "sur mais ses leur nous vous ils elles etait était aussi tres très "
          "ce ces sont ont",
}
# palavra que so existe (na pratica) num idioma vale mais que uma que varios
# compartilham ("que" e pt E es E fr ao mesmo tempo)
EXCLUSIVAS = {}
for _lg, _ws in MARCAS.items():
    for _w in _ws.split():
        EXCLUSIVAS.setdefault(_w, set()).add(_lg)


def detectar_idioma(texto):
    """Idioma do que e FALADO. Conta palavra inteira (nao pedaco de palavra) e
    da peso 3 pra palavra que so aparece num idioma - sem isso o espanhol e o
    frances caiam em portugues, porque 'que'/'la'/'le' sao de todo mundo."""
    palavras = re.findall(r"[a-zà-öø-ÿ]+", (texto or "").lower())
    if not palavras:
        return "pt"
    placar = dict.fromkeys(MARCAS, 0)
    for p in palavras:
        donos = EXCLUSIVAS.get(p)
        if not donos:
            continue
        peso = 3 if len(donos) == 1 else 1
        for lg in donos:
            placar[lg] += peso
    melhor = max(placar, key=placar.get)
    return melhor if placar[melhor] > 0 else "pt"


# ===========================================================================
# BUSCA - todas as fontes
# ===========================================================================
MKT = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "it": "it-IT",
       "de": "de-DE", "fr": "fr-FR"}
REGIAO = {"pt": "br-pt", "en": "us-en", "es": "es-es", "it": "it-it",
          "de": "de-de", "fr": "fr-fr"}

# Banco pago: o preview que Google/Bing/DDG indexam vem SEMPRE com marca
# d'agua atravessada. Nao adianta baixar - e lixo garantido.
BANCOS_PAGOS = (
    "shutterstock", "gettyimages", "istockphoto", "istock.", "alamy",
    "dreamstime", "123rf", "depositphotos", "adobestock", "stock.adobe",
    "bigstockphoto", "canstockphoto", "agefotostock", "photoshelter",
    "vectorstock", "freepik", "lookandlearn", "mauritius-images",
    "picfair", "zumapress", "imago-images", "profimedia", "eyeem",
)


def pago(url, fonte=""):
    alvo = ("%s %s" % (url or "", fonte or "")).lower()
    return any(b in alvo for b in BANCOS_PAGOS)


def http(url, headers=None, timeout=20, dados=None, metodo=None):
    req = urllib.request.Request(url, data=dados,
                                 headers=headers or {"User-Agent": UA},
                                 method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.headers
    except urllib.error.HTTPError as e:
        # o corpo da resposta e onde a API diz o motivo de verdade
        # ("Not enough credits", "invalid api key"...). Sem isso o log so
        # mostrava "HTTP Error 400" e nao dava pra saber o que houve.
        try:
            detalhe = e.read()[:200].decode("utf-8", "ignore").strip()
        except Exception:
            detalhe = ""
        motivo = ""
        if detalhe:
            try:
                motivo = json.loads(detalhe).get("message") or detalhe
            except Exception:
                motivo = detalhe
        raise urllib.error.HTTPError(
            e.url, e.code, "HTTP %s%s" % (e.code, " - " + motivo if motivo else ""),
            e.headers, None)


def http_json(url, headers=None, timeout=20, dados=None, metodo=None):
    bruto, _ = http(url, headers, timeout, dados, metodo)
    return json.loads(bruto.decode("utf-8", "ignore"))


def _lim(n, minimo=3, maximo=30):
    return max(min(int(n), maximo), minimo)


def busca_serper(q, num, lang):
    chave = CHAVES.get("serper")
    if not chave:
        return []
    gl = {"pt": "br", "en": "us", "es": "es", "it": "it",
          "de": "de", "fr": "fr"}.get(lang, "br")
    corpo = json.dumps({"q": q, "num": _lim(num, 10, 40), "hl": lang,
                        "gl": gl}).encode("utf-8")
    d = http_json("https://google.serper.dev/images", timeout=25, dados=corpo,
                  metodo="POST",
                  headers={"X-API-KEY": chave, "Content-Type": "application/json"})
    saida = []
    for it in (d.get("images") or []):
        u = it.get("imageUrl")
        if not u or pago(u, it.get("source", "") + it.get("link", "")):
            continue
        saida.append({"url": u, "thumb": it.get("thumbnailUrl") or u,
                      "titulo": it.get("title", "") or q,
                      "fonte": it.get("source", "") or "google",
                      "w": it.get("imageWidth") or 0,
                      "h": it.get("imageHeight") or 0, "tipo": "imagem"})
    return saida[:num]


def busca_bing(q, num, lang):
    mkt = MKT.get(lang, "pt-BR")
    url = ("https://www.bing.com/images/async?q=%s&first=1&count=%d&mkt=%s"
           "&adlt=moderate" % (urllib.parse.quote(q), max(num * 2, 24), mkt))
    bruto, _ = http(url, {"User-Agent": UA, "Accept-Language": mkt + ",en;q=0.8"})
    corpo = bruto.decode("utf-8", "ignore")
    saida, vistos = [], set()
    for m in re.finditer(r'class="iusc"[^>]*?\sm="([^"]+)"', corpo):
        try:
            meta = json.loads(_html.unescape(m.group(1)))
        except Exception:
            continue
        u = meta.get("murl")
        purl = meta.get("purl") or ""
        if not u or u in vistos or pago(u, purl):
            continue
        vistos.add(u)
        dominio = purl.split("/")[2] if purl.count("/") >= 2 else "bing.com"
        saida.append({"url": u, "thumb": meta.get("turl") or u,
                      "titulo": meta.get("t", "") or q, "fonte": dominio,
                      "w": meta.get("ow") or 0, "h": meta.get("oh") or 0,
                      "tipo": "imagem"})
        if len(saida) >= num:
            break
    return saida


# O i.js do DuckDuckGo passou a devolver 403 pra requisicao "de script".
# Testado de verdade: so volta a responder com (a) cookie da propria visita a
# pagina de busca e (b) os cabecalhos Sec-Fetch-*/sec-ch-ua que um Chrome de
# verdade manda. Sem os dois juntos, 403 sempre - e a versao antiga engolia
# esse erro em silencio, entao o DuckDuckGo parecia "sem resultado".
DDG_EXTRA = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://duckduckgo.com/",
    "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin", "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", '
                 '"Google Chrome";v="122"',
}


def busca_ddg(q, num, lang):
    regiao = REGIAO.get(lang, "br-pt")
    cab = {"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"}
    # opener proprio: guarda o cookie que a pagina de busca entrega e que o
    # i.js exige logo em seguida
    sessao = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())

    def pega(url, cabecalhos):
        req = urllib.request.Request(url, headers=cabecalhos)
        with sessao.open(req, timeout=20) as r:
            return r.read()

    txt = pega("https://duckduckgo.com/?q=%s&iax=images&ia=images"
               % urllib.parse.quote(q), cab).decode("utf-8", "ignore")
    vqd = None
    for pat in (r'vqd="([\d-]+)"', r"vqd=([\d-]+)\&", r'"vqd":"([\d-]+)"'):
        mm = re.search(pat, txt)
        if mm:
            vqd = mm.group(1)
            break
    if not vqd:
        return []
    d = json.loads(pega(
        "https://duckduckgo.com/i.js?l=%s&o=json&q=%s&vqd=%s&f=,,,&p=1"
        % (regiao, urllib.parse.quote(q), vqd),
        dict(cab, **DDG_EXTRA)).decode("utf-8", "ignore"))
    saida = []
    for it in (d.get("results") or []):
        u = it.get("image")
        if not u or pago(u, it.get("source", "") + (it.get("url") or "")):
            continue
        saida.append({"url": u, "thumb": it.get("thumbnail") or u,
                      "titulo": it.get("title", "") or q,
                      "fonte": it.get("source", "") or "duckduckgo",
                      "w": it.get("width") or 0, "h": it.get("height") or 0,
                      "tipo": "imagem"})
        if len(saida) >= num:
            break
    return saida


def busca_openverse(q, num, lang):
    d = http_json("https://api.openverse.org/v1/images/?q=%s&page_size=%d"
                  "&mature=false" % (urllib.parse.quote(q), _lim(num)),
                  {"User-Agent": UA, "Accept": "application/json"})
    return [{"url": it["url"], "thumb": it.get("thumbnail") or it["url"],
             "titulo": it.get("title", "") or q,
             "fonte": it.get("source", "") or "openverse",
             "w": it.get("width") or 0, "h": it.get("height") or 0,
             "tipo": "imagem"}
            for it in (d.get("results") or []) if it.get("url")][:num]


def busca_pexels(q, num, lang):
    chave = CHAVES.get("pexels")
    if not chave:
        return []
    loc = MKT.get(lang, "pt-BR")
    d = http_json("https://api.pexels.com/v1/search?query=%s&per_page=%d"
                  "&locale=%s&orientation=landscape"
                  % (urllib.parse.quote(q), _lim(num, 1), loc),
                  {"User-Agent": UA, "Authorization": chave})
    saida = []
    for it in (d.get("photos") or []):
        src = it.get("src") or {}
        u = (src.get("large2x") or src.get("large") or src.get("original")
             or src.get("medium"))
        if not u:
            continue
        saida.append({"url": u, "thumb": src.get("medium") or u,
                      "titulo": it.get("alt", "") or q, "fonte": "pexels.com",
                      "w": it.get("width") or 0, "h": it.get("height") or 0,
                      "tipo": "imagem"})
    return saida[:num]


def busca_pixabay(q, num, lang):
    chave = CHAVES.get("pixabay")
    if not chave:
        return []
    d = http_json("https://pixabay.com/api/?key=%s&q=%s&per_page=%d"
                  "&image_type=photo&safesearch=true&orientation=horizontal"
                  "&lang=%s" % (urllib.parse.quote(chave),
                                urllib.parse.quote(q), _lim(num), lang),
                  {"User-Agent": UA, "Accept": "application/json"})
    saida = []
    for it in (d.get("hits") or []):
        u = it.get("largeImageURL") or it.get("webformatURL")
        if not u:
            continue
        saida.append({"url": u, "thumb": it.get("previewURL") or u,
                      "titulo": it.get("tags", "") or q, "fonte": "pixabay.com",
                      "w": it.get("imageWidth") or 0,
                      "h": it.get("imageHeight") or 0, "tipo": "imagem"})
    return saida[:num]


def busca_pexels_video(q, num, lang):
    chave = CHAVES.get("pexels")
    if not chave:
        return []
    d = http_json("https://api.pexels.com/videos/search?query=%s&per_page=%d"
                  "&locale=%s&orientation=landscape"
                  % (urllib.parse.quote(q), _lim(num, 1), MKT.get(lang, "pt-BR")),
                  {"User-Agent": UA, "Authorization": chave})
    saida = []
    for it in (d.get("videos") or []):
        arquivos = [a for a in (it.get("video_files") or [])
                    if a.get("link") and (a.get("width") or 0) <= 1920]
        arquivos = arquivos or [a for a in (it.get("video_files") or [])
                                if a.get("link")]
        if not arquivos:
            continue
        melhor = max(arquivos, key=lambda a: a.get("width") or 0)
        fotos = it.get("video_pictures") or []
        saida.append({"url": melhor["link"],
                      "thumb": (fotos[0].get("picture") if fotos else "")
                               or it.get("image") or "",
                      "titulo": (it.get("user") or {}).get("name", "") or q,
                      "fonte": "pexels.com",
                      "w": melhor.get("width") or 0,
                      "h": melhor.get("height") or 0,
                      "dur": it.get("duration") or 0, "tipo": "video"})
    return saida[:num]


def busca_pixabay_video(q, num, lang):
    chave = CHAVES.get("pixabay")
    if not chave:
        return []
    d = http_json("https://pixabay.com/api/videos/?key=%s&q=%s&per_page=%d"
                  "&safesearch=true&lang=%s"
                  % (urllib.parse.quote(chave), urllib.parse.quote(q),
                     _lim(num * 3, 6, 60), lang),
                  {"User-Agent": UA, "Accept": "application/json"})
    saida = []
    for it in (d.get("hits") or []):
        videos = it.get("videos") or {}
        escolhido = next((videos[t] for t in ("large", "medium", "small", "tiny")
                          if videos.get(t, {}).get("url")), None)
        if not escolhido:
            continue
        w, h = escolhido.get("width") or 0, escolhido.get("height") or 0
        if w and h and h > w:          # so paisagem: o video final e 16:9
            continue
        saida.append({"url": escolhido["url"],
                      "thumb": escolhido.get("thumbnail") or "",
                      "titulo": it.get("tags", "") or q, "fonte": "pixabay.com",
                      "w": w, "h": h, "dur": it.get("duration") or 0,
                      "tipo": "video"})
        if len(saida) >= num:
            break
    return saida


# --------------------------------------------------------------- youtube ---
try:
    import yt_dlp
    TEM_YTDLP = True
except ImportError:
    yt_dlp = None
    TEM_YTDLP = False

# Um influenciador cita a marca no titulo e o video nao tem NADA da cena
# (o classico: "Ferrari" que na verdade e um casal posando num parque
# tematico). Medido de verdade com a busca "Ferrari World Abu Dhabi": os
# 8 primeiros resultados crus eram TODOS vlog de influenciador, e nenhum
# deles tinha a palavra "vlog" no titulo - filtrar por termo no titulo, que
# era o que a versao antiga fazia, nao pegava nenhum.
#
# O que funcionou, testado: (a) operador negativo na busca do proprio
# YouTube, incluindo -kids/-family, que sozinho ja trouxe o canal OFICIAL da
# Ferrari pro topo; (b) PONTUAR os candidatos em vez de so excluir, porque a
# marca real de vlog e a primeira pessoa no titulo ("I'M BALD", "JUST CHILL",
# "with Kids", "Fun weekend with Parents"), nao a palavra "vlog".
#
# NAO acrescente "b-roll"/"stock footage" na busca: testado, isso joga a
# relevancia fora (a busca passou a devolver janela de aviao e stock generico
# em vez do assunto). "footage" sozinho, sim, ajuda.
TERMOS_PESSOAIS = (
    "vlog", "reaction", "reagindo", "reacao", "react", "podcast",
    "entrevista", "interview", "unboxing", "haul", "storytime", "q&a",
    "grwm", "day in my life", "meu dia", "rotina", "challenge", "desafio",
    "prank", "pegadinha", "tier list", "asmr", "gameplay", "walkthrough",
    "with kids", "with my", "com meu", "com minha", "minha familia",
    "my family", "our trip", "nossa viagem", "week in", "chill",
)
# primeira pessoa no titulo = quase sempre e sobre QUEM gravou, nao sobre o
# assunto
PRIMEIRA_PESSOA = (
    "i ", "i'm", "im ", "my ", "we ", "our ", "me ", "eu ", "meu ", "minha ",
    "nosso ", "nossa ", "fui ", "fomos ", "yo ", "mi ", "io ", "ich ", "je ",
)
# palavra que aparece em material aproveitavel de verdade
TERMOS_BONS = (
    "footage", "cinematic", "aerial", "drone", "timelapse", "time lapse",
    "off-ride", "off ride", "onride", "on-ride", "pov", "4k", "1080p", "hd",
    "documentary", "documentario", "archive", "arquivo", "promo", "official",
    "oficial", "no copyright", "royalty free", "slow motion", "close up",
    "walkthrough tour", "b roll", "broll",
)
NEGATIVOS = ("-vlog -reaction -podcast -reagindo -unboxing -asmr -gameplay "
             "-shorts -entrevista -kids -family -prank -challenge")


def _yt_tok(t):
    return set(re.findall(r"[a-zà-öø-ÿ0-9]{3,}", (t or "").lower()))


def _yt_bate(q, titulo):
    tq = _yt_tok(q)
    if not tq:
        return True
    comuns = tq & _yt_tok(titulo)
    return len(comuns) >= (1 if len(tq) <= 2 else 2)


def _yt_nota(titulo, canal, dur):
    """Quanto MAIOR, mais provavel de ser material util (e nao vlog).
    So ordena - nunca elimina sozinho, pra a lista nunca ficar vazia."""
    t = " %s " % (titulo or "").lower()
    nota = 0
    for termo in TERMOS_BONS:
        if termo in t:
            nota += 6
    for termo in TERMOS_PESSOAIS:
        if termo in t:
            nota -= 14
    for p in PRIMEIRA_PESSOA:
        if t.startswith(" " + p) or (" " + p) in t:
            nota -= 8
            break
    palavras = re.findall(r"[A-Za-zÀ-ÿ]{3,}", titulo or "")
    caps = sum(1 for p in palavras if p.isupper())
    if palavras and caps / len(palavras) > 0.5:
        nota -= 10                      # TITULO GRITADO = vlog
    nota -= 3 * min(titulo.count("!"), 3)
    if re.search(r"[🌀-🫿☀-➿]", titulo or ""):
        nota -= 5                       # emoji no titulo
    if 45 <= dur <= 900:
        nota += 5                       # duracao de material, nao de vlog
    elif dur > 1800:
        nota -= 6
    if re.search(r"(official|oficial|museum|museu|archiv|institut|"
                 r"magazine|news|tv|media)", (canal or "").lower()):
        nota += 7
    return nota


def _yt_opcoes():
    # NAO fixe "player_client" aqui. Medido de verdade neste yt-dlp
    # (2026.08.19), no mesmo video: a lista que o pipeline antigo carregava
    # ("tv_simply","web_embedded","android","ios") so enxergava ate 360p,
    # enquanto o padrao do proprio yt-dlp enxergava ate 2160p:
    #     tv_simply,web_embedded,android,ios -> [27, 45, 90, 180, 360]
    #     padrao do yt-dlp                   -> [..., 720, 1080, 1440, 2160]
    # Aquela lista resolvia uma degradacao real de 2025, mas hoje e ela que
    # causa a degradacao: o yt-dlp ja acompanha o que o YouTube muda, entao
    # o certo e deixar ele escolher.
    op = {
        "retries": 3, "fragment_retries": 3, "socket_timeout": 20,
        "quiet": True, "no_warnings": True, "noplaylist": True,
        "ignoreerrors": True,
        # pausa entre pedidos: sem isso o YouTube bloqueia por volume
        "sleep_interval_requests": 1,
        "sleep_interval": 5, "max_sleep_interval": 15,
    }
    # cookies.txt (sessao logada, so youtube.com) evita o "prove que nao e robo"
    cookies = os.path.join(RAIZ, "cookies.txt")
    if os.path.isfile(cookies):
        op["cookiefile"] = cookies
    return op


def busca_youtube(q, num, lang):
    if not TEM_YTDLP:
        return []
    for consulta in ("%s %s" % (q, NEGATIVOS), q):
        # os negativos as vezes zeram a busca inteira -> repete sem eles
        op = dict(_yt_opcoes())
        op["extract_flat"] = True
        try:
            with yt_dlp.YoutubeDL(op) as ydl:
                info = ydl.extract_info(
                    "ytsearch%d:%s" % (max(num * 3, 24), consulta),
                    download=False)
        except Exception:
            continue

        crus = []
        for it in ((info or {}).get("entries") or []):
            if not it or not it.get("id"):
                continue
            titulo = it.get("title") or ""
            dur = it.get("duration") or 0
            canal = it.get("channel") or it.get("uploader") or "youtube"
            if not _yt_bate(q, titulo):
                continue
            if dur and dur > 3600:   # compilacao de horas: sortear trecho e loteria
                continue
            if dur and dur < 12:     # short: nao sobra margem pro corte
                continue
            crus.append((_yt_nota(titulo, canal, dur), it["id"], titulo, canal, dur))

        if not crus:
            continue
        crus.sort(key=lambda x: -x[0])
        return [{"url": "https://www.youtube.com/watch?v=" + vid, "yt": vid,
                 "thumb": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % vid,
                 "titulo": titulo, "fonte": canal, "nota": nota,
                 "w": 0, "h": 0, "dur": dur, "tipo": "youtube"}
                for nota, vid, titulo, canal, dur in crus[:num]]
    return []


FONTES = {
    "google": busca_serper, "bing": busca_bing, "ddg": busca_ddg,
    "openverse": busca_openverse, "pexels": busca_pexels,
    "pixabay": busca_pixabay, "pexels_video": busca_pexels_video,
    "pixabay_video": busca_pixabay_video, "youtube": busca_youtube,
}


def buscar(fontes, q, num, lang):
    """Roda as fontes em paralelo e junta, sem repetir URL."""
    resultados = {}
    threads = []

    def tarefa(nome):
        try:
            resultados[nome] = FONTES[nome](q, num, lang) or []
        except Exception as e:
            resultados[nome] = []
            log("   ! %s: %s" % (nome, e))

    for nome in fontes:
        if nome not in FONTES:
            continue
        t = threading.Thread(target=tarefa, args=(nome,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=35)

    saida, vistos = [], set()
    # intercala as fontes: a primeira tela ja mostra variedade em vez de
    # 20 resultados seguidos da mesma fonte
    listas = [resultados.get(n) or [] for n in fontes if n in FONTES]
    for i in range(max((len(l) for l in listas), default=0)):
        for l in listas:
            if i < len(l):
                item = l[i]
                if item["url"] in vistos:
                    continue
                vistos.add(item["url"])
                saida.append(item)
    return saida


# ===========================================================================
# SALVAR MIDIA
# ===========================================================================
EXT_POR_TIPO = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/pjpeg": ".jpg",
    "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif",
    "image/avif": ".avif", "image/bmp": ".bmp", "image/tiff": ".tif",
    "video/mp4": ".mp4", "video/webm": ".webm", "video/quicktime": ".mov",
    "video/x-matroska": ".mkv", "video/mpeg": ".mpeg",
}


def limpar_cena(n):
    """Apaga a midia da cena e o clipe em cache dela."""
    for padrao in (os.path.join(MIDIA, "%03d.*" % n),
                   os.path.join(CACHE, "%03d.*" % n)):
        for caminho in glob.glob(padrao):
            try:
                os.remove(caminho)
            except OSError:
                pass


def baixar_midia(url, timeout=None):
    p = urllib.parse.urlparse(url)
    ext_url = os.path.splitext(p.path)[1].lower()
    provavel_video = ext_url in VID_EXT
    cab = {
        "User-Agent": UA,
        "Accept": ("video/mp4,video/webm,video/*,image/avif,image/webp,"
                   "image/apng,image/*,*/*;q=0.8"),
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "%s://%s/" % (p.scheme, p.netloc),
    }
    dados, cabecalhos = http(url, cab,
                             timeout or (120 if provavel_video else 25))
    ctype = (cabecalhos.get("Content-Type") or "").split(";")[0].strip().lower()
    cabeca = dados[:32].lstrip().lower()
    if ctype.startswith("text/") or cabeca.startswith(b"<!doctype") or \
            cabeca.startswith(b"<html"):
        raise ValueError("o link nao entrega o arquivo direto (pagina protegida)")
    minimo = 4000 if (ctype.startswith("video/") or provavel_video) else 400
    if len(dados) < minimo:
        raise ValueError("arquivo vazio ou pequeno demais (%d bytes)" % len(dados))

    ext = EXT_POR_TIPO.get(ctype) or (ext_url if ext_url in IMG_EXT + VID_EXT
                                      else ".jpg")
    return dados, ext


def salvar_cena(n, url, tipo, yt_id="", dur_alvo=7.0, query=""):
    """Baixa e grava midia/NNN.ext. Sempre substitui o que estava la."""
    os.makedirs(MIDIA, exist_ok=True)
    limpar_cena(n)

    if tipo == "youtube":
        destino = baixar_youtube(yt_id, n, dur_alvo, query)
    else:
        dados, ext = baixar_midia(url)
        destino = os.path.join(MIDIA, "%03d%s" % (n, ext))
        with open(destino, "wb") as f:
            f.write(dados)

    ok, motivo = validar(destino)
    if not ok:
        try:
            os.remove(destino)
        except OSError:
            pass
        raise ValueError(motivo)
    return os.path.basename(destino)


def baixar_youtube(vid, n, dur_alvo, query):
    if not TEM_YTDLP:
        raise ValueError("yt-dlp nao instalado (pip install -U yt-dlp)")

    op = dict(_yt_opcoes())
    op["ignoreerrors"] = False
    try:
        with yt_dlp.YoutubeDL(op) as ydl:
            info = ydl.extract_info("https://www.youtube.com/watch?v=%s" % vid,
                                    download=False) or {}
    except Exception as e:
        raise ValueError("nao consegui ler o video: %s" % e)

    # Aqui NAO existe bloqueio por categoria de proposito. A ferramenta
    # automatica antiga recusava "Travel & Events"/"Entertainment" porque
    # ninguem olhava o conteudo. Testado de verdade: o melhor material de
    # "Ferrari World Abu Dhabi" (on-ride 4K POV, canal CoasterForce) e
    # categoria "Travel & Events" - o bloqueio recusava exatamente o video
    # certo. Neste modo VOCE ja viu a miniatura e o titulo e clicou: recusar
    # a sua escolha seria so atrapalhar.
    dur_video = info.get("duration") or 0
    fatia = max(float(dur_alvo or 7), 2.0) + 2.0

    # capitulo que bate com a busca > sortear trecho no escuro
    inicio = None
    for cap in (info.get("chapters") or []):
        if _yt_bate(query, cap.get("title", "")) and cap.get("start_time") is not None:
            inicio = float(cap["start_time"])
            break
    if inicio is None:
        if dur_video > fatia + 10:
            # comeca depois da vinheta e para antes dos creditos
            inicio = min(max(dur_video * 0.20, 5.0), dur_video - fatia - 1)
        else:
            inicio = 0.0
    inicio = max(0.0, min(inicio, max(dur_video - fatia, 0.0)))
    fim = inicio + fatia

    base = os.path.join(MIDIA, "%03d" % n)
    op = dict(_yt_opcoes())
    op["ignoreerrors"] = False
    op.update({
        # Preferir protocolo m3u8 NAO e preciosismo - foi medido no mesmo
        # video e no mesmo minuto: os formatos "https" do YouTube vem
        # estrangulados (2,2 KiB/s -> 68s pra buscar um trecho de 9s, e ainda
        # assim caiu pra 360p), enquanto os m3u8 do MESMO video baixaram a
        # 371 KiB/s -> 1920x1080 em 9s. Mesma qualidade pedida, 7x mais
        # rapido e na resolucao certa.
        "format": ("best[height=1080][protocol^=m3u8]/"
                   "bestvideo[height=1080][protocol^=m3u8]+ba/"
                   "best[height<=1080][height>=720][protocol^=m3u8]/"
                   "bestvideo[height<=1080][height>=720][protocol^=m3u8]+ba/"
                   "bv*[height<=1080][height>=720]+ba/"
                   "best[height<=1080][height>=480]/"
                   "bv*[height<=1080][height>=480]+ba/"
                   "bv*[height<=1080]+ba/best[height<=1080]/best"),
        "concurrent_fragment_downloads": 4,
        "outtmpl": base + ".%(ext)s",
        "download_ranges": yt_dlp.utils.download_range_func(None, [(inicio, fim)]),
        "force_keyframes_at_cuts": True,
        "merge_output_format": "mp4",
    })
    try:
        with yt_dlp.YoutubeDL(op) as ydl:
            ydl.download(["https://www.youtube.com/watch?v=%s" % vid])
    except Exception as e:
        if "sign in" in str(e).lower():
            raise ValueError("YouTube bloqueou (deteccao de robo) - tente de "
                             "novo em alguns minutos")
        raise ValueError("falha no download: %s" % e)

    achados = sorted(glob.glob(base + ".*"))
    if not achados:
        raise ValueError("o download nao gerou arquivo")
    destino = achados[0]

    # de vez em quando o yt-dlp ignora o corte e baixa o video INTEIRO sem
    # erro nenhum. Isso passaria batido e entupiria a cena com minutos de
    # material - pega aqui em vez de descobrir na montagem.
    real = duracao_arquivo(destino)
    if real and real > fatia * 3 + 10:
        os.remove(destino)
        raise ValueError("o corte falhou (baixou %.0fs em vez de ~%.0fs) - "
                         "tente de novo" % (real, fatia))
    return destino


ASSINATURAS = ((b"\xff\xd8\xff", "jpg"), (b"\x89PNG\r\n\x1a\n", "png"),
               (b"GIF87a", "gif"), (b"GIF89a", "gif"), (b"BM", "bmp"),
               (b"II*\x00", "tiff"), (b"MM\x00*", "tiff"))


def validar(caminho):
    """(ok, motivo). Pega arquivo vazio, truncado, HTML disfarcado e
    imagem que nao decodifica."""
    try:
        tam = os.path.getsize(caminho)
    except OSError:
        return False, "nao consegui ler o arquivo"
    if tam < (4096 if eh_video(caminho) else 1024):
        return False, "download incompleto (%d bytes)" % tam

    with open(caminho, "rb") as f:
        cabeca = f.read(16)
        f.seek(-2, os.SEEK_END)
        cauda = f.read(2)

    if cabeca.lstrip()[:1] == b"<":
        return False, "e uma pagina HTML, nao midia"

    if not eh_video(caminho):
        tipo = next((n for a, n in ASSINATURAS if cabeca.startswith(a)), None)
        if tipo is None:
            if cabeca[:4] == b"RIFF" and cabeca[8:12] == b"WEBP":
                tipo = "webp"
            elif b"ftyp" in cabeca:
                tipo = "avif"
            else:
                return False, "formato irreconhecivel - arquivo corrompido"
        if tipo == "jpg" and cauda != b"\xff\xd9":
            return False, "JPEG truncado - download interrompido"

    if tem("ffmpeg"):
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho,
                            "-frames:v", "1", "-f", "null", "-"],
                           capture_output=True)
        if r.returncode != 0:
            return False, "o ffmpeg nao abre esse arquivo (danificado)"
    return True, ""


# ===========================================================================
# MONTAGEM - quadro exato
# ===========================================================================
ESTADO = {"rodando": False, "feito": 0, "total": 0, "etapa": "",
          "erro": "", "saida": "", "avisos": []}


def _vf_base():
    return ("scale=%d:%d:force_original_aspect_ratio=increase,"
            "crop=%d:%d,fps=%d,format=yuv420p"
            % (LARGURA, ALTURA, LARGURA, ALTURA, FPS))


# "loop=loop=-1:size=1" (filtro) em vez de "-loop 1" (opcao do demuxer
# image2): testado, "-loop 1" simplesmente RECUSA abrir um .avif ("Option
# loop not found") e a cena inteira ia pro video como tela preta; e
# "-stream_loop -1", que resolve o avif, TRAVA pra sempre num .jpg. O filtro
# loop e o unico caminho que funciona igual em jpg, png, webp e avif - e
# ainda deixa um codigo so pra todo tipo de imagem.
LOOP_IMG = "loop=loop=-1:size=1:start=0"


def _vf_vivo(semente):
    """Zoom lento + deslize (Ken Burns) pra imagem parada nao ficar morta na
    tela. O lado do deslize varia por cena (derivado do numero dela) pra nao
    andar tudo pro mesmo lado o video inteiro."""
    deriva = 1 if semente % 2 == 0 else -1
    return ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,%s,"
            "zoompan=z='min(zoom+0.0012,1.14)':"
            "x='iw/2-(iw/zoom/2)+%d*min(0.10*on,70)':"
            "y='ih/2-(ih/zoom/2)':d=1:s=%dx%d:fps=%d,format=yuv420p"
            % (LARGURA * 2, ALTURA * 2, LARGURA * 2, ALTURA * 2, LOOP_IMG,
               deriva, LARGURA, ALTURA, FPS))


# profile/level FIXOS de proposito: a juncao final e feita com "-c:v copy"
# (colar, sem recodificar) e isso so e valido se TODO clipe tiver exatamente
# os mesmos parametros de fluxo. Deixar o x264 escolher o level por clipe
# abriria a chance de dois clipes ficarem incompativeis e o video sair com
# um trecho corrompido no meio.
# "-color_range tv" e os tres metadados de cor NAO sao firula: sem eles, a
# mesma linha de comando gerava clipe "yuv420p" a partir de um .mp4 e
# "yuvj420p" (faixa cheia, de JPEG) a partir de uma foto. Colados com
# "-c copy", os dois convivem no mesmo arquivo e a imagem SALTA de brilho na
# troca de cena. Fixando aqui, todo clipe sai identico.
X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-color_range", "tv",
        "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-profile:v", "high", "-level", "4.1",
        "-g", str(FPS), "-video_track_timescale", str(FPS * 1000)]


def render_clipe(fonte, quadros, destino, vivo=False, semente=0):
    """UM clipe com EXATAMENTE 'quadros' quadros.

    Usa -frames:v (contagem exata) e nao -t (duracao aproximada, que e o que
    a versao antiga fazia): com -t, cada clipe podia sair com 1 quadro a
    mais ou a menos e o erro ia se somando ate a imagem atrasar visivelmente
    no fim de um video longo."""
    comum = ["ffmpeg", "-y", "-nostdin", "-loglevel", "error"]
    if fonte is None:
        entrada = ["-f", "lavfi", "-i",
                   "color=c=black:s=%dx%d:r=%d" % (LARGURA, ALTURA, FPS)]
        vf = "format=yuv420p"
    elif eh_video(fonte):
        # -stream_loop -1 + -frames:v: video curto repete ate encher a cena,
        # sem precisar saber a duracao real dele antes
        entrada = ["-stream_loop", "-1", "-i", fonte]
        vf = _vf_base()
    else:
        entrada = ["-i", fonte]
        vf = (_vf_vivo(semente) if vivo else
              ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
               "%s,fps=%d,format=yuv420p"
               % (LARGURA, ALTURA, LARGURA, ALTURA, LOOP_IMG, FPS)))

    cmd = comum + entrada + ["-frames:v", str(quadros), "-vf", vf, "-an"] \
        + X264 + [destino]
    r = subprocess.run(cmd, capture_output=True, timeout=900)
    if r.returncode != 0:
        return False, r.stderr.decode("utf-8", "ignore")[-400:].strip()
    return True, ""


def _assinatura(fonte, quadros, vivo):
    """Chave de cache: so re-renderiza o que mudou de verdade."""
    if fonte is None:
        return "preto|%d" % quadros
    st = os.stat(fonte)
    return "%s|%d|%d|%d|%d" % (os.path.basename(fonte), st.st_size,
                               int(st.st_mtime), quadros, int(vivo))


def montar(proj, vivo=False, saida="video.mp4"):
    """Renderiza cada cena com a contagem exata de quadros e junta tudo com
    a narracao. Devolve (ok, mensagem)."""
    if not tem("ffmpeg"):
        return False, "ffmpeg nao esta no PATH."
    if proj.erro:
        return False, proj.erro
    if not proj.cenas:
        return False, "nenhuma cena."

    os.makedirs(CACHE, exist_ok=True)
    ESTADO.update(rodando=True, feito=0, total=len(proj.cenas) + 1,
                  etapa="preparando", erro="", saida="", avisos=[])

    avisos = []
    herdadas = []
    ultima_fonte = None
    plano = []
    for c in proj.cenas:
        fonte = os.path.join(MIDIA, c["midia"]) if c.get("midia") else None
        if fonte and not os.path.isfile(fonte):
            fonte = None
        if fonte is None:
            # cena vazia nao pode sumir da linha do tempo, senao tudo depois
            # dela anda pra tras. Ela mantem o tempo dela e repete a ultima
            # midia disponivel (ou fica preta, se for antes da primeira).
            fonte = ultima_fonte
            herdadas.append(c["n"])
        else:
            ultima_fonte = fonte
        plano.append((c, fonte))

    lista = []
    for i, (c, fonte) in enumerate(plano, 1):
        destino = os.path.join(CACHE, "%03d.mp4" % c["n"])
        chave_arq = os.path.join(CACHE, "%03d.key" % c["n"])
        assinatura = _assinatura(fonte, c["quadros"], vivo)

        atual = ""
        if os.path.isfile(chave_arq):
            with open(chave_arq, "r", encoding="utf-8") as f:
                atual = f.read().strip()

        precisa = not (atual == assinatura and os.path.isfile(destino)
                       and os.path.getsize(destino) > 1024)
        ESTADO.update(feito=i - 1,
                      etapa="cena %d/%d%s" % (i, len(plano),
                                              "" if precisa else " (cache)"))
        if precisa:
            ok, msg = render_clipe(fonte, c["quadros"], destino, vivo, c["n"])
            if not ok:
                # sem o clipe, o tempo da cena sumiria -> poe preto no lugar,
                # que mantem a sincronia de tudo que vem depois
                avisos.append("cena %d: %s (entrou preta)" % (c["n"], msg))
                ok2, _ = render_clipe(None, c["quadros"], destino)
                if not ok2:
                    ESTADO.update(rodando=False, erro="falha ao gerar a cena %d"
                                  % c["n"])
                    return False, "falha ao gerar a cena %d" % c["n"]
                # a chave NAO pode ser a da midia real: senao o cache passaria
                # a achar que a tela preta e o render bom dessa midia e nunca
                # mais tentaria de novo, nem depois de voce trocar o arquivo
                assinatura = "falhou|" + assinatura
            with open(chave_arq, "w", encoding="utf-8") as f:
                f.write(assinatura)
        lista.append(destino)

    # limpa clipes de cenas que nao existem mais (roteiro/alvo mudou)
    validos = {"%03d.mp4" % c["n"] for c in proj.cenas} | \
              {"%03d.key" % c["n"] for c in proj.cenas}
    for nome in os.listdir(CACHE):
        if nome not in validos:
            try:
                os.remove(os.path.join(CACHE, nome))
            except OSError:
                pass

    ESTADO.update(feito=len(plano), etapa="juntando com a narracao")
    lista_txt = os.path.join(CACHE, "lista.txt")
    with open(lista_txt, "w", encoding="utf-8") as f:
        for caminho in lista:
            f.write("file '%s'\n" % caminho.replace("'", "'\\''"))

    caminho_saida = os.path.join(RAIZ, saida)
    cmd = ["ffmpeg", "-y", "-nostdin", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", lista_txt]
    if proj.audio:
        cmd += ["-i", proj.audio]
    # -c:v copy: os clipes ja sairam todos com o mesmo codec/tamanho/fps,
    # entao juntar e so colar - sem recodificar e sem perder qualidade
    cmd += ["-c:v", "copy", "-map", "0:v:0"]
    if proj.audio:
        cmd += ["-map", "1:a:0", "-c:a", "aac", "-b:a", "192k"]
    # -t com a duracao EXATA do video montado, em vez de -shortest: medido de
    # verdade, o -shortest parava no ultimo pacote de audio e comia os
    # ultimos quadros do video (o final ficava sem imagem). Com -t, o video
    # sai inteiro e o audio e que e cortado no fim, se sobrar.
    cmd += ["-t", "%.6f" % (sum(c["quadros"] for c in proj.cenas) / float(FPS)),
            "-movflags", "+faststart", caminho_saida]

    r = subprocess.run(cmd, capture_output=True, timeout=3600)
    if r.returncode != 0:
        erro = r.stderr.decode("utf-8", "ignore")[-600:].strip()
        ESTADO.update(rodando=False, erro=erro)
        return False, erro

    exportar(proj, plano, vivo)

    quadros_total = sum(c["quadros"] for c in proj.cenas)
    dur_video = duracao_arquivo(caminho_saida)
    conferencia = ""
    if dur_video and proj.dur_audio:
        conferencia = ("video %.3fs / audio %.3fs / diferenca %+.3fs"
                       % (dur_video, proj.dur_audio, dur_video - proj.dur_audio))
    if herdadas:
        avisos.insert(0, "%d cena(s) sem midia repetiram a anterior: %s"
                      % (len(herdadas), ", ".join(map(str, herdadas[:25]))
                         + (" ..." if len(herdadas) > 25 else "")))

    ESTADO.update(rodando=False, feito=ESTADO["total"], etapa="pronto",
                  saida=caminho_saida, avisos=avisos)
    return True, ("%s  |  %d cenas, %d quadros (%.3fs)  |  %s"
                  % (caminho_saida, len(proj.cenas), quadros_total,
                     quadros_total / FPS, conferencia))


def exportar(proj, plano, vivo):
    """Grava os arquivos que o resto do mundo le: linha_do_tempo.json (o
    projeto_capcut.py monta o projeto do CapCut direto dele), mapa.csv pra
    conferir a olho e concat.txt pro ffmpeg na mao."""
    itens, us = [], 0
    for c, fonte in plano:
        dur_us = int(round(c["quadros"] / FPS * 1000000))
        itens.append({"arquivo": os.path.join(CACHE, "%03d.mp4" % c["n"]),
                      "original": fonte or "",
                      "paragrafo": c["n"], "inicio_us": us,
                      "duracao_us": dur_us})
        us += dur_us

    with open(os.path.join(RAIZ, "linha_do_tempo.json"), "w",
              encoding="utf-8") as f:
        json.dump({"fps": FPS, "largura": LARGURA, "altura": ALTURA,
                   "audio": proj.audio, "srt": proj.srt,
                   "duracao_total_us": us, "vivo": vivo, "itens": itens},
                  f, ensure_ascii=False, indent=1)

    with open(os.path.join(RAIZ, "mapa.csv"), "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["cena", "inicio", "fim", "duracao_s", "quadros",
                    "midia", "texto"])
        for c, fonte in plano:
            w.writerow([c["n"], hms(c["ini"]), hms(c["fim"]),
                        round(c["quadros"] / FPS, 3), c["quadros"],
                        os.path.basename(fonte) if fonte else "(preto)",
                        c["texto"][:120]])

    with open(os.path.join(RAIZ, "concat.txt"), "w", encoding="utf-8") as f:
        for c, _ in plano:
            f.write("file '%s'\n"
                    % os.path.join(CACHE, "%03d.mp4" % c["n"]).replace("'", "'\\''"))

    proj.salvar()


# ===========================================================================
# INTERFACE (a pagina inteira vive aqui - nada de arquivo .html solto)
# ===========================================================================
PAGINA = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estudio</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0e1014;--pn:#171a21;--pn2:#1e222b;--ln:#2b3040;--tx:#e6e9ef;
--dim:#8b93a7;--ac:#4d9fff;--ok:#39c17f;--er:#ff5f56;--wr:#ffb454}
body{background:var(--bg);color:var(--tx);font:14px/1.45 system-ui,"Segoe UI",sans-serif;
height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:var(--pn);border-bottom:1px solid var(--ln);padding:8px 14px;
display:flex;gap:12px;align-items:center;flex-wrap:wrap;flex:0 0 auto}
h1{font-size:15px;font-weight:700;letter-spacing:.5px}
h1 span{color:var(--ac)}
.meta{color:var(--dim);font-size:12px}
.meta b{color:var(--tx);font-weight:600}
button{background:var(--pn2);color:var(--tx);border:1px solid var(--ln);
border-radius:6px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}
button:hover:not(:disabled){border-color:var(--ac)}
button:disabled{opacity:.4;cursor:default}
button.p{background:var(--ac);border-color:var(--ac);color:#06121f;font-weight:600}
input,select{background:var(--pn2);color:var(--tx);border:1px solid var(--ln);
border-radius:6px;padding:6px 10px;font:inherit;font-size:13px}
input:focus,select:focus{outline:0;border-color:var(--ac)}
main{flex:1;display:flex;min-height:0}
#lista{width:37%;min-width:330px;border-right:1px solid var(--ln);overflow-y:auto;
background:var(--pn)}
.cena{display:flex;gap:9px;padding:7px 10px;border-bottom:1px solid #21252f;
cursor:pointer;align-items:flex-start}
.cena:hover{background:#1c2029}
.cena.sel{background:#123055;box-shadow:inset 3px 0 0 var(--ac)}
.cena .th{width:76px;height:44px;flex:0 0 auto;border-radius:4px;background:#0a0c10;
border:1px solid var(--ln);object-fit:cover;display:flex;align-items:center;
justify-content:center;color:#485068;font-size:19px}
.cena.ok .th{border-color:var(--ok)}
.cena .info{min-width:0;flex:1}
.cena .top{display:flex;gap:7px;font-size:11px;color:var(--dim);margin-bottom:2px}
.cena .num{color:var(--ac);font-weight:700}
.cena .tx{font-size:12px;color:#c3cad8;display:-webkit-box;-webkit-line-clamp:2;
-webkit-box-orient:vertical;overflow:hidden}
.tag{font-size:10px;padding:0 5px;border-radius:3px;background:#2a3142;color:var(--dim)}
.tag.v{background:#3a2a12;color:var(--wr)}
#dir{flex:1;display:flex;flex-direction:column;min-width:0}
#barra{padding:9px 12px;border-bottom:1px solid var(--ln);display:flex;gap:8px;
flex-wrap:wrap;align-items:center;background:var(--pn)}
#q{flex:1;min-width:200px}
.fontes{display:flex;gap:4px;flex-wrap:wrap;padding:0 12px 8px;background:var(--pn);
border-bottom:1px solid var(--ln)}
.f{font-size:11px;padding:3px 9px;border-radius:11px;border:1px solid var(--ln);
cursor:pointer;color:var(--dim);user-select:none}
.f.on{background:var(--ac);border-color:var(--ac);color:#06121f;font-weight:600}
.f.off{opacity:.35;cursor:not-allowed}
#grade{flex:1;overflow-y:auto;padding:10px;display:grid;
grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:9px;align-content:start}
.r{background:var(--pn);border:1px solid var(--ln);border-radius:7px;overflow:hidden;
cursor:pointer;position:relative}
.r:hover{border-color:var(--ac)}
.r img{width:100%;height:118px;object-fit:cover;display:block;background:#0a0c10}
.r .cap{padding:4px 6px;font-size:10px;color:var(--dim);white-space:nowrap;
overflow:hidden;text-overflow:ellipsis}
.r .k{position:absolute;top:5px;left:5px;background:#000b;border-radius:4px;
padding:1px 6px;font-size:11px;font-weight:700}
.r .b{position:absolute;top:5px;right:5px;background:#000b;border-radius:4px;
padding:1px 6px;font-size:10px;color:var(--wr)}
.r.salvando{opacity:.4}
.r.falhou{border-color:var(--er)}
#rodape{padding:6px 14px;border-top:1px solid var(--ln);background:var(--pn);
font-size:12px;color:var(--dim);display:flex;gap:14px;align-items:center;flex:0 0 auto}
#prog{flex:1;height:5px;background:var(--pn2);border-radius:3px;overflow:hidden;display:none}
#prog i{display:block;height:100%;background:var(--ac);width:0;transition:width .3s}
.vazio{color:var(--dim);padding:30px;text-align:center;grid-column:1/-1}
#aviso{background:#3a2a12;color:var(--wr);padding:6px 14px;font-size:12px;flex:0 0 auto}
kbd{background:var(--pn2);border:1px solid var(--ln);border-radius:3px;padding:0 4px;
font-size:11px;font-family:inherit}
</style></head><body>

<header>
  <h1>ESTUDIO<span>.</span></h1>
  <span class="meta" id="cab">carregando...</span>
  <span style="flex:1"></span>
  <label class="meta">cena ~<input id="alvo" type="number" min="2" max="20" step="0.5"
    value="6" style="width:62px"> s</label>
  <button id="brec">Recalcular</button>
  <label class="meta"><input id="vivo" type="checkbox"> zoom nas fotos</label>
  <button id="bmontar" class="p">MONTAR VIDEO</button>
</header>
<div id="aviso" style="display:none"></div>

<main>
  <div id="lista"></div>
  <div id="dir">
    <div id="barra">
      <input id="q" placeholder="o que procurar nesta cena">
      <select id="lang">
        <option value="pt">PT</option><option value="en">EN</option>
        <option value="es">ES</option><option value="it">IT</option>
        <option value="de">DE</option><option value="fr">FR</option>
      </select>
      <button id="bbuscar" class="p">Buscar</button>
      <button id="blimpar">Tirar midia</button>
    </div>
    <div class="fontes" id="fontes"></div>
    <div id="grade"><div class="vazio">Escolha uma cena a esquerda.</div></div>
  </div>
</main>

<div id="rodape">
  <span id="st">pronto</span>
  <div id="prog"><i></i></div>
  <span style="flex:1"></span>
  <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> cena &middot; <kbd>1</kbd>..<kbd>9</kbd>
  escolher &middot; <kbd>Enter</kbd> buscar &middot; <kbd>Del</kbd> tirar</span>
</div>

<script>
var P=null, sel=0, itens=[], montando=false;
var FONTES=[['google','Google'],['bing','Bing'],['ddg','DuckDuckGo'],
  ['openverse','Openverse'],['pexels','Pexels'],['pixabay','Pixabay'],
  ['pexels_video','Pexels VIDEO'],['pixabay_video','Pixabay VIDEO'],
  ['youtube','YouTube']];
var ativas=JSON.parse(localStorage.getItem('fontes')||'null')||['google','bing','ddg'];

var $=function(i){return document.getElementById(i)};
function st(t,cor){var e=$('st');e.textContent=t;e.style.color=cor||'';}
function post(rota,dados){return fetch(rota,{method:'POST',
  headers:{'Content-Type':'application/json'},body:JSON.stringify(dados||{})})
  .then(function(r){return r.json()});}

// ------------------------------------------------------------------ fontes
function pintaFontes(){
  var d=$('fontes'); d.innerHTML='';
  FONTES.forEach(function(f){
    var k=f[0], s=document.createElement('span');
    var falta = (k==='pexels'||k==='pexels_video') ? !P.chaves.pexels
              : (k==='pixabay'||k==='pixabay_video') ? !P.chaves.pixabay
              : (k==='google') ? !P.chaves.serper
              : (k==='youtube') ? !P.ytdlp : false;
    s.className='f'+(falta?' off':(ativas.indexOf(k)>=0?' on':''));
    s.textContent=f[1]+(falta?' (indisponivel)':'');
    if(!falta) s.onclick=function(){
      var i=ativas.indexOf(k);
      if(i>=0) ativas.splice(i,1); else ativas.push(k);
      if(!ativas.length) ativas=[k];
      localStorage.setItem('fontes',JSON.stringify(ativas)); pintaFontes();
    };
    d.appendChild(s);
  });
}

// ------------------------------------------------------------------ cenas
function pintaLista(){
  var d=$('lista'); d.innerHTML='';
  P.cenas.forEach(function(c,i){
    var e=document.createElement('div');
    e.className='cena'+(i===sel?' sel':'')+(c.midia?' ok':'');
    var th = c.midia
      ? (c.tipo==='video'
          ? '<div class="th">&#9654;</div>'
          : '<img class="th" src="/midia/'+encodeURIComponent(c.midia)+'?v='+Date.now()+'">')
      : '<div class="th">+</div>';
    e.innerHTML = th +
      '<div class="info"><div class="top"><span class="num">'+c.n+'</span>'+
      '<span>'+c.ini_txt+'</span><span class="tag'+(c.tipo==='video'?' v':'')+'">'+
      c.dur.toFixed(1)+'s</span></div>'+
      '<div class="tx">'+esc(c.texto||'(sem fala)')+'</div></div>';
    e.onclick=function(){ir(i)};
    d.appendChild(e);
  });
  var com=P.cenas.filter(function(c){return c.midia}).length;
  $('cab').innerHTML='<b>'+P.cenas.length+'</b> cenas &middot; <b>'+com+
    '</b> prontas &middot; faltam <b>'+(P.cenas.length-com)+'</b> &middot; '+
    P.dur_txt+' &middot; '+esc(P.audio);
}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

function ir(i){
  if(!P.cenas.length) return;
  sel=Math.max(0,Math.min(i,P.cenas.length-1));
  pintaLista();
  var el=$('lista').children[sel]; if(el) el.scrollIntoView({block:'nearest'});
  $('q').value=P.cenas[sel].busca||'';
  buscar();
}

// ----------------------------------------------------------------- buscar
var pedido=0;
function buscar(){
  var q=$('q').value.trim();
  if(!q){$('grade').innerHTML='<div class="vazio">Digite algo pra buscar.</div>';return}
  var meu=++pedido;
  $('grade').innerHTML='<div class="vazio">buscando em '+ativas.length+' fonte(s)...</div>';
  st('buscando...');
  post('/api/buscar',{q:q,fontes:ativas,lang:$('lang').value,num:14})
  .then(function(r){
    if(meu!==pedido) return;                      // busca velha chegou depois
    itens=r.itens||[];
    if(!itens.length){
      $('grade').innerHTML='<div class="vazio">nada encontrado'+
        (r.erro?' ('+esc(r.erro)+')':'')+'</div>'; st('sem resultado','var(--wr)'); return;
    }
    pintaGrade(); st(itens.length+' resultados');
  }).catch(function(e){st('erro na busca: '+e,'var(--er)')});
}

function pintaGrade(){
  var d=$('grade'); d.innerHTML='';
  itens.forEach(function(it,i){
    var e=document.createElement('div');
    e.className='r';
    var sel=it.tipo==='youtube'?'YT':it.tipo==='video'?'VIDEO':'';
    e.innerHTML='<img loading="lazy" src="'+esc(it.thumb||it.url)+'" '+
      'onerror="this.style.opacity=.15">'+
      (i<9?'<span class="k">'+(i+1)+'</span>':'')+
      (sel?'<span class="b">'+sel+'</span>':'')+
      '<div class="cap">'+esc(it.fonte)+(it.w?' &middot; '+it.w+'x'+it.h:'')+'</div>';
    e.onclick=function(){escolher(i,e)};
    d.appendChild(e);
  });
}

function escolher(i,el){
  var it=itens[i]; if(!it||!P.cenas[sel]) return;
  var c=P.cenas[sel];
  el=el||$('grade').children[i]; if(el) el.classList.add('salvando');
  st(it.tipo==='youtube'?'baixando trecho do YouTube (demora)...':'baixando...');
  post('/api/salvar',{n:c.n,url:it.url,tipo:it.tipo,yt:it.yt||'',
                      dur:c.dur,q:$('q').value})
  .then(function(r){
    if(el) el.classList.remove('salvando');
    if(!r.ok){ if(el) el.classList.add('falhou');
      st('falhou: '+r.erro,'var(--er)'); return; }
    c.midia=r.midia; c.tipo=/\.(mp4|webm|mov|mkv|m4v|avi)$/i.test(r.midia)?'video':'imagem';
    st('cena '+c.n+' ok','var(--ok)');
    if(sel<P.cenas.length-1) ir(sel+1); else pintaLista();
  }).catch(function(e){if(el)el.classList.remove('salvando');
    st('erro: '+e,'var(--er)')});
}

function limpar(){
  var c=P.cenas[sel]; if(!c||!c.midia) return;
  post('/api/limpar',{n:c.n}).then(function(){c.midia='';c.tipo='';pintaLista();
    st('cena '+c.n+' esvaziada')});
}

// ---------------------------------------------------------------- montar
function montar(){
  if(montando) return;
  var faltam=P.cenas.filter(function(c){return !c.midia}).length;
  if(faltam && !confirm(faltam+' cena(s) ainda sem midia.\n\n'+
     'Elas vao repetir a midia da cena anterior (o tempo NAO muda, a '+
     'sincronia continua exata).\n\nMontar assim mesmo?')) return;
  montando=true; $('bmontar').disabled=true; $('prog').style.display='block';
  post('/api/montar',{vivo:$('vivo').checked}).then(function(r){
    if(!r.ok){fim('erro: '+r.erro,'var(--er)');return}
    acompanhar();
  });
}
function acompanhar(){
  fetch('/api/status').then(function(r){return r.json()}).then(function(s){
    var pc=s.total?Math.round(s.feito/s.total*100):0;
    $('prog').firstElementChild.style.width=pc+'%';
    if(s.rodando){ st('montando: '+s.etapa+' ('+pc+'%)');
      setTimeout(acompanhar,700); return; }
    if(s.erro){ fim('falhou: '+s.erro,'var(--er)'); return; }
    (s.avisos||[]).forEach(function(a){console.warn(a)});
    var av=(s.avisos||[]).join(' | ');
    if(av){$('aviso').style.display='block';$('aviso').textContent='! '+av;}
    fim('PRONTO: '+(s.mensagem||s.saida),'var(--ok)');
  }).catch(function(){setTimeout(acompanhar,1500)});
}
function fim(msg,cor){montando=false;$('bmontar').disabled=false;
  $('prog').style.display='none';st(msg,cor)}

// --------------------------------------------------------------- teclado
document.addEventListener('keydown',function(e){
  var dentro=/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName);
  if(dentro){
    if(e.key==='Enter'&&e.target.id==='q'){e.preventDefault();buscar()}
    if(e.key==='Escape') e.target.blur();
    return;
  }
  if(e.key==='ArrowDown'||e.key==='j'){e.preventDefault();ir(sel+1)}
  else if(e.key==='ArrowUp'||e.key==='k'){e.preventDefault();ir(sel-1)}
  else if(e.key>='1'&&e.key<='9'){e.preventDefault();escolher(+e.key-1)}
  else if(e.key==='Delete'||e.key==='Backspace'){e.preventDefault();limpar()}
  else if(e.key==='/'){e.preventDefault();$('q').focus();$('q').select()}
});

// ----------------------------------------------------------------- carga
function carregar(dados){
  return post('/api/projeto',dados||{}).then(function(r){
    P=r;
    if(!r.ok){document.body.innerHTML='<div style="padding:40px;font:16px '+
      'system-ui;color:#ff5f56">'+esc(r.erro)+'<br><br><span style="color:#8b93a7'+
      ';font-size:14px">Coloque narracao + legenda .srt nesta pasta e recarregue.'+
      '</span></div>'; return;}
    $('alvo').value=r.alvo;
    if(r.aviso){$('aviso').style.display='block';$('aviso').textContent='! '+r.aviso}
    $('lang').value=localStorage.getItem('lang')||r.lang||'pt';
    pintaFontes(); pintaLista();
    // abre na primeira cena que ainda falta preencher
    var falta=P.cenas.findIndex(function(c){return !c.midia});
    if(P.cenas.length) ir(falta<0?0:falta);
  });
}
$('bbuscar').onclick=buscar;
$('blimpar').onclick=limpar;
$('bmontar').onclick=montar;
$('lang').onchange=function(){localStorage.setItem('lang',this.value);buscar()};
$('brec').onclick=function(){
  if(!confirm('Recalcular as cenas com ~'+$('alvo').value+'s?\n\n'+
    'As midias ja escolhidas continuam nos numeros de cena atuais, mas se a '+
    'quantidade de cenas mudar elas podem cair no trecho errado. Melhor fazer '+
    'isso ANTES de comecar a escolher.')) return;
  carregar({alvo:parseFloat($('alvo').value)||6});
};
carregar({});
</script></body></html>
"""


# ===========================================================================
# SERVIDOR
# ===========================================================================
PROJETO = None
TRAVA = threading.Lock()

TIPO_POR_EXT = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif",
                ".bmp": "image/bmp", ".tif": "image/tiff", ".tiff": "image/tiff",
                ".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime",
                ".mkv": "video/x-matroska", ".m4v": "video/mp4"}


class Rotas(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _envia(self, codigo, corpo, tipo="application/json; charset=utf-8"):
        if isinstance(corpo, str):
            corpo = corpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(corpo)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, codigo, dados):
        self._envia(codigo, json.dumps(dados, ensure_ascii=False))

    def _corpo(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return {}
        if n <= 0 or n > 32 * 1024 * 1024:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8", "ignore"))
        except Exception:
            return {}

    # -------------------------------------------------------------- GET ---
    def do_GET(self):
        caminho = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)

        if caminho in ("/", "/index.html"):
            return self._envia(200, PAGINA, "text/html; charset=utf-8")

        if caminho == "/api/status":
            return self._json(200, dict(ESTADO))

        if caminho.startswith("/midia/"):
            nome = os.path.basename(caminho[len("/midia/"):])
            arquivo = os.path.abspath(os.path.join(MIDIA, nome))
            # confina em midia/ - sem isso, /midia/..%2f..%2fchaves.json
            # serviria qualquer arquivo do disco
            if not arquivo.startswith(MIDIA + os.sep) or not os.path.isfile(arquivo):
                return self._envia(404, b"nao encontrado", "text/plain")
            ext = os.path.splitext(arquivo)[1].lower()
            with open(arquivo, "rb") as f:
                dados = f.read()
            return self._envia(200, dados,
                               TIPO_POR_EXT.get(ext, "application/octet-stream"))

        self._envia(404, b"nao encontrado", "text/plain")

    # ------------------------------------------------------------- POST ---
    def do_POST(self):
        caminho = urllib.parse.urlparse(self.path).path
        corpo = self._corpo()

        if caminho == "/api/projeto":
            with TRAVA:
                alvo = corpo.get("alvo")
                if alvo or corpo.get("recarregar"):
                    PROJETO.recarregar(alvo)
                else:
                    PROJETO._aplicar_midia()
                if not PROJETO.erro:
                    PROJETO.salvar()
                return self._json(200, PROJETO.para_json())

        if caminho == "/api/buscar":
            q = (corpo.get("q") or "").strip()
            if not q:
                return self._json(200, {"ok": False, "erro": "busca vazia",
                                        "itens": []})
            fontes = corpo.get("fontes") or ["google", "bing", "ddg"]
            lang = corpo.get("lang") or "pt"
            num = max(min(int(corpo.get("num") or 12), 40), 3)
            try:
                itens = buscar(fontes, q, num, lang)
                return self._json(200, {"ok": True, "itens": itens})
            except Exception as e:
                return self._json(200, {"ok": False, "erro": str(e), "itens": []})

        if caminho == "/api/salvar":
            try:
                n = int(corpo.get("n"))
            except (TypeError, ValueError):
                return self._json(200, {"ok": False, "erro": "cena invalida"})
            try:
                nome = salvar_cena(n, corpo.get("url", ""),
                                   corpo.get("tipo", "imagem"),
                                   corpo.get("yt", ""),
                                   float(corpo.get("dur") or 7),
                                   corpo.get("q", ""))
                with TRAVA:
                    PROJETO._aplicar_midia()
                    PROJETO.salvar()
                return self._json(200, {"ok": True, "midia": nome})
            except Exception as e:
                return self._json(200, {"ok": False, "erro": str(e)})

        if caminho == "/api/limpar":
            try:
                limpar_cena(int(corpo.get("n")))
                with TRAVA:
                    PROJETO._aplicar_midia()
                    PROJETO.salvar()
                return self._json(200, {"ok": True})
            except Exception as e:
                return self._json(200, {"ok": False, "erro": str(e)})

        if caminho == "/api/montar":
            if ESTADO["rodando"]:
                return self._json(200, {"ok": False, "erro": "ja esta montando"})
            vivo = bool(corpo.get("vivo"))
            saida = os.path.basename(corpo.get("saida") or "video.mp4")

            def tarefa():
                try:
                    with TRAVA:
                        PROJETO._aplicar_midia()
                    ok, msg = montar(PROJETO, vivo, saida)
                    if not ok:
                        ESTADO.update(rodando=False, erro=msg)
                    else:
                        ESTADO["mensagem"] = msg
                        log("\n OK: %s" % msg)
                except Exception as e:
                    ESTADO.update(rodando=False, erro=str(e))

            ESTADO.update(rodando=True, feito=0, total=len(PROJETO.cenas) + 1,
                          etapa="iniciando", erro="", saida="", avisos=[],
                          mensagem="")
            threading.Thread(target=tarefa, daemon=True).start()
            return self._json(200, {"ok": True})

        self._json(404, {"erro": "rota desconhecida"})


# ===========================================================================
# MAIN
# ===========================================================================
def resumo(proj):
    log("=" * 62)
    if proj.erro:
        log(" ERRO: %s" % proj.erro)
        log("=" * 62)
        return False
    com = sum(1 for c in proj.cenas if c.get("midia"))
    log("  Audio  : %s  (%s)" % (os.path.basename(proj.audio),
                                 hms(proj.fim_total)))
    log("  Legenda: %s" % os.path.basename(proj.srt))
    log("  Cenas  : %d  (alvo %.1fs)  |  com midia: %d  |  faltam: %d"
        % (len(proj.cenas), proj.alvo, com, len(proj.cenas) - com))
    quadros = sum(c["quadros"] for c in proj.cenas)
    log("  Quadros: %d  ->  %.3fs  (audio %.3fs  |  erro %+.3fs)"
        % (quadros, quadros / FPS, proj.fim_total,
           quadros / FPS - proj.fim_total))
    if proj.aviso:
        log("  ! %s" % proj.aviso)
    if not tem("ffmpeg"):
        log("  ! ffmpeg nao esta no PATH - da pra escolher midia, mas nao montar.")
    if not TEM_YTDLP:
        log("  ! yt-dlp nao instalado - a fonte YouTube fica fora"
            " (pip install -U yt-dlp).")
    log("=" * 62)
    return True


def main():
    global PROJETO
    argumentos = sys.argv[1:]

    def opcao(nome, padrao=None):
        if nome in argumentos:
            i = argumentos.index(nome)
            return argumentos[i + 1] if i + 1 < len(argumentos) else True
        return padrao

    alvo = opcao("--alvo")
    PROJETO = Projeto()
    if alvo:
        PROJETO.recarregar(float(alvo))

    if not resumo(PROJETO):
        sys.exit(1)

    if "--montar" in argumentos:
        ok, msg = montar(PROJETO, vivo="--vivo" in argumentos,
                         saida=str(opcao("--saida", "video.mp4")))
        for a in ESTADO.get("avisos") or []:
            log("  ! %s" % a)
        log((" PRONTO: " if ok else " FALHOU: ") + msg)
        sys.exit(0 if ok else 1)

    PROJETO.salvar()
    porta = int(opcao("--porta", PORTA))
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), Rotas)
    url = "http://localhost:%d/" % porta
    log("  Abra:  %s      (Ctrl+C para parar)" % url)
    log("=" * 62)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        log("\n  Encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
