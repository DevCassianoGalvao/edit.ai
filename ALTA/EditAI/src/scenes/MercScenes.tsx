// Animações de "Mercedes — silnik osiowy z Berlina" (pl, enxuto) — painel 20261019-125226-polones-car (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Marienfelde w liczbach (p03)
export const M01Fabryka: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Berlin-Marienfelde · silniki osiowe", titulo: "Nowa produkcja", linhas: [
    { rotulo: "Powierzchnia", valor: `30${NB}000${NB}m²`, cue: "30" },
    { rotulo: "Etapy procesu", valor: "98", cue: "98" },
    { rotulo: "Nowe w skali świata", valor: "35", cue: "35", destaque: true },
  ], tint: "accent" }} />
);

// 2. Trzy razy lżejszy i mniejszy (p08)
export const M02Trzy: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SILNIK OSIOWY · WEDŁUG MERCEDESA" valor={3} sufixo="×" sep=" "
    cue="trzy" nota={{ texto: "mniej masy · mniej miejsca", cue: "miejsca" }} />
);

// 3. Fabryka Yasy w Yarnton (p13)
export const M03Yarnton: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="YASA · FABRYKA W YARNTON, ANGLIA" valor={25000} prefixo="ponad" sep=" "
    cue="25" nota={{ texto: `silników rocznie · modernizacja za 12${NB}mln funtów`, cue: "silników" }} />
);

// 4. GT 63 · osiągi (p17)
export const M04Gt63: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mercedes-AMG GT 63 · według producenta", titulo: "Osiągi", linhas: [
    { rotulo: `0–100${NB}km/h`, valor: `2,4${NB}s`, cue: "2" },
    { rotulo: `0–200${NB}km/h`, valor: `6,4${NB}s`, cue: "200" },
    { rotulo: "Prędkość maks.", valor: `300${NB}km/h`, cue: "300", destaque: true },
  ], tint: "danger" }} />
);

// 5. Ładowanie (p22)
export const M05Ladowanie: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "AMG GT · ładowanie prądem stałym", titulo: "Ładowanie", linhas: [
    { rotulo: "Moc ładowania", valor: `do${NB}600${NB}kW`, cue: "600", destaque: true },
    { rotulo: `10${NB}minut`, valor: `+${NB}460${NB}km`, cue: "460" },
    { rotulo: `10→80${NB}%`, valor: `11${NB}minut`, cue: "80" },
  ], tint: "cool" }} />
);

// 6. Ceny w Niemczech (p28)
export const M06Ceny: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Niemcy · ceny bazowe" titulo="Ile kosztuje AMG GT"
    tint={colors.accent} max={196350} barras={[
    { rotulo: "GT 55", valor: `154${NB}700${NB}€`, v: 154700, cue: "154" },
    { rotulo: "GT 63", valor: `196${NB}350${NB}€`, v: 196350, cue: "196", cor: colors.danger },
    { rotulo: "GT 53", valor: `115${NB}430${NB}€`, v: 115430, cue: "53" },
  ]} />
);

// 7. DeepDrive · obietnice (p33)
export const M07DeepDrive: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BMW · startup DeepDrive · deklaracje", titulo: "Taniej w produkcji", linhas: [
    { rotulo: "Materiał magnetyczny", valor: "o połowę mniej", cue: "połowę" },
    { rotulo: "Żelazo", valor: `−80${NB}%`, cue: "80", destaque: true },
    { rotulo: "Koszt silnika", valor: `<${NB}1/3 ceny`, cue: "1" },
  ], tint: "accent" }} />
);

// 8. Ofensywa modelowa 2026 (p41)
export const M08Ofensywa: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mercedes-Benz · 2026", titulo: "Ofensywa modelowa", linhas: [
    { rotulo: "Premiery", valor: "18", cue: "18" },
    { rotulo: "W tym spalinowe", valor: "9", cue: "9", destaque: true },
    { rotulo: `Klasa S · V8 4,0${NB}l`, valor: `530${NB}KM`, cue: "530" },
  ], tint: "danger" }} />
);

// 9. MAPA: Berlin i Yarnton (p57)
export const M09Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="INŻYNIEROWIE SILNIKA OSIOWEGO" lugares={[
    { nome: "Berlin · Mercedes", lat: 52.42, lon: 13.37, cue: "berlina", esquerda: true },
    { nome: "Yarnton · YASA", lat: 51.80, lon: -1.31, cue: "jarnton", abaixo: true },
  ]} tint={colors.accent} />
);
