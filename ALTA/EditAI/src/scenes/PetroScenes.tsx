// Animações de "Como é a Vida no Maior Petroleiro do Mundo?" (pt) — painel 20261025-125314
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a carga (p04)
export const P01Carga: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CLASSE TI · PETRÓLEO BRUTO NOS TANQUES" valor={2800000} cue="2" sufixo=" barris" sep="."
    nota={{ texto: "a Euronav divulgou 3 milhões de barris por navio", cue: "3" }} />
);

// 2. a tripulação (p12)
export const P02Tripulacao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quem leva o maior petroleiro do mundo", titulo: "Classe TI", linhas: [
    { rotulo: "Tripulação", valor: "35 a 40 pessoas", cue: "35", destaque: true },
    { rotulo: "Motor funcionando", valor: "24 horas por dia", cue: "24" },
  ], tint: "accent" }} />
);

// 3. a Convenção do Trabalho Marítimo (p16)
export const P03Mlc: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="11" linhas={[
    "CONVENÇÃO DO TRABALHO MARÍTIMO",
    "· máximo seguido a bordo, sem férias: 11 meses",
    "· direito de voltar para casa antes de 12 meses",
  ]} chave={1} carimbo={{ texto: "12 MESES", cue: "12" }} />
);

// 4. o descanso (p26)
export const P04Descanso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Convenção do Trabalho Marítimo", titulo: "Descanso mínimo", linhas: [
    { rotulo: "A cada 24 horas", valor: "10 horas", cue: "10", destaque: true },
    { rotulo: "A cada 7 dias", valor: "77 horas", cue: "77" },
    { rotulo: "Um bloco seguido de", valor: "6 horas", cue: "6" },
  ], tint: "accent" }} />
);

// 5. oxigênio no gás inerte (p43)
export const P05Oxigenio: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="OXIGÊNIO NO GÁS INERTE · A LAVAGEM PARA ACIMA DE" valor={8} cue="8" sufixo=" %" sep="."
    barras={[{ rotulo: "Limite das regras (%)", v: 8, cue: "8", destaque: true },
      { rotulo: "Meta das tripulações: 3 a 5 (%)", v: 5, cue: "5" }]} />
);

// 6. MAPA: a grande estrada do petróleo (p54)
const COSTA: { pontos: [number, number][] }[] = [
  { pontos: [[30.0, 48.6], [27.0, 50.0], [25.0, 51.6], [24.1, 53.6], [25.4, 56.3], [26.3, 56.4], [24.0, 57.6], [22.5, 59.8],
    [19.0, 57.7], [17.0, 55.0], [14.0, 48.5], [12.6, 44.0]] },
  { pontos: [[30.0, 48.6], [29.0, 50.7], [27.2, 56.3], [25.3, 61.5], [24.8, 66.8], [23.0, 68.6], [21.0, 72.6], [15.5, 73.8],
    [8.1, 77.5], [13.0, 80.3], [17.0, 82.3], [21.5, 87.0], [22.0, 89.5], [20.0, 92.8], [16.0, 94.3], [16.5, 97.6],
    [10.0, 98.5], [6.0, 100.3], [2.5, 101.5], [1.4, 103.8], [6.0, 102.3], [10.5, 99.4], [13.4, 100.2], [10.5, 104.0],
    [10.4, 107.0], [16.0, 108.2], [21.5, 108.0], [22.3, 114.0], [25.0, 119.5], [31.0, 121.9], [35.0, 119.5], [39.0, 118.5]] },
  { pontos: [[5.6, 95.3], [3.5, 98.6], [1.0, 102.5], [-3.0, 106.0], [-5.8, 105.8], [-4.0, 102.2], [0.5, 99.0], [5.6, 95.3]] },
  { pontos: [[33.5, 130.4], [34.6, 135.2], [35.0, 137.0], [35.4, 139.7], [36.6, 140.7]] },
];
export const P06Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="GOLFO PÉRSICO → JAPÃO · MAIS DE 6.600 MILHAS NÁUTICAS" linhas={COSTA} lugares={[
    { nome: "Golfo Pérsico", lat: 27.0, lon: 51.5, cue: "golfo", esquerda: true, abaixo: true },
    { nome: "Ormuz", lat: 26.6, lon: 56.5, cue: "hormuz" },
    { nome: "Oceano Índico", lat: 6.0, lon: 80.0, cue: "indico", esquerda: true, abaixo: true },
    { nome: "Malaca", lat: 3.0, lon: 100.6, cue: "malaca" },
    { nome: "Singapura", lat: 1.2, lon: 104.0, cue: "singapura", abaixo: true },
    { nome: "Japão", lat: 34.8, lon: 136.8, cue: "japao", esquerda: true },
  ]} tint={colors.accent} />
);

// 7. tempo em terra (p63)
export const P07Terra: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Universidade Marítima Mundial · 2025" titulo="Quanto tempo conseguiram ficar em terra" tint={colors.accent}
    max={100} barras={[
      { rotulo: "Menos de 3 horas", valor: "47%", v: 47, cue: "47", cor: colors.textDim },
      { rotulo: "Menos de 6 horas", valor: "93,5%", v: 93.5, cue: "93", cor: colors.danger },
    ]} />
);

// 8. solidão (p72)
export const P08Solidao: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Solidão entre marítimos" titulo="Sozinhos sempre ou com muita frequência" tint={colors.accent}
    max={25} barras={[
      { rotulo: "De folga, em casa", valor: "4,2%", v: 4.2, cue: "4", cor: colors.textDim },
      { rotulo: "No mar", valor: "20,2%", v: 20.2, cue: "20", cor: colors.danger },
    ]} nota={{ texto: "Quase cinco vezes mais.", cue: "cinco" }} />
);

// 9. comprimento (p88)
export const P09Comprimento: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Seawise Giant · 1979" titulo="Comprimento" tint={colors.accent} max={470} barras={[
    { rotulo: "Seawise Giant", valor: `458,45${NB}m`, v: 458.45, cue: "458", cor: colors.danger },
    { rotulo: "Classe TI (78 m a menos)", valor: `380${NB}m`, v: 380, cue: "78", cor: colors.textDim },
    { rotulo: "Torres Petronas (altura)", valor: `451,9${NB}m`, v: 451.9, cue: "petronas", cor: colors.cool },
  ]} />
);

// 10. resumo (p104)
export const P10Resumo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quem move o monstro", titulo: "A vida a bordo", linhas: [
    { rotulo: "Tripulantes", valor: "35 a 40", cue: "35", destaque: true },
    { rotulo: "Petróleo", valor: "quase 3 milhões de barris", cue: "3" },
    { rotulo: "Sono", valor: "blocos de 4 horas", cue: "4" },
    { rotulo: "Motor", valor: "50 mil cavalos", cue: "50" },
  ], tint: "accent" }} />
);
