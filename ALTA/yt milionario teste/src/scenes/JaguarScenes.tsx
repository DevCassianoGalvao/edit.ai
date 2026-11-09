// Animações de "Jaguar Chce 650 Tysięcy Złotych za To Auto" (pl) — painel 20261012-082955 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 14 s); todo número é dito; milhar com espaço, decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, LinhaDoTempo } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. registros no Reino Unido (p02)
export const J01Rejestracje: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Nowe rejestracje Jaguara · Wielka Brytania" titulo={`Spadek o ponad 99${NB}%`} tint={colors.accent} max={783} barras={[
    { rotulo: "Styczeń 2025", valor: `783${NB}auta`, v: 783, cue: "783", cor: colors.textDim },
    { rotulo: "Styczeń 2026", valor: `6${NB}aut`, v: 6, cue: "6" },
  ]} />
);

// 2. Europa continental (p15)
export const J02Europa: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Rejestracje Jaguara · Europa kontynentalna" titulo={`Spadek o ponad 75${NB}%`} tint={colors.accent} max={10641} barras={[
    { rotulo: "Kwiecień 2025", valor: "49", v: 49, cue: "49" },
    { rotulo: "Styczeń–kwiecień 2025", valor: `2${NB}665`, v: 2665, cue: "2665" },
    { rotulo: "Styczeń–kwiecień 2024", valor: `10${NB}641`, v: 10641, cue: "10", cor: colors.textDim },
  ]} />
);

// 3. o ciberataque (p28)
export const J03Cyberatak: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cyberatak na JLR · wrzesień 2025", titulo: "Rachunek za pięć tygodni przestoju", linhas: [
    { rotulo: "Koszt ataku w kwartale", valor: `196${NB}mln${NB}£`, cue: "196" },
    { rotulo: "Strata kwartalna", valor: `559${NB}mln${NB}£`, cue: "559", destaque: true },
  ], tint: "danger" }} />
);

// 4. os números do Type 01 (p37)
export const J04Liczby: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jaguar Type 01 · dane techniczne", titulo: "Najmocniejszy Jaguar drogowy", linhas: [
    { rotulo: "Moc", valor: `1${NB}030${NB}KM`, cue: "1030", destaque: true },
    { rotulo: "Moment obrotowy", valor: `1${NB}365${NB}Nm`, cue: "1365" },
    { rotulo: "0–100 km/h", valor: `3,2${NB}s`, cue: "3" },
  ], tint: "accent" }} />
);

// 5. MAPA: as fábricas inglesas (p40)
export const J05Fabryki: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Type 01 · made in England" lugares={[
    { nome: "Solihull · montaż", lat: 52.41, lon: -1.78, cue: "solihull", abaixo: true },
    { nome: "Wolverhampton · silniki i baterie", lat: 52.59, lon: -2.13, cue: "wolverhampton", esquerda: true },
    { nome: "Halewood · nadwozia", lat: 53.35, lon: -2.83, cue: "hailwood|halewood", esquerda: true },
  ]} tint={colors.accent} />
);

// 6. o preço (p43)
export const J06Cena: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jaguar Type 01 · cena bazowa", titulo: "Z funtów na złote", linhas: [
    { rotulo: "Cena w Wielkiej Brytanii", valor: `od 130${NB}000${NB}£`, cue: "130" },
    { rotulo: "Kurs z dnia premiery", valor: `5,16${NB}zł`, cue: "5" },
    { rotulo: "W złotych", valor: `ok. 670${NB}tys.${NB}zł`, cue: "670", destaque: true },
  ], tint: "accent" }} />
);

// 7. Xiaomi x Jaguar (p63)
export const J07Xiaomi: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Moc · konie mechaniczne" titulo="Chińczycy dają więcej" tint={colors.accent} max={1548} barras={[
    { rotulo: "Xiaomi SU7 Ultra", valor: `1${NB}548${NB}KM`, v: 1548, cue: "1548" },
    { rotulo: "Jaguar Type 01", valor: `1${NB}030${NB}KM`, v: 1030, cue: "jaguar", cor: colors.textDim },
  ]} />
);

// 8. o balanço (p69)
export const J08Bilans: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="Jaguar · od 783 do 6" tint={colors.accent} marcos={[
    { ano: "XII 2025", texto: "ostatni spalinowy", cue: "spalin" },
    { ano: "I 2026", texto: "6 rejestracji", cue: "szesc|sześć|6" },
    { ano: "X 2026", texto: `ponad 650${NB}tys.${NB}zł`, cue: "650", cor: colors.accent },
  ]} />
);
