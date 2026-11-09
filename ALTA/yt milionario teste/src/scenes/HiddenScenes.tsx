// Animações de "The Hidden World Inside a Mountain" (en, enxuto) — painel 20261105-001911 (b1).
// Cheyenne Mountain Complex (NORAD). REGRA: biblioteca (Painel/MapaRota); motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Blodgett Peak x Cheyenne Mountain (p05)
export const A01Map: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="WHERE TO PUT IT · COLORADO SPRINGS" lugares={[
    { nome: "Blodgett Peak", lat: 38.955, lon: -104.905, cue: "Blodgett", esquerda: true },
    { nome: "Air Force Academy", lat: 39.008, lon: -104.84, cue: "Academy" },
    { nome: "Cheyenne Mountain", lat: 38.744, lon: -104.846, cue: "Cheyenne", abaixo: true },
  ]} linhas={[
    { pontos: [[39.05, -104.84], [38.95, -104.82], [38.84, -104.80], [38.73, -104.75], [38.62, -104.70]], cor: "rgba(255,255,255,0.35)" },
    { pontos: [[39.0, -104.93], [38.9, -104.90], [38.80, -104.89], [38.70, -104.88]], cor: "rgba(140,190,255,0.45)" },
  ]} tint={colors.cool} />
);

// 2. a grade de câmaras (p12)
export const A02Grid: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The grid inside the granite", titulo: "Wide · high · long", linhas: [
    { rotulo: "3 main chambers", valor: `45 · 60 · 588${NB}ft`, cue: "45", destaque: true },
    { rotulo: "4 cross tunnels", valor: `32 · 56 · 335${NB}ft`, cue: "32" },
  ], tint: "cool" }} />
);

// 3. as portas (p21)
export const A03Doors: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The blast doors", titulo: "Steel at the entrance", linhas: [
    { rotulo: "Weight, most cited", valor: `25${NB}tons each`, cue: "25", destaque: true },
    { rotulo: "Thickness", valor: `more than 3${NB}feet`, cue: "three" },
  ], tint: "cool" }} />
);

// 4. as molas (p29)
export const A04Springs: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Steel springs under the buildings", titulo: "A first in shock absorption", linhas: [
    { rotulo: "Original springs", valor: `937`, cue: "937" },
    { rotulo: "Weight of each", valor: `1,500${NB}lb`, cue: "1" },
    { rotulo: "Most cited today", valor: `1,319`, cue: "1319", destaque: true },
  ], tint: "cool" }} />
);

// 5. data e custo (p36)
export const A05Cost: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cheyenne Mountain · operational", titulo: "The date and the bill", linhas: [
    { rotulo: "Full operational capability", valor: `April${NB}20, 1966`, cue: "20th" },
    { rotulo: "Cost in 1960s money", valor: `$142.4${NB}million`, cue: "142", destaque: true },
  ], tint: "accent" }} />
);

// 6. a água dentro da montanha (p43)
export const A06Water: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Water inside the mountain", titulo: "Lakes in the granite", linhas: [
    { rotulo: "Fire reserve", valor: `1.5${NB}million gallons`, cue: "1" },
    { rotulo: "Heat sink", valor: `4.5${NB}million gallons`, cue: "4", destaque: true },
  ], tint: "cool" }} />
);

// 7. a ogiva soviética (p49)
export const A07Megatons: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Soviet intercontinental missile · single warhead", titulo: "Aimed at hardened targets", linhas: [
    { rotulo: "Smallest version", valor: `18${NB}megatons`, cue: "18" },
    { rotulo: "Largest version", valor: `25${NB}megatons`, cue: "25", destaque: true },
  ], tint: "accent" }} />
);

// 8. pessoas lá dentro (p66)
export const A08People: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Inside the mountain today", titulo: "People at work at any given time", linhas: [
    { rotulo: "Between", valor: `350`, cue: "350" },
    { rotulo: "And", valor: `580`, cue: "580", destaque: true },
  ], tint: "cool" }} />
);
