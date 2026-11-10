// Animações de "Your Surge Protector Still Works—But Its Protection May Be Gone" (en, enxuto) — painel 20261103-001304 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. MAPA: a tomada de 120 volts dos EUA (a porta fechada do MOV)
export const R01Volts: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="UNITED STATES · 120 VOLTS AT A STANDARD OUTLET" lugares={[
    { nome: "United States · 120 volts", lat: 39.8, lon: -98.6, cue: "united" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 2. A regra de 3 a 5 anos
export const R02Anos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "How long does it last?", titulo: "The rule of thumb", linhas: [
    { rotulo: "Start paying attention", valor: "3 years", cue: "three" },
    { rotulo: "Have a replacement ready", valor: "5 years", cue: "five", destaque: true },
    { rotulo: "Age of the strip", valor: "unknown = old", cue: "unknown" },
  ], tint: "accent" }} />
);

// 3. Outros sinais de alerta
export const R03Sinais: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="More warning signs" titulo="Stop using it if you notice" tint={colors.accent} itens={[
    { titulo: "A buzzing or crackling sound", cue: "buzzing" },
    { titulo: "A loose or sticky switch", cue: "switch" },
    { titulo: "Devices that flicker or reset", cue: "flicker" },
  ]} />
);

// 4. O que nunca fazer
export const R04Nunca: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Fire risk" titulo="Never do this" tint={colors.accent} itens={[
    { titulo: "Plug one strip into another", cue: "another" },
    { titulo: "Chain extension cords together", cue: "chain" },
    { titulo: "Run a space heater through a strip", cue: "heater" },
  ]} />
);

// 5. Protetor de quadro: três motivos
export const R05Quadro: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="At the panel" titulo="Why people choose it" tint={colors.accent} itens={[
    { titulo: "Coverage: the whole house", cue: "coverage" },
    { titulo: "Longevity: up to about 10 years", cue: "longevity" },
  ]} />
);
