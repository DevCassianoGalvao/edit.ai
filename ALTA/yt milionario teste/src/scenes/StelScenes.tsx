// As animações de "Stellantis Traci Wszystko: Jeep, Dodge i Fiat na Krawędzi Upadku" (pl, arquivo dark) — painel
// 20261008-113639 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito;
// separador de milhar = espaço (pl), decimal com vírgula.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o lucro recorde de 2023 (p01)
export const S01Rekord: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · wyniki za 2023", titulo: "Rekord w historii grupy", linhas: [
    { rotulo: "Zysk netto", valor: `18,6${NB}mld${NB}€`, cue: "18", destaque: true },
    { rotulo: "Wzrost rok do roku", valor: `+11${NB}%`, cue: "11" },
    { rotulo: "Dywidendy i skup akcji", valor: `ok. 7,7${NB}mld${NB}€`, cue: "7" },
  ], tint: "accent" }} />
);

// 2. a venda do Jeep nos EUA (p08)
export const S02Jeep: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Jeep · sprzedaż w USA" titulo={`Spadek o 34${NB}%`} tint={colors.accent} max={973} barras={[
    { rotulo: "2018", valor: `973${NB}tys.`, v: 973, cue: "973", cor: colors.textDim },
    { rotulo: "2023", valor: `643${NB}tys.`, v: 643, cue: "643" },
  ]} />
);

// 3. resultados de 2024 (p23)
export const S03Wyniki2024: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · wyniki za 2024", titulo: "Zysk topnieje", linhas: [
    { rotulo: "Zysk netto", valor: `5,5${NB}mld${NB}€`, cue: "5" },
    { rotulo: "Rok do roku", valor: `−70${NB}%`, cue: "70", destaque: true },
    { rotulo: "Przychody (−17 %)", valor: `156,9${NB}mld${NB}€`, cue: "156" },
  ], tint: "accent" }} />
);

// 4. o Charger elétrico depois do fim do crédito fiscal (p29)
export const S04Charger: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="Dodge Charger Daytona EV · USA · styczeń 2026" valor={80} cue="80" sep=" "
    sufixo={`${NB}sztuk`} nota={{ texto: `koniec ulgi podatkowej 7${NB}500${NB}$ · 30 września 2025`, cue: "7500" }} />
);

// 5. o prejuízo de 2025 (p41)
export const S05Strata: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · wyniki za 2025", titulo: "Pierwsza roczna strata od fuzji", linhas: [
    { rotulo: "Strata netto", valor: `−22,3${NB}mld${NB}€`, cue: "22", destaque: true },
    { rotulo: "Koszty nadzwyczajne", valor: `25,4${NB}mld${NB}€`, cue: "25" },
    { rotulo: "Przychody", valor: `153,5${NB}mld${NB}€`, cue: "153" },
  ], tint: "accent" }} />
);

// 6. a volta ao lucro em 2026 (p47)
export const S06Powrot: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · pierwsze półrocze 2026", titulo: "Oddech, ale do brzegu daleko", linhas: [
    { rotulo: "Ameryka Północna, II kwartał", valor: `+32${NB}%`, cue: "32" },
    { rotulo: "Zysk netto, II kwartał", valor: `ok. 300${NB}mln${NB}€`, cue: "300" },
    { rotulo: "Zysk netto, półrocze", valor: `670${NB}mln${NB}€`, cue: "670", destaque: true },
    { rotulo: "Dostępna płynność", valor: `44,1${NB}mld${NB}€`, cue: "44" },
  ], tint: "cool" }} />
);

// 7. MAPA: carros chineses nas fábricas europeias da Stellantis (p51)
export const S07Europa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Chińskie auta w europejskich zakładach Stellantisa" lugares={[
    { nome: "Saragossa · Hiszpania", lat: 41.65, lon: -0.88, cue: "saragos" },
    { nome: "Madryt · Hiszpania", lat: 40.42, lon: -3.70, cue: "madryt|madryc", abaixo: true },
    { nome: "Rennes · Francja", lat: 48.11, lon: -1.68, cue: "rennes|renn" },
  ]} tint={colors.accent} />
);

// 8. MAPA: Stellantis na Polônia (p62)
export const S08Polska: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Stellantis w Polsce · Śląsk" lugares={[
    { nome: "Bielsko-Biała · zakład silników zamknięty", lat: 49.82, lon: 19.04, cue: "bielsk", abaixo: true },
    { nome: "Tychy", lat: 50.12, lon: 18.99, cue: "tych" },
    { nome: "Gliwice · auta dostawcze", lat: 50.29, lon: 18.67, cue: "gliwic" },
  ]} tint={colors.accent} />
);

// 9. o balanço final (p73)
export const S09Bilans: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Stellantis · luty 2024", titulo: "Od szczytu do rachunku", linhas: [
    { rotulo: "Rekordowy zysk", valor: `18,6${NB}mld${NB}€`, cue: "18" },
    { rotulo: "Wynagrodzenie prezesa", valor: `36,5${NB}mln${NB}€`, cue: "36", destaque: true },
  ], tint: "accent" }} />
);
