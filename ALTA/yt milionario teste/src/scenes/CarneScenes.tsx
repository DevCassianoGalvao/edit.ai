// As animações de "Os 5 frigoríficos mais expostos à China" (pt, arquivo dark) — painel 20261005-161230 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a salvaguarda (p02)
export const S01Salvaguarda: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Cota do Brasil em 2026 · 1,106${NB}milhão de toneladas`, titulo: "A salvaguarda chinesa", linhas: [
    { rotulo: "Dentro da cota", valor: `12${NB}%`, cue: "12" },
    { rotulo: "Sobretaxa acima da cota", valor: `+55${NB}%`, cue: "55" },
    { rotulo: "Imposto total", valor: `67${NB}%`, cue: "67", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA: a reação em cadeia em Mato Grosso do Sul (p13)
export const S02MatoGrosso: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MATO GROSSO DO SUL · FÉRIAS COLETIVAS E ABATE MENOR" lugares={[
    { nome: "Iguatemi", lat: -23.68, lon: -54.56, cue: "iguatemi", abaixo: true },
    { nome: "São Gabriel do Oeste", lat: -19.39, lon: -54.55, cue: "gabriel" },
    { nome: "Aparecida do Taboado", lat: -20.09, lon: -51.09, cue: "aparecida" },
  ]} tint={colors.accent} />
);

// 3. a Minerva na bolsa (p23)
export const S03Minerva: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quando a China anunciou as cotas", titulo: "Minerva Foods", linhas: [
    { rotulo: "Ações no dia", valor: `quase −7${NB}%`, cue: "7", destaque: true },
    { rotulo: "Vendido no ano anterior", valor: `1${NB}milhão`, cue: "1" },
    { rotulo: "mais", valor: `600${NB}mil toneladas`, cue: "600" },
  ], tint: "accent" }} />
);

// 4. Fortunceres (p30)
export const S04Fortunceres: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Plantas habilitadas para a China", titulo: "Fortunceres", linhas: [
    { rotulo: "Plantas", valor: "6", cue: "seis", destaque: true },
    { rotulo: "Mais do que", valor: "a Minerva no Brasil", cue: "minerva" },
    { rotulo: "Em relação à Marfrig", valor: "3 vezes mais", cue: "tres" },
  ], tint: "accent" }} />
);

// 5. MAPA: Pará longe do consumidor (p42)
export const S05Para: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FRETE LONGO, CARO E REFRIGERADO" lugares={[
    { nome: "Água Azul do Norte · Pará", lat: -6.79, lon: -50.48, cue: "paraense" },
    { nome: "São Paulo", lat: -23.55, lon: -46.63, cue: "paulo", abaixo: true },
  ]} tint={colors.accent} />
);

// 6. a demanda chinesa (p48)
export const S06Demanda: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Carne bovina na China, por ano", titulo: "A demanda não desapareceu", linhas: [
    { rotulo: "Produz cerca de", valor: `7${NB}milhões`, cue: "7" },
    { rotulo: "mais", valor: `800${NB}mil toneladas`, cue: "800" },
    { rotulo: "Consome", valor: `mais de 10${NB}milhões`, cue: "10", destaque: true },
  ], tint: "accent" }} />
);

// 7. recapitulação (p53)
export const S07Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Recapitulando", titulo: "Os mais expostos", linhas: [
    { rotulo: "Naturafrig · abates", valor: `−30${NB}%`, cue: "30" },
    { rotulo: "Minerva · receita ligada à China", valor: `8${NB}%`, cue: "8" },
    { rotulo: "até", valor: `9${NB}%`, cue: "9", destaque: true },
  ], tint: "accent" }} />
);
