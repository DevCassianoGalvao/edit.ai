// Animações de "O Que Acontece com a Comida que Ninguém Come no Maior Navio do Mundo" (pt) — painel 20261018-151302
// (baia 1, modo enxuto). REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o navio em números (p01)
export const C01Navio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Icon of the Seas · Royal Caribbean", titulo: "O maior navio do mundo", linhas: [
    { rotulo: "Comprimento", valor: `cerca de 365${NB}m`, cue: "365", destaque: true },
    { rotulo: "Conveses", valor: "20", cue: "20" },
    { rotulo: "Arqueação bruta", valor: `250.800${NB}t`, cue: "250" },
  ], tint: "accent" }} />
);

// 2. comida que sobe a bordo numa viagem de 7 dias (p05)
export const C02Comida: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UMA VIAGEM DE SETE DIAS · COMIDA A BORDO" valor={59} cue="59" sufixo=" toneladas" sep="."
    nota={{ texto: "cerca de 130 mil libras · o peso de uns 40 carros populares", cue: "40" }} />
);

// 3. lagostas e sobremesas por dia (p07)
export const C03Sobremesas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Wall Street Journal · por dia", titulo: "A cozinha do Icon", linhas: [
    { rotulo: "Caudas de lagosta", valor: "cerca de 4.000", cue: "4" },
    { rotulo: "Sobremesas", valor: "40.000", cue: "40", destaque: true },
    { rotulo: "Se 1 em cada 10 sobrar", valor: "4.000 restos de doce", cue: "10" },
  ], tint: "accent" }} />
);

// 4. a regra das 4 horas (p13)
export const C04Horas: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="COMIDA EXPOSTA NO BUFÊ · PRAZO" valor={4} cue="4" sufixo=" horas" sep="."
    nota={{ texto: "depois disso, vai para o lixo — mesmo que ninguém tenha tocado", cue: "tocada" }} />
);

// 5. a peneira de 25 mm (p29)
export const C05Peneira: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="REGRA INTERNACIONAL · COMIDA TRITURADA" valor={25} cue="25" sufixo=" mm" sep="."
    nota={{ texto: "abertura máxima da peneira · dois centímetros e meio", cue: "centímetros" }} />
);

// 6. energia do lixo: 200 kW (p65)
export const C06Energia: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="USINA MAP · COMEÇO DE 2024" valor={200} cue="200" sufixo=" kW" sep="."
    nota={{ texto: "algumas dezenas de chuveiros elétricos ligados ao mesmo tempo", cue: "chuveiros" }} />
);

// 7. 12 milhas náuticas = 22 km (p75)
export const C07Milhas: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="MARPOL · ANEXO V · COMIDA NO MAR" titulo="Distância mínima da costa" tint={colors.accent} max={22}
    barras={[
      { rotulo: "1 milha náutica", valor: `1.852${NB}m`, v: 1.852, cue: "1" },
      { rotulo: "12 milhas náuticas · sem triturar", valor: `22${NB}km`, v: 22, cue: "22", cor: colors.danger },
    ]} />
);

// 8. MAPA: a área especial do Grande Caribe (p79)
export const C08Caribe: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MARPOL · ÁREA ESPECIAL DO GRANDE CARIBE · 2011" lugares={[
    { nome: "Golfo do México", lat: 25.0, lon: -90.0, cue: "Golfo", abaixo: true },
    { nome: "Mar do Caribe", lat: 15.0, lon: -75.0, cue: "Caribe", abaixo: true },
    { nome: "Atlântico", lat: 27.0, lon: -70.0, cue: "Atlântico", esquerda: true },
  ]} tint={colors.accent} />
);

// 9. MAPA: os portos do Four Good Food (p99)
export const C09Portos: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="COSTA CRUZEIROS · FOUR GOOD FOOD" lugares={[
    { nome: "Savona", lat: 44.31, lon: 8.48, cue: "Savona" },
    { nome: "Civitavecchia", lat: 42.09, lon: 11.80, cue: "Civitavecchia", abaixo: true },
    { nome: "Marselha", lat: 43.30, lon: 5.37, cue: "Mars", esquerda: true },
    { nome: "Palermo", lat: 38.12, lon: 13.36, cue: "Palermo", abaixo: true },
    { nome: "Barcelona", lat: 41.39, lon: 2.17, cue: "Barcelona", esquerda: true, abaixo: true },
  ]} tint={colors.accent} />
);

// 10. 14 piscinas olímpicas de comida (p105)
export const C10Piscinas: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ROYAL CARIBBEAN · RESTO DE COMIDA EM 2022" valor={53655} cue="53" sufixo=" m³" sep="."
    nota={{ texto: "compactado: 14 piscinas olímpicas cheias", cue: "14" }} />
);

// 11. a meta: 24 % ou 33 % contra 50 % (p107)
export const C11Meta: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="DESPERDÍCIO DE COMIDA · ROYAL CARIBBEAN" titulo="Os números não batem" tint={colors.accent} max={50}
    barras={[
      { rotulo: "The Takeout · desde 2019", valor: "−24%", v: 24, cue: "24" },
      { rotulo: "Blog da Royal · começo de 2024", valor: "−33%", v: 33, cue: "33" },
      { rotulo: "Meta para 2025", valor: "−50%", v: 50, cue: "50", cor: colors.textDim },
    ]} />
);
