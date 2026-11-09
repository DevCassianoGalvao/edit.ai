// Animações de "Inside America's Secret Bunker Built to Survive a Nuclear War" (en, enxuto) — painel 20261105-001055 (b1).
// Cheyenne Mountain Complex (NORAD). REGRA: biblioteca (Painel/Odometro/MapaRota); motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. as três linhas de radar (p02)
export const A01Radar: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THREE RADAR LINES ACROSS CANADA" lugares={[
    { nome: "Pinetree Line", lat: 49.6, lon: -95, cue: "Pine", abaixo: true },
    { nome: "Mid-Canada Line", lat: 55.0, lon: -95, cue: "Mid" },
    { nome: "Distant Early Warning Line", lat: 68.8, lon: -100, cue: "Distant" },
  ]} linhas={[
    { pontos: [[49.0, -123], [49.0, -95], [45.0, -83], [45.0, -71], [47.0, -67.8]], cor: "rgba(255,255,255,0.35)" },
    { pontos: [[49.3, -124], [49.6, -110], [49.8, -95], [48.5, -80], [47.5, -66], [47.5, -53]] },
    { pontos: [[55.0, -128], [55.2, -110], [55.0, -95], [54.5, -80], [54.5, -65]] },
    { pontos: [[70.3, -148], [69.5, -133], [69.0, -115], [68.8, -100], [68.5, -85], [66.5, -67], [65.6, -37.6]] },
    { pontos: [[58.7, -94.2], [56.0, -88], [53.0, -82], [51.3, -79.5], [55.0, -77.5], [58.5, -78], [62.4, -77.5], [61.0, -71.5], [58.6, -69.5], [59.8, -64.5]], cor: "rgba(140,190,255,0.45)" },
  ]} tint={colors.cool} />
);

// 2. Colorado Springs, Blodgett Peak, Cheyenne Mountain (p09)
export const A02Map: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="WHERE TO PUT IT · COLORADO SPRINGS" lugares={[
    { nome: "Colorado Springs", lat: 38.835, lon: -104.79, cue: "Colorado" },
    { nome: "Blodgett Peak", lat: 38.955, lon: -104.905, cue: "Blodgett" },
    { nome: "Cheyenne Mountain", lat: 38.744, lon: -104.846, cue: "Cheyenne", abaixo: true },
  ]} linhas={[
    { pontos: [[39.05, -104.84], [38.95, -104.82], [38.84, -104.80], [38.73, -104.75], [38.62, -104.70]], cor: "rgba(255,255,255,0.35)" },
    { pontos: [[39.0, -104.93], [38.9, -104.90], [38.80, -104.89], [38.70, -104.88]], cor: "rgba(140,190,255,0.45)" },
  ]} tint={colors.cool} />
);

// 3. granito retirado (p14)
export const A03Granite: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="GRANITE PULLED OUT OF THE MOUNTAIN" valor={700000} cue="700" sufixo={`${NB}tons`}
    nota={{ texto: "More than six million cubic feet of rock", cue: "700" }} />
);

// 4. as molas (p22)
export const A04Springs: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Steel springs under the buildings", titulo: "It depends on the source", linhas: [
    { rotulo: "Museum count", valor: `937`, cue: "937" },
    { rotulo: "Air and Space Forces Magazine", valor: `1,319`, cue: "1", destaque: true },
  ], tint: "cool" }} />
);

// 5. as portas (p31)
export const A05Doors: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The blast door", titulo: "Steel at the entrance", linhas: [
    { rotulo: "Most sources", valor: `25${NB}tons`, cue: "25", destaque: true },
    { rotulo: "The honest range", valor: `20 to 25${NB}tons`, cue: "20" },
  ], tint: "cool" }} />
);

// 6. área, custo e data (p40)
export const A06Cost: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cheyenne Mountain · finished", titulo: "The bill and the date", linhas: [
    { rotulo: "Underground area", valor: `5.1${NB}acres`, cue: "5" },
    { rotulo: "Cost in 1960s money", valor: `$142${NB}million`, cue: "142", destaque: true },
    { rotulo: "Full operational capability", valor: `April${NB}20, 1966`, cue: "20" },
  ], tint: "accent" }} />
);

// 7. a ogiva soviética (p52)
export const A07Megatons: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Soviet R-36 · single warhead", titulo: "Aimed at hardened targets", linhas: [
    { rotulo: "Smallest version", valor: `18${NB}megatons`, cue: "18" },
    { rotulo: "Largest version", valor: `25${NB}megatons`, cue: "25", destaque: true },
  ], tint: "accent" }} />
);

// 8. pessoas lá dentro (p66)
export const A08People: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "50th anniversary · April 2016", titulo: "People inside the mountain", linhas: [
    { rotulo: "At any given time, at least", valor: `350`, cue: "350" },
    { rotulo: "Up to", valor: `580`, cue: "580", destaque: true },
  ], tint: "cool" }} />
);
