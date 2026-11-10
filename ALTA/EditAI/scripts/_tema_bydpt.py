"""Tema do filme "Musk riu da BYD — o que os engenheiros encontraram" (pt, 05/10/2026, baia 1): beats.py, cenas, CUES,
buscas + REUSO das fotos e janelas APROVADAS dos filmes do BYD Seal desmontado (pl, 03/10) e da célula Blade (fr, 05/10).
Busca nova só das tags que esses filmes não tinham (Musk, Buffett, Munro, Seagull, Berlim, Camaçari, navio, Shenzhen, híbrido)."""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
BAIAS = R.parent / "baias"
SRC = [BAIAS / "b2" / "_decisoes_demontaz-byd-seal-pl-2026-10-03", BAIAS / "b2" / "_decisoes_batterie-blade-demontee-fr"]
FORA = {"oslo", "yutong", "gora", "dania", "dane", "telekom", "polska", "aachen", "krzem", "niemcy", "mroz", "chlodzenie"}
MAPA = {"samochod": "byd", "falownik": "naped", "wirnik": "naped", "ziemie": "chiny", "port": "navio"}

s = (S / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "Musk riu da BYD" (pt, 41 parágrafos, 25,1 min). Modo PADRÃO, 20 % VÍDEO / 80 % FOTO.
Pedido do PAINEL 20261005-162130 ("car-pt-2", automático, baia 1): arquivo dark, paralaxe, mapa, sem trilha.
REUSO: material aprovado do BYD Seal desmontado (pl) e da célula Blade (fr). Cartões CARROS (escolha do usuário).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None
TAGS_LUGAR = ["shenzhen", "berlim", "camacari"]

TAGS = {
    "musk": "Elon Musk (Tesla CEO) speaking, Tesla events",
    "tesla": "Tesla cars: Model S, Model 3, Model Y; Tesla factory and stores",
    "byd": "BYD: brand, stores, headquarters, BYD cars (Seal, Dolphin, Atto 3, Han)",
    "shenzhen": "Shenzhen, China: skyline, BYD headquarters",
    "buffett": "Warren Buffett and Berkshire Hathaway",
    "munro": "Sandy Munro and Munro & Associates: car teardown lab in Michigan",
    "demontaz": "a car teardown: disassembled car, parts laid out on a workshop floor, engineers with tools",
    "blade": "the BYD Blade battery: long LFP prismatic cells, battery pack in the car floor",
    "pakiet": "an electric car battery pack opened: cells, modules, cell-to-pack",
    "katoda": "battery materials: lithium iron phosphate powder, nickel, cobalt",
    "pozar": "a battery fire or a battery safety test (nail penetration)",
    "seal": "the BYD Seal electric sedan",
    "naped": "an electric drive unit / e-axle (8-in-1), electric car motor and inverter",
    "chip": "semiconductors: chips, power modules, wafers; the chip shortage",
    "fabryka": "a car factory / assembly line",
    "ford": "Ford factories: Ford Camaçari (Bahia) or Ford River Rouge",
    "japonia": "Japan: Tokyo, Japanese car industry",
    "navio": "BYD car carrier ships (BYD Explorer No.1) and car carriers at port",
    "seagull": "the BYD Seagull (Dolphin Mini) small electric car",
    "hibrido": "BYD plug-in hybrids (DM-i): Song Plus, Qin Plus, Seal U DM-i",
    "berlim": "Tesla Gigafactory Berlin-Brandenburg in Grünheide, Germany",
    "ladowanie": "an electric car charging at a fast charger",
    "chiny": "China: Chinese cities, the Chinese state, Chinese car market",
    "ue": "European Union: Berlaymont, EU flags, Brussels",
    "europa": "European car industry: Volkswagen, Stellantis",
    "usa": "United States government: Capitol, Washington",
    "camacari": "Camaçari, Bahia: the former Ford plant, now the BYD factory in Brazil",
}

BANCO = {"ladowanie": ["ev_carregando"], "chiny": ["chiny_ev"], "pakiet": ["bateria"], "navio": ["porto_carros"]}

REJEITA_TITULO = [r"toy|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|forza|gran turismo|seagull bird|gull|"
                  r"larus|herring gull|bird"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic", "painting"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_P = ["musk tesla G", "musk tesla", "shenzhen byd", "buffett byd", "munro demontaz", "demontaz byd C", "blade pakiet",
      "blade pakiet", "katoda blade", "pozar blade C", "pakiet seal", "seal demontaz C", "seal pakiet", "tesla munro",
      "naped demontaz", "naped demontaz C", "tesla fabryka", "chip demontaz", "chip naped", "chip fabryka",
      "fabryka byd C", "navio fabryka", "navio byd", "seagull byd C", "seagull chiny", "tesla musk", "hibrido byd",
      "berlim tesla C", "blade berlim", "musk chiny", "byd tesla C", "ladowanie byd", "byd seagull", "seal byd",
      "ue chiny", "chiny byd", "camacari ford C", "demontaz byd", "fabryka chip", "tesla byd", "musk byd F"]
_M = {"G": G, "C": C, "F": F}
_T = {i: [x.split()[0], x.split()[1], _M.get(x.split()[2], E) if len(x.split()) > 2 else E] for i, x in enumerate(_P)}
_FRIO = {9, 19, 36}
_REVEAL = {0, 5, 11, 15, 23, 30}
_ANIM = {2: "S01-Shenzhen", 9: "S02-Prego", 15: "S03-OitoEmUm", 19: "S04-Chips", 24: "S05-Seagull", 30: "S06-Vendas",
         36: "S07-Camacari"}
_CAP = {0: ("A RISADA", "ELON MUSK · 2011"),
        2: ("DE BATERIA DE CELULAR A MONTADORA", "SHENZHEN · 1995"),
        4: ("A DESMONTAGEM", "ENGENHARIA REVERSA"),
        6: ("PRIMEIRO CHOQUE", "A BATERIA BLADE"),
        11: ("SEGUNDO CHOQUE", "A BATERIA É O CHÃO"),
        14: ("TERCEIRO CHOQUE", "OITO EM UM"),
        17: ("QUARTO CHOQUE", "OS CHIPS DA CASA"),
        20: ("QUINTO CHOQUE", "INTEGRAÇÃO VERTICAL"),
        23: ("SEXTO CHOQUE", "O CUSTO"),
        27: ("A TESLA COMPRA DA BYD", "BERLIM"),
        33: ("O OUTRO LADO", "PONTOS FRACOS, SUBSÍDIOS, TARIFAS"),
        36: ("O CAPÍTULO BRASILEIRO", "CAMAÇARI · BAHIA"),
        37: ("O QUE ELES ENCONTRARAM", "UM SISTEMA INTEIRO")}
_SLATE = {2: ["BYD · SHENZHEN", "1995"], 36: ["CAMAÇARI", "BAHIA · BRASIL"]}

'''
(S / "beats.py").write_text(HEAD + re.sub(r"range\(\d+\)", "range(41)", s[j:]), "utf-8")

bp = S / "build_plan.py"
b = bp.read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["byd", "fabryka", "seal"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"demontaz", "pakiet", "naped", "chip", "fabryka", "munro", "katoda"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["fabryka", "demontaz"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["byd", "chiny", "tesla", "seal"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {"musk", "buffett", "munro", "shenzhen", "katoda", "pozar", "seagull", "hibrido", "berlim", '
           '"camacari", "ford", "japonia", "ue", "usa", "europa", "navio", "blade", "pakiet", "naped", "chip", "tesla", "seal"}', b, count=1, flags=re.M)
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + '''CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; "a|b" = alternativas
    "S01-Shenzhen": ["shenzhen", "japonesas"],
    "S02-Prego": ["500", "30", "60"],
    "S03-OitoEmUm": ["8", "oito"],
    "S04-Chips": ["21", "22", "crise"],
    "S05-Seagull": ["70", "10"],
    "S06-Vendas": ["2024", "4", "2025"],
    "S07-Camacari": ["bahia", "chinesa"],
}
''' + b[k:]
bp.write_text(b, "utf-8")

(R / "src" / "scenes" / "BydPtScenes.tsx").write_text('''// As animações de "Musk riu da BYD" (pt, arquivo dark) — painel 20261005-162130 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\\u00a0";

