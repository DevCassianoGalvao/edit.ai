// As animações de "12 Meter hohe Wellen und eisige Stürme — Krabbenfischer im Beringmeer" (de, arquivo dark) —
// painel 20261008-000607 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Documento, FotoMedidor, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
export const FOTO_EIS = "stock/pc93e16f5.jpg";

// arco das Aleutas (lat, lon; a Rússia fica em lon < -180 para o mapa não dar a volta no globo)
const ALEUTEN: [number, number][] = [[58.5, -156.0], [56.0, -160.5], [54.6, -163.5], [53.9, -166.5], [52.8, -169.5],
  [52.0, -173.5], [51.8, -177.0], [51.9, -182.0], [52.9, -187.0]];

// 1. o lugar (p01)
export const K01Beringmeer: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DAS BERINGMEER · ZWISCHEN ALASKA UND RUSSLAND" lugares={[
    { nome: "Alaska", lat: 61.2, lon: -149.9, cue: "alaska" },
    { nome: "Russland", lat: 64.7, lon: -182.5, cue: "russland" },
    { nome: "Aleuten", lat: 52.4, lon: -172.0, cue: "aleuten", abaixo: true },
  ]} linhas={[{ pontos: ALEUTEN }]} tint={colors.cool} />
);

// 2. Dutch Harbor (p06)
export const K02DutchHarbor: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Dutch Harbor · Unalaska · 2019", titulo: "Der wichtigste Fischereihafen der USA", linhas: [
    { rotulo: "Angelandet", valor: `763${NB}Mio.${NB}Pfund`, cue: "763" },
    { rotulo: "Das sind rund", valor: `345.000${NB}Tonnen`, cue: "345" },
    { rotulo: "Platz 1 aller Häfen", valor: `zum 23.${NB}Mal in Folge`, cue: "23", destaque: true },
  ], tint: "cool" }} />
);

// 3. a armadilha (p10)
export const K03Falle: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Krabbenfalle · Beringmeer", titulo: "Ein Käfig aus Stahl", linhas: [
    { rotulo: "Leer", valor: `etwa 700${NB}Pfund`, cue: "700" },
    { rotulo: "Das sind", valor: `über 300${NB}Kilo`, cue: "300", destaque: true },
    { rotulo: "Mit Krabben gefüllt", valor: `mehr als 1${NB}Tonne`, cue: "tonne" },
    { rotulo: "In den 50er-Jahren", valor: `nur etwa 140${NB}Kilo`, cue: "140" },
  ], tint: "cool" }} />
);

// 4. MAPA: a última viagem da Destination (p17)
export const K04Destination: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FEBRUAR 2017 · DIE LETZTE FAHRT DER DESTINATION" lugares={[
    { nome: "Dutch Harbor", lat: 53.89, lon: -166.54, cue: "dutch", abaixo: true },
    { nome: "Sankt Paul", lat: 57.12, lon: -170.28, cue: "paul" },
  ]} linhas={[{ pontos: ALEUTEN.slice(1, 6) }]} tint={colors.danger} />
);

// 5. sono (p34)
export const K05Schlaf: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KRABBENFISCHER AUF SEE · STUDIE DER US-GESUNDHEITSBEHÖRDE" valor={40} cue="40" sep="."
    prefixo="rund " sufixo={`${NB}%`}
    nota={{ texto: `Schmerzen stören den Schlaf · nur 3,5 bis 4${NB}Stunden Schlaf in 24${NB}Stunden`, cue: "40" }} />
);

// 6. mortalidade nos anos 90 (p42)
export const K06Sterblichkeit: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KRABBENFLOTTE BERINGMEER · ENDE DER 90ER-JAHRE" valor={770} cue="770" sep="."
    sufixo={`${NB}Tote`}
    nota={{ texto: `pro 100.000 Vollzeitarbeiter · im Schnitt 8${NB}Tote pro Jahr`, cue: "acht" }} />
);

// 7. a regra 1-10-1 (p54)
export const K07EinsZehnEins: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Gordon Giesbrecht · Universität von Manitoba", titulo: "Die 1-10-1-Regel", linhas: [
    { rotulo: "1 Minute", valor: "Kälteschock · Atmung kontrollieren", cue: "1" },
    { rotulo: "10 Minuten", valor: "dann versagen Arme und Beine", cue: "10" },
    { rotulo: "1 Stunde", valor: "bis zur Bewusstlosigkeit", cue: "phasen", destaque: true },
  ], tint: "cool" }} />
);

// 8. a noite da Scandies Rose (p71)
export const K08Silvester: React.FC<SceneProps> = (p) => (
  <FotoMedidor {...p} foto={FOTO_EIS} de={0} ate={-12} unidade={`${NB}°C`} cue="minus" efeito="gelo"
    legenda={`Silvester 2019 · Wellen etwa 6${NB}Meter · Wind rund 65${NB}km/h`} />
);

// 9. o relatório da NTSB (p79)
export const K09Empfehlungen: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="sieben" chave={3} linhas={[
    "NATIONAL TRANSPORTATION SAFETY BOARD",
    "Untergang der Scandies Rose · Silvester 2019",
    "",
    "7 Empfehlungen",
    "4 an die Küstenwache",
    "1 an die Wetter- und Ozeanbehörde",
    "1 an den Nationalen Wetterdienst",
    "1 an einen Verband von Schiffseignern im Nordpazifik",
  ]} carimbo={{ texto: "EMPFEHLUNGEN", cue: "verband" }} />
);

// 10. o colapso do caranguejo-das-neves (p85)
export const K10Milliarden: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="SCHNEEKRABBEN IM ÖSTLICHEN BERINGMEER" valor={8} cue="8" sep="." sufixo={`${NB}Milliarden`}
    barras={[{ rotulo: "2018", v: 8, cue: "8" }, { rotulo: "2021", v: 1, cue: "2021", destaque: true }]} />
);

// 11. as cotas novas (p90)
export const K11Fangmengen: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Fangmengen · 6. Oktober 2026", titulo: "Rote Königskrabbe · Bristol-Bucht", linhas: [
    { rotulo: "Neue Saison", valor: `3,41${NB}Mio.${NB}Pfund`, cue: "3", destaque: true },
    { rotulo: "Das sind rund", valor: `1.546${NB}Tonnen`, cue: "1546" },
    { rotulo: "Vorjahr", valor: `2,68${NB}Mio.${NB}Pfund`, cue: "2" },
  ], tint: "accent" }} />
);

// 12. hoje (p103)
export const K12Heute: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Beringmeer · heute", titulo: "Sicherer, aber nicht sicher", linhas: [
    { rotulo: "Wellen in schweren Winterstürmen", valor: `mehr als 12${NB}Meter`, cue: "12" },
    { rotulo: "Stahlkäfige an Deck", valor: `über 300${NB}Kilo`, cue: "300", destaque: true },
  ], tint: "danger" }} />
);
