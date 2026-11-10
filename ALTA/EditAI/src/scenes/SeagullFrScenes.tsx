// Les animations de "Des ingénieurs américains ont démonté la BYD à 10 000 €" (fr, arquivo dark) — painel
// 20261010-014631 (baia 1). REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. CARTE : Caresoft à Livonia, collée à Detroit (p02)
export const F01Livonia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CARESOFT GLOBAL · AUTOPSIE INDUSTRIELLE" lugares={[
    { nome: "Livonia · Caresoft Global", lat: 42.37, lon: -83.35, cue: "livonia" },
    { nome: "Detroit · cœur de l'automobile américaine", lat: 42.33, lon: -83.05, cue: "detroit", abaixo: true },
  ]} tint={colors.accent} />
);

// 2. Euro NCAP (p09)
export const F02Ncap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Euro NCAP · septembre 2025", titulo: "5 étoiles sur 5", linhas: [
    { rotulo: "Note", valor: `5${NB}étoiles`, cue: "5" },
    { rotulo: "Protection des adultes", valor: `82${NB}%`, cue: "82" },
    { rotulo: "Protection des enfants", valor: `86${NB}%`, cue: "86" },
    { rotulo: "Usagers vulnérables", valor: `76${NB}%`, cue: "76", destaque: true },
  ], tint: "accent" }} />
);

// 3. la balance (p20)
export const F03Poids: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "La balance de Caresoft", titulo: "Seagull contre Chevrolet Bolt", linhas: [
    { rotulo: "BYD Seagull", valor: `environ 1${NB}240${NB}kg`, cue: "1240" },
    { rotulo: "De moins que la Bolt", valor: `environ 400${NB}kg`, cue: "400", destaque: true },
    { rotulo: "Soit le poids de", valor: `5${NB}adultes`, cue: "5" },
  ], tint: "accent" }} />
);

// 4. la baisse en Chine (p29)
export const F04Yuan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Chine · fin mai 2025", titulo: "La Seagull encore moins chère", linhas: [
    { rotulo: "Avant", valor: `69${NB}800${NB}yuans`, cue: "69" },
    { rotulo: "Après", valor: `55${NB}800${NB}yuans`, cue: "55", destaque: true },
    { rotulo: "Baisse", valor: `environ 20${NB}%`, cue: "20" },
    { rotulo: "En euros", valor: `autour de 7${NB}000${NB}€`, cue: "7" },
  ], tint: "accent" }} />
);

// 5. la TVA (p37)
export const F05Tva: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quatrième étage · TVA 20 %", titulo: "Ce qui part à l'État", linhas: [
    { rotulo: "Prix affiché", valor: `18${NB}990${NB}€`, cue: "18" },
    { rotulo: "TVA", valor: `environ 3${NB}165${NB}€`, cue: "3", destaque: true },
    { rotulo: "Prix hors taxes", valor: `environ 15${NB}825${NB}€`, cue: "15" },
  ], tint: "danger" }} />
);

// 6. Renault 5 contre Dolphin Surf (p44)
export const F06Renault: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Prix catalogue · avant bonus", titulo: "Renault 5 contre Dolphin Surf", linhas: [
    { rotulo: "Renault 5 · finition Five", valor: `24${NB}990${NB}€` },
    { rotulo: "Bonus", valor: `3${NB}100 à 4${NB}200${NB}€`, cue: "3" },
    { rotulo: "Dolphin Surf", valor: `18${NB}990${NB}€`, cue: "18" },
    { rotulo: "Écart catalogue", valor: `plus de 6${NB}000${NB}€`, cue: "6", destaque: true },
  ], tint: "accent" }} />
);

// 7. 2035 revu (p50)
export const F07Ue2035: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Commission européenne · 16 décembre 2025" titulo="Émissions des voitures neuves en 2035"
    tint={colors.danger} max={100} barras={[
    { rotulo: "Règle de 2023", valor: `−100${NB}%`, v: 100, cue: "100", cor: colors.textDim },
    { rotulo: "Proposition", valor: `−90${NB}%`, v: 90, cue: "90" },
  ]} />
);
