// As animações de "Xiaomi a acheté 3 Tesla et les a démontées" (fr, arquivo dark) — painel 20261007-150921 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. 30 mars 2021: 10 milliards de dollars sur 10 ans (p07)
export const X01DixMilliards: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="30 MARS 2021 · XIAOMI VA FABRIQUER DES VOITURES" valor={10} cue="10" sep={NB}
    sufixo={`milliards${NB}de${NB}$`} nota={{ texto: `sur 10${NB}ans · Lei Jun aux commandes`, cue: "ans" }} />
);

// 2. Hyper Die-Casting (p20)
export const X02DieCasting: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Xiaomi Hyper Die-Casting · avec Haitian", titulo: "Une seule pièce d'aluminium", linhas: [
    { rotulo: "Force de fermeture max.", valor: `9${NB}500${NB}tonnes`, cue: "9500" },
    { rotulo: "En travail stable", valor: `9${NB}300${NB}tonnes`, cue: "9300" },
    { rotulo: "Îlot de production", valor: `60${NB}équipements`, cue: "60" },
    { rotulo: "Paramètres de procédé", valor: "433", cue: "433", destaque: true },
  ], tint: "accent" }} />
);

// 3. le chrono du Nürburgring (p38)
export const X03Chrono: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nordschleife · 1er avril 2025", titulo: "Xiaomi SU7 Ultra", linhas: [
    { rotulo: "SU7 Ultra", valor: `7${NB}min${NB}04${NB}s${NB}957`, cue: "957", destaque: true },
    { rotulo: "Rimac Nevera", valor: `0,341${NB}s plus lente`, cue: "340" },
    { rotulo: "Porsche Taycan Turbo GT", valor: `7${NB}min${NB}07${NB}s${NB}55`, cue: "2" },
  ], tint: "accent" }} />
);

// 4. les livraisons (p56)
export const X04Livraisons: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Xiaomi · voitures livrées", titulo: "Le direct de Lei Jun", linhas: [
    { rotulo: "Livrées en 2025", valor: `410${NB}000`, cue: "410" },
    { rotulo: "Objectif 2026", valor: `550${NB}000`, cue: "550" },
    { rotulo: "YU7 en six mois", valor: `plus de 150${NB}000`, cue: "150", destaque: true },
  ], tint: "accent" }} />
);

// 5. MAPA: de Pékin à Munich (p70)
export const X05Munich: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SEPTEMBRE 2025 · LE PREMIER CENTRE HORS DE CHINE" lugares={[
    { nome: "Pékin · Xiaomi", lat: 39.90, lon: 116.40, cue: "xiaomi" },
    { nome: "Munich · recherche et design", lat: 48.14, lon: 11.58, cue: "munich", abaixo: true },
  ]} tint={colors.accent} />
);

// 6. en à peine 5 ans (p80)
export const X06CinqAns: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "30 mars 2021 → printemps 2026", titulo: "En à peine 5 ans", linhas: [
    { rotulo: "De zéro voiture", valor: `à plus de 400${NB}000 par an`, cue: "400" },
    { rotulo: "Un record", valor: "au Nürburgring", cue: "record" },
    { rotulo: "Un centre de recherche", valor: "à Munich", cue: "munich", destaque: true },
  ], tint: "accent" }} />
);
