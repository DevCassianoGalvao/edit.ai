// Animações de "B-52D — six seats ranked" (en, enxuto) — painel 20261019-225803-eng-doc-b52 (baia b1).
// REGRA: biblioteca + MAPA; motion curto (cues <= ~12 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { Lista } from "./blocos";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o gigante (p02)
export const E01Gigante: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Boeing B-52D Stratofortress", titulo: "A huge machine", linhas: [
    { rotulo: "Wingspan", valor: `185${NB}feet`, cue: "185" },
    { rotulo: "Length", valor: `156${NB}feet`, cue: "156" },
    { rotulo: "Decks", valor: "two", cue: "decks", destaque: true },
  ], tint: "accent" }} />
);

// 2. Big Belly (p13)
export const E02BigBelly: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Big Belly modification · December 1965", titulo: "The bomb load", linhas: [
    { rotulo: "Inside the bay", valor: `84 bombs · 500${NB}lb`, cue: "84" },
    { rotulo: "Under the wings", valor: `24 bombs · 750${NB}lb`, cue: "24" },
    { rotulo: "Total", valor: "108 bombs", cue: "108", destaque: true },
  ], nota: `about 60,000${NB}pounds`, notaCue: "60", tint: "accent" }} />
);

// 3. a primeira noite (p22)
export const E03Noite: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "December 18 · North Vietnam", titulo: "The first night", linhas: [
    { rotulo: "Missiles launched", valor: "164", cue: "164" },
    { rotulo: "Bombers over Hanoi", valor: "129", cue: "129" },
    { rotulo: "Shot down by missiles", valor: "2", cue: "two", destaque: true },
  ], tint: "danger" }} />
);

// 4. MAPA Guam / U-Tapao -> Vietnã do Norte (p28)
export const E04Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="THE LONG MISSIONS" lugares={[
    { nome: "Guam", lat: 13.45, lon: 144.79, cue: "guam", esquerda: true },
    { nome: "North Vietnam", lat: 21.03, lon: 105.85, cue: "vietnam" },
  ]} marca={{ nome: "U-Tapao · Thailand", lat: 12.68, lon: 101.0, cue: "utapa" }} tint={colors.cool} />
);

// 5. a corrida final (p35)
export const E05Corrida: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Linebacker II · the final run" titulo="No way to dodge" tint={colors.danger} itens={[
    { titulo: "Electronic warfare officer", texto: "jamming", cue: "jamming" },
    { titulo: "Pilots", texto: "holding the line", cue: "holding" },
    { titulo: "Tail gunner", texto: "calling out missiles", cue: "gunner" },
    { titulo: "Radar navigator", texto: "staring at a scope", cue: "staring" },
  ]} />
);

// 6. Brown 3 (p42)
export const E06Turner: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="18" chave={3} linhas={[
    "DECEMBER 18, 1972 · CALL SIGN BROWN 3",
    "",
    "Staff Sergeant Samuel Turner, tail gunner",
    "Shot down a MiG-21",
    "The first B-52 gunner to down an enemy fighter",
  ]} carimbo={{ texto: "FIRST IN HISTORY", cue: "21" }} />
);

// 7. a ordem, do mais seguro ao mais mortal (p49)
export const E07Ordem: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="From safest to deadliest" tint={colors.accent} itens={[
    { titulo: "The copilot", cue: "co" },
    { titulo: "The aircraft commander", cue: "commander" },
    { titulo: "The electronic warfare officer", cue: "electronic" },
    { titulo: "The navigator", cue: "navigator" },
    { titulo: "The radar navigator", cue: "radar" },
    { titulo: "The tail gunner", cue: "tail", cor: colors.danger },
  ]} />
);
