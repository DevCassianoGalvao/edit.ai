// Animações de "Gdzie Trafiają Śmieci 10 Tysięcy Ludzi z Największego Statku Świata?" (pl) — painel 20261015-010548
// (baia 1, modo enxuto). REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com espaço (pl).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o navio em números (p02)
export const SM01Kadlub: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Icon of the Seas · Royal Caribbean", titulo: "Pływające miasto", linhas: [
    { rotulo: "Długość kadłuba", valor: `365${NB}m`, cue: "365", destaque: true },
    { rotulo: "Pokłady", valor: "20", cue: "20" },
    { rotulo: "Pojemność brutto", valor: `ok. 250${NB}800${NB}GT`, cue: "250" },
  ], tint: "accent" }} />
);

// 2. desperdício de comida: 24 % x meta de metade (p07)
export const SM02Marnowanie: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Win on Waste · marnowanie jedzenia" titulo="Wynik a cel" tint={colors.accent} max={50}
    barras={[
      { rotulo: "Spadek marnowania", valor: "24%", v: 24, cue: "24" },
      { rotulo: "Cel: połowa (64 statki, do 2025)", valor: "50%", v: 50, cue: "połowę", cor: colors.textDim },
    ]} />
);

// 3. Save the Waves (p14)
export const SM03Recykling: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Save the Waves · Royal Caribbean", titulo: "Bez wysypiska", linhas: [
    { rotulo: "Program recyklingu", valor: "ponad 30 lat", cue: "30" },
    { rotulo: "Statki floty wyposażone", valor: "100%", cue: "100" },
    { rotulo: "Klasa Icon: omija wysypisko", valor: "ponad 90%", cue: "90", destaque: true },
  ], tint: "accent" }} />
);

// 4. MAPA: a segunda incineradora — Węgry -> Miami (p22)
export const SM04Spalarnia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DRUGA SPALARNIA EVAC · 2025" lugares={[
    { nome: "Węgry", lat: 47.16, lon: 19.50, cue: "Węgrzech", abaixo: true, esquerda: true },
    { nome: "Miami", lat: 25.77, lon: -80.19, cue: "Miami", abaixo: true },
  ]} tint={colors.accent} />
);

// 5. esgoto por semana — navio da classe Oasis (p29)
export const SM05Scieki: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Szacunki · statek klasy Oasis · tydzień" titulo="Ścieki w jednym tygodniu" tint={colors.accent} max={3.7}
    barras={[
      { rotulo: "Woda czarna", valor: `ok. 794${NB}000${NB}l`, v: 0.794, cue: "794", cor: colors.danger },
      { rotulo: "Woda szara", valor: `ponad 3,7${NB}mln${NB}l`, v: 3.7, cue: "700" },
    ]} />
);

// 6. MARPOL: 15 ppm (p37)
export const SM06Marpol: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MARPOL · WODA ZĘZOWA ZA BURTĘ" valor={15} cue="15" sufixo=" ppm" sep={NB}
    nota={{ texto: "nie więcej niż 15 części oleju na milion", cue: "milion" }} />
);

// 7. o gerador de micro-ondas (p53)
export const SM07Mikrofale: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Piroliza mikrofalowa · Scanship", titulo: "Półprzewodnikowy generator", linhas: [
    { rotulo: "Moc generatora", valor: `30${NB}kW`, cue: "30", destaque: true },
    { rotulo: "Częstotliwość", valor: `900–930${NB}MHz`, cue: "900" },
  ], tint: "accent" }} />
);

// 8. energia: 200 kW do lixo x 67 500 kW dos motores (p61)
export const SM08Bilans: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="System MAP · bilans energii" titulo="Mniej niż 0,5% mocy statku" tint={colors.accent} max={67500}
    barras={[
      { rotulo: "Sześć silników", valor: `ok. 67,5${NB}tys.${NB}kW`, v: 67500, cue: "67" },
      { rotulo: "Energia z odpadów", valor: `ok. 200${NB}kW`, v: 200, cue: "200", cor: colors.danger },
    ]} />
);

// 9. palety em Miami: 222 -> 60 (p73)
export const SM09Palety: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Miami · palety odpadów tygodniowo" titulo="Druga spalarnia: 127 palet części" tint={colors.accent} max={222}
    barras={[
      { rotulo: "Z jedną spalarnią", valor: "222", v: 222, cue: "222", cor: colors.danger },
      { rotulo: "Z dwiema spalarniami", valor: "ok. 60", v: 60, cue: "60" },
    ]} />
);
