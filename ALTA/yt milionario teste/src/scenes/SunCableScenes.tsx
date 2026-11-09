// As 8 animações de "SunCable — the solar cable to Singapore" (en, 26 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Painel, Barras (2), MapaRota, Odometro, Documento,
// LinhaDoTempo (2). Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "12,000" -> "12000", "4,300" -> "4300", "95%" -> "95", "22nd", "2030s").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, LinhaDoTempo } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. Powell Creek ----------------
export const S01Precinct = painel({
  kicker: "Powell Creek, Barkly Region, NT",
  titulo: "The solar precinct",
  linhas: [
    { rotulo: "Area", valor: "about 12,000 hectares", cue: "12" },
    { rotulo: "Block", valor: "12 km long × 10 km wide", cue: "10" },
    { rotulo: "Peak capacity", valor: "up to 20 gigawatts", cue: "20", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 2. Singapore vs the desert ----------------
export const S02Singapore: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Electricity in one year"
    titulo="One desert site, one country"
    tint={colors.accent}
    max={60}
    barras={[
      { rotulo: "Singapore consumes", valor: "55–60 TWh", v: 60, cue: "55", cor: colors.textDim },
      { rotulo: "20 GW in the Australian interior", valor: "close to 50 TWh", v: 50, cue: "50", cor: colors.accent },
    ]}
    nota={{ texto: "Roughly the needs of an entire developed country.", cue: "developed" }}
  />
);

// ---------------- 3. the route ----------------
export const S03Route: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="SUBSEA CABLE · AROUND 4,300 KM"
    tint={colors.accent}
    marca={{ nome: "Powell Creek", lat: -18.05, lon: 133.66, nota: "solar precinct", cue: "near" }}
    lugares={[
      { nome: "Darwin", lat: -12.46, lon: 130.84, cue: "darwin" },
      { nome: "Timor Sea", lat: -10.6, lon: 127.4, cue: "timor", abaixo: true },
      { nome: "Indonesian waters", lat: -5.6, lon: 112.5, cue: "archipelago", abaixo: true },
      { nome: "Singapore", lat: 1.29, lon: 103.85, cue: "peninsula" },
    ]}
  />
);

// ---------------- 4. Viking Link ----------------
export const S04Viking: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Subsea power cables"
    titulo="More than five times longer"
    tint={colors.accent}
    max={4300}
    barras={[
      { rotulo: "Viking Link · Britain–Denmark", valor: "765 km", v: 765, cue: "765", cor: colors.textDim },
      { rotulo: "SunCable · Darwin–Singapore", valor: "4,300 km", v: 4300, cue: "five", cor: colors.accent },
    ]}
    nota={{ texto: "Nothing on the scale of 4,300 km has ever been built.", cue: "300" }}
  />
);

// ---------------- 5. gas ----------------
export const S05Gas: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="SINGAPORE · 6 MILLION PEOPLE · 730 KM²"
    valor={95}
    cue="95"
    sufixo=" %"
    nota={{ texto: "of its electricity comes from imported natural gas.", cue: "imported" }}
  />
);

// ---------------- 6. EMA ----------------
export const S06Ema: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="22nd"
    chave={4}
    linhas={[
      "ENERGY MARKET AUTHORITY — SINGAPORE",
      "22 October 2024",
      "",
      "Applicant: SunCable",
      "Import of 1.75 GW of electricity",
      "Provided the project meets the required conditions.",
    ]}
    carimbo={{ texto: "CONDITIONAL APPROVAL", cue: "conditions" }}
  />
);

// ---------------- 7. collapse and rescue ----------------
export const S07Collapse: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="SunCable — from collapse to new owners"
    tint={colors.danger}
    marcos={[
      { ano: "Sale", texto: "Administrators sell the business", cue: "administrators" },
      { ano: "Contest", texto: "Forrest's side vs Cannon-Brookes's side", cue: "forrest" },
      { ano: "Winner", texto: "Grok Ventures + Quinbrook", cue: "grok", cor: colors.accent },
      { ano: "Sept 2023", texto: "Acquisition completed", cue: "september" },
    ]}
  />
);

// ---------------- 8. the moving timeline ----------------
export const S08Timeline: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="A timeline that keeps moving"
    tint={colors.accent}
    marcos={[
      { ano: "2023", texto: "Original construction start", cue: "2023" },
      { ano: "2026–27", texto: "Original first power", cue: "2026" },
      { ano: "Late 2027", texto: "Final investment decision", cue: "investment" },
      { ano: "Early 2030s", texto: "Power to Darwin", cue: "2030s" },
      { ano: "2035", texto: "Imports to Singapore", cue: "2035", cor: colors.accent },
    ]}
  />
);
