// Animações de "Mercedes Odpala Silnik Osiowy YASA z Berlina" (pl, enxuto) — painel 20261021-100641 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Fabryka Yasy w Yarnton (p07)
export const Y01Yarnton: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "YASA · Yarnton pod Oksfordem", titulo: "Fabryka silników osiowych", linhas: [
    { rotulo: "Otwarcie", valor: "13 maja 2025", cue: "13" },
    { rotulo: "Koszt", valor: `ok.${NB}12${NB}mln${NB}£`, cue: "12" },
    { rotulo: "Silników rocznie", valor: `ponad 25${NB}000`, cue: "25", destaque: true },
  ], tint: "cool" }} />
);

// 2. Rekord prototypu, lipiec 2025 (p19)
export const Y02Rekord: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "YASA · prototyp · lipiec 2025", titulo: "Rekord mocy", linhas: [
    { rotulo: "Masa", valor: `13,1${NB}kg`, cue: "13" },
    { rotulo: "Moc szczytowa", valor: `550${NB}kW`, cue: "550" },
    { rotulo: "Na kilogram", valor: `ok.${NB}42${NB}kW`, cue: "42", destaque: true },
  ], tint: "danger" }} />
);

// 3. Marienfelde: 98 etapów (p28)
export const Y03Fabryka: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Berlin-Marienfelde · jeden silnik", titulo: "Proces produkcji", linhas: [
    { rotulo: "Etapy procesu", valor: "98", cue: "98" },
    { rotulo: "Nowe dla Mercedesa", valor: "65", cue: "65" },
    { rotulo: "Nowe dla świata", valor: "35", cue: "35", destaque: true },
  ], tint: "accent" }} />
);

// 4. MAPA: silniki z Berlina, auta z Sindelfingen (p36)
export const Y04Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="AMG GT · ELEKTRYCZNE COUPÉ" lugares={[
    { nome: "Sindelfingen · samochody", lat: 48.71, lon: 9.0, cue: "sindelfingen", abaixo: true },
    { nome: "Berlin · silniki", lat: 52.42, lon: 13.37, cue: "berlina" },
  ]} linhas={[{ pontos: [[54.8, 8.6], [54.4, 11.0], [54.1, 13.8], [53.4, 14.4], [52.4, 14.6], [51.1, 15.0], [50.3, 12.2],
    [49.0, 13.8], [47.6, 13.0], [47.5, 10.2], [47.6, 7.6], [49.0, 8.2], [49.5, 6.4], [50.8, 6.0], [51.9, 6.8], [53.3, 7.2],
    [53.6, 8.5], [54.8, 8.6]] }]} tint={colors.accent} />
);

// 5. Bateria i ładowanie (p41)
export const Y05Ladowanie: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "AMG GT · ładowanie prądem stałym", titulo: "Ładowanie", linhas: [
    { rotulo: "Moc ładowania", valor: `ponad 600${NB}kW`, cue: "600", destaque: true },
    { rotulo: `10${NB}minut`, valor: `ok.${NB}460${NB}km`, cue: "460" },
    { rotulo: `10→80${NB}%`, valor: `11${NB}minut`, cue: "80" },
  ], tint: "cool" }} />
);

// 6. Nardò: długość równika (p46)
export const Y06Nardo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CONCEPT AMG GT XX · NARDÒ, SIERPIEŃ 2025" valor={40075} sufixo={`${NB}km`} sep=" "
    cue="40" nota={{ texto: `7 dni i 13 godzin · ok.${NB}300${NB}km/h`, cue: "7" }} />
);

// 7. Chiny: Pan-Good Power (p55)
export const Y07Chiny: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pan-Good Power · Lanxi, Zhejiang", titulo: "Silniki osiowe w Chinach", linhas: [
    { rotulo: "Linie produkcyjne", valor: "5", cue: "pięć|5" },
    { rotulo: "Silników rocznie", valor: `300${NB}000`, cue: "300", destaque: true },
    { rotulo: "Uzysk produkcji", valor: `ponad 98${NB}%`, cue: "uzysk" },
  ], tint: "danger" }} />
);

// 8. Ceny w Polsce (p62)
export const Y08Ceny: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Polska · według Auto Świata" titulo="Ile kosztuje AMG GT"
    tint={colors.accent} max={839000} barras={[
    { rotulo: "GT 55", valor: `ok.${NB}676${NB}tys.${NB}zł`, v: 676000, cue: "676" },
    { rotulo: "GT 63", valor: `ok.${NB}839${NB}tys.${NB}zł`, v: 839000, cue: "839", cor: colors.danger },
  ]} />
);

// 9. Bilans silnika (p68)
export const Y09Bilans: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Silnik osiowy · według Mercedesa", titulo: "Bilans", linhas: [
    { rotulo: "Miejsce i masa", valor: "1/3", cue: "1" },
    { rotulo: "Gęstość mocy", valor: "× 3", cue: "3" },
    { rotulo: "Trzy silniki GT 63", valor: `860${NB}kW`, cue: "860", destaque: true },
  ], tint: "accent" }} />
);
