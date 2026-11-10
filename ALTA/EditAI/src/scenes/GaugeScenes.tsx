// Animações de "The Day the Gauge Changed" (en) — painel 20261017-011501 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 14 s); todo número é dito; milhar com vírgula (en).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. as duas larguras (p01)
export const G01Allen: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "South Carolina Canal and Rail Road Co.", titulo: "Two widths of track", linhas: [
    { rotulo: "English railways", valor: `4${NB}ft 8½${NB}in`, cue: "english" },
    { rotulo: "Horatio Allen chose", valor: `5${NB}feet`, cue: "five", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA: a linha do Illinois Central (p11)
export const G02Illinois: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CHICAGO, ST. LOUIS & NEW ORLEANS · 547 MILES" lugares={[
    { nome: "East Cairo, Kentucky", lat: 37.00, lon: -89.17, cue: "cairo", esquerda: true },
    { nome: "New Orleans", lat: 29.95, lon: -90.07, cue: "orleans", abaixo: true },
  ]} tint={colors.accent} />
);

// 3. a convenção do Kimball House (p18)
export const G03Kimball: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Kimball House · Atlanta", titulo: "The gauge convention", linhas: [
    { rotulo: "Dates", valor: `February 2–3, 1886`, cue: "2nd" },
    { rotulo: "Railroad officials", valor: `about 70`, cue: "70", destaque: true },
    { rotulo: "Lines represented", valor: `some 30`, cue: "30" },
  ], tint: "accent" }} />
);

// 4. qual largura? (p21)
export const G04Largura: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "How wide, exactly?", titulo: "Choosing the new gauge", linhas: [
    { rotulo: "Most of the country", valor: `4${NB}ft 8½${NB}in`, cue: "eight" },
    { rotulo: "Pennsylvania Railroad", valor: `4${NB}ft 9${NB}in`, cue: "nine", destaque: true },
    { rotulo: "The extra half inch", valor: `slack for old equipment`, cue: "extra" },
  ], tint: "accent" }} />
);

// 5. o exército do L&N (p36)
export const G05LN: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Louisville & Nashville · one day", titulo: "Harahan's army", linhas: [
    { rotulo: "Men on the track", valor: `about 8,000`, cue: "8", destaque: true },
    { rotulo: "Track changed", valor: `about 2,000${NB}miles`, cue: "2" },
    { rotulo: "Men per mile", valor: `about four`, cue: "four" },
  ], tint: "accent" }} />
);

// 6. MAPA: o mesmo treino na mesma manhã (p47)
export const G06Sul: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SAME DRILL, SAME MORNING" lugares={[
    { nome: "Richmond & Danville", lat: 37.54, lon: -77.43, cue: "richmond", esquerda: true },
    { nome: "Cincinnati Southern", lat: 39.10, lon: -84.51, cue: "cincinnati" },
    { nome: "Alabama Great Southern", lat: 33.52, lon: -86.80, cue: "alabama", abaixo: true },
    { nome: "Georgia lines", lat: 33.75, lon: -84.39, cue: "georgia", esquerda: true },
  ]} tint={colors.accent} />
);

// 7. o tamanho (p56)
export const G07Tamanho: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "So how big was it?", titulo: "Counting the miles", linhas: [
    { rotulo: "Southern Railway estimate", valor: `11,500${NB}miles`, cue: "11", destaque: true },
    { rotulo: "Other accounts", valor: `11,000${NB}miles`, cue: "accounts" },
    { rotulo: "At least one claim", valor: `24${NB}hours`, cue: "24" },
  ], tint: "accent" }} />
);

// 8. a última meia polegada (p61)
export const G08Meia: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The last half inch", titulo: "Still not standard", linhas: [
    { rotulo: "The South after the change", valor: `4${NB}ft 9${NB}in`, cue: "nine" },
    { rotulo: "The national standard", valor: `4${NB}ft 8½${NB}in`, cue: "eight", destaque: true },
  ], tint: "accent" }} />
);

// 9. fecho (p65)
export const G09Fim: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "May 31 – June 1, 1886", titulo: "The days they changed the gauge", linhas: [
    { rotulo: "One rail moved", valor: `3${NB}inches`, cue: "three" },
    { rotulo: "Track converted", valor: `11,500${NB}miles`, cue: "11", destaque: true },
    { rotulo: "Time", valor: `about 36${NB}hours`, cue: "36" },
  ], tint: "accent" }} />
);
