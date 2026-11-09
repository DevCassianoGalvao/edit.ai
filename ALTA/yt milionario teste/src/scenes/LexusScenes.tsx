// Animações de "Lexus Rzuca BOMBĘ — Elektryczne LFA Może Zagrozić BMW" (pl, enxuto) — painel 20261102-110333 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Wymiary konceptu (p07)
export const L01Wymiary: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Lexus LFA · koncept elektryczny", titulo: "Wymiary", linhas: [
    { rotulo: "Długość", valor: `ok.${NB}4,69${NB}m`, cue: "69" },
    { rotulo: "Szerokość", valor: `ok.${NB}2,04${NB}m`, cue: "2" },
    { rotulo: "Wysokość", valor: `ok.${NB}1,19${NB}m`, cue: "19", destaque: true },
  ], tint: "cool" }} />
);

// 2. MAPA: dokąd odchodzą klienci (p12)
export const L02Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="KLIENCI PREMIUM · MONACHIUM CZY SZANGHAJ" lugares={[
    { nome: "Monachium", lat: 48.14, lon: 11.58, cue: "monachium", esquerda: true },
    { nome: "Szanghaj", lat: 31.23, lon: 121.47, cue: "szanghaj", esquerda: true, abaixo: true },
  ]} tint={colors.accent} />
);

// 3. Heritage Edition (p18)
export const L03Heritage: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Lexus LS · Heritage Edition · USA", titulo: "Pożegnalna seria", linhas: [
    { rotulo: "Egzemplarzy", valor: "250", cue: "250" },
    { rotulo: "Cena od", valor: `99${NB}280${NB}$`, cue: "99", destaque: true },
    { rotulo: "z dostawą", valor: `+${NB}280${NB}$`, cue: "280" },
  ], tint: "danger" }} />
);

// 4. Baterie stałe: cele, nie wyniki (p33)
export const L04Zasieg: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TOYOTA · BATERIE ZE STAŁYM ELEKTROLITEM · CEL" valor={1000} sufixo={`${NB}km`} sep=" "
    cue="1000" nota={{ texto: `ładowanie ok.${NB}10${NB}minut · niektóre źródła: 1${NB}200${NB}km`, cue: "10" }} />
);

// 5. BMW iX3 Neue Klasse (p47)
export const L05iX3: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BMW iX3 50 xDrive · Neue Klasse", titulo: "Liczby z salonu", linhas: [
    { rotulo: "Bateria", valor: `108${NB}kWh`, cue: "108" },
    { rotulo: "Zasięg WLTP", valor: `805${NB}km`, cue: "805", destaque: true },
    { rotulo: "Moc ładowania", valor: `400${NB}kW`, cue: "400" },
  ], tint: "accent" }} />
);

// 6. Zasięg: obietnica vs BMW dziś (p55)
export const L06Podroz: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Ile zasięgu naprawdę potrzebujesz" titulo="Zasięg: obietnica i salon"
    tint={colors.accent} max={1000} barras={[
    { rotulo: "Obietnica Toyoty", valor: `1${NB}000${NB}km`, v: 1000, cue: "1000" },
    { rotulo: "BMW iX3 dziś", valor: `ok.${NB}800${NB}km`, v: 800, cue: "800", cor: colors.danger },
  ]} />
);
