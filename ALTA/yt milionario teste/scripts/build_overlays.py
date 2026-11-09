"""TEXTO NA TELA do modo ULTRA (PROMPT_v_ULTRA, seção 4): escreve o campo `ov` nos cortes de data/timeline.json.

Quatro famílias, todas na mesma tipografia (src/overlays/Ultra.tsx):
  slate     lugar/data em 2 linhas — vem de beats.json (campo `slate`), entra 1 s depois do corte, fica 4 s
  capitulo  cartela de 2–4 palavras, 2,5 s — vem de beats.json (`capitulo`); em tela só a cada >= GAP_CAPITULO,
            as demais ficam só na lista de capítulos do YouTube (qa/chapters.md, que leva TODAS)
  lower     nome da espécie na PRIMEIRA menção — só em corte cujo arquivo foi escolhido pela tag da espécie
  selo      número na tela = número DITO dentro do corte (`diz`); se o Whisper não achar a palavra ali, o script PARA

E mais duas famílias SOBREPOSTAS (21/09/2026), que não tomam a tela — o plano continua rodando atrás:
  destaque  nome próprio / ano citado na narração, em canto alternado (src/overlays/Destaques.tsx).
            Os candidatos saem SOZINHOS da transcrição (nome próprio e ano); DESTAQUE_FIXO e NOMES_FORA ajustam.
  cartão    cartao | comparacao | fichas | palavra | faixa | numero | etiqueta — tabela DOSSIE, por filme
            (src/overlays/Cartoes.tsx, papel creme e tipografia de máquina de escrever)

Regras que este script não deixa quebrar:
  1. nada por cima de animação (a animação já é a cartela) nem em corte menor que o gráfico precisa
  2. slate e cartela de capítulo nunca no mesmo plano
  3. dois gráficos quaisquer nunca a menos de GAP_GERAL s
  4. corte com `ov` passa a ser renderizado pelo Remotion (render_hybrid lê o mesmo campo)

Uso: python build_overlays.py [--limpar] [--tolerar]
"""
import json
from collections import Counter
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
cfg = json.loads((ROOT / "data" / "pipeline_config.json").read_text("utf-8"))  # idioma do filme (números por extenso)
GAP_GERAL = 25        # s entre dois gráficos quaisquer
GAP_CAPITULO = 90     # s entre duas cartelas de capítulo EM TELA (26/09/2026: todo capítulo abre com carimbo lugar/data)
SLATE = (30, 120)     # entra, fica (quadros)
CAPITULO = (6, 100)
LOWER = (12, 105)
SELO_ENTRA = 20
MIN_SELO_S = 4.5
DESTAQUE = (8, 100)   # entra, fica (quadros) — 3,3 s na tela
GAP_DESTAQUE = 14     # s entre dois destaques (o destaque é pequeno: cabe mais perto que um gráfico grande)
GAP_GRANDE = 12       # s entre um destaque e um gráfico grande (slate, capítulo, selo, lower, cartão)
ATRASO_MAX = 12       # s: nome dito DENTRO de uma animação entra no primeiro corte livre depois dela
MAX_DESTAQUES = 26    # teto por filme: passar disso vira poluição, não ritmo
# REGRA DO USUÁRIO (22/09/2026, 2ª versão): o filme se apoia nos CARTÕES EM PAPEL, não em tela cheia.
# Ele pediu "bem mais desses estilos durante o vídeo e menos motion graphics", numa mescla variada.
#   - cartão em papel (cartao | comparacao | fichas | palavra): pelo menos 1 a cada 2 min, nunca menos de 8
#   - animação de tela cheia (scripts/beats.py): no máximo 1 a cada 3 min, nunca menos de 6
#   - variedade: nenhum tipo de cartão pode passar de metade do total
# Qualquer uma dessas três quebrada = ERRO de build: o filme não sai. Ver src/overlays/Cartoes.tsx.
def _minutos():
    m = json.loads((D / "source_meta.json").read_text("utf-8"))
    return m.get("durationSec", m["durationInFrames"] / m.get("fps", FPS)) / 60


MINUTOS = _minutos()
# 26/09/2026 (regra do usuário, "mescle bem na tela para ficar bem dinâmico"): piso de 1 cartão a cada 1,5 min e a família
# de ARQUIVO obrigatória em todo filme (quadro de provas, checklist, ficha, manchete/telex, lupa, antes/depois, rolo, revela)
MIN_PAPEL = max(8, round(MINUTOS / 1.5))
MAX_ANIM = max(6, round(MINUTOS / 3))
MAX_UM_TIPO = 0.35    # nenhum tipo de cartão passa de 35 % do total (26/09: eram 50 %; com 14 tipos, a mescla tem de girar)
ARQUIVO = ("quadro", "checklist", "ficha", "manchete", "teletipo", "lupa", "antesdepois", "rolo", "revela")
# 04/10/2026 — estilos por GÊNERO (src/scenes/estilos5.tsx), ligados no painel em "Cartões na tela":
# planta (carros/máquinas/navios), caderno (arqueologia), mercado (economia/agro), radar (guerra/marinha), vhs (nostalgia).
# Ligado = pelo menos MIN_GENERO cartões daquele tipo no DOSSIE; desligado = nenhum é exigido (podem entrar mesmo assim).
GENERO = ("planta", "caderno", "mercado", "radar", "vhs",
          # 04/10/2026 (3ª regra: "10 estilos por tema") — src/scenes/estilos_<tema>.tsx
          "velocimetro", "raiox", "testecolisao", "avisorecall", "linhamontagem",                       # carros
          "estratigrafia", "papiro", "etiquetamuseu", "datacaocarbono", "escaneamento3d", "quadriculaescavacao",  # arqueologia
          "cupomfiscal", "rankingbarras", "rosca", "pilhadinheiro", "contratocarimbo",                  # economia
          "dossiesecreto", "sonar", "comparaforcas", "periscopio", "placaidentificacao",                # militar
          "tvtubo", "anunciorevista", "polaroids", "evolucaomarca", "etiquetapreco", "editai_ficha", "editai_linha")                   # nostalgia
# 04/10/2026 (2ª regra do usuário: "quero que o estilo apareça mais vezes para ficar mais dinâmico"):
# o estilo ligado volta 1 vez a cada GENERO_A_CADA min, ESPALHADO pelo filme (nenhum buraco maior que o dobro do
# intervalo); com 2+ estilos ligados a cota se divide entre eles (cada um >= 3). Os estilos de gênero saem do teto de
# 35 % por tipo; o teto deles, somados, é MAX_GENERO dos cartões em papel.
GENERO_A_CADA = 3.0
MIN_GENERO = max(4, round(MINUTOS / GENERO_A_CADA))
MAX_GENERO = 0.5
OBRIGATORIOS = [("quadro",), ("checklist",), ("ficha",), ("manchete", "teletipo"), ("lupa",), ("antesdepois",), ("rolo",), ("revela",)]
PARALAXE_GAP = 45     # s entre duas fotos em 2.5D (scripts/paralaxe.py recorta o sujeito)
MAX_NUMEROS = 14      # teto dos números automáticos (o meio do filme raramente cita nome próprio)
NUMERO = (8, 95)
CANTOS = ["baixo-esq", "baixo-dir", "alto-esq", "centro-esq"]  # alternados, para não repetir o mesmo canto
# 12/10/2026 — MODO ENXUTO (regra do usuário: "1 vídeo por hora bem produzido"). Medido: o Remotion desenhava ~30 % do
# filme (84 % disso eram sobreposições: paralaxe 21x, palavra, teletipo, revela, radar...) e segurava o render em 42-77 min.
# Ficam só as sobreposições que EXPLICAM (ficha, checklist, lupa, antes/depois, comparação), no máx. 1 a cada 3 min;
# paralaxe no máx. 5; sem destaques/números automáticos; estilos de gênero não são exigidos. "enxuto": false = antigo.
ENXUTO = cfg.get("enxuto", True) is not False
ENXUTO_TIPOS = ("ficha", "checklist", "lupa", "antesdepois", "comparacao") + tuple(g for g in GENERO if (cfg.get("cartoes_genero") or {}).get(g))
MAX_PAPEL = 10 ** 6
PARALAXE_MAX = 10 ** 6
if ENXUTO:
    MAX_PAPEL = max(4, round(MINUTOS / 3))
    MIN_PAPEL = max(4, round(MINUTOS / 4))
    MAX_UM_TIPO = 0.5
    OBRIGATORIOS = [("ficha",), ("checklist",), ("lupa",), ("antesdepois",)]
    MAX_DESTAQUES = 0
    MAX_NUMEROS = 0
    PARALAXE_MAX = 5
    PARALAXE_GAP = max(45, MINUTOS * 60 / 6)
