// Animações de "That Beeping May Not Be the Battery—Your CO Alarm Could Be Expired" (en, enxuto) — painel 20261103-001748 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. Vida útil do alarme
export const R01Vida: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "How long does it last?", titulo: "CO alarm lifespan", linhas: [
    { rotulo: "Typical alarm", valor: "5 to 7 years", cue: "5" },
    { rotulo: "Sealed battery models", valor: "10 years", cue: "10", destaque: true },
  ], tint: "accent" }} />
);

// 2. A conta da data de fabricação
export const R02Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Do the math", titulo: "Date + life of the alarm", linhas: [
    { rotulo: "7-year model, made 8 years ago", valor: "Past its time", cue: "7", destaque: true },
    { rotulo: "10-year model, made 6 years ago", valor: "A few years left", cue: "10" },
  ], tint: "accent" }} />
);

// 3. Qual som você ouve
export const R03Escute: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Step 1" titulo="Listen and count" tint={colors.accent} itens={[
    { titulo: "One chirp a minute", cue: "chirp" },
    { titulo: "A quick beep every 30 seconds", cue: "30" },
    { titulo: "A pattern of several beeps", cue: "pattern" },
    { titulo: "A red light flashing", cue: "red" },
  ]} />
);

// 4. Distância dos aparelhos a gás
export const R04Distancia: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "EPA placement tip", titulo: "Away from fuel-burning appliances", linhas: [
    { rotulo: "Minimum distance", valor: "15 feet", cue: "15", destaque: true },
    { rotulo: "Gas furnace and water heater", valor: "Keep away", cue: "furnaces" },
    { rotulo: "Gas stove and fireplace", valor: "Keep away", cue: "stoves" },
  ], tint: "accent" }} />
);

// 5. Alarme de verdade na madrugada
export const R05Emergencia: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="The real alarm" titulo="Do this" tint={colors.accent} itens={[
    { titulo: "Everyone and every pet into fresh air", cue: "fresh" },
    { titulo: "Call 911 from outside", cue: "911" },
    { titulo: "Wait for the firefighters", cue: "firefighters" },
  ]} />
);

// 6. MAPA: os EUA (onde vale a regra do selo de laboratório independente)
export const R06EUA: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="UNITED STATES · LISTED BY AN INDEPENDENT TESTING LAB" lugares={[
    { nome: "United States", lat: 39.8, lon: -98.6, cue: "united" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);
