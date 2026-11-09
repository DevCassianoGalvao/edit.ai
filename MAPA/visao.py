# -*- coding: utf-8 -*-
"""
visao.py - curadoria VISUAL do THANOS 3.0.

A curadoria lexical (no HTML) compara o titulo do resultado com a narracao.
Ela pega o artigo veterinario e a serie chinesa, mas nao tem como saber que
aquela "foto de porto" e na verdade um print de tela com texto, uma montagem
de quatro fotos coladas, ou uma imagem com marca d'agua atravessada.

Aqui a imagem e olhada de verdade: o servidor baixa as candidatas, reduz, e
manda todas numa unica chamada ao Gemini com o trecho narrado. Volta um
veredito por imagem.

Custo: uma chamada por parte. Com o gemini-flash isso e centavos - e cabe no
nivel gratuito na maioria dos dias.
"""

import base64
import json
import re
import urllib.request
import urllib.parse

# gemini-flash-latest hoje aponta pra um modelo 3.x que "pensa" e devolve corpo
# VAZIO quando o teto de tokens e apertado. O 2.5-flash respeita thinkingBudget=0
# e e o certo pra classificar imagem. Alem disso a cota gratis do 2.5-flash caiu
# pra ~20 chamadas/DIA (corte de dez/2025) - use provedor="clip" (local, sem
# cota) pro grosso do trabalho.
MODELO = "gemini-2.5-flash"
MODELO_CLAUDE = "claude-opus-5"
# Groq: cota gratis grande, mas 200k tokens/DIA e cada imagem ~1900 tokens ->
# so ~100 imagens/dia. Serve de reforco, nao de principal.
MODELO_GROQ = "qwen/qwen3.8-27b"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Imagem grande nao melhora o julgamento e custa banda e tempo: 640px de lado
# ja mostra composicao, texto queimado, marca d'agua e montagem.
LADO_MAX = 640
LIMITE_BYTES = 4_000_000


def _baixar(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ct = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            dados = r.read(LIMITE_BYTES)
        if not ct.startswith("image/") or len(dados) < 800:
            return None, None
        return dados, ct
    except Exception:
        return None, None


def _reduzir(dados, ct):
    """Reduz com o ffmpeg (ja esta na maquina; evita depender do Pillow)."""
    import subprocess, tempfile, os as _os
    nowin = {}
    if _os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        nowin = {"startupinfo": si, "creationflags": 0x08000000}
    try:
        ent = tempfile.NamedTemporaryFile(delete=False, suffix=".img")
        ent.write(dados); ent.close()
        sai = ent.name + ".jpg"
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", ent.name,
               "-vf", "scale='min(%d,iw)':-2" % LADO_MAX,
               "-frames:v", "1", "-q:v", "4", sai]
        subprocess.run(cmd, capture_output=True, timeout=25, **nowin)
        if _os.path.isfile(sai) and _os.path.getsize(sai) > 500:
            with open(sai, "rb") as f:
                pequeno = f.read()
            _os.remove(sai); _os.remove(ent.name)
            return pequeno, "image/jpeg"
        _os.remove(ent.name)
    except Exception:
        pass
    return dados, ct


