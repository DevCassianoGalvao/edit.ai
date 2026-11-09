// As 8 animações de "How Australia invented Wi-Fi" (en, 24,7 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — MapaRota, Lista, Colunas,
// Documento, LinhaDoTempo, Painel (2), Barras. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "802 .11a" -> cue "11a"; "$430" -> "430"; "90 %" -> "90").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, LinhaDoTempo, Lista } from "./blocos";
import { Documento, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. home to Sydney (MAPA) ----------------
export const W01Casa: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="FROM THE BLACK HOLE HUNT TO CSIRO RADIOPHYSICS, SYDNEY"
    tint={colors.accent}
    lugares={[
      { nome: "Westerbork, Netherlands", lat: 52.91, lon: 6.6, cue: "carried" },
      { nome: "Sydney", lat: -33.77, lon: 151.11, cue: "sydney", abaixo: true },
    ]}
  />
);

// ---------------- 2. rooms echo ----------------
export const W02Eco: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Multipath"
    titulo="Why rooms break fast radio"
    tint={colors.cool}
    itens={[
      { titulo: "Walls, ceilings, floors, desks, people", cue: "walls" },
      { titulo: "The signal bounces off all of them", cue: "bounces" },
      { titulo: "Dozens of copies arrive", cue: "dozens" },
      { titulo: "Each one a fraction of a second later", cue: "later", cor: colors.danger },
    ]}
  />
);

// ---------------- 3. many slow streams ----------------
export const W03Fluxos: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="The CSIRO idea"
    tint={colors.accent}
    cols={[
      { titulo: "One fast stream", texto: "Destroyed by echoes.", cue: "instead", cor: colors.danger },
      { titulo: "Many slow streams", texto: "Split the data.", cue: "split" },
      { titulo: "Side by side", texto: "Each on its own frequency.", cue: "side" },
      { titulo: "Total speed", texto: "Still high.", cue: "total", cor: colors.accent },
    ]}
  />
);

// ---------------- 4. the patent ----------------
export const W04Patente: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="january"
    chave={3}
    linhas={[
      "UNITED STATES PATENT — JANUARY 1996",
      "Assignee: CSIRO, Australia",
      "",
      "Patent No. 5,487,069",
      "Wireless LAN",
      "O'Sullivan · Daniels · Percival · Ostry · Deane",
    ]}
    carimbo={{ texto: "GRANTED", cue: "history" }}
  />
);

// ---------------- 5. the standard ----------------
export const W05Padrao: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="The standard built on it"
    tint={colors.cool}
    marcos={[
      { ano: "1999", texto: "New wireless specification", cue: "1999" },
      { ano: "802.11a", texto: "The Australian approach at its heart", cue: "11a" },
      { ano: "802.11g", texto: "Same core idea", cue: "11g" },
      { ano: "802.11n", texto: "Same core idea", cue: "11n", cor: colors.accent },
    ]}
  />
);

// ---------------- 6. the money ----------------
export const W06Dinheiro = painel({
  kicker: "CSIRO · Wi-Fi licences",
  titulo: "When the dust settled",
  linhas: [
    { rotulo: "Licensees", valor: "23 companies", cue: "23" },
    { rotulo: "Share of the industry", valor: "around 90 %", cue: "90" },
    { rotulo: "Total revenue", valor: "more than A$430 million", cue: "430", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 7. Ngara backhaul ----------------
export const W07Ngara: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Ngara backhaul · one antenna ≈ 40 microwave dishes"
    titulo="Across tens of kilometres"
    tint={colors.accent}
    max={10}
    barras={[
      { rotulo: "Early systems", valor: "150 Mbit/s", v: 0.3, cue: "150", cor: colors.textDim },
      { rotulo: "With EM Solutions", valor: "5 Gbit/s", v: 5, cue: "5", cor: colors.cool },
      { rotulo: "The target", valor: "10 Gbit/s", v: 10, cue: "10", cor: colors.accent },
    ]}
    nota={{ texto: "A single Ngara antenna does the work of around 40 dishes.", cue: "40" }}
  />
);

// ---------------- 8. ASKAP ----------------
export const W08Askap = painel({
  kicker: "ASKAP · Murchison, Western Australia",
  titulo: "Many small antennas, one smart dish",
  linhas: [
    { rotulo: "Dishes", valor: "36, each 12 metres across", cue: "focus" },
    { rotulo: "Phased array feed", valor: "188 receiving elements", cue: "188" },
    { rotulo: "Beams per dish", valor: "36 at the same time", cue: "36", destaque: true },
  ],
  tint: "cool",
});