# 04/11/2026 estilo ARQUIVO COLORIZADO (receita em painel/estilos/arquivo-colorizado.json): o texto na tela vem das
# etiquetas/nomes da moldura e das peças de src/scenes/arquivo_colorizado.tsx (teto 1 peça a cada ~1,5 min);
# sobreposições do enxuto ficam desligadas (DOSSIE vazio não é erro)
COLORIZADO = bool(cfg.get("arquivo_colorizado"))
if COLORIZADO:
    MIN_PAPEL = 0
    OBRIGATORIOS = []
    MAX_ANIM = max(MAX_ANIM, round(MINUTOS / 1.5))

norm = lambda s: re.sub(r"[^a-z0-9]", "", "".join(
    c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)))
norm_txt = lambda s: " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", "".join(
    c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))).strip()) + " "

# ---------------------------------------------------------------- selos: número na tela = número dito
# para = parágrafo; diz = "palavra|algarismo" que TEM de ser falada dentro do corte que recebe o selo
# (o Whisper escreve "1 .300" em dois tokens — "1" e ".300" —, o roteiro "mil e trezentos": as grafias contam).
DADOS = []   # os numeros vem do extrator automatico (tipo "numero"), roteiro em polones

# ---------------------------------------------------------------- lower thirds: 1ª menção FORA dos slates
ESPECIES = {}
TITULO_EXIGE = {}

# ---------------------------------------------------------------- destaques automáticos (nome próprio / ano)
# Nada a preencher: os candidatos saem da transcrição. Estas duas listas só corrigem o que o automático errar.
NOMES_FORA = {  # 06/11/2026 pt (lag): todo token maiúsculo que não é nome próprio (_dossie_lag.py)
    'AGORA', 'AGÊNCIA', 'AGÊNCIA BRASILEIRA', 'ALGUNS', 'ALÉM', 'AMÉRICA', 'ANDRÉ', 'ANTES', 'ANTÔNIO', 'ANTÔNIO CESAR', 'ANTÔNIO CESAR BERNARDO', 'AO', 'APOIO', 'APRENDEU', 'AQUICULTURA', 'ARTESANAIS', 'AS', 'ATLÂNTICO', 'ATÉ', 'AVIÕES', 'AÉREA', 'AÉREA BRASILEIRA', 'AÍ', 'BANCO', 'BARCOS', 'BERNARDO', 'BORGES', 'BRASILEIRA', 'CACHO', 'CACHO RIBEIRO', 'CADA', 'CARNEIRO', 'CEARENSE', 'CESAR', 'CESAR BERNARDO', 'CIENTÍFICO', 'CINQUENTA', 'CIVIL', 'COLOCA-SE', 'COLÔNIA ZÊ-DEZESSETE', 'COM', 'COMEÇA', 'CRESCE', 'CRUZ', 'DE', 'DEPOIS', 'DESCE', 'DESENVOLVIMENTO', 'DESENVOLVIMENTO CIENTÍFICO', 'DEZ', 'DEZENOVE', 'DEZESSEIS', 'DIAS', 'DISTRITO', 'DISTRITO NAVAL', 'DIÁRIO', 'DO', 'DOIS', 'DOZE', 'DURANTE', 'DÉCADAS', 'EDUARDO', 'EDUARDO BATISTA', 'ELA', 'ELE', 'EM', 'EM ICAPUÍ', 'EM PONTA', 'EM PONTA GROSSA', 'EM REDONDA', 'ENQUANTO', 'ENTRE', 'ENTÃO', 'ESSA', 'ESSE', 'ESSES', 'ESTADOS', 'ESTÁ', 'FAZ', 'FEDERAL', 'FESTIVAL', 'FICA', 'FOGO', 'FOI', 'FORAM', 'FORÇA', 'FORÇA AÉREA', 'FUNDAÇÃO', 'FUNDAÇÃO CEARENSE', 'FÁTIMA', 'GILCIDENE', 'GOSTOSO', 'GRANDE', 'GROSSA', 'GRUPAMENTO', 'GUERRA', 'HAVIA', 'HOJE', 'HOSPITAL', 'HÁ', 'INCLUSIVE', 'INTELIGÊNCIA', 'INTERMINISTERIAL', 'IORQUE', 'ISSO', 'JAILSON', 'JOSÉ', 'JOSÉ MARIA', 'JÁ', 'LAGOSTA', 'LEMBRA', 'LÁ', 'MAIS', 'MARIA', 'MARTIN', 'MARÍTIMO', 'MAS', 'MELQUÍADES', 'MELQUÍADES RIBEIRO', 'METADE', 'MIGUEL', 'MILITAR', 'MINISTÉRIO', 'MUITAS', 'MUITOS', 'NA', 'NAQUELE', 'NAVAL', 'NESSA', 'NINGUÉM', 'NO', 'NO CEARÁ', 'NO TRIBUNAL', 'NO TRIBUNAL MARÍTIMO', 'NORTE', 'NOS', 'NOVA', 'NOVENTA', 'NUM', 'NUMA', 'NÃO', 'OLHAM', 'OS', 'OU', 'OUTRO', 'PARA', 'PATRULHA', 'PATRULHA NAVAL', 'PELO', 'PENSE', 'PERGUNTAM', 'PESCA', 'PESCADORAS', 'PESCADORAS ARTESANAIS', 'PESCADORES', 'PESCADORES ZÊ-DEZESSETE', 'PESQUISADORES', 'POLÍCIA', 'POLÍCIAS', 'POLÍCIAS FEDERAL', 'PONTA', 'POR', 'PORQUE', 'QUANDO', 'QUANTO', 'QUANTOS', 'QUEM', 'RAIMUNDO', 'RAÚL', 'RESTAURANTES', 'RIBEIRO', 'RIBEIRO CARNEIRO', 'RIO', 'RIO GRANDE', 'RIVÂNIA', 'ROLFRAN', 'ROLFRAN CACHO', 'SANTOS', 'SE', 'SEGUNDO', 'SETE', 'SETENTA', 'SILVA', 'SINDICATO', 'SOARES', 'SOUSA', 'SÃO', 'SÃO MIGUEL', 'SÓ', 'TECNOLÓGICO', 'TERCEIRO', 'TERCEIRO DISTRITO', 'TIRAR', 'TOBIAS', 'TODOS', 'TRIBUNAL', 'TRÊS', 'TUDO', 'UM', 'UMA', 'UNIDOS', 'UNIVERSIDADE', 'UNIVERSIDADE FEDERAL', 'VENTURA', 'VOLTAR',
}
DESTAQUE_FIXO = {}     # nome -> sub ("KELSO DEPOT": "Mojave Desert · 1924"); sub None = sem linha de cima

MESES = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
# unidades, idiomas e adjetivos de nacionalidade: vêm em maiúscula no meio da frase mas não são destaque
FUNCAO = {"THE", "A", "AN", "AND", "BUT", "IN", "ON", "AT", "OF", "FOR", "FROM", "TO", "IT", "THIS", "THAT",
          "THERE", "THEN", "WHEN", "WHAT", "IF", "HE", "SHE", "THEY", "WE", "YOU", "HIS", "HER", "THEIR", "OUR",
          "BY", "WITH", "AS", "SO", "NO", "NOT", "EVERY", "EACH", "MOST", "SOME", "AFTER", "BEFORE", "BECAUSE",
          "NOW", "HERE", "INSIDE", "OUTSIDE", "OVER", "UNDER", "STILL", "EVEN", "YOUR", "MY", "THESE", "THOSE"}
GENERICOS = {"FAHRENHEIT", "CELSIUS", "ENGLISH", "SPANISH", "AMERICAN", "NORTH AMERICAN", "BRITISH", "GERMAN",
             "FRENCH", "EUROPEAN", "MR", "MRS", "DR", "ST"}
TOK = re.compile(r"^[A-Z][a-zÀ-ÿ'’]+(?:[-'’][A-Za-zÀ-ÿ]+)?$")
ACRO = re.compile(r"^(?:[A-Z]{2,5}|[IVXL]+)$")
NUM = re.compile(r"^\d{1,4}$")
ANO = re.compile(r"^(1[5-9]\d\d|20\d\d)$")
limpa = lambda t: re.sub(r"^[^\w]+|[^\w'’-]+$", "", t)
frases = lambda txt: re.split(r"(?<=[.!?])\s+", txt.strip())


