"""Tema do filme "Antes do SUS (1988): como a família sem carteira assinada se tratava quando adoecia?" (pt, 31/10/2026, baia b1,
painel 20261031-121514). Família Almeida (fictícia), Inamps (1974-1993), Santa Casa/indigente, farmácia, benzedeira/parteira,
hospital universitário, mortalidade infantil 1980 (69,1 e 97,1), Reforma Sanitária/Arouca, 8ª CNS (1986), Constituinte, art. 196
(5/10/1988), Leis 8.080/8.142 (1990), extinção do Inamps (Lei 8.689/1993), SUS.
REUSO parcial: fotos aprovadas do filme da aposentadoria (b2): Santa Casa, Congresso, INSS, dinheiro.
Uso: python scripts/_tema_sus.py [--reuso]"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
AP = R.parent
BK = R / "_bak_tema_sus"   # cópias dos scripts ANTES deste tema

NP = 58
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "Antes do SUS (1988): como a família sem carteira assinada se tratava quando adoecia?" (pt, 58 parágrafos, 22,5 min).
Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261031-121514 (baia b1): paralaxe, mapa, sem trilha.
Gerado por scripts/_tema_sus.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = "BR"
TAGS_LUGAR = ["brasilia", "santacasa", "casa_pobre", "sus", "previdencia", "ditadura", "reforma", "constituicao", "vacina", "mortalidade"]

TAGS = {
    "familia": "a poor Brazilian family at home: parents with several small children, mother and father with kids, family portrait in a humble house",
    "casa_pobre": "humble Brazilian housing: unplastered brick houses on the periphery of a big city, favela alleys, laundry hanging, poor neighbourhood in Brazil",
    "trabalho": "informal manual work in Brazil: bricklayer or construction labourer carrying cement bags, washerwoman or woman ironing clothes, street vendor, day labourer",
    "previdencia": "Brazilian social security: INSS or Inamps office, people queueing at a social security agency, work card (carteira de trabalho), pension documents",
    "crianca_doente": "a sick child: child with fever being held by mother, nurse or doctor examining a small child, child lying ill in bed",
    "rua": "a Brazilian street in rain or at night: wet street, crowded city bus, bus stop, person walking in the rain with a child",
    "santacasa": "a Santa Casa de Misericordia charity hospital in Brazil: historic hospital building, hospital corridor, nuns or old charity hospital wards",
    "fila": "a crowded public hospital waiting room or corridor: patients sitting on benches or on the floor, people queueing for care, mothers with babies waiting",
    "medico": "a doctor examining a patient: physician with stethoscope, doctor writing a prescription, nurse with a child patient, medical consultation",
    "farmacia": "a pharmacy counter: pharmacist serving a customer, medicine boxes on shelves, buying medicine at a drugstore (Brazil preferred)",
    "benzedeira": "traditional folk healing: benzedeira or rezadeira blessing a person with herbs, medicinal herbs and tea, midwife (parteira) or traditional healer, herbal remedies",
    "hospital": "a hospital building or teaching hospital: university hospital (Hospital das Clinicas), medical students with a professor, hospital exterior and ward in Brazil",
    "mae": "a woman at home in Brazil: mother cooking, ironing or caring for children, woman listening to a radio, housewife in a modest kitchen",
    "vizinhos": "community and neighbours: people of a neighbourhood helping each other, neighbours chatting in a street, community gathering in Brazil",
    "dinheiro": "money: Brazilian banknotes and coins, hands counting money, a wallet being emptied, paying at a counter",
    "mortalidade": "infant health and poverty: newborn baby, malnourished child, babies in a pediatric ward, poor children in northeast Brazil",
    "ditadura": "Brazil under military rule and the return of democracy: Diretas Ja rally, crowd with yellow shirts, 1984 protest, soldiers, the end of the military regime",
    "reforma": "Brazilian health reform movement: Sergio Arouca, Fiocruz castle, public health professionals in a conference or assembly, health conference plenary",
    "brasilia": "Brasilia government buildings: National Congress, Esplanada dos Ministerios, Planalto Palace, Supreme Federal Court building",
    "constituicao": "the Brazilian Constitution of 1988: Ulysses Guimaraes holding the Constitution, constituent assembly, law book, Supreme Federal Court (STF), legal documents",
    "sus": "Brazil's public health system SUS today: UBS health post, SUS signage, nurse and patient at a public clinic, ambulance SAMU, public hospital emergency",
    "vacina": "vaccination: nurse vaccinating a child, vaccination campaign in Brazil, vaccine syringe and vial, children lining up for vaccines",
}

BANCO = {"brasilia": ["br_brasilia", "brasilia_gov"], "dinheiro": ["br_dinheiro"], "rua": ["onibus_br"]}

REJEITA_TITULO = [r"toy\\b|toys|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|miniature|model kit|\\bcg\\b|vector|logo|covid|coronavirus|mask|pandemic"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 58 parágrafos
"previdencia mae G", "mae casa_pobre", "previdencia previdencia", "previdencia previdencia", "previdencia fila",
"mae casa_pobre", "crianca_doente rua", "previdencia fila", "santacasa fila", "santacasa fila",
"trabalho santacasa", "rua trabalho", "fila santacasa", "medico crianca_doente", "farmacia dinheiro",
"farmacia farmacia", "farmacia dinheiro", "crianca_doente casa_pobre", "mae casa_pobre", "benzedeira casa_pobre",
"benzedeira benzedeira", "benzedeira hospital", "benzedeira dinheiro", "hospital dinheiro", "hospital medico",
"santacasa farmacia", "mae mae", "casa_pobre casa_pobre", "previdencia fila", "previdencia fila",
"previdencia trabalho", "mortalidade crianca_doente", "mortalidade casa_pobre", "reforma ditadura", "ditadura ditadura",
"reforma reforma", "reforma brasilia", "reforma brasilia", "brasilia constituicao", "casa_pobre mae",
"mae mae", "constituicao brasilia C", "constituicao constituicao", "constituicao brasilia", "constituicao brasilia",
"constituicao brasilia", "previdencia fila", "sus sus", "sus crianca_doente", "sus mae",
"sus fila", "sus vacina", "vacina sus", "sus brasilia", "santacasa sus",
"santacasa benzedeira", "constituicao brasilia", "mae sus F",
]
assert len(_PT) == 58, len(_PT)
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_CAP = {0: ("A PERGUNTA", "BRASIL — ANTES DE 1988"),
        2: ("O INAMPS", "BRASIL — 1974 A 1993"),
        5: ("O PRIMEIRO EPISÓDIO", "MADRUGADA DE CHUVA"),
        8: ("A SANTA CASA", "O PAI E A PALAVRA INDIGENTE"),
        14: ("A FARMÁCIA", "O BALCÃO COMO CONSULTÓRIO"),
        18: ("A MEDICINA POPULAR", "BENZEDEIRA E PARTEIRA"),
        23: ("PAGAR DO BOLSO", "E O HOSPITAL UNIVERSITÁRIO"),
        25: ("AS PORTAS", "NENHUMA ERA UM DIREITO"),
        28: ("QUEM TINHA CARTEIRA", "TAMBÉM ESPERAVA"),
        31: ("OS NÚMEROS", "MORTALIDADE INFANTIL — 1980"),
        33: ("COMO O PAÍS MUDOU", "A REFORMA SANITÁRIA"),
        36: ("A 8ª CONFERÊNCIA", "BRASÍLIA — MARÇO DE 1986"),
        38: ("A CONSTITUINTE", "BRASÍLIA — 1987 E 1988"),
        41: ("O ARTIGO 196", "5 DE OUTUBRO DE 1988"),
        45: ("DA LEI AO SISTEMA", "1990 A 1993"),
        48: ("DEPOIS DO SUS", "A FAMÍLIA ALMEIDA"),
        54: ("A RESPOSTA", "DO FAVOR AO DIREITO")}
_FRIO = set(_CAP)
_REVEAL = set(_CAP)
_ANIM = __ANIM__
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({NP})", s[j:])
ANIM = {2: "A01-Inamps", 31: "A02-Mortalidade", 42: "A03-Artigo196", 56: "A04-Favor"}
(S / "beats.py").write_text(HEAD.replace("__ANIM__", repr(ANIM)) + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = (BK / "build_plan.py").read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["casa_pobre", "mae", "fila"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"fila", "medico", "hospital", "farmacia", "santacasa", "mae"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["fila", "medico"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["casa_pobre", "mae", "fila"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ', '.join(repr(k).replace("'", '"') for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"A01-Inamps": ["1974", "1993"], "A02-Mortalidade": ["69", "97"], "A03-Artigo196": ["196", "todos"], "A04-Favor": ["favor", "exigir"]}
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

(R / "src" / "scenes" / "SusScenes.tsx").write_text('''// Animações de "Antes do SUS (1988)" (pt) — painel 20261031-121514 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\\u00a0";
// contorno aproximado da costa do Brasil, só como referência do mapa
const COSTA: [number, number][] = [[4.5, -51.6], [1.0, -50.0], [-0.5, -48.0], [-1.5, -44.5], [-2.8, -41.0], [-3.7, -38.5], [-5.2, -35.4],
  [-8.0, -34.8], [-10.5, -36.5], [-13.0, -38.5], [-16.5, -39.0], [-20.3, -40.2], [-22.9, -41.9], [-23.0, -43.5], [-25.0, -47.9],
  [-28.0, -48.6], [-32.0, -52.2], [-33.7, -53.4]];

// 1. O Inamps (p02)
export const A01Inamps: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "INAMPS · INSTITUTO NACIONAL DE ASSISTÊNCIA MÉDICA DA PREVIDÊNCIA SOCIAL", titulo: "A grande porta da saúde pública para quem trabalhava", linhas: [
    { rotulo: "Começou a funcionar em", valor: "1974", cue: "1974" },
    { rotulo: "Funcionou até", valor: "1993", cue: "1993", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA: mortalidade infantil em 1980 (p31)
export const A02Mortalidade: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`MORTALIDADE INFANTIL · 1980 · ÓBITOS DE MENORES DE 1${NB}ANO POR MIL NASCIDOS VIVOS`} lugares={[
    { nome: `BRASIL · 69,1`, lat: -15.8, lon: -47.9, cue: "69", esquerda: true },
    { nome: `NORDESTE · 97,1`, lat: -8.0, lon: -39.5, cue: "97" },
  ]} linhas={[{ pontos: COSTA }]} tint={colors.accent} />
);

// 3. O artigo 196 (p42)
export const A03Artigo196: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="196" linhas={[
    "CONSTITUIÇÃO FEDERAL · 5 DE OUTUBRO DE 1988",
    "ARTIGO 196",
    "A SAÚDE É DIREITO DE TODOS E DEVER DO ESTADO",
    "· acesso universal e igualitário",
    "· às ações e serviços de saúde",
  ]} chave={2} carimbo={{ texto: "DIREITO DE TODOS", cue: "todos" }} />
);

// 4. Do favor ao direito (p56)
export const A04Favor: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "ARTIGO 196 · CONSTITUIÇÃO DE 1988", titulo: "A diferença para a família Almeida", linhas: [
    { rotulo: "Antes", valor: "pedir favor", cue: "favor" },
    { rotulo: "Depois", valor: "exigir um direito", cue: "exigir", destaque: true },
  ], tint: "accent" }} />
);
''', "utf-8")
(R / "src" / "scenes" / "index.ts").write_text('''import React from "react";
import type { SceneProps } from "./shared";
import { A01Inamps, A02Mortalidade, A03Artigo196, A04Favor } from "./SusScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: Antes do SUS (pt, 31/10).
export const SCENES: Record<string, SceneEntry> = {
  "A01-Inamps": { C: A01Inamps, preview: 600 },
  "A02-Mortalidade": { C: A02Mortalidade, preview: 600 },
  "A03-Artigo196": { C: A03Artigo196, preview: 600 },
  "A04-Favor": { C: A04Favor, preview: 600 },
};
''', "utf-8")

Q = {
    "familia": ["família pobre Brasil", "poor family Brazil home", "mãe e filhos casa humilde", "Brazilian family children home"],
    "casa_pobre": ["casas de tijolo sem reboco periferia", "periferia São Paulo casas", "favela beco roupa no varal", "Brazil periphery brick houses", "comunidade periferia Brasil"],
    "trabalho": ["pedreiro obra Brasil", "bricklayer Brazil construction worker", "lavadeira Brasil", "mulher passando roupa", "servente de pedreiro saco de cimento"],
    "previdencia": ["INSS agência fila", "carteira de trabalho", "Inamps", "posto do INSS", "Brazilian work card carteira de trabalho"],
    "crianca_doente": ["criança com febre", "child with fever mother", "pediatrician examining child", "sick child bed"],
    "rua": ["rua chuva noite Brasil", "ônibus lotado Brasil", "ponto de ônibus noite", "rainy night street Brazil"],
    "santacasa": ["Santa Casa de Misericórdia", "Santa Casa hospital", "Santa Casa de Misericórdia de São Paulo", "Santa Casa de Misericórdia corredor", "irmãs de caridade hospital"],
    "fila": ["fila hospital público", "sala de espera hospital Brasil", "pacientes aguardando atendimento", "crowded hospital corridor patients"],
    "medico": ["médico examinando paciente", "doctor examining patient", "médico receita", "consulta médica pediatra"],
    "farmacia": ["farmácia balcão Brasil", "farmacêutico atendendo", "pharmacy counter customer", "drogaria Brasil"],
    "benzedeira": ["benzedeira", "rezadeira benzendo", "parteira tradicional", "ervas medicinais chá", "medicina popular Brasil"],
    "hospital": ["Hospital das Clínicas", "hospital universitário", "teaching hospital medical students", "Hospital das Clínicas São Paulo"],
    "mae": ["mãe cozinhando Brasil", "mulher passando roupa", "dona de casa cozinha", "radio old woman listening", "mother kitchen Brazil"],
    "vizinhos": ["vizinhos conversando rua", "neighbours street Brazil", "mutirão comunidade", "community neighbours helping"],
    "dinheiro": ["cédulas de real", "Brazilian real banknotes", "contando dinheiro", "moedas de real"],
    "mortalidade": ["recém-nascido", "criança desnutrida Nordeste", "pediatric ward babies", "mortalidade infantil Brasil", "sertão nordestino crianças"],
    "ditadura": ["Diretas Já 1984", "comício Diretas Já", "ditadura militar Brasil", "Brazilian military regime 1970s", "Diretas Já Praça da Sé"],
    "reforma": ["Sergio Arouca", "Fiocruz castelo", "Reforma Sanitária", "VIII Conferência Nacional de Saúde", "Fiocruz Manguinhos"],
    "brasilia": ["Congresso Nacional Brasília", "Esplanada dos Ministérios", "Palácio do Planalto", "Supremo Tribunal Federal"],
    "constituicao": ["Constituição de 1988", "Ulysses Guimarães Constituição", "Assembleia Nacional Constituinte", "Constituição Federal 1988 livro", "Supremo Tribunal Federal plenário"],
    "sus": ["Sistema Único de Saúde", "Unidade Básica de Saúde", "posto de saúde SUS", "SAMU ambulância", "Unidade de Pronto Atendimento"],
    "vacina": ["vacinação criança Brasil", "campanha de vacinação", "enfermeira vacinando", "Zé Gotinha"],
}
CATS = {"Category:Santa Casa de Misericórdia de São Paulo": "santacasa", "Category:Santa Casa de Misericórdia": "santacasa",
        "Category:Santas Casas de Misericórdia": "santacasa", "Category:Fiocruz": "reforma", "Category:Sérgio Arouca": "reforma",
        "Category:Castelo Mourisco da Fiocruz": "reforma", "Category:Diretas Já": "ditadura", "Category:Brazilian military dictatorship": "ditadura",
        "Category:Constitution of Brazil of 1988": "constituicao", "Category:Ulysses Guimarães": "constituicao",
        "Category:Supreme Federal Court": "constituicao", "Category:Sistema Único de Saúde": "sus",
        "Category:Unidades Básicas de Saúde": "sus", "Category:SAMU": "sus", "Category:Vaccination in Brazil": "vacina",
        "Category:Zé Gotinha": "vacina", "Category:Instituto Nacional do Seguro Social": "previdencia",
        "Category:Hospital das Clínicas da Faculdade de Medicina da Universidade de São Paulo": "hospital",
        "Category:Carteira de Trabalho e Previdência Social": "previdencia", "Category:Brazilian real": "dinheiro",
        "Category:Banknotes of Brazil": "dinheiro", "Category:Coins of Brazil": "dinheiro",
        "Category:National Congress of Brazil": "brasilia", "Category:Esplanada dos Ministérios": "brasilia"}
PEX = {"farmacia": ["pharmacy counter", "pharmacist customer"], "medico": ["doctor examining patient", "pediatrician child"],
       "crianca_doente": ["sick child fever", "mother holding sick child"], "fila": ["hospital waiting room", "patients waiting hospital"],
       "benzedeira": ["herbal tea healer", "medicinal herbs"], "mae": ["mother ironing clothes", "woman cooking kitchen"],
       "dinheiro": ["counting money coins"], "vacina": ["child vaccination nurse"], "trabalho": ["bricklayer construction worker"],
       "casa_pobre": ["favela brazil", "brick houses poor neighborhood"], "rua": ["rainy night street", "crowded bus"],
       "mortalidade": ["newborn baby hospital"], "sus": ["health clinic nurse", "ambulance emergency"]}
NAVIO = {  # 31/10/2026 slot: Antes do SUS (pt, baia b1)
    "fila": ["hospital waiting room", "patients waiting hospital corridor"],
    "farmacia": ["pharmacy counter", "pharmacist medicine shelf"],
    "medico": ["doctor examining child", "pediatrician checkup"],
    "crianca_doente": ["sick child fever", "mother caring sick child"],
    "casa_pobre": ["favela brazil aerial", "poor neighborhood brick houses"],
    "rua": ["rainy night street", "crowded bus night city"],
    "trabalho": ["bricklayer building wall", "construction workers brazil"],
    "mae": ["woman ironing clothes", "mother cooking kitchen"],
    "benzedeira": ["herbal tea preparation", "medicinal herbs hands"],
    "vacina": ["child vaccination nurse", "vaccine injection arm"],
    "dinheiro": ["counting money coins"],
    "sus": ["ambulance emergency", "health clinic nurse patient"],
    "hospital": ["hospital corridor", "hospital exterior"],
}
YT = """Santa Casa de Misericórdia história hospital
Reforma Sanitária Sérgio Arouca documentário
VIII Conferência Nacional de Saúde 1986
Constituinte 1988 Ulysses Guimarães promulgação da Constituição
história do SUS documentário
Inamps história saúde antes do SUS
Brasil anos 80 imagens de arquivo periferia
benzedeira parteira medicina popular Brasil
mortalidade infantil Brasil anos 80 Nordeste
Diretas Já 1984 comício
"""
(D / "yt_queries_sus.txt").write_text(YT, "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 31/10/2026 Antes do SUS (pt, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)

# ---- REUSO parcial (só na 1ª vez): aposentadoria (b2)
if "--reuso" in sys.argv:
    SRC = AP / "baias" / "b2" / "_decisoes_ate-1923-aposentadoria-pt-2026-10-29"
    MAPA = {"caridade": "santacasa", "inss": "previdencia", "congresso": "brasilia", "dinheiro": "dinheiro"}
    OK = set(TAGS_ALL)
    pool, side = {}, {}
    jl = lambda p, d: json.loads(p.read_text("utf-8")) if p.exists() else d
    sp, ss = jl(SRC / "photo_pool.json", {}), jl(SRC / "photo_side.json", {})
    from collections import Counter
    cnt = Counter()
    for t, v in ss.items():
        tag = (v.get("tags") or [""])[0]
        if v.get("verdict") != "ok" or t not in sp or tag not in MAPA or MAPA[tag] not in OK:
            continue
        tag = MAPA[tag]
        e = dict(sp[t]); e["tags"] = [tag]
        for c in ("file", "thumb_file"):
            if e.get(c):
                e[c] = None
        if v.get("banco"):
            src = AP / "banco" / v["banco"]
            if not src.exists():
                continue
            loc = R / "assets" / "banco" / Path(v["banco"]).name
            loc.parent.mkdir(parents=True, exist_ok=True)
            if not loc.exists():
                import shutil
                shutil.copy2(src, loc)
            e["file"] = str(loc)
        cnt[tag] += 1
        pool[t] = e
        side[t] = dict(v, tags=[tag])
    for nome in ("photo_pool.json", "photo_side.json"):
        if (D / nome).exists():
            (D / (nome + ".bak_antes_reuso")).write_text((D / nome).read_text("utf-8"), "utf-8")
    (D / "photo_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    (D / "photo_side.json").write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    for nome, obj in [("source_side.json", {}), ("api_review.json", {}), ("stock_api_pool.json", {}),
                      ("window_rejects.json", []), ("yt_slices.json", {}), ("yt_review.json", {})]:
        (D / nome).write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    print("fotos reusadas:", len(pool), dict(cnt))
print("tema Antes do SUS (pt) gravado")
