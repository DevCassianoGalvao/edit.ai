#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sincronizar.py — casa as pastas "paragrafo NN" (do buscador-imagens.html)
com os tempos reais da narracao, usando o seu arquivo .srt.

Aceita IMAGEM e VIDEO misturados na mesma pasta "paragrafo NN" (o buscador
agora tambem baixa video do Pexels Video e do Pixabay Video). Um video que
seja mais curto que o tempo que sobrou pra ele fica em leve camera lenta
ou repete em loop pra preencher o trecho - isso e feito no --capcut (modo
principal); no modo rapido sem --capcut, um video curto so toca uma vez.

Como usar:
  1. Coloque na mesma pasta:
        sincronizar.py
        roteiro.txt      (o MESMO texto que voce colou no buscador)
        legenda.srt      (a sincronizacao do audio)
        downloads/       (pasta gerada pelo servidor.py)
        narracao.mp3     (o audio, opcional - so para renderizar)

  2. Rode:
        python sincronizar.py --chars 400

     O --chars precisa ser o MESMO valor de "caracteres por parte"
     que voce usou no buscador. O padrao do buscador costuma ser 400.

  3. Ele gera:
        mapa.csv        -> tabela pasta / inicio / fim / duracao
        concat.txt      -> lista pronta para o ffmpeg
        comando.txt     -> o comando ffmpeg para montar o video

Nao precisa instalar nada (so biblioteca padrao do Python 3).
"""

import argparse
import csv
import difflib
import json
import os
import re
import sys

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".avif", ".tiff")
VID_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi", ".mpeg", ".3gp")
MEDIA_EXT = IMG_EXT + VID_EXT


def eh_video(caminho):
    return os.path.splitext(caminho)[1].lower() in VID_EXT


# ---------------------------------------------------------------- roteiro ---
def split_by_chars(text, max_chars):
    """Porta fiel da funcao splitByChars() do buscador-imagens.html."""
    clean = re.sub(r"\r\n?", "\n", text)
    clean = re.sub(r"[ \t]+", " ", clean)
    clean = re.sub(r"\n{2,}", "\n", clean).strip()

    n = len(clean)
    parts = []
    min_cut = max_chars // 2
    i = 0

    while i < n:
        end = min(i + max_chars, n)

        if end < n:
            window = clean[i:end]
            cut = -1
            for k in range(len(window) - 1, -1, -1):
                c = window[k]
                if c in ".!?…" and (k + 1 >= len(window) or window[k + 1].isspace()):
                    cut = k
                    break
            if cut >= min_cut:
                end = i + cut + 1
            else:
                sp = max(window.rfind(" "), window.rfind("\n"))
                if sp >= min_cut:
                    end = i + sp

        chunk = clean[i:end].strip()
        if chunk:
            parts.append(chunk)
        i = end
        while i < n and clean[i] in " \n":
            i += 1

    return parts


# -------------------------------------------------------------------- srt ---
def parse_time(s):
    s = s.strip().replace(".", ",")
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000.0


def parse_srt(path):
    """Devolve uma lista de (inicio, fim, texto)."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        raw = f.read()
    raw = re.sub(r"\r\n?", "\n", raw)

    cues = []
    for block in re.split(r"\n{2,}", raw.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        idx = 0
        if re.fullmatch(r"\d+", lines[0].strip()):
            idx = 1
        if idx >= len(lines):
            continue
        m = re.search(r"([\d:,.]+)\s*-->\s*([\d:,.]+)", lines[idx])
        if not m:
            continue
        texto = " ".join(lines[idx + 1:])
        texto = re.sub(r"<[^>]+>", "", texto)          # tira tags
        texto = re.sub(r"\{[^}]*\}", "", texto)
        cues.append((parse_time(m.group(1)), parse_time(m.group(2)), texto.strip()))

    return cues


def normalize(word):
    w = word.lower()
    w = re.sub(r"[^0-9a-zà-öø-ÿ]+", "", w)
    return w


def srt_word_times(cues):
    """Explode as legendas em palavras, cada uma com o seu instante estimado."""
    palavras, tempos = [], []
    for ini, fim, texto in cues:
        ws = [w for w in (normalize(x) for x in texto.split()) if w]
        if not ws:
            continue
        dur = max(fim - ini, 0.001)
        passo = dur / len(ws)
        for j, w in enumerate(ws):
            palavras.append(w)
            tempos.append(ini + j * passo)
    return palavras, tempos


# ---------------------------------------------------------------- alinhar ---
def alinhar_proporcional(partes, cues):
    """Alinhamento que NAO depende do idioma.

    A ideia: o SRT e o roteiro contam a mesma historia, na mesma ordem.
    Entao a posicao relativa vale mais que as palavras. Se a parte 3 comeca
    aos 40% do roteiro, ela comeca aos 40% do texto falado - e o SRT diz
    exatamente em que segundo isso acontece, respeitando as pausas reais.
    """
    # posicao acumulada de caracteres no SRT, com o tempo de cada trecho
    marcos = []          # (caracteres_acumulados, inicio, fim, tamanho)
    acumulado = 0
    for ini, fim, texto in cues:
        tam = max(len(re.sub(r"\s+", " ", texto).strip()), 1)
        marcos.append((acumulado, ini, fim, tam))
        acumulado += tam
    total_srt = max(acumulado, 1)

    tamanhos = [max(len(p), 1) for p in partes]
    total_roteiro = sum(tamanhos)

    def tempo_na_fracao(fracao):
        alvo = fracao * total_srt
        for base, ini, fim, tam in marcos:
            if alvo < base + tam:
                dentro = (alvo - base) / tam
                return ini + dentro * (fim - ini)
        return marcos[-1][2] if marcos else 0.0

    inicios = []
    percorrido = 0
    for tam in tamanhos:
        inicios.append(tempo_na_fracao(percorrido / total_roteiro))
        percorrido += tam

    for i in range(1, len(inicios)):
        if inicios[i] < inicios[i - 1]:
            inicios[i] = inicios[i - 1]

    return inicios


def alinhar(partes, srt_palavras, srt_tempos):
    """Descobre o instante em que a primeira palavra de cada parte e falada."""
    roteiro_palavras = []
    parte_da_palavra = []
    for i, p in enumerate(partes):
        for w in p.split():
            nw = normalize(w)
            if nw:
                roteiro_palavras.append(nw)
                parte_da_palavra.append(i)

    matcher = difflib.SequenceMatcher(None, roteiro_palavras, srt_palavras, autojunk=False)
    mapa = {}  # indice da palavra do roteiro -> indice no srt
    for a, b, size in matcher.get_matching_blocks():
        for k in range(size):
            mapa[a + k] = b + k

    # qualidade: quantas palavras do roteiro realmente casaram com o SRT
    qualidade = len(mapa) / len(roteiro_palavras) if roteiro_palavras else 0.0

    # primeiro instante conhecido de cada parte
    inicios = [None] * len(partes)
    for idx in sorted(mapa):
        parte = parte_da_palavra[idx]
        if inicios[parte] is None:
            inicios[parte] = srt_tempos[mapa[idx]]

    # partes sem nenhuma palavra reconhecida herdam o tempo da anterior
    ultimo = 0.0
    for i in range(len(inicios)):
        if inicios[i] is None:
            inicios[i] = ultimo
        else:
            ultimo = inicios[i]

    # garante ordem crescente
    for i in range(1, len(inicios)):
        if inicios[i] < inicios[i - 1]:
            inicios[i] = inicios[i - 1]

    return inicios, qualidade


# ---------------------------------------------------------------- imagens ---
def imagens_da_pasta(base, numero):
    # Aceita "paragrafo 01", "paragrafo 1", "Paragrafo 1", "parágrafo 01"...
    alvo = None
    if os.path.isdir(base):
        for nome in os.listdir(base):
            m = re.fullmatch(r"par[aá]grafo[\s_-]*0*(\d+)", nome.strip(), re.IGNORECASE)
            if m and int(m.group(1)) == numero:
                alvo = os.path.join(base, nome)
                break

    if not alvo:
        return os.path.join(base, "paragrafo %02d" % numero), []

    arquivos = [f for f in os.listdir(alvo) if f.lower().endswith(MEDIA_EXT)]

    def ordem(nome):
        # o buscador salva as imagens com sufixo "-1", "-2", ... na ordem da tela
        m = re.search(r"-(\d+)(?:_\d+)?\.[^.]+$", nome)
        return (int(m.group(1)) if m else 999, nome.lower())

    arquivos.sort(key=ordem)
    return alvo, [os.path.join(alvo, f) for f in arquivos]


# ------------------------------------------------------------- motion graphics --
# O editor de motion graphics grava a instrucao no nome do arquivo. Ler dali
# evita um arquivo de configuracao a parte, que so teria como dar errado.
RX_MOTION = re.compile(r"^00_motion_(parte|fila|(\d+)_(\d+)s)_", re.IGNORECASE)


def separar_motion(caminhos):
    """
    Devolve (cena, modo, segundos, resto).
      modo 'parte' -> a cena ocupa o trecho inteiro (resto fica de fora)
      modo 'inicio'-> a cena reserva 'segundos' no comeco
      modo 'fila'  -> nao separa nada, a cena divide igual com as outras
    """
    cena = None
    modo = None
    segundos = 0.0
    resto = []
    for c in caminhos:
        m = RX_MOTION.match(os.path.basename(c))
        if m and cena is None:
            marca = m.group(1).lower()
            if marca == "parte":
                cena, modo = c, "parte"
            elif marca == "fila":
                resto.append(c)          # entra na fila como qualquer midia
            else:
                cena, modo = c, "inicio"
                segundos = float("%s.%s" % (m.group(2), m.group(3)))
            continue
        resto.append(c)
    return cena, modo, segundos, resto


ASSINATURAS = (
    (b"\xff\xd8\xff", "jpg"),
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"BM", "bmp"),
    (b"II*\x00", "tiff"),
    (b"MM\x00*", "tiff"),
)

