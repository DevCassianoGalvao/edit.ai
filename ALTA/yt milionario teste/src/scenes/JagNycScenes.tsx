// Animações de "Jaguar ROZWALA cały rynek motoryzacyjny!" (pl) — painel 20261019-232219 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 14 s); todo número é dito; milhar com espaço, decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, LinhaDoTempo } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o fim dos modelos antigos (p02)
export const J01Modele: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="Jaguar · koniec starej gamy" tint={colors.accent} marcos={[
    { ano: "V 2024", texto: "koniec XE, XF i F-Type", cue: "maju" },
    { ano: "XII 2024", texto: "ostatnie I-Pace i E-Pace", cue: "grudniu" },
    { ano: "XI 2024", texto: "stop sprzedaży w Wielkiej Brytanii", cue: "listopadzie", cor: colors.accent },
  ]} />
);

// 2. MAPA: a premiere em Nova York (p10)
export const J02NowyJork: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Premiera Type 01 · Nowy Jork, 6 października" lugares={[
    { nome: "Times Square", lat: 40.758, lon: -73.9855, cue: "ekranach", abaixo: true },
    { nome: "Dumbo", lat: 40.7033, lon: -73.9881, cue: "dumbo", esquerda: true },
    { nome: "Lower East Side", lat: 40.715, lon: -73.9843, cue: "lower" },
    { nome: "West Chelsea · galeria Storied", lat: 40.7465, lon: -74.0055, cue: "galerii", esquerda: true },
  ]} tint={colors.accent} />
);

// 3. o Impossible Panel (p15)
export const J03Panel: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Impossible Panel · jedno tłoczenie", titulo: "Panel, którego nie dało się zrobić", linhas: [
    { rotulo: "Etapy formowania na zimno", valor: "6", cue: "sześciu|szesciu|6" },
    { rotulo: "Siła nacisku prasy", valor: `2${NB}500${NB}ton`, cue: "2", destaque: true },
    { rotulo: "Godziny pracy inżynierów", valor: `1${NB}500${NB}h`, cue: "1" },
  ], tint: "accent" }} />
);

// 4. potência (p22)
export const J04Moc: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jaguar Type 01 · trzy silniki elektryczne", titulo: "Najmocniejszy Jaguar drogowy", linhas: [
    { rotulo: "Moc", valor: `1${NB}015${NB}KM`, cue: "1015", destaque: true },
    { rotulo: "Moc metryczna", valor: `ok. 1${NB}030${NB}KM`, cue: "1030" },
    { rotulo: "Moment obrotowy", valor: `ok. 1${NB}300${NB}Nm`, cue: "1300" },
  ], tint: "accent" }} />
);

// 5. preço (p28)
export const J05Cena: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jaguar Type 01 · ceny wyjściowe", titulo: "Ile kosztuje nowy Jaguar", linhas: [
    { rotulo: "Stany Zjednoczone", valor: `130${NB}500${NB}$`, cue: "000" },
    { rotulo: "Wielka Brytania", valor: `130${NB}000${NB}£`, cue: "funtów|funtow", destaque: true },
    { rotulo: "Wersja Design Vision", valor: `145${NB}000${NB}£`, cue: "145" },
  ], tint: "accent" }} />
);

// 6. autonomia x rivais (p31)
export const J06Zasieg: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Zasięg w cyklu EPA · mile" titulo="Wąskie grono aut z 400 milami" tint={colors.accent} max={512} barras={[
    { rotulo: "Lucid Air Grand Touring", valor: `512${NB}mil`, v: 512, cue: "512", cor: colors.textDim },
    { rotulo: "Jaguar Type 01 (szacunek)", valor: `400${NB}mil`, v: 400, cue: "512" },
    { rotulo: "Mercedes EQS 450+", valor: `390${NB}mil`, v: 390, cue: "390", cor: colors.textDim },
  ]} />
);

// 7. o resumo (p40)
export const J07Bilans: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Type 01 · deklaracje producenta", titulo: "Najważniejsze liczby", linhas: [
    { rotulo: "Moc", valor: `ponad 1${NB}000${NB}KM`, cue: "1000", destaque: true },
    { rotulo: "0–100 km/h", valor: `3,2${NB}s`, cue: "3" },
    { rotulo: "Bateria", valor: `118${NB}kWh`, cue: "118" },
    { rotulo: "Zasięg EPA", valor: `do 400${NB}mil`, cue: "400" },
  ], tint: "accent" }} />
);
