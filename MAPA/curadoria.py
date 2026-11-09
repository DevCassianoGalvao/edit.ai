# -*- coding: utf-8 -*-
"""
curadoria.py - a conferencia que um editor faz antes de aceitar uma imagem.

E a porta para Python das travas que ja existiam no buscador-imagens.html. O
motivo de existir aqui: o modo automatico (auto.py) roda SEM navegador, e sem
esta camada ele baixaria tudo que a busca devolvesse - que e exatamente o
problema que a versao com tela ja tinha resolvido.

O que NAO vem junto, de proposito: a parte que ADIVINHA o assunto
(detectDominio, planParts, conceptsRanked...). No modo automatico quem escreve
o assunto, os termos de busca e a lista do que a parte precisa mostrar e o
plano.json - alguem que leu o roteiro de verdade. Portar a adivinhacao seria
duplicar 3 mil linhas de heuristica para fazer pior do que o plano ja faz.

Fica so o que e mecanico e verificavel:
  - de onde veio (loja, jogo, brinquedo, forum, banco limpo)
  - o que o titulo diz (jogo, musica, receita, documento plano)
  - se e miniatura em vez da foto
  - se e previa com marca d'agua
  - se e de outra epoca
  - se mostra o que a parte precisa mostrar
  - e se ja foi usada em outra parte
"""
from __future__ import annotations

import re
import unicodedata

# ---------------------------------------------------------------------------
# DE ONDE VEIO
# ---------------------------------------------------------------------------

# Nunca entrega imagem aproveitavel para video.
DOMINIO_VETADO = """
aliexpress mercadolivre mercadolibre shopee shein temu ebay. amazon.
americanas magazineluiza casasbahia olx. letras.mus cifraclub vagalume
lyrics.com genius.com slideshare scribd academia.edu coursehero passeidireto
wikihow quora.com answers.yahoo
steampowered steamcommunity steamstatic epicgames gog.com playstation
xbox.com nintendo ubisoft electronicarts bethesda rockstargames blizzard
battle.net gamespot ign.com polygon.com kotaku eurogamer pcgamer gamerant
mobygames igdb.com fandom.com wikia. gamepedia nexusmods moddb indiedb
itch.io roblox minecraft gamebanana humblebundle instant-gaming
michtoy hobbylink scalemates tamiya revell airfix wargaming warlordgames
perry-miniatures toysoldier toy-soldier ebayimg
""".split()

# Previa de banco PAGO: a marca d'agua atravessa a foto. Nao e uma imagem pior,
# e uma imagem que NAO SE PODE USAR no video pronto.
DOMINIO_MARCA_DAGUA = """
shutterstock.com istockphoto.com gettyimages. alamy.com depositphotos.com
123rf.com dreamstime.com stock.adobe.com adobestock vecteezy.com
bigstockphoto.com colourbox.com canstockphoto.com agefotostock.com
stocksy.com fotolia.com pond5.com clipartof.com crestock.com photocase.com
""".split()

# Foto CRUA, do jeito que foi fotografada.
FONTE_LIMPA = """
pexels pixabay unsplash openverse wikimedia wikipedia archive.org flickr
nasa.gov esa.int noaa.gov usgs.gov pxhere stocksnap rawpixel picjumbo
freerangestock publicdomain loc.gov iwm.org.uk bundesarchiv
""".split()

# Print de post, meme, montagem.
FONTE_FORUM = """
reddit. redd.it quora twitter x.com facebook instagram tiktok pinterest
blogspot wordpress.com tumblr medium.com
""".split()

# Manchete, tarja e logo de canal por cima da foto.
FONTE_NOTICIA = """
globo.com uol.com.br r7.com folha. estadao terra.com.br band.com.br
cnnbrasil metropoles exame.com infomoney bbc.com dw.com euronews
reuters.com apnews nytimes washingtonpost elpais elmundo abc.es
noticias. jornal gazeta diariod
""".split()


# ---------------------------------------------------------------------------
# O QUE O TITULO DIZ
# ---------------------------------------------------------------------------

