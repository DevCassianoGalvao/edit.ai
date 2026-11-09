// Animações de "What Is Hidden Two Miles Beneath America's Most Secret Military Base?" (en, enxuto) — painel 20261101-112908 (b1).
// REGRA: biblioteca (Painel/MapaRota/Odometro/Documento); motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. A profundidade (p02)
export const A01Depth: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The legend · Nevada", titulo: "Two miles straight down", linhas: [
    { rotulo: "Two miles, in feet", valor: `10,560${NB}ft`, cue: "10", destaque: true },
    { rotulo: "Empire State Building, stacked", valor: `7×`, cue: "seven" },
  ], tint: "cool" }} />
);

// 2. Os lugares candidatos (p08)
export const A02Places: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THE MOST SECRET PLACES IN AMERICA" lugares={[
    { nome: "Cheyenne Mountain", lat: 38.74, lon: -104.84, cue: "cheyenne" },
    { nome: "Raven Rock", lat: 39.73, lon: -77.42, cue: "raven", esquerda: true },
    { nome: "Nevada National Security Site", lat: 36.95, lon: -116.05, cue: "nevada", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. A escolha do lugar (p14)
export const A03Survey: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="12th" linhas={["CENTRAL INTELLIGENCE AGENCY", "", "SITE SURVEY — APRIL 12, 1955", "Groom Lake, Nevada", "Salt flat beside the Atomic Energy",
    "Commission's Nevada Proving Ground", "", "Ideal site for testing the U-2"]} chave={7}
    carimbo={{ texto: "SITE CHOSEN", cue: "ground" }} />
);

// 4. As altitudes (p20)
export const A04Altitude: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "How high they flew", titulo: "Above anything else in the sky", linhas: [
    { rotulo: "Commercial airliners of the era", valor: `20,000${NB}ft`, cue: "20" },
    { rotulo: "The U-2, more than", valor: `60,000${NB}ft`, cue: "60", destaque: true },
  ], tint: "accent" }} />
);

// 5. 58 anos (p32)
export const A05Fiftyeight: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UNTIL THE GOVERNMENT ADMITTED IT" valor={58} cue="58" sufixo=" years"
    nota={{ texto: "Area 51 confirmed in the CIA's own history", cue: "pages" }} />
);

// 6. Os testes subterrâneos (p48)
export const A06Tests: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UNDERGROUND NUCLEAR TESTS · NEVADA · 1963–1992" valor={828} cue="828"
    nota={{ texto: "About 12 explosions every year", cue: "12" }} />
);

// 7. Project Rulison (p63)
export const A07Rulison: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Project Rulison · Colorado", titulo: "The deepest American underground test", linhas: [
    { rotulo: "Detonated", valor: `Sept. 10, 1969`, cue: "10th" },
    { rotulo: "Yield", valor: `40${NB}kilotons`, cue: "40" },
    { rotulo: "Depth", valor: `8,425${NB}ft`, cue: "8", destaque: true },
    { rotulo: "That is", valor: `1.6${NB}miles`, cue: "1" },
  ], tint: "danger" }} />
);

// 8. Cheyenne Mountain x a lenda (p70)
export const A08Cheyenne: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "How deep is the deepest bunker?", titulo: "Cheyenne Mountain", linhas: [
    { rotulo: "Beneath granite", valor: `2,000${NB}ft`, cue: "2" },
    { rotulo: "About", valor: `0.4${NB}miles`, cue: "four" },
    { rotulo: "The depth of the legend", valor: `2${NB}miles`, cue: "legend", destaque: true },
  ], tint: "cool" }} />
);

// 9. WIPP 2014 (p76)
export const A09Wipp: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Waste Isolation Pilot Plant · New Mexico · 2014", titulo: "The plan meets reality", linhas: [
    { rotulo: "February 5", valor: `Salt truck on fire`, cue: "5th" },
    { rotulo: "February 14", valor: `A waste drum bursts`, cue: "14th,", destaque: true },
  ], tint: "danger" }} />
);

// 10. O que há sob a base (p85)
export const A10Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The documented record", titulo: "Two miles beneath the base", linhas: [
    { rotulo: "What the record shows", valor: `Rock`, cue: "rock", destaque: true },
    { rotulo: "Hangar", valor: `None`, cue: "hangar" },
    { rotulo: "Laboratory", valor: `None`, cue: "laboratory" },
    { rotulo: "Hidden city", valor: `None`, cue: "city" },
  ], tint: "accent" }} />
);
