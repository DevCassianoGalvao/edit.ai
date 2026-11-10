// Animações de "Inside the Cab of Big Boy 4014" (en) — painel 20261013-231518 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 14 s); todo número é dito; milhar com vírgula (en).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { LinhaDoTempo } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. MAPA: Cheyenne -> Sherman Hill (p02)
export const G01Sherman: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="UNION PACIFIC · WESTBOUND OVER SHERMAN HILL · GRADE 1.55%" lugares={[
    { nome: "Cheyenne", lat: 41.140, lon: -104.820, cue: "cheyenne", abaixo: true, esquerda: true },
    { nome: "Sherman Hill summit", lat: 41.130, lon: -105.400, cue: "sherman", abaixo: true },
    { nome: "Laramie", lat: 41.311, lon: -105.591, cue: "sherman", esquerda: true },
  ]} tint={colors.accent} />
);

// 2. óleo e água por milha (p07)
export const G02Oleo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Big Boy 4014 · on the climb", titulo: "What the giant drinks", linhas: [
    { rotulo: "Fuel oil", valor: `20–25${NB}gal per mile`, cue: "20", destaque: true },
    { rotulo: "Water", valor: `200${NB}gal per mile`, cue: "200" },
    { rotulo: "Tender capacity", valor: `25,000${NB}gal of water`, cue: "tender" },
  ], tint: "accent" }} />
);

// 3. as medidas (p19)
export const G03Medidas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Union Pacific Big Boy · 4-8-8-4", titulo: "Walk around one", linhas: [
    { rotulo: "Length with tender", valor: `132+${NB}feet`, cue: "132", destaque: true },
    { rotulo: "Driving wheels", valor: `68${NB}inches tall`, cue: "68" },
    { rotulo: "Weight, tender loaded", valor: `1,200,000+${NB}lb`, cue: "weighed" },
  ], tint: "accent" }} />
);

// 4. a linha de Harriman (p31)
export const G04Harriman: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sherman Hill · 1953", titulo: "The Harriman line tames the hill", linhas: [
    { rotulo: "Cost of the new line", valor: `$16${NB}million`, cue: "16" },
    { rotulo: "Steepest grade before", valor: `1.55${NB}%`, cue: "1" },
    { rotulo: "Steepest grade after", valor: `0.82${NB}%`, cue: "0", destaque: true },
  ], tint: "accent" }} />
);

// 5. as milhas da 4014 (p37)
export const G05Milhas: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BIG BOY 4014 · RETIRED DECEMBER 7, 1961" valor={1031205} cue="traveled" sufixo={`${NB}miles`} sep=","
    nota={{ texto: "more than a million miles of freight, war and winter", cue: "million" }} />
);

// 6. MAPA: a volta para casa em 2014 (p43)
export const G06Volta: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="APRIL 28 – MAY 8, 2014 · BIG BOY 4014 GOES HOME" lugares={[
    { nome: "West Colton, California", lat: 34.06, lon: -117.36, cue: "colton", abaixo: true },
    { nome: "Cheyenne, Wyoming", lat: 41.14, lon: -104.82, cue: "wyoming", esquerda: true },
  ]} linhas={[
    { pontos: [[32.5, -117.1], [33.7, -118.3], [34.0, -118.8], [34.4, -119.7], [34.5, -120.5], [35.6, -121.2], [36.6, -121.9], [37.8, -122.5], [38.3, -123.0]] },
    { pontos: [[42.0, -124.2], [42.0, -111.05], [41.0, -111.05], [41.0, -104.05]] },
  ]} tint={colors.accent} />
);

// 7. 2019: o fogo volta (p48)
export const G07Fogo: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="Cheyenne steam shop · 2019" tint={colors.accent} marcos={[
    { ano: "Feb 6", texto: "boiler passes the hydrostatic test", cue: "test" },
    { ano: "Apr 9", texto: "fire lit for the first time in almost 60 years", cue: "lit" },
    { ano: "May 1", texto: "4014 moves under its own power", cue: "may", cor: colors.accent },
  ]} />
);

// 8. MAPA: a perna leste da turnê de 2026 (p54)
export const G08Leste: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="2026 TOUR · THE EASTERN LEG" lugares={[
    { nome: "Cheyenne", lat: 41.14, lon: -104.82, cue: "eastern", abaixo: true },
    { nome: "Omaha", lat: 41.26, lon: -95.94, cue: "omaha" },
    { nome: "West Chicago", lat: 41.88, lon: -88.20, cue: "west", abaixo: true },
  ]} marca={{ nome: "Buffalo, New York", lat: 42.89, lon: -78.88, nota: "east of Chicago · first time", cue: "somewhere" }} linhas={[
    { pontos: [[47.2, -95.2], [45.0, -93.2], [43.0, -91.2], [41.5, -90.6], [40.0, -91.4], [38.6, -90.2], [37.0, -89.2], [35.1, -90.1], [32.3, -90.9], [30.5, -91.2], [29.2, -89.3]] },
    { pontos: [[41.6, -87.5], [42.5, -87.8], [43.6, -87.7], [44.5, -87.5], [45.5, -87.0], [46.0, -85.5], [45.8, -84.7], [45.0, -85.5], [44.0, -86.5], [42.8, -86.2], [41.7, -86.8], [41.6, -87.5]] },
    { pontos: [[41.7, -83.5], [42.0, -81.0], [42.9, -78.9], [42.6, -80.5], [41.9, -83.0], [41.7, -83.5]] },
    { pontos: [[29.7, -93.9], [29.3, -94.8], [28.0, -97.0], [26.0, -97.2]] },
  ]} tint={colors.accent} />
);

// 9. MAPA: as 7 irmãs que sobreviveram (p71)
export const G09Irmas: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SEVEN GIANTS, ALL ASLEEP" lugares={[
    { nome: "4004 · Cheyenne", lat: 41.14, lon: -104.82, cue: "cheyenne", abaixo: true },
    { nome: "4005 · Denver", lat: 39.74, lon: -104.99, cue: "denver", abaixo: true },
    { nome: "4018 · Frisco", lat: 33.15, lon: -96.82, cue: "scranton", abaixo: true },
    { nome: "4006 · St. Louis", lat: 38.63, lon: -90.20, cue: "louis", abaixo: true },
    { nome: "4017 · Green Bay", lat: 44.51, lon: -88.01, cue: "scranton" },
    { nome: "4012 · Scranton", lat: 41.41, lon: -75.66, cue: "scranton", esquerda: true },
  ]} marca={{ nome: "4023 · Omaha", lat: 41.26, lon: -95.94, cue: "scranton" }} linhas={[
    { pontos: [[47.2, -95.2], [45.0, -93.2], [43.0, -91.2], [41.5, -90.6], [40.0, -91.4], [38.6, -90.2], [37.0, -89.2], [35.1, -90.1], [32.3, -90.9], [30.5, -91.2], [29.2, -89.3]] },
    { pontos: [[41.6, -87.5], [42.5, -87.8], [43.6, -87.7], [44.5, -87.5], [45.5, -87.0], [46.0, -85.5], [45.8, -84.7], [45.0, -85.5], [44.0, -86.5], [42.8, -86.2], [41.7, -86.8], [41.6, -87.5]] },
    { pontos: [[41.7, -83.5], [42.0, -81.0], [42.9, -78.9], [42.6, -80.5], [41.9, -83.0], [41.7, -83.5]] },
    { pontos: [[29.7, -93.9], [29.3, -94.8], [28.0, -97.0], [26.0, -97.2]] },
  ]} tint={colors.accent} />
);
