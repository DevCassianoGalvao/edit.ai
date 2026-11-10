// Animações de "Tesla Rzuca BOMBĘ — Nowy Roadster z Napędem SpaceX" (pl, enxuto) — painel 20261017-172925 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: McGregor e Waco, środkowy Teksas (p01)
export const R01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="POKAZ ROADSTERA · OŚRODEK TESTOWY SPACEX" lugares={[
    { nome: "McGregor · SpaceX", lat: 31.44, lon: -97.41, cue: "mcgregor", abaixo: true, esquerda: true },
    { nome: "Waco", lat: 31.55, lon: -97.15, cue: "waco" },
  ]} tint={colors.accent} />
);

// 2. Zbiornik wersji Thrust (p09)
export const R02Zbiornik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Roadster Thrust · według Top Gear", titulo: "Zbiornik w bagażniku", linhas: [
    { rotulo: "Pojemność", valor: `200${NB}litrów`, cue: "200" },
    { rotulo: "Ciśnienie gazu", valor: `≈${NB}690${NB}barów`, cue: "690", destaque: true },
    { rotulo: "Opona osobówki", valor: `≈${NB}2,5${NB}bara`, cue: "2" },
  ], tint: "cool" }} />
);

// 3. Jedno napełnienie = jeden strzał (p14)
export const R03Strzal: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="WERSJA THRUST · JEDNO NAPEŁNIENIE ZBIORNIKA" valor={5} sufixo={`${NB}s`} sep=" "
    cue="5" nota={{ texto: `pracy dysz · jeden start do 100${NB}km/h`, cue: "100" }} />
);

// 4. Moc i ładowanie (p20)
export const R04Moc: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nowy Roadster · bateria i ładowanie", titulo: "Napięcie i ładowanie", linhas: [
    { rotulo: "Napięcie baterii", valor: `800–1000${NB}V`, cue: "800" },
    { rotulo: "Ładowanie", valor: `>${NB}500${NB}kW`, cue: "500", destaque: true },
    { rotulo: `15→80${NB}%`, valor: `10${NB}minut`, cue: "15" },
  ], tint: "accent" }} />
);

// 5. Zasięg: obietnica 2017 i dziś (p28)
export const R05Zasieg: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Roadster · zasięg na jednym ładowaniu" titulo="Zasięg spadł o połowę"
    tint={colors.accent} max={1000} barras={[
    { rotulo: `2017 · 620${NB}mil`, valor: `≈${NB}1${NB}000${NB}km`, v: 1000, cue: "620" },
    { rotulo: `2026 · 300${NB}mil`, valor: `≈${NB}480${NB}km`, v: 480, cue: "300", cor: colors.danger },
  ]} />
);

// 6. Cennik z 2017 roku (p34)
export const R06Cennik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Roadster · obietnica z 2017 roku", titulo: "Ceny z prezentacji Semi", linhas: [
    { rotulo: "Cena bazowa", valor: `200${NB}000${NB}$`, cue: "200" },
    { rotulo: "Founders Series", valor: `250${NB}000${NB}$`, cue: "250", destaque: true },
    { rotulo: "Depozyt", valor: `50${NB}000${NB}$`, cue: "50" },
  ], tint: "danger" }} />
);

// 7. BYD kontra Tesla, III kwartał 2026 (p39)
export const R07Byd: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="III kwartał 2026 · auta w pełni elektryczne" titulo="BYD kontra Tesla"
    tint={colors.accent} max={762478} barras={[
    { rotulo: "BYD", valor: `762${NB}478`, v: 762478, cue: "762", cor: colors.danger },
    { rotulo: "Tesla", valor: `486${NB}532`, v: 486532, cue: "478" },
  ]} nota={{ texto: `BYD: ponad 30${NB}% więcej rok do roku`, cue: "30" }} />
);

// 8. Polska · wrzesień 2026 (p49)
export const R08Polska: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Polska · wrzesień 2026", titulo: "Rejestracje nowych aut", linhas: [
    { rotulo: "Nowe osobowe", valor: `62${NB}492`, cue: "62" },
    { rotulo: "Rok do roku", valor: `+${NB}12,47${NB}%`, cue: "12" },
    { rotulo: "Udział marek z Chin", valor: `15,6${NB}%`, cue: "15", destaque: true },
  ], tint: "accent" }} />
);
