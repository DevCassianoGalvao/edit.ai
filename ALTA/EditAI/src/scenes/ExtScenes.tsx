// Animações de "37.8 Million Fire Extinguishers Were Recalled" (en, enxuto) — painel 20261103-002501 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. MAPA: Estados Unidos (recall)
export const R01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="UNITED STATES · 37.8 MILLION RECALLED" lugares={[
    { nome: "United States", lat: 39.8, lon: -98.6, cue: "united" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);


// 2. Relatos do recall
export const R02Relatos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "What the company received", titulo: "Reports about the recalled units", linhas: [
    { rotulo: "Reports of units that failed", valor: "391", cue: "391", destaque: true },
    { rotulo: "Injuries", valor: "16", cue: "16" },
    { rotulo: "Cases of property damage", valor: "91", cue: "91" },
  ], tint: "accent" }} />
);

// 3. Onde moram os extintores da casa
export const R03Onde: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Step 1" titulo="Where they hide" tint={colors.accent} itens={[
    { titulo: "Under the kitchen sink", cue: "sink" },
    { titulo: "The garage", cue: "garage" },
    { titulo: "Basement or workshop", cue: "basement" },
    { titulo: "The truck or camper", cue: "truck" },
  ]} />
);

// 4. PASS
export const R04Pass: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Firefighters teach" titulo="Pull, aim, squeeze, sweep" tint={colors.accent} itens={[
    { titulo: "Pull the pin", cue: "pull" },
    { titulo: "Aim low, at the base", cue: "aim" },
    { titulo: "Squeeze the handle", cue: "squeeze" },
    { titulo: "Sweep side to side", cue: "sweep" },
  ]} />
);

// 5. 37,8 milhões
export const R05Milhoes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KIDDE FIRE EXTINGUISHERS RECALLED · UNITED STATES" valor={37} cue="37" sufixo=".8 MILLION"
    nota={{ texto: "Plastic handle or push-button design · made from 1973", cue: "1973" }} />
);
