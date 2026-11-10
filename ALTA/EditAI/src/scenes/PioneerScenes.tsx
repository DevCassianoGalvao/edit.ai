// As animações de "Największy na świecie statek 382 m: Jak Pioneering Spirit podnosi 48 000 ton bez dźwigu?"
// (pl, arquivo dark) — painel 20261009-094435 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO;
// todo número é dito. Separador de milhar polonês = NBSP; cues sem "ł".
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. a escala (p02)
export const P01Skala: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "PIONEERING SPIRIT · ALLSEAS", titulo: "Największa jednostka do pracy na morzu", linhas: [
    { rotulo: "Długość", valor: `382${NB}metry`, cue: "382", destaque: true },
    { rotulo: "Szerokość", valor: `124${NB}metry`, cue: "124" },
    { rotulo: "Pojemność brutto", valor: `403${NB}342${NB}jednostki`, cue: "403" },
  ], tint: "cool" }} />
);

// 2. nove segundos (p16)
export const P02Sekundy: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SZYBKIE PODNIESIENIE · BALAST + CYLINDRY" valor={9} cue="9" sep={NB} sufixo={`${NB}sekund`}
    nota={{ texto: "tyle trwało oderwanie pokładu od nóg przy jednej z operacji", cue: "szybkim" }} />
);

// 3. recorde do tubo (p26)
export const P03Rura: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "TURKSTREAM · MORZE CZARNE · 26 SIERPNIA 2018", titulo: "Rekord jednej doby", linhas: [
    { rotulo: "Rura ułożona w ciągu jednej doby", valor: `6${NB}km i 270${NB}m`, cue: "6", destaque: true },
    { rotulo: "Wcześniejsza średnia", valor: `około 4${NB}km dziennie`, cue: "4" },
  ], tint: "accent" }} />
);

// 4. MAPA: Brent Delta -> Teesside (p34)
export const P04Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="BRENT DELTA · W JEDNYM KAWAŁKU DO PORTU" lugares={[
    { nome: "Brent Delta · Morze Północne", lat: 61.05, lon: 1.72, cue: "dalej" },
    { nome: "Teesside · Anglia", lat: 54.63, lon: -1.18, cue: "teesside", abaixo: true },
  ]} tint={colors.cool} />
);

// 5. o limite de projeto (p44)
export const P05Limit: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SYSTEM PODNOSZENIA POKŁADÓW · WIELKOŚĆ PROJEKTOWA" valor={48000} cue="48" sep={NB} sufixo={`${NB}ton`}
    nota={{ texto: `rekord w praktyce: 31${NB}000 ton`, cue: "31" }} />
);

// 6. os recordes lado a lado (p58)
export const P06Rekordy: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="REKORDY PIONEERING SPIRIT" titulo="Granica przesuwa się w górę" tint={colors.accent} max={31000}
    barras={[
      { rotulo: "Yme · 2016", valor: `około 13${NB}400 t`, v: 13400, cue: "13400", cor: colors.textDim },
      { rotulo: "Brent Delta · 2017", valor: `24${NB}200 t`, v: 24200, cue: "24200" },
      { rotulo: "Brent Bravo · 2019", valor: `25${NB}000 t`, v: 25000, cue: "25" },
      { rotulo: "Brent Charlie · 2024", valor: `31${NB}000 t`, v: 31000, cue: "31", cor: colors.danger },
    ]} />
);

// 7. as nove etapas (p68)
export const P07Etapy: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="etap" chave={7} linhas={[
    "ALLSEAS — PROCEDURA PODNIESIENIA POKŁADU",
    "1. Przygotowanie platformy",
    "2. Odłączenie od świata",
    "3. Wzmocnienia i punkty podparcia",
    "4. Dopłynięcie",
    "5. Ustawienie belek",
    "6. Napięcie",
    "7. Właściwe podniesienie",
    "8. Transport do portu",
    "9. Złożenie pokładu na nabrzeżu",
  ]} carimbo={{ texto: "OKNO POGODOWE", cue: "pogod" }} />
);

// 8. os números para lembrar (p75)
export const P08Liczby: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "WYSTARCZY ZAPAMIĘTAĆ", titulo: "Pioneering Spirit w liczbach", linhas: [
    { rotulo: "Szczelina na dziobie", valor: `122${NB}×${NB}59${NB}m`, cue: "122" },
    { rotulo: "Podnoszenie pokładów", valor: `48${NB}000 ton`, cue: "48", destaque: true },
    { rotulo: "Podnoszenie podstaw", valor: `25${NB}000 ton`, cue: "25" },
    { rotulo: "Rekord", valor: `31${NB}000 ton`, cue: "31" },
  ], tint: "cool" }} />
);
