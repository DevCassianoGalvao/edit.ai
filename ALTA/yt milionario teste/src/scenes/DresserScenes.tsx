// Animações de "This $35 Old Dresser Dries Your Garden Harvest" (en, enxuto) — painel 20261105-002554 (b1).
// REGRA: biblioteca (Painel/Odometro/MapaRota); motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a cômoda usada (p00)
export const A01Price: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="AN OLD DRESSER, USED" valor={35} cue="35" prefixo="$" sufixo={`${NB}dollars`}
    nota={{ texto: "Dries herbs, peppers and beans without a single watt", cue: "35" }} />
);

// 2. o que NÃO pode tocar a comida (p06)
export const A02Metal: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Step three · the screen", titulo: "Keep it away from your food", linhas: [
    { rotulo: "Galvanized metal", valor: `zinc can transfer`, cue: "Galvanized", destaque: true },
    { rotulo: "Copper", valor: `same problem`, cue: "Copper" },
    { rotulo: "Peppers", valor: `acidic`, cue: "Peppers" },
  ], tint: "accent" }} />
);

// 3. o cômodo certo (p12)
export const A03Room: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Step five · where the dresser goes", titulo: "All three", linhas: [
    { rotulo: "Dry", valor: `the air itself`, cue: "dry", destaque: true },
    { rotulo: "Dark", valor: `out of direct sun`, cue: "dark" },
    { rotulo: "Airy", valor: `not stagnant`, cue: "airy" },
  ], tint: "cool" }} />
);

// 4. tempo das ervas firmes (p20)
export const A04Herbs: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sturdy herbs · how long", titulo: "Drying time", linhas: [
    { rotulo: "Thyme, dry room", valor: `a few days`, cue: "few" },
    { rotulo: "Thicker herbs, humid house", valor: `a week or two`, cue: "week" },
    { rotulo: "Reasonable upper mark", valor: `2${NB}weeks`, cue: "Two", destaque: true },
  ], tint: "accent" }} />
);

// 5. extensões universitárias (p28)
export const A05Map: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="EXTENSION SERVICES · JUICY VEGETABLES NEED HEAT" lugares={[
    { nome: "Rutgers", lat: 40.50, lon: -74.45, cue: "Rutgers" },
    { nome: "Montana State", lat: 45.67, lon: -111.05, cue: "Montana" },
    { nome: "University of California", lat: 38.54, lon: -121.75, cue: "California", abaixo: true },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[32.5,-117.1],[32.7,-114.7],[31.3,-108.2],[29.8,-101.4],[26.0,-97.2],[29.4,-94.7],[29.0,-89.4],[30.4,-88.0],[29.1,-83.0],[25.2,-80.4],[30.5,-81.4],[35.2,-75.5],[38.9,-74.9],[40.5,-74.0],[41.6,-70.0],[44.8,-66.9],[47.4,-68.3],[45.0,-74.7],[43.3,-79.0],[42.0,-83.0],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 6. quanto tempo as ervas secas duram (p34)
export const A06Year: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Dried herbs · whole leaves", titulo: "How long they keep", linhas: [
    { rotulo: "Good quality", valor: `about a year`, cue: "year", destaque: true },
    { rotulo: "Day 366", valor: `not bad, just fading`, cue: "366" },
  ], tint: "cool" }} />
);
