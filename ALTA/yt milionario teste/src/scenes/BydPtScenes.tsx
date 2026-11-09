// As animações de "Musk riu da BYD" (pt, arquivo dark) — painel 20261005-162130 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

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
