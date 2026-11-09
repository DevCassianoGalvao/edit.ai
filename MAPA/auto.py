# -*- coding: utf-8 -*-
"""
auto.py - do roteiro as imagens, sem abrir o navegador.

    py auto.py

Le tres arquivos da pasta e um plano, e enche `downloads/paragrafo NN/` com as
imagens certas. Depois disso o caminho e o de sempre:

    py sincronizar.py --capcut     (corta em clipes de duracao exata)
    py b.py                        (monta o projeto do CapCut)

------------------------------------------------------------------------------
POR QUE ISTO EXISTE, sendo que o buscador-imagens.html ja fazia isto

Porque as duas metades do trabalho sao de naturezas diferentes, e estavam
juntas.

A metade SEMANTICA - ler o roteiro, entender do que ele fala, decidir o que
cada trecho precisa mostrar e escrever a frase de busca - e um trabalho de
leitura. Na pagina isso e feito por ~3 mil linhas de heuristica (detectDominio,
planParts, conceptsRanked, aspectsFor...) que adivinha o assunto contando
palavra capitalizada. Funciona, mas e adivinhacao: foi ela que produziu "Rogge"
como frase de busca inteira, e "Dioxido de carbono supercritico rodando na
estrada".

A metade MECANICA - consultar oito fontes, cruzar o resultado com o que a parte
pede, jogar fora loja/jogo/brasao/miniatura/marca d'agua/outra epoca, nao
repetir, e baixar - e um trabalho de execucao. Essa parte a heuristica faz bem,
porque e verificavel.

Aqui as duas se separam. A leitura vira `plano.json`, escrito por quem leu o
roteiro de verdade. A execucao continua sendo codigo. O motor nao muda de um
video para o outro; o plano muda.

E o mesmo desenho do `edit_plan.json`: decisao editorial e DADO, nao codigo.

------------------------------------------------------------------------------
O QUE PRECISA ESTAR NA PASTA

    roteiro.txt      o texto narrado (o MESMO que gerou o audio)
    legenda.srt      a sincronia   (ou --sem-srt para dividir por tempo)
    narracao.mp3     opcional, so para conferir a duracao total
    plano.json       o contexto e os termos de busca

Gere um plano em branco, ja dividido nas partes certas, com:

    py auto.py --modelo
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(AQUI, "downloads")

# O console do Windows e cp1252 e nao escreve "-6 C" com o sinal de menos
# tipografico, nem chines, nem cirilico. Sem isto um `print` derruba o
# programa inteiro com UnicodeEncodeError - ja aconteceu tres vezes neste
# projeto, e uma vez custou a geracao de 252 clipes. Mostrar texto e
# conveniencia; o trabalho e outro. O que nao couber vira "?".
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


import curadoria
import sincronizar as S

try:
    import bancos
except Exception as e:                                     # pragma: no cover
    bancos = None
    print(" ! bancos.py nao carregou: %s" % e)

# O servidor tem as funcoes de busca do Serper/Pexels/Pixabay/Openverse/DDG.
# Importa-lo NAO sobe servidor nenhum: o main() dele so roda sob __main__.
try:
    import servidor as SRV
except Exception as e:                                     # pragma: no cover
    SRV = None
    print(" ! servidor.py nao carregou: %s" % e)


# ===========================================================================
# CHAVES
# ===========================================================================
def chave(nome, arquivo=""):
    v = (os.environ.get(nome) or "").strip()
    if v:
        return v
    for cand in ([arquivo] if arquivo else []) + [nome.lower() + ".txt"]:
        p = os.path.join(AQUI, cand)
        if os.path.isfile(p):
            try:
                return open(p, encoding="utf-8").read().strip().splitlines()[0].strip()
            except Exception:
                pass
    # .env simples (CHAVE=valor), se existir
    env = os.path.join(AQUI, ".env")
    if os.path.isfile(env):
        try:
            for linha in open(env, encoding="utf-8"):
                if linha.strip().startswith(nome + "="):
                    return linha.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return ""


# ===========================================================================
# 1. AS PARTES E OS TEMPOS
# ===========================================================================
def dividir_roteiro(texto, chars):
    return S.split_by_chars(texto, chars)


def tempos_por_srt(partes, caminho_srt, duracao_audio=None):
    """Instante real de inicio e fim de cada parte, lido da legenda.

    Casa as palavras do roteiro com as da legenda por comparacao de sequencia.
    Se o casamento for ruim (roteiro diferente do que foi narrado), cai para o
    modo proporcional - menos exato, mas nunca fora de ordem.
    """
    cues = S.parse_srt(caminho_srt)
    if not cues:
        raise SystemExit("a legenda %s nao tem nenhuma marcacao de tempo" % caminho_srt)

    palavras, marcas = S.srt_word_times(cues)
    inicios, qualidade = S.alinhar(partes, palavras, marcas)
    metodo = "palavra a palavra (%.0f%% de casamento)" % (qualidade * 100)

    if qualidade < 0.35:
        inicios = S.alinhar_proporcional(partes, cues)
        metodo = "proporcional (casamento de so %.0f%%)" % (qualidade * 100)

    # O SRT costuma terminar um pouco antes do audio (silencio no fim, vinheta),
    # e nesse caso a ultima parte se estende para cobrir a narracao inteira -
    # senao o video sai mais curto que o som. E o que o sincronizar.py tambem
    # faz, e os dois precisam concordar ou a linha do tempo nao bate.
    #
    # Mas "um pouco" tem limite. Um audio MUITO maior que o SRT nao e silencio
    # no fim: e outro arquivo. Esticar calado nesse caso dava uma ultima parte
    # de 24 minutos pedindo 12 imagens - o erro silencioso, que so aparece
    # assistindo. Acima de 25% de diferenca a legenda manda, e a tela avisa.
    fim_srt = cues[-1][1]
    fim_total = fim_srt
    aviso = ""
    if duracao_audio and duracao_audio > fim_srt + 0.5:
        sobra = duracao_audio - fim_srt
        if sobra <= max(fim_srt * 0.25, 5.0):
            fim_total = duracao_audio
            aviso = "audio %s alem do SRT: ultima parte esticada" % S.hms_curto(sobra)
        else:
            aviso = ("ATENCAO: o audio (%s) e MUITO maior que a legenda (%s). "
                     "Provavelmente nao sao do mesmo video - usando o fim da legenda."
                     % (S.hms_curto(duracao_audio), S.hms_curto(fim_srt)))
    elif duracao_audio and duracao_audio < fim_srt - 0.5:
        aviso = ("ATENCAO: a legenda vai ate %s mas o audio so tem %s - "
                 "a legenda parece ser de outra versao da narracao."
                 % (S.hms_curto(fim_srt), S.hms_curto(duracao_audio)))
    if aviso:
        metodo += chr(10) + "           " + aviso

    fora = []
    for i, ini in enumerate(inicios):
        fim = inicios[i + 1] if i + 1 < len(inicios) else fim_total
        fora.append({"inicio": round(ini, 3), "fim": round(fim, 3),
                     "duracao": round(max(fim - ini, 0.1), 3)})
    return fora, metodo


def quantas_midias(tempos, seg_por_item, minimo, maximo):
    """Quantas imagens cada parte comporta, pela duracao REAL dela.

    Uma parte de 45s com alvo de 6s pede 8 imagens; uma de 12s pede 2. E o
    oposto de dar o mesmo numero para todas - narracao nao e uniforme.

    O piso cede quando a parte e curta: exigir 2 midias numa parte de 1,2s da
    0,6s cada, que o olho nao le - vira flash, nao imagem.
    """
    fora = []
    for t in tempos:
        dur = t["duracao"]
        n = int(round(dur / seg_por_item)) or 1
        cabe = max(1, int(dur / 1.5))
        n = max(min(n, maximo), min(minimo, cabe))
        fora.append(n)
    return fora


# ===========================================================================
# 2. A BUSCA
# ===========================================================================
def _img(url, titulo, fonte, w=0, h=0, prov="", x=None):
    x = x or {}
    return {"url": url, "title": titulo, "source": fonte,
            "width": w or 0, "height": h or 0, "provider": prov, "isVideo": False,
            "license": x.get("license") or "unverified", "author": x.get("author") or "",
            "page": x.get("page") or "",
            "origWidth": x.get("origWidth") or 0, "origHeight": x.get("origHeight") or 0}


# Fonte que nao responde sai de cena. Sem isto, um servico fora do ar custa o
# TEMPO DE ESPERA vezes o numero de consultas - e foi exatamente o que
# aconteceu: o DuckDuckGo passou a devolver zero resultado em 20 segundos
# (bloqueio do lado deles), e 41 partes x 2 frases x 20s viraram quase meia
# hora de espera por NADA. A rodada inteira ficou 11 minutos mais lenta sem que
# nenhuma imagem a mais entrasse.
#
# Tres tentativas seguidas sem resultado e a fonte fica de fora do resto da
# rodada. Nao e desistir cedo: e parar de pagar por um servico que ja disse
# tres vezes que nao tem nada.
_ZEROS = {}
_LIMITE_ZEROS = 3


def _buscar_fonte_bruto(nome, q, quantos, lang, offset, chaves, log):
    """Uma fonte, isolada: se ela cair, as outras seguem. Era esse isolamento
    que faltava na primeira versao da pagina - a excecao do Serper (chave
    vencida) abortava a parte ANTES de consultar os bancos, e o video inteiro
    vinha vazio mesmo com o Pexels respondendo."""
    if _ZEROS.get(nome, 0) >= _LIMITE_ZEROS:
        return []
    t0 = time.monotonic()
    try:
        if nome == "wikimedia" and bancos:
            return [_img(x["imageUrl"], x["title"], x["source"], x.get("width"), x.get("height"), "Wikimedia", x)
                    for x in bancos.wikimedia_images(q, quantos, lang, offset=offset)]
        if nome == "nasa" and bancos:
            return [_img(x["imageUrl"], x["title"], x["source"], 0, 0, "NASA")
                    for x in bancos.nasa_images(q, quantos, lang, offset=offset)]
        if nome == "archive" and bancos:
            return [_img(x["imageUrl"], x["title"], x["source"], 0, 0, "Internet Archive")
                    for x in bancos.archive_images(q, quantos, lang, offset=offset)]
        if not SRV:
            return []
        if nome == "openverse":
            return [_img(x["imageUrl"], x["title"], x["source"], x.get("width"), x.get("height"), "Openverse", x)
                    for x in SRV.openverse_images(q, quantos, lang)]
        if nome == "pexels" and chaves.get("pexels"):
            return [_img(x["imageUrl"], x["title"], x["source"], x.get("width"), x.get("height"), "Pexels")
                    for x in SRV.pexels_images(q, quantos, lang, chaves["pexels"])]
        if nome == "pixabay" and chaves.get("pixabay"):
            return [_img(x["imageUrl"], x["title"], x["source"], x.get("width"), x.get("height"), "Pixabay")
                    for x in SRV.pixabay_images(q, quantos, lang, chaves["pixabay"])]
        if nome == "ddg":
            return [_img(x["imageUrl"], x["title"], x["source"], x.get("width"), x.get("height"), "DuckDuckGo")
                    for x in SRV.ddg_images(q, quantos, lang)]
        if nome == "google" and chaves.get("serper"):
            r = SRV.serper_images(chaves["serper"], {"q": q, "num": quantos,
                                                     "hl": lang, "gl": lang, "tbs": "itp:photo"})
            return [_img(x.get("imageUrl"), x.get("title"), x.get("domain") or x.get("source") or "",
                         x.get("imageWidth"), x.get("imageHeight"), "Google")
                    for x in (r.get("images") or []) if x.get("imageUrl")]
    except Exception as e:
        log("      ! %s falhou: %s" % (nome, str(e)[:70]))
        _marcar_zero(nome, time.monotonic() - t0, log)
    return []


def buscar_fonte(nome, q, quantos, lang, offset, chaves, log):
    """Chama a fonte e CONTA os zeros. O caminho de sucesso tambem conta: o
    DuckDuckGo respondia 200 com lista vazia em 20 segundos - nao era erro,
    era uma fonte viva que nao serve para nada. Contar so as excecoes deixaria
    ela consumindo a rodada inteira."""
    if _ZEROS.get(nome, 0) >= _LIMITE_ZEROS:
        return []
    t0 = time.monotonic()
    r = _buscar_fonte_bruto(nome, q, quantos, lang, offset, chaves, log)
    if r:
        _ZEROS[nome] = 0          # respondeu: zera a contagem
    else:
        _marcar_zero(nome, time.monotonic() - t0, log)
    return r


def _marcar_zero(nome, gasto, log):
    _ZEROS[nome] = _ZEROS.get(nome, 0) + 1
    if _ZEROS[nome] == _LIMITE_ZEROS:
        log("      (%s nao devolveu nada %d vezes - fica fora do resto da rodada%s)"
            % (nome, _LIMITE_ZEROS,
               ", estava custando %.0fs por consulta" % gasto if gasto > 3 else ""))


def buscar_parte(parte, quantos, fontes, lang, idx, chaves, log):
    """Todas as frases da parte, em todas as fontes marcadas.

    Pede MUITO mais do que vai usar: a curadoria descarta a maior parte, e sem
    essa folga a parte terminaria com metade das midias - o remedio ficaria
    pior que a doenca.
    """
    from concurrent.futures import ThreadPoolExecutor

    pool = max(quantos * 3, quantos + 8)
    achados = []
    for j, q in enumerate(parte.get("busca") or []):
        if not q:
            continue
        # Deslocamento diferente por parte E por frase: duas partes que caem na
        # mesma frase generica recebem material diferente, em vez das mesmas
        # duas primeiras fotos.
        #
        # A FAIXA E CURTA (0 a 11) de proposito, e isso custou caro para
        # descobrir. Com 0 a 40, a parte 11 de um roteiro caia em off=30 - e a
        # trigesima resposta de uma busca especifica ja nao tem nada a ver.
        # Medido em "alagamento Sao Paulo":
        #
        #     off= 0   Alagamento Taboao
        #     off= 6   Alagamento Taboao
        #     off=12   Obras anti enchente no corrego
        #     off=30   Toronto's Flood          <- outro pais
        #
        # A parte ficava vazia e o motivo aparecia como "falta o que a parte
        # EXIGE", mascarando a causa real: a busca nem tinha chegado ao
        # material certo. A repeticao entre partes ja e evitada pela memoria de
        # "ja usada"; o deslocamento e so um desempate, e nao precisa ser largo.
        off = (idx * 5 + j * 3) % 12

        # As fontes sao SERVIDORES DIFERENTES: esperar a resposta do Commons
        # para so entao perguntar ao Openverse e tempo jogado fora. Em paralelo
        # a frase inteira custa o tempo da fonte mais lenta, nao a soma de
        # todas. O freio de requisicoes continua valendo - ele e por host, e
        # hosts diferentes nao competem entre si.
        vivas = [f for f in fontes if _ZEROS.get(f, 0) < _LIMITE_ZEROS]
        if not vivas:
            break
        if len(vivas) == 1:
            achados += buscar_fonte(vivas[0], q, pool, lang, off, chaves, log)
        else:
            with ThreadPoolExecutor(max_workers=len(vivas)) as ex:
                for r in ex.map(lambda f: buscar_fonte(f, q, pool, lang, off, chaves, log), vivas):
                    achados += r
        if len(achados) >= pool * 2:
            break
    return achados


# ===========================================================================
# 3. O DOWNLOAD
# ===========================================================================
# Espacamento entre downloads do MESMO servidor. A busca ja tinha freio; o
# download nao tinha nenhum - e foi ali que a coisa quebrou: 252 imagens
# pedidas em rajada ao upload.wikimedia.org devolveram 52 vezes
# "429 Too many requests", e o vídeo ficou com 200 fotos em vez de 252.
#
# O numero e por HOST, nao global: baixar do Openverse enquanto se espera a
# Wikimedia nao custa nada.
_ESPERA_HOST = {"upload.wikimedia.org": 0.7, "commons.wikimedia.org": 0.7}
_ESPERA_PADRAO = 0.15
_ultimo_em = {}


def _freio(url):
    import urllib.parse
    host = urllib.parse.urlparse(url).netloc.lower()
    espera = _ESPERA_HOST.get(host, _ESPERA_PADRAO)
    gap = time.monotonic() - _ultimo_em.get(host, 0.0)
    if gap < espera:
        time.sleep(espera - gap)
    _ultimo_em[host] = time.monotonic()
    return host


def _nome_ascii(titulo):
    """Nome de arquivo em ASCII puro.

    O padrao de palavra do Python 3 e Unicode-aware, entao titulos do Commons
    "SZ ..... Shenzhen ..... BaoAn" chegavam INTEIROS ao nome do arquivo. Esses
    arquivos viajam para o CapCut e passam pelo console do Windows (cp1252),
    e um deles derrubou a geracao dos 252 clipes com UnicodeEncodeError.
    Acento vira a letra base; o que nao tem equivalente sai.
    """
    import unicodedata
    t = unicodedata.normalize("NFKD", str(titulo or "img"))
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^\w\- ]+", "_", t).strip()
    t = re.sub(r"_{2,}", "_", t)[:40].strip(" _")
    return t or "img"


def baixar(itens, numero, log, inicio=1, limpar=True):
    pasta = "paragrafo %02d" % numero
    destino = os.path.join(DOWNLOADS, pasta)
    os.makedirs(destino, exist_ok=True)
    salvos = []
    for k, it in enumerate(itens, inicio):
        nome = "%02d_%s" % (k, _nome_ascii(it.get("title")))
        erro = ""
        # 429 nao e "esta imagem nao existe", e "voce pediu rapido demais" -
        # desistir na primeira tentativa joga fora material que estava ali.
        for tentativa in range(3):
            host = _freio(it["url"])
            try:
                salvos.append(SRV.save_image(pasta, nome, it["url"]))
                erro = ""
                break
            except Exception as e:
                erro = str(e)
                if "429" in erro or "too many" in erro.lower() or "503" in erro:
                    # e o servidor pedindo calma: espera mais e alarga o freio
                    # daquele host para o resto da rodada.
                    _ESPERA_HOST[host] = min(_ESPERA_HOST.get(host, _ESPERA_PADRAO) * 1.8, 6.0)
                    time.sleep(1.5 * (tentativa + 1))
                    continue
                break          # erro de verdade (404, link morto): nao insiste
        if erro:
            log("      ! nao baixou (%s): %s" % (it.get("provider"), erro[:60]))

    # A pasta e o RESULTADO desta rodada, nao um acumulador. Rodar de novo
    # escolhe imagens um pouco diferentes (a memoria de "ja usada" comeca
    # limpa), e com nomes diferentes as antigas ficavam. Numa medicao real
    # sobraram 41 arquivos em 11 partes: a parte 04 terminou com 12 imagens
    # para 34,7s, ou seja 2,9s cada em vez dos 6s pedidos. O ritmo do video
    # mudava sem ninguem pedir - e sem ninguem ver.
    ficam = {os.path.basename(x) for x in salvos}
    sobrou = 0
    # --completar: o que ja esta na pasta foi aprovado na folha de contato e fica.
    for velho in (os.listdir(destino) if limpar else []):
        if velho.startswith(".") or velho in ficam:
            continue
        try:
            os.remove(os.path.join(destino, velho))
            sobrou += 1
        except OSError:
            pass
    if sobrou:
        log("      (removi %d arquivo(s) de uma rodada anterior)" % sobrou)
    return salvos


def ja_tem(numero):
    """Quantos arquivos a pasta desta parte ja tem. E o que permite rodar de
    novo para COMPLETAR em vez de refazer tudo."""
    d = os.path.join(DOWNLOADS, "paragrafo %02d" % numero)
    if not os.path.isdir(d):
        return 0
    return len([x for x in os.listdir(d) if not x.startswith(".")])


# ===========================================================================
# O PLANO
# ===========================================================================
def modelo_de_plano(partes, tempos, quantos, destino):
    """Escreve um plano em BRANCO, ja com as partes divididas e a duracao real
    de cada uma. E o arquivo que alguem que leu o roteiro preenche."""
    plano = {
        "_leia": "Preencha 'busca' (1 a 3 frases) e 'mostrar' de cada parte. "
                 "O texto e a duracao ja estao certos - nao mexa neles.",
        "idioma": "pt",
        "tema": "",
        "assunto": "",
        "epoca": None,
        "fontes": ["wikimedia", "archive", "openverse", "nasa"],
        "evitar": [],
        "partes": [],
    }
    for i, txt in enumerate(partes):
        plano["partes"].append({
            "n": i + 1,
            "dur": tempos[i]["duracao"],
            "midias": quantos[i],
            "texto": txt.strip()[:400],
            "busca": [],
            "mostrar": [],
        })
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(plano, f, ensure_ascii=False, indent=2)
    return destino


def validar_plano(plano, n_partes):
    problemas = []
    partes = plano.get("partes") or []
    if len(partes) != n_partes:
        problemas.append("o plano tem %d partes e o roteiro tem %d - o roteiro ou o "
                         "--chars mudou desde que o plano foi escrito" % (len(partes), n_partes))
    vazias = [p.get("n") for p in partes if not (p.get("busca") or [])]
    if vazias:
        problemas.append("%d parte(s) sem frase de busca: %s"
                         % (len(vazias), ", ".join(str(x) for x in vazias[:12])))
    sem_mostrar = [p.get("n") for p in partes if not (p.get("mostrar") or [])]
    if len(sem_mostrar) > n_partes * 0.5:
        problemas.append("%d parte(s) sem 'mostrar' - a curadoria fica sem regua e "
                         "aprova quase tudo" % len(sem_mostrar))
    return problemas


# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="do roteiro as imagens, sem navegador")
    ap.add_argument("--roteiro", default="roteiro.txt")
    ap.add_argument("--srt", default="legenda.srt")
    ap.add_argument("--audio", default="")
    ap.add_argument("--plano", default="plano.json")
    ap.add_argument("--chars", type=int, default=700,
                    help="tamanho de cada parte, em caracteres (padrao 700)")
    ap.add_argument("--seg", type=float, default=6.0,
                    help="segundos que cada imagem fica na tela (padrao 6; use 5 a 8)")
    ap.add_argument("--seg-inicio", type=float, default=0.0, dest="seg_inicio",
                    help="segundos por imagem no gancho (ex.: 3.3); 0 desliga")
    ap.add_argument("--inicio", type=float, default=90.0,
                    help="ate que segundo vale o --seg-inicio (padrao 90)")
    ap.add_argument("--min", type=int, default=2, dest="minimo")
    ap.add_argument("--max", type=int, default=12, dest="maximo")
    ap.add_argument("--modelo", action="store_true",
                    help="so escreve um plano.json em branco, ja dividido, e sai")
    ap.add_argument("--so-plano", action="store_true",
                    help="mostra o que seria buscado e nao baixa nada")
    ap.add_argument("--parte", type=int, default=0, help="roda uma parte so (para testar)")
    ap.add_argument("--partes", default="",
                    help="roda so estas partes (ex.: 9,13,24). As outras ficam intactas no disco "
                         "e no relatorio, e o que elas ja usam nao pode ser escolhido de novo")
    ap.add_argument("--completar", action="store_true",
                    help="so as partes com falta de foto; MANTEM o que ja esta na pasta e baixa "
                         "apenas o que falta (numeracao continua depois das antigas)")
    args = ap.parse_args()

    def log(m):
        print(m)
        sys.stdout.flush()

    for f in (args.roteiro, args.srt):
        if not os.path.isfile(os.path.join(AQUI, f)):
            sys.exit("nao achei %s nesta pasta." % f)

    texto = open(os.path.join(AQUI, args.roteiro), encoding="utf-8-sig", errors="replace").read()
    partes = dividir_roteiro(texto, args.chars)
    if not partes:
        sys.exit("o roteiro ficou vazio depois de dividir.")

    # `achar_audio` devolve (nome, achou_sozinho) e procura no diretorio ATUAL;
    # aqui o certo e sempre a pasta do projeto, entao a busca e feita a mao.
    audio = args.audio
    if not audio:
        cands = [(os.path.getsize(os.path.join(AQUI, n)), n) for n in os.listdir(AQUI)
                 if n.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"))]
        audio = max(cands)[1] if cands else ""
    dur_audio = S.duracao_audio(os.path.join(AQUI, audio)) if audio else None

    log("=" * 62)
    log(" Roteiro : %d partes de ~%d caracteres" % (len(partes), args.chars))
    tempos, metodo = tempos_por_srt(partes, os.path.join(AQUI, args.srt), dur_audio)
    log(" Sincronia: %s" % metodo)
    quantos = quantas_midias(tempos, args.seg, args.minimo, args.maximo)
    # Gancho: o trecho antes de --inicio segundos pede corte mais curto
    # (--seg-inicio). A parte que atravessa a fronteira soma as duas cotas.
    if args.seg_inicio:
        for i, t in enumerate(tempos):
            dentro = max(0.0, min(t["fim"], args.inicio) - t["inicio"])
            if dentro <= 0:
                continue
            fora = t["duracao"] - dentro
            quantos[i] = max(quantos[i], int(round(dentro / args.seg_inicio))
                             + int(round(fora / args.seg)))
    log(" Ritmo   : ~%.1fs por imagem  ->  %d imagens no total"
        % (args.seg, sum(quantos)))
    log(" Fim     : %s" % S.hms(tempos[-1]["fim"]))
    log("=" * 62)

    caminho_plano = os.path.join(AQUI, args.plano)
    if args.modelo:
        modelo_de_plano(partes, tempos, quantos, caminho_plano)
        log("")
        log(" Escrevi %s com %d partes em branco." % (args.plano, len(partes)))
        log(" Preencha 'busca' e 'mostrar' de cada parte e rode de novo sem --modelo.")
        return

    if not os.path.isfile(caminho_plano):
        sys.exit("nao achei %s. Gere um em branco com:  py auto.py --modelo" % args.plano)

    plano = json.load(open(caminho_plano, encoding="utf-8"))
    problemas = validar_plano(plano, len(partes))
    if problemas:
        log("")
        for p in problemas:
            log(" ! " + p)
        if any("partes e o roteiro tem" in p for p in problemas):
            sys.exit(" O plano nao corresponde a este roteiro. Refaca com --modelo.")
        log("")

    lang = plano.get("idioma") or "pt"
    epoca = plano.get("epoca") or None
    fontes = plano.get("fontes") or ["wikimedia", "archive", "openverse"]
    evitar_global = plano.get("evitar") or []
    exigir_global = plano.get("exigir") or []
    chaves = {"serper": chave("SERPER_API_KEY", "serper.txt"),
              "pexels": chave("PEXELS_KEY", "pexels.txt"),
              "pixabay": chave("PIXABAY_KEY", "pixabay.txt")}
    if "google" in fontes and not chaves["serper"]:
        fontes = [f for f in fontes if f != "google"]
        log(" (sem chave da Serper - o Google fica de fora)")

    log(" Fontes  : %s" % ", ".join(fontes))
    if epoca:
        log(" Epoca   : %s (janela %s-%s)" % (epoca.get("ano"), epoca.get("min"), epoca.get("max")))
    log("=" * 62)
    log("")

    memoria = curadoria.Memoria()
    relatorio = []
    t0 = time.time()

    so = {int(x) for x in args.partes.split(",") if x.strip()} if args.partes else set()
    if args.parte:
        so.add(args.parte)
    if args.completar:
        so = {i + 1 for i in range(len(quantos)) if ja_tem(i + 1) < quantos[i] - 1}
        log(" Completar: %d parte(s) com falta -> %s" % (len(so), ", ".join(map(str, sorted(so)))))

    # Rejeitadas na folha de contato: fora do pool em TODA rodada. Sem isto o
    # auto.py recria a memoria do zero e traz o mesmo lixo de volta (cache).
    caminho_rej = os.path.join(AQUI, "data", "image_rejects.json")
    rejeitadas = set()
    if os.path.isfile(caminho_rej):
        rejeitadas = {curadoria.chave_url(x.get("url")) for x in
                      json.load(open(caminho_rej, encoding="utf-8")).get("itens", [])}
        log(" Rejeitadas (folha de contato): %d fora do pool" % len(rejeitadas))

    # Rodando so algumas partes: o que as outras ja mostram conta como usado,
    # senao a parte refeita pega a mesma foto de uma vizinha.
    caminho_rel = os.path.join(AQUI, "auto_relatorio.json")
    relatorio_antigo = []
    if so and os.path.isfile(caminho_rel):
        relatorio_antigo = json.load(open(caminho_rel, encoding="utf-8")).get("partes", [])
        for r in relatorio_antigo:
            if r.get("n") in so:
                continue
            for it in r.get("itens") or []:
                memoria.marcar({"url": it.get("url"), "title": it.get("titulo")})

    for i, p_plano in enumerate(plano["partes"]):
        n = i + 1
        if so and n not in so:
            continue
        alvo = quantos[i]
        antigos, inicio = [], 1
        if args.completar:
            antigos = next((r.get("itens") or [] for r in relatorio_antigo if r.get("n") == n), [])
            pasta_n = os.path.join(DOWNLOADS, "paragrafo %02d" % n)
            no_disco_idx = ({int(x.split("_")[0]) for x in os.listdir(pasta_n) if x[:2].isdigit()}
                            if os.path.isdir(pasta_n) else set())
            for k, it in enumerate(antigos, 1):
                if k in no_disco_idx:
                    memoria.marcar({"url": it.get("url"), "title": it.get("titulo")})
            inicio = len(antigos) + 1
            alvo = max(0, alvo - len(no_disco_idx))
        mostrar = p_plano.get("mostrar") or []
        # `exigir` sai da parte OU do plano inteiro. O global e o que amarra o
        # video ao seu lugar: num roteiro sobre a enchente no Rio Grande do Sul,
        # sem isso o acervo devolve enchente em Salt Lake City com nota alta.
        exigir = list(p_plano.get("exigir") or exigir_global or [])
        evitar = list(evitar_global) + list(p_plano.get("evitar") or [])
        buscas = p_plano.get("busca") or []

        log(" parte %02d  %5.1fs  pede %d  |  %s"
            % (n, tempos[i]["duracao"], alvo, " / ".join(buscas)[:58]))

        if not buscas:
            log("           (sem frase de busca no plano - pulada)")
            relatorio.append({"n": n, "pedidas": alvo, "achadas": 0, "motivo": "sem busca no plano"})
            continue

        brutos = buscar_parte(p_plano, alvo, fontes, lang, i, chaves, log)
        if rejeitadas:
            brutos = [b for b in brutos if curadoria.chave_url(b.get("url")) not in rejeitadas]
        if p_plano.get("retrato"):
            for b in brutos:
                b["_retrato_ok"] = True
        escolhidos, motivos = curadoria.curar(brutos, mostrar, alvo, evitar, epoca, memoria, exigir)

        desc = sum(motivos.values())
        top = sorted(motivos.items(), key=lambda kv: -kv[1])[:3]
        log("           %d de %d candidatas | descartou %d%s"
            % (len(escolhidos), len(brutos), desc,
               ("  (" + ", ".join("%s %d" % (k, v) for k, v in top) + ")") if top else ""))

        if len(escolhidos) < alvo:
            log("           ! faltaram %d - amplie 'busca' desta parte no plano"
                % (alvo - len(escolhidos)))

        no_disco = 0
        if not args.so_plano and escolhidos:
            salvos = baixar(escolhidos, n, log, inicio=inicio, limpar=not args.completar)
            no_disco = ja_tem(n)
            aviso = ""
            if no_disco < alvo:
                aviso = "   (a pasta ficou com %d de %d)" % (no_disco, alvo)
            log("           baixou %d para downloads/paragrafo %02d/%s"
                % (len(salvos), n, aviso))
        relatorio.append({"n": n, "pedidas": alvo, "achadas": len(escolhidos),
                          "no_disco": no_disco,
                          "candidatas": len(brutos), "motivos": motivos,
                          "itens": antigos + [{"url": x["url"], "titulo": x["title"],
                                     "fonte": x["source"], "nota": x["_nota"],
                                     "licenca": x.get("license") or "unverified",
                                     "autor": x.get("author") or "",
                                     "pagina": x.get("page") or ""}
                                    for x in escolhidos]})

    # Rodada parcial: MESCLA com o relatorio do disco (as outras partes guardam
    # licenca e autor das fotos que continuam no filme).
    if so and relatorio_antigo:
        novos = {r["n"]: r for r in relatorio}
        relatorio = [novos.pop(r["n"], r) for r in relatorio_antigo] + list(novos.values())
        relatorio.sort(key=lambda r: r["n"])
    with open(caminho_rel, "w", encoding="utf-8") as f:
        json.dump({"partes": relatorio, "tempos": tempos, "metodo": metodo},
                  f, ensure_ascii=False, indent=2)

    # partes.json e a fonte da verdade do sincronizar.py: sem ele o script
    # recalcula a divisao no chute e as pastas saem fora de posicao.
    os.makedirs(DOWNLOADS, exist_ok=True)
    with open(os.path.join(DOWNLOADS, "partes.json"), "w", encoding="utf-8") as f:
        json.dump({"charsPer": args.chars, "partes": partes}, f, ensure_ascii=False, indent=2)

    pedidas = sum(r["pedidas"] for r in relatorio)
    achadas = sum(r["achadas"] for r in relatorio)

    log("")
    log("=" * 62)
    log(" Curadoria aprovou : %d de %d pedidas   em %.0f min"
        % (achadas, pedidas, (time.time() - t0) / 60))

    # O que a curadoria APROVOU e o que esta NO DISCO sao dois numeros, e eles
    # divergem: um download pode falhar (429, link morto) depois da imagem ja
    # ter sido escolhida. A primeira versao mostrava so o primeiro numero e
    # dizia "252 de 252, 100%" com 200 arquivos na pasta - a ferramenta
    # mentindo sobre o proprio resultado, que e o pior tipo de erro porque so
    # aparece na montagem.
    if not args.so_plano:
        no_disco = sum(ja_tem(r["n"]) for r in relatorio)
        curtas = [(r["n"], ja_tem(r["n"]), r["pedidas"])
                  for r in relatorio if ja_tem(r["n"]) < r["pedidas"]]
        log(" NO DISCO          : %d de %d   (%.0f%%)"
            % (no_disco, pedidas, 100 * no_disco / max(pedidas, 1)))
        if curtas:
            log("")
            log(" %d parte(s) com menos arquivo do que o pedido:" % len(curtas))
            log("   " + ", ".join("%02d (%d/%d)" % c for c in curtas[:18]))
            log("")
            log(" Rode  py auto.py  de novo: a busca vem do cache (rapida) e o")
            log(" download tenta so o que faltou. Se persistir, amplie 'busca'")
            log(" dessas partes no plano.json.")
    log("")
    log(" Detalhes em auto_relatorio.json")
    log("=" * 62)
    if not args.so_plano:
        log("")
        log(" Agora:   py sincronizar.py --capcut")
        log("          py b.py")


if __name__ == "__main__":
    main()