TEM_FFMPEG = None


def ffmpeg_disponivel():
    global TEM_FFMPEG
    if TEM_FFMPEG is None:
        import shutil
        TEM_FFMPEG = shutil.which("ffmpeg") is not None
    return TEM_FFMPEG


def validar_imagem(caminho):
    """Devolve (ok, motivo). Descarta arquivos vazios, truncados ou corrompidos."""
    try:
        tamanho = os.path.getsize(caminho)
    except OSError:
        return False, "nao consegui ler o arquivo"

    if tamanho == 0:
        return False, "arquivo vazio (0 KB)"
    if tamanho < 1024:
        return False, "arquivo minusculo (%d bytes) - download incompleto" % tamanho

    try:
        with open(caminho, "rb") as f:
            cabeca = f.read(16)
            f.seek(-2, os.SEEK_END)
            cauda = f.read(2)
    except OSError:
        return False, "nao consegui ler o arquivo"

    tipo = None
    for assinatura, nome in ASSINATURAS:
        if cabeca.startswith(assinatura):
            tipo = nome
            break
    if tipo is None:
        if cabeca[:4] == b"RIFF" and cabeca[8:12] == b"WEBP":
            tipo = "webp"
        elif b"ftyp" in cabeca:
            tipo = "avif"
        elif cabeca.lstrip()[:5] in (b"<?xml", b"<svg "):
            return False, "e um SVG - o CapCut nao usa"
        elif cabeca.lstrip()[:1] == b"<":
            return False, "e uma pagina HTML, nao uma imagem"

    if tipo is None:
        return False, "formato irreconhecivel - arquivo corrompido"

    # GIF: a biblioteca do CapCut trata como video animado e engasga.
    # Melhor descartar aqui, onde o tempo e redistribuido direitinho.
    if tipo == "gif":
        return False, "GIF - o CapCut nao aceita"

    # JPEG completo sempre termina com FFD9; se nao terminar, veio truncado
    if tipo == "jpg" and cauda != b"\xff\xd9":
        return False, "JPEG truncado - download interrompido"

    # Teste definitivo: tenta realmente decodificar a imagem
    if ffmpeg_disponivel():
        import subprocess
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", caminho, "-frames:v", "1",
             "-f", "null", "-"],
            capture_output=True,
        )
        if r.returncode != 0:
            return False, "nao abre (imagem danificada)"

    return True, ""


def validar_video(caminho):
    """Devolve (ok, motivo). Confere se o arquivo de video baixado e valido
    de verdade (nao e uma pagina de erro, nao esta truncado, o ffmpeg
    consegue abrir e ler pelo menos 1 quadro)."""
    try:
        tamanho = os.path.getsize(caminho)
    except OSError:
        return False, "nao consegui ler o arquivo"

    if tamanho == 0:
        return False, "arquivo vazio (0 KB)"
    if tamanho < 4096:
        return False, "arquivo minusculo (%d bytes) - download incompleto" % tamanho

    try:
        with open(caminho, "rb") as f:
            cabeca = f.read(32)
    except OSError:
        return False, "nao consegui ler o arquivo"

    if cabeca.lstrip()[:1] == b"<":
        return False, "e uma pagina HTML, nao um video (link protegido/quebrado)"

    if not ffmpeg_disponivel():
        # sem ffmpeg nao da pra confirmar que abre de verdade - aceita pelo
        # tamanho/cabecalho, que ja pega a maioria dos casos quebrados
        return True, ""

    import subprocess
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", caminho, "-frames:v", "1",
         "-f", "null", "-"],
        capture_output=True,
    )
    if r.returncode != 0:
        return False, "nao abre (video danificado)"
    return True, ""


def validar_midia(caminho):
    """Escolhe o validador certo conforme a extensao (imagem ou video)."""
    if eh_video(caminho):
        return validar_video(caminho)
    return validar_imagem(caminho)


def progresso(atual, total, rotulo):
    largura = 30
    fracao = atual / total if total else 1.0
    cheio = int(largura * fracao)
    barra = "#" * cheio + "-" * (largura - cheio)
    # O console do Windows e cp1252 e nao escreve caractere chines, japones nem
    # cirilico. Um arquivo chamado "SZ 深圳 Shenzhen.jpg" derrubava a geracao
    # INTEIRA com UnicodeEncodeError - 252 clipes perdidos por causa de uma
    # barra de progresso. Mostrar o nome e conveniencia; renderizar e o
    # trabalho. O que nao couber no console vira "?".
    try:
        sys.stdout.write("\r   [%s] %d/%d  %s" % (barra, atual, total, rotulo))
    except UnicodeEncodeError:
        cod = getattr(sys.stdout, "encoding", None) or "ascii"
        seguro = str(rotulo).encode(cod, "replace").decode(cod, "replace")
        sys.stdout.write("\r   [%s] %d/%d  %s" % (barra, atual, total, seguro))
    sys.stdout.flush()
    if atual >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()


