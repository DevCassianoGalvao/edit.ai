// Animações de "Berliner Arbeiterfamilien vermieteten Betten stundenweise" (de, enxuto) — painel 20261029-131224 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// contorno aproximado da Alemanha e da Áustria (lat, lon), só como referência do mapa
const DE: [number, number][] = [[47.6, 7.6], [48.0, 7.6], [49.0, 8.2], [49.4, 6.4], [50.2, 6.1], [51.0, 5.9], [51.9, 6.4], [53.3, 7.2],
  [53.6, 8.0], [54.0, 8.8], [54.9, 8.6], [54.8, 9.8], [54.4, 10.3], [54.1, 11.0], [54.4, 13.0], [54.0, 14.2], [52.7, 14.5], [51.5, 15.0],
  [50.8, 14.8], [50.3, 12.3], [49.0, 13.8], [48.6, 13.5], [47.6, 13.0], [47.6, 10.1], [47.5, 9.6], [47.6, 8.5], [47.6, 7.6]];
const AT: [number, number][] = [[47.5, 9.6], [47.3, 10.5], [47.5, 12.2], [47.6, 13.0], [48.6, 13.8], [48.8, 15.0], [48.7, 16.9], [48.0, 17.1],
  [47.4, 16.4], [46.9, 16.0], [46.6, 14.5], [46.5, 13.7], [46.9, 12.2], [46.8, 10.5], [47.0, 9.6], [47.5, 9.6]];

// 1. Berlin wächst (p02)
export const B01Wachstum: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Einwohner Berlins", titulo: "Eine Stadt wächst um das Vierfache", linhas: [
    { rotulo: "Um 1850", valor: `500${NB}000`, cue: "500" },
    { rotulo: "Vor dem Ersten Weltkrieg", valor: `2${NB}Millionen`, cue: "Millionen" },
    { rotulo: "In gut", valor: `60${NB}Jahren`, cue: "60", destaque: true },
  ], tint: "accent" }} />
);

// 2. Dichte 1905 (p09)
export const B02Dichte: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Einwohner pro Hektar bebauter Fläche · 1905", titulo: "Die dichteste Stadt", linhas: [
    { rotulo: "Berlin", valor: `719${NB}pro Hektar`, cue: "berlin", destaque: true },
    { rotulo: "Schöneberg", valor: `576${NB}pro Hektar`, cue: "Schöneberg" },
    { rotulo: "Charlottenburg", valor: `456${NB}pro Hektar`, cue: "Charlottenburg" },
  ], tint: "accent" }} />
);

// 3. Schlafleute um 1900 (p20)
export const B03Schlafleute: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Berlin samt Vororten · um 1900", titulo: "Haushalte mit Schlafleuten", linhas: [
    { rotulo: "Haushalte", valor: `72${NB}445`, cue: "72" },
    { rotulo: "Schlafgänger insgesamt", valor: `114${NB}158`, cue: "114", destaque: true },
    { rotulo: "davon Männer", valor: `84${NB}235`, cue: "84" },
  ], tint: "cool" }} />
);

// 4. Karls Bett (p28)
export const B04Karl: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Karl · Nachtschicht · Maschinenfabrik", titulo: "Ein Bett in der Kammer", linhas: [
    { rotulo: "Er kommt ans Haus", valor: `5${NB}Uhr`, cue: "5" },
    { rotulo: "Das Bett gehört ihm ab", valor: `6${NB}Uhr`, cue: "6", destaque: true },
    { rotulo: "Bis ungefähr", valor: `16${NB}Uhr`, cue: "4" },
  ], tint: "accent" }} />
);

// 5. Die Rechnung der Familie (p52)
export const B05Rechnung: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="2" chave={3} linhas={[
    "HAUSHALTSRECHNUNG · BERLIN",
    "",
    `2 Schlafgänger · 1 Bett in der Kammer`,
    `je 2${NB}Mark die Woche`,
    `= 4${NB}Mark in der Woche`,
    `= rund 17${NB}Mark im Monat`,
  ]} carimbo={{ texto: "17 MARK", cue: "17" }} />
);

// 6. Die Fotografien (p77)
export const B06Fotos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="WOHNUNGSUNTERSUCHUNGEN · BERLIN · 1902 – 1920" valor={175} cue="175" sep="."
    sufixo={`${NB}Fotografien`}
    nota={{ texto: "aus 112 Wohnungen · Albert Kohn", cue: "112" }} />
);

// 7. Das Ledigenheim (p85)
export const B07Ledigenheim: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="Charlottenburg" chave={2} linhas={[
    "LEDIGENHEIM · DANCKELMANNSTRASSE 46/47",
    "",
    "Eröffnet am 1. April 1908",
    "Stadtbaurat Rudolf Walter",
    `Einzelzimmer von etwa 6${NB}Quadratmetern`,
  ]} carimbo={{ texto: "370 MÄNNER", cue: "370" }} />
);

// 8. MAPA: Wien (p104)
export const B08Wien: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="BETTGEHER UM 1900 · KEIN BERLINER SONDERFALL" lugares={[
    { nome: "Berlin", lat: 52.52, lon: 13.40, cue: "Berliner", esquerda: true },
    { nome: "Wien", lat: 48.21, lon: 16.37, cue: "Wien" },
  ]} linhas={[{ pontos: DE }, { pontos: AT }]} tint={colors.accent} />
);
