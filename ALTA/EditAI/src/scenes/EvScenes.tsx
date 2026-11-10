// As animações de "7 Samochodów Elektrycznych, Które Psują Się w 2026 Roku" (pl) — painel 20261027-123909 (baia b1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. VW ID.4 — a 1ª ação de janeiro de 2026 (p03)
export const E01Recall: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VOLKSWAGEN ID.4 · AKCJA SERWISOWA · STYCZEŃ 2026" valor={43881} cue="43" sep=" "
    nota={{ texto: `roczniki 2023–2025 · moduły baterii mogły się przegrzewać`, cue: "2023" }} />
);

// 2. Fisker Ocean — a ação de junho de 2024 (p15)
export const E02Fisker: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Fisker · akcja serwisowa · czerwiec 2024", titulo: "Fisker Ocean", linhas: [
    { rotulo: "Samochody objęte akcją", valor: `11${NB}201`, cue: "11", destaque: true },
    { rotulo: "Rynki", valor: "USA · Kanada · Europa", cue: "kanadzie" },
  ], tint: "danger" }} />
);

// 3. MAPA: Neta no Sudeste Asiático (p26)
const TAJLANDIA: [number, number][] = [[20.4, 99.9], [20.3, 100.9], [19.3, 101.0], [18.4, 101.2], [17.9, 102.1], [18.4, 103.0],
  [17.9, 104.0], [16.9, 104.8], [16.3, 105.4], [15.2, 105.5], [14.4, 105.2], [14.3, 103.5], [14.2, 102.5], [13.5, 102.4],
  [12.6, 102.4], [12.3, 101.9], [12.6, 101.3], [13.4, 100.9], [13.7, 100.6], [13.1, 100.1], [12.5, 99.9], [11.8, 99.8],
  [11.0, 99.6], [10.1, 99.2], [9.1, 99.3], [8.4, 99.9], [7.5, 100.4], [6.9, 100.6], [6.5, 100.3], [6.9, 99.9], [7.9, 98.4],
  [9.0, 98.3], [9.96, 98.6], [11.0, 99.1], [12.5, 99.0], [13.5, 99.1], [15.1, 98.2], [16.9, 98.6], [18.3, 97.7], [19.7, 98.9],
  [20.4, 99.9]];
const MALEZJA: [number, number][] = [[6.5, 100.3], [6.2, 102.0], [5.2, 103.4], [3.8, 103.4], [2.6, 103.5], [1.5, 104.2],
  [1.3, 103.6], [2.2, 102.2], [3.0, 101.4], [4.2, 100.6], [5.4, 100.3], [6.5, 100.3]];
export const E03Neta: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`NETA · PONAD 25${NB}TYS. AUT W TAJLANDII`} lugares={[
    { nome: "Tajlandia · ponad 25 tys. aut", lat: 13.75, lon: 100.5, cue: "tajlandii", esquerda: true },
    { nome: "Magazyn części · importer", lat: 13.08, lon: 100.9, cue: "importer", abaixo: true },
  ]} linhas={[{ pontos: TAJLANDIA }, { pontos: MALEZJA }]} tint={colors.accent} />
);

// 4. Mustang Mach-E — a 1ª ação, junho de 2022 (p34)
export const E04MachE: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ford Mustang Mach-E · czerwiec 2022", titulo: "Pierwsza akcja serwisowa", linhas: [
    { rotulo: "Samochody z wadą styczników", valor: `ok. 49${NB}tys.`, cue: "49", destaque: true },
    { rotulo: "Fabryka", valor: "Cuautitlán · Meksyk", cue: "cuautit|meksyk" },
  ], tint: "accent" }} />
);

// 5. Jaguar I-Pace — o recompra nos EUA (p45)
export const E05IPace: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="JAGUAR LAND ROVER · SKUP I-PACE Z ROCZNIKA 2019 · USA" valor={2760} cue="2760" sep=" "
    nota={{ texto: `decyzja: 11${NB}listopada 2024`, cue: "11" }} />
);

// 6. Kia/Hyundai — garantia estendida na Alemanha (p56)
export const E06Gwarancja: React.FC<SceneProps> = (p) => (
  <Documento {...p} linhas={[
    `ELECTRIVE · 17${NB}KWIETNIA 2026`, "", "Hyundai i Kia · Niemcy", "przedłużona gwarancja na ICCU", `15${NB}lat od rejestracji`,
    `albo 300${NB}000${NB}km`, "", "Wcześniej: Finlandia"]} cue="17" chave={4}
    carimbo={{ texto: "TO NIE AKCJA SERWISOWA", cue: "15" }} />
);

// 7. Ioniq 5 e 6 — o que a garantia alemã cobre (p66)
export const E07Ioniq: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hyundai · gwarancja na ICCU · Niemcy", titulo: "Które auta obejmuje", linhas: [
    { rotulo: "Ioniq 5", valor: "do kwietnia 2024", cue: "5" },
    { rotulo: "Ioniq 6", valor: "do września 2024", cue: "6", destaque: true },
  ], tint: "cool" }} />
);
