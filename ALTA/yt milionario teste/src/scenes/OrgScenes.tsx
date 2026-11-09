// Animações de "If You Can't Stop Organizing, Here's Why" (en, enxuto) — painel 20261020-215447 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. Aaron Kay 2008: 67 países (camada 1)
export const O01Kay: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Aaron Kay · 2008 · God and the Government", titulo: "When personal control feels shaky", linhas: [
    { rotulo: "Countries compared", valor: "67", cue: "67", destaque: true },
    { rotulo: "Less personal control", valor: "more support for government control", cue: "support" },
  ], tint: "accent" }} />
);

// 2. Whitson & Galinsky 2008 (Science): 6 experimentos, 43 % de imagens inventadas
export const O02Pontos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Whitson & Galinsky · Science · 2008", titulo: "Seeing patterns in random dots", linhas: [
    { rotulo: "Experiments", valor: "6", cue: "six" },
    { rotulo: "Empty pictures where people out of control saw an image", valor: "43 %", cue: "43", destaque: true },
  ], tint: "accent" }} />
);

// 3. MAPA: o laboratório na República Tcheca (camada 2)
export const O03Tcheca: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LAYER TWO · A LAB IN THE CZECH REPUBLIC" lugares={[
    { nome: "Czech Republic", lat: 49.75, lon: 15.4, cue: "czech" },
  ]} linhas={[
    { pontos: [[50.25, 12.1], [50.8, 12.9], [51.05, 14.3], [50.75, 15.0], [50.7, 16.2], [50.2, 16.9], [50.3, 17.7], [50.0, 18.0], [49.9, 18.6], [49.5, 18.85], [49.0, 17.9], [48.75, 17.1], [48.6, 16.9], [48.8, 16.0], [48.6, 15.0], [48.55, 14.7], [48.75, 13.8], [49.1, 13.4], [49.5, 12.5], [50.1, 12.3], [50.25, 12.1]] },
  ]} tint={colors.accent} />
);

// 4. Lang et al. 2015: a escultura
export const O04Lang: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Martin Lang · Current Biology · 2015", titulo: "The sculpture experiment", linhas: [
    { rotulo: "University students", valor: "62", cue: "sixty", destaque: true },
    { rotulo: "Groups", valor: "2", cue: "groups" },
    { rotulo: "Everyone was handed", valor: "a metal sculpture", cue: "sculpture" },
  ], tint: "accent" }} />
);

// 5. Brooks et al. 2016: o ritual sem lógica (camada 3)
export const O05Ritual: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Don't Stop Believing · 2016" titulo="A ritual with no logical purpose" tint={colors.accent} itens={[
    { titulo: "Draw how you feel", cue: "drew" },
    { titulo: "Sprinkle salt on it", cue: "sprinkled" },
    { titulo: "Count out loud", cue: "counted" },
    { titulo: "Throw the paper away", cue: "threw" },
  ]} />
);

// 6. o laço do hábito
export const O06Loop: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Layers one to three" titulo="How the habit is born" tint={colors.accent} itens={[
    { titulo: "Repetitive, orderly action", cue: "action" },
    { titulo: "A little relief", cue: "relief" },
    { titulo: "Your brain files it away", cue: "files" },
    { titulo: "Next time you reach faster", cue: "faster" },
  ]} />
);

// 7. Vohs, Redden & Rahinel 2013: sala arrumada x bagunçada (camada 6)
export const O07Vohs: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "University of Minnesota · 2013", titulo: "Tidy room vs. messy room", linhas: [
    { rotulo: "Donated · tidy room", valor: "82 %", cue: "82", destaque: true },
    { rotulo: "Donated · messy room", valor: "47 %", cue: "47" },
    { rotulo: "Chose the apple · tidy room", valor: "67 %", cue: "67", destaque: true },
    { rotulo: "Chose the apple · messy room", valor: "20 %", cue: "20" },
  ], colunas: true, tint: "accent" }} />
);

// 8. Curran & Hill 2019: perfeccionismo em alta (camada 7)
export const O08Curran: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Curran & Hill · 41,641 students · 1989–2016", titulo: "Perfectionism is increasing", linhas: [
    { rotulo: "Self-oriented", valor: "+10 %", cue: "10" },
    { rotulo: "Other-oriented", valor: "+16 %", cue: "16" },
    { rotulo: "Socially prescribed", valor: "+33 %", cue: "33", destaque: true },
  ], colunas: true, tint: "danger" }} />
);

// 9. NIMH: TOC nos adultos dos EUA
export const O09Nimh: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "National Institute of Mental Health", titulo: "OCD in U.S. adults", linhas: [
    { rotulo: "In the past year", valor: "1.2 %", cue: "1" },
    { rotulo: "At some point in life", valor: "2.3 %", cue: "2", destaque: true },
  ], tint: "danger" }} />
);
