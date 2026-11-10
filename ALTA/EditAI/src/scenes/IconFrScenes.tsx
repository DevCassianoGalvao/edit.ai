// As animações de "La Ville Cachée Que Personne Ne Voit" (fr, arquivo dark) — painel 20261010-234322 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito. Separador fr = espaço (NBSP).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. quantas pessoas (texto p3)
export const F01Population: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ICON OF THE SEAS · À PLEINE CAPACITÉ" valor={9950} cue="9" sep=" " sufixo={`${NB}personnes`}
    barras={[{ rotulo: "passagers", v: 7600, cue: "7" },
      { rotulo: "membres d'équipage", v: 2350, cue: "2", destaque: true }]} />
);

// 2. MAPA: a I-95, da Flórida ao Maine (texto p11)
export const F02Autoroute: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="INTERSTATE 95 · LA CÔTE EST DES ÉTATS-UNIS" lugares={[
    { nome: "Floride", lat: 25.77, lon: -80.19, cue: "floride", abaixo: true },
    { nome: "Maine", lat: 46.13, lon: -67.84, cue: "maine" },
  ]} linhas={[{ pontos: [[25.77, -80.19], [30.33, -81.66], [32.08, -81.09], [35.78, -78.64], [37.54, -77.44],
    [38.9, -77.04], [39.95, -75.17], [40.71, -74.0], [42.36, -71.06], [43.66, -70.26], [46.13, -67.84]], cor: colors.cool }]}
    tint={colors.cool} />
);

// 3. as cabines (texto p16)
export const F03Cabines: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="QUATRE PONTS · RÉSERVÉS À L'ÉQUIPAGE" valor={1175} cue="1175" sep=" " sufixo={`${NB}cabines`}
    nota={{ texto: "jamais plus de deux personnes par cabine", cue: "deux" }} />
);

// 4. as cozinhas (texto p28)
export const F04Coqueries: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Icon of the Seas · en cuisine", titulo: "La machine à nourrir", linhas: [
    { rotulo: "coqueries · galleys", valor: "23" },
    { rotulo: "restaurants", valor: "27", cue: "27" },
    { rotulo: "cuisiniers", valor: "425", cue: "425", destaque: true },
  ], tint: "accent" }} />
);

// 5. a lei do mar (texto p34)
export const F05Repos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Convention du travail maritime · 2006", titulo: "Deux façons de compter", linhas: [
    { rotulo: "repos minimum · 24 heures", valor: `10${NB}heures`, cue: "10" },
    { rotulo: "repos minimum · 7 jours", valor: `77${NB}heures`, cue: "77" },
    { rotulo: "travail maximum · 24 heures", valor: `14${NB}heures`, cue: "14" },
    { rotulo: "travail maximum · 7 jours", valor: `72${NB}heures`, cue: "72", destaque: true },
  ], tint: "cool" }} />
);

// 6. os salários (texto p42)
export const F06Salaires: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Royal Caribbean · estimations de l'équipage", titulo: "Salaire minimum garanti par mois", linhas: [
    { rotulo: "plongeur", valor: `500 à 600${NB}$`, cue: "500" },
    { rotulo: "serveur · steward · barman", valor: `800 à 1${NB}300${NB}$`, cue: "800", destaque: true },
  ], tint: "danger" }} />
);

// 7. os motores (texto p52)
export const F07Moteurs: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SIX MOTEURS WÄRTSILÄ · ENSEMBLE" valor={67500} cue="67" sep=" " sufixo={`${NB}kilowatts`}
    nota={{ texto: "une usine électrique flottante", cue: "67" }} />
);

// 8. Viking Sky (texto p69)
export const F08Viking: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VIKING SKY · HUSTADVIKA · NORVÈGE" valor={475} cue="475" sufixo={`${NB}passagers hélitreuillés`}
    nota={{ texto: "39 minutes pour relancer deux moteurs", cue: "39" }} />
);

// 9. o balanço (texto p82)
export const F09Bilan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Icon of the Seas · la ville cachée", titulo: "Comment vivent les marins", linhas: [
    { rotulo: "marins", valor: `2${NB}350`, destaque: true },
    { rotulo: "cabines d'équipage", valor: `1${NB}175` },
    { rotulo: "pays", valor: "83", cue: "83" },
    { rotulo: "heures par semaine · maximum", valor: "72", cue: "72" },
  ], tint: "accent" }} />
);
