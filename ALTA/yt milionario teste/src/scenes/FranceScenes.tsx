// Animations du film "La France Ouvre ses Portes à BYD — Des Ingénieurs Ont Démonté la Voiture" (fr, enxuto) — painel
// 20261014-002112 (baia b1). REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. marques chinoises en France, 2025 (p01)
export const F01Marche: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "France · année 2025", titulo: "Les marques chinoises", linhas: [
    { rotulo: "Voitures neuves immatriculées", valor: `57${NB}269`, cue: "57", destaque: true },
    { rotulo: "Part du marché", valor: `3,5${NB}%`, cue: "3" },
  ], tint: "accent" }} />
);

// 2. BYD en France (p03)
export const F02Byd: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="BYD · immatriculations en France" titulo="Six mois contre une année"
    tint={colors.accent} max={14000} barras={[
    { rotulo: "Toute l'année 2025", valor: `13${NB}533`, v: 13533, cue: "533", cor: colors.textDim },
    { rotulo: "1er semestre 2026", valor: `13${NB}935`, v: 13935, cue: "935" },
  ]} />
);

// 3. MAPA: de la France à Livonia, collée à Détroit (p09)
export const F03Livonia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CARESOFT GLOBAL · MICHIGAN" lugares={[
    { nome: "France", lat: 48.86, lon: 2.35, cue: "atlantique" },
    { nome: "Livonia · Caresoft", lat: 42.37, lon: -83.35, cue: "livonia", esquerda: true },
    { nome: "Détroit", lat: 42.33, lon: -83.05, cue: "michigan", abaixo: true },
  ]} tint={colors.accent} />
);

// 4. prix de la Seagull en Chine (p14)
export const F04Prix: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD Seagull · Chine", titulo: "Le prix", linhas: [
    { rotulo: "Lancement · avril 2023", valor: `< 90${NB}000 yuans ≈ 12${NB}000${NB}$`, cue: "90" },
    { rotulo: "Entrée de gamme", valor: `69${NB}800 yuans ≈ 9${NB}700${NB}$`, cue: "69", destaque: true },
  ], tint: "accent" }} />
);

// 5. batterie Blade de la Seagull (p28)
export const F05Batterie: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Batterie Blade · cycle chinois", titulo: "Deux tailles", linhas: [
    { rotulo: `30,08${NB}kWh`, valor: `305${NB}km`, cue: "305" },
    { rotulo: `38,88${NB}kWh`, valor: `405${NB}km`, cue: "405", destaque: true },
    { rotulo: `Recharge 30 → 80${NB}%`, valor: "≈ une demi-heure", cue: "80" },
  ], tint: "accent" }} />
);

// 6. la balance (p36)
export const F06Poids: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "La sixième surprise", titulo: "BYD Seagull sur la balance", linhas: [
    { rotulo: "Poids", valor: `1160–1240${NB}kg`, cue: "1160", destaque: true },
    { rotulo: "Moteur", valor: `55${NB}kW · 74${NB}ch`, cue: "74" },
    { rotulo: `0 à 100${NB}km/h`, valor: `13${NB}s`, cue: "13" },
  ], tint: "accent" }} />
);

// 7. droits européens sur les électriques chinoises (p49)
export const F07Droits: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Union européenne · octobre 2024" titulo="Droits compensateurs"
    tint={colors.danger} max={36} barras={[
    { rotulo: "BYD", valor: `17${NB}%`, v: 17, cue: "17" },
    { rotulo: "Geely", valor: `18,8${NB}%`, v: 18.8, cue: "18", cor: colors.textDim },
    { rotulo: "Autres chinois", valor: `jusqu'à 35,3${NB}%`, v: 35.3, cue: "35", cor: colors.textDim },
  ]} />
);

// 8. MAPA: l'usine BYD de Szeged, Hongrie (p51)
export const F08Szeged: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="BYD · UNE USINE DANS L'UNION" lugares={[
    { nome: "Szeged · BYD", lat: 46.25, lon: 20.15, cue: "zeged|szeged", abaixo: true, esquerda: true },
    { nome: "Paris", lat: 48.86, lon: 2.35, cue: "usine" },
  ]} tint={colors.accent} />
);
