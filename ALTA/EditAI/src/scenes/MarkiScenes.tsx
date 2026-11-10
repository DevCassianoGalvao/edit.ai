// As 8 animações de "10 Nowych Aut, Których w Polsce Nikt Nie Chce w 2026" (pl, 25,7 min) — painel 20261104-011341 (baia b1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é DITO (Samar, I–IX 2026).
// Tipos: Odometro (2), Barras (3), Painel (2), MapaRota (1).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. O mercado inteiro cresce (p02)
export const M01Rynek: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="NOWE AUTA OSOBOWE · POLSKA · STYCZEŃ–WRZESIEŃ 2026" valor={470520} cue="470" sep=" "
    nota={{ texto: `ok. +10${NB}% rok do roku · sam wrzesień: 56${NB}357 aut`, cue: "56" }} />
);

// 2. Tropeços no topo em agosto (p05)
export const M02Sierpien: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Sierpień 2026 · spadki nawet w czołówce" titulo="Jeden miesiąc to za mało" tint={colors.danger} max={65}
    barras={[
      { rotulo: "Hyundai Tucson", valor: `−59,8${NB}%`, v: 59.8, cue: "59", cor: colors.danger },
      { rotulo: "Toyota Yaris Cross", valor: `−29${NB}%`, v: 29, cue: "29" },
      { rotulo: "MG HS", valor: `−20${NB}%`, v: 20, cue: "20" },
    ]} />
);

// 3. Nº 8 Suzuki (p15)
export const M03Suzuki: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Numer 8 · Suzuki · rejestracje w Polsce", titulo: "Suzuki traci klientów", linhas: [
    { rotulo: "Styczeń–wrzesień", valor: `−13${NB}%`, cue: "13", destaque: true },
    { rotulo: "Sierpień", valor: `−33,8${NB}%`, cue: "33" },
    { rotulo: "Wrzesień", valor: `−15,5${NB}%`, cue: "15" },
  ], tint: "danger" }} />
);

// 4. Nº 5 Seat (p27)
export const M04Seat: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Numer 5 · Seat · spadek rejestracji" titulo="Spada po cichu" tint={colors.danger} max={32}
    barras={[
      { rotulo: "Styczeń–wrzesień", valor: `−21,6${NB}%`, v: 21.6, cue: "21", cor: colors.danger },
      { rotulo: "Pierwsze półrocze", valor: `−19,7${NB}%`, v: 19.7, cue: "19" },
      { rotulo: "Styczeń–sierpień", valor: `−22,6${NB}%`, v: 22.6, cue: "22" },
      { rotulo: "Sam sierpień", valor: `−28${NB}%`, v: 28, cue: "28" },
    ]} />
);

// 5. Nº 3 Subaru (p36)
export const M05Subaru: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Numer 3 · Subaru · rejestracje w Polsce", titulo: "Dwa miesiące załamania", linhas: [
    { rotulo: "Styczeń–wrzesień", valor: `−25,9${NB}%`, cue: "25" },
    { rotulo: "Sierpień", valor: `−70,9${NB}%`, cue: "70", destaque: true },
    { rotulo: "Wrzesień", valor: `−53,6${NB}%`, cue: "53" },
  ], tint: "danger" }} />
);

// 6. Nº 1 Mitsubishi (p46)
export const M06Mitsubishi: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Numer 1 · Mitsubishi · krok po kroku" titulo="Marka, która topnieje" tint={colors.danger} max={65}
    barras={[
      { rotulo: "Pierwsze półrocze", valor: `−22,1${NB}%`, v: 22.1, cue: "22" },
      { rotulo: "Styczeń–sierpień", valor: `−33,1${NB}%`, v: 33.1, cue: "33" },
      { rotulo: "Sam sierpień", valor: `−61${NB}%`, v: 61, cue: "61", cor: colors.danger },
      { rotulo: "Wrzesień", valor: `−49${NB}%`, v: 49, cue: "49" },
    ]} />
);

// 7. MAPA: japońscy i koreańscy outsiderzy (p53)
const HONSIU: [number, number][] = [[41.5, 140.0], [40.5, 141.5], [39.0, 141.9], [37.8, 141.0], [36.9, 140.8], [35.7, 140.9],
  [35.0, 139.9], [34.6, 138.9], [34.7, 137.6], [34.3, 136.9], [33.5, 135.8], [34.3, 135.1], [34.6, 134.0], [34.0, 132.3],
  [34.3, 131.0], [35.4, 132.6], [35.6, 134.5], [35.7, 135.9], [36.6, 136.6], [37.4, 136.8], [37.0, 137.3], [37.8, 138.8],
  [38.5, 139.6], [39.6, 140.0], [40.6, 139.9], [41.5, 140.0]];
const KIUSIU: [number, number][] = [[34.0, 130.9], [33.0, 129.6], [31.4, 130.2], [31.0, 131.2], [32.0, 131.6], [33.5, 131.7], [34.0, 130.9]];
const SIKOKU: [number, number][] = [[34.3, 133.0], [34.2, 134.6], [33.6, 134.4], [32.8, 132.8], [33.5, 132.4], [34.3, 133.0]];
const HOKKAIDO: [number, number][] = [[41.6, 140.1], [42.6, 139.9], [43.4, 141.4], [45.5, 141.9], [44.0, 144.5], [43.3, 145.6],
  [42.0, 143.3], [42.3, 140.8], [41.6, 140.1]];
const KOREA: [number, number][] = [[37.7, 126.1], [38.2, 124.9], [39.8, 124.4], [41.0, 126.9], [42.4, 130.6], [41.0, 129.7],
  [39.9, 127.9], [38.5, 128.4], [37.0, 129.4], [35.2, 129.2], [34.7, 128.0], [34.5, 126.4], [35.1, 126.1], [36.4, 126.5], [37.7, 126.1]];
export const M07Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="JAPOŃSCY I KOREAŃSCY OUTSIDERZY" lugares={[
    { nome: "Mitsubishi", lat: 34.52, lon: 133.74, cue: "mitsubishi", abaixo: true, esquerda: true },
    { nome: "Subaru", lat: 36.29, lon: 139.38, cue: "subaru" },
    { nome: "Suzuki", lat: 34.71, lon: 137.73, cue: "suzuki" },
    { nome: "KGM", lat: 36.99, lon: 127.11, cue: "kgm", esquerda: true },
  ]} linhas={[{ pontos: HONSIU }, { pontos: KIUSIU }, { pontos: SIKOKU }, { pontos: HOKKAIDO }, { pontos: KOREA }]}
    tint={colors.accent} />
);

// 8. Fecho: o mercado depois de outubro (p73)
export const M08Koniec: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="POLSKA · REJESTRACJE PO PAŹDZIERNIKU · RAZEM Z DOSTAWCZYMI" valor={526} sufixo=" tys." cue="526" sep=" "
    nota={{ texto: `po 9 miesiącach: prawie 470${NB}tys. aut osobowych`, cue: "526" }} />
);
