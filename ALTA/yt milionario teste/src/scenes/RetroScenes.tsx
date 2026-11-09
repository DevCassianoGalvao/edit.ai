// As animações de "Chiny produkują klasyki z elektrykiem" (pl, arquivo dark) — painel 20261005-111311 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
// Polonês: NBSP depois de palavra de uma letra (w, z, i, a, o, u).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Tank 300 (p08)
export const S01Tank: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Great Wall · marka Tank, czyli czołg", titulo: "Tank 300", linhas: [
    { rotulo: "Model", valor: `Tank${NB}300`, cue: "300", destaque: true },
    { rotulo: "Debiut", valor: "początek lat dwudziestych", cue: "dwudziestych" },
    { rotulo: "Sylwetka", valor: `kanciasta bryła, koło na${NB}klapie`, cue: "kanciasta" },
  ], tint: "accent" }} />
);

// 2. Wuling Hongguang Mini (p13)
export const S02Wuling: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Wuling · SAIC + General Motors", titulo: "Hongguang Mini", linhas: [
    { rotulo: "Model", valor: "Hongguang Mini", cue: "hongguang" },
    { rotulo: "Miejsca", valor: `4${NB}osoby`, cue: "4" },
    { rotulo: "Cena w${NB}Chinach", valor: `około 29${NB}tys. juanów`, cue: "29", destaque: true },
  ], tint: "accent" }} />
);

// 3. Landwind X7 x Evoque (p26)
export const S03Landwind: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Najgłośniejsza sprawa", titulo: "Kopia czy inspiracja?", linhas: [
    { rotulo: "Chiński model", valor: `Landwind${NB}X7`, cue: "x7" },
    { rotulo: "Oryginał", valor: "Range Rover Evoque", cue: "evoque", destaque: true },
  ], tint: "accent" }} />
);

// 4. Hongqi (p31)
export const S04Hongqi: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hongqi · Czerwona Flaga", titulo: "Najstarsza chińska marka luksusowa", linhas: [
    { rotulo: "Założona", valor: `koniec lat${NB}50.`, cue: "50", destaque: true },
    { rotulo: "Limuzyny", valor: "dla przywódców państwa", cue: "przywodcy" },
    { rotulo: "Na${NB}defiladach", valor: `i${NB}oficjalnych wizytach`, cue: "defilad" },
  ], tint: "accent" }} />
);

// 5. MAPA: fabryki poza Chinami (p35)
export const S05Fabryki: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CŁA NIE ZATRZYMAŁY ZJAWISKA · FABRYKI POZA CHINAMI" lugares={[
    { nome: "Chiny", lat: 34.0, lon: 108.9, cue: "chinami" },
    { nome: "Turcja", lat: 38.6, lon: 27.4, cue: "turcji", abaixo: true },
    { nome: "Węgry", lat: 46.25, lon: 20.15, cue: "wegrzech" },
    { nome: "Hiszpania", lat: 41.35, lon: 2.15, cue: "hiszpanii", abaixo: true },
    { nome: "Tajlandia", lat: 12.7, lon: 101.2, cue: "tajlandii", abaixo: true },
    { nome: "Brazylia", lat: -12.7, lon: -38.3, cue: "brazylii" },
  ]} tint={colors.accent} />
);

// 6. wartość rezydualna (p52)
export const S06Wartosc: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Wartość rezydualna", titulo: "Ile będzie wart taki samochód?", linhas: [
    { rotulo: "Za", valor: `8${NB}lat?`, cue: "8" },
    { rotulo: "Za", valor: `10${NB}lat?`, cue: "10", destaque: true },
    { rotulo: "Serwis i${NB}części", valor: "czekanie tygodniami", cue: "serwis" },
  ], tint: "accent" }} />
);

// 7. ta sama deskorolka (p57)
export const S07Deskorolka: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ta sama deskorolka", titulo: "Do wyboru wygląd", linhas: [
    { rotulo: "Wygląd", valor: "Garbus", cue: "garbusa" },
    { rotulo: "Wygląd", valor: "Defender", cue: "defendera" },
    { rotulo: "Wygląd", valor: `limuzyna z${NB}lat${NB}50.`, cue: "50", destaque: true },
  ], tint: "accent" }} />
);
