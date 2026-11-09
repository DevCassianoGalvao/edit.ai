// Animações de "What Lies Under Loch Ness?" (en, enxuto) — painel 20261031-110425 (b1).
// REGRA: biblioteca (Painel/MapaRota); motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Os números do lago (p02)
export const A01Numbers: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Loch Ness · Scottish Highlands", titulo: "A long, narrow, very deep loch", linhas: [
    { rotulo: "Length, end to end", valor: `37${NB}km`, cue: "37" },
    { rotulo: "Surface area", valor: `56${NB}km²`, cue: "56" },
    { rotulo: "Deepest point", valor: `230${NB}m`, cue: "230", destaque: true },
  ], tint: "cool" }} />
);

// 2. O Great Glen (p05)
export const A02Glen: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SCOTLAND · THE GREAT GLEN FAULT" linhas={[{ pontos: [[57.48, -4.23], [57.35, -4.4], [57.2, -4.62], [57.14, -4.68],
    [57.06, -4.78], [56.98, -4.9], [56.9, -5.0], [56.82, -5.11]] }]} lugares={[
    { nome: "Inverness", lat: 57.48, lon: -4.23, cue: "inverness" },
    { nome: "Fort William", lat: 56.82, lon: -5.11, cue: "william", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. Quanto deslizou (p08)
export const A03Slide: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Great Glen Fault · sideways slip", titulo: "Nobody agrees on the distance", linhas: [
    { rotulo: "A common estimate, a little over", valor: `100${NB}km`, cue: "100" },
    { rotulo: "Banded-rock studies", valor: `160${NB}km`, cue: "160", destaque: true },
    { rotulo: "Other researchers", valor: `200–300${NB}km`, cue: "200" },
  ], tint: "accent" }} />
);

// 4. Operation Deepscan (p30)
export const A04Deepscan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Operation Deepscan · 1987", titulo: "A wall of sonar across the loch", linhas: [
    { rotulo: "Boats, by some accounts", valor: `20`, cue: "20" },
    { rotulo: "Boats, by others", valor: `24`, cue: "24", destaque: true },
  ], tint: "cool" }} />
);

// 5. DNA ambiental (p38)
export const A05Edna: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Environmental DNA · 2018", titulo: "Reading the water", linhas: [
    { rotulo: "Sampling places around the loch", valor: `250+`, cue: "250", destaque: true },
    { rotulo: "Depths sampled at each", valor: `3`, cue: "three" },
  ], tint: "accent" }} />
);

// 6. O que há sob o Loch Ness (p58)
export const A06Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "What lies under Loch Ness", titulo: "Water, trench, sediment, fault", linhas: [
    { rotulo: "Surface area", valor: `56${NB}km²`, cue: "56" },
    { rotulo: "Deepest point", valor: `230${NB}m`, cue: "230", destaque: true },
    { rotulo: "Sediment records", valor: `10,000${NB}years` },
  ], tint: "danger" }} />
);
