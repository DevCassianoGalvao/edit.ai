// Animações de "Recife, 1950: como as famílias aguentavam o calor" (pt) — painel 20261026-141020-recife-pt
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

// costa do Nordeste (lat, lon) — aproximada: Ceará -> Rio Grande do Norte -> Paraíba -> Pernambuco -> Alagoas -> Bahia
const COSTA_NE: [number, number][] = [[-2.8, -40.5], [-3.0, -39.5], [-3.7, -38.5], [-4.6, -37.3], [-5.0, -36.2],
  [-5.15, -35.45], [-5.8, -35.2], [-6.6, -34.95], [-7.12, -34.82], [-8.05, -34.87], [-8.8, -35.1], [-9.7, -35.72],
  [-10.5, -36.4], [-10.95, -37.05], [-12.0, -37.7], [-12.97, -38.5]];

// 1. MAPA: Recife, perto do Equador, encostada no Atlântico (p01)
export const P01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="RECIFE · POUCOS GRAUS AO SUL DO EQUADOR" lugares={[
    { nome: "Recife", lat: -8.05, lon: -34.88, cue: "recife", esquerda: true },
    { nome: "Linha do Equador", lat: 0, lon: -36.5, cue: "equador" },
  ]} linhas={[{ pontos: COSTA_NE }]} tint={colors.accent} />
);

// 2. a casa que respira (p05)
export const P02Casa: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="4" linhas={[
    "A CASA RECIFENSE CONTRA O CALOR",
    "PÉ-DIREITO DE MAIS DE 4 METROS",
    "O AR QUENTE SOBE",
    "A CAMADA ABAFADA FICA LONGE DA CABEÇA",
    "SEM MÁQUINA NENHUMA",
  ]} chave={1} carimbo={{ texto: "FÍSICA SIMPLES", cue: "física" }} />
);

// 3. o cobogó (p08)
export const P03Cobogo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Uma invenção de Recife", titulo: "O cobogó", linhas: [
    { rotulo: "Nasceu na cidade", valor: "década de 1920", cue: "1920", destaque: true },
    { rotulo: "Criado por", valor: "três engenheiros e arquitetos", cue: "três" },
    { rotulo: "O nome", valor: "as primeiras sílabas dos sobrenomes", cue: "sílabas" },
  ], tint: "accent" }} />
);

// 4. o relógio do sol: a cozinha começa cedo (p13)
export const P04Relogio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A vida no ritmo do sol", titulo: "A cozinha começa cedo", linhas: [
    { rotulo: "Logo cedo", valor: "fogão a lenha ou a carvão aceso", cue: "lenha" },
    { rotulo: "O almoço", valor: "pronto antes do calor apertar", cue: "almoço" },
    { rotulo: "Fogão aceso às 11h", valor: "era castigo", cue: "11", destaque: true },
  ], tint: "accent" }} />
);

// 5. como o barro esfria a água (p24)
export const P05Barro: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="evapora" linhas={[
    "COMO A MORINGA ESFRIA A ÁGUA",
    "O BARRO COZIDO É POROSO",
    "A ÁGUA ATRAVESSA A PAREDE E EVAPORA",
    "EVAPORAR CONSOME O CALOR DE DENTRO",
    "A ÁGUA FICA MAIS FRIA QUE O AMBIENTE",
  ]} chave={3} carimbo={{ texto: "ALGUNS GRAUS A MENOS", cue: "graus" }} />
);

// 6. Josué de Castro e a Geografia da Fome (p40)
export const P06Josue: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="1946" linhas={[
    "GEOGRAFIA DA FOME",
    "JOSUÉ DE CASTRO · MÉDICO RECIFENSE",
    "PUBLICADO EM 1946",
    "A MISÉRIA ALIMENTAR DO NORDESTE",
    "POBREZA, CLIMA E FALTA DE COMIDA",
  ]} chave={2} carimbo={{ texto: "REFERÊNCIA MUNDIAL", cue: "mundial" }} />
);

// 7. a casa depois da máquina (p44)
export const P07Mudanca: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quando o frio vem da máquina", titulo: "A casa muda", linhas: [
    { rotulo: "Janelas", valor: "pequenas, de vidro", cue: "janelas" },
    { rotulo: "Pé-direito", valor: "baixou", cue: "baixou" },
    { rotulo: "Varandas e alpendres", valor: "encolheram ou sumiram", cue: "varandas" },
    { rotulo: "A cadeira na calçada", valor: "trocada pelo sofá", cue: "calçada", destaque: true },
  ], tint: "accent", colunas: false }} />
);