# JOGO - a armadilha mais cara num roteiro historico. O jogo e titulado com o
# vocabulario exato da narracao ("Headquarters World War II"), entao a
# conferencia lexical nao so aprova: aprova com nota ALTA. So a fonte e o
# titulo denunciam.
TITULO_JOGO = re.compile("|".join([
    r"gameplay", r"\bgame ?play\b", r"walkthrough", r"playthrough", r"speedrun",
    r"lets? play", r"\bmod(s|ded)?\b", r"\bdlc\b", r"launch trailer",
    r"game trailer", r"gaming\b", r"\bgamer\b", r"jogabilidade", r"detonado",
    r"\bfps\b", r"\brpg\b", r"\bmmo\b", r"\brts\b", r"\bnpc\b",
    r"xbox", r"playstation", r"\bps[45]\b", r"nintendo",
    r"unreal engine", r"in-?game", r"video ?game", r"videojuego",
    r"war ?thunder", r"world of (tanks|warships|warplanes)", r"hearts of iron",
    r"call of duty", r"battlefield [1-9]", r"company of heroes", r"panzer corps",
    r"men of war", r"steel division", r"\barma [23]\b", r"hoi4",
    r"roblox", r"minecraft", r"fortnite",
]), re.I)

# Assunto que nunca e imagem de apoio.
TITULO_VETADO = re.compile("|".join([
    r"lyrics?\b", r"cifra\b", r"acordes\b", r"\bchords?\b",
    r"hor[oó]scopo", r"\bsigno\b", r"palpites?\b",
    r"frete gr[aá]tis", r"comprar online", r"melhores pre[cç]os", r"\bcupom\b",
    r"em promo[cç][aã]o", r"exerc[ií]cios? para", r"como emagrecer",
    r"receita de", r"modo de preparo", r"curr[ií]culo\b", r"modelo de contrato",
]), re.I)

# DOCUMENTO PLANO FOTOGRAFADO - brasao, bandeira, mapa, medalha, cedula,
# cartaz, capa de revista, divisa de patente. Passa em todo teste automatico
# (e JPG grande, nitido, sem marca d'agua) mas nenhum editor poe um brasao no
# meio de uma narracao.
_DOC_PALAVRA = """
map mapa mapas karte carte kaart locator flag flagge bandera bandeira drapeau
logo logotipo wordmark emblem emblema insignia distintivo signature assinatura
autograph unterschrift stamp postage selo banknote cedula coin moeda currency
medal medalha medaille orden ribbon poster cartaz plakat affiche leaflet
diagram diagrama schematic esquema chart graph grafico partitura
constitution constituicao certificate certificado diploma letterhead envelope
postcard postal seal sello siegel crest heraldry heraldica wappen escudo brasao
titelblatt titlepage frontispiece timeline organigram icon icone template
abzeichen kriegsabzeichen urkunde ausweis briefmarke muenze orden ehrenzeichen
insigne ecusson blason armoiries timbre medaille sceau
distintivo escarapela condecoracion estampilla
""".split()
_DOC_TRECHO = (
    "coat of arms", "title page", "cover of", "front cover", "sheet music",
    "family tree", "order of battle", "table of", "list of", "page from",
    "scan of", "excerpt from", "rank insignia", "shoulder board",
    "collar patch", "cap badge", "col, sleeve", "epaulette",
    # emblema bordado: "STF-1 Patch", "mission patch". E pano com desenho,
    # nao fotografia - a mesma familia do brasao.
    " patch", "patch)", "mission patch", "embroidered",
)
TITULO_DOCUMENTO = re.compile(r"(?<![a-z])(" + "|".join(_DOC_PALAVRA) + r")(?![a-z])", re.I)