def montar_video(caminho_audio, saida):
    """Monta o video final (imagens + narracao) direto, sem editor no meio."""
    import subprocess

    if not ffmpeg_disponivel():
        print(" ! ffmpeg nao encontrado.")
        return False
    if not caminho_audio or not os.path.exists(caminho_audio):
        print(" ! nao achei o audio para grudar no video.")
        return False

    cmd = [
        "ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-stats",
        "-f", "concat", "-safe", "0", "-i", "concat.txt",
        "-i", caminho_audio,
        "-vf", ("scale=1920:1080:force_original_aspect_ratio=increase,"
                "crop=1920:1080,fps=30,format=yuv420p"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-threads", "4",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", saida,
    ]
    print(" Montando %s ..." % saida)
    print(" (isso demora - o ffmpeg vai mostrando o andamento abaixo)")
    print()
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print()
        print(" ! o ffmpeg falhou ao montar o video.")
        return False

    dur = duracao_audio(saida)
    print()
    print("=" * 60)
    print(" VIDEO PRONTO: %s" % os.path.abspath(saida))
    if dur:
        print(" Duracao: %s" % hms(dur))
    print("=" * 60)
    return True


def montar_video(caminho_concat, caminho_audio, saida, dur_total):
    """Monta o video final (imagens + audio) sem depender de editor nenhum."""
    import subprocess

    if not ffmpeg_disponivel():
        print(" ! ffmpeg nao encontrado.")
        return False

    af = ""
    if caminho_audio:
        print(" Medindo o loudness da narracao...")
        af = filtro_loudness(caminho_audio)

    cmd = [
        "ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
        "-progress", "pipe:1",
        "-f", "concat", "-safe", "0", "-i", caminho_concat,
    ]
    if caminho_audio:
        cmd += ["-i", caminho_audio]
    cmd += [
        "-vf", ("scale=1920:1080:force_original_aspect_ratio=increase,"
                "crop=1920:1080,fps=30,format=yuv420p"),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
    ]
    if caminho_audio:
        if af:
            cmd += ["-af", af]
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += [saida]

    print(" Montando %s ..." % saida)
    print(" Isso demora: conte uns 2 a 5 minutos por 10 minutos de video.")

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    total_ms = max(dur_total, 1) * 1000000
    try:
        for linha in proc.stdout:
            if linha.startswith("out_time_ms="):
                try:
                    feito = int(linha.split("=", 1)[1])
                except ValueError:
                    continue
                progresso(min(feito, int(total_ms)), int(total_ms), "montando")
    except KeyboardInterrupt:
        proc.kill()
        print("\n Cancelado.")
        return False

    proc.wait()
    progresso(1, 1, "concluido")
    if proc.returncode != 0:
        print(" ! o ffmpeg reclamou:")
        print(proc.stderr.read()[:800])
        return False
    return True



# ---------------------------------------------------------------- movimento ---
# Movimento das fotos. Nenhuma imagem fica parada, e duas seguidas nunca fazem
# o mesmo movimento - a lista roda conforme a posicao da imagem na sequencia.
MOVIMENTOS = [
    ("aproxima",       "zoom lento pra dentro"),
    ("corre_direita",  "camera correndo pra direita"),
    ("afasta",         "zoom lento pra fora"),
    ("corre_esquerda", "camera correndo pra esquerda"),
    # Era "aproxima_alto" (zoom E subida ao mesmo tempo). Saiu porque combinar
    # duas grandezas quantizadas compoe o erro das duas: media pico 2,11, o
    # pior dos seis. E no quadro 0 o zoom vale 1,0, ou seja margem vertical
    # ZERO - a subida inteira ficava espremida no fim do clipe.
    # A diagonal com zoom FIXO se comporta como os pans, que sao os movimentos
    # mais lisos: pico 1,37.
    ("diagonal_sobe",  "corre pra direita subindo"),
    ("corre_baixo",    "desce devagar"),
]

# Quanto a imagem chega a ser ampliada. 12% e o ponto em que o movimento se
# percebe sem que a foto perca definicao nem pareca "zoom de novela".
ZOOM_MAX = 1.12

# Amplia antes de mover: o zoompan anda de pixel em pixel, e num 1920x1080 isso
# aparece como tremor. Em 3840 cada passo vira meio pixel na tela final.
# Largura em que o movimento acontece, antes de voltar para 1920.
#
# O `zoompan` posiciona o recorte em pixel INTEIRO da imagem de trabalho. Quanto
# maior essa imagem, menor o passo minimo na tela final - e o passo minimo e o
# que se ve como "soluco": um quadro que anda o dobro dos vizinhos.
#
# 5760 nao e um numero redondo qualquer: e 3 x 1920 EXATO. Com essa proporcao
# inteira, cada pixel de trabalho vale um terco de pixel na tela e os passos
# caem sempre no mesmo lugar. Medido num pan de 90 quadros (pico/mediana da
# diferenca entre quadros; 1,00 seria movimento perfeitamente constante):
#
#     3840 (antes)   tremor 0,22   pico 1,52   <- um quadro anda 50% mais
#     5760           tremor 0,17   pico 1,05
#     7680           tremor 0,14   pico 1,23   <- PIOR que 5760, e mais caro
#
# O 7680 ser pior que o 5760 e a prova de que o que manda aqui e a proporcao
# inteira com 1920, nao o tamanho bruto. Custo: +27% por clipe, que a geracao
# em paralelo absorve. Nitidez medida: identica.
LARGURA_TRABALHO = 5760

# ...menos para os movimentos VERTICAIS, que precisam de mais.
#
# O quadro e 16:9, entao a imagem de trabalho tem menos altura que largura - e
# o percurso que sobra para andar tambem. Com zoom de 1,12 em 5760x3240:
#
#     percurso horizontal   617 px
#     percurso VERTICAL     347 px      <- pouco mais da metade
#
# Como os dois percursos sao feitos no MESMO numero de quadros, o movimento
# vertical anda na metade da velocidade do horizontal - e bate no piso do
# pixel inteiro em dobro. Era por isso que, dos seis movimentos, exatamente os
# dois verticais saiam travados:
#
#     aproxima         pico 1,46        corre_esquerda   pico 1,52
#     corre_direita    pico 1,52        aproxima_alto    pico 2,11   <--
#     afasta           pico 1,59        corre_baixo      pico 2,02   <--
#
# 7680 de largura da 4320 de altura - que e 4 x 1080 EXATO, a mesma propriedade
# que faz o 5760 funcionar no horizontal - e leva o percurso vertical a 463 px.
# Medido no pan vertical: pico 2,02 -> 1,04.
#
# E por que nao usar 7680 em tudo? Porque no HORIZONTAL ele e pior (pico 1,23
# contra 1,05 do 5760) e mais caro. Cada eixo tem o seu ponto certo; usar um so
# numero para os dois era o erro.
# REVERTIDO PARA 5760. Eu tinha subido isto para 7680 depois de medir o pan
# vertical numa foto de carro, onde o pico caiu de 2,02 para 1,04. O erro foi
# generalizar a partir de UMA imagem. Medindo de novo, noutra foto:
#
#     corre_baixo @5760   2,4 s   pico 2,00
#     corre_baixo @7680  28,8 s   pico 2,07     <- pior E doze vezes mais lento
#
# O ganho de fluidez nao se sustenta entre imagens; o custo se sustenta sempre.
# Subir para 7680 obriga o `scale` a levar cada quadro a 7680x4320 antes do
# zoompan - e a mesma armadilha que o BENCHMARKS da ferramenta irma ja tinha
# documentado ("prescale para 4K com lanczos antes do zoompan: mais de dois
# minutos para seis segundos").
#
# O preco apareceu na pratica: com 6 processos em paralelo, quatro clipes
# estouraram o limite de 90 s e nao foram gerados.
LARGURA_TRABALHO_VERTICAL = LARGURA_TRABALHO
MOVIMENTOS_VERTICAIS = ("diagonal_sobe", "corre_baixo")


# Quanto da curva e "ease" e quanto e velocidade constante.
#
# O smoothstep PURO (o que estava aqui) tem velocidade ZERO nas duas pontas -
# e essa era a causa do tremido. O `zoompan` posiciona o recorte em pixel
# INTEIRO: quando a velocidade cai perto de zero, a imagem fica parada dois ou
# tres quadros e depois pula um pixel de uma vez. Medido num pan de 60 quadros,
# o perfil de diferenca entre quadros saia assim:
#
#     0.06  1.15  0.07  1.15  0.08  1.16      <- parado, pulo, parado, pulo
#
# Ampliar para 3840 antes do movimento (o que o codigo ja fazia) reduz o
# tamanho do pulo pela metade, mas nao resolve: o problema nao e o TAMANHO do
# passo, e a imagem ESTACIONAR entre um passo e outro.
#
# Misturando um quarto de smoothstep com tres quartos de velocidade constante,
# a camera continua acelerando e freando de forma visivel, mas a velocidade
# nunca cai abaixo de ~60% da media - entao nunca ha dois quadros iguais.
#
# Medido no mesmo pan (tremor = desvio/media da diferenca entre quadros; menor
# e mais fluido):
#
#     smoothstep puro (antes)   tremor 0,44   2 quadros travados   vel.min  0%
#     25% ease + 75% linear     tremor 0,15   0 travados          vel.min 60%
#     linear puro               tremor 0,14   0 travados          vel.min 84%
#
# Linear puro e marginalmente mais liso, mas comeca e termina no susto - que
# foi o motivo de existir o smoothstep. 0,15 com ease e o melhor dos dois.
PESO_EASE = 0.25


def _curva(n):
    """Posicao do movimento no quadro `on`, de 0 a 1.

    Ease suficiente para a camera nao comecar nem parar no susto, velocidade
    constante suficiente para o zoompan nunca repetir a mesma posicao inteira
    em dois quadros seguidos. Ver o comentario de PESO_EASE acima.
    """
    t = "(on/%d)" % max(n - 1, 1)
    smooth = "(%s*%s*(3-2*%s))" % (t, t, t)
    return "(%.2f*%s+%.2f*%s)" % (PESO_EASE, smooth, 1 - PESO_EASE, t)


def expressao_movimento(nome, quadros):
    """Devolve (z, x, y) prontos para o zoompan."""
    P = _curva(quadros)
    zfixo = "%.4f" % ZOOM_MAX
    centro_x = "iw/2-(iw/zoom/2)"
    centro_y = "ih/2-(ih/zoom/2)"
    # com zoom fixo, a sobra que da pra percorrer de um lado ao outro
    sobra_x = "(iw-iw/zoom)"
    sobra_y = "(ih-ih/zoom)"

    if nome == "aproxima":
        return ("1+%.4f*%s" % (ZOOM_MAX - 1, P), centro_x, centro_y)
    if nome == "afasta":
        return ("%s-%.4f*%s" % (zfixo, ZOOM_MAX - 1, P), centro_x, centro_y)
    if nome == "corre_direita":
        return (zfixo, "%s*%s" % (sobra_x, P), "%s/2" % sobra_y)
    if nome == "corre_esquerda":
        return (zfixo, "%s*(1-%s)" % (sobra_x, P), "%s/2" % sobra_y)
    if nome == "diagonal_sobe":
        return (zfixo, "%s*%s" % (sobra_x, P), "%s*(1-%s)" % (sobra_y, P))
    if nome == "corre_baixo":
        return (zfixo, "%s/2" % sobra_x, "%s*%s" % (sobra_y, P))
    return ("1", centro_x, centro_y)


def filtro_imagem_com_movimento(dur, fps, indice):
    """
    A cadeia inteira para uma foto:
      1. preenche 1920x1080 exato (corta o que sobra, nunca deixa tarja)
      2. amplia pra 3840 (o passo do zoompan vira meio pixel)
      3. move
      4. volta pra 1920x1080
    """
    quadros = max(int(round(dur * fps)), 2)
    nome = MOVIMENTOS[indice % len(MOVIMENTOS)][0]
    z, x, y = expressao_movimento(nome, quadros)
    # Movimento vertical anda menos, entao precisa de mais imagem embaixo dele.
    # Ver o comentario de LARGURA_TRABALHO_VERTICAL.
    largura = (LARGURA_TRABALHO_VERTICAL if nome in MOVIMENTOS_VERTICAIS
               else LARGURA_TRABALHO)
    return (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,"
        "scale=%d:-2:flags=lanczos,"
        "zoompan=z='%s':x='%s':y='%s':d=%d:s=1920x1080:fps=%d,"
        "setsar=1,format=yuv420p" % (largura, z, x, y, quadros, fps)
    ), nome


def _renderizar_item(caminho, dur, destino, fps=30, limite=90, indice=0,
                     movimento=True):
    """Gera um clipe de 'dur' segundos EXATOS a partir de UM item (imagem
    parada ou video). Se for video mais curto que 'dur', repete (loop) até
    preencher o tempo certinho, sem precisar saber a duração real dele com
    antecedência. Devolve True/False (conseguiu ou não)."""
    import subprocess

    quadros = max(int(round(dur * fps)), 2)

    vf = ("scale=1920:1080:force_original_aspect_ratio=increase,"
          "crop=1920:1080,fps=%d,format=yuv420p" % fps)
    if eh_video(caminho):
        # Tira a borda queimada nos pixels ANTES de reampliar. Reupload de
        # YouTube costuma vir com o conteudo dentro de uma moldura preta; sem
        # isto o scale=increase amplia a moldura junto e a tela sai com tarja.
        borda = detectar_borda(caminho)
        vf_v = (borda + "," + vf) if borda else vf
        cmd = [
            "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-stream_loop", "-1", "-i", caminho,
            "-t", "%.4f" % dur,
            "-vf", vf_v, "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            destino,
        ]
    else:
        # Foto: entra com movimento. Video nao - ele ja se move sozinho, e por
        # cima do movimento dele qualquer zoom fica enjoativo.
        if movimento:
            vf_img, _ = filtro_imagem_com_movimento(dur, fps, indice)
        else:
            vf_img = vf
        cmd = [
            "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-loop", "1", "-i", caminho,
            "-vf", vf_img,
            "-frames:v", str(quadros),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            destino,
        ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=limite)
        if r.returncode != 0:
            return False
    except subprocess.TimeoutExpired:
        if os.path.exists(destino):
            try:
                os.remove(destino)
            except OSError:
                pass
        return False

    # "-frames:v N" e "-t S" sao TETOS, nao garantias: se a fonte acaba antes,
    # o clipe sai curto e o ffmpeg nao avisa. Confere o que NOS geramos e, se
    # faltou, refaz segurando o ultimo quadro ate a duracao exata.
    tem = contar_frames(destino)
    if 0 <= tem < quadros - 1:
        falta = (quadros - tem) / fps
        if falta <= 3.05:  # acima disto o congelamento e defeito visivel
            base = cmd[cmd.index("-vf") + 1]
            cmd_rep = list(cmd)
            cmd_rep[cmd.index("-vf") + 1] = (
                base + ",tpad=stop_mode=clone:stop_duration=%.3f" % dur)
            if "-frames:v" not in cmd_rep:
                cmd_rep[-1:-1] = ["-frames:v", str(quadros)]
            try:
                subprocess.run(cmd_rep, capture_output=True, timeout=limite * 2)
            except subprocess.TimeoutExpired:
                pass
    return os.path.exists(destino) and os.path.getsize(destino) > 1024


def gerar_clipes_por_parte(blocos, pasta_saida, limite=300, movimento=True):
    """Gera UM mp4 por paragrafo, com as imagens/videos daquele trecho em
    sequencia. Menos arquivos = menos junções na linha do tempo = menos
    chance do editor comer tempo na importacao.

    Video real dentro do bloco vira antes um clipinho temporário de duração
    EXATA (com loop se for curto) - assim o concat do ffmpeg só junta peças
    que já têm o tamanho certo, sem depender do "duration" do concat demuxer
    pra esticar um video (isso não é confiável pra video de verdade, só pra
    imagem parada)."""
    import subprocess

    if not ffmpeg_disponivel():
        print(" ! ffmpeg nao encontrado.")
        return 0

    os.makedirs(pasta_saida, exist_ok=True)
    for antigo in os.listdir(pasta_saida):
        if re.fullmatch(r"\d{3}\.mp4", antigo):
            try:
                os.remove(os.path.join(pasta_saida, antigo))
            except OSError:
                pass

    fps = 30
    feitos = 0
    falhas = []
    lista_tmp = os.path.join(pasta_saida, "_lista.txt")
    tmp_dir = os.path.join(pasta_saida, "_tmp_video")

    for ordem, (numero, itens) in enumerate(blocos, 1):
        destino = os.path.join(pasta_saida, "%03d.mp4" % ordem)
        total = sum(d for _, d in itens)
        # arredonda para quadro inteiro sem acumular erro dentro do bloco
        quadros = round(total * fps)
        alvo = quadros / fps

        linhas_concat = []
        temporarios = []
        for idx, (caminho, dur) in enumerate(itens):
            os.makedirs(tmp_dir, exist_ok=True)
            # precisa ser ABSOLUTO: o concat demuxer do ffmpeg resolve
            # caminho relativo em relacao a pasta do PROPRIO _lista.txt,
            # nao em relacao a pasta onde o script esta rodando
            tmp = os.path.abspath(os.path.join(tmp_dir, "v_%03d_%03d.mp4" % (ordem, idx)))
            # Foto tambem passa pelo render agora: e ali que ela ganha o
            # movimento. Antes ela ia crua pro concat e ficava parada na tela.
            if _renderizar_item(caminho, dur, tmp, fps=fps, limite=limite,
                                indice=idx, movimento=movimento):
                linhas_concat.append((tmp, dur))
                temporarios.append(tmp)
            else:
                # nao processou -> usa o arquivo cru mesmo
                linhas_concat.append((caminho, dur))

        with open(lista_tmp, "w", encoding="utf-8") as f:
            for caminho, dur in linhas_concat:
                f.write("file '%s'\n" % caminho.replace("'", "'\\''"))
                f.write("duration %.4f\n" % dur)
            f.write("file '%s'\n" % linhas_concat[-1][0].replace("'", "'\\''"))

        cmd = [
            "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", lista_tmp,
            "-t", "%.4f" % alvo,
            "-vf", ("scale=1920:1080:force_original_aspect_ratio=increase,"
                    "crop=1920:1080,fps=30,format=yuv420p"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            destino,
        ]
        progresso(ordem, len(blocos), "paragrafo %02d (%d item)" % (numero, len(itens)))
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=limite)
            if r.returncode == 0:
                feitos += 1
            else:
                falhas.append((numero, "erro do ffmpeg"))
        except subprocess.TimeoutExpired:
            falhas.append((numero, "travou"))

        for tmp in temporarios:
            try:
                os.remove(tmp)
            except OSError:
                pass

    if os.path.exists(lista_tmp):
        try:
            os.remove(lista_tmp)
        except OSError:
            pass
    if os.path.isdir(tmp_dir):
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass

    for numero, motivo in falhas:
        print("   ! paragrafo %02d -> %s" % (numero, motivo))
    return feitos


def gerar_clipes_capcut(concat, pasta_saida, retomar=False, limite=90, movimento=True):
    """Transforma cada imagem/video num mini-video com a duracao exata.
    Assim, ao arrastar tudo de uma vez para o CapCut, os cortes ja vem prontos.
    Video mais curto que a duracao pedida repete em loop (via -stream_loop)
    ate preencher o tempo certinho."""
    import subprocess

    if not ffmpeg_disponivel():
        print(" ! ffmpeg nao encontrado. Instale-o para gerar os clipes do CapCut.")
        return 0

    os.makedirs(pasta_saida, exist_ok=True)
    # As copias LIMPAS que o overlays.py guarda sao de clipes ANTERIORES: se
    # ficarem aqui depois de um render novo, a proxima passada de overlay
    # restaura o clipe velho por cima do novo. Foi assim que 3,87s sumiram da
    # linha do tempo - a soma parava de bater com o audio e a unica pista era o
    # aviso de duracao no fim do overlays.py.
    if not retomar:
        for velho_limpo in os.listdir(pasta_saida):
            if velho_limpo.endswith(".limpo"):
                try:
                    os.remove(os.path.join(pasta_saida, velho_limpo))
                except OSError:
                    pass
    # limpa clipes de execucoes anteriores, senao sobram arquivos velhos na pasta
    for antigo in ([] if retomar else os.listdir(pasta_saida)):
        if re.fullmatch(r"\d{3}\.mp4", antigo):
            try:
                os.remove(os.path.join(pasta_saida, antigo))
            except OSError:
                pass

    # Ajusta cada duracao para um numero inteiro de quadros, sem acumular erro:
    # o arredondamento de um clipe e compensado no seguinte.
    fps = 30
    duracoes = []
    acumulado = 0.0
    quadros_gastos = 0
    for _, dur in concat:
        acumulado += dur
        quadros_alvo = round(acumulado * fps)
        duracoes.append(max(quadros_alvo - quadros_gastos, 1) / fps)
        quadros_gastos = quadros_alvo

    feitos = 0
    pulados = 0
    falhas = []
    falhou_idx = set()

    # --- fila de trabalho (o que realmente precisa ser gerado) ---
    fila = []
    for i, ((caminho, _), dur) in enumerate(zip(concat, duracoes), 1):
        destino = os.path.join(pasta_saida, "%03d.mp4" % i)
        if retomar and os.path.exists(destino) and os.path.getsize(destino) > 1024:
            feitos += 1
            pulados += 1
            continue
        fila.append((i, caminho, dur, destino))

    # Cada clipe e independente do outro - nada aqui depende da ordem, so a
    # NUMERACAO do arquivo, que ja vem calculada. Entao da para gerar varios ao
    # mesmo tempo, e o ganho e grande porque um ffmpeg sozinho nao usa a
    # maquina inteira: ele passa boa parte do tempo esperando disco e usando um
    # nucleo so.
    #
    # O numero de processos vem dos nucleos, com teto de 6: acima disso o
    # gargalo passa a ser compartilhado (disco e memoria) e o ganho some -
    # medido na ferramenta irma, 6 simultaneos deram 4,4x contra 1,7x de um so.
    try:
        trabalhadores = min(6, max(2, (os.cpu_count() or 4) - 1))
    except Exception:
        trabalhadores = 4
    if len(fila) < 4:
        trabalhadores = 1

    from concurrent.futures import ThreadPoolExecutor
    import threading
    _trava = threading.Lock()
    _feitos = [0]

    def tarefa(item):
        i, caminho, dur, destino = item
        ok = _renderizar_item(caminho, dur, destino, fps=fps, limite=limite,
                              indice=i - 1, movimento=movimento)
        with _trava:
            _feitos[0] += 1
            progresso(_feitos[0], len(fila), os.path.basename(caminho)[:28])
        return i, caminho, ok

    if fila:
        print("   Gerando %d clipe(s) com %d processo(s) ao mesmo tempo..."
              % (len(fila), trabalhadores))
        with ThreadPoolExecutor(max_workers=trabalhadores) as pool:
            for i, caminho, ok in pool.map(tarefa, fila):
                if ok:
                    feitos += 1
                else:
                    falhas.append((os.path.basename(caminho),
                                   "erro do ffmpeg (ou travou/passou de %ds)" % limite))
                    falhou_idx.add(i - 1)
        progresso(len(fila), len(fila), "concluido")

    # Se algum clipe falhou, a duracao dele nao pode simplesmente sumir,
    # senao tudo depois dele sai do sincronismo. Ela e somada ao vizinho.
    if falhas:
        print("   Compensando o tempo dos clipes que falharam...")
        for idx in sorted(falhou_idx):
            vizinho = None
            for j in range(idx - 1, -1, -1):
                if j not in falhou_idx:
                    vizinho = j
                    break
            if vizinho is None:
                for j in range(idx + 1, len(concat)):
                    if j not in falhou_idx:
                        vizinho = j
                        break
            if vizinho is None:
                continue

            duracoes[vizinho] += duracoes[idx]
            destino = os.path.join(pasta_saida, "%03d.mp4" % (vizinho + 1))
            try:
                _renderizar_item(concat[vizinho][0], duracoes[vizinho], destino,
                                  fps=fps, limite=limite * 2)
            except Exception:
                pass

    if pulados:
        print("   %d clipe(s) ja existiam e foram reaproveitados." % pulados)
    for nome, motivo in falhas:
        print("   ! pulei %s  ->  %s" % (nome, motivo))
    if falhas:
        print("   (a sincronia foi mantida: o tempo desses itens")
        print("    passou para o item anterior)")
    return feitos


def duracao_audio(caminho):
    """Le a duracao real do arquivo de audio com o ffprobe (se existir)."""
    if not caminho or not os.path.exists(caminho):
        return None
    import shutil
    import subprocess
    if shutil.which("ffprobe") is None:
        return None
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", caminho],
            capture_output=True, text=True, timeout=30,
        )
        return float(r.stdout.strip())
    except Exception:
        return None


