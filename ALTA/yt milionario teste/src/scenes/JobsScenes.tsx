// Animações de "Every Job on a Carrier Flight Deck Ranked From Safest to Deadliest" (en, enxuto) — painel 20261020-000304 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~12 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. os LSOs na beira do convés (p17)
export const J01Lso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Landing Signal Officers · the platform", titulo: "A few dozen yards away", linhas: [
    { rotulo: "The aircraft", valor: `a 30-ton jet`, cue: "30" },
    { rotulo: "Arriving at", valor: `roughly 150${NB}mph`, cue: "150" },
    { rotulo: "When a landing goes wrong", valor: "only seconds to decide", cue: "seconds", destaque: true },
  ], tint: "accent" }} />
);

// 2. o combustível JP-5 (p29)
export const J02Jp5: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The grapes · navy jet fuel", titulo: "JP-5", linhas: [
    { rotulo: "Flash point", valor: "high", cue: "flash" },
    { rotulo: "To ignite", valor: "much harder", cue: "harder" },
    { rotulo: "When it catches", valor: "it still burns hard", cue: "burns", destaque: true },
  ], tint: "accent" }} />
);

// 3. as zonas de perigo em volta do jato (p44)
export const J03Zonas: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Blue shirts · around a running engine" titulo="The no-go zones" tint={colors.danger} itens={[
    { titulo: "The intake", texto: "pulls in anything loose", cue: "intakes" },
    { titulo: "The jet blast", texto: "a wall of heat and force", cue: "wall" },
    { titulo: "The edge", texto: "thrown across the deck, or overboard", cue: "overboard" },
  ]} />
);

// 4. o lançamento da catapulta (p49)
export const J04Catapulta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The catapult · one launch", titulo: "Standing still to flying", linhas: [
    { rotulo: "Launch speed", valor: `roughly 165${NB}mph`, cue: "165" },
    { rotulo: "Time", valor: `about 2${NB}seconds`, cue: "two" },
    { rotulo: "Track", valor: "only a few hundred feet", cue: "feet", destaque: true },
  ], tint: "accent" }} />
);

// 5. o cabo de parada (p57)
export const J05Cabo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Arresting gear · the controlled crash", titulo: "One landing", linhas: [
    { rotulo: "Touchdown at", valor: `roughly 150${NB}mph`, cue: "150" },
    { rotulo: "Steel cables across the deck", valor: "4", cue: "four" },
    { rotulo: "Jet stopped in", valor: `about 2${NB}seconds`, cue: "two", destaque: true },
  ], tint: "accent" }} />
);

// 6. três porta-aviões, três incêndios (p69)
export const J06Incendios: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Three carriers · three fires" titulo="Ordnance was part of the story" tint={colors.danger} itens={[
    { titulo: "1966 · USS Oriskany", texto: "a flare ignited · 44 men killed", cue: "oris" },
    { titulo: "1967 · USS Forrestal", texto: "134 sailors dead", cue: "44" },
    { titulo: "1969 · USS Enterprise", texto: "a rocket exploded · 28 sailors died", cue: "enterprise" },
  ]} />
);

// 7. ninguém trabalha sozinho (p75)
export const J07Corrente: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Nobody on a carrier works alone" tint={colors.accent} itens={[
    { titulo: "Yellow shirt", cue: "yellow", cor: "#f4c430" },
    { titulo: "Blue shirt", cue: "blue", cor: "#3b7be0" },
    { titulo: "Plane captain", cue: "captain", cor: "#a0682f" },
    { titulo: "Pilot", cue: "pilot" },
    { titulo: "Landing signal officer", cue: "landing" },
  ]} />
);

// 8. MAPA: o Forrestal no verão de 1967 (p67)
export const J08Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THE CARRIER FORRESTAL · SUMMER OF 1967" lugares={[
    { nome: "USS Forrestal", lat: 19.6, lon: 107.6, cue: "forrestal" },
  ]} linhas={[
    { pontos: [[22.5, 107.9], [21.5, 107.4], [20.9, 106.7], [20.0, 106.0], [19.0, 105.7], [18.0, 106.4], [17.0, 107.1], [16.0, 108.2]] },
    { pontos: [[20.1, 110.3], [19.6, 109.2], [18.5, 108.7], [18.2, 109.6], [19.2, 111.0], [20.1, 110.3]] },
  ]} tint={colors.danger} />
);
