# -*- coding: utf-8 -*-
"""
audio.py - camada de AUDIO E SINCRONIA do THANOS 3.0.

O problema que este arquivo resolve:

  Ate a 2.0, o roteiro era dividido por NUMERO DE CARACTERES (~700 por parte)
  e cada parte ganhava o mesmo tanto de imagem. Só que narracao nao e uniforme:
  um paragrafo de 700 caracteres pode levar 28 segundos e o seguinte, com o
  mesmo tamanho, levar 45 - porque tem pausa, enfase, respiracao. Resultado:
  imagem trocando fora do compasso da voz.

  Aqui a gente para de adivinhar. O audio da narracao e transcrito com o
  faster-whisper PALAVRA POR PALAVRA, e cada parte do roteiro e casada com o
  trecho falado correspondente. Dai sai o tempo REAL de cada parte - e com o
  tempo real da pra saber quantas imagens aquela parte aguenta e quanto tempo
  cada uma fica na tela.

Duas etapas:

  1. transcrever()     -> audio  ->  palavras com inicio e fim (com cache)
  2. alinhar_partes()  -> roteiro + palavras  ->  tempo real de cada parte

Precisa de: faster-whisper (ja instalado) e ffmpeg (ja instalado).
"""

import difflib
import hashlib
import json
import os
import re
import subprocess
import threading
import time
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, "downloads", "_transcricoes")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".opus")

_NOWIN = {}
if os.name == "nt":
    _si = subprocess.STARTUPINFO()
    _si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _NOWIN = {"startupinfo": _si, "creationflags": 0x08000000}


# ===========================================================================
# UTILITARIOS
# ===========================================================================
def duracao_audio(caminho):
    """Duracao real em segundos, pelo ffprobe."""
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", caminho],
            capture_output=True, timeout=40, **_NOWIN)
        return float((p.stdout or b"").decode("utf-8", "ignore").strip() or 0)
    except Exception:
        return 0.0


def _assinatura(caminho):
    """
    Identidade do arquivo pro cache. Nao le o arquivo inteiro (audio de 20MB+
    seria desperdicio): usa nome, tamanho e data de modificacao, mais os
    primeiros e ultimos 256KB - o suficiente pra nunca confundir dois audios.
    """
    st = os.stat(caminho)
    h = hashlib.md5()
    h.update(os.path.basename(caminho).encode("utf-8", "ignore"))
    h.update(str(st.st_size).encode())
    h.update(str(int(st.st_mtime)).encode())
    try:
        with open(caminho, "rb") as f:
            h.update(f.read(262144))
            if st.st_size > 524288:
                f.seek(-262144, os.SEEK_END)
                h.update(f.read(262144))
    except Exception:
        pass
    return h.hexdigest()[:16]


def normalizar(palavra):
    """Mesma normalizacao do sincronizar.py: minusculas, sem pontuacao."""
    w = unicodedata.normalize("NFC", str(palavra or "")).lower()
    return re.sub(r"[^0-9a-zà-öø-ÿ]+", "", w)


def listar_audios():
    """Audios que ja estao na pasta do projeto, do mais novo pro mais velho."""
    fora = []
    for nome in os.listdir(ROOT):
        if nome.lower().endswith(AUDIO_EXTS):
            caminho = os.path.join(ROOT, nome)
            if os.path.isfile(caminho):
                fora.append({
                    "nome": nome,
                    "tamanho": os.path.getsize(caminho),
                    "mtime": os.path.getmtime(caminho),
                    "transcrito": _tem_cache(caminho),
                })
    fora.sort(key=lambda a: a["mtime"], reverse=True)
    return fora


def _tem_cache(caminho_audio):
    """Ja existe transcricao deste audio com QUALQUER modelo?"""
    try:
        assinatura = _assinatura(caminho_audio)
    except Exception:
        return False
    if not os.path.isdir(CACHE):
        return False
    return any(n.startswith(assinatura + "_") for n in os.listdir(CACHE))


