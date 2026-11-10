// As animações de "Jak Startuje Helikopter Ważący 105 Ton? 5 Najcięższych Śmigłowców Świata i Ich Sekret" (pl,
// arquivo dark) — painel 20261008-010525 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO;
// todo número é dito; separador de milhar = espaço (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. CH-53K: a massa (p01)
export const H01Ogier: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Miejsce 5 · Sikorsky CH-53K King Stallion", titulo: "Maksymalna masa startowa", linhas: [
    { rotulo: "Z ładunkiem pod kadłubem", valor: `88${NB}000 funtów`, cue: "88" },
    { rotulo: "W naszych jednostkach", valor: `prawie 40${NB}ton`, cue: "40" },
    { rotulo: "Ściśle", valor: `39${NB}t 916${NB}kg`, cue: "916", destaque: true },
  ], tint: "cool" }} />
);

// 2. CH-53K: o que a marinha exige (p09)
export const H02Udzwig: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Wymóg marynarki USA · CH-53K", titulo: "Ładunek w gorącym powietrzu", linhas: [
    { rotulo: "Ładunek", valor: `27${NB}000 funtów`, cue: "27" },
    { rotulo: "Czyli", valor: `ponad 12${NB}ton`, cue: "12", destaque: true },
    { rotulo: "Zasięg", valor: `110 mil morskich`, cue: "110" },
  ], tint: "cool" }} />
);

// 3. o contrato de 2023 (p14)
export const H03Zamowienie: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="35" chave={3} linhas={[
    "US NAVY · ZAMÓWIENIE 2023",
    "Śmigłowiec: CH-53K King Stallion",
    "Liczba: 35 sztuk",
    `Wartość: 2 miliardy 770 milionów USD`,
    "w tym 8 dla Izraela (łącznie 12)",
  ]} carimbo={{ texto: "ZAMÓWIONO", cue: "770" }} />
);

// 4. Mi-6: 1957 (p19)
export const H04Mi6: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Miejsce 4 · Mil Mi-6 · 1957", titulo: "Maszyna, która przerosła wszystko", linhas: [
    { rotulo: "Podniósł podczas prób", valor: `20${NB}ton`, cue: "20" },
    { rotulo: "Średnica wirnika", valor: `35${NB}metrów`, cue: "35" },
    { rotulo: "Pole tarczy wirnika", valor: `ponad 960${NB}m²`, cue: "960", destaque: true },
  ], tint: "accent" }} />
);

// 5. os pylons da Instal (p25)
export const H05Slupy: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="INSTAL NASIELSK · Mi-6 · LINIE WYSOKIEGO NAPIĘCIA" valor={39} cue="39" sep=" "
    sufixo={`${NB}słupów`} nota={{ texto: `w 9 godzin · około 14 minut na jeden słup`, cue: "14" }} />
);

// 6. MAPA: o rei de bronze, Gliwice -> Kraków (p29)
export const H06Jagiello: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="1976 · POMNIK JAGIEŁŁY POD KADŁUBEM Mi-6" unidade="km" sep=" " lugares={[
    { nome: "Gliwice", lat: 50.29, lon: 18.67, valor: 0, cue: "gliwick", abaixo: true },
    { nome: "Kraków", lat: 50.06, lon: 19.94, valor: 97, cue: "krakow" },
  ]} tint={colors.accent} />
);

// 7. Mi-10: o guindaste voador (p39)
export const H07Mi10: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MIEJSCE 3 · Mil Mi-10 · LATAJĄCY DŹWIG" valor={15} cue="15" sep=" " sufixo={`${NB}ton`}
    barras={[{ rotulo: "Na platformie", v: 15, cue: "15", destaque: true }, { rotulo: "Na zawiesiu", v: 8, cue: "8" },
      { rotulo: "W środku", v: 3, cue: "3" }]}
    nota={{ texto: "prawdziwa robota działa się pod spodem", cue: "3" }} />
);

// 8. Mi-26: o segredo das pás (p53)
export const H08Lopaty: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Miejsce 2 · Mil Mi-26 · sekret wirnika", titulo: "Mniejszy wirnik, więcej łopat", linhas: [
    { rotulo: "Mi-6 · wirnik 35 m", valor: `5${NB}łopat`, cue: "5" },
    { rotulo: "Mi-26 · wirnik 32 m", valor: `8${NB}łopat`, cue: "8", destaque: true },
  ], tint: "accent", colunas: true }} />
);

// 9. Chernobyl (p61)
export const H09Czarnobyl: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CZARNOBYL · 27 KWIETNIA – 5 MAJA 1986" valor={1800} cue="1800" sep=" " prefixo="około "
    sufixo={`${NB}lotów`} nota={{ texto: `około 5${NB}000 ton piasku, ołowiu i innych materiałów`, cue: "5000" }} />
);

// 10. MAPA: o mamute (p66)
export const H10Mamut: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="PAŹDZIERNIK 1999 · MAMUT W BLOKU ZMARZLINY · 23 TONY" lugares={[
    { nome: "Północna Syberia", lat: 73.6, lon: 104.5, cue: "syberi" },
    { nome: "Chatanga", lat: 71.98, lon: 102.47, cue: "hatand|chatand", abaixo: true },
  ]} tint={colors.cool} />
);

// 11. V-12 (p71)
export const H11V12: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Miejsce 1 · Mil W-12 (Mi-12)", titulo: "Największy śmigłowiec w historii", linhas: [
    { rotulo: "Maksymalna masa startowa", valor: `105${NB}ton`, cue: "105", destaque: true },
    { rotulo: "Masa pustej maszyny", valor: `69${NB}t 100${NB}kg`, cue: "69" },
  ], tint: "danger" }} />
);

// 12. o recorde de 1969 (p84)
export const H12Rekord: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="6 SIERPNIA 1969 · REKORD ŚWIATA · W-12" valor={40204} cue="40" sep=" " sufixo={`${NB}kg`}
    nota={{ texto: `na wysokość 2${NB}255 metrów · do dziś niepobity`, cue: "2255" }} />
);

// 13. os cinco juntos (p92)
export const H13Piatka: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="5 NAJCIĘŻSZYCH ŚMIGŁOWCÓW ŚWIATA" valor={105} cue="105" sep=" " sufixo={`${NB}ton`}
    barras={[{ rotulo: "CH-53K", v: 40, cue: "56" }, { rotulo: "Mi-10", v: 43.7, cue: "56" },
      { rotulo: "Mi-26", v: 56, cue: "56" }, { rotulo: "W-12", v: 105, cue: "105", destaque: true }]} />
);

// 14. MAPA: Dęblin (p96)
export const H14Deblin: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Mi-6 „JAGIEŁŁO” · MUZEUM SIŁ POWIETRZNYCH" lugares={[
    { nome: "pod Moskwą", lat: 55.75, lon: 37.62, cue: "moskw" },
    { nome: "Dęblin", lat: 51.56, lon: 21.85, cue: "deblin", abaixo: true },
  ]} tint={colors.accent} />
);
