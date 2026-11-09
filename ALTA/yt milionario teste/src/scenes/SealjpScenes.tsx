// Animações de "Japońscy inżynierowie sprawdzili chińskie auto" (pl, enxuto) — painel 20261101-121736 (baia b1).
// REGRA: biblioteca; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com espaço duro (pl).
import React from "react";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { colors } from "../design/tokens";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a książka da Nikkei BP (p03)
export const J01Ksiazka: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nikkei BP · demontaż BYD Seal", titulo: "Podręcznik za miliony jenów", linhas: [
    { rotulo: "Liczba stron", valor: `350`, cue: "350" },
    { rotulo: "Premiera", valor: `15${NB}września 2023`, cue: "15" },
    { rotulo: "Cena", valor: `ok.${NB}6${NB}340${NB}USD`, cue: "340", destaque: true },
  ], tint: "accent" }} />
);

// 2. UBS: koszt wytworzenia (p22)
export const J02Koszt: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UBS · KOSZT WYTWORZENIA BYD SEAL" valor={25} sufixo={`${NB}%`} cue="25" sep=" "
    nota={{ texto: "taniej niż europejscy rywale", cue: "25" }} />
);

// 3. integracja pionowa (p26)
export const J03Integracja: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KOMPONENTY SEALA ROBI SAM BYD" valor={75} sufixo={`${NB}%`} cue="75" sep=" "
    nota={{ texto: "marże dostawców zostają w domu", cue: "75" }} />
);

// 4. cykl projektowy (p34)
export const J04Cykl: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Jak często powstaje nowa generacja", titulo: "Dwa światy", linhas: [
    { rotulo: "Pickupy", valor: `raz na${NB}10${NB}lat`, cue: "czasem" },
    { rotulo: "Tradycyjni producenci", valor: `raz na${NB}5${NB}lat`, cue: "5" },
    { rotulo: "Chińskie firmy", valor: "co kilkanaście miesięcy", cue: "kilkana", destaque: true },
  ], tint: "danger" }} />
);

// 5. MAPA: Japonia kontra Detroit (p63)
export const J05Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DAWNIEJ AMERYKANIE ROZBIERALI JAPOŃSKIE AUTA" lugares={[
    { nome: "Nagoja · Japonia", lat: 35.18, lon: 136.91, cue: "japo", esquerda: true, abaixo: true },
    { nome: "Detroit · USA", lat: 42.33, lon: -83.05, cue: "detroit", abaixo: true },
  ]} tint={colors.accent} />
);

// 6. fakt trzeci (p74)
export const J06Fakty: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Fakt trzeci · szacunek UBS", titulo: "Rząd wielkości, nie wyrok", linhas: [
    { rotulo: "Koszt wytworzenia vs Europa", valor: `−25${NB}%`, cue: "25", destaque: true },
    { rotulo: "Komponenty własne BYD", valor: `75${NB}%`, cue: "75" },
  ], tint: "accent" }} />
);
