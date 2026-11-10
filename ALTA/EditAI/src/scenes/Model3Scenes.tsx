// As animações de "Ce que les ingénieurs ont trouvé dans la Tesla Model 3" (fr, arquivo dark) — painel 20261007-100803.
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
// Separador de milhar em francês = espaço fino sem quebra.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. MAPA: a Tesla no estacionamento do Technocentre (p00)
export const M01Guyancourt: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="AVRIL 2018 · UNE TESLA CHEZ RENAULT" lugares={[
    { nome: "Paris", lat: 48.857, lon: 2.352, cue: "parking" },
    { nome: "Guyancourt · Technocentre Renault", lat: 48.772, lon: 2.074, cue: "guyancourt", abaixo: true },
  ]} tint={colors.accent} />
);

// 2. Caresoft paga até 100 000 $ por uma Model 3 (p07)
export const M02Caresoft: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="WALL STREET JOURNAL · CARESOFT RACHÈTE DES MODEL 3" valor={100000} cue="100" sep={NB}
    prefixo="jusqu'à " sufixo={`${NB}$`}
    nota={{ texto: `Prix de base annoncé : 35${NB}000${NB}$`, cue: "35" }} />
);

// 3. o relatório da Munro (p17)
export const M03Munro: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="rapport" chave={4} linhas={[
    "MUNRO & ASSOCIATES · MICHIGAN",
    "",
    "Rapport de démontage : Tesla Model 3",
    "Jusqu'aux écrous, capteurs et cartes",
    `Rapport complet : 60${NB}000${NB}dollars`,
    `Démontage : environ 6${NB}000${NB}heures`,
  ]} carimbo={{ texto: `6${NB}000 HEURES`, cue: "6" }} />
);

// 4. o veredito da Nikkei (p28)
export const M04Nikkei: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="nikkei" chave={5} linhas={[
    "NIKKEI · DÉMONTAGE · FÉVRIER 2020",
    "",
    "Véhicule : Tesla Model 3",
    "Ordinateur central : Hardware 3",
    "Deux puces d'IA conçues par Tesla",
    `Électronique : environ 6${NB}ans d'avance`,
    "sur Toyota et Volkswagen",
  ]} carimbo={{ texto: `6${NB}ANS D'AVANCE`, cue: "6" }} />
);

// 5. o custo real segundo a WirtschaftsWoche (p37)
export const M05Cout: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "WirtschaftsWoche · mai 2018", titulo: "Le vrai coût d'une Model 3", linhas: [
    { rotulo: "Toutes les pièces", valor: `≈${NB}18${NB}000${NB}$`, cue: "18" },
    { rotulo: "Production", valor: `+${NB}10${NB}000${NB}$`, cue: "10" },
    { rotulo: "Total", valor: `≈${NB}28${NB}000${NB}$`, cue: "28", destaque: true },
    { rotulo: "Prix de vente", valor: `35${NB}000${NB}$`, cue: "35" },
  ], tint: "accent" }} />
);

// 6. o gigacasting (p43)
export const M06Gigacast: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Model Y · le gigacasting", titulo: "L'arrière de la caisse", linhas: [
    { rotulo: "Avant", valor: `70${NB}pièces`, cue: "70" },
    { rotulo: "Après", valor: "une seule pièce moulée", cue: "seule", destaque: true },
    { rotulo: "Robots d'assemblage", valor: "beaucoup moins", cue: "robots" },
  ], tint: "accent" }} />
);

// 7. a guerra de preço na França (p53)
export const M07Prix: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "France · avril 2023", titulo: "Le prix d'entrée", linhas: [
    { rotulo: "Tesla Model 3", valor: `41${NB}990${NB}€`, cue: "41", destaque: true },
    { rotulo: "Renault Mégane électrique", valor: `42${NB}000${NB}€`, cue: "42" },
  ], tint: "danger" }} />
);
