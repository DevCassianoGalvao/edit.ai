// Animações de "9 Strange Features in Old American Homes" (en, enxuto) — painel 20261102-014710 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. Tuberculose e o ar livre (nº 1)
export const H01Porch: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Number one · The sleeping porch", titulo: "Why people slept outdoors", linhas: [
    { rotulo: "Brooklyn, tuberculosis year", valor: "1908", cue: "1908" },
    { rotulo: "Share of all deaths", valor: "about 1 in 10", cue: "ten", destaque: true },
  ], tint: "accent" }} />
);

// 2. Garrafa e porta do leite (nº 2)
export const H02Milk: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Number two · The milk door", titulo: "The glass bottle era", linhas: [
    { rotulo: "First glass milk bottle patented", valor: "1878", cue: "1878", destaque: true },
    { rotulo: "Milk doors built, late 1800s through", valor: "the 1950s", cue: "1950s" },
  ], tint: "accent" }} />
);

// 3. O caminho do carvão (nº 3)
export const H03Carvao: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Number three · The coal chute" titulo="From the truck to the furnace" tint={colors.accent} itens={[
    { titulo: "A truck pulls up to the curb", cue: "truck" },
    { titulo: "A metal chute hooks to the house", cue: "chute" },
    { titulo: "Coal slides into the bin by the furnace", cue: "bin" },
  ]} />
);

// 4. MAPA: onde estão as cozinhas de verão (nº 4)
export const H04Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="NUMBER FOUR · WHERE SUMMER KITCHENS STAND" lugares={[
    { nome: "Pennsylvania", lat: 40.9, lon: -77.8, cue: "pennsylvania" },
    { nome: "The Midwest", lat: 41.0, lon: -89.5, cue: "midwest" },
    { nome: "The South", lat: 33.2, lon: -83.5, cue: "south" },
  ]} tint={colors.accent} />
);

// 5. Porão de raízes: temperatura e umidade (nº 5)
export const H05Porao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Number five · The root cellar", titulo: "What vegetables need", linhas: [
    { rotulo: "Temperature, degrees Fahrenheit", valor: "32 to 40", cue: "32", destaque: true },
    { rotulo: "Humidity, percent", valor: "85 to 95", cue: "85" },
  ], tint: "accent" }} />
);

// 6. Como o ar passa pela bandeira (nº 6)
export const H06Ar: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Number six · The transom" titulo="How the air moved" tint={colors.accent} itens={[
    { titulo: "Warm air rises to the ceiling", cue: "rises" },
    { titulo: "The open transom lets it escape", cue: "escape" },
    { titulo: "Cooler air comes in lower down", cue: "cooler" },
  ]} />
);

// 7. O Gossiper (nº 9)
export const H07Gossiper: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Number nine · The gossip bench", titulo: "The first famous one", linhas: [
    { rotulo: "Made by Floral City Furniture", valor: "the Gossiper", cue: "floral" },
    { rotulo: "Year", valor: "1928", cue: "1928", destaque: true },
    { rotulo: "Combined a stand, a bench and a rack for the", valor: "phone book", cue: "phone" },
  ], tint: "accent" }} />
);
