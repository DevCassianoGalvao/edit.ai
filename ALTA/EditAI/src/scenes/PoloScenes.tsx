// Animações de "Czterdziestka Ptolemeusza — życie 4000 wioślarzy" (pl, enxuto) — painel 20261019-234718-doc-polo
// (baia b1). REGRA: biblioteca + MAPA; motion curto (cues <= ~13 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { LinhaDoTempo } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: de onde vinha a madeira (p03)
export const P01Drewno: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DREWNO OKRĘTOWE · CEDR, SOSNA, JODŁA" lugares={[
    { nome: "Góry Libanu", lat: 34.24, lon: 36.01, cue: "libanu", abaixo: true },
    { nome: "Cypr", lat: 35.0, lon: 33.0, cue: "cypru", esquerda: true },
    { nome: "Wybrzeże Syrii", lat: 35.52, lon: 35.78, cue: "syrii" },
  ]} marca={{ nome: "Aleksandria", lat: 31.2, lon: 29.92, cue: "drewno" }} linhas={[{ pontos: [[31.0, 25.2], [31.3, 27.2], [30.9, 29.0], [31.2, 29.9], [31.5, 31.0], [31.3, 32.3], [31.2, 34.2], [32.1, 34.8], [32.8, 35.0], [33.9, 35.5], [34.9, 35.9], [35.5, 35.8], [36.2, 35.95], [36.6, 36.2], [36.8, 35.5], [36.6, 34.6], [36.2, 33.6], [36.1, 32.6]] }, { pontos: [[35.17, 32.3], [35.4, 32.9], [35.35, 33.6], [35.65, 34.55], [35.3, 34.0], [34.95, 34.05], [34.65, 33.0], [34.7, 32.4], [35.17, 32.3]] }, { pontos: [[31.4, 30.3], [30.1, 31.2], [27.2, 31.2]], cor: "#3E7FB0" }]} tint={colors.accent} />
);

// 2. a tripulação (p12: "dodajmy to")
export const P02Zaloga: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ZAŁOGA CZTERDZIESTKI · WEDŁUG ATENAJOSA" valor={7250} cue="7250" sep=" "
    sufixo={`${NB}ludzi`} barras={[
      { rotulo: "Wioślarze", v: 4000, cue: "4000" },
      { rotulo: "Ludzie pokładowi", v: 400, cue: "400" },
      { rotulo: "Żołnierze", v: 2850, cue: "2850", destaque: true },
    ]} />
);

// 3. a trirreme clássica (p19)
export const P03Trirema: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Klasyczna grecka trirema", titulo: "Trzy rzędy wioseł", linhas: [
    { rotulo: "Układ wioseł", valor: "3 rzędy, schodkowo", cue: "schodkowym" },
    { rotulo: "Wioślarze", valor: "170", cue: "170" },
    { rotulo: "Cała załoga", valor: `około 200${NB}osób`, cue: "200" },
    { rotulo: "Długość", valor: `około 37${NB}m`, cue: "37", destaque: true },
  ], tint: "cool" }} />
);

// 4. MAPA: Atenas -> Sicília, 415 a.C. (p31)
export const P04Sycylia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="415 P.N.E. · FLOTA ATEŃSKA PŁYNIE NA SYCYLIĘ" lugares={[
    { nome: "Pireus", lat: 37.94, lon: 23.65, cue: "floty", esquerda: true },
    { nome: "Syrakuzy", lat: 37.07, lon: 15.29, cue: "sycyl", abaixo: true },
  ]} linhas={[{ pontos: [[38.25, 15.65], [38.2, 13.4], [38.0, 12.5], [37.6, 12.6], [37.1, 14.3], [36.7, 15.1], [37.1, 15.3], [37.5, 15.1], [38.25, 15.65]] }, { pontos: [[40.0, 15.6], [38.9, 16.2], [38.0, 15.7], [38.4, 16.6], [39.4, 17.1], [40.4, 17.3]] }, { pontos: [[39.4, 20.2], [38.6, 21.1], [38.3, 21.8], [37.6, 21.3], [36.8, 21.7], [36.5, 22.4], [37.0, 22.7], [36.45, 23.1], [37.5, 23.1], [37.9, 23.0], [37.95, 23.6], [37.65, 24.05], [38.2, 24.1], [38.9, 23.4]] }, { pontos: [[38.3, 21.8], [38.1, 22.6], [37.95, 23.0]] }]} tint={colors.accent} />
);

