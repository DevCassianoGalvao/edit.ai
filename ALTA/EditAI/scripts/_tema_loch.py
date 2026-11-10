"""Tema do filme "What Lies Under Loch Ness? (Scotland Was Torn in Two Here)" (en, 31/10/2026, baia b1, painel
20261031-110425). Loch Ness: números do lago, Falha de Great Glen (strike-slip), geleiras, água escura, lenda (1933/1934),
sonar (Deepscan 1987), DNA ambiental (Gemmell 2019), enguias, sedimento. Sem reuso (assunto novo).
Uso: python scripts/_tema_loch.py"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
BK = R / "_bak_tema_loch"   # cópias dos scripts ANTES deste tema

NP = 64
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "What Lies Under Loch Ness?" (en, 64 parágrafos, 21,6 min).
Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261031-110425 (arquivo-dark ajustado, baia b1): paralaxe, mapa, sem trilha.
Assunto: Loch Ness, Great Glen Fault, glaciação, lenda de Nessie, sonar, eDNA, enguias.
Gerado por scripts/_tema_loch.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None
TAGS_LUGAR = []

TAGS = {
    "loch_surface": "Loch Ness seen from the shore or a boat: a long calm dark stretch of water between forested Highland hills, Scotland",
    "loch_aerial": "aerial or drone view of Loch Ness and the Great Glen: the long narrow straight loch between hills, Scotland",
    "loch_shore": "the shore of Loch Ness: Urquhart Castle ruins on the loch, the road along the water, a pier or jetty",
    "tourists": "tourists on the bank of Loch Ness with cameras, a tour boat or cruise boat on the loch, visitors looking at the water",
    "great_glen": "the Great Glen in Scotland: the long straight valley with lochs, Loch Oich, Loch Lochy, Fort Augustus, the Caledonian Canal",
    "scotland_map": "a map of Scotland (physical or geological map, relief map) showing the Great Glen, Loch Ness, Inverness and Fort William",
    "fault": "a fault in rock: a geological fault line, fault plane or offset rock layers, strike-slip fault outcrop or fault scarp",
    "rock_folded": "ancient metamorphic rock in Scotland: folded layered rock, schist, gneiss, a rock outcrop of banded strata in the Highlands",
    "continents": "plate tectonics and continental collision: diagram of colliding continents, old eroded mountain belt, Caledonian mountain building",
    "highlands": "the Scottish Highlands: rugged mountains, moorland, glens and lochs under cloud",
    "glacier": "a glacier or ice sheet grinding through a valley, ice age ice, glacial ice flowing downhill, glacial erosion",
    "ushape": "a U-shaped glacial valley: a steep-sided glen carved by ice, Scottish or similar glaciated valley seen from above",
    "peat": "dark brown peat-stained water: a Highland burn, peaty river or brown loch water, peat bog and moorland stream",
    "dark_water": "dark murky lake water: black deep water, underwater murk with suspended particles, a loch in dim light",
    "diver": "a scuba diver with a torch in dark murky cold water, divers descending in a lake",
    "sonar": "a sonar or echo sounder screen on a boat showing the lake bottom and echoes, fish finder display, sonar scan image",
    "survey_boat": "a research or survey boat on a loch with scientists and instruments, a small fleet of boats on a lake",
    "fishing_boat": "an old fishing boat or drifter on the water, a 1950s style wooden fishing vessel with nets",
    "nessie": "the Loch Ness Monster as culture: a Nessie statue, souvenir, exhibition, sign or model of the monster at Loch Ness",
    "press30s": "1930s newspapers and archive material: old newspaper front pages, vintage press photographs, black and white archive of the 1930s",
    "columba": "Saint Columba and early Christian Scotland: Pictish stone, Iona Abbey, medieval illuminated manuscript, early monks",
    "inverness": "Inverness, Scotland: the River Ness, the castle, the city centre and bridges over the river",
    "edna": "environmental DNA work: water sampling bottles, a scientist filtering water, laboratory pipette, DNA sequencing, genetics lab",
    "eel": "a European eel (Anguilla anguilla): an eel swimming underwater or in a river, eel close-up",
    "fish": "freshwater fish in a lake or river: trout, salmon, Arctic char, perch, fish underwater in Scotland",
    "bigfish": "a big fish: sturgeon, wels catfish or Greenland shark swimming underwater",
    "plesiosaur": "a plesiosaur: fossil skeleton in a museum, plesiosaur reconstruction, long-necked marine reptile",
    "sediment": "lake bed sediment: a sediment core, layered silt, mud on a lake bottom, varves, sediment sample",
    "birds": "waterbirds on a Scottish loch: cormorant, goosander, grebe, geese, a heron on the shore",
}

BANCO = {}

REJEITA_TITULO = [r"toy\\b|toys|lego|diorama|\\b3d\\b|game|clipart|cartoon|minecraft|vector|logo|stamp|coin|"
                  r"cgi|ai generated|wallpaper|postcard|painting|drawing|illustration"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "infographic"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 64 parágrafos
"loch_aerial great_glen G", "loch_surface tourists G", "loch_aerial loch_surface", "loch_surface loch_aerial", "great_glen loch_aerial",
"scotland_map great_glen", "fault rock_folded", "fault scotland_map", "scotland_map rock_folded", "rock_folded fault",
"continents highlands", "fault rock_folded", "glacier", "glacier ushape", "ushape great_glen",
"glacier loch_surface", "dark_water loch_surface", "peat dark_water", "dark_water diver", "diver sonar",
"columba inverness", "loch_shore press30s", "press30s nessie", "press30s nessie", "nessie press30s",
"press30s nessie", "press30s nessie", "sonar survey_boat", "fishing_boat sonar", "survey_boat sonar",
"survey_boat loch_surface", "sonar survey_boat", "sonar fish", "sonar dark_water", "loch_surface sonar",
"loch_surface nessie", "edna dark_water", "edna fish", "edna survey_boat", "edna loch_surface",
"edna", "plesiosaur bigfish", "eel fish", "eel", "eel nessie",
"eel fish", "nessie plesiosaur", "plesiosaur glacier", "bigfish fish", "tourists loch_shore",
"nessie tourists", "loch_surface dark_water", "dark_water sediment", "sediment dark_water", "rock_folded continents",
"continents scotland_map", "loch_surface fault", "loch_aerial loch_surface", "loch_aerial sediment C", "eel birds",
"nessie eel", "loch_surface nessie", "loch_surface nessie", "loch_surface dark_water F"
]
assert len(_PT) == 64, len(_PT)
_OV = {}
for _k, _v in _OV.items():
    _PT[_k] = _v
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {0, 12, 16, 27, 36, 51}
_REVEAL = {0, 12, 16, 27, 36, 51}
_ANIM = __ANIM__
_CAP = {0: ("THE HOLE", "230 METERS DEEP"),
        5: ("THE CRACK", "THE GREAT GLEN FAULT"),
        12: ("THE ICE", "CARVING THE TRENCH"),
        16: ("THE WATER", "DARK AND COLD"),
        20: ("THE LEGEND", "FROM COLUMBA TO 1933"),
        27: ("THE SEARCH", "SONAR"),
        36: ("THE DNA", "WHAT THE WATER REMEMBERS"),
        46: ("THE VERDICT", "A BIOLOGIST'S VIEW"),
        51: ("THE BOTTOM", "WHAT IS REALLY DOWN THERE")}
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({NP})", s[j:])
ANIM = {2: "A01-Numbers", 5: "A02-Glen", 8: "A03-Slide", 30: "A04-Deepscan", 38: "A05-Edna", 58: "A06-Recap"}
(S / "beats.py").write_text(HEAD.replace("__ANIM__", repr(ANIM)) + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = (BK / "build_plan.py").read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["loch_surface", "loch_aerial", "highlands"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"edna"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["edna"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["loch_surface", "loch_aerial", "highlands"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ', '.join(repr(k).replace("'", '"') for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"A01-Numbers": ["37", "56", "230"], "A02-Glen": ["inverness", "william"], "A03-Slide": ["100", "160", "200"],
        "A04-Deepscan": ["20", "24"], "A05-Edna": ["250", "three"], "A06-Recap": ["56", "230", "10"]}
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

# DOSSIE vazio (escrito depois das fotos aprovadas)
bo = (BK / "build_overlays.py").read_text("utf-8")
a0 = bo.index("DOSSIE = [")
a1 = bo.index("\n]\n", a0) + 3
bo = bo[:a0] + "DOSSIE = [  # 31/10/2026 Loch Ness (en) — preenchido depois das fotos\n]\n" + bo[a1:]
(S / "build_overlays.py").write_text(bo, "utf-8")

Q = {
    "loch_surface": ["Loch Ness", "Loch Ness view", "Loch Ness water hills", "Loch Ness from shore"],
    "loch_aerial": ["Loch Ness aerial", "Loch Ness from above", "Great Glen aerial", "Loch Ness Urquhart Bay aerial"],
    "loch_shore": ["Urquhart Castle Loch Ness", "Loch Ness shore road", "Loch Ness Drumnadrochit", "Loch Ness pier"],
    "tourists": ["Loch Ness tourists", "Loch Ness cruise boat", "Loch Ness visitors Urquhart"],
    "great_glen": ["Great Glen", "Caledonian Canal Fort Augustus", "Loch Oich", "Loch Lochy", "Great Glen Way"],
    "scotland_map": ["Great Glen Fault map", "geological map Scotland", "relief map Scotland", "Scotland map Great Glen"],
    "fault": ["strike-slip fault", "Great Glen Fault", "fault line rock outcrop", "fault plane outcrop"],
    "rock_folded": ["folded rock Scotland", "Moine schist", "metamorphic rock outcrop Highlands", "gneiss outcrop Scotland"],
    "continents": ["Caledonian orogeny", "continental collision diagram", "Laurentia Avalonia Baltica", "Iapetus Ocean closing"],
    "highlands": ["Scottish Highlands", "Highlands glen Scotland", "Scottish Highlands mountains", "Glen Coe"],
    "glacier": ["glacier flowing valley", "valley glacier ice", "ice sheet glacier erosion", "glacier terminus ice"],
    "ushape": ["U-shaped valley", "glacial valley Scotland", "glaciated glen Highlands", "Glen Coe glacial valley"],
    "peat": ["peat stained water Scotland", "Highland burn peat", "peat bog Scotland", "brown river peat Highlands"],
    "dark_water": ["dark lake water", "Loch Ness dark water", "black water lake", "underwater murky lake"],
    "diver": ["scuba diver lake dark", "diver torch murky water", "diver loch Scotland"],
    "sonar": ["sonar scan lake bottom", "echo sounder display", "fish finder screen", "side scan sonar image"],
    "survey_boat": ["research boat Loch Ness", "survey boat loch", "Loch Ness research vessel", "boats Loch Ness"],
    "fishing_boat": ["old fishing boat drifter", "wooden fishing boat 1950s", "herring drifter boat"],
    "nessie": ["Loch Ness Monster statue", "Nessie", "Loch Ness Monster exhibition", "Nessie sign Loch Ness"],
    "press30s": ["Daily Mail 1930s newspaper", "1930s newspaper front page", "Loch Ness Monster 1934 photograph", "Surgeon's Photograph"],
    "columba": ["Saint Columba", "Iona Abbey", "Pictish stone", "Adomnan Life of Columba manuscript"],
    "inverness": ["Inverness River Ness", "Inverness castle", "Inverness Scotland city"],
    "edna": ["environmental DNA water sampling", "water sample filtering eDNA", "DNA sequencing laboratory", "pipette laboratory DNA"],
    "eel": ["European eel", "Anguilla anguilla", "eel underwater", "elver eel"],
    "fish": ["brown trout", "Arctic char", "Atlantic salmon river", "perch freshwater fish"],
    "bigfish": ["Atlantic sturgeon", "wels catfish", "Greenland shark", "sturgeon underwater"],
    "plesiosaur": ["plesiosaur skeleton museum", "Plesiosaurus fossil", "plesiosaur reconstruction", "Elasmosaurus"],
    "sediment": ["lake sediment core", "varves sediment", "lake bottom mud sample", "sediment layers core"],
    "birds": ["cormorant loch", "goosander", "heron lake Scotland", "waterbirds Scotland loch"],
}
CATS = {"Category:Loch Ness": "loch_surface", "Category:Urquhart Castle": "loch_shore", "Category:Great Glen": "great_glen",
        "Category:Caledonian Canal": "great_glen", "Category:Loch Oich": "great_glen", "Category:Loch Lochy": "great_glen",
        "Category:Fort Augustus": "great_glen", "Category:Great Glen Fault": "fault", "Category:Strike-slip faults": "fault",
        "Category:Inverness": "inverness", "Category:River Ness": "inverness", "Category:Loch Ness Monster": "nessie",
        "Category:Surgeon's Photograph": "press30s", "Category:Columba of Iona": "columba", "Category:Iona Abbey": "columba",
        "Category:Anguilla anguilla": "eel", "Category:Plesiosauria": "plesiosaur", "Category:Somniosus microcephalus": "bigfish",
        "Category:Silurus glanis": "bigfish", "Category:Acipenser sturio": "bigfish", "Category:Sonar": "sonar",
        "Category:Scottish Highlands": "highlands", "Category:U-shaped valleys": "ushape", "Category:Varves": "sediment",
        "Category:Caledonian orogeny": "continents"}
PEX = {"loch_surface": ["scottish loch", "loch scotland water hills"], "loch_aerial": ["scottish loch aerial", "scotland lake drone"],
       "loch_shore": ["scottish castle loch", "scotland lake shore road"], "tourists": ["tourists lake boat", "tourists photographing lake"],
       "great_glen": ["scottish glen", "scotland valley lake"], "scotland_map": ["scotland map", "relief map terrain"],
       "fault": ["fault line rock", "rock layers cliff"], "rock_folded": ["folded rock layers", "rock strata outcrop"],
       "continents": ["tectonic plates", "mountain range collision"], "highlands": ["scottish highlands", "scotland mountains moor"],
       "glacier": ["glacier ice valley", "glacier ice"], "ushape": ["glacial valley", "scottish glen mountains"],
       "peat": ["peat bog stream", "brown water stream moorland"], "dark_water": ["dark water lake", "murky water underwater"],
       "diver": ["scuba diver dark water", "diver torch underwater"], "sonar": ["sonar screen boat", "fish finder screen"],
       "survey_boat": ["research boat lake", "scientists boat lake"], "fishing_boat": ["old fishing boat", "wooden fishing boat"],
       "nessie": ["loch ness monster statue", "sea monster toy"], "press30s": ["old newspaper 1930s", "vintage newspaper"],
       "columba": ["celtic cross stone", "medieval manuscript"], "inverness": ["inverness scotland", "river ness inverness"],
       "edna": ["water sample laboratory", "scientist filtering water"], "eel": ["eel underwater", "european eel"],
       "fish": ["trout underwater", "freshwater fish lake"], "bigfish": ["sturgeon fish", "catfish underwater"],
       "plesiosaur": ["plesiosaur fossil", "marine reptile skeleton"], "sediment": ["lake sediment", "mud layers core"],
       "birds": ["cormorant water", "heron lake"]}
NAVIO = {
    "loch_surface": ["scottish loch", "loch scotland mist"],
    "loch_aerial": ["scottish loch aerial", "scotland lake drone"],
    "great_glen": ["scottish glen aerial", "scotland valley drone"],
    "highlands": ["scottish highlands", "scotland mountains clouds"],
    "glacier": ["glacier ice flowing", "glacier valley aerial"],
    "dark_water": ["dark water lake", "murky underwater lake"],
    "diver": ["diver torch dark water", "scuba diver murky"],
    "sonar": ["sonar screen boat", "fish finder screen"],
    "survey_boat": ["research boat lake", "boat on loch"],
    "edna": ["water sample laboratory", "scientist pipette lab"],
    "eel": ["eel underwater", "european eel"],
    "fish": ["trout underwater", "freshwater fish lake"],
    "peat": ["peat bog stream", "brown stream moorland"],
    "birds": ["cormorant water", "heron lake"],
    "tourists": ["tourists boat lake", "castle ruins lake"],
}
YT = """Loch Ness drone 4K Scotland
Loch Ness Urquhart Castle aerial
Great Glen Fault geology Scotland
Caledonian Canal Fort Augustus locks
Loch Ness environmental DNA Neil Gemmell
Operation Deepscan 1987 Loch Ness sonar
Loch Ness sonar search boat
Scottish Highlands glen glacier carved valley
Loch Ness underwater dive
European eel underwater
Loch Ness monster legend history documentary
"""
(D / "yt_queries_loch.txt").write_text(YT, "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 31/10/2026 Loch Ness (en, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)

NB = chr(160)
sc = '''// Animações de "What Lies Under Loch Ness?" (en, enxuto) — painel 20261031-110425 (b1).
// REGRA: biblioteca (Painel/MapaRota); motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "@@NB@@";

// 1. Os números do lago (p02)
export const A01Numbers: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Loch Ness · Scottish Highlands", titulo: "A long, narrow, very deep loch", linhas: [
    { rotulo: "Length, end to end", valor: `37${NB}km`, cue: "37" },
    { rotulo: "Surface area", valor: `56${NB}km²`, cue: "56" },
    { rotulo: "Deepest point", valor: `230${NB}m`, cue: "230", destaque: true },
  ], tint: "cool" }} />
);

// 2. O Great Glen (p05)
export const A02Glen: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SCOTLAND · THE GREAT GLEN FAULT" linhas={[{ pontos: [[57.48, -4.23], [57.35, -4.4], [57.2, -4.62], [57.14, -4.68],
    [57.06, -4.78], [56.98, -4.9], [56.9, -5.0], [56.82, -5.11]] }]} lugares={[
    { nome: "Inverness", lat: 57.48, lon: -4.23, cue: "inverness" },
    { nome: "Fort William", lat: 56.82, lon: -5.11, cue: "william", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. Quanto deslizou (p08)
export const A03Slide: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Great Glen Fault · sideways slip", titulo: "Nobody agrees on the distance", linhas: [
    { rotulo: "A common estimate, a little over", valor: `100${NB}km`, cue: "100" },
    { rotulo: "Banded-rock studies", valor: `160${NB}km`, cue: "160", destaque: true },
    { rotulo: "Other researchers", valor: `200–300${NB}km`, cue: "200" },
  ], tint: "accent" }} />
);

// 4. Operation Deepscan (p30)
export const A04Deepscan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Operation Deepscan · 1987", titulo: "A wall of sonar across the loch", linhas: [
    { rotulo: "Boats, by some accounts", valor: `20`, cue: "20" },
    { rotulo: "Boats, by others", valor: `24`, cue: "24", destaque: true },
  ], tint: "cool" }} />
);

// 5. DNA ambiental (p38)
export const A05Edna: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Environmental DNA · 2018", titulo: "Reading the water", linhas: [
    { rotulo: "Sampling places around the loch", valor: `250+`, cue: "250", destaque: true },
    { rotulo: "Depths sampled at each", valor: `3`, cue: "three" },
  ], tint: "accent" }} />
);

// 6. O que há sob o Loch Ness (p58)
export const A06Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "What lies under Loch Ness", titulo: "Water, trench, sediment, fault", linhas: [
    { rotulo: "Surface area", valor: `56${NB}km²`, cue: "56" },
    { rotulo: "Deepest point", valor: `230${NB}m`, cue: "230", destaque: true },
    { rotulo: "Sediment records", valor: `10,000${NB}years`, cue: "10" },
  ], tint: "danger" }} />
);
'''.replace("@@NB@@", NB)
(R / "src" / "scenes" / "LochScenes.tsx").write_text(sc, "utf-8")
idx = '''import React from "react";
import type { SceneProps } from "./shared";
import { A01Numbers, A02Glen, A03Slide, A04Deepscan, A05Edna, A06Recap } from "./LochScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: Loch Ness (en, 31/10).
export const SCENES: Record<string, SceneEntry> = {
''' + "".join(f'  "{k}": {{ C: {k.replace("-", "")}, preview: 600 }},\n' for k in ANIM.values()) + "};\n"
(R / "src" / "scenes" / "index.ts").write_text(idx, "utf-8")
print("tema loch (en) gravado")
