// As 8 animações de "Canada's German submarines" (en, 27 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Painel (2), MapaRota, LinhaDoTempo (2), Lista,
// Documento, Odometro. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: milhar partido "7 ,000" -> cue "7", "2 ,800" -> "2", "100 ,000" -> "100"; "Jinhai").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { LinhaDoTempo, Lista } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. requirements ----------------
export const C01Requisitos = painel({
  kicker: "Canadian Patrol Submarine Project",
  titulo: "The requirements were brutal",
  linhas: [
    { rotulo: "Range", valor: "7,000 nautical miles without refuelling", cue: "7" },
    { rotulo: "Underwater", valor: "3,000 nautical miles before snorkelling", cue: "3" },
    { rotulo: "On station", valor: "21 days", cue: "21" },
    { rotulo: "Ice", valor: "under first-year Arctic ice up to 1 metre", cue: "meter", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 2. the Korean voyage ----------------
export const C02Viagem: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="DOSAN AHN CHANGHO · MARCH 25 – MAY 26, 2026 · MORE THAN 14,000 KM"
    tint={colors.accent}
    lugares={[
      { nome: "Jinhae", lat: 35.14, lon: 128.66, cue: "jinhai|jinhae" },
      { nome: "Guam", lat: 13.44, lon: 144.79, cue: "guam", abaixo: true },
      { nome: "Hawaii", lat: 21.3, lon: 202.14, cue: "hawaii", abaixo: true },
      { nome: "CFB Esquimalt", lat: 48.43, lon: 236.57, cue: "esquimalt" },
    ]}
  />
);

// ---------------- 3. Hanwha's schedule ----------------
export const C03Hanwha: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Hanwha's promise"
    tint={colors.accent}
    marcos={[
      { ano: "2026", texto: "Contract signed", cue: "2026" },
      { ano: "2032", texto: "First Korean-built boat", cue: "2032" },
      { ano: "2035", texto: "Four boats delivered", cue: "2035" },
      { ano: "2043", texto: "All 12 delivered", cue: "2043", cor: colors.accent },
    ]}
  />
);

// ---------------- 4. the German boat ----------------
export const C04Tamanho = painel({
  kicker: "Type 212CD · Common Design",
  titulo: "Smaller — built around one idea",
  linhas: [
    { rotulo: "Length", valor: "about 73 metres", cue: "73" },
    { rotulo: "Submerged", valor: "around 2,800 tonnes", cue: "2" },
    { rotulo: "Crew", valor: "roughly 30", cue: "30" },
    { rotulo: "Idea", valor: "Stealth", cue: "stealth", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 5. power and weapons ----------------
export const C05Motor: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Type 212CD"
    titulo="Almost silent"
    tint={colors.cool}
    itens={[
      { titulo: "Hydrogen fuel cells", texto: "No big moving parts — almost silent.", cue: "fuel" },
      { titulo: "More than 20 knots", cue: "20" },
      { titulo: "Around 41 days of endurance", cue: "41" },
      { titulo: "6 tubes, up to 14 weapons", texto: "Torpedoes, anti-ship missiles, underwater air defence.", cue: "14", cor: colors.accent },
    ]}
  />
);

// ---------------- 6. the decision ----------------
export const C06Decisao: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="july"
    chave={3}
    linhas={[
      "GOVERNMENT OF CANADA — 6 JULY 2026",
      "Canadian Patrol Submarine Project",
      "",
      "Preferred supplier: ThyssenKrupp Marine Systems",
      "Up to 12 Type 212CD submarines",
      "Reserve option: Hanwha Ocean",
    ]}
    carimbo={{ texto: "PREFERRED SUPPLIER", cue: "reserve" }}
  />
);

// ---------------- 7. the cost ----------------
export const C07Custo: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="ESTIMATED TOTAL COST · INCLUDING LONG-TERM MAINTENANCE"
    valor={60}
    cue="60"
    prefixo="~$"
    sufixo=" billion CAD"
    nota={{ texto: "Well over 100,000 jobs — the largest defence procurement in Canadian history.", cue: "100" }}
  />
);

// ---------------- 8. the Northwest Passage ----------------
export const C08Passagem: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="The Northwest Passage"
    tint={colors.danger}
    marcos={[
      { ano: "1985", texto: "USCGC Polar Sea sails through without permission", cue: "1985" },
      { ano: "1987", texto: "Canada plans 10–12 nuclear attack submarines", cue: "1987" },
      { ano: "Washington", texto: "Not enthusiastic", cue: "washington" },
      { ano: "Cancelled", texto: "Within two years, citing cost", cue: "cancelled", cor: colors.danger },
    ]}
  />
);
