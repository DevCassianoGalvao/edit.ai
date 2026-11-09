// Animações de "Bis 1893 hatte jede deutsche Stadt ihre eigene Uhrzeit" (de, enxuto) — painel 20261029-130025 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// contorno aproximado da Alemanha (lat, lon), só como referência do mapa
const DE: [number, number][] = [[47.6, 7.6], [48.0, 7.6], [49.0, 8.2], [49.4, 6.4], [50.2, 6.1], [51.0, 5.9], [51.9, 6.4], [53.3, 7.2],
  [53.6, 8.0], [54.0, 8.8], [54.9, 8.6], [54.8, 9.8], [54.4, 10.3], [54.1, 11.0], [54.4, 13.0], [54.0, 14.2], [52.7, 14.5], [51.5, 15.0],
  [50.8, 14.8], [50.3, 12.3], [49.0, 13.8], [48.6, 13.5], [47.6, 13.0], [47.6, 10.1], [47.5, 9.6], [47.6, 8.5], [47.6, 7.6]];

// 1. Die Rechnung dahinter (p03)
export const U01Rechnung: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Die Erde dreht sich", titulo: "Die Rechnung dahinter", linhas: [
    { rotulo: "Eine Drehung", valor: `24${NB}Stunden`, cue: "24" },
    { rotulo: "Voller Kreis", valor: `360${NB}Grad`, cue: "360" },
    { rotulo: "Pro Stunde", valor: `15${NB}Grad`, cue: "15" },
    { rotulo: "Pro Grad", valor: `4${NB}Minuten`, cue: "4", destaque: true },
  ], tint: "accent" }} />
);

// 2. München und Stuttgart (p12)
export const U02Minuten: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sonnenzeit · bis zum 15. Längengrad", titulo: "Minuten Unterschied", linhas: [
    { rotulo: "München", valor: `14${NB}Minuten`, cue: "14" },
    { rotulo: "Stuttgart", valor: `23${NB}Minuten`, cue: "23", destaque: true },
  ], tint: "cool" }} />
);

// 3. MAPA: Karlsruhe und Berlin (p50)
export const U03Karte: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="KARLSRUHE UND BERLIN" lugares={[
    { nome: "Karlsruhe", lat: 49.0, lon: 8.4, cue: "karlsruhe", esquerda: true },
    { nome: "Berlin", lat: 52.5, lon: 13.4, cue: "berlin" },
  ]} linhas={[{ pontos: DE }]} tint={colors.accent} />
);

// 4. Moltke im Reichstag (p64)
export const U04Moltke: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="16" chave={2} linhas={[
    "REICHSTAG · BERLIN",
    "",
    `16. März 1891`,
    `Helmuth von Moltke, über 90${NB}Jahre alt`,
    "Fünf Zeiten im Reich gefährden",
    "die Mobilmachung",
  ]} carimbo={{ texto: "FÜNF ZEITEN", cue: "90" }} />
);

// 5. Die Bahnzeit (p72)
export const U05Bahnzeit: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mitteleuropäische Eisenbahnzeit", titulo: "Eine Uhr für alle Bahnen", linhas: [
    { rotulo: "Jahr", valor: "1891", cue: "1891" },
    { rotulo: "Stichtag", valor: `1. Juni`, cue: "1" },
    { rotulo: "Zeit des Längengrades", valor: `15${NB}Grad Ost`, cue: "15", destaque: true },
  ], tint: "cool" }} />
);

// 6. Das Gesetz (p85)
export const U06Gesetz: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="12" chave={3} linhas={[
    "DEUTSCHES REICH · GESETZ",
    "",
    "betreffend die Einführung einer",
    "einheitlichen Zeitbestimmung",
    "Erlassen am 12. März 1893",
  ]} carimbo={{ texto: "1. APRIL 1893", cue: "1893" }} />
);

// 7. Europa folgt (p103)
export const U07Europa: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mitteleuropäische Zeit", titulo: "Wer sie noch einführte", linhas: [
    { rotulo: "Ungarn", valor: "1890", cue: "1890" },
    { rotulo: "Böhmen", valor: "1891", cue: "1891" },
    { rotulo: "Österreich und Italien", valor: "1893", cue: "1893", destaque: true },
  ], tint: "accent" }} />
);
