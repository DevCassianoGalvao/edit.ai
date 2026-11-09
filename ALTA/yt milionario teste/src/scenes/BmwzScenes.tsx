// Animações de "BMW contre Zeekr 001 : des ingénieurs ont comparé les deux moteurs" (fr, enxuto) — painel 20261104-010302 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (fr).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { Documento, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. O relatório MarkLines (p03)
export const Z01Rapport: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="rapport" chave={1} linhas={[
    `MARKLINES — 25${NB}JUIN${NB}2024`,
    "BMW contre Geely : analyse de démontage",
    "et comparaison des coûts de l'essieu électrique",
    "",
    "BMW iX xDrive50 · Zeekr 001",
    "Moteur · transistors · carte de contrôle · réducteur",
    "Tableaux de poids, coûts ligne par ligne",
  ]} carimbo={{ texto: "PAYANT", cue: "payant" }} />
);

// 2. MAPA: os controles chineses de abril de 2025 (p14)
export const Z02Export: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`CONTRÔLES CHINOIS · AVRIL${NB}2025`} lugares={[
    { nome: "Chine", lat: 39.9, lon: 116.4, cue: "divis", esquerda: true },
    { nome: "Japon", lat: 34.7, lon: 137.7, cue: "japon", abaixo: true },
    { nome: "Europe", lat: 48.14, lon: 11.58, cue: "europe" },
  ]} tint={colors.danger} />
);

// 3. MAPA: Zeekr (Hangzhou) e o motor japonês da Nidec (Kyoto) (p25)
export const Z03Nidec: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`ESSIEU DE LA ZEEKR 001 · 200${NB}kW · NIDEC`} lugares={[
    { nome: "Hangzhou · Zeekr", lat: 30.27, lon: 120.15, cue: "zicker", esquerda: true },
    { nome: "Kyoto · Nidec", lat: 35.01, lon: 135.77, cue: "kyoto", esquerda: true, abaixo: true },
  ]} tint={colors.accent} />
);

// 4. Zeekr 001 mise à jour 2024 (p34)
export const Z04Zeekr: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Zeekr 001 · mise à jour 2024`, titulo: "Carbure de silicium", linhas: [
    { rotulo: "Système", valor: `800${NB}volts`, cue: "800" },
    { rotulo: "0 à 100 km/h", valor: `3,3${NB}s`, cue: "3", destaque: true },
    { rotulo: "Version à 4 moteurs", valor: `+${NB}de${NB}1${NB}200${NB}ch`, cue: "1200" },
  ], tint: "accent" }} />
);

// 5. BMW Neue Klasse: ganhos anunciados (p44)
export const Z05Gains: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="BMW · nouvelle génération · chiffres du constructeur" titulo="Ce que BMW annonce"
    tint={colors.accent} max={40} barras={[
    { rotulo: "Pertes d'énergie", valor: `−40${NB}%`, v: 40, cue: "40" },
    { rotulo: "Coût", valor: `−20${NB}%`, v: 20, cue: "20" },
    { rotulo: "Poids", valor: `−10${NB}%`, v: 10, cue: "10", cor: colors.danger },
  ]} />
);

// 6. iX3 Neue Klasse (p59)
export const Z06iX3: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BMW iX3 · Neue Klasse · 2025", titulo: "Deux moteurs sans aimants", linhas: [
    { rotulo: "Puissance totale", valor: `345${NB}kW`, cue: "345" },
    { rotulo: "Couple", valor: `645${NB}Nm`, cue: "645" },
    { rotulo: "Batterie", valor: `108,7${NB}kWh`, cue: "108", destaque: true },
  ], tint: "cool" }} />
);

// 7. União Europeia 2035 (p67)
export const Z07UE: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Union européenne · voitures neuves", titulo: "Le calendrier", linhas: [
    { rotulo: "À partir de", valor: "2035", cue: "2035" },
    { rotulo: "À l'échappement", valor: `0${NB}g de CO₂`, cue: "0", destaque: true },
  ], tint: "danger" }} />
);