PROMPT = """Voce e um editor de video profissional montando um documentario.

O video e narrado em {idioma}.

O NARRADOR esta dizendo exatamente isto neste momento do video:
\"\"\"{texto}\"\"\"

Vou te mostrar {n} imagens candidatas, numeradas a partir de 1, na ordem.
Para CADA UMA responda se ela pode entrar NA TELA CHEIA neste momento.

A imagem vai ocupar a TELA CHEIA, 1920x1080. Qualquer coisa escrita nela vai
aparecer enorme. O padrao e o de imagem de banco: a foto CRUA, do jeito que foi
fotografada, sem nada por cima.

REPROVE a imagem quando:
- nao mostra nada do que esta sendo narrado (assunto errado)
- e print de tela, pagina de site, documento, slide ou qualquer coisa cheia de
  texto para ler
- e montagem/colagem de varias fotos, ou grade de miniaturas
- e grafico, tabela ou infografico de um assunto que nao e o narrado
- e desenho, cartoon, meme, capa de video com seta e rosto espantado
- esta desfocada, escura demais, ou muito pequena/esticada para tela cheia

REPROVE TAMBEM, e este e o caso que mais escapa: FOTOGRAFIA DE VERDADE, boa,
mas SUJA - com alguma coisa impressa por cima dela. Olhe a imagem inteira,
inclusive os cantos e as bordas:
- tarja, faixa ou caixa de manchete atravessando a foto (foto de site de
  noticia quase sempre vem assim)
- titulo, chamada, data ou creditos escritos sobre a imagem
- logo de canal, de agencia ou de jornal em qualquer canto
- marca d'agua, mesmo transparente, mesmo pequena
- legenda queimada, tarja de "AO VIVO", "URGENTE", placar, relogio
- moldura, borda decorativa, faixa colorida em cima ou embaixo
- foto colada dentro de um fundo colorido com espaco pra texto ao lado

Uma palavra pequena que faz parte da CENA (o nome do navio no casco, uma placa
de rua, o letreiro de uma loja) NAO e sujeira - isso e a fotografia. O que
reprova e o texto que foi COLOCADO EM CIMA depois.

Entre duas imagens boas, a SEM NADA ESCRITO e sempre a melhor.

REGRA DE IDIOMA (importante, olhe o texto ESCRITO na imagem):
- texto grande e legivel numa lingua que NAO e {idioma} e NAO e ingles
  (espanhol, alemao, russo, chines, arabe, japones...) -> REPROVE, e diga
  "texto em <lingua>". O espectador le a palavra estranha na tela e estranha.
- texto em INGLES so reprove se for MUITO e em destaque (manchete, cartaz
  inteiro, legenda grande). Palavra solta, placa, nome de empresa ou marca em
  ingles esta liberado.
- texto em {idioma} esta liberado.
- imagem sem texto nenhum e sempre a melhor - nao reprove por isso.

APROVE quando e uma fotografia limpa, legivel em tela cheia, que mostra algo
que o narrador esta falando (mesmo que de forma geral: um porto, um reator,
uma multidao). Na duvida entre "serve mais ou menos" e "nao serve", aprove -
o editor humano tem a palavra final.

Responda SO um JSON, sem texto em volta:
{{"itens":[{{"n":1,"ok":true,"motivo":"porto com conteineres, limpa"}},
{{"n":2,"ok":false,"motivo":"print de tela com texto"}}]}}
O motivo deve ter no maximo 8 palavras."""


# Como o idioma do roteiro e escrito no pedido - o modelo precisa saber qual e
# a lingua "de casa" pra julgar o que e texto estrangeiro na imagem.
IDIOMAS = {
    "pt": "portugues", "en": "ingles", "es": "espanhol", "ru": "russo",
    "pl": "polones", "it": "italiano", "fr": "frances", "de": "alemao",
    "tr": "turco",
}


def _perguntar_claude(chave, prompt, partes, timeout):
    """
    Mesma pergunta, formato da API da Anthropic. As imagens vao como blocos
    'image' com base64, na mesma ordem em que foram baixadas.
    """
    conteudo = [{"type": "text", "text": prompt}]
    for pt in partes:
        conteudo.append({"type": "image", "source": {
            "type": "base64",
            "media_type": pt["inline_data"]["mime_type"],
            "data": pt["inline_data"]["data"],
        }})
    corpo = {
        "model": MODELO_CLAUDE,
        # Sem "temperature": nos modelos atuais (Opus 5, Sonnet 5, Fable 5,
        # Opus 4.7/4.8) os parametros de amostragem foram REMOVIDOS e a API
        # devolve 400. Era esse o erro.
        "max_tokens": 8000,
        # Esforco baixo: julgar imagem e classificacao simples. E o jeito certo
        # de baratear, em vez de rebaixar o modelo.
        "output_config": {"effort": "low"},
        "messages": [{"role": "user", "content": conteudo}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(corpo).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "x-api-key": chave,
                 "anthropic-version": "2023-06-01"},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8", "ignore"))
    for bloco in (resp.get("content") or []):
        if bloco.get("type") == "text":
            return bloco.get("text", "")
    return ""


def _avaliar_clip(texto, urls, assunto=""):
    """Curadoria LOCAL com CLIP (clipcheck.py) - gratis, offline, sem cota.
    Compara cada candidata com a FRASE DE BUSCA da parte (concreta, visual) e
    com negativos (print, colagem, documento, marca d'agua...). Nao le texto na
    imagem, mas resolve o "assunto errado", que e o grosso do problema.

    Usa a frase de busca ('assunto') quando existe - ela e uma descricao visual
    ("EE-9 Cascavel armored car"); o CLIP nao entende a NARRACAO crua, que e so
    prosa no idioma do video."""
    try:
        import clipcheck
    except Exception as e:
        return {"erro": "clipcheck.py: %s" % e, "itens": []}
    if not clipcheck.available():
        return {"erro": "CLIP indisponivel (pip install onnxruntime huggingface_hub tokenizers pillow)", "itens": []}
    assunto = (assunto or "").strip() or " ".join(str(texto or "").split()[:40])
    itens, vistas = [], 0
    for i, u in enumerate(urls, 1):
        dados, _ = _baixar(u)
        if not dados:
            continue
        vistas += 1
        try:
            ok = clipcheck.relevant(dados, assunto)
        except Exception:
            ok = True
        itens.append({"n": i, "ok": bool(ok),
                      "motivo": "" if ok else "CLIP: nao parece o assunto narrado"})
    return {"itens": itens, "vistas": vistas}


def _perguntar_groq(chave, prompt, partes, timeout):
    """Mesma pergunta, API OpenAI-compativel do Groq (qwen3.8-27b, multimodal).
    O Groq fica atras do Cloudflare - precisa de User-Agent de navegador."""
    conteudo = [{"type": "text", "text": prompt}]
    for pt in partes:
        d = pt["inline_data"]
        conteudo.append({"type": "image_url", "image_url": {
            "url": "data:%s;base64,%s" % (d["mime_type"], d["data"])}})
    corpo = {"model": MODELO_GROQ, "temperature": 0, "max_tokens": 2000,
             "messages": [{"role": "user", "content": conteudo}],
             "response_format": {"type": "json_object"}}
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(corpo).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + chave,
                 "User-Agent": UA},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8", "ignore"))
    return resp["choices"][0]["message"]["content"] or ""


