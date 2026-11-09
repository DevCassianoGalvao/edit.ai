// As animações de "Honda Rzuca BOMBĘ — Nowa Hybryda od 2027" (pl) — painel 20261022-123739 (baia b1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o comunicado de 9/10/2026 (p02)
export const H01Komunikat: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Honda · komunikat z 9 października 2026", titulo: "Honda Hybrid", linhas: [
    { rotulo: "Debiut globalny", valor: `od 2027${NB}roku`, cue: "2027" },
    { rotulo: "Termin", valor: `do 31${NB}marca 2030`, cue: "31" },
    { rotulo: "Nowe modele hybrydowe", valor: "15", cue: "15", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA: Ohio e Ontário — os cortes de maio de 2025 (p08)
export const H02Kanada: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`MAJ 2025 · CIĘCIA O 21${NB}MLD${NB}$`} lugares={[
    { nome: "Ohio · centrum aut elektrycznych", lat: 40.24, lon: -83.37, cue: "elektryki", abaixo: true },
    { nome: `Ontario · 11${NB}mld${NB}$ wstrzymane`, lat: 44.15, lon: -79.87, cue: "kanadzie" },
  ]} linhas={[
    { pontos: [[41.68, -83.47], [41.5, -81.7], [42.13, -80.08], [42.88, -78.9], [42.85, -79.6], [42.6, -80.4],
      [42.65, -81.2], [42.3, -82.0], [42.0, -82.5], [42.05, -83.15], [41.68, -83.47]] },
    { pontos: [[43.25, -79.8], [43.65, -79.38], [43.95, -78.2], [44.05, -77.0], [44.2, -76.5], [43.47, -76.5],
      [43.27, -77.6], [43.3, -79.05], [43.25, -79.8]] },
    { pontos: [[43.0, -82.42], [43.75, -81.72], [44.45, -81.4], [45.0, -81.3]] },
    { pontos: [[41.7, -84.81], [41.68, -83.47]] },
    { pontos: [[41.98, -80.52], [40.64, -80.52], [39.6, -80.8], [38.9, -82.1], [38.4, -82.6], [39.1, -84.82], [41.7, -84.81]] },
  ]} tint={colors.accent} />
);

// 3. o rodowód das hybrydy Hondy (p17)
export const H03Rodowod: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Honda · hybrydy od 1999 roku", titulo: "Rodowód", linhas: [
    { rotulo: "Pierwszy Insight · układ IMA", valor: "1999", cue: "1999" },
    { rotulo: "Trzy nowe systemy", valor: "2012", cue: "2012", destaque: true },
  ], tint: "cool" }} />
);

// 4. os motores Atkinson de dezembro de 2024 (p24)
export const H04Atkinson: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cykl Atkinsona · 1,5 l i 2 l", titulo: "Nowa generacja", linhas: [
    { rotulo: "Obszar wysokiej sprawności (1,5 l)", valor: `szerszy o ponad 40${NB}%`, cue: "40", destaque: true },
    { rotulo: "Spalanie całej generacji", valor: `o ponad 10${NB}% mniej`, cue: "10" },
  ], tint: "accent" }} />
);

// 5. a Toyota na Polônia (p37)
export const H05Toyota: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TOYOTA · POLSKA · STYCZEŃ–WRZESIEŃ 2026" valor={73945} cue="73" sep={NB}
    sufixo="aut" nota={{ texto: `ponad 24${NB}tysiące aut przewagi nad drugą marką`, cue: "24" }} />
);

// 6. BYD, 5ª geração DM (p42)
export const H06BYD: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BYD · piąta generacja · maj 2024", titulo: "Qin L i Seal 06", linhas: [
    { rotulo: "Sprawność cieplna silnika", valor: `46,06${NB}%`, cue: "46", destaque: true },
    { rotulo: "Zużycie przy pustej baterii (NEDC)", valor: `2,9${NB}l/100${NB}km`, cue: "2" },
  ], tint: "danger" }} />
);

// 7. UE 2035 (p49)
export const H07UE2035: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Komisja Europejska · 16 grudnia 2025", titulo: "Rok 2035", linhas: [
    { rotulo: "Dotąd: redukcja CO₂", valor: `100${NB}%`, cue: "100" },
    { rotulo: "Propozycja", valor: `90${NB}%`, cue: "90", destaque: true },
  ], tint: "cool" }} />
);

// 8. Polônia, 1º semestre de 2026 (p55)
export const H08Polska: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="POLSKA · I PÓŁROCZE 2026 · PZPM" valor={75951} cue="75" sep={NB}
    sufixo="hybryd" nota={{ texto: `wzrost o 16,6${NB}%`, cue: "16" }} />
);