def _caminho_cache(caminho_audio, modelo="tiny"):
    """
    A chave do cache inclui o MODELO de proposito. Sem isso, transcrever com
    o "small" e depois pedir o "large-v3" devolvia o resultado do small sem
    avisar - a pessoa esperaria mais qualidade e receberia a antiga.
    """
    try:
        return os.path.join(CACHE, "%s_%s.json" % (_assinatura(caminho_audio),
                                                   re.sub(r"[^\w\-]", "", str(modelo))))
    except Exception:
        return os.path.join(CACHE, "sem_cache.json")


# ===========================================================================
# TRANSCRICAO
# ===========================================================================
# O modelo fica carregado entre chamadas: carregar o "small" leva uns 10s, e
# seria um desperdicio repetir isso a cada audio.
_modelos = {}
_trava_modelo = threading.Lock()

# Quantos caminhos o modelo explora antes de decidir a palavra.
# Medido nesta maquina, com 2 minutos da narracao real:
#     small beam=5 -> 122,7s   |   small beam=1 -> 78,9s
# ...e a transcricao saiu IDENTICA (mesmas 320 palavras, mesmo texto). Em
# narracao limpa de estudio, explorar 5 caminhos e so gastar 36% mais tempo
# pra chegar no mesmo lugar. O beam alto fica reservado pro large-v3, que e
# escolhido justamente por quem quer o maximo de qualidade e aceita esperar.
BEAM = {"tiny": 1, "small": 1, "medium": 1, "large-v3": 5, "large-v2": 5}

# POR QUE O PADRAO E O "tiny", E NAO UM MODELO MAIOR
#
# Aqui a transcricao nao existe pra virar legenda: existe pra dizer EM QUE
# SEGUNDO cada palavra foi falada. Se o modelo escrever "conteiner" no lugar de
# "contêiner", nada quebra - o difflib casa assim mesmo, e o tempo, que e o que
# interessa, e o mesmo.
#
# Medido nesta maquina, com 2 minutos da narracao real, tendo o small beam=5
# como referencia:
#
#     small  beam=5 : 123,0s  (1,0x tempo real)   320 palavras
#     small  beam=1 :  78,9s  (1,5x)              320 palavras, texto identico
#     tiny   beam=1 :  18,5s  (6,5x)              303 palavras
#                      -> casamento de 88% com a referencia
#                      -> desvio MEDIANO de tempo: 0,10 segundo
#
# 0,10s de desvio numa imagem que fica 5 segundos na tela e invisivel. E a
# diferenca pratica e enorme: um audio de 25 minutos sai em ~4 minutos com o
# tiny e em ~25 minutos com o small.
#
# Quem quiser a transcricao boa de texto (pra gerar legenda, por exemplo) troca
# o modelo no seletor da pagina - continua tudo disponivel.


def _carregar(nome_modelo):
    with _trava_modelo:
        if nome_modelo not in _modelos:
            from faster_whisper import WhisperModel
            # int8 na CPU: e o que faz caber em maquina normal sem placa de
            # video, com perda de qualidade que na pratica nao aparece em
            # narracao limpa de estudio.
            _modelos[nome_modelo] = WhisperModel(
                nome_modelo, device="cpu", compute_type="int8",
                cpu_threads=max(os.cpu_count() or 4, 2))
        return _modelos[nome_modelo]


