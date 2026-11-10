// Animações de "Musk Rzuca BOMBĘ — Latający Roadster z Dyszami SpaceX" (pl, enxuto) — painel 20261016-134202 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, LinhaDoTempo } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: McGregor e Waco, środkowy Teksas (p01)
export const R01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="POKAZ ROADSTERA · OŚRODEK TESTOWY SPACEX" lugares={[
    { nome: "McGregor · SpaceX", lat: 31.44, lon: -97.41, cue: "mcgregor", abaixo: true, esquerda: true },
    { nome: "Waco", lat: 31.55, lon: -97.15, cue: "waco" },
  ]} tint={colors.accent} />
);

// 2. Przyspieszenie: deklaracja Tesli (p07)
export const R02Start: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Roadster z dyszami · deklaracja Tesli", titulo: `Poniżej 1${NB}sekundy`, linhas: [
    { rotulo: "Sprint", valor: `0–60${NB}mil/h`, cue: "60" },
    { rotulo: "Czyli mniej więcej", valor: `0–97${NB}km/h`, cue: "97" },
    { rotulo: "Czas", valor: `poniżej 1${NB}s`, cue: "1" },
    { rotulo: "Na stronie Tesli", valor: `0,81${NB}s`, cue: "wartość", destaque: true },
  ], tint: "accent" }} />
);

// 3. Co napędza skok (p19)
export const R03Dysze: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Lars Moravy · Tesla", titulo: "Napęd skoku", linhas: [
    { rotulo: "Dysze w samochodzie", valor: "10", cue: "10" },
    { rotulo: "Sprężone powietrze", valor: `600${NB}litrów`, cue: "600", destaque: true },
    { rotulo: "Układ", valor: "gaz zimny · bez spalania", cue: "zimnego" },
  ], tint: "cool" }} />
);

// 4. Strefa zakazu lotów nad McGregor (p27)
export const R04Strefa: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FAA · TYMCZASOWA STREFA ZAKAZU LOTÓW · McGREGOR" valor={10000} sufixo={`${NB}stóp`} sep=" "
    cue="10" nota={{ texto: `około 3${NB}km wysokości`, cue: "3" }} />
);

// 5. Lista dat (p34)
export const R05Daty: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="Roadster · przesuwane terminy" tint={colors.danger} marcos={[
    { ano: "IX 2021", texto: "na 2023", cue: "2021" },
    { ano: "V 2023", texto: "na 2024", cue: "2023" },
    { ano: "II 2024", texto: "na 2025", cue: "2024", cor: colors.danger },
  ]} />
);

// 6. Liczby, które się skurczyły (p42)
export const R06Liczby: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Roadster · obietnica 2017 i dziś" titulo="Liczby się skurczyły"
    tint={colors.accent} max={1000} barras={[
    { rotulo: "Zasięg · 2017", valor: `≈${NB}1${NB}000${NB}km`, v: 1000, cue: "300" },
    { rotulo: "Zasięg · dziś", valor: `≈${NB}480${NB}km`, v: 480, cue: "480", cor: colors.danger },
    { rotulo: "Prędkość maks. · 2017", valor: `>${NB}400${NB}km/h`, v: 400, cue: "230" },
    { rotulo: "Prędkość maks. · dziś", valor: `≈${NB}370${NB}km/h`, v: 370, cue: "370", cor: colors.danger },
  ]} />
);

// 7. Cennik rezerwacji: Performance (p48)
export const R07Cennik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Roadster Performance · rezerwacja", titulo: `50${NB}000${NB}dolarów`, linhas: [
    { rotulo: "Rezerwacja", valor: `50${NB}000${NB}$`, cue: "50", destaque: true },
    { rotulo: "Najpierw", valor: `5${NB}000${NB}$`, cue: "5" },
    { rotulo: "W ciągu 10 dni", valor: `+${NB}45${NB}000${NB}$`, cue: "45" },
  ], tint: "danger" }} />
);

// 8. Polska · wrzesień (p61)
export const R08Polska: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Polska · wrzesień · Samar", titulo: "Rejestracje nowych aut", linhas: [
    { rotulo: "Osobowe i dostawcze", valor: `62${NB}492`, cue: "62" },
    { rotulo: "Rok do roku", valor: `+${NB}prawie 12,5${NB}%`, cue: "12" },
    { rotulo: "Udział marek z Chin", valor: `15,6${NB}%`, cue: "15", destaque: true },
  ], tint: "accent" }} />
);
