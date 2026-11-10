// Animações de "Cosa Mangiano gli Operai Chiusi 28 Giorni su una Piattaforma" (it) — painel 20261022-130920
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número è detto; migliaia con punto (it).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// penisola di Avalon (Terranova): baia di Conception, St. John's, Cape Race, Placentia
const AVALON: [number, number][] = [[48.16, -53.0], [47.73, -53.22], [47.39, -53.13], [47.6, -52.95], [47.81, -52.79],
  [47.57, -52.70], [47.52, -52.62], [47.31, -52.75], [46.95, -52.90], [46.66, -53.07], [46.73, -53.40], [46.82, -54.20],
  [47.25, -53.97], [47.75, -53.95]];
// costa romagnola: delta del Po -> Ravenna -> Rimini
const ROMAGNA: [number, number][] = [[45.05, 12.40], [44.97, 12.55], [44.85, 12.30], [44.68, 12.25], [44.56, 12.28],
  [44.49, 12.29], [44.33, 12.35], [44.26, 12.36], [44.20, 12.40], [44.06, 12.58]];

// 1. le rotazioni (p01)
export const A01Rotazioni: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Golfo del Messico · annunci per cuochi offshore", titulo: "La rotazione", linhas: [
    { rotulo: "A bordo · a terra", valor: "14 + 14 giorni", cue: "14", destaque: true },
    { rotulo: "Giornata di lavoro", valor: "12-14 ore", cue: "12" },
    { rotulo: "Settimana", valor: "7 giorni su 7", cue: "7" },
  ], tint: "accent" }} />
);

// 2. i conti di Mark Hepburn (p05)
export const A02Conti: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mark Hepburn · catering offshore, golfo del Messico", titulo: "I conti della cucina", linhas: [
    { rotulo: "Pasti a testa", valor: "3 al giorno", cue: "3" },
    { rotulo: "Pasti ogni giorno", valor: "600", cue: "600", destaque: true },
    { rotulo: "Persone a bordo", valor: "200", cue: "200" },
    { rotulo: "Carne cruda al giorno", valor: "400-450 libbre", cue: "400" },
  ], tint: "accent" }} />
);

// 3. Hibernia: le uova (p15)
export const A03Uova: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hibernia · una settimana tipica", titulo: "La colazione", linhas: [
    { rotulo: "Uova a settimana", valor: "2.160", cue: "2160", destaque: true },
    { rotulo: "Persone a bordo", valor: "circa 235", cue: "235" },
    { rotulo: "A testa", valor: "più di 9 uova", cue: "9" },
  ], tint: "accent" }} />
);

// 4. il pasto di mezzanotte (p22)
export const A04Notte: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Turno di notte", titulo: "Il pasto di mezzanotte", linhas: [
    { rotulo: "Turno", valor: "dalle 19 alle 7", cue: "19", destaque: true },
    { rotulo: "A mezzanotte", valor: "il pranzo", cue: "pranzo" },
  ], tint: "accent" }} />
);

// 5. MAPPA: da St. John's a Hibernia (p28)
export const A05Hibernia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LA SPESA DI HIBERNIA · TERRANOVA, CANADA" lugares={[
    { nome: "St. John's · il porto", lat: 47.56, lon: -52.71, cue: "john", esquerda: true },
    { nome: "Hibernia · 5-7 container a settimana", lat: 46.75, lon: -48.78, cue: "5", abaixo: true },
  ]} linhas={[{ pontos: AVALON }]}
    tint={colors.accent} />
);

// 6. il martedì della bistecca (p39)
export const A06Bistecche: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ROWAN GORILLA III · IL GIORNO DELLA BISTECCA" valor={170} cue="170" sep="."
    sufixo=" bistecche" nota={{ texto: "una dopo l'altra, sulla piastra, ogni martedì", cue: "170" }} />
);

// 7. MAPPA: Ravenna e il primo gas in mare (p46)
export const A07Ravenna: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MARE ADRIATICO · IL DISTRETTO OFFSHORE DI RAVENNA" lugares={[
    { nome: "Ravenna", lat: 44.42, lon: 12.20, cue: "ravenna", esquerda: true },
    { nome: "Ravenna Mare 3 · 1960", lat: 44.45, lon: 12.48, cue: "1960" },
  ]} linhas={[{ pontos: ROMAGNA }]}
    tint={colors.accent} />
);

// 8. le cozze delle piattaforme (p51)
export const A08Cozze: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="COZZE RACCOLTE OGNI ANNO DALLE STRUTTURE OFFSHORE" valor={6000} cue="6" sep="."
    sufixo=" quintali" nota={{ texto: "La Romagnola · quasi 30 quintali al giorno", cue: "30" }} />
);

// 9. il peso medio (p59)
export const A09Peso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Peso medio di un operaio offshore britannico", titulo: "Il conto sulla bilancia", linhas: [
    { rotulo: "1975", valor: `75${NB}kg`, cue: "75" },
    { rotulo: "2023", valor: `99${NB}kg`, cue: "99", destaque: true },
    { rotulo: "In meno di 50 anni", valor: `+24${NB}kg`, cue: "24" },
  ], tint: "accent" }} />
);

// 10. il comunicato del febbraio 2026 (p68)
export const A10Comunicato: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="comunicato" linhas={[
    "OFFSHORE ENERGIES UK · COMUNICATO",
    "5 FEBBRAIO 2026 · MARE DEL NORD",
    "MALTEMPO DA SETTIMANE",
    `ONDE FINO A 6${NB}METRI`,
    "LE NAVI NON RIESCONO A CONSEGNARE",
    "MANCANO ACQUA DOLCE E CIBO FRESCO",
  ]} chave={5} carimbo={{ texto: "RIFORNIMENTI BLOCCATI", cue: "6" }} />
);

// 11. l'ultimo conto (p83)
export const A11Conto: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Una piattaforma da 200 persone", titulo: "28 giorni di cucina", linhas: [
    { rotulo: "Rotazione", valor: "28 giorni", cue: "28" },
    { rotulo: "Persone a bordo", valor: "200", cue: "200" },
    { rotulo: "Pasti serviti", valor: "circa 16.800", cue: "16", destaque: true },
    { rotulo: "Carne cucinata", valor: "più di 5 tonnellate", cue: "5" },
  ], tint: "accent" }} />
);
