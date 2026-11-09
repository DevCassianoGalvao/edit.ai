// Animações de "You Own the Home. Someone Else Controls the Land." (en, enxuto) — painel 20261103-082605 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. MAPA: Maryland e Havaí (gancho)
export const R01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ACROSS THE PACIFIC · HAWAII" lugares={[
    { nome: "Hawaii", lat: 21.3, lon: -157.9, cue: "hawaii" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 2. Baltimore: 521 casas, dívida de 24 dólares, 18 mil para manter a casa
export const R02Baltimore: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Baltimore, 2006", titulo: "A tiny ground rent debt", linhas: [
    { rotulo: "Homes awarded to ground rent owners", valor: "521", cue: "521" },
    { rotulo: "Smallest unpaid debt", valor: "$24", cue: "24", destaque: true },
    { rotulo: "Paid to keep one house", valor: "$18,000", cue: "18" },
  ], tint: "accent" }} />
);

// 3. Oahu: 22 donos, 72,5 % dos títulos
export const R03Oahu: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Oahu, Hawaii", titulo: "Who owned the land", linhas: [
    { rotulo: "Landowners", valor: "22", cue: "22" },
    { rotulo: "Share of fee simple titles", valor: "72.5%", cue: "72", destaque: true },
  ], tint: "accent" }} />
);

// 4. Casas pré-fabricadas: 17 a 22 milhões de americanos
export const R04Moradias: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Manufactured homes", titulo: "Americans living in them", linhas: [
    { rotulo: "Lower estimate", valor: "17 million", cue: "17" },
    { rotulo: "Higher estimate", valor: "22 million", cue: "22", destaque: true },
  ], tint: "accent" }} />
);

// 5. HOAs: 74,2 milhões de pessoas, 28 %, 358 mil associações
export const R05Associacoes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Community associations", titulo: "Life under an HOA", linhas: [
    { rotulo: "Americans living in them", valor: "74.2 million", cue: "74" },
    { rotulo: "Share of the country", valor: "28%", cue: "28", destaque: true },
    { rotulo: "Associations (2021)", valor: "358,000", cue: "358" },
  ], tint: "accent" }} />
);

// 6. As quatro perguntas
export const R06Quatro: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Add to your emergency plan" titulo="Four questions" tint={colors.accent} itens={[
    { titulo: "Who owns the land under my home?", cue: "owns" },
    { titulo: "Who can raise my cost on that land?", cue: "raise" },
    { titulo: "Who can tell me to leave?", cue: "leave" },
    { titulo: "What happens if it is damaged or the contract ends?", cue: "happens" },
  ]} />
);