// 1. MAPA: Shenzhen x Japão (p02)
export const S01Shenzhen: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="1995 · BATERIAS PARA CELULAR" lugares={[
    { nome: "Shenzhen · nasce a BYD", lat: 22.54, lon: 114.06, cue: "shenzhen" },
    { nome: "Japão · dominava as baterias", lat: 35.68, lon: 139.69, cue: "japonesas", abaixo: true },
  ]} tint={colors.accent} />
);

// 2. o teste do prego (p09)
export const S02Prego: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Teste de penetração por prego", titulo: "Níquel contra Blade", linhas: [
    { rotulo: "Bateria de níquel", valor: `mais de 500${NB}°C · fogo`, cue: "500" },
    { rotulo: "Blade · de", valor: `30${NB}°C`, cue: "30" },
    { rotulo: "a", valor: `60${NB}°C · sem chama`, cue: "60", destaque: true },
  ], tint: "accent" }} />
);

// 3. o 8 em 1 (p15)
export const S03OitoEmUm: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Num único bloco", titulo: "Sistema 8 em 1", linhas: [
    { rotulo: "Sistema", valor: `8${NB}em${NB}1`, cue: "8", destaque: true },
    { rotulo: "Funções", valor: "oito numa mesma carcaça", cue: "oito" },
  ], tint: "accent" }} />
);

