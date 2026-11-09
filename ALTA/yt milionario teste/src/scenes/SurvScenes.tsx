// Animações de "12 cheap Harbor Freight items when the furnace dies" (en, enxuto) — painel 20261020-101524-eng-suvival (baia b1).
// REGRA: biblioteca; motion curto (cues <= ~12 s); todo número é dito. Cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

// 1. a noite em que a fornalha parou (p0)
export const S01Relogio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "The furnace quit", titulo: "No heat tonight", linhas: [
    { rotulo: "The furnace stopped at", valor: "2 a.m.", cue: "two" },
    { rotulo: "The house is losing", valor: "a degree every hour", cue: "degree" },
    { rotulo: "The repair company", valor: "not until Thursday", cue: "thursday", destaque: true },
  ], tint: "accent" }} />
);

// 2. as frestas que agem como janelas abertas (p8)
export const S02Frestas: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Drafts · the silent enemy" titulo="Tiny open windows" tint={colors.accent} itens={[
    { titulo: "The bottom of an exterior door", cue: "bottom" },
    { titulo: "The edges of old windows", cue: "edges" },
    { titulo: "The crack around an attic hatch", cue: "attic" },
    { titulo: "The gap around a pipe", cue: "pipe" },
  ]} />
);

// 3. as coisas simples antes de chamar o técnico (p14)
export const S03Simples: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Before you assume the worst" titulo="Check the simple things" tint={colors.accent} itens={[
    { titulo: "A dead thermostat battery", cue: "battery" },
    { titulo: "A tripped breaker", cue: "tripped" },
    { titulo: "A switch flipped by accident", cue: "switch" },
    { titulo: "A loose wire", cue: "loose" },
  ]} />
);

// 4. MAPA: tempestade de inverno, energia oscilando (p20)
export const S04Tempestade: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FURNACE FAILURES LOVE BAD TIMING · A WINTER STORM" lugares={[
    { nome: "Winter storm", lat: 42.5, lon: -89.0, cue: "storm" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[33.7,-118.3],[32.5,-117.1],[32.7,-114.7],[31.3,-111.0],[31.3,-108.2],[31.8,-106.5],[29.6,-104.4],[29.8,-101.4],[26.0,-97.2],[27.8,-97.4],[29.4,-94.7],[29.6,-92.0],[29.0,-89.4],[30.4,-88.0],[30.0,-85.0],[29.1,-83.0],[26.0,-81.7],[25.2,-80.4],[26.8,-80.0],[30.5,-81.4],[32.0,-80.9],[33.8,-78.0],[35.2,-75.5],[37.0,-76.0],[38.9,-74.9],[40.5,-74.0],[41.3,-72.0],[41.6,-70.0],[42.9,-70.6],[44.8,-66.9],[47.4,-68.3],[45.0,-71.5],[45.0,-74.7],[43.6,-76.2],[43.3,-79.0],[42.0,-83.0],[45.7,-82.5],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);

// 5. vestir em camadas (p27)
export const S05Camadas: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Your body is the heating system" titulo="Think in layers" tint={colors.accent} itens={[
    { titulo: "Base layer", texto: "thin, next to the skin", cue: "base" },
    { titulo: "Middle layer", texto: "fleece or wool", cue: "middle" },
    { titulo: "Outer layer", texto: "windproof", cue: "outer" },
  ]} />
);

// 6. descongelar um cano com o soprador térmico (p30)
export const S06Degelo: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="A heat gun · a frozen pipe" titulo="Thaw it in order" tint={colors.danger} itens={[
    { titulo: "Open the faucet first", cue: "faucet" },
    { titulo: "Heat the side closest to the faucet", cue: "closest" },
    { titulo: "Work back toward the frozen section", cue: "frozen" },
  ]} />
);

// 7. a regra do monóxido de carbono (p36)
export const S07Regra: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Carbon monoxide · the rule" titulo="Never inside your home" tint={colors.danger} itens={[
    { titulo: "Never burn charcoal", cue: "charcoal" },
    { titulo: "Never run a grill", cue: "grill" },
    { titulo: "Never run a generator", cue: "generator" },
    { titulo: "Never use an unvented fuel heater", cue: "unvented" },
  ]} />
);