def candidatos(tr):
    """Nomes próprios e anos do ROTEIRO (grafia certa — o Whisper escreve "Sema Hill" para "Cima Hill"),
    com todos os instantes em que aparecem: [(nome, sub, [segundos])], em ordem de tempo."""
    palavras = [(w["s"], norm(w["w"])) for fr in tr["sentences"] for w in fr["words"]]

    # 1ª passada: palavra em maiúscula FORA do início de frase é nome mesmo; palavra que TAMBÉM aparece em
    # minúscula no roteiro ("railroad", "hours", "service") é substantivo comum e não vira destaque sozinha
    meio, minusc = set(), set()
    for pa in tr["paragraphs"]:
        for fr in frases(pa["text"]):
            xs = [limpa(x) for x in fr.split()]
            for t in xs[1:]:
                if TOK.match(t) or ACRO.match(t):
                    meio.add(t)
            for t in xs:
                if t[:1].islower():
                    minusc.add(t.upper())

    achados, ordem = {}, []
    for pi, pa in enumerate(tr["paragraphs"]):
        a, z = pa["startSec"], pa["endSec"]
        janela = [(s, w) for s, w in palavras if a - 1 <= s <= z + 1]
        for fr in frases(pa["text"]):
            cru = fr.split()
            ws = [limpa(x) for x in cru]
            # "em Paris, Berlim ou Madri" são TRÊS nomes, não um: a vírgula fecha o nome
            corta = [bool(re.search(r"[,;:!?—–)]$", x)) for x in cru]
            anos = [t for t in ws if ANO.match(t)]
            i, n = 0, len(ws)
            while i < n:
                t = ws[i]
                proprio = (TOK.match(t) or ACRO.match(t)) and t not in MESES
                if proprio and (i > 0 or t in meio):
                    run, fim = [t], i
                    while fim + 1 < n and not corta[fim]:
                        t2 = ws[fim + 1]
                        if ((TOK.match(t2) or ACRO.match(t2)) and t2 not in MESES) or (NUM.match(t2) and run):
                            run.append(t2)
                            fim += 1
                            if NUM.match(t2):   # "Interstate 15", "Route 66": o número fecha o nome
                                break
                        else:
                            break
                    while run and run[0].upper() in FUNCAO:   # "The Mojave" -> "MOJAVE"
                        run = run[1:]
                    if not run:
                        i = fim + 1
                        continue
                    nome = re.sub(r"['’]S$", "", " ".join(run).upper())
                    uma = len(run) == 1
                    vale = (not uma or (len(run[0]) >= 5 and run[0] in meio and nome not in minusc))                         and nome not in GENERICOS
                    if vale and nome not in NOMES_FORA:
                        achados.setdefault(nome, [])
                        ordem.append(nome) if nome not in ordem else None
                        alvo = norm(run[0])
                        t0 = next((s for s, w in janela if w.startswith(alvo) and alvo), None)
                        if t0 is not None:
                            achados[nome].append(t0)
                        if nome not in DESTAQUE_FIXO and anos and len(achados[nome]) == 1:
                            DESTAQUE_FIXO.setdefault(nome, anos[0])
                    i = fim + 1
                    continue
                if ANO.match(t) and t not in NOMES_FORA:
                    achados.setdefault(t, [])
                    ordem.append(t) if t not in ordem else None
                    t0 = next((s for s, w in janela if w == t), None)
                    if t0 is not None:
                        achados[t].append(t0)
                i += 1

    # tira o nome que é pedaço de outro já visto ("MOJAVE" depois de "MOJAVE DESERT")
    fora, vistos = set(), []
    for nome in ordem:
        if any(f" {nome} " in f" {v} " or f" {v} " in f" {nome} " for v in vistos):
            fora.add(nome)
        else:
            vistos.append(nome)
    saida = [(n, DESTAQUE_FIXO.get(n), sorted(achados[n])) for n in ordem if n not in fora and achados[n]]
    return sorted(saida, key=lambda x: x[2][0])


# ---------------------------------------------------------------- números automáticos ("110 °F", "40 miles")
# O número TEM de estar escrito por extenso ou em algarismo no roteiro e ser seguido de uma unidade da tabela.
# NUMEROS_FORA tira um valor que não deve ir para a tela neste filme (ex.: {"12 hours"}).
NUMEROS_FORA = {"6 km", "10 m"}  # 12/10 gelo pt: "6 km" errado (p08), "10 m" era 10,5 m
NUMEROS_ROTULO = {}    # "118 °F" -> "Inside the cab" (rótulo em cima do número; sem entrada = só o número)
UNI_EN = {"degrees": "°", "degree": "°", "miles": "miles", "mile": "mile", "feet": "ft", "foot": "ft",
          "hours": "hours", "hour": "hour", "minutes": "min", "minute": "min", "tons": "tons", "ton": "ton",
          "pounds": "lb", "percent": "%", "years": "years", "year": "year", "gallons": "gal", "gallon": "gal",
          "kilometres": "km", "kilometers": "km", "metres": "m", "meters": "m", "days": "days", "day": "day"}
UNI_PT = {"graus": "°", "quilômetros": "km", "quilometros": "km", "metros": "m", "horas": "h", "hora": "h",
          "minutos": "min", "toneladas": "t", "quilos": "kg", "por cento": "%", "anos": "anos", "ano": "ano",
          "litros": "L", "reais": "R$", "dias": "dias", "dia": "dia"}
NUM_EN = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
          "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
          "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
          "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
UNI_ES = {"grados": "°", "kilómetros": "km", "kilometros": "km", "metros": "m", "metro": "m",
          "centímetros": "cm", "centimetros": "cm", "milímetros": "mm", "milimetros": "mm",
          "toneladas": "t", "tonelada": "t", "caballos": "cv", "horas": "h", "hora": "h",
          "minutos": "min", "años": "años", "año": "año", "kilos": "kg", "litros": "L",
          "por ciento": "%", "hombres": "hombres", "días": "días", "dia": "día"}
NUM_ES = {"cero": 0, "uno": 1, "una": 1, "un": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
          "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
          "quince": 15, "dieciséis": 16, "dieciseis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
          "veinte": 20, "veintiuno": 21, "veintidós": 22, "veintidos": 22, "veintitrés": 23, "veintitres": 23,
          "veinticuatro": 24, "veinticinco": 25, "veintiséis": 26, "veintiseis": 26, "veintisiete": 27,
          "veintiocho": 28, "veintinueve": 29, "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60,
          "setenta": 70, "ochenta": 80, "noventa": 90, "cien": 100, "ciento": 100, "doscientos": 200,
          "trescientos": 300, "cuatrocientos": 400, "quinientos": 500, "seiscientos": 600,
          "setecientos": 700, "ochocientos": 800, "novecientos": 900}
ESCALA_ES = {"mil": 1000, "millón": 1000000, "millon": 1000000, "millones": 1000000}
NUM_PT = {"zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3, "quatro": 4, "cinco": 5,
          "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13,
          "quatorze": 14, "catorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18,
          "dezenove": 19, "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60,
          "setenta": 70, "oitenta": 80, "noventa": 90, "cem": 100, "cento": 100, "duzentos": 200,
          "trezentos": 300, "quatrocentos": 400, "quinhentos": 500, "seiscentos": 600, "setecentos": 700,
          "oitocentos": 800, "novecentos": 900}  # "mil" e ESCALA (multiplica), nao numero
ESCALA_EN = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000}
ESCALA_PT = {"mil": 1000, "milhão": 1000000, "milhões": 1000000, "bilhão": 1000000000, "bilhões": 1000000000}
UNI_IT = {"gradi": "°", "chilometri": "km", "metri": "m", "centimetri": "cm", "millimetri": "mm",
          "tonnellate": "t", "kilowatt": "kW", "cavalli": "CV", "ore": "h", "minuti": "min", "anni": "anni",
          "chili": "kg", "litri": "L", "giorni": "giorni", "cilindri": "cilindri"}


