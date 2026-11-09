// Animações de "Dentro do Maior Comboio Fluvial do Brasil" (pt) — painel 20261105-162740 (b1, modo enxuto).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
// Rios (lat, lon) aproximados: Tapajós (Itaituba -> Santarém), Amazonas (Santarém -> Gurupá), Pará (Breves -> Belém)
const TAPAJOS: [number, number][] = [[-4.28, -55.99], [-3.6, -55.5], [-2.9, -55.1], [-2.42, -54.72]];
const AMAZONAS: [number, number][] = [[-2.2, -56.6], [-1.92, -55.5], [-2.42, -54.72], [-1.98, -53.6], [-1.6, -52.6], [-1.42, -51.6]];
const PARA: [number, number][] = [[-1.42, -51.6], [-1.7, -50.6], [-1.85, -49.8], [-1.6, -49.0], [-1.45, -48.5]];

export const S01Maior: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hidrovias do Brasil · Rio Tapajós", titulo: "O maior comboio fluvial do Brasil", linhas: [
    { rotulo: "Comprimento", valor: `346${NB}m`, cue: "346" },
    { rotulo: "Largura", valor: `75${NB}m`, cue: "75" },
    { rotulo: "Barcaças", valor: "35", cue: "35" },
    { rotulo: "Carga", valor: `70${NB}mil toneladas`, cue: "70", destaque: true },
  ], tint: "accent" }} />
);

export const S02Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="TAPAJÓS · AMAZONAS · PARÁ" lugares={[
    { nome: "Itaituba", lat: -4.28, lon: -55.99, cue: "itaituba", abaixo: true },
    { nome: "Barcarena", lat: -1.51, lon: -48.62, cue: "barcarena", esquerda: true },
  ]} linhas={[{ pontos: TAPAJOS }, { pontos: AMAZONAS }, { pontos: PARA }]} tint={colors.accent} />
);

export const S03Carretas: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Confederação Nacional do Transporte" titulo={`Para levar 70${NB}mil toneladas`} tint={colors.accent} max={2000} barras={[
    { rotulo: "Carretas de 35 t", valor: "2.000", v: 2000, cue: "carretas" },
    { rotulo: "Vagões de 70 t", valor: "1.000", v: 1000, cue: "vagões" },
    { rotulo: "Comboio de 35 barcaças", valor: "1", v: 20, cue: "único" },
  ]} />
);

export const S04Empurrador: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "HB Dourada · HB Mapará", titulo: "Os empurradores da rota", linhas: [
    { rotulo: "Propulsão", valor: "diesel-elétrica", cue: "diesel" },
    { rotulo: "Propulsores", valor: "azimutais", cue: "azimutal" },
    { rotulo: "Giro das hélices", valor: `360${NB}graus`, cue: "360", destaque: true },
    { rotulo: "Bloco empurrado", valor: `346${NB}m`, cue: "346" },
  ], tint: "accent" }} />
);

export const S05Seca: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Seca de 2023 · Rio Tapajós", titulo: "Barcaças com menos carga", linhas: [
    { rotulo: "Carga nas barcaças (Amport)", valor: `−40${NB}%`, cue: "40", destaque: true },
    { rotulo: "Hidrovias do Brasil", valor: "2/3 da capacidade", cue: "terços" },
  ], tint: "accent" }} />
);

export const S06Estreitos: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DOS ESTREITOS AO RIO PARÁ" lugares={[
    { nome: "Miritituba", lat: -4.28, lon: -55.99, cue: "miritituba", abaixo: true },
    { nome: "Vila do Conde", lat: -1.54, lon: -48.75, cue: "vila", esquerda: true },
  ]} marca={{ nome: "Estreitos", lat: -1.68, lon: -50.48, nota: "Boiuçu e Breves", cue: "estreito" }}
    linhas={[{ pontos: TAPAJOS }, { pontos: AMAZONAS }, { pontos: PARA }]} tint={colors.accent} />
);

export const S07Poraque: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Baird Maritime · HB Poraquê", titulo: "O empurrador elétrico", linhas: [
    { rotulo: "Comprimento", valor: `20,4${NB}m`, cue: "20" },
    { rotulo: "Propulsores", valor: `2 × 375${NB}kW`, cue: "375" },
    { rotulo: "Baterias", valor: `600${NB}kWh`, cue: "600", destaque: true },
    { rotulo: "CO₂ evitado", valor: `até 2.168${NB}t/ano`, cue: "carbônico" },
  ], tint: "accent" }} />
);

export const S08Emissoes: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Inventário de 2020 · Hidrovias do Brasil" titulo="Gramas de CO₂ por tonelada por km" tint={colors.accent} max={14} barras={[
    { rotulo: "Barcaça", valor: "4 g", v: 4, cue: "4" },
    { rotulo: "Trem", valor: "12 g", v: 12, cue: "12" },
    { rotulo: "Caminhão", valor: "14 g", v: 14, cue: "14" },
  ]} />
);

export const S09Cargill: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cargill · julho de 2025", titulo: "O desafiante do Tapajós", linhas: [
    { rotulo: "Barcaças", valor: "36", cue: "36" },
    { rotulo: "Milho", valor: `110.971${NB}t`, cue: "110", destaque: true },
    { rotulo: "Empurrador", valor: `6.400${NB}cv`, cue: "cavalos" },
    { rotulo: "Equivale a", valor: `2.500${NB}carretas`, cue: "carretas" },
  ], tint: "accent" }} />
);

export const S10ArcoNorte: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="ANTAQ · revista Cultivar" titulo="Fatia do Arco Norte na exportação de soja e milho" tint={colors.accent} max={35} barras={[
    { rotulo: "2010", valor: "14,4 %", v: 14.4, cue: "14" },
    { rotulo: "2019", valor: "31,9 %", v: 31.9, cue: "31" },
  ]} nota={{ texto: "2020: 42,3 milhões de toneladas", cue: "42" }} />
);
