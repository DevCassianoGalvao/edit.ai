// Animações de "IF YOU MAKE YOUR BED EVERY MORNING, Here's Why" (en, enxuto) — painel 20261024-123051 (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~14 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const TEXAS: [number, number][] = [[36.5, -103.04], [36.5, -100.0], [34.56, -100.0], [34.0, -98.5], [33.85, -96.6],
  [33.6, -94.04], [31.0, -93.55], [29.7, -93.84], [29.3, -94.7], [28.0, -96.9], [26.0, -97.15], [26.05, -97.5],
  [26.4, -98.9], [27.5, -99.5], [28.6, -100.4], [29.8, -101.4], [29.5, -102.7], [29.0, -103.2], [29.9, -104.6],
  [31.0, -105.0], [31.8, -106.5], [32.0, -106.6], [32.0, -103.06], [36.5, -103.04]];

const BRITAIN: [number, number][] = [[50.1, -5.7], [50.6, -3.5], [50.7, -1.5], [50.8, 0.3], [51.1, 1.4], [51.4, 1.4],
  [51.8, 1.2], [52.5, 1.75], [52.95, 1.0], [53.5, 0.1], [54.5, -0.6], [55.0, -1.4], [55.8, -2.0], [56.0, -3.0],
  [56.5, -2.6], [57.7, -1.8], [57.6, -4.0], [58.6, -3.0], [58.6, -5.0], [57.5, -5.8], [56.3, -5.7], [55.4, -5.5],
  [54.8, -5.0], [54.8, -3.4], [54.0, -3.1], [53.4, -3.0], [53.3, -4.6], [52.8, -4.7], [52.0, -5.1], [51.6, -5.1],
  [51.4, -3.2], [51.2, -4.2], [50.1, -5.7]];

// 1. MAPA: Austin, Texas — o discurso de McRaven (camada 1)
export const B01Austin: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LAYER ONE · MAY 2014 · UNIVERSITY OF TEXAS" lugares={[
    { nome: "Austin, Texas", lat: 30.27, lon: -97.74, cue: "austin" },
  ]} linhas={[{ pontos: TEXAS }]} tint={colors.accent} />
);

// 2. Amabile & Kramer: o princípio do progresso
export const B02Progresso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Amabile & Kramer · The Progress Principle · 2011", titulo: "What makes a good workday", linhas: [
    { rotulo: "Daily diary entries", valor: "~12,000", cue: "12", destaque: true },
    { rotulo: "People", valor: "238", cue: "238" },
    { rotulo: "Companies", valor: "7", cue: "seven" },
  ], tint: "accent" }} />
);

// 3. Alcoa e Paul O'Neill: o hábito-chave da segurança (camada 2)
export const B03Alcoa: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Alcoa · Paul O'Neill · according to Duhigg", titulo: "Safety was the keystone", linhas: [
    { rotulo: "O'Neill retired", valor: "2000", cue: "2000" },
    { rotulo: "Annual net income", valor: "5× larger", cue: "five", destaque: true },
  ], tint: "accent" }} />
);

// 4. Langer & Rodin 1976: o asilo em Connecticut (camada 3)
export const B04Langer: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Langer & Rodin · Connecticut · 1976", titulo: "18 months later", linhas: [
    { rotulo: "Given responsibility · died", valor: "7 of 47", cue: "7", destaque: true },
    { rotulo: "Comparison group · died", valor: "13 of 44", cue: "13" },
  ], colunas: true, tint: "danger" }} />
);

// 5. Zeigarnik 1927: tarefas interrompidas (camada 5)
export const B05Zeigarnik: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Bluma Zeigarnik · 1927", titulo: "The unfinished task stays open", linhas: [
    { rotulo: "Tasks", valor: "puzzles · beads", cue: "puzzles" },
    { rotulo: "Unfinished tasks remembered", valor: "about 2×", cue: "twice", destaque: true },
  ], tint: "accent" }} />
);

// 6. National Sleep Foundation · Bedroom Poll (camada 6)
export const B06Poll: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "National Sleep Foundation · Bedroom Poll", titulo: "Bed makers and sleep", linhas: [
    { rotulo: "Adults asked", valor: "~1,500", cue: "1" },
    { rotulo: "Ages", valor: "25–55", cue: "25" },
    { rotulo: "More likely to report good sleep", valor: "+19 %", cue: "19", destaque: true },
  ], tint: "accent" }} />
);

// 7. Hunch.com: 68 mil respostas (camada 7)
export const B07Hunch: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hunch.com · about 68,000 people", titulo: "Do you make your bed?", linhas: [
    { rotulo: "Don't make it", valor: "59 %", cue: "59", destaque: true },
    { rotulo: "Make it", valor: "27 %", cue: "27" },
    { rotulo: "Pay a housekeeper", valor: "12 %", cue: "12" },
  ], colunas: true, tint: "accent" }} />
);

// 8. MAPA: Kingston University, Londres — os ácaros (camada 8)
export const B08Kingston: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="LAYER EIGHT · JANUARY 2005" lugares={[
    { nome: "Kingston University, London", lat: 51.41, lon: -0.30, cue: "kingston" },
  ]} linhas={[{ pontos: BRITAIN }]} tint={colors.accent} />
);
