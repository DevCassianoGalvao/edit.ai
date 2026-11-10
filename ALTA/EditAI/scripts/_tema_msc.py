"""Tema do filme "Os Maiores Navios Porta-Contêineres Feitos na China: Como Carregam Milhares de Contêineres?" (pt, 31/10/2026,
baia b1, painel 20261031-111153, seu canal). Assunto: MSC Irina (24.346 TEU, Yangzi Xinfu/Jingjiang), TEU,
peça de canto/twist lock, guias de célula, tampas, amarração, plano de estiva (baia/fileira/camada), lastro, guindastes, tripulação,
Ideal X 1956, canais, peso verificado.
REUSO: fotos/vídeos aprovados do MSC Irina pl (10/10) e it (15/10), baia b2.
Uso: python scripts/_tema_msc.py [--reuso]"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
AP = R.parent
BK = R / "_bak_tema_msc"   # cópias dos scripts ANTES deste tema

NP = 90
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "Os Maiores Navios Porta-Contêineres Feitos na China: Como Carregam Milhares de Contêineres?" (pt, 90 parágrafos com
7 pausas, 36,6 min). Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261031-111153 (seu canal,
automático, baia b1): paralaxe, mapa, sem trilha. Assunto: MSC Irina e como um porta-contêineres é carregado.
Gerado por scripts/_tema_msc.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None   # China (estaleiros), Singapura, Reino Unido (Felixstowe), Egito (Suez), Panamá, EUA (Newark)
TAGS_LUGAR = ["estaleiro", "docagem", "yangtze", "xangai", "singapura", "felixstowe", "rotterdam", "panama", "suez", "evergiven",
              "mclean", "china_fabrica"]

TAGS = {
    "irina": "the container ship MSC IRINA (2023, 24,346 TEU) or her sister ultra-large container ships MSC Tessa, MSC Loreto, MSC Gülsun, MSC Turkiye — only these MSC mega ships",
    "megaship": "any very large CONTAINER SHIP seen from outside (ultra large container vessel) at sea, in port or in a canal, loaded with stacked containers — NOT tankers, bulk carriers, cruise or naval ships",
    "container": "a single SHIPPING CONTAINER up close: corrugated steel box, doors, a 20-foot or 40-foot container on a truck, on the ground or being lifted",
    "boxes": "STACKS of shipping containers: walls of colourful containers in a terminal yard, container stacks on a quay or on a ship deck",
    "cantos": "container CORNER CASTINGS and TWIST LOCKS: close-up of the corner of a container, twist lock pins and cones, corner fitting holes",
    "amarracao": "container LASHING on a ship: lashing rods and turnbuckles, lashing bridge platforms, lashers securing containers on deck",
    "guias": "inside the HOLD of a container ship: cell guides (vertical steel rails) with containers lowered into the cells, hold interior, container being lowered into a hold",
    "escotilha": "HATCH COVERS of a container ship: giant steel hatch cover panels, a hatch cover lifted by a crane, containers stacked on hatch covers",
    "estiva": "STOWAGE / LOAD PLANNING: bay plan on screens, container loading software, a cargo planner or officer at a computer in a terminal or ship's cargo control room",
    "pesagem": "WEIGHING a container: truck weighbridge or scale at a port gate, container weight verification, weighing a loaded container",
    "reefer": "REFRIGERATED containers (reefers): reefer plugs and power sockets on a rack, reefer containers stacked with cables",
    "perigosa": "DANGEROUS GOODS containers: hazard placards and IMDG labels on containers, chemical containers, dangerous cargo markings",
    "lastro": "BALLAST and stability: ballast tank pipes and pumps, ballast water, a ship heeling / listing, draft marks on a hull, ship loading control room",
    "dragagem": "a deep DREDGED port channel and DRAFT: dredger working, a big ship in a narrow access channel, draft marks on the hull",
    "guindaste": "STS GANTRY CRANES (ship-to-shore container cranes) loading or unloading a container ship at a quay",
    "spreader": "a crane SPREADER lifting a container: the spreader frame locking onto a container, container hanging from a crane, crane cab view",
    "patio": "a CONTAINER TERMINAL YARD: rubber-tyred gantry cranes (RTG), straddle carriers, terminal tractors, automated terminal, port terminal overview",
    "caminhao": "container TRUCKS and TRAINS: a container on a lorry on a road, a container train, intermodal transport",
    "rebocador": "TUGBOATS assisting a large ship, harbour pilots and pilot boats, mooring lines at a quay",
    "estaleiro": "a Chinese SHIPYARD: hull blocks, giant gantry crane, a large ship under construction (Yangzijiang, Jiangsu, Shanghai)",
    "docagem": "a ship DRY DOCK: dry dock being flooded, hull block assembly in a dock, ship hull inside a dock",
    "yangtze": "the YANGTZE RIVER in China: the Yangtze with ships, Jiangsu river landscape, Jingjiang, Yangtze bridge",
    "xangai": "SHANGHAI port and skyline: Yangshan deep-water port, Shanghai harbour container terminal, Hudong-Zhonghua shipyard",
    "singapura": "PORT OF SINGAPORE: Singapore container terminal, ships anchored off Singapore",
    "felixstowe": "PORT OF FELIXSTOWE in England: Felixstowe container terminal and cranes",
    "rotterdam": "PORT OF ROTTERDAM container terminal (Maasvlakte, Netherlands, Europe)",
    "panama": "the PANAMA CANAL: locks, a Neopanamax ship in the expanded locks, a ship in the Miraflores locks",
    "suez": "the SUEZ CANAL: ships in the canal, desert canal, Port Said / Ismailia",
    "evergiven": "EVER GIVEN stuck in the Suez Canal (March 2021): the grounded ship, excavators and tugboats around it",
    "mclean": "the IDEAL X (1956) and Malcom McLean: the first container ship, Port Newark in the 1950s, early container shipping",
    "estivadores": "traditional BREAK-BULK cargo handling before containers: dockers / longshoremen with sacks, barrels, wooden crates, old docks",
    "acidente": "CONTAINER ACCIDENTS: containers fallen into the sea, a collapsed container stack on deck, a burning container ship, MSC Zoe containers",
    "china_fabrica": "a CHINESE FACTORY producing consumer goods or appliances: assembly line, workers, packed appliances, warehouse",
    "varejo": "a SHOP shelf or supermarket aisle with goods; people shopping; the product on the shelf at the end of the chain",
    "ponte": "the navigation BRIDGE of a merchant ship (inside): wheelhouse windows, radar and ECDIS screens, officer on watch",
    "maquinas": "a merchant ship's ENGINE ROOM: catwalks, pipes, generators, engine control room consoles, engineers in coveralls",
    "tripulacao": "merchant SEAFARERS at work on a cargo ship: crew in coveralls and hard hats on deck, mooring, maintenance",
    "conves": "the main DECK of a container ship seen from deck level: stacked containers along the deck, walkway, crew walking on deck",
    "mar": "the open OCEAN: deep blue water, waves, horizon with no land, seen from a big ship",
    "noite": "a container ship or port at NIGHT: ship lights over dark water, night watch at sea",
    "tempestade": "a STORM at sea: huge waves, spray over the bow, a container ship rolling in heavy seas, dark clouds",
}

BANCO = {"mar": ["mar_aberto", "mar_ocean", "oceano_superficie"], "noite": ["mar_noite", "porto_noite"],
         "tempestade": ["mar_tempestade", "mar_bravo"], "ponte": ["ponte_comando"], "maquinas": ["casa_maquinas"],
         "docagem": ["doca_seca"], "estaleiro": ["estaleiro"], "rebocador": ["cabo_navio"]}

REJEITA_TITULO = [r"toy\\b|toys|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|model kit|scale model|"
                  r"aquarium|cruise|princess|carnival|titanic|uss |usns|us navy|navy|warship|frigate|destroyer|aircraft carrier|"
                  r"submarine|yacht|sailing ship|q-max|\\blng\\b|tanker|icon of the seas|bulk carrier|ferry"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic", "painting"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 90 parágrafos (pausas 18, 23, 27, 35, 45, 56, 65)
"irina megaship G", "irina megaship", "container boxes", "megaship irina", "estaleiro megaship",
"yangtze estaleiro", "estaleiro estaleiro", "estaleiro estaleiro", "irina xangai C", "megaship estaleiro",
"megaship irina", "container megaship", "container container", "container boxes", "container boxes",
"container boxes", "boxes container", "megaship boxes", "megaship megaship", "boxes boxes C",
"boxes megaship", "megaship megaship", "megaship megaship", "boxes megaship", "boxes container",
"tempestade mar", "boxes megaship", "mar megaship", "ponte boxes", "ponte boxes",
"ponte megaship", "ponte ponte", "container boxes", "ponte megaship", "reefer perigosa",
"lastro megaship", "lastro megaship", "megaship megaship C", "megaship lastro", "lastro boxes",
"lastro maquinas", "lastro ponte", "guindaste lastro", "dragagem megaship", "guindaste patio",
"rebocador megaship", "rebocador megaship", "guindaste megaship", "spreader guindaste", "guindaste spreader",
"patio caminhao", "singapura felixstowe", "guindaste boxes", "patio container", "boxes megaship",
"ponte megaship", "mar noite", "tripulacao megaship", "ponte tripulacao", "ponte maquinas C",
"ponte noite", "mar noite", "maquinas ponte", "megaship tempestade", "megaship mar",
"mar megaship", "estivadores estivadores", "estivadores estivadores", "megaship estivadores", "panama suez",
"suez panama", "evergiven suez", "patio guindaste", "guindaste patio", "acidente megaship C",
"reefer boxes", "perigosa boxes", "container container", "ponte boxes", "china_fabrica caminhao",
"ponte boxes", "guindaste spreader", "lastro ponte", "mar megaship", "rotterdam patio",
"megaship mar", "xangai estaleiro", "irina megaship", "container boxes", "varejo boxes F",
]
assert len(_PT) == 90, len(_PT)
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {0, 4, 11, 19, 28, 35, 46, 57, 66, 69, 79, 87}
_REVEAL = {0, 4, 11, 19, 28, 35, 46, 57, 66, 69, 79, 87}
_ANIM = __ANIM__
_CAP = {0: ("O GIGANTE", "MSC IRINA — 24.346 TEU"),
        4: ("DO ESTALEIRO AO MAR", "JINGJIANG, CHINA"),
        11: ("A CAIXA", "CANTOS E TRAVAS"),
        19: ("PORÃO E CONVÉS", "COMO A PILHA FICA PRESA"),
        28: ("O PLANO DE ESTIVA", "BAIA, FILEIRA E CAMADA"),
        35: ("ESTABILIDADE", "CENTRO DE GRAVIDADE E LASTRO"),
        46: ("NO CAIS", "GUINDASTES E PÁTIO"),
        57: ("A TRIPULAÇÃO", "QUEM OPERA UM GIGANTE"),
        66: ("DE 58 CAIXAS A 24 MIL", "1956 ATÉ HOJE"),
        69: ("OS LIMITES", "CANAIS, PORTOS, TEMPO E RISCO"),
        79: ("O CAMINHO COMPLETO", "DA FÁBRICA À PRATELEIRA"),
        87: ("OS NÚMEROS", "MSC IRINA")}
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({NP})", s[j:])
ANIM = {2: "S01-TEU", 8: "S02-Irmaos", 29: "S03-Enderecos", 42: "S04-Lastro", 51: "S05-Recorde", 70: "S06-Canais",
        77: "S07-Peso", 87: "S08-Recap"}
(S / "beats.py").write_text(HEAD.replace("__ANIM__", repr(ANIM)) + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = (BK / "build_plan.py").read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["megaship", "boxes", "mar"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"guias", "ponte", "maquinas", "estiva", "lastro"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["ponte", "maquinas", "guias"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["megaship", "boxes", "mar"]', b, count=1, flags=re.M)
n0 = len(b)
b = re.sub(r'^SECAO_FB = \{.*?\n\}\n', 'SECAO_FB = {}\n', b, count=1, flags=re.M | re.S)
assert n0 - len(b) < 2000, "SECAO_FB regex comeu demais"
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ', '.join(repr(k).replace("'", '"') for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"S01-TEU": ["20", "40"], "S02-Irmaos": ["116", "346"], "S03-Enderecos": ["baia", "fileira", "camada"],
        "S04-Lastro": ["20", "inclinar", "esquerdo"], "S05-Recorde": ["22", "singapura"], "S06-Canais": ["panam", "suez"],
        "S07-Peso": ["2016", "confirmado"], "S08-Recap": ["400", "61", "24", "9"]}
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

(R / "src" / "scenes" / "MscScenes.tsx").write_text('''// Animações de "Os Maiores Navios Porta-Contêineres Feitos na China" (pt) — painel 20261031-111153 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\\u00a0";

// 1. o que é um TEU (p02)
export const S01TEU: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A MEDIDA DO COMÉRCIO MUNDIAL", titulo: "TEU · unidade equivalente a 20 pés", linhas: [
    { rotulo: "Contêiner curto · vale 1 TEU", valor: `20${NB}pés · ≈${NB}6${NB}m`, cue: "20", destaque: true },
    { rotulo: "Contêiner comum nos portos · vale 2 TEU", valor: `40${NB}pés · ≈${NB}12${NB}m`, cue: "40" },
  ], tint: "accent" }} />
);

// 2. dois irmãos, dois estaleiros (p08)
export const S02Irmaos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "MESMO DIA DE ENTREGA · DOIS ESTALEIROS CHINESES", titulo: "Capacidade informada", linhas: [
    { rotulo: "MSC Tessa · Hudong-Zhonghua (Xangai)", valor: `24.116${NB}TEU`, cue: "116" },
    { rotulo: "MSC Irina · Yangzi Xinfu (Jingjiang)", valor: `24.346${NB}TEU`, cue: "346", destaque: true },
  ], tint: "accent" }} />
);

// 3. o endereço de cada caixa (p29)
export const S03Enderecos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O ENDEREÇO DE CADA CAIXA", titulo: "Plano de estiva · três números", linhas: [
    { rotulo: "Primeiro número · baia", valor: "posição de proa a popa", cue: "baia" },
    { rotulo: "Segundo número · fileira", valor: "da linha central para os lados", cue: "fileira" },
    { rotulo: "Terceiro número · camada", valor: "a altura", cue: "camada", destaque: true },
  ], tint: "accent" }} />
);

// 4. o lastro compensa (p42)
export const S04Lastro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "UMA DANÇA ENTRE A CARGA E A ÁGUA", titulo: "Enquanto o guindaste trabalha", linhas: [
    { rotulo: "O guindaste coloca", valor: `20${NB}toneladas à direita`, cue: "20", destaque: true },
    { rotulo: "O navio tende a", valor: "inclinar para a direita", cue: "inclinar" },
    { rotulo: "Os oficiais bombeiam água para", valor: "tanques da esquerda", cue: "esquerdo" },
  ], tint: "accent" }} />
);

// 5. a maior carga já transportada (p51)
export const S05Recorde: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MAIOR CARGA JÁ TRANSPORTADA POR UM SÓ NAVIO" valor={22233} cue="22" sufixo=" TEU" sep="."
    nota={{ texto: "numa única viagem · Singapura → Felixstowe", cue: "singapura" }} />
);

// 6. MAPA: os canais por onde os gigantes passam (p70)
export const S06Canais: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CANAIS QUE LIMITAM O TAMANHO DO NAVIO" lugares={[
    { nome: "Canal do Panamá", lat: 9.08, lon: -79.68, cue: "panam", esquerda: true },
    { nome: "Canal de Suez", lat: 30.46, lon: 32.35, cue: "suez" },
  ]} tint={colors.accent} />
);

// 7. o peso verificado (p77)
export const S07Peso: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="2016" linhas={[
    "A PARTIR DE 2016 · REGRA INTERNACIONAL",
    "TODO CONTÊINER TEM O PESO VERIFICADO",
    "· pesando a caixa inteira",
    "· ou somando tudo que está dentro",
    "SEM O NÚMERO CONFIRMADO, NÃO EMBARCA",
  ]} chave={1} carimbo={{ texto: "PESO VERIFICADO", cue: "confirmado" }} />
);

// 8. os números do MSC Irina (p87)
export const S08Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "OS NÚMEROS DO GIGANTE", titulo: "MSC Irina", linhas: [
    { rotulo: "Comprimento", valor: `quase 400${NB}m`, cue: "400" },
    { rotulo: "Largura", valor: `61,3${NB}m`, cue: "61" },
    { rotulo: "Capacidade", valor: `24.346${NB}TEU`, cue: "24", destaque: true },
    { rotulo: "Entregue em", valor: `9${NB}de março de 2023`, cue: "9" },
  ], tint: "accent", colunas: false }} />
);
''', "utf-8")
(R / "src" / "scenes" / "index.ts").write_text('''import React from "react";
import type { SceneProps } from "./shared";
import { S01TEU, S02Irmaos, S03Enderecos, S04Lastro, S05Recorde, S06Canais, S07Peso, S08Recap } from "./MscScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: MSC Irina / porta-contêineres (pt, 31/10).
export const SCENES: Record<string, SceneEntry> = {
  "S01-TEU": { C: S01TEU, preview: 600 },
  "S02-Irmaos": { C: S02Irmaos, preview: 600 },
  "S03-Enderecos": { C: S03Enderecos, preview: 600 },
  "S04-Lastro": { C: S04Lastro, preview: 600 },
  "S05-Recorde": { C: S05Recorde, preview: 600 },
  "S06-Canais": { C: S06Canais, preview: 600 },
  "S07-Peso": { C: S07Peso, preview: 600 },
  "S08-Recap": { C: S08Recap, preview: 600 },
};
''', "utf-8")

Q = {
    "irina": ["MSC Irina", "MSC Irina container ship", "MSC Tessa", "MSC Loreto", "MSC Gülsün", "MSC Türkiye ship"],
    "megaship": ["ultra large container ship", "largest container ship", "container ship fully loaded", "container ship aerial"],
    "container": ["shipping container", "40-foot container", "20-foot container", "container doors corrugated"],
    "boxes": ["container stack terminal", "stacked shipping containers", "containers on deck ship", "container yard stacks"],
    "cantos": ["container corner casting", "twist lock container", "twistlock", "container corner fitting"],
    "amarracao": ["container lashing", "lashing rods container ship", "lashing bridge container ship", "turnbuckle lashing container"],
    "guias": ["cell guides container ship", "container ship hold", "container lowered into hold", "container cell guide"],
    "escotilha": ["hatch cover container ship", "hatch covers crane", "hatch cover lifting"],
    "estiva": ["container stowage plan", "bay plan container ship", "cargo control room ship", "container terminal planning screen"],
    "pesagem": ["container weighbridge", "weighing container truck scale", "verified gross mass container"],
    "reefer": ["reefer container plugs", "reefer containers ship", "refrigerated container"],
    "perigosa": ["dangerous goods container", "IMDG container placard", "hazmat container label"],
    "lastro": ["ship ballast tanks", "ballast water pump", "ship heeling list", "ship draft marks"],
    "dragagem": ["dredger port channel", "deep draft container ship channel", "dredging port access channel"],
    "guindaste": ["ship-to-shore crane", "container gantry crane ship", "STS crane container terminal", "container crane loading ship"],
    "spreader": ["crane spreader container", "container spreader lifting", "container crane cab view"],
    "patio": ["container terminal yard", "rubber tyred gantry crane", "straddle carrier container", "automated container terminal"],
    "caminhao": ["container truck", "container train", "intermodal container transport"],
    "rebocador": ["tugboats container ship", "tug assisting large ship", "harbour pilot boat", "pilot ladder ship"],
    "estaleiro": ["Yangzijiang Shipbuilding", "Jiangsu shipyard container ship", "Chinese shipyard", "shipyard hull block"],
    "docagem": ["shipyard dry dock", "hull block assembly shipyard", "dry dock flooded"],
    "yangtze": ["Yangtze River", "Jingjiang", "Yangtze River ships", "长江 靖江"],
    "xangai": ["Yangshan Deep-Water Port", "Shanghai port container", "Hudong-Zhonghua Shipbuilding", "Shanghai harbour"],
    "singapura": ["Port of Singapore container terminal", "Singapore port ships", "PSA Singapore"],
    "felixstowe": ["Port of Felixstowe", "Felixstowe container terminal", "Felixstowe cranes"],
    "rotterdam": ["Port of Rotterdam container terminal", "Maasvlakte container terminal", "Rotterdam port Europe"],
    "panama": ["Panama Canal locks", "Neopanamax Panama Canal", "Miraflores locks ship", "Agua Clara locks"],
    "suez": ["Suez Canal ships", "Suez Canal container ship", "Port Said Suez Canal"],
    "evergiven": ["Ever Given Suez Canal", "Ever Given grounded", "Ever Given 2021"],
    "mclean": ["Ideal X ship 1956", "Malcom McLean", "Port Newark 1956", "first container ship"],
    "estivadores": ["longshoremen break bulk cargo", "dockers sacks docks", "docker loading barrels ship", "stevedores 1950s"],
    "acidente": ["MSC Zoe containers lost", "containers overboard", "collapsed container stack ship", "container ship fire"],
    "china_fabrica": ["Chinese appliance factory", "factory assembly line China", "China factory workers", "appliance warehouse"],
    "varejo": ["supermarket shelf products", "store shelf goods", "shopping aisle"],
    "ponte": ["ship bridge ECDIS", "container ship bridge", "wheelhouse merchant ship"],
    "maquinas": ["ship engine room", "engine control room ship"],
    "tripulacao": ["seafarers deck cargo ship", "merchant seamen at work", "container ship crew"],
    "conves": ["container ship deck", "container ship main deck", "deck containers walkway"],
    "mar": ["Indian Ocean waves", "open ocean from ship"],
    "noite": ["container ship night", "ship at night sea"],
    "tempestade": ["container ship heavy seas", "ship storm waves"],
}
CATS = {"Category:MSC Irina (ship, 2023)": "irina", "Category:MSC Tessa (ship, 2023)": "irina", "Category:MSC Loreto (ship, 2023)": "irina",
        "Category:MSC Gülsün (ship, 2019)": "irina", "Category:MSC Türkiye (ship, 2023)": "irina",
        "Category:Corner castings": "cantos", "Category:Twist locks": "cantos", "Category:Container lashing": "amarracao",
        "Category:Lashing bridges": "amarracao", "Category:Hatch covers": "escotilha", "Category:Cell guides": "guias",
        "Category:Ship-to-shore gantry cranes": "guindaste", "Category:Container cranes": "guindaste",
        "Category:Container spreaders": "spreader", "Category:Rubber tyred gantry cranes": "patio",
        "Category:Straddle carriers": "patio", "Category:Container terminals": "patio",
        "Category:Yangzijiang Shipbuilding": "estaleiro", "Category:Jingjiang": "yangtze", "Category:Yangtze River": "yangtze",
        "Category:Yangshan Port": "xangai", "Category:Hudong-Zhonghua Shipbuilding": "xangai",
        "Category:Port of Singapore": "singapura", "Category:Port of Felixstowe": "felixstowe",
        "Category:Port of Rotterdam": "rotterdam", "Category:Maasvlakte": "rotterdam",
        "Category:Panama Canal": "panama", "Category:Panama Canal expansion": "panama", "Category:Suez Canal": "suez",
        "Category:Ever Given (ship, 2018)": "evergiven", "Category:Ever Given grounding": "evergiven",
        "Category:Ideal X (ship)": "mclean", "Category:Malcom McLean": "mclean", "Category:MSC Zoe (ship, 2015)": "acidente",
        "Category:Container ships lost cargo": "acidente", "Category:Reefer containers": "reefer",
        "Category:Dangerous goods containers": "perigosa", "Category:Dredgers": "dragagem", "Category:Tugboats": "rebocador",
        "Category:Ships in dry docks": "docagem", "Category:Ballast tanks": "lastro", "Category:Engine rooms": "maquinas",
        "Category:Bridges (nautical)": "ponte", "Category:Shipping containers": "container",
        "Category:Containers on ships": "boxes", "Category:Longshoremen": "estivadores"}
PEX = {"container": ["shipping container"], "boxes": ["container stack port", "shipping containers"], "megaship": ["container ship"],
       "guindaste": ["container crane port"], "patio": ["container terminal"], "caminhao": ["container truck"],
       "estaleiro": ["shipyard"], "china_fabrica": ["factory production line"], "varejo": ["supermarket shelf"],
       "mar": ["open ocean waves"], "pesagem": ["truck scale weighing"], "estiva": ["logistics planning screen"],
       "cantos": ["container lock"], "rotterdam": ["rotterdam port"], "singapura": ["singapore port"]}
NAVIO = {  # 31/10/2026 slot: MSC Irina / porta-contêineres (pt, baia b1)
    "megaship": ["container ship aerial", "container ship sailing sea"],
    "guindaste": ["container crane loading ship", "port crane container"],
    "patio": ["container terminal aerial", "straddle carrier port"],
    "boxes": ["shipping containers stack", "container yard"],
    "spreader": ["crane lifting container"],
    "rebocador": ["tugboat pushing ship", "tug ship port"],
    "mar": ["open ocean waves", "ship at sea aerial"],
    "noite": ["cargo ship night"],
    "tempestade": ["ship in storm waves"],
    "caminhao": ["container truck highway", "container train"],
    "estaleiro": ["shipyard welding", "shipyard crane ship hull"],
    "conves": ["container ship deck"],
    "china_fabrica": ["factory production line"],
}
YT = """MSC Irina container ship
MSC Irina largest container ship
MSC Irina Yangzijiang delivery
container ship loading ship-to-shore cranes timelapse
container lashing twist lock container ship
inside container ship cell guides hold
container ship stowage plan bay row tier
how container ship stability ballast works
Ever Given Suez Canal aerial
container terminal automated port
MSC Tessa container ship"""
(D / "yt_queries_msc.txt").write_text(YT + "\n", "utf-8")
DV = """conves: container ship deck cargo handling
guindaste: port crane container loading pier
rebocador: tugboat assisting large ship pier
mar: ship underway open ocean
ponte: bridge watch merchant ship mariners
maquinas: engine room merchant vessel mariners
tempestade: ship heavy seas rough weather
patio: container terminal port operations"""
(D / "dvids_queries_msc.txt").write_text(DV + "\n", "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 31/10/2026 MSC Irina porta-contêineres (pt, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)

# ---- REUSO (só na 1ª vez)
if "--reuso" in sys.argv:
    OK = set(TAGS_ALL)
    B2 = AP / "baias" / "b2"
    MAPA_IRINA = {"irina": "irina", "siostry": "irina", "vizhinjam": "irina", "kontenerowiec": "megaship", "kontenery": "boxes",
                  "dzwig": "guindaste", "port": "patio", "stocznia": "estaleiro", "singapur": "singapura", "suez": "suez",
                  "ocean": "mar", "noc": "noite", "sztorm": "tempestade", "mostek": "ponte", "maszynownia": "maquinas",
                  "holownik": "rebocador", "zaloga": "tripulacao", "pratico": "rebocador", "zoe": "acidente"}
    FONTES = [(B2 / "_decisoes_msc-irina-zaloga-pl-2026-10-10", MAPA_IRINA),
              (B2 / "_decisoes_cosi-vivono-marinai-msc-irina-it-2026-10-15", MAPA_IRINA)]
    FORA = re.compile(r"titanic|princess|cruise|carnival|royal caribbean|aida|ferry|uss |usns|navy|warship|q-max|qatar|nakilat|"
                      r"\blng\b|tanker|boi|cattle|military|marine corps|coast guard|uscg|pirate|hapag|alba|sorrento|hmm|phone", re.I)
    TETO = {"mar": 30, "noite": 16, "tempestade": 12, "ponte": 16, "maquinas": 14, "tripulacao": 10, "rebocador": 14, "megaship": 40,
            "irina": 30, "boxes": 30, "guindaste": 14, "patio": 30, "estaleiro": 10, "singapura": 8, "suez": 10, "acidente": 14}

    def jl(p, d):
        return json.loads(p.read_text("utf-8")) if p.exists() else d

    from collections import Counter
    cnt = Counter()
    pool, side = {}, {}
    api, srs, stp = {}, {}, {}
    for SRC, MAPA in FONTES:
        sp, ss = jl(SRC / "photo_pool.json", {}), jl(SRC / "photo_side.json", {})
        for t, v in ss.items():
            tag = (v.get("tags") or [""])[0]
            if v.get("verdict") != "ok" or t not in sp or tag not in MAPA or t in pool:
                continue
            tag = MAPA[tag]
            if tag not in OK or FORA.search(t + " " + (sp[t].get("desc") or "")):
                continue
            if cnt[tag] >= TETO.get(tag, 99):
                continue
            cnt[tag] += 1
            e = dict(sp[t]); e["tags"] = [tag]
            for c in ("file", "thumb_file"):
                if e.get(c):
                    e[c] = None
            if v.get("banco"):
                src = AP / "banco" / v["banco"]
                if not src.exists():
                    cnt[tag] -= 1
                    continue
                loc = R / "assets" / "banco" / Path(v["banco"]).name
                loc.parent.mkdir(parents=True, exist_ok=True)
                if not loc.exists():
                    import shutil
                    shutil.copy2(src, loc)
                e["file"] = str(loc)
            pool[t] = e
            side[t] = dict(v, tags=[tag])
        a0 = jl(SRC / "api_review.json", {})
        sp0 = jl(SRC / "stock_api_pool.json", {})
        ss0 = jl(SRC / "source_side.json", {})
        for k2, fr in a0.items():
            if k2 in api or FORA.search(json.dumps(sp0.get(k2, {}), ensure_ascii=False)):
                continue
            d2 = {q: [MAPA[t] for t in ts if t in MAPA and MAPA[t] in OK] for q, ts in fr.items()}
            d2 = {q: ts for q, ts in d2.items() if ts}
            if d2 and k2 in sp0:
                api[k2] = d2
                stp[k2] = sp0[k2]
                if k2 in ss0:
                    srs[k2] = ss0[k2]
    for nome in ("photo_pool.json", "photo_side.json"):
        if (D / nome).exists():
            (D / (nome + ".bak_antes_reuso")).write_text((D / nome).read_text("utf-8"), "utf-8")
    (D / "photo_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    (D / "photo_side.json").write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    for nome, obj in [("source_side.json", srs), ("api_review.json", api), ("stock_api_pool.json", stp),
                      ("window_rejects.json", []), ("yt_slices.json", {}), ("yt_review.json", {})]:
        (D / nome).write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    (D / "_reuso_video.json").write_text(json.dumps({"api_review": api, "source_side": srs, "stock_api_pool": stp},
                                                    ensure_ascii=False), "utf-8")
    print("fotos:", len(pool), dict(Counter(e["tags"][0] for e in pool.values())))
    print("api:", len(api), dict(Counter(t for fr in api.values() for ts in fr.values() for t in ts)))
print("tema MSC Irina porta-contêineres (pt) gravado")