// 5. um dia no navio (p47)
export const P05Dzien: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="JEDEN DZIEŃ NA OKRĘCIE" tint={colors.accent} marcos={[
    { ano: "ŚWIT", texto: "wypłynięcie, morze jeszcze spokojne", cue: "świcie" },
    { ano: "WIOSŁA", texto: "pierwsze godziny: wyjście z portu", cue: "godziny" },
    { ano: "WIATR", texto: "jeśli dopisze", cue: "wiatr" },
    { ano: "ŻAGIEL", texto: "wiosła idą do wnętrza", cue: "żagiel" },
  ]} />
);

// 6. Arginusas, 406 a.C. (p55)
export const P06Arginuzy: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="arginuz" chave={4} linhas={[
    "ATENY · 406 P.N.E.",
    "",
    "Bitwa pod Arginuzami: Ateńczycy wygrali",
    "Burza: rozbitków nie uratowano",
    "Wielu marynarzy utonęło",
    "Sześciu dowódców floty przed sądem",
  ]} carimbo={{ texto: "SKAZANI NA ŚMIERĆ", cue: "skazano" }} />
);

// 7. MAPA: a tempestade de 255 a.C. (p60)
export const P07Burza: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="255 P.N.E. · FLOTA RZYMSKA WRACA Z AFRYKI" unidade="okrętów" sep=" " lugares={[
    { nome: "Afryka", lat: 36.85, lon: 11.1, cue: "afryki", valor: 300, abaixo: true },
    { nome: "Sycylia", lat: 36.87, lon: 14.45, cue: "80", valor: 80, esquerda: true },
  ]} linhas={[{ pontos: [[38.25, 15.65], [38.2, 13.4], [38.0, 12.5], [37.6, 12.6], [37.1, 14.3], [36.7, 15.1], [37.1, 15.3], [37.5, 15.1], [38.25, 15.65]] }, { pontos: [[37.3, 9.8], [37.2, 10.3], [37.05, 11.05], [36.85, 11.1], [36.4, 10.6], [35.8, 10.6], [35.2, 11.1], [34.5, 10.5]] }]} tint={colors.danger} />
);

// 8. a ração (p67)
export const P08Racja: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="alfita" chave={2} linhas={[
    "CODZIENNA RACJA WIOŚLARZA",
    "",
    "Jęczmienna mąka — alphita",
    "Papka albo płaskie placki",
    "Oliwki · cebula · czosnek",
    "Ser · sól · suszone figi",
  ]} />
);

// 9. MAPA: Alexandria, Heptastádio e Faros (p73)
export const P09Faros: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ALEKSANDRIA · DWA PORTY, GROBLA I LATARNIA" lugares={[
    { nome: "Aleksandria", lat: 31.198, lon: 29.905, cue: "aleksandria", abaixo: true },
    { nome: "Heptastadion", lat: 31.205, lon: 29.894, cue: "hepta", esquerda: true },
    { nome: "Faros", lat: 31.214, lon: 29.8856, cue: "pharos" },
  ]} linhas={[{ pontos: [[31.17, 29.84], [31.19, 29.86], [31.2, 29.875], [31.21, 29.878], [31.216, 29.882], [31.215, 29.89], [31.207, 29.893], [31.2, 29.9], [31.205, 29.91], [31.212, 29.92], [31.22, 29.94], [31.235, 29.96]] }]} tint={colors.accent} />
);

// 10. a peste de Potideia (p83)
export const P10Zaraza: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Tukidydes · zaraza", titulo: "Potidaja", linhas: [
    { rotulo: "Rok", valor: "430 p.n.e.", cue: "430" },
    { rotulo: "Ciężkozbrojni pod Potidają", valor: `4${NB}000`, cue: "czterech" },
    { rotulo: "W ciągu", valor: `40${NB}dni`, cue: "40" },
    { rotulo: "Zmarło", valor: `1${NB}050`, cue: "1050", destaque: true },
  ], tint: "danger" }} />
);

// 11. a Syracusia (p92)
export const P11Syrakuzja: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="iliady" chave={6} linhas={[
    "SYRAKUZJA · OKRĘT HIERONA II",
    "",
    "Mozaiki ze scenami z Iliady",
    "Gimnazjon i ogrody w donicach",
    "Świątynia Afrodyty",
    "Biblioteka · łaźnia",
    "Zbiornik z żywymi rybami",
  ]} />
);

// 12. Ácio, 31 a.C. (p97)
export const P12Akcjum: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Akcjum · 31 p.n.e.", titulo: "Gigantyzm kontra zwrotność", linhas: [
    { rotulo: "Antoniusz", valor: "od 3 do 10 rzędów wioseł, wieże", cue: "trzech" },
    { rotulo: "Oktawian", valor: "mniejsze, zwrotniejsze jednostki", cue: "oktawian" },
    { rotulo: "Wynik", valor: "flota Antoniusza przegrała", cue: "przegra", destaque: true },
  ], tint: "accent" }} />
);
