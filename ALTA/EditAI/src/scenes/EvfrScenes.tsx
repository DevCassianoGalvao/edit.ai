// As animações de "7 voitures électriques qui tombent en panne en 2026" (fr) — painel 20261027-130313 (baia b1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. VW ID.3 — a limitação a 80 % (p05)
export const E01Charge: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VOLKSWAGEN ID.3 · CHARGE MAXIMALE LIMITÉE" valor={80} cue="80" sufixo="%" sep={NB}
    nota={{ texto: `soit 4/5 de la batterie`, cue: "4" }} />
);

// 2. O exemplo de autonomia (p16)
export const E02Autonomie: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Exemple concret · limite de 80 %", titulo: "Autonomie sur le papier", linhas: [
    { rotulo: "Batterie complète", valor: `400${NB}km`, cue: "400" },
    { rotulo: "Avec la limite à 80 %", valor: `320${NB}km`, cue: "320", destaque: true },
  ], tint: "accent" }} />
);

// 3. Nissan Leaf — o recall do Japão (p33)
export const E03Leaf: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nissan Leaf 2026 · rappel au Japon", titulo: "Défaut de fabrication", linhas: [
    { rotulo: "Rappel annoncé le", valor: `27${NB}mars 2026`, cue: "27", destaque: true },
    { rotulo: "Cause", valor: "plaques d'électrodes des cellules", cue: "plaques" },
  ], tint: "danger" }} />
);

// 4. MAPA: Renault 5 / 4 — 19 véhicules em França (p42)
const FRANCE: [number, number][] = [[51.05, 2.4], [50.7, 3.1], [50.1, 4.2], [49.5, 5.9], [49.0, 8.2], [48.1, 7.6], [47.6, 7.6],
  [47.3, 6.9], [46.3, 6.1], [45.9, 7.0], [44.1, 7.5], [43.7, 7.4], [43.3, 6.6], [43.1, 5.9], [43.3, 3.9], [42.5, 3.1],
  [42.8, 0.7], [43.4, -1.8], [44.7, -1.2], [46.2, -1.2], [47.3, -2.5], [48.0, -4.7], [48.6, -4.5], [48.8, -1.6],
  [49.7, -1.6], [49.4, 0.1], [50.2, 1.6], [51.05, 2.4]];
export const E04France: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`RENAULT 5 ET 4 E-TECH · 65${NB}VÉHICULES, DONT 19 EN FRANCE`} lugares={[
    { nome: `19 véhicules en France`, lat: 47.0, lon: 2.4, cue: "19", abaixo: true },
  ]} linhas={[{ pontos: FRANCE }]} tint={colors.accent} />
);

// 5. Presunção legal de conformidade (p62)
export const E05Presomption: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Garantie légale de conformité · présomption", titulo: "Le défaut est présumé exister dès la livraison", linhas: [
    { rotulo: "Voiture neuve", valor: `24${NB}mois`, cue: "24", destaque: true },
    { rotulo: "Voiture d'occasion", valor: `12${NB}mois`, cue: "12" },
  ], tint: "cool" }} />
);
