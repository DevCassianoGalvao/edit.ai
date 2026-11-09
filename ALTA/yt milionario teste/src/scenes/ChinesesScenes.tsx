// Animações de "7 Carros Chineses Que os Brasileiros SE RECUSAM a Comprar em 2026" (pt, enxuto) — painel 20261015-012323 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Zeekr 7X: a versão mais barata perdeu um motor (p06)
export const C01Zeekr: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Zeekr 7X · Brasil", titulo: `70${NB}mil a menos`, linhas: [
    { rotulo: "Flagship", valor: `R$${NB}448${NB}mil`, cue: "70" },
    { rotulo: "Premium · junho", valor: `R$${NB}378${NB}mil`, cue: "378", destaque: true },
    { rotulo: "Potência antes", valor: `646${NB}cv`, cue: "646" },
    { rotulo: "Potência com um motor", valor: `421${NB}cv`, cue: "421", destaque: true },
  ], tint: "accent" }} />
);

// 2. GAC Hyptec HT: R$ 50 mil pelas portas asa de gaivota (p16)
export const C02Portas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "GAC Hyptec HT · lançamento", titulo: "O preço das portas", linhas: [
    { rotulo: "Elite", valor: `R$${NB}299.990`, cue: "349" },
    { rotulo: "Ultra · asa de gaivota", valor: `R$${NB}349.990`, cue: "349" },
    { rotulo: "Diferença", valor: `R$${NB}50${NB}mil`, cue: "50", destaque: true },
  ], tint: "accent" }} />
);

// 3. MG Cyberster: Fipe abaixo do preço sugerido (p25)
export const C03Fipe: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "MG Cyberster · linha 2026", titulo: "O mercado já paga menos", linhas: [
    { rotulo: "Preço sugerido", valor: `R$${NB}529.800`, cue: "477" },
    { rotulo: "Tabela Fipe · setembro", valor: `R$${NB}477.569`, cue: "477", destaque: true },
    { rotulo: "Abaixo do sugerido", valor: `+${NB}de${NB}R$${NB}50${NB}mil`, cue: "50" },
  ], tint: "danger" }} />
);

// 4. Aion UT x Aion ES na mesma concessionária (p35)
export const C04Aion: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="GAC · emplacamentos · setembro de 2026" titulo="O rival na mesma loja"
    tint={colors.accent} max={1500} barras={[
    { rotulo: "GAC Aion UT", valor: `1.470`, v: 1470, cue: "1" },
    { rotulo: "GAC Aion ES", valor: `8`, v: 8, cue: "8", cor: colors.danger },
  ]} />
);

// 5. MAPA: as 3 concessionárias da Neta + a loja de São Paulo (p41)
export const C05Neta: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="NETA NO BRASIL · 3 CONCESSIONÁRIAS" lugares={[
    { nome: "Rio de Janeiro", lat: -22.91, lon: -43.17, cue: "rio", abaixo: true },
    { nome: "Brasília", lat: -15.79, lon: -47.88, cue: "brasília" },
    { nome: "Manaus", lat: -3.12, lon: -60.02, cue: "manaus" },
    { nome: "São Paulo · virou Ford", lat: -23.55, lon: -46.63, cue: "são", abaixo: true, esquerda: true },
  ]} tint={colors.accent} />
);

// 6. Dolphin Mini x E-JS1 (p52)
export const C06Abismo: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Emplacamentos · setembro de 2026" titulo="O tamanho do abismo"
    tint={colors.accent} max={9385} barras={[
    { rotulo: "BYD Dolphin Mini", valor: `9.385`, v: 9385, cue: "9" },
    { rotulo: "JAC E-JS1", valor: `5`, v: 5, cue: "5", cor: colors.danger },
  ]} nota={{ texto: `mais de 1.800 Dolphin Mini para cada E-JS1`, cue: "1" }} />
);

// 7. BYD Tan: Fipe perto da metade do zero km (p63)
export const C07Tan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD Tan elétrico AWD · ano 2023", titulo: "Metade em três anos", linhas: [
    { rotulo: "Tabela Fipe · agosto de 2026", valor: `R$${NB}260.468`, cue: "260", destaque: true },
    { rotulo: "Zero quilômetro", valor: `≈${NB}R$${NB}500${NB}mil`, cue: "500" },
  ], tint: "danger" }} />
);