// 4. a crise dos chips (p19)
export const S04Chips: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Chips feitos em casa", titulo: "A grande crise dos chips", linhas: [
    { rotulo: "De", valor: "2021", cue: "21" },
    { rotulo: "a", valor: "2022", cue: "22" },
    { rotulo: "A BYD", valor: "continuou acelerando", cue: "crise", destaque: true },
  ], tint: "accent" }} />
);

// 5. o Seagull (p24)
export const S05Seagull: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD Seagull · gaivota", titulo: "Um elétrico novo de fábrica", linhas: [
    { rotulo: "Na China", valor: `cerca de 70${NB}mil yuans`, cue: "70" },
    { rotulo: "Equivale a", valor: `uns US$${NB}10${NB}mil`, cue: "10", destaque: true },
  ], tint: "accent" }} />
);

// 6. as vendas (p30)
export const S06Vendas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD contra Tesla", titulo: "A maior vendedora de elétricos", linhas: [
    { rotulo: "Em", valor: "2024", cue: "2024" },
    { rotulo: "Eletrificados vendidos", valor: `mais de 4${NB}milhões`, cue: "4", destaque: true },
    { rotulo: "Em 2025", valor: "supera a Tesla no ano inteiro", cue: "2025" },
  ], tint: "accent" }} />
);