class _NumIT:
    """Numero italiano scritto per esteso e ATTACCATO ("duemilatrecento", "ottantamila", "novantasei")."""
    U = {"zero": 0, "uno": 1, "un": 1, "una": 1, "due": 2, "tre": 3, "tré": 3, "quattro": 4, "cinque": 5, "sei": 6,
         "sette": 7, "otto": 8, "nove": 9, "dieci": 10, "undici": 11, "dodici": 12, "tredici": 13,
         "quattordici": 14, "quindici": 15, "sedici": 16, "diciassette": 17, "diciotto": 18, "diciannove": 19}
    D = {"venti": 20, "trenta": 30, "quaranta": 40, "cinquanta": 50, "sessanta": 60, "settanta": 70,
         "ottanta": 80, "novanta": 90}

    def _sotto_mille(self, w):
        if not w:
            return 0
        if w in self.U:
            return self.U[w]
        if "cento" in w:
            a, b = w.split("cento", 1)
            ca = 1 if a == "" else self.U.get(a)
            r = self._sotto_mille(b)
            return None if ca is None or r is None else ca * 100 + r
        for k, v in self.D.items():
            for pref in (k, k[:-1]):   # "ventotto", "novantuno": la vocale cade
                if w.startswith(pref):
                    r = w[len(pref):]
                    if r == "":
                        return v
                    if r in self.U and self.U[r] < 10:
                        return v + self.U[r]
        return None

    def _val(self, w):
        w = w.lower()
        if w == "mille":
            return 1000
        if w.startswith("mille"):
            r = self._sotto_mille(w[5:])
            return None if r is None else 1000 + r
        if "mila" in w:
            a, b = w.split("mila", 1)
            ca, r = self._sotto_mille(a), self._sotto_mille(b)
            return None if not ca or r is None else ca * 1000 + r
        return self._sotto_mille(w)

    def __contains__(self, w):
        return self._val(w) is not None

    def __getitem__(self, w):
        return self._val(w)


NUM_IT = _NumIT()
ESCALA_IT = {"milione": 1000000, "milioni": 1000000, "miliardo": 1000000000, "miliardi": 1000000000}


def _valor(toks, NUM, ESCALA):
    """"one hundred ten" -> 110; "twelve" -> 12; "1,300" -> 1300. Devolve None se não for número."""
    total, atual, achou = 0, 0, False
    for t in toks:
        t = t.lower().strip(",.")
        if re.fullmatch(r"\d[\d.,]*", t):
            atual = int(re.sub(r"[.,]", "", t))
            achou = True
        elif t in NUM:
            atual += NUM[t]
            achou = True
        elif t in ESCALA:
            e = ESCALA[t]
            atual = max(atual, 1) * e
            if e >= 1000:
                total += atual
                atual = 0
            achou = True
        elif t in ("and", "e", "y", "ed"):
            continue
        else:
            return None
    return (total + atual) if achou else None


def numeros(tr):
    """[(valor_na_tela, rótulo, [segundos])] — número + unidade ditos no roteiro."""
    lang = str((cfg or {}).get("screenLanguage", "en"))[:2]
    pt = lang == "pt"
    NUM, ESCALA, UNI = {"pt": (NUM_PT, ESCALA_PT, UNI_PT), "es": (NUM_ES, ESCALA_ES, UNI_ES),
                       "it": (NUM_IT, ESCALA_IT, UNI_IT)}.get(
        lang, (NUM_EN, ESCALA_EN, UNI_EN))
    palavras = [(w["s"], norm(w["w"])) for fr in tr["sentences"] for w in fr["words"]]
    achados, ordem = {}, []
    for pa in tr["paragraphs"]:
        a, z = pa["startSec"], pa["endSec"]
        janela = [(s, w) for s, w in palavras if a - 1 <= s <= z + 1]
        for fr in frases(pa["text"]):
            xs = [limpa(x) for x in fr.split()]
            i = 0
            while i < len(xs):
                j = i
                while j < len(xs) and _valor(xs[i:j + 1], NUM, ESCALA) is not None:
                    j += 1
                if j <= i:
                    i += 1
                    continue
                uni, ku = None, None
                for k in (j, j + 1):   # "one hundred ten degrees", "forty miles per hour"
                    if k < len(xs) and xs[k].lower().strip(",.") in UNI:
                        uni, ku = xs[k].lower().strip(",."), k
                        break
                v = _valor(xs[i:j], NUM, ESCALA)
                # 26/09/2026: decimal falado ("doze VÍRGULA sete bilhões") virava "R$ 7 bi" e "por CENTO ao ano"
                # virava "100 ano" (filme das revendas). Parte depois da vírgula/ponto, ou "cento" de "por cento": fora.
                antes = xs[i - 1].lower().strip(",.") if i > 0 else ""
                depois = xs[j].lower().strip(",.") if j < len(xs) else ""
                if antes in ("vírgula", "virgula", "point", "coma", "virgola", "komma", "przecinek") or                         depois in ("vírgula", "virgula", "point", "coma", "virgola", "komma", "przecinek") or                         (antes == "por" and xs[i].lower().startswith("cento")):
                    i = j
                    continue
                if not uni or v is None or v <= 1:
                    i = j
                    continue
                simb = UNI[uni]
                if simb == "R$":   # valor em dinheiro: bilhão/milhão por extenso, como se fala
                    tela = (("R$ %g bi" % round(v / 1e9, 1)) if v >= 1e9 else
                            ("R$ %g mi" % round(v / 1e6, 1)) if v >= 1e6 else
                            ("R$ %s" % f"{v:,}".replace(",", ".")))
                    tela = tela.replace(".", ",") if tela.endswith(("bi", "mi")) else tela
                    if tela not in NUMEROS_FORA:
                        achados.setdefault(tela, (NUMEROS_ROTULO.get(tela), []))
                        if tela not in ordem:
                            ordem.append(tela)
                        for alvo in (str(v), norm(xs[i]), norm(xs[ku])):
                            t0 = next((s for s, w in janela if alvo and w.startswith(alvo)), None)
                            if t0 is not None:
                                achados[tela][1].append(t0)
                                break
                    break
                fahr = not pt and simb == "°" and "fahrenheit" in " ".join(xs[ku:ku + 3]).lower()
                # separador de milhar: vírgula em inglês ("300,000"), ponto em português ("400.000"),
                # espaço em espanhol ("300 000")
                mil = f"{v:,}" if lang == "en" else f"{v:,}".replace(",", "." if lang in ("pt", "it") else " ")
                tela = mil + ("°F" if fahr else (simb if simb in ("°", "%") else f" {simb}"))
                if tela not in NUMEROS_FORA:
                    achados.setdefault(tela, (NUMEROS_ROTULO.get(tela), []))
                    if tela not in ordem:
                        ordem.append(tela)
                    # o Whisper escreve número em ALGARISMO: procura o algarismo, depois a palavra por extenso,
                    # e por último a unidade (dita logo depois do número, então o instante é praticamente o mesmo)
                    for alvo in (str(v), norm(xs[i]), norm(xs[ku])):
                        t0 = next((s for s, w in janela if alvo and w.startswith(alvo)), None)
                        if t0 is not None:
                            achados[tela][1].append(t0)
                            break
                break   # UM número por frase: "sobe dois pés a cada cem pés" não vira dois gráficos
    # se o filme disse "graus Fahrenheit" uma vez, todo grau solto vira °F (senão sai "118°" na tela)
    if any(t.endswith("°F") for t in ordem):
        junta = {}
        for t in ordem:
            k = t[:-1] + "°F" if t.endswith("°") else t
            a, b = achados[t]
            r, ts = junta.get(k, (a, []))
            junta[k] = (r or a, ts + b)
        ordem = list(dict.fromkeys((t[:-1] + "°F" if t.endswith("°") else t) for t in ordem))
        achados = junta
    return sorted([(t, achados[t][0], sorted(achados[t][1])) for t in ordem if achados[t][1]],
                  key=lambda x: x[2][0])


