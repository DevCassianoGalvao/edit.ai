// Animações de "Volvo Traci Wszystko — 3000 Zwolnień i Miliardowy Odpis" (pl, enxuto) — painel 20261027-233458 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { LinhaDoTempo } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Druga fala zwolnień (p00)
export const V01Fala: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Volvo Cars · zwolnienia", titulo: "Dwie fale cięć", linhas: [
    { rotulo: "Ogłoszenie", valor: `23${NB}października 2026`, cue: "23" },
    { rotulo: "Druga fala", valor: `2${NB}500 osób`, cue: "2", destaque: true },
    { rotulo: "Rok wcześniej", valor: `3${NB}000 osób`, cue: "3" },
  ], tint: "danger" }} />
);

// 2. Nowy cel na 2030 (p12)
export const V02Cel: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Volvo · wrzesień 2024 · cel na 2030", titulo: "Nowy plan sprzedaży", linhas: [
    { rotulo: "Elektryczne i plug-in, od", valor: `90${NB}%`, cue: "90" },
    { rotulo: "Elektryczne i plug-in, do", valor: `100${NB}%`, cue: "100", destaque: true },
    { rotulo: "Łagodne hybrydy", valor: `do 10${NB}%`, cue: "10" },
  ], tint: "accent" }} />
);

// 3. Maj 2025: 3000 osób (p19)
export const V03Maj: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VOLVO CARS · KONIEC MAJA 2025 · ZWOLNIENIA" valor={3000} sufixo={`${NB}osób`} cue="3" sep=" "
    nota={{ texto: `ok. 15${NB}% pracowników biurowych`, cue: "15" }} />
);

// 4. Odpis (p28)
export const V04Odpis: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Volvo · odpis z lipca 2025", titulo: "Gdzie poszedł odpis", linhas: [
    { rotulo: "Odpis łącznie", valor: `11,4${NB}mld SEK`, cue: "11", destaque: true },
    { rotulo: "Koszt sprzedaży", valor: `ok. 4${NB}mld SEK`, cue: "4" },
  ], nota: "Reszta obciążyła badania i rozwój", tint: "danger" }} />
);

// 5. Wynik roku 2025 (p44)
export const V05Wynik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Volvo Cars · cały rok 2025", titulo: "Wynik roku", linhas: [
    { rotulo: "Strata netto", valor: `4${NB}mld SEK`, cue: "4" },
    { rotulo: "Spadek przychodów", valor: `−11${NB}%`, cue: "11" },
    { rotulo: "Przychody", valor: `357${NB}mld SEK`, cue: "357" },
    { rotulo: "Zysk operacyjny", valor: `−98${NB}%`, cue: "98", destaque: true },
  ], tint: "danger" }} />
);

// 6. Razem 5500 (p56)
export const V06Razem: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VOLVO CARS · DWIE FALE ZWOLNIEŃ RAZEM" valor={5500} prefixo="ok. " sufixo={`${NB}osób`} cue="5" sep=" "
    nota={{ texto: `2${NB}500 teraz + 3${NB}000 rok wcześniej`, cue: "5" }} />
);

// 7. MAPA: gdzie Volvo buduje samochody (p77)
export const V07Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FABRYKI VOLVO CARS" lugares={[
    { nome: "Torslanda · Szwecja", lat: 57.72, lon: 11.89, cue: "Szwecji" },
    { nome: "Chiny", lat: 30.6, lon: 104.1, cue: "Chinach" },
    { nome: "Charleston · USA", lat: 33.1, lon: -80.2, cue: "Charleston", esquerda: true },
  ]} tint={colors.accent} />
);

// 8. Oś czasu (p89) — só o que cabe na janela de 14 s do parágrafo
export const V08Os: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="VOLVO · OŚ CZASU OBIETNICY" tint={colors.accent} marcos={[
    { ano: "2021", texto: "obietnica: 100 % elektryków", cue: "2021" },
    { ano: "2030", texto: "termin obietnicy", cue: "2030" },
    { ano: "Northvolt", texto: "fabryka baterii dla pół miliona aut", cue: "northvolt", cor: colors.danger },
  ]} />
);
