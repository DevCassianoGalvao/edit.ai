// Animações de "10 cheap Dollar Tree items when the furnace dies at night" (en, enxuto) — painel 20261020-135837-ingles-suvival-2 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~12 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. a fornalha calou no meio da noite (p0)
export const D01Noite: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The furnace went silent", titulo: "A cold night ahead", linhas: [
    { rotulo: "When", valor: "the middle of the night", cue: "night" },
    { rotulo: "The furnace", valor: "gone silent", cue: "silent" },
    { rotulo: "The budget", valor: "a few dollars", cue: "few", destaque: true },
  ], tint: "accent" }} />
);

// 2. como o aquecedor de mão esquenta (p6)
export const D02Ferrugem: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Inside a hand warmer" titulo="Heat from rust" tint={colors.accent} itens={[
    { titulo: "Iron powder in the pouch", cue: "iron" },
    { titulo: "Air reaches the iron", cue: "air" },
    { titulo: "Rusting releases heat", cue: "rusting" },
  ]} />
);

// 3. vestir em camadas (p11)
export const D03Camadas: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Think in layers" titulo="Not one giant sweater" tint={colors.accent} itens={[
    { titulo: "Base layer", texto: "snug", cue: "base" },
    { titulo: "Middle layer", texto: "loose", cue: "middle" },
    { titulo: "Outer layer", texto: "heavier", cue: "outer" },
  ]} />
);

// 4. MAPA: tempestade de inverno leva a luz junto (p16)
export const D04Tempestade: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="A DEAD FURNACE DOES NOT ALWAYS COME ALONE · A WINTER STORM" lugares={[
    { nome: "Winter storm", lat: 42.5, lon: -89.0, cue: "storm" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 5. isopor na janela (p24)
export const D05Isopor: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Foam board · an extra wall" titulo="Fit it to the window" tint={colors.accent} itens={[
    { titulo: "Measure the glass", cue: "measure" },
    { titulo: "Cut it slightly larger", cue: "larger" },
    { titulo: "Press it in until it wedges", cue: "wedges" },
    { titulo: "Seal the edges with tape", cue: "seal" },
  ]} />
);

// 6. canos no frio (p32)
export const D06Canos: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Deep freeze · protect the pipes" titulo="Keep the water moving" tint={colors.accent} itens={[
    { titulo: "Wrap exposed pipes in towels", cue: "wrap" },
    { titulo: "Secure them with tape", cue: "secure" },
    { titulo: "Open the cabinet doors", cue: "cabinet" },
  ]} />
);

// 7. o padrão por trás da lista (p41)
export const D07Padrao: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="The pattern behind the list" titulo="Three simple things" tint={colors.accent} itens={[
    { titulo: "Keep your warmth close", cue: "close" },
    { titulo: "Stop the cold air getting in", cue: "getting" },
    { titulo: "Shrink the space to keep warm", cue: "shrink" },
  ]} />
);
