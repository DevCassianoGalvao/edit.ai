// As animações de "Mazda Rzuca BOMBĘ — Nowy Silnik Skyactiv-Z" (pl) — painel 20261024-114529 (baia b1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. a norma Euro 7 (p05)
export const M01Euro7: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Unia Europejska · norma Euro 7", titulo: "Euro 7", linhas: [
    { rotulo: "Rozporządzenie UE", valor: "2024/1257", cue: "1257" },
    { rotulo: "Nowe typy aut osobowych", valor: `od 29${NB}listopada 2026`, cue: "29", destaque: true },
  ], tint: "danger" }} />
);

// 2. Skyactiv-X na Europa em 2019 (p14)
export const M02SkyactivX: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Skyactiv-X · Europa · 2019", titulo: "Udział w zamówieniach", linhas: [
    { rotulo: "Mazda 3", valor: `60${NB}%`, cue: "60", destaque: true },
    { rotulo: "Mazda CX-30", valor: `45${NB}%`, cue: "45" },
  ], tint: "accent" }} />
);

// 3. o que se sabe do Skyactiv-Z (p25)
export const M03SkyactivZ: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Skyactiv-Z · zdjęcia z testów", titulo: "Co już wiemy", linhas: [
    { rotulo: "Cztery cylindry · pojemność", valor: `2,5${NB}l`, cue: "2", destaque: true },
    { rotulo: "Skyactiv-G · stopień sprężania", valor: `do 14:1`, cue: "14" },
  ], tint: "cool" }} />
);

// 4. o corte do investimento em elétricos (p37)
export const M04Jeny: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mazda · elektryfikacja · marzec 2025", titulo: "Cięcie inwestycji", linhas: [
    { rotulo: "Plan wcześniej", valor: `2${NB}biliony jenów`, cue: "2" },
    { rotulo: "Po zmianie", valor: `1,5${NB}biliona jenów`, cue: "1" },
    { rotulo: "Różnica", valor: `500${NB}mld jenów`, cue: "500", destaque: true },
  ], tint: "danger" }} />
);

// 5. o pacote de 16/12/2025 (p46)
export const M05UE2035: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Komisja Europejska · 16 grudnia 2025", titulo: "Rok 2035", linhas: [
    { rotulo: "Redukcja CO₂ z rur wydechowych", valor: `90${NB}%`, cue: "90", destaque: true },
    { rotulo: "Rekompensata (stal, e-paliwa)", valor: `10${NB}%`, cue: "10" },
  ], tint: "cool" }} />
);

// 6. MAPA: as encomendas do novo CX-5 na Europa (p55)
export const M06Europa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`NOWA MAZDA CX-5 · 2500${NB}ZAMÓWIEŃ W POLSCE`} lugares={[
    { nome: "Polska · rekord Europy", lat: 52.23, lon: 21.01, cue: "rekord", esquerda: true },
    { nome: "Niemcy · drugie miejsce", lat: 51.0, lon: 10.4, cue: "niemcy", abaixo: true },
    { nome: "Hiszpania · trzecie miejsce", lat: 40.42, lon: -3.7, cue: "hiszpania" },
  ]} linhas={[
    { pontos: [[54.4, 14.2], [54.8, 18.3], [54.4, 19.6], [54.35, 22.8], [53.9, 23.5], [52.2, 23.2], [51.6, 23.6],
      [50.4, 24.1], [49.1, 22.6], [49.4, 19.4], [49.6, 18.8], [50.3, 17.7], [50.8, 16.0], [51.0, 14.9], [52.6, 14.6], [54.4, 14.2]] },
    { pontos: [[54.8, 8.7], [54.4, 11.0], [54.1, 13.8], [53.4, 14.4], [52.6, 14.6], [51.0, 14.9], [50.3, 12.1], [48.8, 13.8],
      [47.6, 13.0], [47.6, 10.2], [47.6, 7.6], [49.0, 8.2], [49.5, 6.4], [50.8, 6.0], [51.9, 6.8], [53.4, 7.2], [54.8, 8.7]] },
    { pontos: [[43.4, -8.9], [43.5, -3.8], [43.3, -1.8], [42.5, 3.2], [41.0, 0.9], [39.5, -0.3], [38.7, 0.2], [37.6, -0.7],
      [36.7, -4.4], [36.0, -5.6], [37.2, -7.4], [38.2, -7.0], [39.7, -7.5], [42.0, -8.9], [43.4, -8.9]] },
    { pontos: [[43.3, -1.8], [46.2, -1.2], [47.3, -2.5], [48.6, -4.6], [48.8, -1.6], [49.7, 0.2], [51.0, 2.5], [51.9, 4.0], [53.4, 7.2]] },
    { pontos: [[42.5, 3.2], [43.3, 5.4], [43.7, 7.4], [44.4, 8.9]] },
  ]} tint={colors.accent} />
);