# ---------------------------------------------------------------------------
# QUALIDADE DO ARQUIVO GERADO - tres cuidados que a 3.0 nao tinha e que a
# reescrita (pasta TESTE) provou serem necessarios:
#
#  1. "-frames:v N" e "no maximo N", nao "exatamente N". Se a fonte acaba
#     antes, o clipe sai curto e o ffmpeg nao reclama. Medido na outra
#     ferramenta: 60 frames sumiram numa montagem inteira. A saida: encodar,
#     conferir a contagem do que NOS geramos (o nb_frames da PROPRIA saida do
#     ffmpeg e confiavel), e so entao aceitar.
#  2. Material reenviado no YouTube costuma vir com o conteudo dentro de uma
#     moldura preta: o container diz 1920x1080 e metade daquilo e borda. Sem
#     recortar, a tela do video sai nao preenchida.
#  3. Normalizacao de loudness: a narracao de TTS chega baixa (~-19 LUFS) e o
#     YouTube normaliza para -14. loudnorm sozinho TRAVA em ~-15,6 em voz ja
#     limitada; o caminho e medir o integrado, aplicar o ganho que falta e
#     segurar os picos com um limitador de verdade.
# ---------------------------------------------------------------------------

ALVO_LUFS = -14.0
ALVO_TP = -1.5
# -1.5 dBTP em escala linear (10^(-1.5/20)); alimiter usa isto no 'limit'.
_TP_LINEAR = 0.841


