// As 7 animações de "Australia's New Invention Could Replace Coal Forever" (en, 26,2 min). Pedido do painel (auto).
// REGRA (25/09 + 26/09/2026): biblioteca + MAPA — Colunas, Odometro, Painel, Barras, Lista, MapaCampanha, Documento.
// Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES na grafia do Whisper ("CSIRO", "$65", "$1 .3").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. o que o carvão faz: três trabalhos (p07) ----------------
export const S01Tres: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="REPLACING COAL MEANS REPLACING THREE THINGS AT ONCE"
    tint={colors.accent}
    cols={[
      { titulo: "Power at night", texto: "steady electricity after sunset", cue: "night", cor: colors.cool },
      { titulo: "Heat for heavy industry", texto: "smelters, furnaces, steel", cue: "heat", cor: colors.accent },
      { titulo: "A fuel that ships", texto: "exported across oceans", cue: "fuel", cor: colors.danger },
    ]}
  />
);

// ---------------- 2. vapor supercrítico, CSIRO 2014 (p15) ----------------
export const S02Vapor: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="SUPERCRITICAL STEAM FROM SUNLIGHT · CSIRO NEWCASTLE · 2014"
    valor={570}
    cue="570"
    sufixo=" °C"
    nota={{ texto: "at more than 200 times the pressure of the air around us", cue: "200" }}
  />
);

// ---------------- 3. Vast Solar One (p21) ----------------
export const S03VastOne: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Vast Solar One · Port Augusta, South Australia",
      titulo: "A solar plant that works after dark",
      linhas: [
        { rotulo: "Power", valor: "30 MW", cue: "30" },
        { rotulo: "Thermal storage", valor: "288 MWh in hot salt", cue: "288" },
        { rotulo: "After sunset", valor: "more than eight hours", cue: "eight" },
        { rotulo: "ARENA grant", valor: "up to $65 million", cue: "65" },
        { rotulo: "Concessional finance", valor: "up to $110 million", cue: "110", destaque: true },
      ],
      tint: "accent",
    }}
  />
);

// ---------------- 4. escala: 30 MW x uma usina a carvão (p22) ----------------
export const S04Escala: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Not a replacement — a reference plant"
    titulo="Thirty megawatts is not enormous"
    tint={colors.cool}
    max={1000}
    barras={[
      { rotulo: "Vast Solar One", valor: "30 MW", v: 30, cue: "30", cor: colors.accent },
      { rotulo: "A big coal plant", valor: "well over 1,000 MW", v: 1000, cue: "thousand", cor: colors.textDim },
    ]}
    nota={{ texto: "Its job is to prove the technology works", cue: "reference" }}
  />
);

// ---------------- 5. o ciclo da céria (p31) ----------------
export const S05Ceria: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Solar thermochemical water splitting · doped ceria"
    titulo="A mineral that breathes oxygen"
    tint={colors.accent}
    itens={[
      { titulo: "Concentrated sunlight heats the ceria", cue: "heats" },
      { titulo: "It releases oxygen — now it is hungry for oxygen", cue: "hungry" },
      { titulo: "Steam is fed into the reactor", cue: "steam" },
      { titulo: "The ceria grabs the oxygen: pure hydrogen is left", cue: "hydrogen", cor: colors.cool },
      { titulo: "Heat it again — the cycle repeats", cue: "cycle", cor: colors.accent },
    ]}
  />
);

// ---------------- 6. mesmas rotas, outra carga (MAPA, p38) ----------------
const AUSTRALIA: [number, number][] = [
  [-10.7, 142.5], [-16.9, 145.8], [-19.3, 146.8], [-23.4, 150.5], [-27.5, 153.1], [-32.9, 151.8], [-33.9, 151.2],
  [-37.5, 149.9], [-38.4, 145.0], [-38.1, 140.7], [-35.6, 138.1], [-34.9, 138.5], [-32.5, 137.8], [-34.8, 135.8],
  [-32.1, 133.6], [-31.7, 129.0], [-33.9, 122.0], [-35.0, 117.9], [-31.95, 115.85], [-24.9, 113.6], [-20.3, 118.6],
  [-17.9, 122.2], [-14.9, 128.0], [-12.4, 130.8], [-12.2, 136.8], [-17.5, 140.8], [-10.7, 142.5],
];
const COREIA: [number, number][] = [
  [38.6, 128.4], [37.5, 129.1], [35.5, 129.4], [35.1, 129.0], [34.6, 127.7], [34.7, 126.3], [35.9, 126.6], [37.5, 126.6], [37.8, 126.2],
];
const JAPAO: [number, number][] = [
  [41.4, 141.4], [40.5, 141.9], [38.3, 141.5], [36.9, 140.8], [35.6, 140.1], [34.9, 139.1], [34.6, 137.2], [33.5, 135.8],
  [34.3, 134.9], [34.0, 132.9], [33.0, 132.0], [31.0, 130.6], [31.6, 130.2], [33.6, 130.2], [34.3, 131.0], [35.5, 133.1],
  [35.6, 135.5], [37.0, 136.8], [37.9, 139.1], [39.8, 140.0], [41.4, 141.4],
];
const CHINA: [number, number][] = [
  [40.9, 121.6], [39.0, 121.6], [37.4, 122.6], [36.1, 120.4], [34.8, 119.3], [32.0, 121.8], [30.6, 122.0], [27.9, 120.8],
  [24.5, 118.1], [22.5, 114.2], [21.5, 109.8], [20.2, 110.3],
];
export const S06Rotas: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="SAME CUSTOMERS · SAME PORTS · SAME TRADE ROUTES · A DIFFERENT CARGO"
    pontos={[
      { nome: "Australian ports", lat: -27.5, lon: 153.1, data: "COAL TODAY · AMMONIA & METHANOL TOMORROW", cue: "australian" },
      { nome: "Japan", lat: 35.7, lon: 139.7, data: "BUYS AUSTRALIAN COAL", cue: "japan" },
      { nome: "South Korea", lat: 37.5, lon: 127.0, data: "BUYS AUSTRALIAN COAL", cue: "korea", lado: "esq" },
    ]}
    setas={[
      { de: 0, para: 1, cue: "ammonia" },
      { de: 0, para: 2, cue: "methanol", cor: "#1f5f8b" },
    ]}
    costa={[AUSTRALIA, COREIA, JAPAO, CHINA]}
  />
);

// ---------------- 7. o corte do orçamento 2026 (p45) ----------------
export const S07Corte: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    linhas={[
      "AUSTRALIAN GOVERNMENT · FEDERAL BUDGET 2026",
      "",
      "Hydrogen Headstart — cut back",
      "Solar Sunshot — cut back",
      "Total: around $1.3 billion over 10 years",
      "Reason: hydrogen industry to produce much less than forecast",
      "Hydrogen tax incentive estimate: nearly $2 billion lower",
    ]}
    cue="2026"
    chave={4}
    carimbo={{ texto: "CUT", cue: "cut", cor: colors.danger }}
  />
);
