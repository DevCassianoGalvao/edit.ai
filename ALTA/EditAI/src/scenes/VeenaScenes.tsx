// Animações de "Australia's New Invention Turns Old Mattresses and Glass Into Tiles" (en, arquivo dark) —
// painel 20261010-104926 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. colchões no aterro (p01)
export const V01Colchoes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="AUSTRALIA · MATTRESSES EVERY YEAR" valor={740000} cue="740" sep=","
    prefixo={`more than${NB}`} sufixo=""
    nota={{ texto: `still buried in landfill · of about 1.8${NB}million thrown away`, cue: "buried" }} />
);

// 2. Índia -> Canadá -> Austrália (p08)
export const V02Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="VEENA SAHAJWALLA · THE ROAD TO SYDNEY" lugares={[
    { nome: "Mumbai · India", lat: 19.08, lon: 72.88, cue: "after", abaixo: true },
    { nome: "Vancouver · Canada", lat: 49.26, lon: -123.25, cue: "moved" },
    { nome: "Sydney", lat: -33.92, lon: 151.23, cue: "australia", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. green steel (p18)
export const V03Pneus: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Green steel · Polymer Injection Technology", titulo: "Old tyres instead of coal", linhas: [
    { rotulo: "Tyres used · by March 2012", valor: `more than 1${NB}million`, cue: "one" },
    { rotulo: "Kept out of landfill · by October 2014", valor: `more than 2${NB}million`, cue: "2", destaque: true },
  ], tint: "cool" }} />
);

// 4. a primeira microfábrica (p27)
export const V04Micro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "UNSW Sydney · the first microfactory", titulo: "A factory on a tiny site", linhas: [
    { rotulo: "Launched", valor: "4 April 2018", cue: "university" },
    { rotulo: "The whole facility", valor: `just 50${NB}m²`, cue: "50", destaque: true },
  ], tint: "accent" }} />
);

// 5. colchões no depósito de West Nowra (p46)
export const V05Nowra: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="WEST NOWRA DEPOT · DISCARDED MATTRESSES" valor={12000} cue="12" sep=","
    prefixo={`around${NB}`} sufixo={`${NB}a year`}
    nota={{ texto: "shredded into fluff · mixed with glass sand", cue: "shred" }} />
);

// 6. a proibição da pedra engenheirada (p55)
export const V06Proibicao: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="july" linhas={[
    "COMMONWEALTH OF AUSTRALIA · NATIONAL BAN",
    "",
    "From 1 July 2024:",
    "engineered stone benchtops, panels and slabs",
    "manufacture · supply · processing · installation",
    "illegal in every state and territory",
  ]} chave={5} carimbo={{ texto: "BANNED", cue: "banned" }} />
);

// 7. a escala honesta (p67)
export const V07Escala: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Waste per year", titulo: "One microfactory against the tip", linhas: [
    { rotulo: "Nowra microfactory", valor: `around 700${NB}tonnes`, cue: "700" },
    { rotulo: "Australia to landfill", valor: `roughly 67${NB}million tonnes`, cue: "67", destaque: true },
  ], tint: "accent" }} />
);

// 8. o caminho da invenção (p76)
export const V08Jornada: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FROM THE LAB TO THE FACTORY" lugares={[
    { nome: "UNSW · Sydney", lat: -33.92, lon: 151.23, cue: "university" },
    { nome: "Cootamundra", lat: -34.64, lon: 148.03, cue: "kutamundra" },
    { nome: "Nowra", lat: -34.88, lon: 150.6, cue: "nora", abaixo: true },
    { nome: "Brisbane", lat: -27.47, lon: 153.03, cue: "brisbane" },
  ]} tint={colors.cool} />
);
