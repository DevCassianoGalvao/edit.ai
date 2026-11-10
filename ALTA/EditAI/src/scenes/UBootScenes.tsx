// As animações de "18 Tage unter Wasser ohne Tageslicht — Wie leben 28 Soldaten in einem deutschen U-Boot?" (de,
// arquivo dark) — painel 20261008-004326 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO;
// todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o gancho (p00)
export const U01Stahlroehre: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U 32 · Klasse 212A · Deutsche Marine", titulo: "Eine Stahlröhre unter dem Atlantik", linhas: [
    { rotulo: "Soldaten an Bord", valor: "28", cue: "28" },
    { rotulo: "Länge des Bootes", valor: `56${NB}Meter`, cue: "56", destaque: true },
  ], tint: "cool" }} />
);

// 2. MAPA: Eckernförde -> Florida (p08)
export const U02Route: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FEBRUAR 2013 · VON ECKERNFÖRDE NACH FLORIDA" lugares={[
    { nome: "Eckernförde", lat: 54.47, lon: 9.84, cue: "ostsee", abaixo: true },
    { nome: "Dänemark", lat: 57.75, lon: 10.6, cue: "danemark" },
    { nome: "Nordsee", lat: 58.5, lon: 1.5, cue: "nordsee" },
    { nome: "Atlantik", lat: 45.0, lon: -30.0, cue: "atlantik" },
    { nome: "Mayport, Florida", lat: 30.39, lon: -81.41, cue: "florida", abaixo: true },
  ]} tint={colors.cool} />
);

// 3. as camas (p23)
export const U03Kojen: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U 32 · Schlafplätze", titulo: "Die Rechnung geht nicht auf", linhas: [
    { rotulo: "Kojen", valor: "24", cue: "24" },
    { rotulo: "Menschen", valor: "28", cue: "28", destaque: true },
  ], tint: "danger" }} />
);

// 4. U 35 (p35)
export const U04Spielraum: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U 35 · dieselbe Klasse", titulo: "Wenn es voll wird", linhas: [
    { rotulo: "Stammbesatzung", valor: "28", cue: "28" },
    { rotulo: "Bei Bedarf eingeschifft", valor: `bis zu 36`, cue: "36", destaque: true },
    { rotulo: "Kojen", valor: "24", cue: "24" },
  ], tint: "cool" }} />
);

// 5. a célula de combustível (p44)
export const U05Brennstoffzelle: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="U 32 · BRENNSTOFFZELLENANLAGE" valor={306} cue="306" sep="." sufixo={`${NB}Kilowatt`}
    nota={{ texto: "neun Module von Siemens · wassergekühlt · ohne Außenluft", cue: "306" }} />
);

// 6. o periscópio (p60)
export const U06Sehrohr: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U 32 · das einzige Auge nach draußen", titulo: "Das Sehrohr", linhas: [
    { rotulo: "Sehrohrtiefe", valor: `13,5${NB}Meter`, cue: "13", destaque: true },
    { rotulo: "Vergrößerung", valor: "zwölffach", cue: "zwolffach" },
  ], tint: "cool" }} />
);

// 7. a tempestade (p80)
export const U07Sturm: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="NORDATLANTIK · TENDER MAIN · FEBRUAR 2013" valor={8} cue="8" sep="." prefixo="bis zu "
    sufixo={`${NB}Meter`} nota={{ texto: "Wellenhöhe · ein Haus mit drei Stockwerken", cue: "8" }} />
);

// 8. a profundidade (p94)
export const U08Tiefe: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KLASSE 212A · TAUCHTIEFE" valor={700} cue="700" sep="." sufixo={`${NB}Meter`}
    barras={[{ rotulo: "Einsatz", v: 250, cue: "250" }, { rotulo: "Einsatz", v: 400, cue: "400" },
      { rotulo: "Zerstörungstiefe", v: 700, cue: "700", destaque: true }]}
    nota={{ texto: "ab hier würde der Wasserdruck den Rumpf zerquetschen", cue: "700" }} />
);

// 9. a família (p110)
export const U09Familie: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U-Boot-Besatzungen der Deutschen Marine", titulo: "Tage auf See pro Jahr", linhas: [
    { rotulo: "Im Durchschnitt", valor: `150 bis 200${NB}Tage`, cue: "150", destaque: true },
    { rotulo: "Das ist", valor: "mehr als die Hälfte des Jahres", cue: "200" },
  ], tint: "danger" }} />
);

// 10. o balanço (p121)
export const U10Bilanz: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "U 32 · Februar bis August 2013", titulo: "Die Bilanz der Reise", linhas: [
    { rotulo: "Zurückgelegt", valor: `mehr als 17.000${NB}Seemeilen`, cue: "17", destaque: true },
    { rotulo: "Das sind", valor: `über 30.000${NB}Kilometer`, cue: "30" },
  ], tint: "accent" }} />
);