def contar_frames(caminho):
    """Frames que o arquivo REALMENTE tem. Para um mp4 que o ffmpeg acabou de
    gerar, o nb_frames do cabecalho e confiavel e sai sem decodificar."""
    import shutil
    import subprocess
    if shutil.which("ffprobe") is None or not os.path.exists(caminho):
        return -1
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=nb_frames", "-of", "csv=p=0", caminho],
            capture_output=True, text=True, timeout=30,
        )
        # ffprobe as vezes devolve "5856," (virgula de campo vazio); le so o numero
        m = re.match(r"\s*(\d+)", r.stdout or "")
        return int(m.group(1)) if m else -1
    except Exception:
        return -1


_BORDA_CACHE = {}


def detectar_borda(caminho):
    """Retangulo de conteudo real dentro do quadro, como filtro 'crop=w:h:x:y',
    ou "" se o clipe ja preenche a tela. Resultado guardado por caminho."""
    if caminho in _BORDA_CACHE:
        return _BORDA_CACHE[caminho]
    _BORDA_CACHE[caminho] = ""
    if not ffmpeg_disponivel() or not os.path.exists(caminho):
        return ""
    import subprocess
    try:
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-ss", "2", "-t", "6",
             "-i", caminho, "-vf", "cropdetect=limit=24:round=2:reset=0",
             "-an", "-f", "null", "-"],
            capture_output=True, text=True, timeout=90,
        )
    except Exception:
        return ""
    achados = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", r.stderr or "")
    if not achados:
        return ""
    w, h, x, y = (int(v) for v in achados[-1])
    if w <= 0 or h <= 0:
        return ""
    # so vale a pena cortar se a borda for de verdade (>3% do quadro) e sobrar
    # imagem suficiente para reampliar sem destruir (<62% de perda).
    perda = 1 - (w * h) / (1920 * 1080)
    if perda < 0.03 or perda > 0.62:
        return ""
    w -= w % 2
    h -= h % 2
    filtro = "crop=%d:%d:%d:%d" % (w, h, x, y)
    _BORDA_CACHE[caminho] = filtro
    return filtro


def filtro_loudness(caminho_audio):
    """Mede o loudness integrado da narracao e devolve a cadeia de filtros de
    audio que a leva ao alvo da plataforma. Se a medicao falhar, cai para um
    loudnorm de passada unica (menos exato, mas nunca pior que nada)."""
    fallback = "loudnorm=I=%g:TP=%g:LRA=11" % (ALVO_LUFS, ALVO_TP)
    if not ffmpeg_disponivel() or not caminho_audio or not os.path.exists(caminho_audio):
        return fallback
    import subprocess
    try:
        r = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", caminho_audio,
             "-af", "loudnorm=I=%g:TP=%g:LRA=11:print_format=json" % (ALVO_LUFS, ALVO_TP),
             "-f", "null", "-"],
            capture_output=True, text=True, timeout=1800,
        )
    except Exception:
        return fallback
    err = r.stderr or ""
    ini, fim = err.rfind("{"), err.rfind("}")
    if ini == -1 or fim == -1 or fim < ini:
        return fallback
    try:
        medido = float(json.loads(err[ini:fim + 1])["input_i"])
    except Exception:
        return fallback
    if medido <= -70:  # silencio / medicao invalida
        return fallback
    ganho = round(ALVO_LUFS - medido, 2)
    print("   loudness medido: %.1f LUFS  ->  ganho %+.1f dB + limitador em %g dBTP"
          % (medido, ganho, ALVO_TP))
    return "volume=%.2fdB,alimiter=limit=%.3f" % (ganho, _TP_LINEAR)