# VISUALIZACAO DE DADOS - a terceira forma do mesmo problema.
#
# Nao e brasao nem pagina de livro: e um GRAFICO que nao se parece com
# grafico. O "warming stripes" e uma sequencia de faixas coloridas, sem eixo,
# sem numero, sem legenda - e a curadoria nao tinha como saber que aquilo nao e
# uma foto. Num video sobre El Nino ele passou SEIS vezes na mesma parte, com
# nota 94, porque o titulo casa perfeitamente com tudo que a parte pede
# ("temperature", "Pacific", "ocean").
#
# Entram aqui tambem os mapas em falsa cor de satelite ("Sea Surface
# Temperature Anomaly"): sao dado pintado, nao fotografia.
#
# CUIDADO com "stripe" sozinho: "Stripe rust on wheat" e uma doenca de planta
# real e legitima num video sobre lavoura. So a construcao do nome denuncia a
# visualizacao.
TITULO_VISUALIZACAO = re.compile("|".join([
    r"show\s+your\s+stripes", r"(warming|climate|temperature)\s+stripes\b",
    r"\bclimate\s+spiral\b", r"temperature\s+graphic\b",
    r"(temperature|height|precipitation|salinity)\s+anomal",
    r"\banomal\w*\s+(of|map|chart|plot|index)\b",
    r"\btime\s+series\b", r"\bplotting\s+(board|room)\b",
    r"\bdata\s+visuali", r"\bvisuali\w*\s+of\b",
    r"\bfalse\s*-?\s*colou?r\b", r"\bheat\s*map\b",
    r"\bscatter\s*plot\b", r"\bbar\s+graph\b", r"\bhistogram\b",
    r"\bisotherm\b", r"\bcontour\s+(map|plot)\b",
]), re.I)


# PAGINA DE LIVRO DIGITALIZADA e GRAVURA ANTIGA.
#
# E o mesmo problema do brasao, em outra forma: uma prancha anatomica do
# seculo XIX e um JPG grande, nitido, sem marca d'agua e perfeitamente no
# assunto - "Muscles tendons and bones of the knee-joint: two figures" bate em
# tudo que uma parte sobre articulacoes pede. Passa em todos os testes e chega
# na tela como um desenho a bico de pena no meio de um documentario.
#
# Medido no roteiro do Otzi: 16 de 492 imagens (3%), concentradas justamente
# nas partes que pediam anatomia.
#
# Os padroes sao ESTREITOS de proposito. "manual" sozinho pegaria "cambio
# manual"; "plate" pegaria "placa tectonica" e "prato"; "guide" pegaria "guia
# de montanha". O que denuncia o livro e a CONSTRUCAO do titulo de catalogo:
# "a manual of", "N figures", "illustrated guide", "anatomy of the".
TITULO_LIVRO = re.compile("|".join([
    r"\b(a|the)\s+manual\s+of\b", r"\bmanual\s+of\s+(instruction|anatomy)",
    r"\b(two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+figures?\b",
    r"\billustrated\s+(guide|manual|catalogue|edition)\b",
    r"\bfield\s+guide\b", r"\ba\s+treatise\b", r"\bhandbook\s+of\b",
    r"\banatomy\s+of\s+the\b", r"\batlas\s+of\b",
    r"\b(engraving|woodcut|lithograph|etching|mezzotint)\b",
    r"\b(pencil|pen and ink|ink)\s+drawing\b",
    r"\bplate\s+[ivxlc]{1,6}\b", r"\bplates?\s+from\b",
    r"\b(recto|verso)\b", r"\bfolio\b", r"\bwellcome\s+(collection|images)\b",
    r"\bbook\s+illustration\b", r"\bfrom\s+the\s+book\b",
    # Titulo que TERMINA em "manual"/"handbook" e o nome de um livro
    # ("Autopsy manual"). No meio da frase nao vale: "cambio manual" e
    # "manual transmission" sao outra coisa.
    r"\b(manual|handbook|textbook|compendium)\s*$",
]), re.I)

