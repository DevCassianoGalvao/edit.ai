// Animações de "Cristóbal Colón — comment vit l'équipage" (fr, enxuto) — painel 20261019-160043-frances-doc-1 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (fr).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Le navire en chiffres (p02)
export const D01Navire: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Cristóbal Colón · 223${NB}m de long`, titulo: "Le navire", linhas: [
    { rotulo: "Largeur", valor: `41${NB}m`, cue: "41" },
    { rotulo: "Port en lourd", valor: `≈${NB}78${NB}000${NB}t`, cue: "78" },
    { rotulo: "Le puits", valor: `46${NB}000${NB}m³`, cue: "46", destaque: true },
  ], tint: "accent" }} />
);

// 2. Vider le puits (p11)
export const D02Vider: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Trois façons de vider le puits", titulo: "Vider", linhas: [
    { rotulo: "Le jet en arc", valor: "rainbowing", cue: "rainbowing" },
    { rotulo: "Pompes de refoulement", valor: `2${NB}×${NB}8${NB}000${NB}kW`, cue: "8000" },
    { rotulo: "Au total", valor: `16${NB}000${NB}kW`, cue: "16000", destaque: true },
  ], tint: "cool" }} />
);

// 3. Stuyvesant x Cristóbal Colón (p22)
export const D03Stuyvesant: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Un petit calcul · ordre de grandeur", titulo: "Deux dragues", linhas: [
    { rotulo: "Stuyvesant · sable", valor: `≈${NB}7${NB}000${NB}t`, cue: "7" },
    { rotulo: "Cristóbal Colón · places", valor: "46", cue: "46" },
    { rotulo: "Cristóbal Colón · port en lourd", valor: `≈${NB}78${NB}000${NB}t`, cue: "78", destaque: true },
  ], tint: "accent" }} />
);

// 4. 84 heures par semaine x MLC 2006 (p32)
export const D04Calcul: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "12 h par jour · 7 jours sur 7", titulo: "La semaine", linhas: [
    { rotulo: "Travail", valor: `84${NB}h`, cue: "84" },
    { rotulo: "Plafond · 1re façon", valor: `72${NB}h`, cue: "72" },
    { rotulo: "Repos exigé · 2e façon", valor: `77${NB}h`, cue: "77", destaque: true },
  ], tint: "danger" }} />
);

// 5. La centrale flottante (p44)
export const D05Puissance: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker={`Puissance installée · 41${NB}650${NB}kW`} titulo="Où va la puissance"
    tint={colors.accent} max={19200} barras={[
    { rotulo: "Propulsion (×2)", valor: `19${NB}200${NB}kW`, v: 19200, cue: "19", cor: colors.danger },
    { rotulo: "Pompes de dragage (×2)", valor: `6${NB}500${NB}kW`, v: 6500, cue: "6" },
    { rotulo: "Pompes de refoulement (×2)", valor: `8${NB}000${NB}kW`, v: 8000, cue: "8" },
  ]} />
);

// 6. Cuxhaven : le nombre de chargements (p51)
export const D06Cuxhaven: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker={`CUXHAVEN · 2${NB}500${NB}000${NB}M³ ÷ 46${NB}000${NB}M³`} valor={54} prefixo="plus de" sep={NB}
    cue="54" nota={{ texto: "chargements à pleine capacité", cue: "chargements" }} />
);

// 7. MAPA: Cuxhaven et Dubaï (p58)
export const D07Carte: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LES CHANTIERS DU CRISTÓBAL COLÓN" lugares={[
    { nome: "Cuxhaven · Allemagne", lat: 53.87, lon: 8.70, cue: "cuxhaven", esquerda: true },
    { nome: "Dubaï · Émirats", lat: 25.20, lon: 55.27, cue: "dubai", esquerda: true },
  ]} tint={colors.accent} />
);

// 8. Les jumelles (p66)
export const D08Jumelles: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jan De Nul · deux navires jumeaux", titulo: "Les jumelles", linhas: [
    { rotulo: "Hébergement · chacune", valor: "46 places", cue: "46" },
    { rotulo: "Cristóbal Colón", valor: "2009", cue: "2009" },
    { rotulo: "Leiv Eiriksson", valor: "2010", cue: "2010", destaque: true },
  ], tint: "cool" }} />
);
