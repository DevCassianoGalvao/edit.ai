// Animações de "Como Vivem os Técnicos que Cuidam das Torres de Energia no Meio da Floresta" (pt, enxuto) — painel 20261029-105046 (b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// contorno aproximado do norte do Brasil (costa e fronteira), só como referência do mapa
const NORTE: [number, number][] = [[-3.0, -41.0], [-2.5, -44.0], [-1.0, -46.5], [0.0, -49.5], [2.0, -50.8], [4.4, -51.6],
  [2.3, -54.0], [2.0, -55.9], [4.0, -59.8], [5.2, -60.7], [4.2, -64.0], [2.0, -67.0], [1.2, -69.6], [-1.0, -69.5], [-4.0, -70.0],
  [-7.5, -73.9], [-9.8, -70.5], [-10.0, -65.5]];

// 1. MAPA: de Tucuruí a Macapá e a Manaus (p02)
export const T01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LINHÃO DE TUCURUÍ · PARÁ, AMAPÁ E AMAZONAS" lugares={[
    { nome: "Usina de Tucuruí", lat: -3.83, lon: -49.65, cue: "tucuru" },
    { nome: "Macapá", lat: 0.03, lon: -51.07, cue: "macap" },
    { nome: "Manaus", lat: -3.12, lon: -60.02, cue: "manaus", abaixo: true },
  ]} linhas={[{ pontos: NORTE }]} tint={colors.accent} />
);

// 2. Os três lotes (p11)
export const T02Lotes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Linhão de Tucuruí · três lotes", titulo: "Quilômetros por trecho", linhas: [
    { rotulo: "Tucuruí a Jurupari", valor: `527${NB}km`, cue: "527" },
    { rotulo: "Oriximiná a Macapá", valor: `713${NB}km`, cue: "713", destaque: true },
    { rotulo: "Oriximiná a Manaus", valor: `586${NB}km`, cue: "586" },
  ], tint: "cool" }} />
);

// 3. MAPA: Manaus a Boa Vista (p32)
export const T03Mapa2: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="EXTENSÃO MANAUS – BOA VISTA · BR-174" unidade="km" lugares={[
    { nome: "Manaus", lat: -3.12, lon: -60.02, valor: 0, cue: "manaus" },
    { nome: "Boa Vista", lat: 2.82, lon: -60.67, valor: 721, cue: "721", esquerda: true },
  ]} linhas={[{ pontos: NORTE }]} tint={colors.accent} />
);

// 4. Travessia do Amazonas (p60)
export const T04Travessia: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Travessia do Rio Amazonas · ilha de Jurupari", titulo: "Altura de cada torre", linhas: [
    { rotulo: "Torres da travessia", valor: `295${NB}m`, cue: "295", destaque: true },
    { rotulo: "Torre Eiffel, em Paris", valor: `324${NB}m`, cue: "324" },
  ], tint: "cool" }} />
);

// 5. Distância até o ponto da falha (p75)
export const T05Falha: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="A LINHA CAIU · DISTÂNCIA ATÉ O PONTO PROVÁVEL DA FALHA" valor={80} sufixo={`${NB}km`} cue="80"
    sep="." nota={{ texto: "em um trecho sem estrada boa", cue: "80" }} />
);

// 6. Extensão para Roraima (p96)
export const T06Roraima: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Extensão para Roraima · cerca de 721 km", titulo: "Rodovia e donos da concessão", linhas: [
    { rotulo: "Rodovia que a linha acompanha", valor: "BR-174", cue: "174" },
    { rotulo: "Alupar", valor: `51${NB}%`, cue: "51", destaque: true },
    { rotulo: "Eletronorte", valor: `49${NB}%`, cue: "49" },
  ], tint: "accent" }} />
);

// 7. Os números do Linhão (p129)
export const T07Resumo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Linhão de Tucuruí", titulo: "Os números em resumo", linhas: [
    { rotulo: "Extensão", valor: `1.800${NB}km`, cue: "1" },
    { rotulo: "Torres", valor: `3.600`, cue: "3" },
    { rotulo: "Tensão", valor: `500${NB}kV`, cue: "500", destaque: true },
    { rotulo: "Capacidade de transporte", valor: `2.400${NB}MW`, cue: "2" },
  ], tint: "accent" }} />
);
