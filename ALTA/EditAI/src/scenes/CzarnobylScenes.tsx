// Animações de "36 000 Ton Stali nad Reaktorem" (pl) — painel 20261015-004953 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com espaço (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o arco em números (p01)
export const C01Luk: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nowa Bezpieczna Osłona · Czarnobyl", titulo: "Łuk nad czwartym blokiem", linhas: [
    { rotulo: "Rozpiętość", valor: `257${NB}m`, cue: "257", destaque: true },
    { rotulo: "Długość", valor: `162${NB}m`, cue: "162" },
    { rotulo: "Wysokość", valor: `108${NB}m`, cue: "108" },
  ], tint: "accent" }} />
);

// 2. MAPA: a nuvem de 1986 — Czarnobyl -> Białoruś -> Mikołajki (p05)
export const C02Chmura: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="KWIECIEŃ 1986 · RADIOAKTYWNA CHMURA" lugares={[
    { nome: "Czarnobyl", lat: 51.39, lon: 30.10, cue: "helikopterów", abaixo: true, esquerda: true },
    { nome: "Białoruś", lat: 53.10, lon: 27.60, cue: "Białoruś" },
    { nome: "Mikołajki", lat: 53.80, lon: 21.57, cue: "Mikołajkach", abaixo: true },
  ]} tint={colors.danger} />
);

// 3. o sarcófago de 1986 (p11)
export const C03Sarkofag: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="206" chave={2} linhas={[
    "SARKOFAG · CZWARTY BLOK · 1986",
    "",
    `Budowa: 206${NB}dni`,
    `Beton: ponad 400${NB}000${NB}m³`,
    `Stal: 7${NB}300${NB}ton`,
  ]} carimbo={{ texto: "ZDALNIE", cue: "zdalnie" }} />
);

// 4. a dose: 20 mSv x fundo natural x raio X (p19)
export const C04Dawka: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Dawka promieniowania · milisiwerty" titulo="Ile to jest 20 mSv?" tint={colors.accent} max={20}
    barras={[
      { rotulo: "Roczny limit pracownika", valor: `20${NB}mSv`, v: 20, cue: "20", cor: colors.danger },
      { rotulo: "Naturalne tło (rocznie)", valor: `ok. 2,5${NB}mSv`, v: 2.5, cue: "2" },
      { rotulo: "Prześwietlenie klatki piersiowej", valor: `ok. 0,1${NB}mSv`, v: 0.4, cue: "prześwietlenie", cor: colors.textDim },
    ]} />
);

// 5. o deslize da Mammoet (p37)
export const C05Mammoet: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mammoet · listopad 2016", titulo: "Jak przesunąć 36 000 ton", linhas: [
    { rotulo: "Płozy ślizgowe", valor: "116", cue: "116" },
    { rotulo: "Udźwig jednej płozy", valor: `ok. 700${NB}t`, cue: "700" },
    { rotulo: "Siłowniki hydrauliczne", valor: "224", cue: "224", destaque: true },
  ], tint: "accent" }} />
);

// 6. MAPA: o trem Sławutycz -> elektrownia, cruzando a Bielorrússia (p48)
export const C06Pociag: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="POCIĄG DO PRACY · SŁAWUTYCZ — CZARNOBYL" lugares={[
    { nome: "Sławutycz", lat: 51.52, lon: 30.75, cue: "Sławutycza", abaixo: true, esquerda: true },
    { nome: "Elektrownia", lat: 51.39, lon: 30.10, cue: "elektrowni", esquerda: true },
  ]} marca={{ nome: "Białoruś", lat: 51.62, lon: 30.40, nota: "trasa 2 razy przez granicę", cue: "Białorusią" }}
    tint={colors.accent} />
);

// 7. as pontes rolantes sob o arco (p56)
export const C07Suwnice: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pod łukiem · dwie suwnice mostowe", titulo: "Dźwigi sterowane zdalnie", linhas: [
    { rotulo: "Rozpiętość suwnicy", valor: `84${NB}m`, cue: "84" },
    { rotulo: "Wózek ładunkowy", valor: `50${NB}t`, cue: "50" },
    { rotulo: "Wózek dla ludzi", valor: `50${NB}t`, cue: "przewożenia" },
    { rotulo: "Platforma w dół", valor: `do 75${NB}m`, cue: "75", destaque: true },
  ], tint: "accent" }} />
);

// 8. a zmiana que ficou presa (p69)
export const C08Zmiana: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ZMIANA Z 24 LUTEGO 2022 · NA POSTERUNKU" valor={25} cue="25" sufixo=" dni" sep={NB}
    nota={{ texto: `około 600${NB}godzin bez zmiany`, cue: "600" }} />
);

// 9. o preço do conserto (p84)
export const C09Naprawa: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="pół" chave={2} linhas={[
    "NAPRAWA ŁUKU · EBOiR",
    "",
    "Pełna naprawa: ponad pół miliarda euro",
    `Zebrano: ponad 70${NB}milionów`,
    "Czas: jeszcze 3-4 lata",
  ]} carimbo={{ texto: "3-4 LATA", cue: "lata" }} />
);
