"""Tema do filme "Motor de Popa Elétrico Dá Conta de Pescaria? O Que Troca e o Que Não Troca" (pt, 29/10/2026, baia b1,
painel 20261029-132218). Elétrico (Torqeedo/ePropulsion) x gasolina (Tohatsu/Mercury/Yamaha): preço, autonomia, recarga,
custo, manutenção, peso, velocidade, ruído, onde serve e onde não serve, bateria, segurança, regra da metade.
Sem reuso (assunto novo). Uso: python scripts/_tema_popa.py"""
import json, re, shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
BK = R / "_bak_tema_popa"   # cópias dos scripts ANTES deste tema

NP = 108
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "Motor de Popa Elétrico Dá Conta de Pescaria? O Que Troca e o Que Não Troca" (pt, 108 parágrafos, 34,7 min).
Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261029-132218 (militar, baia b1): paralaxe, mapa, sem trilha.
Assunto: motor de popa elétrico x a gasolina na pescaria (preço, autonomia, recarga, custo, peso, ruído, onde serve).
Gerado por scripts/_tema_popa.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None
TAGS_LUGAR = []

TAGS = {
    "motor_eletrico": "an electric outboard motor (Torqeedo, ePropulsion or similar) mounted on the transom of a small boat: slim electric motor with a tiller, lithium battery, display",
    "motor_gasolina": "a gasoline outboard motor (Yamaha, Mercury, Tohatsu, Honda, Suzuki) on the back of a small boat: petrol outboard engine with cowling and propeller",
    "barco_aluminio": "a small aluminum fishing boat (jon boat or skiff) on a lake or river, seen from the side or from the water",
    "pescador": "an angler fishing from a small boat: a man casting a rod or holding a fishing rod on a river or reservoir",
    "represa": "a calm reservoir or lake with small boats: still water, shoreline, fishing boats near a dam lake",
    "rio": "a river seen from a boat: calm river with forested banks, small boat on the water",
    "bateria": "a lithium marine battery pack or large battery for a boat motor: battery with cables and terminals",
    "carregador": "charging a battery: charger, power cable plugged into a wall outlet, extension cord, charging at home or on a dock",
    "posto": "refueling with gasoline: a red fuel can or jerrycan, filling a boat or outboard tank at a dock or gas station",
    "manutencao": "servicing an outboard engine: mechanic working on a motor, spark plug, carburetor, tools and engine parts on a workbench",
    "helice": "a boat propeller close up: outboard propeller blades, lower unit of a motor, prop in the water",
    "silencio": "quiet dawn on a misty lake: still water, fog, a lone boat gliding silently, peaceful nature",
    "peixe": "a freshly caught fish held by a fisherman, bass, tilapia or catfish, fish in a net or a cooler with ice",
    "marcoaberto": "open sea with big waves and a small boat in rough weather, ocean swell, stormy water",
    "caiaque": "a kayak or small canoe used for fishing on calm water, paddle, small lightweight boat",
    "dinheiro": "money and prices: cash bills, dollar notes, price tags, coins, a wallet, paying for something",
    "calculadora": "doing the math: a calculator, notebook with numbers, pen, accounting sheet, spreadsheet on a desk",
    "balanca": "weight: carrying a heavy motor or battery, lifting equipment onto a boat, a scale showing kilos",
    "gps": "marine GPS chartplotter or smartphone navigation on a boat dashboard, digital display showing speed and route",
    "lancha": "a fast planing boat or speedboat cruising with a wake, powerboat at speed on a lake or river",
    "fogo": "fire hazard: flames, a burning boat or battery fire, firefighter extinguisher, smoke",
    "manguezal": "mangrove channel or sheltered bay: small boat in a mangrove creek, estuary canal with green vegetation",
    "correnteza": "a strong river current: fast brown river, rapids, a boat against the flow, flood water",
    "acampamento": "a fishing camp by a river or lake: tent, campfire, camp stove, tarp, remote riverbank camp",
    "solar": "solar panel charging: portable solar panel, portable generator, power station on a boat or camp",
    "remo": "oars and paddles in a small boat: rowing a boat, wooden oars resting on the gunwale",
    "gelo": "a cooler box full of ice and fish on a boat, fishing gear, tackle box, equipment loaded in a boat",
    "pescador_vive": "a professional river fisherman at work with a small wooden or aluminum boat and nets, working fishermen at dawn",
}