// 7. MAPA: Camaçari (p36)
export const S07Camacari: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ONDE A FORD FECHOU, A BYD ABRIU" lugares={[
    { nome: "Camaçari · Bahia", lat: -12.70, lon: -38.32, cue: "bahia", abaixo: true },
    { nome: "Shenzhen · sede da BYD", lat: 22.54, lon: 114.06, cue: "chinesa" },
  ]} tint={colors.accent} />
);
''', "utf-8")
(R / "src" / "scenes" / "index.ts").write_text('''import React from "react";
import type { SceneProps } from "./shared";
import { S01Shenzhen, S02Prego, S03OitoEmUm, S04Chips, S05Seagull, S06Vendas, S07Camacari } from "./BydPtScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: Musk riu da BYD (pt).
export const SCENES: Record<string, SceneEntry> = {
  "S01-Shenzhen": { C: S01Shenzhen, preview: 600 },
  "S02-Prego": { C: S02Prego, preview: 600 },
  "S03-OitoEmUm": { C: S03OitoEmUm, preview: 600 },
  "S04-Chips": { C: S04Chips, preview: 600 },
  "S05-Seagull": { C: S05Seagull, preview: 600 },
  "S06-Vendas": { C: S06Vendas, preview: 600 },
  "S07-Camacari": { C: S07Camacari, preview: 600 },
};
''', "utf-8")

Q = {
    "musk": ["Elon Musk", "Elon Musk Tesla", "Elon Musk 2011", "Elon Musk speaking"],
    "buffett": ["Warren Buffett", "Berkshire Hathaway", "Warren Buffett 2008"],
    "munro": ["Sandy Munro", "Munro and Associates", "car teardown", "vehicle teardown engineering"],
    "shenzhen": ["Shenzhen skyline", "BYD headquarters Shenzhen", "Shenzhen Futian"],
    "seagull": ["BYD Seagull", "BYD Dolphin Mini", "BYD Seagull 2023"],
    "hibrido": ["BYD Song Plus DM-i", "BYD Qin Plus DM-i", "BYD Seal U DM-i", "BYD Song Pro"],
    "berlim": ["Gigafactory Berlin", "Tesla Gigafactory Berlin-Brandenburg", "Tesla Grünheide", "Tesla Model Y Berlin"],
    "camacari": ["Camaçari", "Ford Camaçari", "BYD Camaçari", "Polo Industrial de Camaçari"],
    "navio": ["BYD Explorer No.1", "BYD car carrier ship", "BYD ship", "car carrier ship"],
    "pozar": ["battery fire electric car", "nail penetration test battery", "lithium battery fire"],
    "ford": ["Ford Camaçari", "Ford River Rouge", "Ford Bahia"],
}
CATS = {"Category:BYD Seagull": "seagull", "Category:BYD Dolphin Mini": "seagull", "Category:Gigafactory Berlin-Brandenburg": "berlim",
        "Category:Sandy Munro": "munro", "Category:Warren Buffett": "buffett", "Category:BYD Explorer No.1": "navio",
        "Category:Camaçari": "camacari", "Category:Elon Musk": "musk"}
PEX = {"musk": [], "shenzhen": ["shenzhen skyline"], "pozar": ["battery fire"]}


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 05/10/2026 Musk riu da BYD (baia 1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)


# ---- REUSO
def jl(p, d):
    return json.loads(p.read_text("utf-8")) if p.exists() else d


pool, side = {}, {}
for src in SRC:
    sp, ss = jl(src / "photo_pool.json", {}), jl(src / "photo_side.json", {})
    for t, v in ss.items():
        tag = (v.get("tags") or [""])[0]
        if v.get("verdict") != "ok" or t not in sp or tag in FORA:
            continue
        nt = MAPA.get(tag, tag)
        e = dict(sp[t]); e["tags"] = [nt]
        pool[t] = e
        side[t] = dict(v, tags=[nt])
for nome in ("photo_pool.json", "photo_side.json"):
    if (D / nome).exists():
        (D / (nome + ".bak_antes_reuso")).write_text((D / nome).read_text("utf-8"), "utf-8")
(D / "photo_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
(D / "photo_side.json").write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
ytp, ytr, srs, api, stp, wr = {}, {}, {}, {}, {}, []
for src in SRC:
    ytp.update(jl(src / "yt_pool.json", {}))
    for nome, alvo in (("yt_review.json", ytr), ("api_review.json", api)):
        for k2, fr in jl(src / nome, {}).items():
            d2 = {q: [MAPA.get(t, t) for t in ts if t not in FORA] for q, ts in fr.items()}
            d2 = {q: ts for q, ts in d2.items() if ts}
            if d2:
                alvo[k2] = d2
    srs.update(jl(src / "source_side.json", {}))
    stp.update(jl(src / "stock_api_pool.json", {}))
    wr += jl(src / "window_rejects.json", [])
for nome, obj in [("yt_pool.json", ytp), ("yt_review.json", ytr), ("source_side.json", srs), ("api_review.json", api),
                  ("stock_api_pool.json", stp), ("window_rejects.json", sorted(set(wr))), ("yt_slices.json", {})]:
    (D / nome).write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
from collections import Counter
print("fotos:", len(pool), dict(Counter(e["tags"][0] for e in pool.values())))
print("yt:", len(ytr), " api:", len(api))
print("tema BYD pt gravado")
