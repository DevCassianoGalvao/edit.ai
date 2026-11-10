// Animações de "Enfermés des Mois Avec le Plus Gros Moteur du Monde" (fr) — painel 20261021-103507
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com espaço fino (fr).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. as dimensões do navio (p02)
export const E01Dimensions: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="EMMA MÆRSK · LONGUEUR" valor={397} cue="397" sufixo=" mètres" sep=" "
    nota={{ texto: `largeur 56${NB}m · coque 16${NB}m sous l'eau`, cue: "56" }} />
);

// 2. MAPA: a viagem inaugural (p06)
export const E02Voyage: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="VOYAGE INAUGURAL · 2006" lugares={[
    { nome: "Aarhus", lat: 56.16, lon: 10.21, cue: "arus" },
    { nome: "Singapour", lat: 1.26, lon: 103.82, cue: "singapour", esquerda: true },
  ]} tint={colors.accent} />
);

// 3. o nome do motor (p13)
export const E03Moteur: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Moteur principal", titulo: "Wärtsilä-Sulzer 14RT-flex96C", linhas: [
    { rotulo: "Cylindres", valor: "14", cue: "14", destaque: true },
    { rotulo: "Diamètre de chaque cylindre", valor: `96${NB}cm`, cue: "diam" },
    { rotulo: "Course du piston", valor: `2,50${NB}m`, cue: "course" },
  ], tint: "accent" }} />
);

// 4. a potência (p17)
export const E04Puissance: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FICHE DU CONSTRUCTEUR · 14 CYLINDRES" valor={107390} cue="107" sufixo=" chevaux" sep=" "
    nota={{ texto: "plus de 1 000 voitures familiales", cue: "1000" }} />
);

// 5. o barulho (p24)
export const E05Bruit: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Règles britanniques · salle des machines", titulo: "Le bruit", linhas: [
    { rotulo: "Panneau d'avertissement", valor: `85${NB}dB`, cue: "85" },
    { rotulo: "Refuge obligatoire", valor: `90${NB}dB`, cue: "90" },
    { rotulo: "Plafond absolu", valor: `110${NB}dB`, cue: "110", destaque: true },
  ], tint: "accent" }} />
);

// 6. o combustível (p33)
export const E06Fioul: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ce que boit le moteur", titulo: "Fioul lourd", linhas: [
    { rotulo: "Consommation spécifique", valor: `171${NB}g/kWh`, cue: "171" },
    { rotulo: "À pleine puissance", valor: `14${NB}tonnes par heure`, cue: "14", destaque: true },
    { rotulo: "Maximum", valor: `250${NB}tonnes par jour`, cue: "250" },
  ], tint: "accent" }} />
);

// 7. a convenção do trabalho marítimo (p42)
export const E07Repos: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="convention" linhas={[
    "CONVENTION DU TRAVAIL MARITIME",
    `· repos minimum : 10${NB}h sur 24${NB}h`,
    `· repos minimum : 77${NB}h sur 7${NB}jours`,
    `· travail maximum : 14${NB}h sur 24${NB}h`,
    `· travail maximum : 72${NB}h sur 7${NB}jours`,
  ]} chave={1} carimbo={{ texto: "SUR LE PAPIER", cue: "72" }} />
);

// 8. MAPA: o reboque depois da inundação (p53)
export const E08Suez: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FÉVRIER 2013 · REMORQUÉ POUR RÉPARATION" lugares={[
    { nome: "Port-Saïd", lat: 31.26, lon: 32.3, cue: "remorqu", esquerda: true },
    { nome: "Palerme", lat: 38.12, lon: 13.36, cue: "palerme" },
  ]} tint={colors.accent} />
);

// 9. os salários (p63)
export const E09Salaires: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Offres d'emploi · porte-conteneurs", titulo: "Salaire par mois", linhas: [
    { rotulo: "Chef mécanicien", valor: `8${NB}500 – 11${NB}000${NB}$`, cue: "8", destaque: true },
    { rotulo: "Troisième mécanicien", valor: `3${NB}400 – 4${NB}500${NB}$`, cue: "troisi" },
  ], tint: "accent" }} />
);

// 10. MAPA: a rota Europa-Ásia (p71)
export const E10Route: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LA ROUTE VERS L'ASIE" lugares={[
    { nome: "La Manche", lat: 50.2, lon: -1.0, cue: "manche" },
    { nome: "Golfe de Gascogne", lat: 45.5, lon: -4.5, cue: "gascogne", abaixo: true },
    { nome: "Méditerranée", lat: 36.5, lon: 16.0, cue: "mediterr" },
    { nome: "Canal de Suez", lat: 30.6, lon: 32.33, cue: "suez", esquerda: true },
  ]} tint={colors.accent} />
);