# ---------------------------------------------------------------- cartões em papel (src/overlays/Cartoes.tsx)
# Tabela POR FILME. `para` = parágrafo; `diz` (opcional) exige que a palavra seja falada dentro do corte.
# Tipos: cartao (foto emoldurada) | comparacao (dois cartões) | fichas (papéis espetados) | palavra (palavra
# cheia) | faixa (frase na base) | numero (algarismo no canto) | etiqueta (marcador de canto).
# `src` de foto é caminho dentro de public/ (o mesmo `file` de data/clips.json, ex.: "stock/p01efc1b6.jpg").
DOSSIE = [  # 06/11/2026 pescadores de lagosta (pt)
    {'tipo': 'ficha', 'para': 4, 'nome': 'ICAPUÍ', 'orgao': 'TERRA DA LAGOSTA DO CEARÁ', 'modo': 'revelar', 'campos': [{'rotulo': 'Pescadores', 'valor': 'cerca de 5 mil'}, {'rotulo': 'Embarcações', 'valor': '1.800'}, {'rotulo': 'Setor pesqueiro em 2023', 'valor': 'R$ 129 milhões'}], 'foto': 'stock/p27b444d2.jpg', 'carimbo': 'LAGOSTA'},
    {'tipo': 'comparacao', 'para': 7, 'titulo': 'NÃO É A LAGOSTA DO NORTE', 'a': {'src': 'stock/p0bfd7e78.jpg', 'legenda': 'ESPINHOSA · SEM GARRAS'}, 'b': {'src': 'stock/pabe6ac3b.jpg', 'legenda': 'ANTENAS LONGAS · ESPINHOS'}},
    {'tipo': 'checklist', 'para': 9, 'fundo': 'stock/p317a864e.jpg', 'titulo': 'O MANZUÁ', 'itens': [{'texto': 'engradado de varas', 'marca': 'check'}, {'texto': 'entrada em funil', 'marca': 'check'}, {'texto': 'isca dentro', 'marca': 'check'}, {'texto': 'puxado no dia seguinte', 'marca': 'check'}]},
    {'tipo': 'checklist', 'para': 22, 'fundo': 'stock/pacc01563.jpg', 'titulo': 'O COMPRESSOR, PEÇA POR PEÇA', 'itens': [{'texto': 'botijão de gás vazio', 'marca': 'check'}, {'texto': 'válvula trocada', 'marca': 'check'}, {'texto': 'correia no motor do barco', 'marca': 'check'}, {'texto': '300 m de mangueira', 'marca': 'check'}, {'texto': 'regulador de mergulho', 'marca': 'x'}]},
    {'tipo': 'lupa', 'para': 28, 'src': 'stock/p3947eb26.jpg', 'x': 0.5, 'y': 0.55, 'r': 0.25, 'rotulo': 'TAMBORES, GELADEIRAS, PNEUS', 't': 'cor'},
    {'tipo': 'ficha', 'para': 30, 'nome': 'APREENSÃO EM ACARAÚ', 'orgao': 'IBAMA + ABIN · FEVEREIRO DE 2025', 'modo': 'revelar', 'campos': [{'rotulo': 'Área', 'valor': '15.000 m²'}, {'rotulo': 'Lagosta poupada', 'valor': '300 toneladas'}, {'rotulo': 'Praia', 'valor': 'Aranaú'}], 'foto': 'stock/p4df6d4eb.jpg', 'carimbo': 'APREENDIDO'},
    {'tipo': 'antesdepois', 'para': 41, 'a': {'src': 'stock/p00dec92e.jpg', 'rotulo': 'NO FUNDO · NITROGÊNIO DISSOLVIDO'}, 'b': {'src': 'stock/p4fcc8721.jpg', 'rotulo': 'SUBIDA RÁPIDA · BOLHAS'}},
    {'tipo': 'checklist', 'para': 45, 'fundo': 'stock/p876523ae.jpg', 'titulo': 'OS SINTOMAS', 'itens': [{'texto': 'coceira e manchas', 'marca': 'check'}, {'texto': 'dor nas articulações', 'marca': 'check'}, {'texto': 'dormência nas pernas', 'marca': 'check'}, {'texto': 'vertigem', 'marca': 'check'}, {'texto': 'falta de ar', 'marca': 'check'}]},
    {'tipo': 'ficha', 'para': 50, 'nome': 'MORTE EM BARRINHA', 'orgao': 'TRIBUNAL MARÍTIMO', 'modo': 'revelar', 'campos': [{'rotulo': 'Profundidade', 'valor': 'cerca de 30 m'}, {'rotulo': 'Compressor', 'valor': 'artesanal'}, {'rotulo': 'Mergulhador', 'valor': 'sem habilitação'}], 'foto': 'stock/p298ee608.jpg', 'carimbo': 'FATAL'},
    {'tipo': 'lupa', 'para': 58, 'src': 'stock/p050588a3.jpg', 'x': 0.5, 'y': 0.5, 'r': 0.25, 'rotulo': '3 VEZES A PRESSÃO ATMOSFÉRICA', 't': 'cor'},
    {'tipo': 'ficha', 'para': 70, 'nome': 'MAIO DE 2010', 'orgao': 'MAR DE ICAPUÍ', 'modo': 'revelar', 'campos': [{'rotulo': 'Cada pescador', 'valor': 'R$ 100'}, {'rotulo': 'Lancha', 'valor': 'R$ 65 mil'}, {'rotulo': 'Alvo', 'valor': 'barcos de compressor'}], 'foto': 'stock/pbb45dec7.jpg', 'carimbo': 'GUERRA'},
    {'tipo': 'antesdepois', 'para': 75, 'a': {'src': 'stock/p0198ce7a.jpg', 'rotulo': 'NOVEMBRO A ABRIL · DEFESO'}, 'b': {'src': 'stock/p3bfa6c45.jpg', 'rotulo': 'MAIO A OUTUBRO · SAFRA'}},
    {'tipo': 'ficha', 'para': 88, 'nome': 'JAILSON JOSÉ', 'orgao': 'PESCADOR DE ICAPUÍ · JUNHO DE 2025', 'modo': 'revelar', 'campos': [{'rotulo': 'Lagosta', 'valor': '3,2 quilos'}, {'rotulo': 'Profundidade', 'valor': 'mais de 70 m'}, {'rotulo': 'Vídeo', 'valor': '170 mil visualizações'}], 'foto': 'stock/padbeb3b4.jpg', 'carimbo': 'GIGANTE'},
]


