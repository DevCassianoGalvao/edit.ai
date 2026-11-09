// Animações de "Tak Żyją Marynarze na Supertankowcu" (pl) — painel 20261014-001235 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com espaço (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. wymiary VLCC (p01)
export const T01Vlcc: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Typowy supertankowiec klasy VLCC", titulo: "Wymiary", linhas: [
    { rotulo: "Długość", valor: `330${NB}m`, cue: "330", destaque: true },
    { rotulo: "Szerokość", valor: `60${NB}m`, cue: "60" },
    { rotulo: "Zanurzenie", valor: `20,5${NB}m`, cue: "20" },
  ], tint: "accent" }} />
);

// 2. MAPA: z Zatoki Perskiej przez Malakkę do Chin (p04)
export const T02Malakka: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="KLASA MALAKKA · TRASA ROPY" lugares={[
    { nome: "Zatoka Perska", lat: 26.6, lon: 50.2, cue: "malakka", abaixo: true },
    { nome: "Cieśnina Malakka", lat: 2.5, lon: 101.3, cue: "sumatra", abaixo: true },
    { nome: "Chiny", lat: 29.9, lon: 121.6, cue: "tras", esquerda: true },
  ]} tint={colors.accent} />
);

// 3. konwencja MLC 2006 — odpoczynek (p16)
export const T03Odpoczynek: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Konwencja o pracy na morzu · 2006", titulo: "Minimum odpoczynku", linhas: [
    { rotulo: "W każdej dobie", valor: "10 godzin", cue: "10", destaque: true },
    { rotulo: "W każdym tygodniu", valor: "77 godzin", cue: "77" },
    { rotulo: "Podział", valor: "najwyżej 2 okresy", cue: "dwa" },
  ], tint: "accent" }} />
);

// 4. wytwornica wody słodkiej (p24)
export const T04Woda: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="WYTWORNICA WODY SŁODKIEJ · W PODCIŚNIENIU WODA MORSKA WRZE W" valor={40} cue="40"
    sufixo={`–60${NB}°C`} sep=" " nota={{ texto: "ciepło z wody chłodzącej silnik główny", cue: "60" }} />
);

// 5. tlen w zbiornikach (p30)
export const T05Tlen: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TLEN W ZBIORNIKACH ŁADUNKOWYCH · LIMIT IMO" valor={8} cue="8" prefixo="maks. " sufixo=" %" sep=" "
    barras={[{ rotulo: "Limit IMO (%)", v: 8, cue: "8", destaque: true }, { rotulo: "W praktyce (%)", v: 5, cue: "5" },
      { rotulo: "Powietrze (%)", v: 21, cue: "21" }]} />
);

// 6. pompy ładunkowe (p48)
export const T06Pompy: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ROZŁADUNEK · 3 POMPY PO 5 000 M³ NA GODZINĘ" valor={15000} cue="15000" sufixo={`${NB}m³/h`} sep=" "
    nota={{ texto: "każda pompa: 5 000 m³ ropy na godzinę", cue: "5000" }} />
);

// 7. ile trwa podróż (p51)
export const T07Rejsy: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Podróż supertankowca do Chin", titulo: "Dni na morzu", linhas: [
    { rotulo: "Z Ras Tanura (Arabia Saudyjska)", valor: "19 dni", cue: "19" },
    { rotulo: "Z Brazylii", valor: "37 dni", cue: "37" },
    { rotulo: "Z Zatoki Meksykańskiej", valor: "53 dni", cue: "53", destaque: true },
  ], tint: "accent" }} />
);

// 8. Betelgeuse 1979 (p68)
export const T08Betelgeuse: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Betelgeuse · Whiddy Island · 1979", titulo: "50 ofiar", linhas: [
    { rotulo: "Francuzi", valor: "42", cue: "42", destaque: true },
    { rotulo: "Irlandczycy", valor: "7", cue: "7" },
    { rotulo: "Anglik", valor: "1", cue: "1" },
  ], tint: "accent" }} />
);

// 9. wartość ładunku (p78)
export const T09Ladunek: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="PRAWIE 2 MILIONY BARYŁEK ROPY · ŁADUNEK WART" valor={100} cue="100" prefixo="ponad " sufixo=" mln USD" sep=" "
    nota={{ texto: "25 marynarzy · 3 tygodnie albo 2 miesiące na morzu", cue: "25" }} />
);