BANCO = {}

REJEITA_TITULO = [r"toy\\b|toys|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|"
                  r"tamiya|miniature|model kit|scale model|cg\\b|blueprint|vector|logo|rc boat|model boat|remote control"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic", "painting"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 108 parágrafos
"motor_eletrico dinheiro G", "dinheiro motor_eletrico G", "motor_gasolina motor_eletrico", "motor_eletrico dinheiro", "dinheiro barco_aluminio",
"pescador barco_aluminio", "motor_eletrico motor_gasolina", "motor_eletrico bateria", "motor_eletrico helice", "motor_gasolina motor_eletrico",
"bateria represa", "motor_gasolina barco_aluminio", "bateria motor_eletrico", "bateria represa", "bateria pescador",
"bateria remo", "motor_gasolina bateria", "carregador", "carregador bateria", "acampamento carregador",
"carregador dinheiro", "carregador posto", "posto dinheiro", "dinheiro posto", "dinheiro motor_eletrico",
"dinheiro calculadora", "calculadora dinheiro", "calculadora pescador", "bateria calculadora", "dinheiro motor_eletrico C",
"manutencao", "manutencao dinheiro", "motor_eletrico helice", "motor_gasolina manutencao", "balanca",
"motor_gasolina balanca", "motor_eletrico balanca", "balanca barco_aluminio", "motor_eletrico motor_gasolina", "caiaque motor_eletrico",
"motor_gasolina motor_eletrico", "caiaque barco_aluminio", "rio barco_aluminio", "lancha motor_gasolina", "gps rio",
"lancha motor_gasolina", "lancha gps", "silencio pescador", "silencio represa", "motor_eletrico silencio",
"represa silencio", "silencio pescador", "pescador gps", "rio pescador", "represa pescador",
"manguezal pescador", "caiaque pescador", "gps rio", "gps rio", "gelo barco_aluminio",
"correnteza rio", "marcoaberto", "acampamento solar", "pescador_vive", "manutencao motor_eletrico",
"dinheiro posto", "dinheiro posto", "calculadora dinheiro", "bateria", "bateria motor_eletrico",
"bateria calculadora", "bateria", "bateria gps", "fogo", "fogo posto",
"bateria fogo", "gps remo", "remo bateria", "represa barco_aluminio", "represa gps",
"calculadora gps", "motor_eletrico motor_gasolina", "silencio dinheiro", "motor_gasolina gps", "motor_eletrico silencio",
"pescador represa", "pescador barco_aluminio", "pescador_vive rio", "motor_gasolina dinheiro", "dinheiro motor_gasolina",
"posto dinheiro", "motor_gasolina dinheiro", "bateria motor_eletrico", "remo", "calculadora",
"dinheiro motor_eletrico", "posto motor_gasolina", "manutencao motor_eletrico", "bateria", "balanca motor_eletrico",
"silencio motor_eletrico", "motor_gasolina motor_eletrico", "pescador", "rio represa F", "gps calculadora",
"gps calculadora", "pescador barco_aluminio F", "represa pescador F"
]
assert len(_PT) == 108, len(_PT)
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {0, 6, 10, 22, 30, 34, 42, 47, 52, 57, 68, 73, 78, 81, 94, 102}
_REVEAL = {0, 6, 10, 22, 30, 34, 42, 47, 52, 57, 68, 73, 78, 81, 94, 102}
_ANIM = __ANIM__
_CAP = {0: ("O PREÇO", "ELÉTRICO X GASOLINA"),
        6: ("POR DENTRO", "WATTS X CAVALOS"),
        10: ("AUTONOMIA E RECARGA", "A BATERIA MANDA"),
        22: ("O CUSTO DE USAR", "DEZ ANOS DE CONTAS"),
        30: ("MANUTENÇÃO", "ONDE O ELÉTRICO BRILHA"),
        34: ("O PESO", "MOTOR MAIS BATERIA"),
        42: ("VELOCIDADE", "VELOCIDADE DE CASCO"),
        47: ("O RUÍDO", "SILÊNCIO NA ÁGUA"),
        52: ("ONDE SERVE", "RIO, REPRESA E MARGEM"),
        57: ("ONDE NÃO SERVE", "DISTÂNCIA, CARGA E MAR"),
        68: ("A BATERIA", "O CUSTO ESCONDIDO"),
        73: ("SEGURANÇA", "FOGO E A REGRA DA METADE"),
        78: ("A CONTA NA PRÁTICA", "OITO QUILÔMETROS X VINTE"),
        81: ("O QUE TROCA", "E O QUE NÃO TROCA"),
        94: ("OS NÚMEROS", "A REGRA PARA GUARDAR"),
        102: ("O VEREDITO", "DÁ CONTA OU NÃO DÁ")}
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({NP})", s[j:])
ANIM = {2: "P01-Precos", 18: "P02-Recarga", 23: "P03-Gasto", 31: "P04-Manut", 37: "P05-Peso", 65: "P06-Conta",
        69: "P07-Bateria", 78: "P08-Exemplo", 89: "P09-Grandes"}