def main():
    tl = json.loads((D / "timeline.json").read_text("utf-8"))
    items = tl["items"]
    for it in items:  # sempre recalcula do zero
        it.pop("ov", None)
    if "--limpar" in sys.argv:
        (D / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), "utf-8")
        print("[ov] campo ov removido de todos os itens")
        return

    tr = json.loads((D / "master_transcript.json").read_text("utf-8"))
    palavras = [(w["s"], norm(w["w"])) for s in tr["sentences"] for w in s["words"]]
    paras = tr["paragraphs"]
    beats = json.loads((D / "beats.json").read_text("utf-8"))["beats"]
    lib = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
    cortes = [it for it in items if it["type"] == "cut"]

    def tags_de(it):
        return set(lib.get(it.get("clip") or "", {}).get("tags", []))

    def cortes_do_beat(bid):
        return [c for c in cortes if c.get("beat") == bid]

    def janela_para(pi):
        a = paras[pi]["startFrame"]
        z = paras[pi + 1]["startFrame"] if pi + 1 < len(paras) else 10 ** 9
        return a, z

    def cortes_do_para(pi):
        a, z = janela_para(pi)
        return [c for c in cortes if c["from"] < z and c["from"] + c["dur"] > a]

    def casa(spec, w):
        """"palavra|123": palavra por prefixo, algarismo exato (o Whisper escreve números em algarismo)."""
        for alt in spec.split("|"):
            a = norm(alt)
            if (w == a) if a.isdigit() else w.startswith(a):
                return True
        return False

    def fala(it, alvo):
        a, z = it["from"] / FPS, (it["from"] + it["dur"]) / FPS
        return [s for s, w in palavras if a <= s < z and casa(alvo, w)]

    def livre(it, entra, fica, gap=GAP_GERAL):
        if it.get("ov") or it["type"] != "cut" or it["dur"] < entra + fica + 6:
            return False
        t = it["from"] / FPS
        return not any(abs(t - o["from"] / FPS) < gap for o in items if o.get("ov"))

    erros, conta = [], {}

    def poe(it, ov):
        it["ov"] = ov
        conta[ov["tipo"]] = conta.get(ov["tipo"], 0) + 1

    # --- 1) slates de lugar/data (prioridade máxima: ancoram o espectador)
    for b in beats:
        if not b.get("slate"):
            continue
        cs = cortes_do_beat(b["id"])
        # beat de uma frase ("Descemos mais.") pode nem ter corte próprio: o slate entra nos 60 s seguintes ao
        # início do parágrafo — ainda é o mesmo lugar
        f0 = cs[0]["from"] if cs else paras[b["para"]]["startFrame"]
        cs = cs + [c for c in cortes if f0 < c["from"] <= f0 + 60 * FPS and c not in cs]
        for c in cs:  # corte curto (ritmo de clímax): o slate encurta até 2,5 s em vez de pular o lugar
            fica = min(SLATE[1], c["dur"] - SLATE[0] - 6)
            if fica >= 75 and livre(c, SLATE[0], fica):
                poe(c, {"tipo": "slate", "linha1": b["slate"][0], "linha2": b["slate"][1], "entra": SLATE[0], "fica": fica})
                break
        else:
            erros.append(f"slate {b['id']} {b['slate'][1]}: nenhum corte livre no beat nem nos 60 s seguintes")

    # --- 2) cartelas de capítulo em tela (a cada >= GAP_CAPITULO); todas vão para qa/chapters.md
    capitulos, ultimo_cap = [], -1e9
    # parágrafo que já tem cartão do DOSSIE não leva TAMBÉM a cartela de capítulo: o cartão é o marcador
    # (o capítulo continua na lista do YouTube, em qa/chapters.md)
    com_cartao = {d["para"] for d in DOSSIE}
    for b in beats:
        if not b.get("capitulo"):
            continue
        cs = cortes_do_beat(b["id"])
        t0 = cs[0]["from"] / FPS if cs else paras[b["para"]]["startFrame"] / FPS
        capitulos.append((t0, b["capitulo"]))
        if t0 - ultimo_cap < GAP_CAPITULO or b["para"] in com_cartao:
            continue
        for c in cs:
            if livre(c, *CAPITULO):   # nunca no mesmo plano do slate (livre() já nega corte com ov)
                poe(c, {"tipo": "capitulo", "nome": b["capitulo"], "lugar": b.get("lugar"), "entra": CAPITULO[0], "fica": CAPITULO[1]})
                ultimo_cap = t0
                break

    # --- 3) selos: o número tem de ser dito dentro do corte
    anims = [it for it in items if it["type"] == "animation"]
    for d in DADOS:
        cs = [c for c in cortes_do_para(d["para"]) if fala(c, d["diz"])]
        if not cs:
            # número dito DURANTE uma animação: a animação já é a cartela desse dado — selo desnecessário
            if any(fala(an, d["diz"]) for an in anims):
                print(f"[ov] selo p{d['para']:03d} {d['valor']}: número dito dentro da animação — sem selo")
                continue
            erros.append(f"selo p{d['para']:03d} '{d['diz']}': nenhum corte desse parágrafo tem a palavra dita dentro")
            continue
        c = next((c for c in cs if livre(c, SELO_ENTRA, int(MIN_SELO_S * FPS) - SELO_ENTRA)), None)
        if c is None:
            print(f"[ov] selo p{d['para']:03d} {d['valor']} pulado (corte curto ou gráfico perto demais)")
            continue
        poe(c, {"tipo": "selo", "rotulo": d["rotulo"], "valor": d["valor"], "nota": d.get("nota"), "entra": SELO_ENTRA})

    # --- 4) lower third na primeira menção da espécie, só se o arquivo do corte foi escolhido pela tag
    for tag, (pi, nome, detalhe) in ESPECIES.items():
        a, _ = janela_para(pi)
        def titulo_ok(c):
            src = (lib.get(c.get("clip") or "", {}).get("source") or lib.get(c.get("clip") or "", {}).get("title") or "").lower()
            return any(w in src for w in TITULO_EXIGE.get(tag, []))
        cands = [c for c in cortes if a <= c["from"] < a + 90 * FPS and tag in tags_de(c) and titulo_ok(c)]  # até 90 s da 1ª menção
        c = next((c for c in cands if livre(c, *LOWER)), None)
        if c is None:
            print(f"[ov] lower {nome}: sem corte livre com a tag {tag} perto de p{pi:03d}")
            continue
        poe(c, {"tipo": "lower", "nome": nome, "detalhe": detalhe, "entra": LOWER[0], "fica": LOWER[1]})

    # --- 5) cartões em papel da tabela DOSSIE (cada um exige corte livre no parágrafo; falta = ERRO)
    # o cartão em papel tem de caber DENTRO de um plano. No modo ULTRA a curva de ritmo encurta os cortes
    # (ASL ~4,6 s contra ~8 s do padrão), então o cartão encolhe junto — senão a regra dos 14 cartões
    # brigaria com o ritmo do próprio prompt e nenhum dos dois caberia.
    _ultra = json.loads((D / "pipeline_config.json").read_text("utf-8")).get("modo") == "ultra"
    _k = 0.72 if _ultra else 1.0
    _d = lambda e, f: (e, max(70, round(f * _k)))
    DUR = {"cartao": _d(8, 138), "comparacao": _d(8, 140), "fichas": _d(8, 145), "palavra": _d(6, 110),
           "faixa": _d(8, 130), "numero": _d(8, 110), "etiqueta": _d(8, 120), "destaque": DESTAQUE,
           "comparativo": _d(8, 140), "lower": LOWER,
           # cartões de ARQUIVO (src/overlays/Arquivo.tsx): tomam o quadro inteiro, precisam de plano de ~5 s
           "quadro": _d(6, 150), "checklist": _d(6, 150), "ficha": _d(6, 150), "manchete": _d(4, 132),
           "teletipo": _d(6, 140), "lupa": _d(4, 140), "antesdepois": _d(4, 136), "rolo": _d(4, 140), "revela": _d(4, 140),
           "planta": _d(6, 150), "caderno": _d(6, 150), "mercado": _d(6, 150), "radar": _d(6, 140), "vhs": _d(4, 140),
           **{t: _d(6, 150) for t in GENERO[5:]}}
    # cartão em papel primeiro: é o gráfico mais caro de encaixar (precisa de plano longo e livre)
    PAPEL = ("cartao", "comparacao", "fichas", "palavra") + ARQUIVO + GENERO
    # 04/10/2026 — AUTO-CORREÇÃO do DOSSIE (o preparar parava e era refeito à mão: 10 voltas no porta-aviões):
    #  a) mescla: tipo acima de MAX_UM_TIPO vira outro (fichas -> palavra com o mesmo texto; palavra -> cartão com a foto
    #     do próprio corte) — o texto e os números ditos não mudam;
    #  b) parágrafo sem corte livre: tenta os vizinhos (±2; ARQUIVO ±3) antes de desistir;
    #  c) cartão que não cabe em lugar nenhum sai com AVISO (o mínimo de cartões e a família de ARQUIVO seguem como ERRO).
    dossie = [dict(d) for d in DOSSIE]
    if ENXUTO:   # 12/10/2026: só os tipos que explicam, no máx. MAX_PAPEL, espalhados pelo filme
        _fora = Counter(d["tipo"] for d in dossie if d["tipo"] in PAPEL and d["tipo"] not in ENXUTO_TIPOS)
        dossie = [d for d in dossie if d["tipo"] not in PAPEL or d["tipo"] in ENXUTO_TIPOS]
        _pap = sorted([d for d in dossie if d["tipo"] in PAPEL], key=lambda d: d["para"])
        if len(_pap) > MAX_PAPEL:
            # mantém 1 de cada tipo obrigatório e completa espalhando pelo filme
            _keep = [next(d for d in _pap if d["tipo"] == g[0]) for g in OBRIGATORIOS if any(d["tipo"] == g[0] for d in _pap)]
            _resto = [d for d in _pap if all(d is not k for k in _keep)]
            _vagas = MAX_PAPEL - len(_keep)
            if _vagas > 0 and _resto:
                _passo = len(_resto) / _vagas
                _keep += [_resto[int(i * _passo)] for i in range(min(_vagas, len(_resto)))]
            dossie = [d for d in dossie if d["tipo"] not in PAPEL or any(d is k for k in _keep)]
        print(f"[ov] MODO ENXUTO: tirados do DOSSIE {dict(_fora)}; cartões {sum(1 for d in dossie if d['tipo'] in PAPEL)} "
              f"(mín {MIN_PAPEL}, máx {MAX_PAPEL}: só {', '.join(ENXUTO_TIPOS)})")
    auto = Counter()
    while True:
        cont = Counter(d["tipo"] for d in dossie if d["tipo"] in PAPEL)
        tot = sum(cont.values())
        if not tot:
            break
        dom, n = cont.most_common(1)[0]
        if n <= MAX_UM_TIPO * tot or dom not in ("fichas", "palavra"):
            break
        lista = [d for d in dossie if d["tipo"] == dom]
        d = lista[len(lista) // 2]          # do meio: espalha as trocas pelo filme
        if dom == "fichas":
            its = d.get("itens") or [{}]
            sub = its[0].get("texto", "") + (f" · {its[1].get('rotulo', '')}: {its[1].get('texto', '')}" if len(its) > 1 else "")
            d.update(tipo="palavra", palavra=str(its[0].get("rotulo", "")).upper(), sub=sub)
            d.pop("itens", None)
        else:
            d.update(tipo="cartao", etiqueta=str(d.get("palavra", "")).capitalize(), legenda=d.get("sub", ""), lado="centro",
                     auto_src=True)
            d.pop("palavra", None)
            d.pop("sub", None)
        auto[f"{dom}->{d['tipo']}"] += 1
    for d in sorted(dossie, key=lambda x: 0 if x["tipo"] in PAPEL else 1):
        tipo = d["tipo"]
        entra, fica = DUR[tipo]
        for campo in ("src",):  # foto tem de existir em public/ antes do render
            fotos = [d.get(k) for k in ("src", "fundo", "foto", "fg") if d.get(k)] + [x if isinstance(x, str) else x.get("src") for x in (d.get("fotos") or [])] + [x.get("src") for x in (d.get("itens") or []) if isinstance(x, dict) and x.get("src")] +                 [x.get("src") for x in (d.get("provas") or [])] + [x.get("src") for x in (d.get("a"), d.get("b")) if x]
            for alvo in [a for a in fotos if a]:
                if alvo and not (ROOT / "public" / alvo).exists():
                    erros.append(f"{tipo} p{d['para']:03d}: arquivo public/{alvo} não existe")
        cs = cortes_do_para(d["para"])
        # parágrafo de anúncio ("Número dezenove. Citroën C3...") é curto e às vezes só tem o corte da
        # cartela de capítulo: o cartão do item pode cair no começo do parágrafo seguinte, que é o mesmo item
        if d["tipo"] in ("destaque", "numero", "etiqueta", "faixa") and d["para"] + 1 < len(paras):
            a2 = paras[d["para"] + 1]["startFrame"]
            cs = cs + [c for c in cortes if a2 <= c["from"] < a2 + 25 * FPS and c not in cs]
        if d.get("diz"):
            cs = [c for c in cs if fala(c, d["diz"])]
        if d.get("auto_src"):   # cartão convertido usa a foto do próprio corte
            cs = [c for c in cs if c.get("kind") == "photo" and c.get("src")]
        # cartão em papel é gráfico GRANDE (GAP_GERAL); destaque/número/etiqueta/faixa são pequenos
        pequeno = tipo in ("destaque", "numero", "etiqueta", "faixa")
        # 28/09/2026: no ULTRA o qa.py exige 25 s entre textos grandes — o cartão em papel usa a mesma folga
        gap = GAP_DESTAQUE if pequeno else ((25 if _ultra else 18) if tipo in PAPEL else GAP_GERAL)
        c = next((c for c in cs if livre(c, entra, fica, gap)
                  and (not pequeno or not any(abs(c["from"] / FPS - o["from"] / FPS) < GAP_GRANDE for o in items
                                              if o.get("ov") and o["ov"]["tipo"] not in
                                              ("destaque", "numero", "etiqueta", "faixa")))), None)
        if c is None and not d.get("diz"):   # 04/10: tenta os parágrafos vizinhos (mesmo assunto, poucos segundos)
            alcance = 3 if tipo in ARQUIVO + GENERO else 2
            for k in [x for r in range(1, alcance + 1) for x in (r, -r)]:
                pv = d["para"] + k
                if not 0 <= pv < len(paras):
                    continue
                cs2 = [x for x in cortes_do_para(pv) if not d.get("auto_src") or (x.get("kind") == "photo" and x.get("src"))]
                c = next((x for x in cs2 if livre(x, entra, fica, gap)), None)
                if c is not None:
                    auto["movido"] += 1
                    break
        if c is None:
            auto["tirado"] += 1
            print(f"[ov] AVISO {tipo} p{d['para']:03d}: sem corte livre nem nos vizinhos — cartão tirado")
            continue
        ov = {k: v for k, v in d.items() if k not in ("para", "diz", "auto_src")}
        if d.get("auto_src"):
            ov["src"] = c["src"]
        ov["entra"], ov["fica"] = entra, fica
        poe(c, ov)

    if auto:
        print("[ov] auto-correção do DOSSIE:", dict(auto))

    # --- 5b) PARALAXE 2.5D (regra 26/09/2026): fotos com sujeito recortado por scripts/paralaxe.py (data/paralaxe.json
    # {src: fg}) viram corte em duas camadas; uma a cada PARALAXE_GAP s, só em plano de foto livre.
    plx_on = cfg.get("paralaxe", True) is not False   # 27/09 painel: "paralaxe": false desliga as fotos em 2.5D
    if plx_on and not (D / "paralaxe.json").exists():
        erros.append("paralaxe: data/paralaxe.json não existe — rodar `python scripts/paralaxe.py` (regra 26/09/2026)")
    plx = json.loads((D / "paralaxe.json").read_text("utf-8")) if plx_on and (D / "paralaxe.json").exists() else {}
    n_plx, ult_plx = 0, -1e9
    for c in cortes:
        fg = plx.get(c.get("src", ""))
        if not fg or c.get("kind") != "photo" or c["from"] / FPS - ult_plx < PARALAXE_GAP or n_plx >= PARALAXE_MAX:
            continue
        if not (ROOT / "public" / fg).exists() or not livre(c, 0, c["dur"] - 6, 10):
            continue
        poe(c, {"tipo": "paralaxe", "src": c["src"], "fg": fg, "dir": 1 if n_plx % 2 == 0 else -1, "entra": 0, "fica": c["dur"]})
        n_plx += 1
        ult_plx = c["from"] / FPS
    if plx:
        print(f"[ov] paralaxe 2.5D: {n_plx} fotos de {len(plx)} recortadas")
        if n_plx < (min(3, len(plx)) if ENXUTO else max(3, round(MINUTOS / 4))):
            erros.append(f"paralaxe: só {n_plx} fotos em 2.5D (mínimo {max(3, round(MINUTOS / 4))}) — rodar scripts/paralaxe.py com mais fotos")

    # --- 6) destaques automáticos: nome próprio / ano dito, em canto alternado
    ditos = {p.get("linha2", "").upper() for p in [o["ov"] for o in items if o.get("ov")] if p["tipo"] == "slate"}
    ditos |= {str(o["ov"].get("nome") or "").upper() for o in items if o.get("ov")}
    ditos |= {str(o["ov"].get("titulo") or "").upper() for o in items if o.get("ov")}
    ditos |= {w for t in list(ditos) for w in t.split() if len(w) > 3}   # "TESLA CYBERTRUCK" cobre "CYBERTRUCK"
    # 25/09/2026 — o destaque só entra se o NOME CASA COM A IMAGEM do corte. Nos filmes polonês e brasileiro de 24/09
    # os destaques automáticos saíam sobre a foto errada ("VOLKSWAGEN" sobre o BMW Welt, "ELETRA" sobre Jaraguá do
    # Sul, o nome do empresário sobre um Mustang) e, em polonês, declinados ("WARSZAWIE", "TYCHACH") — cada um
    # custava um re-render. Casa = o nome aparece no título do arquivo/vídeo, no canal ou na descrição das tags do
    # corte. Idioma com declinação (pl, cs, ru, uk): a palavra tem de estar EXATA ali (título do Commons vem no
    # nominativo: "Warszawa", "Tychy"); nos outros basta o começo da palavra ("COPENAGHEN" casa "Copenhagen").
    # Ano (1974, 2026) não é nome de coisa: entra sem essa checagem.
    bj_tags = json.loads((D / "beats.json").read_text("utf-8")).get("tags", {})
    declina = str((cfg or {}).get("screenLanguage", "en"))[:2] in ("pl", "cs", "ru", "uk", "sk")
    sem_acento = lambda t: "".join(ch for ch in unicodedata.normalize("NFD", str(t)) if unicodedata.category(ch) != "Mn").upper()

    def casa_com_imagem(nome, corte):
        if ANO.match(nome):
            return True
        cl = lib.get(corte.get("clip") or "", {})
        texto = sem_acento(" ".join([cl.get("title") or "", cl.get("channel") or "", cl.get("artist") or ""] +
                                    [f"{t} {bj_tags.get(t, '')}" for t in cl.get("tags", [])]))
        palavras_img = set(re.findall(r"[A-Z0-9]+", texto))
        for w in re.findall(r"[A-Z0-9]+", sem_acento(nome)):
            if len(w) < 4:
                continue
            if declina:
                if w not in palavras_img:
                    return False
            elif not any(p.startswith(w[:5]) for p in palavras_img):
                return False
        return True

    posto, cands, sem_imagem = 0, candidatos(tr), []
    for nome, sub, tempos in cands:   # 1ª menção; se aquele corte não servir, tenta as menções seguintes
        if posto >= MAX_DESTAQUES or nome in ditos:
            continue
        for seg in tempos:
            f0 = seg * FPS
            c = next((c for c in cortes if c["from"] <= f0 < c["from"] + c["dur"]), None)
            if c is None:   # dito dentro de uma animação: cai no primeiro corte logo depois (mesmo assunto)
                c = next((k for k in cortes if f0 < k["from"] <= f0 + ATRASO_MAX * FPS), None)
            if c is None or not livre(c, DESTAQUE[0], DESTAQUE[1], GAP_DESTAQUE):
                continue
            if not casa_com_imagem(nome, c):
                sem_imagem.append(nome)
                continue
            t = c["from"] / FPS   # gráfico grande manda mais: fica mais longe
            if any(abs(t - o["from"] / FPS) < GAP_GRANDE for o in items
                   if o.get("ov") and o["ov"]["tipo"] != "destaque"):
                continue
            poe(c, {"tipo": "destaque", "titulo": nome, "sub": str(sub) if sub else None,
                    "canto": CANTOS[posto % len(CANTOS)], "entra": DESTAQUE[0], "fica": DESTAQUE[1]})
            posto += 1
            break
    print(f"[ov] destaques automáticos: {posto} de {len(cands)} candidatos (teto {MAX_DESTAQUES}) | "
          f"{len(set(sem_imagem))} fora por não casar com a imagem do corte")

    # --- 7) números automáticos: valor + unidade ditos no roteiro, no canto oposto ao último destaque
    # já na tela: compara só os algarismos ("40 miles" x selo "40 miles away", "2 000 ft" x slate "2,000 FEET")
    so_num = lambda t: re.sub(r"[^0-9]", "", str(t or ""))
    ja = {so_num(x) for d in DADOS for x in (d["valor"],)} | {
        so_num(v) for o in items if o.get("ov") for v in
        (o["ov"].get("valor"), o["ov"].get("linha1"), o["ov"].get("linha2"), o["ov"].get("titulo"))}
    ja.discard("")
    posn, nums = 0, numeros(tr)
    for tela, rot, tempos in nums:
        if posn >= MAX_NUMEROS or any(so_num(tela) and so_num(tela) in j for j in ja):
            continue
        for seg in tempos:
            f0 = seg * FPS
            c = next((c for c in cortes if c["from"] <= f0 < c["from"] + c["dur"]), None)
            if c is None:
                c = next((k for k in cortes if f0 < k["from"] <= f0 + ATRASO_MAX * FPS), None)
            if c is None or not livre(c, NUMERO[0], NUMERO[1], GAP_DESTAQUE):
                continue
            t = c["from"] / FPS
            if any(abs(t - o["from"] / FPS) < GAP_GRANDE for o in items
                   if o.get("ov") and o["ov"]["tipo"] not in ("destaque", "numero")):
                continue
            poe(c, {"tipo": "numero", "valor": tela, "rotulo": rot or None,
                    "canto": CANTOS[(posto + posn) % len(CANTOS)], "entra": NUMERO[0], "fica": NUMERO[1]})
            posn += 1
            break
    print(f"[ov] números automáticos: {posn} de {len(nums)} candidatos (teto {MAX_NUMEROS})")

    PAPEL = ("cartao", "comparacao", "fichas", "palavra") + ARQUIVO + GENERO
    n_papel = sum(1 for it in items if it.get("ov", {}).get("tipo") in PAPEL)
    tipos = Counter(it["ov"]["tipo"] for it in items if it.get("ov", {}).get("tipo") in PAPEL)
    if n_papel < MIN_PAPEL:
        erros.append(f"só {n_papel} cartões em papel na tela (mínimo {MIN_PAPEL} para {MINUTOS:.0f} min): "
                     f"o DOSSIE precisa de mais cartao/comparacao/fichas/palavra — regra do usuário para TODO filme")
    _sem_gen = Counter({k: v for k, v in tipos.items() if k not in GENERO})
    if n_papel and _sem_gen and max(_sem_gen.values()) > MAX_UM_TIPO * n_papel:
        maior = _sem_gen.most_common(1)[0]
        erros.append(f"mescla pobre: {maior[0]} é {maior[1]} dos {n_papel} cartões (teto {MAX_UM_TIPO:.0%}) — "
                     f"variar entre cartao, comparacao, fichas e palavra")
    faltam = [" ou ".join(g) for g in OBRIGATORIOS if not any(tipos.get(t) for t in g)]
    if faltam and cfg.get("arquivo_dark", True) is not False:   # 27/09 painel: "arquivo_dark": false desliga a família
        erros.append(f"família de ARQUIVO incompleta: falta {', '.join(faltam)} — regra do usuário (26/09/2026) para TODO filme")
    _gen = [] if ENXUTO else [g for g in GENERO if (cfg.get("cartoes_genero") or {}).get(g)]
    if _gen:
        cada = max(3 if len(_gen) < 4 else 2, -(-MIN_GENERO // len(_gen)))   # tema inteiro ligado (7) = 2 de cada
        for g in _gen:
            if tipos.get(g, 0) < cada:
                erros.append(f"estilo '{g}' ligado no painel, mas só {tipos.get(g, 0)} cartões '{g}' (mínimo {cada}: 1 a cada "
                             f"{GENERO_A_CADA:.0f} min) — props em src/overlays/Arquivo.tsx (OvArquivo)")
        n_gen = sum(tipos.get(g, 0) for g in GENERO)
        if n_gen > MAX_GENERO * n_papel:
            erros.append(f"estilos de gênero são {n_gen} dos {n_papel} cartões (teto {MAX_GENERO:.0%}) — pôr mais cartões da família")
        # espalhado: o maior buraco sem cartão de gênero (contando início e fim) não passa do dobro do intervalo
        ts = sorted(it["from"] / FPS for it in items if it.get("ov", {}).get("tipo") in _gen)
        total_s = MINUTOS * 60
        if ts:
            marcos = [0.0] + ts + [total_s]
            buraco, onde = max((b - a, a) for a, b in zip(marcos, marcos[1:]))
            lim = 2 * total_s / max(1, MIN_GENERO)
            if buraco > lim:
                erros.append(f"estilo de gênero amontoado: {buraco / 60:.1f} min sem nenhum a partir de {onde / 60:.1f} min "
                             f"(máx {lim / 60:.1f}) — espalhar no DOSSIE")
        print(f"[ov] estilos de gênero {', '.join(_gen)}: {n_gen} cartões (meta {MIN_GENERO}, 1 a cada {GENERO_A_CADA:.0f} min)")
    cena = next((l.split('"./')[1].split('"')[0] for l in (ROOT / "src" / "scenes" / "index.ts").read_text("utf-8").splitlines()
                 if 'from "./' in l and "Scenes" in l), None)
    if cena and cfg.get("mapa", True) is not False and not re.search(r"<(MapaRota|MapaCampanha|MapaPergaminho)\b", (ROOT / "src" / "scenes" / f"{cena}.tsx").read_text("utf-8")):
        erros.append(f"nenhum mapa (MapaRota/MapaCampanha) em src/scenes/{cena}.tsx — regra do usuário: todo filme tem mapa")
    n_anim = sum(1 for b in beats if b.get("anim"))
    if n_anim > MAX_ANIM:
        erros.append(f"{n_anim} animações de tela cheia (teto {MAX_ANIM} para {MINUTOS:.0f} min): "
                     f"tirar as sobrando do scripts/beats.py e virar cartão em papel — regra do usuário")

    if erros:
        for e in erros:
            print("[ov] ERRO", e)
        if "--tolerar" not in sys.argv:   # --tolerar: só para testes com plano incompleto (grava mesmo assim)
            raise SystemExit(f"[ov] {len(erros)} erro(s) — nada foi gravado")

    (D / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), "utf-8")
    (ROOT / "qa").mkdir(exist_ok=True)
    linhas = ["00:00 Abertura"] + [f"{int(t // 60):02d}:{int(t % 60):02d} {n.title()}" for t, n in capitulos if t >= 10]
    (ROOT / "qa" / "chapters.md").write_text("\n".join(linhas) + "\n", "utf-8")
    quadros = sum(it["dur"] for it in items if it.get("ov"))
    print(f"[ov] {sum(conta.values())} sobreposições: {conta} | {quadros} quadros ({quadros / FPS:.0f} s) vão para o Remotion"
          f" | {len(linhas)} capítulos -> qa/chapters.md")
    print(f"[ov] cartões em papel: {n_papel} (mínimo {MIN_PAPEL}) {dict(tipos)} | "
          f"animações de tela cheia: {n_anim} (teto {MAX_ANIM})")


if __name__ == "__main__":
    main()
