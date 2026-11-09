// Animações de "Every Job Aboard a WWII Liberty Ship" (en, enxuto) — painel 20261028-003238-every-job-aboard-a-wwii-liberty-ship-ran (baia b1).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o navio (p03)
export const L01Navio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The Liberty ship · 1941–1945", titulo: "Built in a hurry", linhas: [
    { rotulo: "Shipyards", valor: "18", cue: "18" },
    { rotulo: "Ships built", valor: `2,700+`, cue: "2" },
    { rotulo: "Jeremiah O'Brien", valor: `56${NB}days`, cue: "56", destaque: true },
  ], tint: "accent" }} />
);

// 2. dois navios, dois finais (p33)
export const L02Duas: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="30" chave={3} linhas={[
    "TWO LIBERTY SHIPS · TWO ENDINGS",
    "",
    `SS Lydia M. Child — sank in about 30${NB}minutes`,
    `All 62${NB}men got off`,
    `SS Sumner I. Kimball — 70${NB}men aboard`,
    "No lifeboat and no raft was ever found",
  ]} carimbo={{ texto: "70 MEN · NO TRACE", cue: "70" }} />
);

// 3. Stephen Hopkins (p49)
export const L03Hopkins: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stephen Hopkins · September 27, 1942", titulo: "One gun against a raider", linhas: [
    { rotulo: "Killed in the action", valor: "42", cue: "forty", destaque: true },
    { rotulo: "Survivors in a lifeboat", valor: "15", cue: "15" },
    { rotulo: "Days adrift to Brazil", valor: "31", cue: "31" },
  ], tint: "danger" }} />
);

// 4. a caldeira (p66)
export const L04Calor: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="THE BOILER ROOM · IN THE TROPICS" valor={130} cue="130" prefixo="over " sufixo="°F"
    nota={{ texto: "men took salt tablets", cue: "salt" }} />
);

const COSTA: [number, number][] = [[48.4, -124.7], [46.2, -124.0], [43.0, -124.4], [40.4, -124.4], [38.9, -123.7], [37.8, -122.5], [36.6, -121.9], [34.5, -120.5], [34.0, -118.5], [32.5, -117.1]];

// 5. MAPA: o O'Brien hoje (p77)
export const L05Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THE LAST SAILING LIBERTY SHIPS" linhas={[{ pontos: COSTA }]} lugares={[
    { nome: "San Francisco", lat: 37.8, lon: -122.4, cue: "san", esquerda: true },
  ]} tint={colors.cool} />
);
