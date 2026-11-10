// Animações de "5 Biggest Port Machines" (en, enxuto) — painel 20261029-133149 (b1).
// REGRA: biblioteca (Painel); motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const COSTA: [number, number][] = [[32.6, -117.2], [33.0, -117.3], [33.4, -117.7], [33.75, -118.4], [34.0, -118.5], [34.4, -119.7],
  [34.5, -120.5], [35.2, -120.8], [35.7, -121.3], [36.6, -121.9], [37.0, -122.2], [37.6, -122.5], [38.0, -123.0], [38.9, -123.7],
  [39.8, -123.85], [40.4, -124.4], [41.7, -124.2], [42.0, -124.3]];

const NB = " ";

// 1. A régua do filme: Triple-E (p02)
export const A01Triple: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Maersk Triple-E class · the yardstick", titulo: "The ship every machine is measured against", linhas: [
    { rotulo: "Length", valor: `400${NB}m`, cue: "400" },
    { rotulo: "Width", valor: `59${NB}m`, cue: "59" },
    { rotulo: "Capacity, twenty-foot boxes", valor: `18,000${NB}TEU`, cue: "18", destaque: true },
  ], tint: "cool" }} />
);

// 2. Handler de contêiner cheio (p05)
export const A02Handler: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Laden container handler · Konecranes", titulo: "A forklift that went to the gym", linhas: [
    { rotulo: "Lifts a full container, up to", valor: `45${NB}tonnes`, cue: "45", destaque: true },
    { rotulo: "Same weight as roughly", valor: `30${NB}family cars`, cue: "30" },
    { rotulo: "Lifting height", valor: `16${NB}m` },
  ], tint: "accent" }} />
);

// 3. Rebocador Venture (p15)
export const A03Tug: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Crowley tug Venture · Los Angeles and Long Beach", titulo: "Small boat, huge pull", linhas: [
    { rotulo: "Length", valor: `82${NB}feet`, cue: "82" },
    { rotulo: "Bollard pull, up to", valor: `95${NB}tonnes`, cue: "95", destaque: true },
  ], tint: "cool" }} />
);

// 4. Long Beach: guindastes empilhadores (p23)
export const A04LongBeach: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Long Beach Container Terminal · Middle Harbor", titulo: "Automated stacking cranes", linhas: [
    { rotulo: "Per the project plan", valor: `70${NB}cranes`, cue: "70" },
    { rotulo: "Per a trade report after opening", valor: `72${NB}cranes`, cue: "72", destaque: true },
  ], tint: "accent" }} />
);

// 5. Oakland: quanto mede o guindaste (p35)
export const A05Oakland: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Port of Oakland · ZPMC cranes", titulo: "How tall is the crane?", linhas: [
    { rotulo: "Boom nearly vertical", valor: `442${NB}feet`, cue: "442", destaque: true },
    { rotulo: "Boom stowed at 45 degrees", valor: `372${NB}feet`, cue: "372" },
    { rotulo: "Earlier reports, boom raised", valor: `440${NB}feet`, cue: "440" },
  ], tint: "cool" }} />
);

// 6. Thialf (p48)
export const A06Thialf: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Thialf · Heerema Marine Contractors", titulo: "Two cranes, one record", linhas: [
    { rotulo: "Combined lifting capacity", valor: `14,200${NB}tonnes`, cue: "14", destaque: true },
    { rotulo: "Heaviest lift on record", valor: `11,883${NB}tonnes`, cue: "11" },
  ], tint: "accent" }} />
);

// 7. Saipem 7000 (p50)
export const A07Saipem: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Saipem 7000 · two revolving cranes", titulo: "Seven thousand tonnes each", linhas: [
    { rotulo: "Each crane", valor: `7,000${NB}tonnes`, cue: "7000" },
    { rotulo: "Combined rating", valor: `14,000${NB}tonnes`, cue: "14", destaque: true },
    { rotulo: "Crane length", valor: `140${NB}m`, cue: "140" },
  ], tint: "cool" }} />
);

// 8. Pioneering Spirit x Triple-E (p58)
export const A08Spirit: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pioneering Spirit · Allseas", titulo: "Almost as long. Twice as wide.", linhas: [
    { rotulo: "Pioneering Spirit, hull length", valor: `382${NB}m`, cue: "382" },
    { rotulo: "Triple-E, length", valor: `400${NB}m`, cue: "400" },
    { rotulo: "Pioneering Spirit, hull width", valor: `124${NB}m`, cue: "124", destaque: true },
  ], tint: "danger" }} />
);

// 10. Os dois portos do recap (p63)
export const A10Costa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CALIFORNIA · TWO PORTS, TWO KINDS OF GIANT" linhas={[{ pontos: COSTA }]} lugares={[
    { nome: "Long Beach", lat: 33.75, lon: -118.2, cue: "beach", abaixo: true },
    { nome: "Oakland", lat: 37.8, lon: -122.3, cue: "oakland" },
  ]} tint={colors.cool} />
);

// 9. A escada (p65)
export const A09Ladder: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The ladder · smallest to largest", titulo: "Each step, a different kind of strength", linhas: [
    { rotulo: "Container handler", valor: `45${NB}t lift`, cue: "45" },
    { rotulo: "Tug", valor: `95${NB}t pull`, cue: "95" },
    { rotulo: "Crane reach over a deck", valor: `225${NB}ft`, cue: "225" },
    { rotulo: "Floating crane", valor: `14,000${NB}t` },
    { rotulo: "Pioneering Spirit", valor: `48,000${NB}t`, cue: "48", destaque: true },
  ], tint: "danger" }} />
);
