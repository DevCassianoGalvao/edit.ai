// As animações de "A montadora chinesa que o Faustão vendia" (pt, arquivo dark) — painel 20261007-124807 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o pedido de 6 de outubro de 2026 (p01)
export const J01Pedido: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="GRUPO SHC · RECUPERAÇÃO JUDICIAL · 6 DE OUTUBRO DE 2026" valor={239500000} cue="239" sep="."
    prefixo={`R$${NB}`} nota={{ texto: "44 empresas no pedido", cue: "44" }} />
);

// 2. MAPA: do Brasil até Anhui (p10)
export const J02Anhui: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FIM DOS ANOS 2000 · A PRÓXIMA GRANDE ONDA" lugares={[
    { nome: "Brasil · o mercado perfeito", lat: -23.55, lon: -46.63, cue: "brasil", abaixo: true },
    { nome: "Hefei · Anhui · JAC Motors", lat: 31.82, lon: 117.23, cue: "anhui" },
  ]} tint={colors.accent} />
);

// 3. a rainha das chinesas em 2011 (p19)
export const J03Rainha: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Emplacamentos · 2011" titulo="A rainha das chinesas" tint={colors.accent} max={23747} barras={[
    { rotulo: "JAC", valor: "23.747", v: 23747, cue: "23" },
    { rotulo: "Chery", valor: "21.680", v: 21680, cue: "21", cor: colors.textDim },
    { rotulo: "Hafei", valor: "16.723", v: 16723, cue: "16", cor: colors.textDim },
  ]} />
);

// 4. o projeto de Camaçari (p27)
export const J04Camacari: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Camaçari · Bahia · projeto de 2012", titulo: "A fábrica prometida", linhas: [
    { rotulo: "Investimento", valor: `R$${NB}900${NB}milhões`, cue: "900" },
    { rotulo: "Capacidade", valor: `100${NB}mil carros por ano`, cue: "100", destaque: true },
    { rotulo: "Pronta", valor: "no fim de 2014", cue: "2014" },
  ], tint: "accent" }} />
);

// 5. a primeira recuperação judicial (p40)
export const J05PrimeiraRJ: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="14" chave={4} linhas={[
    "PEDIDO DE RECUPERAÇÃO JUDICIAL",
    "",
    "Requerente: Grupo SHC",
    "Data: 14 de novembro de 2018",
    `Dívida declarada: R$${NB}517,7${NB}milhões`,
    "Causas: crise, IPI, Inovar-Auto, Citroën",
  ]} carimbo={{ texto: "1ª RECUPERAÇÃO", cue: "517" }} />
);

// 6. os balanços (p48)
export const J06Balanco: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Balanços analisados por auditores", titulo: "Dívida sobre o ativo", linhas: [
    { rotulo: "No período auditado", valor: `364${NB}%`, cue: "364", destaque: true },
    { rotulo: "No começo da recuperação, em 2018", valor: `154${NB}%`, cue: "154" },
  ], tint: "danger" }} />
);

// 7. a mansão de Trancoso (p58)
export const J07Mansao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Trancoso · sul da Bahia · segundo o Metrópoles", titulo: "A mansão", linhas: [
    { rotulo: "Terreno", valor: `40${NB}mil m² de frente para o mar`, cue: "40" },
    { rotulo: "Casa", valor: `12${NB}suítes e 5${NB}bangalôs`, cue: "12" },
    { rotulo: "Vendida por", valor: `R$${NB}300${NB}milhões`, cue: "300", destaque: true },
  ], tint: "danger" }} />
);