# EGITO: mumia de ANIMAL e retrato de Fayum (pintura) sao as duas colisoes que
# o `evitar` (soft) nunca segurou - passam com nota alta porque "mummy" bate. Como
# regra de pool o item nem chega a nota. Titulos italianos/holandeses dizem
# "Mummia di gatto" / "Mummie van": por isso `mumm\w*`.
TITULO_MUMIA_FALSA = re.compile("|".join([
    r"\b(cat|dog|ibis|falcon|hawk|raptor|crocodile|baboon|monkey|animal|bird|fish|snake|gazelle|cow|lion|jackal|shrew|mongoose)\b.{0,30}\bmumm\w*",
    r"\bmumm\w*\b.{0,20}\b(cat|dog|ibis|falcon|hawk|raptor|crocodile|baboon|animal|bird|fish)\b",
    r"\bmummy\s+portrait", r"\bfayum\b", r"\bfaiyum\b",
    r"\bportrait\s+of\s+an?\s+(man|woman|boy|girl|youth|young|bearded)",
]), re.I)

# So existe DEPOIS. Serve para reprovar sem precisar de data no titulo, e so e
# consultado quando o roteiro tem epoca definida.
MARCA_MODERNA = re.compile("|".join([
    r"\bsts-\d", r"space shuttle", r"\bnasa\b", r"space station",
    r"satellite launch", r"\bspacex\b", r"international space",
    r"\bimo \d{7}", r"\bmmsi\b", r"container terminal", r"containership",
    r"\bdrone\b", r"\bgps\b", r"\buav\b", r"smartphone", r"internet",
    r"website", r"laptop", r"\bf-(1[5-9]|2[0-9])\b", r"\bf/a-18\b",
    r"nimitz", r"aegis", r"change of command \d", r"useucom",
    # Codigo de casco da marinha americana MODERNA. Todos sao do pos-guerra:
    # porta-avioes nuclear (CVN), navio de assalto anfibio (LHD/LHA), destroier
    # de misseis (DDG), submarino nuclear (SSN/SSBN). Aparecem sempre no
    # formato "(LHD 6)" ou "USS Nome (CVN-72)" - e a assinatura mais confiavel
    # de "isto e de hoje" num acervo naval.
    r"\b(cvn|lhd|lha|lpd|ddg|ssn|ssbn|ssgn|lcs|t-ah)[\s-]?\d",
    r"\bnavsource\b", r"\bu\.?s\.? navy photo by\b",
]), re.I)

# Metade de um titulo de banco de imagem e enfeite. Continua contando no total
# (senao um titulo so de enfeite ficaria com denominador zero e escaparia do
# julgamento), mas nao vale como PROVA de assunto.
PALAVRA_GENERICA = set("""
stock footage video videos clip clips free gratis gratuito royalty copyright
licence license download baixar background fundo motion graphics animation
template photo photos foto fotos image images imagem imagens picture pictures
best view vista high quality resolution archive arquivo historic historical
vintage antique
""".split())

MINIATURA_URL = ("encrypted-tbn", "gstatic.com/images", "_thumb.", "/tb/",
                 "=w80-h", "=s90", "=s72", "/90x90", "/150x", "mini.jpg", "icon.png")

# Nao baixa por link direto: hotlink protegido, URL que expira, exige login.
DOMINIO_QUEBRADO = ("instagram.com", "cdninstagram", "fbcdn.net", "lookaside",
                    "scontent", "facebook.com", "fbsbx.com", "tiktokcdn",
                    "pinimg.com/originals", "twimg.com", "licdn.com")

_ANO = re.compile(r"\b(1[5-9]\d{2}|20[0-4]\d)\b")
_PX = re.compile(r"/(\d{2,4})px-")


