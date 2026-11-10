// Animações de "Xiaomi vient de dévoiler un moteur à 28 000 tr/min" (fr, enxuto) — painel 20261021-105508 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (fr).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
const FRANCE: [number, number][] = [[51.05, 2.55], [50.1, 1.5], [49.7, 0.2], [49.4, -1.2], [48.6, -1.6], [48.8, -3.0],
  [48.4, -4.8], [47.7, -3.4], [47.2, -2.2], [46.2, -1.2], [45.5, -1.2], [44.6, -1.25], [43.4, -1.8], [43.0, -0.5],
  [42.7, 1.4], [42.4, 3.1], [43.3, 3.5], [43.5, 4.8], [43.1, 6.0], [43.7, 7.5], [44.3, 6.9], [45.1, 6.6], [45.9, 7.0],
  [46.4, 6.1], [47.5, 7.5], [48.6, 7.8], [49.0, 8.2], [49.5, 6.4], [49.5, 5.8], [50.1, 4.8], [50.7, 3.1], [51.05, 2.55]];

// 1. V8s: 27 200 tr/min (p06)
export const F01V8s: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="XIAOMI HYPERENGINE V8S · TOURS PAR MINUTE" valor={27200} sep=" " cue="27"
    nota={{ texto: `425${NB}kW · 578${NB}ch · 635${NB}Nm`, cue: "635" }} />
);

// 2. Nürburgring: SU7 Ultra x Taycan Turbo GT x Rimac Nevera (p11)
export const F02Ring: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nürburgring Nordschleife · électriques de série", titulo: "Le record du tour", linhas: [
    { rotulo: "Xiaomi SU7 Ultra", valor: "7:04,957", cue: "7", destaque: true },
    { rotulo: "Porsche Taycan Turbo GT", valor: "7:07,55", cue: "55" },
    { rotulo: "Rimac Nevera", valor: "7:05,29", cue: "29" },
  ], tint: "danger" }} />
);

// 3. Force centrifuge: de 20 000 à 28 000 tr/min (p19)
export const F03Centrifuge: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Force centrifuge · elle grandit avec le carré de la vitesse" titulo="Tours par minute"
    tint={colors.accent} max={28000} barras={[
    { rotulo: "Tesla Plaid (environ)", valor: `20${NB}000`, v: 20000, cue: "20" },
    { rotulo: "Xiaomi V8S Evo", valor: `28${NB}000`, v: 28000, cue: "28", cor: colors.danger },
  ]} />
);

// 4. V8s Evo: 28 000 tr/min, 611 ch (p27)
export const F04Evo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="XIAOMI V8S EVO · TOURS PAR MINUTE" valor={28000} sep=" " cue="28"
    nota={{ texto: `+800${NB}tr/min · 611${NB}ch à lui seul`, cue: "611" }} />
);

// 5. YU7 GT: 1003 ch, 738 kW (p36)
export const F05YU7GT: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="XIAOMI YU7 GT · V8S EVO + V6S PLUS" valor={1003} sufixo={`${NB}ch`} sep=" " cue="003"
    nota={{ texto: `soit 738${NB}kW`, cue: "738" }} />
);

// 6. MAPA: Trémery, en Moselle (p42)
export const F06Tremery: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="STELLANTIS · EMOTORS" lugares={[
    { nome: "Trémery · moteurs électriques", lat: 49.25, lon: 6.22, cue: "moselle", esquerda: true, abaixo: true },
  ]} linhas={[{ pontos: FRANCE }]} tint={colors.accent} />
);

// 7. Objectif 2026: 550 000 voitures (p54)
export const F07Livraisons: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="XIAOMI AUTO · OBJECTIF DE LIVRAISONS 2026" valor={550000} sufixo={`${NB}voitures`} sep=" "
    cue="550" nota={{ texto: `au 1er mai : environ 20${NB}% atteints`, cue: "20" }} />
);