def transcrever(caminho_audio, modelo="tiny", idioma=None, on_progresso=None,
                usar_cache=True):
    """
    Devolve:
      {"idioma", "duracao", "modelo",
       "palavras": [{"w": "china", "i": 0.42, "f": 0.71}, ...],
       "frases":   [{"t": "A China acaba...", "i": 0.0, "f": 6.4}, ...]}

    O cache e por conteudo do arquivo: trocar de audio refaz, reabrir o mesmo
    audio nao refaz nunca.
    """
    if not os.path.isfile(caminho_audio):
        raise FileNotFoundError("audio nao encontrado: %s" % caminho_audio)

    os.makedirs(CACHE, exist_ok=True)
    destino = _caminho_cache(caminho_audio, modelo)
    if usar_cache and os.path.isfile(destino):
        try:
            with open(destino, encoding="utf-8") as f:
                dados = json.load(f)
            if dados.get("palavras"):
                dados["do_cache"] = True
                if on_progresso:
                    on_progresso(1.0, "transcricao ja existia (cache)")
                return dados
        except Exception:
            pass

    total = duracao_audio(caminho_audio) or 0.0
    if on_progresso:
        on_progresso(0.0, "carregando o modelo %s..." % modelo)

    md = _carregar(modelo)
    # PyAV 19 removeu metadata_errors; FFmpeg entrega amostras compatíveis.
    import numpy as np
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho_audio, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True, **_NOWIN)
    segmentos, info = md.transcribe(
        np.frombuffer(decoded.stdout, dtype=np.float32),
        language=idioma or None,
        word_timestamps=True,      # <- o coracao de tudo: tempo por PALAVRA
        vad_filter=True,           # corta silencio, melhora muito o tempo
        vad_parameters={"min_silence_duration_ms": 400},
        beam_size=BEAM.get(modelo, 5),
        condition_on_previous_text=False,   # evita o modelo "inventar" repeticao
    )

    dur = float(getattr(info, "duration", 0) or total or 1.0)
    palavras, frases = [], []

    for seg in segmentos:
        texto = (seg.text or "").strip()
        if texto:
            frases.append({"t": texto, "i": round(float(seg.start), 3),
                           "f": round(float(seg.end), 3)})
        for w in (getattr(seg, "words", None) or []):
            limpo = normalizar(w.word)
            if not limpo:
                continue
            palavras.append({"w": limpo,
                             "i": round(float(w.start), 3),
                             "f": round(float(w.end), 3)})
        if on_progresso:
            on_progresso(min(float(seg.end) / dur, 0.99),
                         "transcrevendo... %s" % _hms(seg.end))

    dados = {
        "idioma": getattr(info, "language", "") or (idioma or ""),
        "duracao": round(float(total or dur), 3),
        "modelo": modelo,
        "palavras": palavras,
        "frases": frases,
        "arquivo": os.path.basename(caminho_audio),
    }
    try:
        with open(destino, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
    except Exception:
        pass
    if on_progresso:
        on_progresso(1.0, "pronto: %d palavras" % len(palavras))
    return dados


def _hms(seg):
    seg = int(max(seg, 0))
    return "%d:%02d" % (seg // 60, seg % 60)


# ===========================================================================
# TRANSCRICAO EM SEGUNDO PLANO (a pagina pergunta o progresso de tempos em
# tempos, em vez de ficar pendurada num fetch de 4 minutos)
# ===========================================================================
_tarefas = {}
_trava_tarefas = threading.Lock()


def iniciar_transcricao(caminho_audio, modelo="tiny", idioma=None, forcar=False):
    tid = hashlib.md5(("%s|%s|%s" % (caminho_audio, modelo, time.time())).encode()).hexdigest()[:12]
    with _trava_tarefas:
        _tarefas[tid] = {"progresso": 0.0, "etapa": "na fila", "pronto": False,
                         "erro": "", "resultado": None}

    def _andamento(fracao, etapa):
        with _trava_tarefas:
            if tid in _tarefas:
                _tarefas[tid]["progresso"] = round(float(fracao), 4)
                _tarefas[tid]["etapa"] = etapa

    def _rodar():
        try:
            r = transcrever(caminho_audio, modelo=modelo, idioma=idioma,
                            on_progresso=_andamento, usar_cache=not forcar)
            with _trava_tarefas:
                _tarefas[tid].update({"pronto": True, "progresso": 1.0,
                                      "resultado": r, "etapa": "pronto"})
        except Exception as e:
            with _trava_tarefas:
                _tarefas[tid].update({"pronto": True, "erro": str(e),
                                      "etapa": "erro"})

    threading.Thread(target=_rodar, daemon=True).start()
    return tid


def status_transcricao(tid, com_resultado=False):
    with _trava_tarefas:
        t = _tarefas.get(tid)
        if not t:
            return {"erro": "tarefa desconhecida", "pronto": True}
        fora = {k: v for k, v in t.items() if k != "resultado"}
        if com_resultado and t.get("pronto") and t.get("resultado"):
            fora["resultado"] = t["resultado"]
        return fora


# ===========================================================================
# ALINHAMENTO ROTEIRO <-> FALA
#
# Duas estrategias, e a segunda so entra se a primeira nao convencer:
#
#   1. POR PALAVRA (difflib): casa a sequencia de palavras do roteiro com a
#      sequencia de palavras faladas. E o mais preciso, porque usa o tempo
#      real de cada palavra. Funciona mesmo com o narrador trocando uma
#      palavra aqui e ali.
#
#   2. PROPORCIONAL: se o roteiro colado nao for o mesmo texto que foi narrado
#      (traducao, versao antiga), o casamento por palavra vira ruido. Ai vale
#      a posicao relativa: a parte que comeca aos 40% do roteiro comeca aos
#      40% da fala. Nao e perfeito, mas nunca sai da ordem.
# ===========================================================================
def alinhar_partes(partes, palavras, duracao_total=0.0):
    """
    partes  - lista de textos (a MESMA divisao que a pagina mostrou)
    palavras- [{"w","i","f"}] vindo de transcrever()
    Devolve {"partes": [{"inicio","fim","duracao"}...], "qualidade", "metodo"}
    """
    partes = [str(p or "") for p in partes]
    if not partes:
        return {"partes": [], "qualidade": 0.0, "metodo": "vazio"}

    fim_audio = float(duracao_total or (palavras[-1]["f"] if palavras else 0.0))
    if not palavras:
        return _proporcional(partes, fim_audio, "sem transcricao")

    faladas = [p["w"] for p in palavras]

    # ---- 1. casamento palavra a palavra ----------------------------------
    do_roteiro, dono = [], []
    for i, p in enumerate(partes):
        for bruta in p.split():
            w = normalizar(bruta)
            if w:
                do_roteiro.append(w)
                dono.append(i)

    if not do_roteiro:
        return _proporcional(partes, fim_audio, "roteiro vazio")

    casador = difflib.SequenceMatcher(None, do_roteiro, faladas, autojunk=False)
    mapa = {}
    for a, b, tam in casador.get_matching_blocks():
        for k in range(tam):
            mapa[a + k] = b + k
    qualidade = len(mapa) / len(do_roteiro)

    # Abaixo de 35% de casamento o roteiro colado nao e o texto narrado.
    # Insistir no alinhamento por palavra ali produz tempo pior do que a
    # simples regra de tres.
    if qualidade < 0.35:
        r = _proporcional(partes, fim_audio, "proporcional (roteiro nao bate com a fala)")
        r["qualidade"] = round(qualidade, 3)
        return r

    inicios = [None] * len(partes)
    fins = [None] * len(partes)
    for idx in sorted(mapa):
        i = dono[idx]
        p = palavras[mapa[idx]]
        if inicios[i] is None:
            inicios[i] = p["i"]
        fins[i] = p["f"]        # ultima palavra reconhecida da parte

    # parte sem nenhuma palavra reconhecida herda o fim da anterior
    ultimo = 0.0
    for i in range(len(partes)):
        if inicios[i] is None:
            inicios[i] = ultimo
        ultimo = max(ultimo, fins[i] if fins[i] is not None else inicios[i])

    # ordem crescente, sempre
    for i in range(1, len(inicios)):
        if inicios[i] < inicios[i - 1]:
            inicios[i] = inicios[i - 1]

    # O fim de uma parte e o comeco da proxima: assim a linha do tempo fica
    # continua, sem buraco entre um bloco de imagem e o seguinte.
    fora = []
    for i in range(len(partes)):
        ini = float(inicios[i])
        fim = float(inicios[i + 1]) if i + 1 < len(partes) else fim_audio
        if fim <= ini:
            fim = ini + 0.5
        fora.append({"inicio": round(ini, 3), "fim": round(fim, 3),
                     "duracao": round(fim - ini, 3)})

    return {"partes": fora, "qualidade": round(qualidade, 3),
            "metodo": "palavra a palavra", "duracao": round(fim_audio, 3)}


def _proporcional(partes, fim_audio, motivo):
    """Regra de tres pelo tamanho de cada parte. Sempre em ordem, nunca falha."""
    tamanhos = [max(len(p), 1) for p in partes]
    total = float(sum(tamanhos))
    fora, acumulado = [], 0.0
    for tam in tamanhos:
        ini = (acumulado / total) * fim_audio
        acumulado += tam
        fim = (acumulado / total) * fim_audio
        fora.append({"inicio": round(ini, 3), "fim": round(fim, 3),
                     "duracao": round(fim - ini, 3)})
    return {"partes": fora, "qualidade": 0.0, "metodo": motivo,
            "duracao": round(fim_audio, 3)}


# ===========================================================================
# PLANO DE MIDIA: quantas imagens cabem em cada parte e quanto tempo cada uma
# fica na tela. E o que faz a troca de imagem andar junto com a voz.
# ===========================================================================
def plano_de_midia(alinhamento, seg_por_item=5.0, minimo=2, maximo=12):
    """
    Para cada parte alinhada, calcula quantos itens de midia ela comporta.
    Uma parte de 45s com alvo de 5s por imagem pede 9 imagens; uma de 12s
    pede 2. E o oposto do que a 2.0 fazia (mesmo numero pra todas).
    """
    seg_por_item = max(float(seg_por_item or 5.0), 1.0)
    fora = []
    for p in (alinhamento.get("partes") or []):
        dur = float(p.get("duracao") or 0)
        n = int(round(dur / seg_por_item)) or 1
        # O piso nunca pode forcar uma imagem a piscar. Numa parte de 1,2s
        # exigir 2 midias da 0,6s cada, que o olho nao le - vira flash. Entao
        # o piso cede conforme o que a parte comporta, contando 1,5s como o
        # minimo pra uma imagem ser lida.
        piso_que_cabe = max(1, int(dur / 1.5))
        pedido = n
        n = max(min(n, maximo), min(minimo, piso_que_cabe))
        fora.append({
            "inicio": p["inicio"], "fim": p["fim"], "duracao": p["duracao"],
            "itens": n,
            "seg_por_item": round(dur / n, 3) if n else dur,
            # A parte bateu no teto? Entao o ritmo dela NAO e o que foi pedido,
            # e a tela precisa dizer isso - senao a pessoa mexe no "segundos por
            # midia" e nao entende por que nada muda naquelas partes.
            "no_teto": bool(pedido > maximo),
        })
    return fora


# ===========================================================================
# LEGENDA .SRT
# O sincronizar.py pede um legenda.srt pra saber os tempos. Nos ja temos algo
# melhor que isso - o tempo de cada PALAVRA - entao gerar o SRT aqui e so
# reagrupar o que ja existe, e o usuario para de precisar de um site de
# legenda no meio do caminho.
# ===========================================================================
def _tempo_srt(seg):
    seg = max(float(seg or 0), 0)
    h = int(seg // 3600); m = int((seg % 3600) // 60)
    s_ = int(seg % 60); ms = int(round((seg - int(seg)) * 1000))
    if ms == 1000:
        ms = 0; s_ += 1
    return "%02d:%02d:%02d,%03d" % (h, m, s_, ms)


def gerar_srt(dados, destino=None, max_chars=84, max_seg=6.0):
    """
    Monta o .srt a partir das PALAVRAS (nao das frases do whisper): assim cada
    bloco fecha num tamanho legivel e o tempo bate com a fala de verdade.
    Um bloco fecha quando passa de max_chars, quando passa de max_seg, ou
    quando ha uma pausa clara na narracao.
    """
    palavras = (dados or {}).get("palavras") or []
    if not palavras:
        # sem palavras, cai nas frases (algum modelo pode nao dar palavra)
        blocos = [(f["i"], f["f"], f["t"]) for f in ((dados or {}).get("frases") or [])]
    else:
        blocos = []
        atual, ini, fim = [], None, None
        for w in palavras:
            if ini is None:
                ini = w["i"]
            pausa = (w["i"] - fim) if fim is not None else 0
            texto = " ".join(atual + [w["w"]])
            estourou = (len(texto) > max_chars or (w["f"] - ini) > max_seg
                        or pausa > 0.7)
            if atual and estourou:
                blocos.append((ini, fim, " ".join(atual)))
                atual, ini = [], w["i"]
            atual.append(w["w"])
            fim = w["f"]
        if atual:
            blocos.append((ini, fim, " ".join(atual)))

    linhas = []
    for i, (ini, fim, txt) in enumerate(blocos, 1):
        if fim <= ini:
            fim = ini + 0.4
        linhas.append("%d\n%s --> %s\n%s\n" % (i, _tempo_srt(ini), _tempo_srt(fim), txt.strip()))
    conteudo = "\n".join(linhas)

    if destino:
        with open(destino, "w", encoding="utf-8") as f:
            f.write(conteudo)
    return {"blocos": len(blocos), "conteudo": conteudo}


# ===========================================================================
# LINHA DO TEMPO: o arquivo que a montagem final consome. Mesmo formato que o
# sincronizar.py ja usava, pra nada la precisar mudar.
# ===========================================================================
def salvar_linha_do_tempo(caminho_audio, plano, midias_por_parte, fps=30,
                          largura=1920, altura=1080):
    """
    midias_por_parte - lista de listas: os arquivos ja baixados de cada parte,
                       na ordem em que devem aparecer.
    """
    itens = []
    for i, parte in enumerate(plano):
        arquivos = midias_por_parte[i] if i < len(midias_por_parte) else []
        if not arquivos:
            continue
        dur_parte = float(parte["fim"]) - float(parte["inicio"])
        passo = dur_parte / len(arquivos)
        for j, arq in enumerate(arquivos):
            ini = float(parte["inicio"]) + j * passo
            itens.append({
                "arquivo": arq,
                "paragrafo": i + 1,
                "inicio_us": int(round(ini * 1_000_000)),
                "duracao_us": int(round(passo * 1_000_000)),
            })

    total = max((it["inicio_us"] + it["duracao_us"]) for it in itens) if itens else 0
    linha = {
        "fps": fps, "largura": largura, "altura": altura,
        "audio": os.path.abspath(caminho_audio) if caminho_audio else "",
        "duracao_total_us": total,
        "itens": itens,
    }
    destino = os.path.join(ROOT, "linha_do_tempo.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(linha, f, ensure_ascii=False, indent=2)
    return destino


if __name__ == "__main__":
    import sys
    alvo = sys.argv[1] if len(sys.argv) > 1 else ""
    if not alvo:
        for a in listar_audios():
            print("%-50s %8.1f MB  %s" % (a["nome"], a["tamanho"] / 1e6,
                                          "(transcrito)" if a["transcrito"] else ""))
        raise SystemExit
    r = transcrever(alvo, modelo=(sys.argv[2] if len(sys.argv) > 2 else "small"),
                    on_progresso=lambda f, e: print("  %5.1f%%  %s" % (f * 100, e)))
    print("idioma:", r["idioma"], "| duracao:", r["duracao"], "| palavras:", len(r["palavras"]))
    print("primeiras:", " ".join(p["w"] for p in r["palavras"][:15]))
