// Animações de "Brise-glace nucléaire à 1 milliard $" (fr, arquivo dark) — painel 20261012-081400 (baia 1).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com espaço fino (fr), decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. MAPA: la route maritime du Nord (p04)
export const A01Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`ROUTE MARITIME DU NORD · 5${NB}600${NB}KM`} lugares={[
    { nome: "Portes de Kara", lat: 70.4, lon: 58.0, cue: "portes", abaixo: true },
    { nome: "Mer de Kara", lat: 75.5, lon: 72.0, cue: "kara" },
    { nome: "Mer des Laptev", lat: 76.5, lon: 125.0, cue: "lapteuves" },
    { nome: "Sibérie orientale", lat: 73.5, lon: 160.0, cue: "siberie", abaixo: true },
    { nome: "Détroit de Béring", lat: 66.0, lon: 191.0, cue: "siberie", abaixo: true, esquerda: true },
  ]} tint={colors.accent} />
);

// 2. les dimensions de la coque (p12)
export const A02Medidas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Projet 22220 · la coque", titulo: "La taille de l'Arktika", linhas: [
    { rotulo: "Longueur", valor: `173,30${NB}m`, cue: "173" },
    { rotulo: "Soit", valor: "un terrain et demi de football", cue: "football" },
    { rotulo: "Largeur", valor: `34${NB}m`, cue: "34", destaque: true },
  ], tint: "accent" }} />
);

// 3. l'énergie jusqu'aux hélices (p25)
export const A03Energia: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Propulsion nucléaire turbo-électrique", titulo: "Des réacteurs aux hélices", linhas: [
    { rotulo: "3 moteurs électriques", valor: `20${NB}MW chacun`, cue: "20" },
    { rotulo: "Au total", valor: `60${NB}MW`, cue: "60", destaque: true },
    { rotulo: "L'équivalent de", valor: `80${NB}000${NB}chevaux`, cue: "80" },
  ], tint: "accent" }} />
);

// 4. la vitesse dans 2,80 m de glace (p33)
export const A04Vitesse: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Glace plate de 2,80${NB}m · marche continue`, titulo: "Au pas d'un homme", linhas: [
    { rotulo: "Vitesse", valor: `1,5 à 2${NB}nœuds`, cue: "demi" },
    { rotulo: "Soit", valor: `3 à 4${NB}km/h`, cue: "3" },
    { rotulo: "Comme", valor: "un homme qui marche", cue: "homme", destaque: true },
  ], tint: "accent" }} />
);

// 5. le double tirant d'eau (p46)
export const A05Calado: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Double tirant d'eau · deux navires en un", titulo: "Ballasts pleins ou vides", linhas: [
    { rotulo: "Ballasts pleins", valor: `10,50${NB}m`, cue: "remonte" },
    { rotulo: "Ballasts vides", valor: `8,50${NB}m`, cue: "8" },
    { rotulo: "Déplacement allégé", valor: `≈${NB}25${NB}500${NB}t`, cue: "25", destaque: true },
  ], tint: "accent" }} />
);

// 6. MAPA: Saint-Pétersbourg -> pôle Nord -> Mourmansk (p68)
export const A06Polo: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ARKTIKA · VOYAGE DE LIVRAISON · SEPTEMBRE 2020" lugares={[
    { nome: "Saint-Pétersbourg", lat: 59.93, lon: 30.33, cue: "saint", abaixo: true },
    { nome: "Mer de Barents", lat: 72.0, lon: 38.0, cue: "chemin" },
    { nome: "Pôle Nord", lat: 89.5, lon: 40.0, cue: "nord" },
  ]} marca={{ nome: "Mourmansk", lat: 68.97, lon: 33.08, nota: "port d'attache", cue: "mourmansk" }} tint={colors.accent} />
);

// 7. l'équipage (p77)
export const A07Equipage: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Qui vit à bord", titulo: "L'équipage d'un géant", linhas: [
    { rotulo: "Membres d'équipage", valor: "54", cue: "54" },
    { rotulo: "Autres personnes", valor: "21", cue: "20" },
    { rotulo: "Au total", valor: "75", cue: "75", destaque: true },
  ], tint: "accent" }} />
);

// 8. le méthanier Christophe de Margerie (p92)
export const A08Methanier: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Christophe de Margerie · méthanier brise-glace", titulo: "Un navire hors norme", linhas: [
    { rotulo: "Propulsion", valor: `45${NB}MW`, cue: "45" },
    { rotulo: "Glace, seul", valor: `2,10${NB}m`, cue: "10", destaque: true },
    { rotulo: "Conçu pour", valor: `−52${NB}°C`, cue: "52" },
  ], tint: "accent" }} />
);

// 9. la série du projet 22220 (p102)
export const A09Frota: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="leningrad" linhas={[
    "PROJET 22220 · LA SÉRIE",
    "· Arktika · 2020 · Sibir · 2021",
    "· Oural · 2022",
    "· Iakoutie · 2025",
    "· Tchoukotka · 2027",
    "· Leningrad · 2028",
    "· Stalingrad · 2030",
  ]} chave={6} carimbo={{ texto: "SEPT BRISE-GLACE", cue: "sept" }} />
);
