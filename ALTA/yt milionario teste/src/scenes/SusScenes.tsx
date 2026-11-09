// Animações de "Antes do SUS (1988)" (pt) — painel 20261031-121514 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";
// contorno aproximado da costa do Brasil, só como referência do mapa
const COSTA: [number, number][] = [[4.5, -51.6], [1.0, -50.0], [-0.5, -48.0], [-1.5, -44.5], [-2.8, -41.0], [-3.7, -38.5], [-5.2, -35.4],
  [-8.0, -34.8], [-10.5, -36.5], [-13.0, -38.5], [-16.5, -39.0], [-20.3, -40.2], [-22.9, -41.9], [-23.0, -43.5], [-25.0, -47.9],
  [-28.0, -48.6], [-32.0, -52.2], [-33.7, -53.4]];

// 1. O Inamps (p02)
export const A01Inamps: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "INAMPS · INSTITUTO NACIONAL DE ASSISTÊNCIA MÉDICA DA PREVIDÊNCIA SOCIAL", titulo: "A grande porta da saúde pública para quem trabalhava", linhas: [
    { rotulo: "Começou a funcionar em", valor: "1974", cue: "1974" },
    { rotulo: "Funcionou até", valor: "1993", cue: "1993", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA: mortalidade infantil em 1980 (p31)
export const A02Mortalidade: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`MORTALIDADE INFANTIL · 1980 · ÓBITOS DE MENORES DE 1${NB}ANO POR MIL NASCIDOS VIVOS`} lugares={[
    { nome: `BRASIL · 69,1`, lat: -15.8, lon: -47.9, cue: "69", esquerda: true },
    { nome: `NORDESTE · 97,1`, lat: -8.0, lon: -39.5, cue: "97" },
  ]} linhas={[{ pontos: COSTA }]} tint={colors.accent} />
);

// 3. O artigo 196 (p42)
export const A03Artigo196: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="196" linhas={[
    "CONSTITUIÇÃO FEDERAL · 5 DE OUTUBRO DE 1988",
    "ARTIGO 196",
    "A SAÚDE É DIREITO DE TODOS E DEVER DO ESTADO",
    "· acesso universal e igualitário",
    "· às ações e serviços de saúde",
  ]} chave={2} carimbo={{ texto: "DIREITO DE TODOS", cue: "todos" }} />
);

// 4. Do favor ao direito (p56)
export const A04Favor: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "ARTIGO 196 · CONSTITUIÇÃO DE 1988", titulo: "A diferença para a família Almeida", linhas: [
    { rotulo: "Antes", valor: "pedir favor", cue: "favor" },
    { rotulo: "Depois", valor: "exigir um direito", cue: "exigir", destaque: true },
  ], tint: "accent" }} />
);
