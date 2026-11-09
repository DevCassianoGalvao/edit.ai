// As animações de "7 Fábricas de Carro Que Fecharam no Brasil" (pt, arquivo dark) — painel 20261007-125241 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o investimento da Mercedes em Iracemápolis (p02)
export const F01Mercedes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MERCEDES-BENZ · IRACEMÁPOLIS · MARÇO DE 2016" valor={170} cue="170" sep="."
    prefixo={`€${NB}`} sufixo={`${NB}milhões`} nota={{ texto: `perto de R$${NB}600${NB}milhões na época`, cue: "600" }} />
);

// 2. MAPA: as três fábricas da Ford fechadas de uma vez (p17)
export const F02TresFord: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FORD · 11 DE JANEIRO DE 2021 · TRÊS FÁBRICAS DE UMA VEZ" lugares={[
    { nome: "Camaçari · Bahia", lat: -12.70, lon: -38.32, cue: "camas|kamas" },
    { nome: "Taubaté · São Paulo", lat: -23.03, lon: -45.56, cue: "taubat", abaixo: true },
    { nome: "Troller · Horizonte · Ceará", lat: -4.10, lon: -38.49, cue: "horizon" },
  ]} tint={colors.accent} />
);

// 3. o complexo de Camaçari em 2001 (p36)
export const F03Camacari: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ford · Camaçari · 12 de outubro de 2001", titulo: "O maior complexo da lista", linhas: [
    { rotulo: "Inauguração", valor: "12 de outubro de 2001", cue: "12" },
    { rotulo: "Capacidade", valor: `250${NB}mil carros por ano`, cue: "250", destaque: true },
    { rotulo: "Empregos", valor: `cerca de 7.900`, cue: "7" },
  ], tint: "accent" }} />
);

// 4. a capacidade da BYD em Camaçari (p45)
export const F04BydCapacidade: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BYD · CAMAÇARI · VEÍCULOS POR ANO" valor={300000} cue="300" sep="."
    nota={{ texto: `investimento anunciado: R$${NB}5,5${NB}bilhões`, cue: "5" }} barras={[
      { rotulo: "1ª fase", v: 150000, cue: "150" },
      { rotulo: "2ª fase", v: 300000, cue: "300", destaque: true },
    ]} />
);

// 5. as vendas da Jaguar Land Rover em 2025 (p63)
export const F05Evoque: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Jaguar Land Rover · Itatiaia · 2025" titulo="Vendas contra a capacidade" tint={colors.accent} max={24000} barras={[
    { rotulo: "Discovery Sport", valor: "425", v: 425, cue: "425", cor: colors.textDim },
    { rotulo: "Range Rover Evoque", valor: "332", v: 332, cue: "332", cor: colors.textDim },
    { rotulo: "Os dois somados", valor: "757", v: 757, cue: "757" },
    { rotulo: "Capacidade da fábrica", valor: "24.000", v: 24000, cue: "24" },
  ]} />
);

// 6. o plano da Toyota em Sorocaba (p78)
export const F06Sorocaba: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Toyota · plano até 2030", titulo: "Tudo para Sorocaba", linhas: [
    { rotulo: "Investimento no país", valor: `R$${NB}11${NB}bilhões`, cue: "11", destaque: true },
    { rotulo: "Sorocaba hoje", valor: `170${NB}mil veículos por ano`, cue: "170" },
    { rotulo: "Sorocaba depois", valor: `cerca de 270${NB}mil por ano`, cue: "270" },
  ], tint: "accent" }} />
);
