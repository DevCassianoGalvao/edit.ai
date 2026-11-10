"""Tema do filme "5 Biggest Port Machines That Make Giant Ships Look Tiny" (en, 29/10/2026, baia b1, painel
20261029-133149). Handler de contêiner cheio, rebocador, guindaste empilhador automático (Long Beach), guindaste
navio-terra (Oakland/LA/Vancouver), guindastes flutuantes (Thialf, Saipem 7000) e bônus Pioneering Spirit.
Sem reuso (assunto novo). Uso: python scripts/_tema_port.py"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
BK = R / "_bak_tema_port"   # cópias dos scripts ANTES deste tema

NP = 69
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "5 Biggest Port Machines That Make Giant Ships Look Tiny" (en, 69 parágrafos, 25,7 min).
Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261029-133149 (carros ajustado, baia b1): paralaxe, mapa, sem trilha.
Assunto: máquinas de porto (handler, rebocador, ASC Long Beach, STS Oakland, Thialf/Saipem 7000, Pioneering Spirit) x Triple-E.
Gerado por scripts/_tema_port.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None
TAGS_LUGAR = []

TAGS = {
    "container_ship": "a huge modern container ship (ultra large, Maersk Triple-E class or similar) loaded with stacked colourful containers, at sea or arriving at a port",
    "ship_dock": "a container ship berthed at a container terminal with ship-to-shore gantry cranes loading it, containers stacked on the wharf",
    "handler": "a laden container handler or reach stacker lifting a full shipping container in a terminal yard (Kalmar, Konecranes, Hyster style heavy forklift with a container hanging in front)",
    "empty_handler": "an empty container handler or electric Kalmar container handler stacking empty containers high in a depot",
    "terminal_yard": "rows of stacked shipping containers in a port terminal yard with trucks and handlers working",
    "tug": "a harbor tugboat pushing or pulling a big ship near a dock, tugboat working alongside a ship hull",
    "tug_escort": "a powerful harbor tug (Crowley, Foss, escort tug) seen from the side or from above, tug with ship at a port such as Los Angeles or Long Beach",
    "tug_crew": "the deck of a tugboat with crew handling tow lines, winch, ropes and fenders beside a large ship hull",
    "asc": "automated stacking cranes in an automated container terminal: rows of rail-mounted electric stacking cranes over container blocks",
    "agv": "an automated guided vehicle (AGV) carrying a container in a driverless container terminal",
    "lb_terminal": "aerial view of the Long Beach container terminal, Middle Harbor, Southern California: ships, cranes, container blocks and rail yard",
    "rail_yard": "an on-dock rail yard at a container terminal: a long train of container wagons under rail-mounted gantry cranes",
    "control_room": "a terminal control room with operators watching screens and monitors, remote operation centre",
    "terminal_night": "a container terminal at night with floodlights, cranes lit up and containers stacked",
    "stsc": "a ship-to-shore container gantry crane on a wharf with its boom raised over the water, giant steel crane at a port",
    "stsc_deck": "a ship-to-shore crane boom reaching over the containers on the deck of a large container ship, lifting a container",
    "zpmc_ship": "giant port cranes being transported on a special heavy-lift ship, or assembled on a wharf, cranes with booms lowered arriving at a port",
    "oakland": "the Port of Oakland, California: container cranes with the San Francisco-Oakland Bay Bridge and the San Francisco bay in view",
    "bridge_raise": "port cranes at the Port of Los Angeles (Pier 400, Los Angeles harbor) with raised booms and container ships",
    "vancouver": "Deltaport container terminal at Roberts Bank, British Columbia, Canada: cranes and container ships",
    "crane_cab": "the cab of a container crane or a crane operator in a cabin high above a ship looking down at a container",
    "crane_vessel": "a giant offshore crane vessel at sea (Thialf, Saipem 7000 or similar), a ship built around huge revolving cranes",
    "thialf": "the semi-submersible crane vessel Thialf of Heerema Marine Contractors with its two huge cranes",
    "saipem": "the semi-submersible crane vessel Saipem 7000 with its two revolving cranes lifting at sea",
    "pioneering": "the Pioneering Spirit (Allseas), the huge platform-lifting vessel with its split bow and two front arms",
    "platform": "an offshore oil and gas platform with its topsides in the North Sea, steel jacket and deck modules",
    "offshore_lift": "an offshore heavy lift: a crane vessel lifting a platform deck or jacket module at sea",
    "sea_swell": "heavy ocean swell and waves rolling under a big ship or offshore structure, rough North Sea weather",
    "offshore_crew": "offshore workers in hard hats and coveralls on a deck, riggers and lift crew with radios on a crane vessel or platform",
}

BANCO = {"container_ship": ["portacontainer"], "platform": ["ns_platforma"]}

REJEITA_TITULO = [r"toy\\b|toys|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|"
                  r"tamiya|miniature|model kit|scale model|cg\\b|blueprint|vector|logo|rc boat|model ship|remote control|"
                  r"cruise ship|ferry|warship|destroyer|frigate|aircraft carrier"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic", "painting"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 69 parágrafos
"container_ship ship_dock G", "ship_dock terminal_yard G", "container_ship ship_dock", "ship_dock container_ship", "handler terminal_yard",
"handler", "handler terminal_yard", "empty_handler container_ship", "handler container_ship", "terminal_yard handler",
"terminal_yard ship_dock", "handler ship_dock", "tug tug_escort", "tug tug_escort", "tug_escort tug",
"tug tug_escort", "tug_escort tug_crew", "tug container_ship", "tug_crew tug", "tug tug_crew",
"asc agv", "terminal_yard asc", "lb_terminal", "asc agv", "agv rail_yard",
"rail_yard", "control_room", "control_room asc", "asc container_ship", "asc terminal_yard",
"terminal_night asc", "stsc ship_dock", "stsc stsc_deck", "stsc", "zpmc_ship oakland",
"oakland stsc", "stsc_deck oakland", "stsc_deck container_ship", "bridge_raise stsc", "stsc ship_dock",
"container_ship stsc", "vancouver stsc", "oakland stsc_deck", "crane_cab", "container_ship stsc_deck",
"crane_vessel thialf", "crane_vessel offshore_lift", "crane_vessel thialf", "thialf", "thialf offshore_lift",
"saipem", "saipem thialf", "sea_swell offshore_lift", "thialf platform", "offshore_crew",
"crane_vessel platform", "pioneering", "pioneering", "pioneering container_ship C", "pioneering platform",
"pioneering offshore_lift", "platform offshore_lift", "pioneering platform", "stsc pioneering", "container_ship pioneering",
"tug stsc", "container_ship stsc", "container_ship tug F", "ship_dock container_ship F"
]
assert len(_PT) == 69, len(_PT)
_OV = {4: "handler terminal_yard", 5: "handler container_ship", 6: "handler terminal_yard", 8: "handler ship_dock", 9: "terminal_yard handler",
       10: "terminal_yard ship_dock", 11: "handler empty_handler",
       12: "tug container_ship", 13: "tug ship_dock", 14: "tug container_ship", 15: "tug", 16: "tug ship_dock", 17: "tug container_ship",
       18: "tug container_ship", 19: "tug ship_dock",
       20: "agv lb_terminal", 21: "terminal_yard lb_terminal", 22: "lb_terminal agv", 23: "agv terminal_night", 24: "agv rail_yard",
       25: "rail_yard terminal_yard", 27: "control_room agv", 28: "lb_terminal container_ship", 29: "terminal_night terminal_yard",
       30: "terminal_night lb_terminal", 32: "stsc ship_dock", 36: "oakland stsc", 37: "stsc container_ship", 42: "oakland ship_dock",
       43: "stsc oakland", 44: "container_ship stsc", 46: "crane_vessel platform", 47: "crane_vessel thialf", 49: "thialf platform",
       52: "sea_swell platform", 54: "platform sea_swell", 55: "crane_vessel platform", 60: "pioneering platform", 61: "platform pioneering",
       62: "pioneering platform", 65: "tug stsc", 67: "container_ship tug F"}
for _k, _v in _OV.items():
    _PT[_k] = _v
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {0, 12, 20, 31, 45, 56}
_REVEAL = {0, 12, 20, 31, 45, 56}
_ANIM = __ANIM__
_CAP = {0: ("THE YARDSTICK", "A 400-METRE SHIP"),
        2: ("NUMBER FIVE", "LADEN CONTAINER HANDLER"),
        12: ("NUMBER FOUR", "HARBOR TUGS"),
        20: ("NUMBER THREE", "AUTOMATED STACKING CRANES"),
        31: ("NUMBER TWO", "SHIP-TO-SHORE GANTRY CRANES"),
        45: ("NUMBER ONE", "FLOATING CRANES"),
        56: ("BONUS", "PIONEERING SPIRIT")}
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({NP})", s[j:])
ANIM = {3: "A01-Triple", 5: "A02-Handler", 15: "A03-Tug", 23: "A04-LongBeach", 35: "A05-Oakland", 48: "A06-Thialf",
        50: "A07-Saipem", 58: "A08-Spirit", 63: "A10-Costa"}
(S / "beats.py").write_text(HEAD.replace("__ANIM__", repr(ANIM)) + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = (BK / "build_plan.py").read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["ship_dock", "container_ship", "stsc"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"control_room", "crane_cab"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["control_room", "crane_cab"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["ship_dock", "container_ship", "stsc"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ', '.join(repr(k).replace("'", '"') for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"A01-Triple": ["400", "59", "18"], "A02-Handler": ["45", "30"], "A03-Tug": ["82", "95"],
        "A04-LongBeach": ["70", "72"], "A05-Oakland": ["442", "372", "440"], "A06-Thialf": ["14", "11"],
        "A07-Saipem": ["7000", "14", "140"], "A08-Spirit": ["382", "400", "124"],
        "A10-Costa": ["beach", "oakland"]}
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

# DOSSIE vazio (escrito depois das fotos aprovadas)
bo = (BK / "build_overlays.py").read_text("utf-8")
a0 = bo.index("DOSSIE = [")
a1 = bo.index("\n]\n", a0) + 3
bo = bo[:a0] + "DOSSIE = [  # 29/10/2026 port machines (en) — preenchido depois das fotos\n]\n" + bo[a1:]
(S / "build_overlays.py").write_text(bo, "utf-8")

Q = {
    "container_ship": ["Maersk Triple E container ship", "ultra large container ship", "Mærsk Mc-Kinney Møller ship", "container ship at sea loaded"],
    "ship_dock": ["container ship at terminal cranes", "container terminal ship loading", "port of Long Beach container ship", "port of Oakland container ship"],
    "handler": ["laden container handler", "Kalmar container handler", "Konecranes container handler", "reach stacker container", "Hyster container handler"],
    "empty_handler": ["empty container handler", "Kalmar electric empty container handler", "empty container stacker depot"],
    "terminal_yard": ["container terminal yard", "stacked shipping containers port", "container yard port trucks"],
    "tug": ["harbor tug pushing ship", "tugboat container ship", "tugboat assisting ship docking"],
    "tug_escort": ["Crowley tug Los Angeles", "Crowley Harbor class tug", "Foss tug Long Beach", "escort tug port of Los Angeles"],
    "tug_crew": ["tugboat deck crew line", "tugboat deck winch rope", "tug crew towing line"],
    "asc": ["automated stacking crane", "automated container terminal stacking cranes", "automated container yard crane"],
    "agv": ["automated guided vehicle container", "AGV container terminal", "driverless container carrier port"],
    "lb_terminal": ["Long Beach Container Terminal Middle Harbor", "Long Beach container terminal aerial", "port of Long Beach terminal"],
    "rail_yard": ["on-dock rail yard container", "container train rail mounted gantry crane", "intermodal rail yard cranes"],
    "control_room": ["port terminal control room", "container terminal control room operators", "remote crane operator screens"],
    "terminal_night": ["container terminal at night", "port cranes night lights", "container port night"],
    "stsc": ["ship to shore gantry crane", "container gantry crane port", "ZPMC container crane", "port crane boom raised"],
    "stsc_deck": ["container crane loading ship deck", "gantry crane lifting container ship", "ship to shore crane boom over ship"],
    "zpmc_ship": ["ZPMC crane ship transport", "container cranes arrive on ship port", "ZPMC cranes Oakland arrive"],
    "oakland": ["Port of Oakland cranes", "Oakland container cranes Bay Bridge", "Oakland harbor cranes"],
    "bridge_raise": ["Pier 400 Los Angeles cranes", "port of Los Angeles cranes raised", "Los Angeles harbor container cranes"],
    "vancouver": ["Deltaport Roberts Bank", "Deltaport container terminal", "Roberts Bank terminal cranes"],
    "crane_cab": ["crane operator cabin container", "crane cab view down", "container crane operator"],
    "crane_vessel": ["crane vessel offshore", "heavy lift crane ship", "semi-submersible crane vessel"],
    "thialf": ["Thialf crane vessel", "Thialf Heerema", "Thialf semi-submersible"],
    "saipem": ["Saipem 7000", "Saipem 7000 crane vessel", "Saipem 7000 lifting"],
    "pioneering": ["Pioneering Spirit Allseas", "Pioneering Spirit ship", "Pioneering Spirit platform lift"],
    "platform": ["North Sea oil platform", "Brent Delta platform", "offshore platform topsides", "Yme platform"],
    "offshore_lift": ["offshore platform lift crane vessel", "topsides lift offshore", "platform removal single lift"],
    "sea_swell": ["North Sea waves platform", "heavy swell ship", "rough sea offshore"],
    "offshore_crew": ["offshore crew deck hard hats", "offshore workers crane", "riggers offshore deck"],
}
CATS = {"Category:Container ships": "container_ship", "Category:Maersk Line container ships": "container_ship",
        "Category:Mærsk Triple E class ships": "container_ship", "Category:Container terminals in the United States": "ship_dock",
        "Category:Straight mast container handlers": "handler", "Category:Reach stackers": "handler", "Category:Kalmar": "handler",
        "Category:Konecranes": "handler", "Category:Empty container handlers": "empty_handler",
        "Category:Tugboats of the United States": "tug_escort", "Category:Crowley Maritime": "tug_escort", "Category:Foss Maritime": "tug_escort",
        "Category:Port of Long Beach": "lb_terminal", "Category:Port of Los Angeles": "bridge_raise", "Category:Port of Oakland": "oakland",
        "Category:Automated guided vehicles": "agv", "Category:Container cranes": "stsc", "Category:Portainers": "stsc",
        "Category:Gantry cranes": "stsc", "Category:Stacker cranes": "asc", "Category:Control rooms": "control_room",
        "Category:DeltaPort": "vancouver", "Category:Roberts Bank Superport": "vancouver", "Category:Thialf (ship, 1985)": "thialf",
        "Category:Thialf": "thialf", "Category:Heerema Marine Contractors": "thialf", "Category:Saipem 7000 (ship, 1987)": "saipem",
        "Category:Saipem 7000 (ship, 1987) at sea": "saipem", "Category:Pioneering Spirit (ship, 2014)": "pioneering",
        "Category:Allseas": "pioneering", "Category:Yme (oil platform)": "platform", "Category:Offshore platforms": "platform",
        "Category:Floating cranes": "crane_vessel", "Category:Crane ships": "crane_vessel"}
PEX = {"container_ship": ["container ship sea", "cargo ship containers"], "ship_dock": ["container terminal ship", "port cranes ship"],
       "handler": ["container handler", "reach stacker container"], "empty_handler": ["container yard forklift", "empty containers stacked"],
       "terminal_yard": ["container yard stacked", "shipping containers port"], "tug": ["tugboat harbor", "tugboat pushing ship"],
       "tug_escort": ["tugboat port", "tug boat water"], "tug_crew": ["tugboat deck ropes", "ship mooring ropes"],
       "asc": ["automated container terminal", "container port cranes"], "agv": ["automated vehicle port", "container carrier port"],
       "lb_terminal": ["container port aerial", "port terminal aerial"], "rail_yard": ["container train port", "freight train containers"],
       "control_room": ["control room monitors", "operator screens control room"], "terminal_night": ["container port night", "port cranes night"],
       "stsc": ["gantry crane port", "port crane containers"], "stsc_deck": ["crane loading container ship", "container crane ship"],
       "crane_cab": ["crane operator cabin", "crane cab view"], "crane_vessel": ["offshore crane vessel", "heavy lift ship"],
       "platform": ["oil platform sea", "offshore platform"], "offshore_lift": ["offshore crane lift", "offshore heavy lift"],
       "sea_swell": ["ocean swell ship", "rough sea waves"], "offshore_crew": ["offshore workers deck", "oil rig workers"],
       "oakland": ["Oakland port cranes", "San Francisco bay bridge port"], "vancouver": ["Vancouver port cranes", "British Columbia port"],
       "bridge_raise": ["Los Angeles port cranes", "Long Beach port"]}
NAVIO = {
    "container_ship": ["container ship sea", "cargo ship aerial"],
    "ship_dock": ["container terminal aerial", "port cranes ship"],
    "handler": ["container handler", "reach stacker"],
    "terminal_yard": ["container yard", "stacked containers port"],
    "tug": ["tugboat harbor", "tugboat pushing ship"],
    "asc": ["automated container terminal", "container port aerial"],
    "control_room": ["control room monitors", "operator control room"],
    "rail_yard": ["container train cranes", "freight train port"],
    "stsc": ["port crane container ship", "gantry crane containers"],
    "crane_cab": ["crane operator cabin", "crane cab"],
    "crane_vessel": ["offshore crane vessel", "heavy lift ship"],
    "platform": ["oil platform sea", "offshore platform"],
    "offshore_lift": ["offshore crane lift", "offshore heavy lift"],
    "sea_swell": ["ocean waves ship storm", "rough sea ship"],
    "offshore_crew": ["offshore workers deck", "oil rig workers"],
    "terminal_night": ["container port night", "port cranes night"],
}
YT = """Konecranes laden container handler
Kalmar electric empty container handler
Crowley Harbor class tug escort Los Angeles
Foss Jamie Ann tug Long Beach
Long Beach Container Terminal Middle Harbor automated stacking cranes
Port of Oakland ZPMC cranes arrive Bay Bridge
ship to shore crane operator cab view
Thialf crane vessel lift
Saipem 7000 crane vessel lift
Pioneering Spirit Brent Delta removal
Pioneering Spirit Yme platform lift
Maersk Triple-E docking tugs
"""
(D / "yt_queries_port.txt").write_text(YT, "utf-8")
DV = """tug: tugboat harbor ship assist
container_ship: container ship pier cargo
stsc: crane pier loading container ship
handler: container handler port forklift
ship_dock: port terminal cargo ship pier
crane_vessel: heavy lift crane ship
platform: offshore oil platform
sea_swell: heavy seas ship
"""
(D / "dvids_queries_port.txt").write_text(DV, "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 29/10/2026 port machines (en, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)

# cenas + registro
NB = chr(160)
sc = '''// Animações de "5 Biggest Port Machines" (en, enxuto) — painel 20261029-133149 (b1).
// REGRA: biblioteca (Painel); motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const COSTA: [number, number][] = [[32.6, -117.2], [33.0, -117.3], [33.4, -117.7], [33.75, -118.4], [34.0, -118.5], [34.4, -119.7],
  [34.5, -120.5], [35.2, -120.8], [35.7, -121.3], [36.6, -121.9], [37.0, -122.2], [37.6, -122.5], [38.0, -123.0], [38.9, -123.7],
  [39.8, -123.85], [40.4, -124.4], [41.7, -124.2], [42.0, -124.3]];

const NB = "@@NB@@";

// 1. A régua do filme: Triple-E (p02)
export const A01Triple: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Maersk Triple-E class · the yardstick", titulo: "The ship every machine is measured against", linhas: [
    { rotulo: "Length", valor: `400${NB}m`, cue: "400" },
    { rotulo: "Width", valor: `59${NB}m`, cue: "59" },
    { rotulo: "Capacity, twenty-foot boxes", valor: `18,000${NB}TEU`, cue: "18", destaque: true },
  ], tint: "cool" }} />
);

// 2. Handler de contêiner cheio (p05)
export const A02Handler: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Laden container handler · Konecranes", titulo: "A forklift that went to the gym", linhas: [
    { rotulo: "Lifts a full container, up to", valor: `45${NB}tonnes`, cue: "45", destaque: true },
    { rotulo: "Same weight as roughly", valor: `30${NB}family cars`, cue: "30" },
    { rotulo: "Lifting height", valor: `16${NB}m` },
  ], tint: "accent" }} />
);

// 3. Rebocador Venture (p15)
export const A03Tug: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Crowley tug Venture · Los Angeles and Long Beach", titulo: "Small boat, huge pull", linhas: [
    { rotulo: "Length", valor: `82${NB}feet`, cue: "82" },
    { rotulo: "Bollard pull, up to", valor: `95${NB}tonnes`, cue: "95", destaque: true },
  ], tint: "cool" }} />
);

// 4. Long Beach: guindastes empilhadores (p23)
export const A04LongBeach: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Long Beach Container Terminal · Middle Harbor", titulo: "Automated stacking cranes", linhas: [
    { rotulo: "Per the project plan", valor: `70${NB}cranes`, cue: "70" },
    { rotulo: "Per a trade report after opening", valor: `72${NB}cranes`, cue: "72", destaque: true },
  ], tint: "accent" }} />
);

// 5. Oakland: quanto mede o guindaste (p35)
export const A05Oakland: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Port of Oakland · ZPMC cranes", titulo: "How tall is the crane?", linhas: [
    { rotulo: "Boom nearly vertical", valor: `442${NB}feet`, cue: "442", destaque: true },
    { rotulo: "Boom stowed at 45 degrees", valor: `372${NB}feet`, cue: "372" },
    { rotulo: "Earlier reports, boom raised", valor: `440${NB}feet`, cue: "440" },
  ], tint: "cool" }} />
);

// 6. Thialf (p48)
export const A06Thialf: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Thialf · Heerema Marine Contractors", titulo: "Two cranes, one record", linhas: [
    { rotulo: "Combined lifting capacity", valor: `14,200${NB}tonnes`, cue: "14", destaque: true },
    { rotulo: "Heaviest lift on record", valor: `11,883${NB}tonnes`, cue: "11" },
  ], tint: "accent" }} />
);

// 7. Saipem 7000 (p50)
export const A07Saipem: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Saipem 7000 · two revolving cranes", titulo: "Seven thousand tonnes each", linhas: [
    { rotulo: "Each crane", valor: `7,000${NB}tonnes`, cue: "7000" },
    { rotulo: "Combined rating", valor: `14,000${NB}tonnes`, cue: "14", destaque: true },
    { rotulo: "Crane length", valor: `140${NB}m`, cue: "140" },
  ], tint: "cool" }} />
);

// 8. Pioneering Spirit x Triple-E (p58)
export const A08Spirit: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pioneering Spirit · Allseas", titulo: "Almost as long. Twice as wide.", linhas: [
    { rotulo: "Pioneering Spirit, hull length", valor: `382${NB}m`, cue: "382" },
    { rotulo: "Triple-E, length", valor: `400${NB}m`, cue: "400" },
    { rotulo: "Pioneering Spirit, hull width", valor: `124${NB}m`, cue: "124", destaque: true },
  ], tint: "danger" }} />
);

// 10. Os dois portos do recap (p63)
export const A10Costa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CALIFORNIA · TWO PORTS, TWO KINDS OF GIANT" linhas={[{ pontos: COSTA }]} lugares={[
    { nome: "Long Beach", lat: 33.75, lon: -118.2, cue: "beach", abaixo: true },
    { nome: "Oakland", lat: 37.8, lon: -122.3, cue: "oakland" },
  ]} tint={colors.cool} />
);

// 9. A escada (p65)
export const A09Ladder: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The ladder · smallest to largest", titulo: "Each step, a different kind of strength", linhas: [
    { rotulo: "Container handler", valor: `45${NB}t lift`, cue: "45" },
    { rotulo: "Tug", valor: `95${NB}t pull`, cue: "95" },
    { rotulo: "Crane reach over a deck", valor: `225${NB}ft`, cue: "225" },
    { rotulo: "Floating crane", valor: `14,000${NB}t` },
    { rotulo: "Pioneering Spirit", valor: `48,000${NB}t`, cue: "48", destaque: true },
  ], tint: "danger" }} />
);
'''.replace("@@NB@@", NB)
(R / "src" / "scenes" / "PortScenes.tsx").write_text(sc, "utf-8")
idx = '''import React from "react";
import type { SceneProps } from "./shared";
import { A01Triple, A02Handler, A03Tug, A04LongBeach, A05Oakland, A06Thialf, A07Saipem, A08Spirit, A09Ladder, A10Costa } from "./PortScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: port machines (en, 29/10).
export const SCENES: Record<string, SceneEntry> = {
''' + "".join(f'  "{k}": {{ C: {k.replace("-", "")}, preview: 600 }},\n' for k in ANIM.values()) + "};\n"
(R / "src" / "scenes" / "index.ts").write_text(idx, "utf-8")
print("tema port (en) gravado")
