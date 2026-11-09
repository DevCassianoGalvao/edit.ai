// Animações de "Como Vivem os Milionários que Pagam US$ 15 Milhões para Morar em um Navio" (pt, arquivo dark) —
// painel 20261010-020012 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o navio (p01)
export const W01Navio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "MS The World · navio residencial", titulo: "Um condomínio que navega", linhas: [
    { rotulo: "Comprimento", valor: `196${NB}m`, cue: "196" },
    { rotulo: "Conveses", valor: "12", cue: "12" },
    { rotulo: "Peso", valor: `cerca de 43${NB}mil toneladas`, cue: "43", destaque: true },
  ], tint: "cool" }} />
);

// 2. o casco rebocado (p09)
export const W02Casco: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O CASCO REBOCADO PELO MAR" lugares={[
    { nome: "Landskrona · Suécia", lat: 55.87, lon: 12.83, cue: "landskrona", abaixo: true },
    { nome: "Rissa · Noruega", lat: 63.58, lon: 9.96, cue: "rissa" },
  ]} tint={colors.cool} />
);

// 3. a taxa anual (p21)
export const W03Taxa: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Taxa anual dos moradores", titulo: "O preço de manter a casa navegando", linhas: [
    { rotulo: "Mínimo anual · menor unidade", valor: `US$${NB}200${NB}mil`, cue: "200", destaque: true },
    { rotulo: "Segundo várias reportagens", valor: `≈${NB}10${NB}% do apartamento por ano`, cue: "10" },
  ], tint: "accent" }} />
);

// 4. quem mora (p38)
export const W04Familias: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="DONOS DE RESIDÊNCIAS NO THE WORLD" valor={150} cue="150" sep="."
    prefixo={`cerca de${NB}`} sufixo={`${NB}famílias`}
    nota={{ texto: `de uns 20${NB}países`, cue: "20" }} />
);

// 5. a soma das viagens (p68)
export const W05Portos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ATÉ 2017" valor={1213} cue="1" sep="."
    sufixo={`${NB}portos visitados`}
    nota={{ texto: `quase 30${NB}voltas na Terra pela linha do Equador`, cue: "30" }} />
);

// 6. Passagem do Noroeste (p72)
const NOROESTE: [number, number][] = [[64.5, -165.4], [71.3, -156.8], [70.2, -133.0], [68.6, -110.0], [69.2, -100.0],
  [74.2, -94.0], [74.0, -80.0], [72.5, -70.0], [68.5, -58.0], [64.2, -51.7]];
export const W06Noroeste: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="PASSAGEM DO NOROESTE · 2012" unidade="dias" lugares={[
    { nome: "Nome · Alasca", lat: 64.5, lon: -165.4, valor: 0, cue: "18", abaixo: true },
    { nome: "Nuuk · Groenlândia", lat: 64.18, lon: -51.72, valor: 26, cue: "12", abaixo: true },
  ]} linhas={[{ pontos: NOROESTE }]} tint={colors.cool} />
);

// 7. a pandemia: sem porto (p87)
export const W07Pandemia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="PANDEMIA · SEM PORTO PARA PARAR" lugares={[
    { nome: "Fremantle · Austrália", lat: -32.06, lon: 115.74, cue: "fremantle" },
    { nome: "Nova Zelândia · pedido negado", lat: -41.29, lon: 174.78, cue: "zelandia", abaixo: true },
  ]} tint={colors.accent} />
);

// 8. o rival (p96)
export const W08Explorer: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Seven Seas Explorer · Regent Seven Seas", titulo: "Hotel de luxo flutuante", linhas: [
    { rotulo: "Hóspedes", valor: "750", cue: "750" },
    { rotulo: "Tripulantes", valor: "552", cue: "552", destaque: true },
    { rotulo: "Só na cozinha", valor: `cerca de 102`, cue: "102" },
  ], tint: "accent" }} />
);

// 9. pode ser ele (p116)
export const W09Ele: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "MS The World", titulo: "Pode ser ele", linhas: [
    { rotulo: "Navio branco", valor: `196${NB}m`, cue: "196" },
    { rotulo: "Conveses", valor: "12", cue: "12" },
    { rotulo: "Famílias", valor: "150", cue: "150" },
    { rotulo: "Pessoas trabalhando", valor: "280", cue: "280", destaque: true },
  ], tint: "cool" }} />
);