def hms_curto(t):
    return "%d:%05.2f" % (int(t // 60), t % 60)


def hms(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return "%02d:%02d:%06.3f" % (h, m, s)


# ---------------------------------------------------------- fala por fala ---
def limites_de_fala(ini, fim, cues):
    """Instantes (dentro do intervalo) em que uma nova frase/deixa do SRT
    comeca. Sao as pausas REAIS da narracao - o lugar certo para cortar
    uma imagem e trocar para a proxima."""
    pontos = []
    for c_ini, c_fim, _ in cues:
        if ini < c_ini < fim:
            pontos.append(c_ini)
    return sorted(set(pontos))


def dividir_por_fala(ini, fim, k, cues):
    """Divide o intervalo [ini, fim) em k pedacos (um por imagem).

    Em vez de cortar em pontos igualmente espacados (que caem no meio de
    uma palavra sendo falada), cada corte e "imantado" para a deixa do SRT
    mais proxima. Assim a troca de imagem acontece numa pausa real da fala,
    nao num instante arbitrario da media."""
    total = max(fim - ini, 0.1)
    if k <= 1:
        return [total]

    alvos = [ini + j * (total / k) for j in range(1, k)]
    pontos = limites_de_fala(ini, fim, cues)

    cortes = []
    usados = set()
    janela = (total / k) * 0.6  # so imanta se a deixa estiver perto o bastante
    for alvo in alvos:
        candidatos = [p for p in pontos if p not in usados]
        escolhido = None
        if candidatos:
            melhor = min(candidatos, key=lambda p: abs(p - alvo))
            if abs(melhor - alvo) <= janela:
                escolhido = melhor
        cortes.append(escolhido if escolhido is not None else alvo)
        if escolhido is not None:
            usados.add(escolhido)

    limites = [ini] + sorted(cortes) + [fim]
    for i in range(1, len(limites)):
        if limites[i] <= limites[i - 1]:
            limites[i] = limites[i - 1] + 0.05

    return [limites[i + 1] - limites[i] for i in range(k)]


# ------------------------------------------------------------------- main ---
def verificar_clipes(pasta, caminho_audio):
    """Soma a duracao real dos clipes gerados e compara com o audio."""
    import glob
    arquivos = sorted(glob.glob(os.path.join(pasta, "*.mp4")))
    if not arquivos:
        print(" Nenhum clipe encontrado em %s/" % pasta)
        return

    print(" Medindo %d clipe(s) em %s/ ..." % (len(arquivos), pasta))
    total = 0.0
    curtos = []
    for i, f in enumerate(arquivos, 1):
        d = duracao_audio(f) or 0.0
        total += d
        if d < 0.4:
            curtos.append((os.path.basename(f), d))
        progresso(i, len(arquivos), "medindo")

    dur_audio = duracao_audio(caminho_audio)

    print()
    print("=" * 60)
    print(" Clipes na pasta   : %d" % len(arquivos))
    print(" Soma dos clipes   : %s" % hms(total))
    if dur_audio:
        print(" Duracao do audio  : %s" % hms(dur_audio))
        dif = dur_audio - total
        print(" Diferenca         : %+.2f s" % dif)
        print("=" * 60)
        if abs(dif) <= 1.0:
            print(" OS CLIPES ESTAO CERTOS.")
            print(" Se o video ficou curto no CapCut, o problema esta la:")
            print(" transicao automatica, clipes faltando na linha do tempo,")
            print(" ou algum clipe encurtado sem querer.")
        else:
            print(" OS CLIPES ESTAO ERRADOS - falta %s de video." % hms_curto(abs(dif)))
            print(" A pasta capcut/ e de uma execucao antiga.")
            print(" Apague a pasta capcut/ inteira e gere de novo,")
            print(" SEM usar --retomar.")
    else:
        print("=" * 60)
        print(" Nao achei o audio (%s) para comparar." % caminho_audio)
    if curtos:
        print("-" * 60)
        print(" Clipes muito curtos (podem sumir no CapCut):")
        for nome, d in curtos[:10]:
            print("   - %s  (%.2f s)" % (nome, d))
    print("=" * 60)


def abrir_para_escrever(caminho, **kw):
    """No Windows, um arquivo aberto no Excel fica bloqueado. Em vez de
    quebrar tudo, grava num nome alternativo e avisa."""
    try:
        return open(caminho, "w", **kw), caminho
    except PermissionError:
        base, ext = os.path.splitext(caminho)
        for n in range(2, 30):
            alternativo = "%s_%d%s" % (base, n, ext)
            try:
                f = open(alternativo, "w", **kw)
                print(" ! %s esta aberto em outro programa (Excel?)." % caminho)
                print("   Gravei em %s no lugar." % alternativo)
                return f, alternativo
            except PermissionError:
                continue
        raise


AUDIO_EXT = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma", ".mp4")


def achar_audio(preferido):
    """Usa o arquivo indicado; se nao existir, procura o maior audio da pasta."""
    if preferido and os.path.exists(preferido):
        return preferido, False

    candidatos = []
    for nome in os.listdir("."):
        if nome.lower().endswith(AUDIO_EXT) and os.path.isfile(nome):
            candidatos.append((os.path.getsize(nome), nome))
    if not candidatos:
        return None, False
    candidatos.sort(reverse=True)
    return candidatos[0][1], True


def contar_pastas(base):
    if not os.path.isdir(base):
        return 0
    n = 0
    for nome in os.listdir(base):
        if re.fullmatch(r"par[aá]grafo[\s_-]*0*\d+", nome.strip(), re.IGNORECASE):
            n += 1
    return n


def ler_partes_json(base):
    """Divisao exata gravada pelo buscador. E a fonte da verdade.

    O buscador-imagens.html grava "partes" como uma lista SIMPLES de textos,
    ja na ordem certa: {"charsPer": 650, "partes": ["texto 1", "texto 2", ...]}.
    (Versao antiga deste arquivo esperava uma lista de objetos {"n":.., "texto":..},
    formato que o buscador nunca produziu - por isso a leitura sempre falhava
    silenciosamente e o script recalculava a divisao do zero, na base do
    chute, gerando pastas fora de posicao com o roteiro.)
    """
    caminho = os.path.join(base, "partes.json")
    if not os.path.exists(caminho):
        return None, None
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        itens = dados.get("partes", [])
        if not itens:
            return None, None
        if isinstance(itens[0], dict):
            # compatibilidade com um formato antigo/alternativo, caso exista
            itens = sorted(itens, key=lambda x: x.get("n", 0))
            textos = [x.get("texto", "") for x in itens]
        else:
            # formato real gravado pelo buscador-imagens.html: lista de strings
            textos = [str(x) for x in itens]
        if not textos:
            return None, None
        return textos, dados.get("charsPer")
    except Exception:
        return None, None


def calibrar_chars(texto, alvo, chute):
    """Procura o valor de chars que produz exatamente 'alvo' partes.
    Usado quando nao existe partes.json (roteiros baixados antes)."""
    candidatos = []
    for c in range(80, 3001):
        if len(split_by_chars(texto, c)) == alvo:
            candidatos.append(c)
    if not candidatos:
        return None, []
    # prefere valores redondos (o usuario digitou algo tipo 400, 500, 1000)
    redondos = [c for c in candidatos if c % 100 == 0] or \
               [c for c in candidatos if c % 50 == 0]
    escolha = None
    if chute in candidatos:
        escolha = chute
    elif redondos:
        escolha = min(redondos, key=lambda c: abs(c - chute))
    else:
        escolha = min(candidatos, key=lambda c: abs(c - chute))
    return escolha, candidatos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roteiro", default="roteiro.txt")
    ap.add_argument("--srt", default="legenda.srt")
    ap.add_argument("--downloads", default="downloads")
    ap.add_argument("--audio", default="narracao.mp3")
    ap.add_argument("--chars", type=int, default=400,
                    help="mesmo valor de 'caracteres por parte' usado no buscador")
    ap.add_argument("--saida", default="video.mp4")
    ap.add_argument("--metodo", choices=["auto", "palavras", "proporcional"],
                    default="auto",
                    help="auto (padrao), palavras (mesmo idioma) ou proporcional "
                         "(roteiro e SRT em idiomas diferentes)")
    ap.add_argument("--verificar", action="store_true",
                    help="so mede os clipes ja gerados e compara com o audio")
    ap.add_argument("--qa", action="store_true",
                    help="so roda os portoes de qualidade sobre o video ja montado "
                         "(preto, congelado, loudness, deriva de sincronia)")
    ap.add_argument("--sem-qa", action="store_true",
                    help="nao roda o QA automatico depois do --montar")
    ap.add_argument("--retomar", action="store_true",
                    help="continua de onde parou, aproveitando os clipes ja gerados")
    ap.add_argument("--limite", type=int, default=90,
                    help="segundos maximos por clipe antes de desistir dele (padrao 90)")
    ap.add_argument("--montar", action="store_true",
                    help="monta o video final direto (imagens + narracao)")
    ap.add_argument("--porparagrafo", action="store_true",
                    help="gera UM clipe por paragrafo (menos arquivos, mais seguro)")
    ap.add_argument("--capcut", action="store_true",
                    help="gera a pasta capcut/ com um mini-video por imagem, ja cortado")
    ap.add_argument("--sem-movimento", action="store_true",
                    help="deixa as fotos paradas. Por padrao cada foto entra com um "
                         "movimento lento de camera (aproxima, afasta, corre pro lado), "
                         "alternando para que duas seguidas nunca facam o mesmo")
    args = ap.parse_args()

    if args.verificar:
        verificar_clipes("capcut", args.audio)
        return

    if args.qa:
        try:
            import qa
        except Exception as e:
            sys.exit("qa.py nao carregou: %s" % e)
        ok, _ = qa.rodar(args.saida, args.audio)
        sys.exit(0 if ok else 1)

    for caminho in (args.roteiro, args.srt):
        if not os.path.exists(caminho):
            sys.exit("Nao encontrei o arquivo: %s" % caminho)

    with open(args.roteiro, "r", encoding="utf-8-sig", errors="replace") as f:
        texto = f.read()

    # ---- de onde vem a divisao do roteiro ----
    pastas_existentes = contar_pastas(args.downloads)
    partes, chars_gravado = ler_partes_json(args.downloads)
    origem = ""

    if partes:
        origem = (" Divisao: partes.json (exata, gravada pelo buscador)%s"
                  % ("  [chars=%s]" % chars_gravado if chars_gravado else ""))
    else:
        partes = split_by_chars(texto, args.chars)
        origem = " Divisao: calculada com --chars %d" % args.chars

        if pastas_existentes and len(partes) != pastas_existentes:
            print()
            print(" O --chars %d gera %d partes, mas existem %d pastas."
                  % (args.chars, len(partes), pastas_existentes))
            print(" Calibrando automaticamente...")
            achado, todos = calibrar_chars(texto, pastas_existentes, args.chars)
            if achado:
                partes = split_by_chars(texto, achado)
                origem = (" Divisao: calibrada automaticamente para --chars %d\n"
                          " (%d valor(es) davam %d partes; usei o mais redondo)"
                          % (achado, len(todos), pastas_existentes))
                print(" Achei: --chars %d da exatamente %d partes."
                      % (achado, pastas_existentes))
            else:
                print(" Nao existe valor de --chars que gere %d partes."
                      % pastas_existentes)
                print(" O roteiro.txt provavelmente nao e igual ao que voce")
                print(" colou no buscador (texto editado, faltando ou sobrando).")

    cues = parse_srt(args.srt)
    if not cues:
        sys.exit("O arquivo .srt parece vazio ou em formato nao reconhecido.")

    srt_palavras, srt_tempos = srt_word_times(cues)

    if args.metodo == "proporcional":
        inicios = alinhar_proporcional(partes, cues)
        nota_metodo = " Metodo: proporcional (forcado)"
    else:
        inicios, qualidade = alinhar(partes, srt_palavras, srt_tempos)
        if args.metodo == "palavras":
            nota_metodo = " Metodo: palavras (forcado) - %.0f%% casou" % (qualidade * 100)
        elif qualidade < 0.45:
            inicios = alinhar_proporcional(partes, cues)
            nota_metodo = (
                " Metodo: proporcional\n"
                " (so %.0f%% das palavras do roteiro apareceram no SRT - eles\n"
                "  parecem estar em idiomas diferentes, entao usei a posicao\n"
                "  relativa no texto em vez de casar palavra por palavra)"
                % (qualidade * 100)
            )
        else:
            nota_metodo = " Metodo: palavras - %.0f%% casou" % (qualidade * 100)
    fim_total = cues[-1][1]

    # O SRT costuma terminar antes do audio (trilha, vinheta, silencio no fim).
    # Se for o caso, a ultima parte se estende ate o fim real da narracao,
    # senao o video sai mais curto que o audio.
    caminho_audio, achado_sozinho = achar_audio(args.audio)
    dur_audio = duracao_audio(caminho_audio)
    aviso_audio = ""
    if caminho_audio is None:
        aviso_audio = (
            " !!! NAO ACHEI NENHUM ARQUIVO DE AUDIO NESTA PASTA !!!\n"
            " Sem o audio eu nao sei onde a narracao termina, entao o video\n"
            " vai cobrir apenas ate o fim do SRT (%s).\n"
            " Copie a narracao para esta pasta e rode de novo." % hms_curto(fim_total)
        )
    elif dur_audio is None:
        aviso_audio = (" Achei %s mas nao consegui medir a duracao\n"
                       " (ffprobe faltando?). Usando o fim do SRT." % caminho_audio)
    else:
        rotulo = "%s (achado automaticamente)" % caminho_audio if achado_sozinho else caminho_audio
        if dur_audio > fim_total + 0.5:
            aviso_audio = (
                " Audio: %s -> %s\n"
                " O SRT termina %s ANTES do fim do audio.\n"
                " A ultima parte foi esticada para cobrir o audio inteiro."
                % (rotulo, hms_curto(dur_audio), hms_curto(dur_audio - fim_total))
            )
            fim_total = dur_audio
        elif dur_audio < fim_total - 0.5:
            aviso_audio = (" ATENCAO: o SRT vai ate %s, mas o audio so tem %s.\n"
                           " O SRT parece ser de outra versao da narracao."
                           % (hms_curto(fim_total), hms_curto(dur_audio)))
        else:
            aviso_audio = " Audio: %s -> %s (bate com o SRT)" % (rotulo, hms_curto(dur_audio))
    fins = inicios[1:] + [fim_total]

    linhas = []
    concat = []
    sem_imagem = []
    descartadas = []

    # --- 1) confere todas as imagens antes de montar a linha do tempo ---
    catalogo = []
    for i in range(len(partes)):
        _, imgs = imagens_da_pasta(args.downloads, i + 1)
        catalogo.append(imgs)

    if pastas_existentes and pastas_existentes != len(partes):
        print()
        print("!" * 60)
        print(" ATENCAO: o roteiro foi dividido em %d partes, mas existem" % len(partes))
        print(" %d pastas em %s/." % (pastas_existentes, args.downloads))
        print()
        print(" O --chars nao esta igual ao que voce usou no buscador.")
        if len(partes) > pastas_existentes:
            print(" Tente um valor MAIOR que %d." % args.chars)
        else:
            print(" Tente um valor MENOR que %d." % args.chars)
        print(" Sem isso, as imagens vao cair no trecho errado da fala.")
        print("!" * 60)

    total_imgs = sum(len(x) for x in catalogo)
    print()
    print(" Conferindo %d arquivo(s) de imagem/vídeo%s..."
          % (total_imgs, " com o ffmpeg" if ffmpeg_disponivel() else ""))
    checadas = 0
    validas = []
    for i, imgs in enumerate(catalogo):
        boas = []
        for caminho in imgs:
            ok, motivo = validar_midia(caminho)
            if ok:
                boas.append(caminho)
            else:
                descartadas.append(("paragrafo %02d" % (i + 1),
                                    os.path.basename(caminho), motivo))
            checadas += 1
            progresso(checadas, total_imgs, "conferindo imagens")
        validas.append(boas)

    # --- 2) monta a linha do tempo so com as imagens boas ---
    # Se uma parte nao tem imagem, o tempo dela NAO pode desaparecer, senao
    # o video fica mais curto que o audio. Ele e repassado para a proxima
    # parte que tiver imagem (ou para a anterior, se for no fim).
    sobra = 0.0
    pendente_ini = None   # inicio real da primeira parte "sem imagem" pendurada
    indice_ultimo_com_img = None
    blocos = []   # [(numero_do_paragrafo, [(caminho, duracao), ...]), ...]

    for i, parte in enumerate(partes):
        numero = i + 1
        ini, fim = inicios[i], fins[i]
        dur = max(fim - ini, 0.1)
        imgs = validas[i]

        if not imgs:
            sem_imagem.append(numero)
            sobra += dur
            if pendente_ini is None:
                pendente_ini = ini
            linhas.append({
                "pasta": "paragrafo %02d" % numero,
                "inicio": hms(ini),
                "fim": hms(fim),
                "duracao_s": round(dur, 3),
                "imagens": 0,
                "seg_por_imagem": "",
                "trecho": parte[:70].replace("\n", " ") + ("..." if len(parte) > 70 else ""),
            })
            continue

        dur_efetiva = dur + sobra
        ini_efetivo = pendente_ini if pendente_ini is not None else ini
        sobra = 0.0
        pendente_ini = None
        indice_ultimo_com_img = len(concat)

        # A cena de motion graphics, se houver, tem o tempo dela reservado
        # ANTES de dividir o que sobra entre as fotos.
        cena, modo_cena, seg_cena, fotos = separar_motion(imgs)
        bloco = []

        if cena and modo_cena == "parte":
            # a cena e o trecho inteiro; as fotos daquela pasta ficam de fora
            item = (os.path.abspath(cena), dur_efetiva)
            concat.append(item); bloco.append(item)
        elif cena and modo_cena == "inicio" and fotos:
            # nunca deixar a cena comer o trecho todo: no maximo 70% dele,
            # senao um valor digitado errado apaga as imagens da parte
            reserva = max(min(seg_cena, dur_efetiva * 0.7), 0.5)
            item = (os.path.abspath(cena), reserva)
            concat.append(item); bloco.append(item)
            duracoes_fotos = dividir_por_fala(ini_efetivo + reserva, fim, len(fotos), cues)
            for caminho, dur_img in zip(fotos, duracoes_fotos):
                it = (os.path.abspath(caminho), dur_img)
                concat.append(it); bloco.append(it)
        else:
            # sem cena reservada (ou cena em modo fila): divide igual, como antes
            todos = imgs if not cena else ([cena] + fotos)
            duracoes_imgs = dividir_por_fala(ini_efetivo, fim, len(todos), cues)
            for caminho, dur_img in zip(todos, duracoes_imgs):
                it = (os.path.abspath(caminho), dur_img)
                concat.append(it); bloco.append(it)

        blocos.append((numero, bloco))

        linhas.append({
            "pasta": "paragrafo %02d" % numero,
            "inicio": hms(ini),
            "fim": hms(fim),
            "duracao_s": round(dur_efetiva, 3),
            "imagens": len(imgs),
            "seg_por_imagem": round(dur_efetiva / len(imgs), 3),
            "trecho": parte[:70].replace("\n", " ") + ("..." if len(parte) > 70 else ""),
        })

    # sobrou tempo depois da ultima parte com imagem: vai para ela
    if sobra > 0 and indice_ultimo_com_img is not None:
        inicio_bloco = indice_ultimo_com_img
        qtd = len(concat) - inicio_bloco
        extra = sobra / qtd
        for k in range(inicio_bloco, len(concat)):
            concat[k] = (concat[k][0], concat[k][1] + extra)
        if blocos:
            numero_ult, bloco_ult = blocos[-1]
            blocos[-1] = (numero_ult,
                          [(c, d + extra) for c, d in bloco_ult])

    f, nome_mapa = abrir_para_escrever("mapa.csv", encoding="utf-8-sig", newline="")
    with f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)

    f, _ = abrir_para_escrever("mapa.json", encoding="utf-8")
    with f:
        json.dump(linhas, f, ensure_ascii=False, indent=2)

    f, _ = abrir_para_escrever("concat.txt", encoding="utf-8")
    with f:
        for caminho, dur in concat:
            f.write("file '%s'\n" % caminho.replace("'", "'\\''"))
            f.write("duration %.3f\n" % dur)
        if concat:
            f.write("file '%s'\n" % concat[-1][0].replace("'", "'\\''"))

    # linha do tempo em microssegundos, para o gerador de projeto do CapCut.
    # A duracao de cada item e a DIFERENCA entre o inicio dele e o do proximo.
    # Arredondar inicio e duracao separadamente criava sobreposicao de 1 us,
    # e o CapCut recusa o projeto por causa disso.
    fps_ref = 30
    idx_por_bloco = {}
    for numero, bloco in blocos:
        for caminho, _ in bloco:
            idx_por_bloco[os.path.abspath(caminho)] = numero

    inicios_us = []
    acum = 0.0
    for _, dur in concat:
        inicios_us.append(int(round(round(acum * fps_ref) / fps_ref * 1000000)))
        acum += dur
    fim_us = int(round(round(acum * fps_ref) / fps_ref * 1000000))

    itens_tl = []
    for i, (caminho, _) in enumerate(concat):
        proximo = inicios_us[i + 1] if i + 1 < len(inicios_us) else fim_us
        dur_us = max(proximo - inicios_us[i], 33333)
        itens_tl.append({
            "arquivo": caminho,
            "paragrafo": idx_por_bloco.get(caminho),
            "inicio_us": inicios_us[i],
            "duracao_us": dur_us,
        })

    f, _ = abrir_para_escrever("linha_do_tempo.json", encoding="utf-8")
    with f:
        json.dump({
            "fps": fps_ref,
            "largura": 1920,
            "altura": 1080,
            "audio": os.path.abspath(caminho_audio) if caminho_audio else None,
            "srt": os.path.abspath(args.srt),
            "duracao_total_us": int(round(fim_total * 1000000)),
            "itens": itens_tl,
        }, f, ensure_ascii=False, indent=2)

    # O -af leva a narracao para -14 LUFS (o alvo do YouTube). Aqui vai um
    # loudnorm de passada unica porque este comando e escrito sem medir o
    # audio; o --montar do proprio script mede antes e faz melhor.
    comando = (
        'ffmpeg -y -f concat -safe 0 -i concat.txt -i "%s" '
        '-vf "scale=1920:1080:force_original_aspect_ratio=increase,'
        'crop=1920:1080,fps=30,format=yuv420p" '
        '-af "loudnorm=I=-14:TP=-1.5:LRA=11" '
        '-c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -shortest "%s"'
        % (args.audio, args.saida)
    )
    f, _ = abrir_para_escrever("comando.txt", encoding="utf-8")
    with f:
        f.write(comando + "\n")

    print()
    print("=" * 60)
    print(" Partes do roteiro : %d" % len(partes))
    print(" Fim da linha      : %s" % hms(fim_total))
    print("-" * 60)
    print(origem)
    print(nota_metodo)
    print("-" * 60)
    if aviso_audio:
        print("-" * 60)
        print(aviso_audio)
        print("-" * 60)
    print(" Imagens boas      : %d de %d" % (len(concat), total_imgs))
    if descartadas:
        print(" Descartadas       : %d" % len(descartadas))
    if sem_imagem:
        lista = ", ".join(map(str, sem_imagem[:20]))
        if len(sem_imagem) > 20:
            lista += " ... (+%d)" % (len(sem_imagem) - 20)
        print(" SEM IMAGEM        : %d parte(s) -> %s" % (len(sem_imagem), lista))
        print("                     (o tempo delas foi repassado as vizinhas)")
    print("=" * 60)

    if descartadas:
        print(" Imagens ignoradas (nao entraram no video):")
        for pasta, nome, motivo in descartadas:
            print("   - %s / %s  ->  %s" % (pasta, nome, motivo))
        print("=" * 60)

    print(" Gerados: %s | mapa.json | concat.txt | comando.txt" % nome_mapa)

    if args.montar:
        print()
        ok = montar_video("concat.txt", caminho_audio, args.saida, fim_total)
        print()
        print("=" * 60)
        if ok:
            print(" PRONTO! Video montado: %s" % os.path.abspath(args.saida))
            print(" Duracao: %s - imagem e audio sincronizados." % hms(fim_total))
            print(" Abra esse arquivo no CapCut como uma peca so e coloque")
            print(" a legenda (legenda.srt) por cima.")
        else:
            print(" Nao consegui montar o video. Veja o erro acima.")
        print("=" * 60)
        if ok and not args.sem_qa:
            try:
                import qa
                qa.rodar(args.saida, caminho_audio or args.audio)
            except Exception as e:
                print(" (QA nao rodou: %s)" % e)
    elif args.capcut:
        print()
        print(" Gerando os clipes para o CapCut...")
        if args.porparagrafo:
            feitos = gerar_clipes_por_parte(blocos, "capcut",
                                            movimento=not args.sem_movimento)
        else:
            feitos = gerar_clipes_capcut(concat, "capcut",
                                         movimento=not args.sem_movimento,
                                         retomar=args.retomar, limite=args.limite)
        print()
        print("=" * 60)
        print(" CONCLUIDO! %d clipe(s) prontos na pasta capcut/" % feitos)
        print("=" * 60)
        print(" No CapCut: selecione TODOS os arquivos da pasta capcut/,")
        print(" arraste de uma vez para a linha do tempo e depois solte")
        print(" o audio da narracao na trilha de baixo. Fica sincronizado.")
    else:
        print()
        print(" CONCLUIDO! Para montar o video direto, rode:")
        print("   " + comando)
        print()
        print(" Ou rode com --capcut para gerar os clipes ja cortados.")
    print("=" * 60)


if __name__ == "__main__":
    main()
