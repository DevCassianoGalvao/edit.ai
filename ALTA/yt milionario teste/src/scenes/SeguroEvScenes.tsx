// Animações de "Bateu de Leve e o Elétrico Virou Perda Total" (pt, arquivo dark) — painel 20261011-142210 (baia 1).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o orçamento do Fiat 500e (p03)
export const A01Fiat: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FIAT 500e · DOIS AMASSADOS NO ASSOALHO · TROCA DA BATERIA" valor={240000} cue="240" sep="."
    prefixo="R$"
    nota={{ texto: `bateria de pouco mais de 200${NB}km de autonomia`, cue: "200" }} />
);

// 2. a garantia do Kwid E-Tech (p11)
export const A02Garantia: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="8" linhas={[
    "RENAULT KWID E-TECH",
    "GARANTIA DA BATERIA",
    "",
    `· 8${NB}anos ou 120${NB}mil${NB}km`,
    "· cobre: defeito de fábrica",
    "· não cobre: batida",
  ]} chave={5} carimbo={{ texto: "NÃO COBRE BATIDA", cue: "batida" }} />
);

// 3. a conta da indenização integral (p22)
export const A03Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Indenização integral · a conta", titulo: "Elétrico avaliado em R$ 150 mil", linhas: [
    { rotulo: "Valor do carro na apólice", valor: `R$${NB}150.000`, cue: "150" },
    { rotulo: "Limite: 75 % do valor", valor: `R$${NB}112.500`, cue: "112" },
    { rotulo: "Bateria custa mais que isso", valor: "perda total", cue: "perda", destaque: true },
  ], tint: "accent" }} />
);

// 4. MAPA: leilões de salvados (p39)
export const A04Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="REUTERS · LEILÕES DE SALVADOS · MARÇO DE 2023" lugares={[
    { nome: "Estados Unidos", lat: 39.0, lon: -95.0, cue: "estados" },
    { nome: "Europa", lat: 50.0, lon: 8.0, cue: "europa" },
    { nome: "Brasil", lat: -15.8, lon: -47.9, cue: "brasileiros", abaixo: true },
  ]} tint={colors.accent} />
);

// 5. Thatcham, julho de 2023 (p48)
export const A05Thatcham: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Thatcham Research · julho de 2023", titulo: "Sinistro de elétrico x combustão", linhas: [
    { rotulo: "Custo médio do sinistro", valor: `+25,5${NB}%`, cue: "25", destaque: true },
    { rotulo: "Tempo de conserto", valor: `+14${NB}%`, cue: "14" },
  ], tint: "accent" }} />
);

// 6. o que procurar nas condições gerais (p59)
export const A06Apolice: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="70" linhas={[
    "CONDIÇÕES GERAIS",
    "INDENIZAÇÃO INTEGRAL",
    "",
    `· percentual: 70${NB}% ou 75${NB}%`,
    "· tem de estar escrito",
    "· sem resposta: peça por escrito",
  ]} chave={3} carimbo={{ texto: "EXIGÊNCIA DA SUSEP", cue: "susep" }} />
);

// 7. os alertas, em ordem (p67)
export const A07Alertas: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="2022" linhas={[
    "OS ALERTAS",
    "",
    "· 2022 · Munro: reparabilidade zero",
    "· 2023 · Reuters: baterias no ferro-velho",
    "· 2023 · Allianz: os casos vão aumentar",
    `· 2023 · Thatcham: +25,5${NB}% de custo`,
  ]} chave={5} carimbo={{ texto: "O SETOR SABIA", cue: "seguradoras" }} />
);
