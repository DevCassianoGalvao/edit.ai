// Animações de "10 cheap Walmart foods that become priceless when you can't cook for three days" (en, enxuto) —
// painel 20261020-174417-10-cheap-walmart-foods-that-become-price (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~12 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista, Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. quanto tempo a geladeira segura (p1)
export const W01Geladeira: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Federal food safety guidance", titulo: "When the power goes out", linhas: [
    { rotulo: "A closed fridge", valor: "about 4 hours", cue: "four" },
    { rotulo: "A full freezer", valor: "about 48 hours", cue: "48" },
    { rotulo: "A half-full freezer", valor: "about 24 hours", cue: "24", destaque: true },
  ], tint: "accent" }} />
);

// 2. a conta do pote de pasta de amendoim (p3)
export const W02Amendoim: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Great Value creamy peanut butter", titulo: "One standard serving", linhas: [
    { rotulo: "Serving", valor: "2 tablespoons", cue: "2" },
    { rotulo: "Calories", valor: "about 190", cue: "190" },
    { rotulo: "Protein", valor: "7 grams", cue: "7" },
    { rotulo: "A 40-ounce jar", valor: "roughly 35 servings", cue: "35", destaque: true },
  ], tint: "accent" }} />
);

// 3. MAPA: luz, fogão e estradas fechadas (p0)
export const W03Nevasca: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THE POWER IS GONE · THE STOVE IS DEAD · THE ROADS ARE CLOSED" lugares={[
    { nome: "Roads closed", lat: 42.5, lon: -89.0, cue: "roads" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 4. sódio do feijão (p23)
export const W04Sodio: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Figures from the Bean Institute" titulo="Sodium removed from canned beans" tint={colors.accent} max={50} barras={[
    { rotulo: "Just draining", valor: "about 36%", v: 36, cue: "36" },
    { rotulo: "Draining and rinsing", valor: "about 41%", v: 41, cue: "41" },
  ]} />
);

// 5. aveia sem fogo (p58)
export const W05Aveia: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Quick oats · no stove" titulo="A cold breakfast" tint={colors.accent} itens={[
    { titulo: "Half a cup of oats", cue: "half" },
    { titulo: "Cover them with liquid", texto: "water, milk or fruit juice", cue: "cover" },
    { titulo: "Let them sit", texto: "20 to 30 minutes", cue: "30" },
    { titulo: "Stir in peanut butter and fruit", cue: "stir" },
  ]} />
);

// 6. água do kit (p64)
export const W06Agua: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Water for the three-day kit", titulo: "At least one gallon per person, per day", linhas: [
    { rotulo: "Per person, per day", valor: "1 gallon", cue: "gallon" },
    { rotulo: "One person, three days", valor: "3 gallons", cue: "three" },
    { rotulo: "A family of four", valor: "12 gallons", cue: "twelve", destaque: true },
  ], tint: "accent" }} />
);

// 7. a ordem de compra (p68)
export const W07Ordem: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Can't buy it all at once?" titulo="Buy in this order" tint={colors.accent} itens={[
    { titulo: "A manual can opener", cue: "first" },
    { titulo: "The peanut butter", cue: "second" },
    { titulo: "Canned chicken and tuna", cue: "third" },
    { titulo: "The water", cue: "fourth" },
  ]} />
);
