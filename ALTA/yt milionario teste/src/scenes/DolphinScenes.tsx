// Animações de "Ninguém Viu o Dolphin Mini Chegando" (pt, enxuto) — painel 20261015-002404 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. ranking de automóveis, agosto de 2026 (p02)
export const D01Ranking: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Fenabrave · automóveis · agosto de 2026" titulo="O 4º lugar"
    tint={colors.accent} max={11000} barras={[
    { rotulo: "1º VW Polo", valor: `10.472`, v: 10472, cue: "polo", cor: colors.textDim },
    { rotulo: "2º VW Tera", valor: `10.338`, v: 10338, cue: "terra", cor: colors.textDim },
    { rotulo: "3º Fiat Argo", valor: `8.811`, v: 8811, cue: "argo", cor: colors.textDim },
    { rotulo: "4º BYD Dolphin Mini", valor: `8.299`, v: 8299, cue: "argo" },
    { rotulo: "5º Chevrolet Onix", valor: `7.635`, v: 7635, cue: "onix", cor: colors.textDim },
    { rotulo: "6º Hyundai Creta", valor: `7.354`, v: 7354, cue: "creta", cor: colors.textDim },
  ]} />
);

// 2. o preço: China x Brasil (p10)
export const D02Preco: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Seagull na China · Dolphin Mini no Brasil", titulo: "O mesmo carro", linhas: [
    { rotulo: "Na China", valor: `68${NB}mil yuans`, cue: "68" },
    { rotulo: "Na época, em reais", valor: `≈ R$${NB}47.900`, cue: "47" },
    { rotulo: "No Brasil · 4 lugares", valor: `R$${NB}115.800`, cue: "115", destaque: true },
  ], tint: "accent" }} />
);

// 3. a BYD em 2026 x 2025 (p16)
export const D03Byd: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD no Brasil", titulo: "Seis vezes mais rápido", linhas: [
    { rotulo: "Janeiro a agosto de 2026", valor: `146.930`, cue: "146", destaque: true },
    { rotulo: "O ano inteiro de 2025", valor: `≈ 112${NB}mil`, cue: "112" },
    { rotulo: "Crescimento da BYD", valor: `+118,69${NB}%`, cue: "118" },
    { rotulo: "Crescimento do mercado", valor: `+19,78${NB}%`, cue: "19" },
  ], tint: "accent" }} />
);

// 4. MAPA: Camaçari x Taubaté, as fábricas que a Ford fechou (p24)
export const D04Camacari: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FORD · JANEIRO DE 2021" lugares={[
    { nome: "Camaçari · Bahia", lat: -12.70, lon: -38.32, cue: "ford" },
    { nome: "Taubaté · São Paulo", lat: -23.03, lon: -45.56, cue: "taubate", abaixo: true },
  ]} tint={colors.accent} />
);

// 5. imposto de importação do elétrico (p35)
export const D05Imposto: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Elétrico importado · alíquota" titulo="O calendário do imposto"
    tint={colors.danger} max={36} barras={[
    { rotulo: "Janeiro de 2024", valor: `10${NB}%`, v: 10, cue: "10", cor: colors.textDim },
    { rotulo: "Julho de 2024", valor: `18${NB}%`, v: 18, cue: "18", cor: colors.textDim },
    { rotulo: "Julho de 2025", valor: `25${NB}%`, v: 25, cue: "25", cor: colors.textDim },
    { rotulo: "Julho de 2026", valor: `35${NB}%`, v: 35, cue: "35" },
  ]} />
);

// 6. varejo de janeiro a agosto de 2026 (p50)
export const D06Varejo: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Varejo · Renavam/Fenabrave · jan–ago 2026" titulo="Quem compra do próprio bolso"
    tint={colors.accent} max={42000} barras={[
    { rotulo: "1º BYD Dolphin Mini", valor: `41.015`, v: 41015, cue: "41" },
    { rotulo: "2º Hyundai Creta", valor: `34.060`, v: 34060, cue: "creta", cor: colors.textDim },
    { rotulo: "3º VW Tera", valor: `30.992`, v: 30992, cue: "terra", cor: colors.textDim },
    { rotulo: "4º Fiat Strada", valor: `30.233`, v: 30233, cue: "strada", cor: colors.textDim },
    { rotulo: "5º BYD Song", valor: `29.589`, v: 29589, cue: "song", cor: colors.textDim },
  ]} />
);
