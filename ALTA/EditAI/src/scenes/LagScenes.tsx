// Animações de "Como Vivem os Pescadores de Lagosta do Ceará que Mergulham com Compressor" (pt) — painel 20261106-111356 (b1, enxuto).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// Litoral do Ceará e do Rio Grande do Norte (lat, lon) aproximado
const COSTA: [number, number][] = [[-2.88, -40.12], [-3.05, -39.6], [-3.42, -39.0], [-3.73, -38.52], [-4.2, -38.05],
  [-4.56, -37.75], [-4.71, -37.36], [-4.93, -37.05], [-5.08, -36.5], [-5.12, -35.95], [-5.12, -35.6], [-5.27, -35.38],
  [-5.55, -35.25], [-5.79, -35.2], [-6.25, -35.05]];
// divisa CE/RN (aprox.)
const DIVISA: [number, number][] = [[-4.83, -37.25], [-5.2, -37.6], [-5.6, -38.0]];

export const L01Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LITORAL LESTE DO CEARÁ" lugares={[
    { nome: "Redonda · Icapuí", lat: -4.65, lon: -37.42, cue: "redonda", abaixo: true },
    { nome: "Fortaleza", lat: -3.73, lon: -38.52, cue: "fortaleza", esquerda: true },
  ]} linhas={[{ pontos: COSTA }, { pontos: DIVISA }]} tint={colors.accent} />
);

export const L04Ovos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Panulirus argus", titulo: "A lagosta-vermelha", linhas: [
    { rotulo: "Ovos de uma adulta", valor: `300${NB}mil`, cue: "300" },
    { rotulo: "Fêmea grande", valor: `150${NB}mm de carapaça`, cue: "150" },
    { rotulo: "Ovos da fêmea grande", valor: `perto de 2${NB}milhões`, cue: "milhões", destaque: true },
  ], tint: "accent" }} />
);

export const L05Queda: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Sindicato dos Pescadores de Icapuí" titulo="Toneladas de lagosta por ano" tint={colors.accent} max={11500} barras={[
    { rotulo: "Antes", valor: "11.500 t", v: 11500, cue: "11" },
    { rotulo: "Hoje", valor: "4.500 t", v: 4500, cue: "4" },
  ]} />
);

export const L06Portaria: React.FC<SceneProps> = (p) => (
  <Documento {...p} linhas={[
    "PORTARIA Nº 43 · 1995",
    "",
    "Fica proibido o mergulho",
    "na pesca da lagosta",
    "no Brasil.",
    "",
    "Motivo: mortes e lesões",
    "de mergulhadores.",
  ]} cue="1995" chave={2} carimbo={{ texto: "PROIBIDO", cue: "43" }} />
);

export const L14Marambaias: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="IBAMA · LITORAL DO CEARÁ · 2009" valor={100} cue="100" prefixo="até " sufixo=" mil" sep="."
    nota={{ texto: "marambaias no fundo do mar — a maioria em Icapuí", cue: "icapuí" }} />
);

export const L07Prof: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Hospital Naval · 1 braça = 2,22 m" titulo="Até onde eles descem" tint={colors.accent} max={135} barras={[
    { rotulo: "Mergulho recreativo", valor: "40 m", v: 40, cue: "40" },
    { rotulo: "21 a 30 braças", valor: "46 a 66 m", v: 66, cue: "esses" },
    { rotulo: "61 a 70 braças", valor: "+ de 130 m", v: 133, cue: "130", cor: colors.danger },
  ]} />
);

export const L15Regras: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mergulho seguro", titulo: "As regras da subida", linhas: [
    { rotulo: "Subida máxima", valor: `10${NB}m por minuto`, cue: "10", destaque: true },
    { rotulo: "Paradas", valor: "durante a subida", cue: "paradas" },
    { rotulo: "Mergulhos", valor: "no máximo 1 por dia", cue: "dia" },
    { rotulo: "Tabelas", valor: "tempo por profundidade", cue: "tabelas" },
  ], tint: "accent" }} />
);

export const L09Casos: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="UFRN · Hospital Naval · 2009 a 2013" titulo="O que aconteceu com os 28 pescadores" tint={colors.danger} max={28} barras={[
    { rotulo: "Dor e formigamento", valor: "19", v: 19, cue: "16" },
    { rotulo: "Lesão na medula", valor: "16", v: 16, cue: "16" },
    { rotulo: "Convulsão ou infarto", valor: "3", v: 3, cue: "3" },
    { rotulo: "Morreram", valor: "7", v: 7, cue: "7", cor: colors.danger },
  ]} />
);

export const L10Natal: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="A ÚNICA CÂMARA MILITAR DO 3º DISTRITO NAVAL" lugares={[
    { nome: "Natal", lat: -5.79, lon: -35.21, cue: "natal", esquerda: true },
    { nome: "Rio do Fogo", lat: -5.27, lon: -35.38, cue: "fogo", esquerda: true },
  ]} linhas={[{ pontos: COSTA }, { pontos: DIVISA }]} tint={colors.accent} />
);

export const L13Preco: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Quilo da lagosta inteira em Icapuí" titulo="O preço pago ao pescador" tint={colors.danger} max={120} barras={[
    { rotulo: "2021", valor: "R$ 120", v: 120, cue: "120" },
    { rotulo: "2023", valor: "R$ 60", v: 60, cue: "60" },
  ]} nota={{ texto: "Metade do preço em dois anos", cue: "metade" }} />
);

