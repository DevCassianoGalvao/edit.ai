// Animações de "Inside the Greenbrier: The Secret Bunker..." (en, enxuto) — painel 20261102-102253 (b1).
// REGRA: biblioteca (Painel/Odometro/MapaRota); motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o segredo durou trinta anos (p00)
export const A01Thirty: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="NOBODY KNEW IT WAS THERE FOR" valor={30} cue="30" sufixo={`${NB}years`}
    nota={{ texto: "A hidden city under a luxury resort", cue: "30" }} />
);

// 2. Washington -> White Sulphur Springs (p07)
export const A02Map: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="WASHINGTON TO THE ALLEGHENY MOUNTAINS" lugares={[
    { nome: "Washington, D.C.", lat: 38.89, lon: -77.01, cue: "Greenbrier", esquerda: true },
    { nome: "The Greenbrier · White Sulphur Springs", lat: 37.79, lon: -80.30, cue: "Springs", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. o tamanho do bunker (p16)
export const A03Area: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="THE BUNKER · SQUARE FEET ON TWO LEVELS" valor={112000} cue="112" sufixo={`${NB}sq ft`}
    nota={{ texto: "About the size of a large shopping center", cue: "112" }} />
);

// 4. a porta de explosão (p30)
export const A04Blast: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The entrance · blast door", titulo: "Steel and concrete", linhas: [
    { rotulo: "Weight", valor: `25${NB}tons`, cue: "25", destaque: true },
    { rotulo: "Built to survive a blast", valor: `15${NB}miles away`, cue: "15" },
  ], tint: "cool" }} />
);

// 5. quem dormiria no bunker (p36)
export const A05Who: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Who the bunker was built for", titulo: "Congress and staff", linhas: [
    { rotulo: "Senators", valor: `100`, cue: "100" },
    { rotulo: "Representatives", valor: `435`, cue: "435", destaque: true },
    { rotulo: "Staff", valor: `about 500`, cue: "500" },
  ], tint: "accent" }} />
);
