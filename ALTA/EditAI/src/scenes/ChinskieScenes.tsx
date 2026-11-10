// Animações de "Tysiące Polaków Kupiło BYD lub MG" (pl, enxuto) — painel 20261028-143200 (baia b1).
// REGRA: biblioteca; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { colors } from "../design/tokens";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Skala rynku 2025 (p01)
export const S01Skala: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Polska · rejestracje w 2025 roku", titulo: "Skala rynku", linhas: [
    { rotulo: "Nowe samochody osobowe", valor: `597${NB}428`, cue: "597" },
    { rotulo: "Marki z Chin", valor: `49${NB}161`, cue: "49", destaque: true },
  ], tint: "accent" }} />
);

// 2. Gwarancja BYD kontra MG (p06)
export const S02Gwarancja: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Gwarancja · akumulator i auto", titulo: "BYD kontra MG", linhas: [
    { rotulo: "BYD · akumulator", valor: `8${NB}lat`, cue: "8", destaque: true },
    { rotulo: "MG · całe auto", valor: `7${NB}lat`, cue: "7" },
    { rotulo: "MG · limit przebiegu", valor: `150${NB}tys.${NB}km`, cue: "150" },
  ], tint: "accent" }} />
);

// 3. Tło: warunki innych marek (p10)
export const S03Tlo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Autocentrum · chińskie marki w Polsce", titulo: "Gwarancje na tle rynku", linhas: [
    { rotulo: "Chery · Omoda · Jaecoo", valor: `8${NB}lat`, cue: "8", destaque: true },
    { rotulo: "Próg pojemności akumulatora", valor: `75${NB}%`, cue: "75" },
    { rotulo: "Xpeng · całe auto", valor: `7${NB}lat`, cue: "7" },
  ], tint: "accent" }} />
);

// 4. Przeglądy MG HS (p29)
export const S04Przeglady: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Autocentrum · MG HS · przeglądy", titulo: "Ile kosztuje serwis", linhas: [
    { rotulo: "Pierwszy przegląd, 1 000 km", valor: `664${NB}zł`, cue: "664" },
    { rotulo: "Kolejne przeglądy, od", valor: `1${NB}254${NB}zł`, cue: "1254" },
    { rotulo: "Kolejne przeglądy, do", valor: `2${NB}531${NB}zł`, cue: "2531", destaque: true },
  ], nota: "Auto bez serwisu to auto bez gwarancji", tint: "danger" }} />
);

// 5. Wartość po czterech latach (p31)
export const S05Wartosc: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Carfax · po 4 latach i 60 tys. km", titulo: "Ile zostaje z ceny", linhas: [
    { rotulo: "MG", valor: `48,3${NB}%`, cue: "48" },
    { rotulo: "BAIC", valor: `47,2${NB}%`, cue: "47" },
    { rotulo: "BYD", valor: `44,7${NB}%`, cue: "44", destaque: true },
  ], tint: "danger" }} />
);

// 6. Hybrydy kontra elektryki (p40)
export const S06Hybrydy: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Grudzień · udział chińskich marek", titulo: "Gdzie naprawdę wygrywają", linhas: [
    { rotulo: "Hybrydy plug-in", valor: `51,7${NB}%`, cue: "51", destaque: true },
    { rotulo: "Samochody elektryczne", valor: `20,8${NB}%`, cue: "20" },
  ], tint: "accent" }} />
);

// 7. Dolphin Surf (p42)
export const S07Surf: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BYD DOLPHIN SURF · REJESTRACJE W CAŁYM ROKU" valor={1277} sufixo={`${NB}sztuk`} cue="1277" sep=" "
    nota={{ texto: `z ${6}${NB}853 rejestracji całej marki`, cue: "6853" }} />
);

// contorno da Polônia (lat, lon), sentido horário a partir de Świnoujście
const POLSKA: [number, number][] = [[53.91, 14.25], [54.18, 15.57], [54.58, 16.86], [54.76, 17.55], [54.6, 18.8], [54.35, 18.65],
  [54.45, 19.5], [54.35, 22.8], [54.3, 23.2], [53.95, 23.5], [53.5, 23.9], [52.8, 23.9], [52.08, 23.6], [51.5, 23.6],
  [50.8, 24.1], [50.4, 24.1], [49.9, 24.1], [49.8, 22.8], [49.0, 22.85], [49.1, 21.9], [49.4, 20.9], [49.2, 20.1],
  [49.4, 19.2], [49.75, 18.6], [49.95, 18.0], [50.3, 17.0], [50.4, 16.7], [50.9, 15.3], [51.15, 14.95], [51.7, 14.75],
  [52.3, 14.6], [52.8, 14.2], [53.4, 14.3], [53.91, 14.25]];

// 8. MAPA: dystans do serwisu (p26)
export const S08Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SIEĆ SERWISOWA · POLSKA" linhas={[{ pontos: POLSKA }]} lugares={[
    { nome: "Twój dom", lat: 53.18, lon: 22.06, cue: "mapie", esquerda: true },
    { nome: "Autoryzowany serwis", lat: 52.23, lon: 21.01, cue: "autoryzowanego", abaixo: true },
  ]} tint={colors.accent} />
);
