// Animações de "SUVs 2026 Novos Já Estão Caindo aos Pedaços" (pt) — painel 20261014-000000 (baia 1).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a pesquisa: mais de 380 mil carros, os 12 piores (p00)
export const A01Donos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CONSUMER REPORTS · PESQUISA COM DONOS" valor={380000} cue="380" sep="."
    sufixo=" carros"
    nota={{ texto: "os 12 piores SUVs modelo 2026", cue: "12" }} />
);

// 2. Traverse: o V6 sai, o 2,5 turbo entra (p11)
export const A02Motor: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Chevrolet Traverse · reformulação 2024", titulo: "O motor trocado", linhas: [
    { rotulo: "Sai: V6 aspirado", valor: `3,6${NB}litros`, cue: "v6" },
    { rotulo: "Entra: 4 cilindros turbo", valor: `2,5${NB}litros`, cue: "4" },
    { rotulo: "Potência no papel", valor: `328${NB}cv`, cue: "328", destaque: true },
  ], tint: "accent" }} />
);

// 3. Honda Prologue: nota 25 de 0 a 100 (p21)
export const A03Nota: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="HONDA PROLOGUE · CONFIABILIDADE PREVISTA" valor={25} cue="25" sep="."
    nota={{ texto: "numa escala de 0 a 100", cue: "100" }} />
);

// 4. Kia EV9 no Brasil (p32)
export const A04Ev9: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Kia EV9 · Brasil, 2025", titulo: `R$${NB}749.990`, linhas: [
    { rotulo: "Dois motores elétricos", valor: `385${NB}cv`, cue: "385" },
    { rotulo: "Autonomia pelo Inmetro", valor: `434${NB}km`, cue: "434", destaque: true },
  ], tint: "accent" }} />
);

// 5. GMC Terrain = irmão do Equinox (p58)
export const A05Terrain: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "GMC Terrain · nº 2 da lista", titulo: "O irmão do Equinox", linhas: [
    { rotulo: "Mesma base do Equinox", valor: "nº 10", cue: "10" },
    { rotulo: "Motor", valor: `1,5${NB}turbo`, cue: "1" },
    { rotulo: "Nota da Consumer Reports", valor: "17", cue: "17", destaque: true },
  ], tint: "accent" }} />
);

// 6. o padrão: as trocas da General Motors (p69)
export const A06Padrao: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="v6" linhas={[
    "AS PEÇAS DO QUEBRA-CABEÇA",
    "",
    "· Acadia + Traverse: V6 → 2,5 turbo",
    "· Terrain + Equinox: 1,5 turbo",
    "· Blazer EV + Prologue: Ultium",
  ]} chave={2} carimbo={{ texto: "GENERAL MOTORS", cue: "1" }} />
);

// 7. MAPA: de onde vêm os SUVs vendidos no Brasil (p88)
export const A07Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DE ONDE VÊM OS SUVs IMPORTADOS" lugares={[
    { nome: "Brasil", lat: -15.8, lon: -47.9, cue: "aqui", abaixo: true },
    { nome: "México", lat: 23.6, lon: -102.5, cue: "méxico", esquerda: true },
    { nome: "Estados Unidos", lat: 39.0, lon: -98.0, cue: "estados", esquerda: true },
    { nome: "Coreia do Sul", lat: 36.5, lon: 127.8, cue: "coreia", esquerda: true },
  ]} tint={colors.accent} />
);