def sem_acento(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


# Palavra de 3 letras que aparece em qualquer titulo e nao diz nada. Existe
# porque o piso de tamanho teve de baixar para 3 (ver `palavras`), e sem esta
# lista "the", "and" e "for" entrariam no denominador da relevancia.
_RUIDO3 = set("""
the and for with from into out off per via not but nor yet its his her
que com por dos das nos nas uma sem sob ate ele ela seu sua foi sao era
der die das und von den dem ein eine ist auf fur aus bei
del las los con una por sin sus era son
""".split())


def palavras(texto, minimo=3):
    """Tokens de conteudo de um titulo.

    O piso e 3, nao 4, e isso importa: MARCA DE CARRO costuma ter tres letras
    - BYD, KIA, BMW, VW, GM. Com piso 4, o titulo "BYD Atto 3" devolvia so
    ['atto'] e a marca central do roteiro ficava invisivel para a conferencia.
    Uma parte inteira sobre a BYD podia aprovar qualquer carro.

    O preco de baixar o piso e o ruido de tres letras ("the", "and"), tratado
    pela lista acima em vez de por um piso que joga fora o que importa.
    """
    fora = []
    for w in re.split(r"[^\w]+", sem_acento(texto)):
        if len(w) < minimo:
            continue
        if len(w) == 3 and w in _RUIDO3:
            continue
        fora.append(w)
    return fora


def assinatura(titulo):
    """Quatro fotos da MESMA materia, com o mesmo titulo, sao uma imagem so
    ocupando quatro lugares. Usa o titulo INTEIRO: com um pedaco dele, 'porto
    de Santos' e 'porto de Roterda' viravam a mesma assinatura."""
    toks = [w for w in palavras(titulo) if w not in PALAVRA_GENERICA]
    return "-".join(toks) if len(toks) >= 3 else ""


def chave_url(url):
    """Ignora a querystring, que muda entre fontes e faria a mesma imagem
    passar duas vezes."""
    s = str(url or "").split("?")[0].rstrip("/").lower()
    return s


def _bate(vocab, palavra):
    """Casamento por prefixo nos dois sentidos: 'navios' bate com 'navio',
    'ship' bate com 'ships'. Sem isso o plural da narracao nunca casava com o
    singular do titulo - justamente a palavra mais importante do trecho."""
    if palavra in vocab:
        return True
    for v in vocab:
        if len(v) >= 4 and len(palavra) >= 4 and (v.startswith(palavra) or palavra.startswith(v)):
            return True
    return False


def dominio(item):
    """So o HOST, sem caminho e sem nome de arquivo.

    O veto de dominio existe para recusar a LOJA que hospeda a imagem, nao a
    palavra que aparece no nome do arquivo. Lendo a URL inteira, uma foto do
    Commons chamada `Salon_Shein_w_Galerii_Mlociny.jpg` era recusada como
    "loja/agregador" - e num video SOBRE a Shein isso apagava a parte inteira
    (30 de 30 candidatas). O mesmo valia para qualquer arquivo com "amazon",
    "olx" ou "temu" no nome.
    """
    u = str(item.get("url") or "")
    try:
        from urllib.parse import urlparse
        host = urlparse(u).netloc
    except Exception:
        host = ""
    return sem_acento(host + " " + str(item.get("source") or ""))


def limpeza_fonte(item):
    """0 = crua ... 3 = print de post. Vira DESEMPATE, nunca criterio: imagem
    limpa do assunto errado e pior que imagem com tarja do assunto certo -
    tarja se corta, assunto errado nao tem conserto."""
    onde = sem_acento(str(item.get("source") or "") + " " + str(item.get("url") or ""))
    if any(d in onde for d in FONTE_LIMPA):
        return 0
    if any(d in onde for d in FONTE_FORUM):
        return 3
    if any(d in onde for d in FONTE_NOTICIA):
        return 2
    return 1


def e_miniatura(item):
    u = str(item.get("url") or "").lower()
    if any(d in u for d in MINIATURA_URL):
        return True
    # O Wikimedia escreve a largura na propria URL (/440px-Foto.jpg). ATENCAO:
    # nao da para vetar por "/thumb/" - TODA URL redimensionada do Commons tem
    # esse trecho, inclusive a de 1920px, e o veto apagaria o Commons inteiro.
    m = _PX.search(u)
    if m and int(m.group(1)) < 500:
        return True
    w, h = int(item.get("width") or 0), int(item.get("height") or 0)
    return bool(w and h and w < 400 and h < 400)


def anos_do_titulo(titulo):
    return [int(x) for x in _ANO.findall(str(titulo or ""))]


def conferir(item, mostrar, evitar=None, epoca=None, exigir=None):
    """Julga UM item. Devolve (veto:str|None, nota:int, detalhe:dict).

    `mostrar` e a lista do que a parte precisa mostrar - vem do plano.json,
    escrita por quem leu o roteiro. E contra ela que a imagem e julgada, nao
    contra a frase de busca: a frase e uma string comprimida de palavra-chave,
    boa para pedir ao Google, ruim para julgar resultado. Era isso que deixava
    'Car Industry Stock Footage' passar num roteiro de navio - batia em
    'industry', que estava na frase, sem mostrar nada do que a parte precisava.

    `exigir` e o que NAO PODE FALTAR - pelo menos uma dessas palavras tem que
    aparecer, por melhor que o resto esteja.

    Sao duas listas, e nao uma, por um motivo que so aparece medindo. Num
    roteiro sobre a enchente no Rio Grande do Sul, o `mostrar` levava "flood",
    "street", "city" - e o acervo devolveu, com nota alta, enchentes em Salt
    Lake City, em Brisbane em 1893 e na Alemanha. Todas casam perfeitamente com
    "enchente numa rua de cidade"; nenhuma e o assunto. Com o lugar no
    `exigir`, a foto tem que ser DALI.

    A versao com tela ja tinha essa separacao (obrigatorio x desejavel); ao
    portar para Python eu achatei as duas numa lista so, e o sintoma voltou.
    """
    titulo = str(item.get("title") or "")
    onde = sem_acento(str(item.get("source") or "") + " " + str(item.get("url") or ""))
    url = str(item.get("url") or "")
    e_video = bool(item.get("isVideo"))

    if not url.lower().startswith(("http://", "https://")):
        return "link invalido", 0, {}
    host = dominio(item)
    if any(d in host for d in DOMINIO_QUEBRADO):
        return "nao baixa por link direto", 0, {}
    if any(d in host for d in DOMINIO_VETADO):
        return "loja/jogo/agregador", 0, {}
    if TITULO_JOGO.search(titulo):
        return "jogo / gameplay", 0, {}
    if TITULO_VETADO.search(titulo):
        return "assunto fora (musica/receita/loja)", 0, {}
    if TITULO_DOCUMENTO.search(titulo) or any(t in titulo.lower() for t in _DOC_TRECHO):
        return "documento plano (brasao/mapa/cartaz)", 0, {}
    if TITULO_LIVRO.search(titulo):
        return "pagina de livro / gravura", 0, {}
    if TITULO_VISUALIZACAO.search(titulo):
        return "visualizacao de dados (grafico/mapa em falsa cor)", 0, {}
    if not e_video and any(d in host for d in DOMINIO_MARCA_DAGUA):
        return "previa com marca d'agua", 0, {}
    # Miniatura so e descarte para IMAGEM. Num video a miniatura e a capa - o
    # arquivo que vai ser baixado e outro.
    if not e_video and e_miniatura(item):
        return "miniatura, nao a foto", 0, {}
    if TITULO_MUMIA_FALSA.search(titulo):
        return "mumia de animal / retrato de Fayum", 0, {}
    # Formato como regra de pool (filme so de foto, recorte 16:9): o recorte de uma
    # foto muito em pe ou muito panoramica corta o assunto, e ampliar mais que
    # 1,3x pixeliza. Usa a dimensao ORIGINAL quando o banco informa (Commons).
    ow, oh = int(item.get("origWidth") or 0), int(item.get("origHeight") or 0)
    if not e_video and ow and oh:
        asp = ow / oh
        # `retrato: true` na parte do plano (rosto de mumia, estatua) aceita foto em pe
        # ate 0,72: o recorte 16:9 vira um close com movimento vertical
        if asp < (0.72 if item.get("_retrato_ok") else 0.9):
            return "foto em pe demais para recorte 16:9", 0, {}
        if asp > 2.2:
            return "panoramica demais para recorte 16:9", 0, {}
        ew = min(ow, 1920)
        eh = oh * ew / ow
        escala = 1080 / eh if asp >= 16 / 9 else 1920 / ew
        if escala > 1.3:
            return "ampliaria mais que 1,3x", 0, {}

    vocab = set()
    for termo in (mostrar or []):
        for w in palavras(termo, 3):
            vocab.add(w)

    # `exigir` pode ser uma lista de palavras (UM requisito) ou uma lista de
    # listas (VARIOS requisitos, todos obrigatorios). A segunda forma existe
    # porque uma parte pode precisar de duas coisas ao mesmo tempo, e com uma
    # lista so nao da para dizer isso.
    #
    # O caso que obrigou a mudanca: a parte sobre enchente urbana no Sudeste
    # precisa de "enchente" E "Brasil". Com uma lista unica juntando os dois,
    # bastava bater em "flood" e entrou enchente em Salt Lake City; separando em
    # duas listas, a foto tem que mostrar enchente E ser dali.
    grupos = []
    if exigir:
        bruto = exigir if isinstance(exigir[0], (list, tuple)) else [exigir]
        for grupo in bruto:
            g = set()
            for termo in (grupo or []):
                for w in palavras(termo, 3):
                    g.add(w)
                    vocab.add(w)      # o obrigatorio tambem conta como acerto
            if g:
                grupos.append(g)

    fora = set()
    for termo in (evitar or []):
        for w in palavras(termo, 3):
            fora.add(w)

    toks = [w for w in palavras(titulo) if w not in PALAVRA_GENERICA]
    acertos = sum(1 for w in toks if _bate(vocab, w))
    contras = sum(1 for w in toks if _bate(fora, w))

    # ---- a EPOCA -----------------------------------------------------------
    # So roda quando o roteiro e datado. Um roteiro de 1941 recebia cerimonia
    # militar de 2024 com nota alta, porque 'military', 'command' e 'ship'
    # batem igual nos dois seculos. As palavras estao certas; errada esta a
    # decada. So vale quando TODAS as datas do titulo estao fora - um titulo
    # como '1941 x 2015' tem uma data certa e fica.
    epoca_ok = 0
    if epoca:
        anos = anos_do_titulo(titulo)
        if anos:
            epoca_ok = sum(1 for a in anos if epoca["min"] <= a <= epoca["max"])
            if not epoca_ok:
                return "de outra epoca (%d)" % anos[0], 0, {}
        elif MARCA_MODERNA.search(titulo):
            return "coisa moderna, roteiro de epoca", 0, {}

    # ---- o julgamento central --------------------------------------------
    # Titulo com 1 ou 2 palavras de conteudo nao da para julgar (pode ser so
    # 'Kun' e estar certissimo). Com 3 ou mais e NENHUMA batendo, e o artigo
    # veterinario no roteiro do navio.
    # Titulo curto demais para julgar nao e reprovado aqui - ele ja cai na faixa
    # "sem prova" mais abaixo, com nota de ultimo recurso.
    if grupos and len(toks) >= 2:
        for g in grupos:
            if not any(_bate(g, w) for w in toks):
                return "falta o que a parte EXIGE", 0, {}

    if contras and not acertos:
        return "assunto de outro setor", 0, {}
    if len(toks) >= 3 and not acertos:
        return "nada a ver com a parte", 0, {}
    # VIDEO tem piso mais alto: ocupa 5 a 20 segundos de tela, com movimento.
    # Um video errado estraga muito mais que uma foto errada, que passa em 4
    # segundos. A regra geral perdoa titulo curto, e era ali que o video fora
    # do tema entrava - um arquivo do Commons chamado 'Sonnenblume 4.webm' tem
    # 2 palavras de conteudo e passava sem ninguem perguntar se tinha a ver.
    if e_video and vocab and not acertos:
        return "video sem relacao com a parte", 0, {}

    # ---- SEM NENHUMA EVIDENCIA -------------------------------------------
    # Um titulo de uma ou duas palavras escapa do veto acima ("curto demais
    # para julgar"), e ate aqui isso lhe dava nota 22 - que era, INTEIRA, o
    # bonus de fonte limpa. Ou seja: o item entrava no video sem uma unica
    # prova de assunto, so por ser do Commons.
    #
    # E o mesmo erro que este projeto ja tinha cometido e corrigido uma vez:
    # LIMPO nao e RELEVANTE. Ele voltou por uma brecha de tamanho de titulo.
    # Medido num roteiro sobre o Otzi: "Manja Rogan (2)" (uma pessoa qualquer),
    # "Rogan josh01" (um prato indiano) e "MuseAcroItems283-6654" (codigo de
    # catalogo) entraram todos com 22.
    #
    # Zero acerto continua podendo entrar - as vezes e tudo que existe - mas
    # com nota de ultimo recurso, atras de QUALQUER item que tenha uma prova.
    # Assim ele so aparece se a parte estiver faminta de verdade.
    if not acertos:
        nota = 5 - 2 * limpeza_fonte(item)
        return None, int(round(nota)), {"acertos": 0, "de": len(toks),
                                        "epoca": epoca_ok, "sem_prova": True}

    relevancia = acertos / len(toks)
    nota = 100 * relevancia + 14 * min(acertos, 5)
    nota -= 25 * contras
    if epoca_ok:
        nota += 40
    if limpeza_fonte(item) == 0:
        nota += 22
    nota -= 9 * limpeza_fonte(item)
    w = int(item.get("width") or 0)
    if w and w < 600:
        nota -= 12
    return None, int(round(nota)), {"acertos": acertos, "de": len(toks), "epoca": epoca_ok}


class Memoria:
    """O que ja foi para a tela. DUAS memorias, de proposito: a chave de URL
    nao basta porque o Commons entrega a mesma fotografia sob larguras
    diferentes, e um portal republica a mesma foto em dois caminhos - a
    assinatura do titulo pega esses casos."""

    def __init__(self):
        self.urls = set()
        self.assinaturas = set()

    def ja_usada(self, item):
        if chave_url(item.get("url")) in self.urls:
            return True
        a = assinatura(item.get("title"))
        return bool(a and a in self.assinaturas)

    def marcar(self, item):
        self.urls.add(chave_url(item.get("url")))
        a = assinatura(item.get("title"))
        if a:
            self.assinaturas.add(a)


def curar(itens, mostrar, quantos, evitar=None, epoca=None, memoria=None, exigir=None):
    """A curadoria da parte inteira. Devolve (escolhidos, motivos:dict).

    Marca como usado SO o que realmente vai para a tela - candidato aprovado
    mas cortado pela cota continua livre para a proxima parte. Registrar no
    laco de aprovacao queimava material bom sem nunca mostra-lo.
    """
    memoria = memoria if memoria is not None else Memoria()
    motivos = {}
    vistos_aqui = set()
    aprovados = []

    for item in itens:
        if memoria.ja_usada(item):
            motivos["ja usada em outra parte"] = motivos.get("ja usada em outra parte", 0) + 1
            continue
        k = chave_url(item.get("url"))
        if k in vistos_aqui:
            continue
        a = assinatura(item.get("title"))
        if a and a in vistos_aqui:
            motivos["repetido (mesma materia)"] = motivos.get("repetido (mesma materia)", 0) + 1
            continue
        veto, nota, det = conferir(item, mostrar, evitar, epoca, exigir)
        if veto:
            motivos[veto] = motivos.get(veto, 0) + 1
            continue
        vistos_aqui.add(k)
        if a:
            vistos_aqui.add(a)
        item = dict(item)
        item["_nota"] = nota
        item["_detalhe"] = det
        aprovados.append(item)

    aprovados.sort(key=lambda x: -x["_nota"])
    escolhidos = aprovados[:quantos]
    for it in escolhidos:
        memoria.marcar(it)
    return escolhidos, motivos