def avaliar(chave, texto, urls, timeout=90, idioma="pt", provedor="gemini", assunto=""):
    """
    Devolve {"itens":[{"n":..,"ok":bool,"motivo":str}], "vistas":N, "erro":str}
    Indices sao 1-based e batem com a ordem de 'urls'.
    """
    urls = [u for u in (urls or []) if u][:12]
    if not urls:
        return {"itens": [], "vistas": 0}

    if provedor == "clip":
        return _avaliar_clip(texto, urls, assunto)

    chave = (chave or "").strip()
    if not chave:
        return {"erro": "sem chave (ou use provedor 'clip', que nao pede chave)", "itens": []}

    partes = []
    mapa = []            # posicao no pedido -> indice original (1-based)
    for i, u in enumerate(urls, 1):
        dados, ct = _baixar(u)
        if not dados:
            continue
        dados, ct = _reduzir(dados, ct)
        partes.append({"inline_data": {"mime_type": ct,
                                       "data": base64.b64encode(dados).decode("ascii")}})
        mapa.append(i)

    if not partes:
        return {"itens": [], "vistas": 0, "erro": "nenhuma imagem abriu"}

    prompt = PROMPT.format(texto=(texto or "")[:1200], n=len(partes),
                           idioma=IDIOMAS.get((idioma or "pt").lower(), "portugues"))
    marca = {"claude": "Claude", "groq": "Groq"}.get(provedor, "Gemini")

    try:
        if provedor == "claude":
            txt = _perguntar_claude(chave, prompt, partes, timeout)
        elif provedor == "groq":
            txt = _perguntar_groq(chave, prompt, partes, timeout)
        else:
            corpo = {
                "contents": [{"parts": [{"text": prompt}] + partes}],
                "generationConfig": {
                    "temperature": 0.1, "maxOutputTokens": 2000,
                    "responseMimeType": "application/json",
                    # sem isto o 2.5-flash gasta o teto "pensando" e volta vazio
                    "thinkingConfig": {"thinkingBudget": 0},
                },
            }
            url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
                   % (MODELO, urllib.parse.quote(chave)))
            req = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8"),
                                         headers={"Content-Type": "application/json"},
                                         method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read().decode("utf-8", "ignore"))
            txt = "".join(p.get("text", "") for p in
                          resp["candidates"][0].get("content", {}).get("parts", []))
    except urllib.error.HTTPError as e:
        detalhe = ""
        try:
            bruto = json.loads(e.read().decode("utf-8", "ignore"))
            detalhe = (bruto.get("error", {}) or {}).get("message", "") or str(bruto)[:240]
        except Exception:
            pass
        # O detalhe da API e a unica coisa que diz o que esta errado de verdade
        # (foi ele que revelou o problema do "temperature") - entao vai inteiro
        # pra tela, sem cortar em 160 caracteres.
        return {"erro": "%s %s: %s" % (marca, e.code, detalhe[:240]), "itens": []}
    except Exception as e:
        return {"erro": "%s: %s" % (marca, str(e)[:160]), "itens": []}

    try:
        m = re.search(r"\{.*\}", txt, re.S)
        dados = json.loads(m.group(0) if m else txt)
    except Exception:
        return {"erro": "a resposta do %s nao veio em JSON" % marca, "itens": []}

    fora = []
    for it in (dados.get("itens") or []):
        try:
            pos = int(it.get("n"))
        except Exception:
            continue
        if 1 <= pos <= len(mapa):
            fora.append({"n": mapa[pos - 1], "ok": bool(it.get("ok", True)),
                         "motivo": str(it.get("motivo", ""))[:80]})
    return {"itens": fora, "vistas": len(partes)}
