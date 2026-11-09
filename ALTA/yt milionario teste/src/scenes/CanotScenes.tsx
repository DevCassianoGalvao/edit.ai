// Animações de "Ce qu'il y a dans le canot de sauvetage d'un cargo" (fr) — painel 20261012-084050 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com espaço (fr), decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. la taille (p04)
export const C01Taille: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Recueil international LSA · la taille", titulo: "Combien de marins ?", linhas: [
    { rotulo: "Maximum homologué", valor: `150${NB}personnes`, cue: "150", destaque: true },
    { rotulo: "Personne moyenne", valor: `82,5${NB}kg`, cue: "kg" },
    { rotulo: "Avec", valor: "son gilet de sauvetage", cue: "gilet" },
  ], tint: "accent" }} />
);

// 2. le record de chute libre (p12)
export const C02Record: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SCHAT-HARDING FF1200 · HAUTEUR DE CHUTE · 2009" valor={55} cue="55" sufixo={`${NB}m`} sep=" "
    nota={{ texto: "Record mondial à l'époque", cue: "record" }} />
);

// 3. moteur et autonomie (p20)
export const C03Moteur: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Diesel · eau calme · canot plein", titulo: "Les performances minimales", linhas: [
    { rotulo: "Vitesse", valor: `6${NB}nœuds ≈ 11${NB}km/h`, cue: "11" },
    { rotulo: "En remorquant le radeau", valor: `2${NB}nœuds`, cue: "2" },
    { rotulo: "Gazole pour 24 h", valor: `144${NB}milles ≈ 267${NB}km`, cue: "24", destaque: true },
  ], tint: "accent" }} />
);

// 4. la fusée à parachute (p30)
export const C04Fusee: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FUSÉE À PARACHUTE · ALTITUDE MINIMALE" valor={300} cue="300" sufixo={`${NB}m`} sep=" "
    nota={{ texto: `Flamme rouge : 40${NB}s · 30${NB}000${NB}candelas`, cue: "40" }} />
);

// 5. le répondeur radar SART (p40)
export const C05Sart: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Répondeur radar de recherche et de sauvetage", titulo: "Une flèche sur l'écran", linhas: [
    { rotulo: "En veille", valor: `au moins 96${NB}h`, cue: "veille" },
    { rotulo: "Répond aux radars", valor: `9${NB}GHz`, cue: "9" },
    { rotulo: "Sur l'écran du sauveteur", valor: `12${NB}points`, cue: "12", destaque: true },
  ], tint: "accent" }} />
);

// 6. le calcul de l'eau (p49)
export const C06Eau: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="trois" linhas={[
    "LE CALCUL DE L'EAU · CANOT DE SAUVETAGE",
    "· Réserve : 3 litres par personne",
    "· Premier jour : rien",
    "· Ensuite : un demi-litre par jour",
    "",
    "· Les réserves tiennent jusqu'au 7e jour",
  ]} chave={5} carimbo={{ texto: "SEPTIÈME JOUR", cue: "septi" }} />
);

// 7. MAPA: le Benlomond et Poon Lim (p55)
export const C07Benlomond: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`SS BENLOMOND · 23 NOVEMBRE 1942`} lugares={[
    { nome: "Benlomond torpillé", lat: 0.5, lon: -38.75, cue: "lomond", esquerda: true },
    { nome: "Côte du Brésil", lat: -0.8, lon: -47.5, cue: "400", abaixo: true },
  ]} tint={colors.accent} />
);