(S / "beats.py").write_text(HEAD.replace("__ANIM__", repr(ANIM)) + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = (BK / "build_plan.py").read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["pescador", "barco_aluminio", "represa"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"carregador", "calculadora", "manutencao", "dinheiro", "balanca"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["calculadora", "dinheiro"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["pescador", "barco_aluminio", "represa"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ', '.join(repr(k).replace("'", '"') for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"P01-Precos": ["6", "7", "4"], "P02-Recarga": ["350", "12", "4"], "P03-Gasto": ["600", "24", "6", "240"],
        "P04-Manut": ["100", "300", "300"], "P05-Peso": ["37", "57", "20"], "P06-Conta": ["3", "12", "200", "2"],
        "P07-Bateria": ["5", "4", "48"], "P08-Exemplo": ["8", "5", "2", "3"], "P09-Grandes": ["8", "29", "12", "37"]}
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

# DOSSIE vazio (escrito depois das fotos aprovadas)
bo = (BK / "build_overlays.py").read_text("utf-8")
a0 = bo.index("DOSSIE = [")
a1 = bo.index("\n]\n", a0) + 3
bo = bo[:a0] + "DOSSIE = [  # 29/10/2026 motor de popa elétrico (pt) — preenchido depois das fotos\n]\n" + bo[a1:]
(S / "build_overlays.py").write_text(bo, "utf-8")

Q = {
    "motor_eletrico": ["electric outboard motor", "Torqeedo Cruise outboard", "ePropulsion Spirit outboard", "electric outboard boat", "Torqeedo Travel"],
    "motor_gasolina": ["outboard motor", "Yamaha outboard motor", "Mercury outboard 6 hp", "Tohatsu outboard", "small outboard engine boat"],
    "barco_aluminio": ["aluminum fishing boat", "jon boat", "aluminium boat lake", "small fishing boat outboard"],
    "pescador": ["fishing from a boat", "angler boat river", "fisherman boat lake", "pescador barco rio"],
    "represa": ["reservoir lake boats", "represa pescaria", "lake fishing boat morning", "represa barco"],
    "rio": ["river boat fishing", "rio barco pescador", "calm river boat", "small boat river"],
    "bateria": ["marine lithium battery", "lithium boat battery", "deep cycle battery boat", "battery pack lithium"],
    "carregador": ["battery charger plug", "charging battery outlet", "extension cord charging", "power cable plug socket"],
    "posto": ["gasoline can refueling boat", "fuel can outboard", "jerrycan fuel", "refueling boat dock"],
    "manutencao": ["outboard motor repair", "spark plug engine", "mechanic engine workshop", "carburetor cleaning"],
    "helice": ["boat propeller", "outboard propeller", "propeller blades close up"],
    "silencio": ["misty lake morning boat", "dawn lake fog boat", "quiet lake sunrise boat"],
    "peixe": ["bass fish caught", "fisherman holding fish", "tilapia fishing", "fish cooler ice"],
    "marcoaberto": ["small boat rough sea", "ocean waves boat", "stormy sea fishing boat"],
    "caiaque": ["kayak fishing", "canoe small motor", "fishing kayak lake"],
    "dinheiro": ["dollar bills cash", "money bills hand", "price tag", "cash dollars"],
    "calculadora": ["calculator notebook desk", "accounting calculator numbers", "budget notebook calculator"],
    "balanca": ["carrying outboard motor", "lifting heavy battery", "bathroom scale weight", "man carrying motor boat"],
    "gps": ["marine GPS chartplotter", "boat dashboard GPS", "fishfinder display boat", "smartphone navigation boat"],
    "lancha": ["speedboat lake", "powerboat planing", "fast boat wake", "lancha velocidade"],
    "fogo": ["boat fire", "battery fire", "fire extinguisher", "lithium battery fire"],
    "manguezal": ["mangrove channel boat", "mangrove creek boat", "manguezal barco", "estuary small boat"],
    "correnteza": ["fast river current", "river rapids boat", "flooded river brown water"],
    "acampamento": ["riverside camp tent", "fishing camp", "camping lake tent", "campfire river"],
    "solar": ["portable solar panel", "portable power station", "solar panel boat", "generator camp"],
    "remo": ["rowing boat oars", "oars boat", "paddle boat lake"],
    "gelo": ["cooler ice fish", "fishing gear boat", "tackle box", "cooler box boat"],
    "pescador_vive": ["river fisherman net boat", "artisanal fisherman dawn", "pescador artesanal rio", "fisherman wooden boat river"],
}
CATS = {"Category:Outboard motors": "motor_gasolina", "Category:Yamaha outboard motors": "motor_gasolina",
        "Category:Mercury Marine": "motor_gasolina", "Category:Tohatsu": "motor_gasolina", "Category:Torqeedo": "motor_eletrico",
        "Category:Electric outboard motors": "motor_eletrico", "Category:Electric boats": "motor_eletrico",
        "Category:Jon boats": "barco_aluminio", "Category:Aluminium boats": "barco_aluminio", "Category:Recreational fishing": "pescador",
        "Category:Fishing from boats": "pescador", "Category:Angling": "pescador", "Category:Fishing in Brazil": "pescador_vive",
        "Category:Artisanal fishing": "pescador_vive", "Category:Reservoirs in Brazil": "represa", "Category:Lakes of Brazil": "represa",
        "Category:Lithium-ion batteries": "bateria", "Category:Marine batteries": "bateria", "Category:Battery chargers": "carregador",
        "Category:Jerrycans": "posto", "Category:Boat propellers": "helice", "Category:Propellers": "helice",
        "Category:Kayak fishing": "caiaque", "Category:Fishing kayaks": "caiaque", "Category:Oars": "remo", "Category:Rowing boats": "remo",
        "Category:Mangroves in Brazil": "manguezal", "Category:Chartplotters": "gps", "Category:Marine electronics": "gps",
        "Category:Speedboats": "lancha", "Category:Coolers": "gelo", "Category:Portable solar panels": "solar",
        "Category:Rapids": "correnteza", "Category:Fishing camps": "acampamento", "Category:Fire extinguishers": "fogo",
        "Category:Boat fires": "fogo"}
PEX = {"motor_eletrico": ["electric outboard motor", "electric boat motor"], "motor_gasolina": ["outboard motor", "boat engine"],
       "barco_aluminio": ["aluminum boat fishing", "small fishing boat"], "pescador": ["fishing boat man", "fisherman boat"],
       "represa": ["lake boat fishing", "reservoir boat"], "rio": ["river boat", "boat river forest"],
       "bateria": ["lithium battery", "battery pack"], "carregador": ["charging cable plug", "power outlet plug"],
       "posto": ["fuel can", "gas can refuel"], "manutencao": ["engine repair", "mechanic tools engine"],
       "helice": ["boat propeller"], "silencio": ["misty lake boat", "lake fog sunrise"], "peixe": ["fish caught", "fisherman fish"],
       "marcoaberto": ["rough sea boat", "stormy ocean waves"], "caiaque": ["kayak fishing", "fishing canoe"],
       "dinheiro": ["dollar bills", "cash money"], "calculadora": ["calculator desk", "budget notebook"],
       "balanca": ["carrying heavy motor", "lifting equipment boat"], "gps": ["boat gps display", "fish finder"],
       "lancha": ["speedboat lake", "powerboat wake"], "fogo": ["fire extinguisher", "boat fire"],
       "manguezal": ["mangrove boat", "mangrove river"], "correnteza": ["river rapids", "fast river water"],
       "acampamento": ["camp by river tent", "campfire lake"], "solar": ["portable solar panel", "power station camping"],
       "remo": ["rowing boat oars", "oars boat"], "gelo": ["cooler ice fish", "tackle box"],
       "pescador_vive": ["river fisherman", "fisherman net boat"]}
NAVIO = {
    "motor_eletrico": ["electric outboard motor", "electric boat motor lake"],
    "motor_gasolina": ["outboard motor boat", "boat engine outboard"],
    "barco_aluminio": ["aluminum fishing boat", "small boat lake"],
    "pescador": ["fisherman boat", "fishing from boat lake"],
    "represa": ["lake boats drone", "reservoir aerial"],
    "rio": ["river boat", "boat river drone"],
    "silencio": ["misty lake boat", "boat sunrise lake"],
    "lancha": ["speedboat lake", "powerboat wake"],
    "marcoaberto": ["rough sea boat", "stormy waves boat"],
    "caiaque": ["kayak fishing", "canoe lake"],
    "correnteza": ["river rapids boat", "fast river"],
    "manguezal": ["mangrove boat", "mangrove river drone"],
    "acampamento": ["camp by lake", "campfire river"],
    "carregador": ["charging cable plug", "plug outlet"],
    "posto": ["fuel can refuel", "gas station pump"],
    "gps": ["boat gps", "chartplotter"],
}
YT = """electric outboard motor review fishing
Torqeedo Cruise 3.0 test
ePropulsion Spirit 1.0 Evo electric outboard
electric outboard vs gas outboard
electric outboard motor jon boat fishing
motor de popa elétrico pescaria
motor elétrico de popa Torqeedo Travel
electric outboard range test lake
"""
(D / "yt_queries_popa.txt").write_text(YT, "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 29/10/2026 motor de popa elétrico (pt, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)

# cenas + registro
NB = chr(160)
sc = '''// Animações de "Motor de Popa Elétrico Dá Conta de Pescaria?" (pt, enxuto) — painel 20261029-132218 (b1).
// REGRA: biblioteca (Painel); motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { Painel } from "./Painel";
import { SceneProps } from "./shared";

const NB = "@@NB@@";

// 1. Preços na classe de 6 cavalos (p02)
export const P01Precos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Classe de 6${NB}cavalos · gasolina custava US$${NB}1.900`, titulo: "Quanto custava o elétrico", linhas: [
    { rotulo: "ePropulsion, com bateria e carregador", valor: `US$${NB}6.100`, cue: "6" },
    { rotulo: "Torqeedo, com bateria e carregador", valor: `US$${NB}7.896`, cue: "7", destaque: true },
    { rotulo: "Só de diferença sobre a gasolina", valor: `US$${NB}4.200 a 6.000`, cue: "4" },
  ], tint: "accent" }} />
);

// 2. Tempo de recarga (p18)
export const P02Recarga: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Torqeedo Cruise · carregador padrão de 350${NB}W`, titulo: "Quanto leva para encher a bateria", linhas: [
    { rotulo: "Carregador padrão", valor: `12${NB}horas`, cue: "12", destaque: true },
    { rotulo: "Carregadores mais rápidos", valor: `4 a 6${NB}horas`, cue: "4" },
  ], tint: "cool" }} />
);

// 3. Gasto de combustível: 1 ano e 10 anos (p23)
export const P03Gasto: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mercury a gasolina x Torqeedo elétrico", titulo: "Energia gasta no uso", linhas: [
    { rotulo: "Gasolina · 1 ano", valor: `US$${NB}600`, cue: "600" },
    { rotulo: "Eletricidade · 1 ano", valor: `US$${NB}24`, cue: "24" },
    { rotulo: "Gasolina · 10 anos", valor: `US$${NB}6.006`, cue: "6", destaque: true },
    { rotulo: "Eletricidade · 10 anos", valor: `US$${NB}240`, cue: "240" },
  ], tint: "cool" }} />
);

// 4. Manutenção do a gasolina (p31)
export const P04Manut: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Motor a gasolina · manutenção", titulo: "O que o a gasolina cobra", linhas: [
    { rotulo: `Revisão a cada 100 a 150${NB}horas`, valor: `US$${NB}200`, cue: "100" },
    { rotulo: `Impelidor a cada 300${NB}horas`, valor: `US$${NB}200`, cue: "300" },
    { rotulo: "Estimativa por ano", valor: `US$${NB}300`, cue: "300", destaque: true },
  ], tint: "accent" }} />
);

// 5. Peso do conjunto (p37)
export const P05Peso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Peso do conjunto pronto para pescar", titulo: "Gasolina x elétrico", linhas: [
    { rotulo: "A gasolina, com o tanque", valor: `37${NB}kg`, cue: "37" },
    { rotulo: "O elétrico, com a bateria", valor: `57${NB}kg`, cue: "57", destaque: true },
    { rotulo: "Diferença", valor: `20${NB}kg`, cue: "20" },
  ], tint: "cool" }} />
);

// 6. A conta do pescador de rio (p65)
export const P06Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Pescador de rio · 6${NB}horas por dia`, titulo: "A conta da gasolina", linhas: [
    { rotulo: "Galões por dia", valor: "3", cue: "3" },
    { rotulo: "Combustível por dia", valor: `US$${NB}12`, cue: "12" },
    { rotulo: "Dias de pesca por ano", valor: "200", cue: "200" },
    { rotulo: "Gasolina por ano", valor: `US$${NB}2.400`, cue: "2", destaque: true },
  ], tint: "accent" }} />
);

// 7. Motor e bateria do Torqeedo Cruise (p69)
export const P07Bateria: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Torqeedo Cruise · o custo escondido", titulo: "A bateria pesa no preço", linhas: [
    { rotulo: "Motor", valor: `US$${NB}5.759`, cue: "5" },
    { rotulo: "Bateria sozinha", valor: `US$${NB}4.019`, cue: "4", destaque: true },
    { rotulo: "Bateria do ePropulsion", valor: `48${NB}volts`, cue: "48" },
  ], tint: "danger" }} />
);

// 8. Exemplo completo: represa, 8 km (p78)
export const P08Exemplo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Exemplo completo · represa grande", titulo: "Os dados do trajeto", linhas: [
    { rotulo: "Distância até a enseada", valor: `8${NB}km`, cue: "8" },
    { rotulo: "Barco de alumínio", valor: `5${NB}m`, cue: "5" },
    { rotulo: "Pescadores a bordo", valor: "2", cue: "2" },
    { rotulo: "Motor elétrico", valor: `3${NB}kW`, cue: "3", destaque: true },
  ], tint: "cool" }} />
);

// 9. Motores maiores (p89)
export const P09Grandes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Motores maiores · preço de compra", titulo: "Gasolina x elétrico", linhas: [
    { rotulo: `40${NB}cavalos a gasolina`, valor: `US$${NB}8.346`, cue: "8" },
    { rotulo: "Elétrico Deep Blue, com bateria", valor: `US$${NB}29.000`, cue: "29", destaque: true },
    { rotulo: `80${NB}cavalos a gasolina`, valor: `US$${NB}12.744`, cue: "12" },
    { rotulo: "Elétrico equivalente", valor: `US$${NB}37.900`, cue: "37", destaque: true },
  ], tint: "danger" }} />
);
'''.replace("@@NB@@", NB)
(R / "src" / "scenes" / "PopaScenes.tsx").write_text(sc, "utf-8")
idx = '''import React from "react";
import type { SceneProps } from "./shared";
import { P01Precos, P02Recarga, P03Gasto, P04Manut, P05Peso, P06Conta, P07Bateria, P08Exemplo, P09Grandes } from "./PopaScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: motor de popa elétrico (pt, 29/10).
export const SCENES: Record<string, SceneEntry> = {
''' + "".join(f'  "{k}": {{ C: {k.replace("-", "")}, preview: 600 }},\n' for k in ANIM.values()) + "};\n"
(R / "src" / "scenes" / "index.ts").write_text(idx, "utf-8")
print("tema popa (pt) gravado")
