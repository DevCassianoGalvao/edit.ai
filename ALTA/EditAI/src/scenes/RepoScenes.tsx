// Animações de "They Repossessed the Car. Why Do You Still Owe Money?" (en, enxuto) — painel 20261103-083422 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. Exemplo: deve 30 mil, leilão 18 mil, buraco de 12 mil
export const R01Exemplo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A simple example", titulo: "Where the gap comes from", linhas: [
    { rotulo: "Owed on the loan", valor: "$30,000", cue: "30" },
    { rotulo: "Sold at dealer auction", valor: "$18,000", cue: "18" },
    { rotulo: "The gap", valor: "$12,000", cue: "12", destaque: true },
  ], tint: "accent" }} />
);

// 2. Venda comercialmente razoável: método, maneira, momento, lugar, termos
export const R02Padrao: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="The legal standard" titulo="Commercially reasonable" tint={colors.accent} itens={[
    { titulo: "The method", cue: "method" },
    { titulo: "The manner", cue: "manner" },
    { titulo: "The timing", cue: "timing" },
    { titulo: "The place", cue: "place" },
    { titulo: "The terms", cue: "terms" },
  ]} />
);

// 3. Pertences: Illinois, 45 dias (mapa)
export const R03Pertences: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ILLINOIS · 45 DAYS TO CLAIM YOUR BELONGINGS" lugares={[
    { nome: "Illinois", lat: 40.0, lon: -89.2, cue: "illinois" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] }
  ]} tint={colors.accent} />
);

// 4. Recapitulação: 30 mil, 18 mil, 1.800 e 13.800
export const R04Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The opening number", titulo: "What you still owe", linhas: [
    { rotulo: "Owed on the loan", valor: "$30,000", cue: "30" },
    { rotulo: "Car sold for", valor: "$18,000", cue: "18" },
    { rotulo: "Costs added", valor: "$1,800", cue: "1" },
    { rotulo: "Deficiency", valor: "$13,800", cue: "13", destaque: true },
  ], tint: "accent" }} />
);
