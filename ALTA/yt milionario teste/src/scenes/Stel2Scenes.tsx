// Animações de "Stellantis Tonie: Jeep, Dodge i Fiat na Krawędzi" (pl, arquivo dark) — painel 20261011-140346 (baia 1).
// REGRA: biblioteca + MAPA; motion curto (cues <= 14 s); todo número é dito; milhar com espaço, decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. do recorde ao prejuízo (p00)
export const T01Rekord: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · dwa lata", titulo: "Od rekordu do przepaści", linhas: [
    { rotulo: "Zysk netto 2023", valor: `18,6${NB}mld${NB}€`, cue: "18" },
    { rotulo: "Strata netto 2025", valor: `−22,3${NB}mld${NB}€`, cue: "22", destaque: true },
  ], tint: "accent" }} />
);

// 2. o pacote do Tavares (p08)
export const T02Pensja: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Carlos Tavares · wynagrodzenie za 2023", titulo: `Razem do 36,5${NB}mln${NB}€`, linhas: [
    { rotulo: "Pensja podstawowa", valor: `2${NB}mln${NB}€`, cue: "2" },
    { rotulo: "Premia roczna", valor: `11,4${NB}mln${NB}€`, cue: "11" },
    { rotulo: "Bonus za transformację", valor: `10${NB}mln${NB}€`, cue: "10" },
    { rotulo: "Akcje (cele długoterminowe)", valor: `ok. 13${NB}mln${NB}€`, cue: "13", destaque: true },
  ], tint: "accent" }} />
);

// 3. dias de estoque (p18)
export const T03Zapasy: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Dni zapasu u dealerów · USA · 2024" titulo="Auta, których nikt nie kupuje" tint={colors.accent} max={131} barras={[
    { rotulo: "Średnia rynku", valor: `77${NB}dni`, v: 77, cue: "77", cor: colors.textDim },
    { rotulo: "Marki Stellantisa", valor: `ponad 100${NB}dni`, v: 100, cue: "100" },
    { rotulo: "Dodge", valor: `131${NB}dni`, v: 131, cue: "131" },
  ]} />
);

// 4. resultados de 2024 (p28)
export const T04Wyniki2024: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · wyniki za 2024", titulo: "Zysk topnieje", linhas: [
    { rotulo: "Przychody (−17 %)", valor: `156,9${NB}mld${NB}€`, cue: "156" },
    { rotulo: "Zysk netto rok do roku", valor: `−70${NB}%`, cue: "70", destaque: true },
    { rotulo: "Zysk netto", valor: `5,5${NB}mld${NB}€`, cue: "5" },
  ], tint: "accent" }} />
);

// 5. o Charger elétrico (p35)
export const T05Charger: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Dodge Charger · USA · III kwartał 2026" titulo={`Elektryk: −92${NB}%`} tint={colors.accent} max={3446} barras={[
    { rotulo: "Daytona EV", valor: `233${NB}szt.`, v: 233, cue: "233" },
    { rotulo: "Benzynowy, 6 cylindrów", valor: `3${NB}446${NB}szt.`, v: 3446, cue: "3446", cor: colors.textDim },
  ]} />
);

// 6. o investimento nos EUA (p42)
export const T06Inwestycja: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · inwestycje w USA", titulo: "Powrót do Ameryki", linhas: [
    { rotulo: "Belvidere, Illinois", valor: `ponad 600${NB}mln${NB}$`, cue: "600" },
    { rotulo: "Miejsca pracy w Belvidere", valor: `ok. 3${NB}300`, cue: "3300", destaque: true },
    { rotulo: "Toledo, Ohio", valor: `prawie 400${NB}mln${NB}$`, cue: "400" },
  ], tint: "cool" }} />
);

// 7. a conta de 2025 (p48)
export const T07Rachunek: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · wyniki za 2025", titulo: "Pierwsza roczna strata od fuzji", linhas: [
    { rotulo: "Koszty jednorazowe", valor: `25,4${NB}mld${NB}€`, cue: "25" },
    { rotulo: "Przychody", valor: `153,5${NB}mld${NB}€`, cue: "153" },
    { rotulo: "Skorygowany wynik operacyjny", valor: `−842${NB}mln${NB}€`, cue: "842", destaque: true },
  ], tint: "accent" }} />
);

// 8. MAPA: Detroit, Paris e Tychy (p56)
export const T08Polska: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Od Detroit i Paryża do Śląska" lugares={[
    { nome: "Paryż", lat: 48.86, lon: 2.35, cue: "paryż|paryz", abaixo: true },
    { nome: "Tychy · Śląsk", lat: 50.12, lon: 18.99, cue: "tych", esquerda: true },
  ]} tint={colors.accent} />
);

// 9. o balanço final (p70)
export const T09Bilans: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Od początku do końca", titulo: "Łańcuch decyzji", linhas: [
    { rotulo: "Wynagrodzenie prezesa", valor: `36,5${NB}mln${NB}€`, cue: "36" },
    { rotulo: "Ceny w USA", valor: `+50${NB}%`, cue: "50" },
    { rotulo: "Auta na placach", valor: `430${NB}tys.`, cue: "430", destaque: true },
  ], tint: "accent" }} />
);
