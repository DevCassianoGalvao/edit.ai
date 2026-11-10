// Animações de "Meyers Hof: Eine Stadt in einem Haus" (de, enxuto) — painel 20261101-110530 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// contorno aproximado da Alemanha (lat, lon), só como referência do mapa
const DE: [number, number][] = [[47.6, 7.6], [48.0, 7.6], [49.0, 8.2], [49.4, 6.4], [50.2, 6.1], [51.0, 5.9], [51.9, 6.4], [53.3, 7.2],
  [53.6, 8.0], [54.0, 8.8], [54.9, 8.6], [54.8, 9.8], [54.4, 10.3], [54.1, 11.0], [54.4, 13.0], [54.0, 14.2], [52.7, 14.5], [51.5, 15.0],
  [50.8, 14.8], [50.3, 12.3], [49.0, 13.8], [48.6, 13.5], [47.6, 13.0], [47.6, 10.1], [47.5, 9.6], [47.6, 8.5], [47.6, 7.6]];

// 1. MAPA: Zuzug nach Berlin (p04)
export const M01Zuzug: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ZUZUG NACH BERLIN · MITTE DES 19. JAHRHUNDERTS" lugares={[
    { nome: "Schlesien", lat: 51.1, lon: 17.0, cue: "Schlesien" },
    { nome: "Pommern", lat: 53.4, lon: 14.5, cue: "Pommern", abaixo: false },
    { nome: "Posen", lat: 52.4, lon: 16.9, cue: "Posen", abaixo: true },
    { nome: "Ostpreußen", lat: 54.7, lon: 20.5, cue: "Ostpreußen", esquerda: true },
  ]} marca={{ nome: "Berlin", lat: 52.52, lon: 13.40, cue: "Arbeit" }} linhas={[{ pontos: DE }]} tint={colors.accent} />
);

// 2. Die Hypothek (p09)
export const M02Hypothek: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="1871" chave={3} linhas={[
    "HYPOTHEK · FABRIKGRUNDSTÜCK",
    "KÖPENICKER STRASSE 18–20",
    "",
    `Eingetragen am 30. Dezember 1871`,
    `Rückzahlung bis 1. Januar 1877`,
  ]} carimbo={{ texto: "BIS 1877", cue: "1877" }} />
);

// 3. Die Wohnungen (p25)
export const M03Wohnungen: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Meyers Hof · Ackerstraße 132", titulo: "Küche, Stube, Kammer", linhas: [
    { rotulo: "Wohnungen insgesamt", valor: `257`, cue: "257" },
    { rotulo: "davon Küche · Stube · Kammer", valor: `229`, cue: "229", destaque: true },
  ], tint: "accent" }} />
);

// 4. Die Toilette (p37)
export const M04Toilette: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Toiletten im Meyers Hof", titulo: "Erst nach zwanzig Jahren", linhas: [
    { rotulo: "Eine Toilette pro Flur ab", valor: `1895`, cue: "1895" },
    { rotulo: "bis", valor: `1897`, cue: "1897" },
    { rotulo: "nach dem Einzug", valor: `20${NB}Jahre`, cue: "20", destaque: true },
  ], tint: "cool" }} />
);

// 5. Die Dampfmaschine (p46)
export const M05Dampf: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Vom Wohnhaus zum Gewerbehof", titulo: "Kraft für Maschinen", linhas: [
    { rotulo: "Jahr", valor: `1903`, cue: "1903" },
    { rotulo: "Eingebaut im", valor: `sechsten Quergebäude`, cue: "sechsten" },
    { rotulo: "Neu im Haus", valor: `Dampfmaschine`, cue: "Dampfmaschine", destaque: true },
  ], tint: "accent" }} />
);

// 6. Der Schwund (p68)
export const M06Schwund: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BEWOHNER DES MEYERS HOF" valor={2100} cue="2100" sep="."
    sufixo={`${NB}Menschen`}
    nota={{ texto: "danach nur noch etwa 900", cue: "900" }} />
);

// 7. Die Mieterstreiks (p76)
export const M07Streik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Roter Wedding", titulo: "Berliner Mieterstreiks", linhas: [
    { rotulo: "In den Jahren", valor: `1932`, cue: "1932", destaque: true },
    { rotulo: "und", valor: `1933`, cue: "1933" },
    { rotulo: "Die Bewohner", valor: `schlossen sich an`, cue: "Bewohner" },
  ], tint: "cool" }} />
);

// 8. Der Niedergang (p84)
export const M08Niedergang: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Meyers Hof · 1970", titulo: "Was vom Haus blieb", linhas: [
    { rotulo: "Mietparteien", valor: `42`, cue: "42", destaque: true },
    { rotulo: "in Wohnungen", valor: `82`, cue: "82" },
    { rotulo: "Einst Wohnungen", valor: `257`, cue: "257" },
    { rotulo: "Einst Menschen", valor: `2${NB}100`, cue: "2100" },
  ], tint: "accent" }} />
);
