// Animações de "Como Vivem os Tripulantes dos Comboios Gigantes que Levam Soja" (pt) — painel 20261104-004259 (b1, modo enxuto).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

export const S01Bertolini: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Revista Oeste · Miritituba", titulo: "Comboio Bertolini 150", linhas: [
    { rotulo: "Comboio", valor: "Bertolini 150", cue: "150" },
    { rotulo: "Embarque da carga", valor: `2 a 4${NB}dias`, cue: "2" },
    { rotulo: "Barcaças", valor: "25", cue: "25" },
    { rotulo: "Carga", valor: `60${NB}mil toneladas`, cue: "60", destaque: true },
  ], tint: "accent" }} />
);

export const S02Maior: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hidrovias do Brasil · fevereiro de 2023", titulo: "O maior comboio do país", linhas: [
    { rotulo: "Barcaças", valor: "35", cue: "35", destaque: true },
    { rotulo: "Capacidade", valor: `70${NB}mil t`, cue: "70" },
    { rotulo: "Comprimento", valor: `346${NB}m`, cue: "346" },
    { rotulo: "Largura", valor: `75${NB}m`, cue: "75" },
  ], tint: "accent" }} />
);

export const S03Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="TAPAJÓS · MIRITITUBA ATÉ BARCARENA" lugares={[
    { nome: "Miritituba", lat: -4.28, lon: -55.99, cue: "miritituba", abaixo: true },
    { nome: "Barcarena", lat: -1.51, lon: -48.62, cue: "barca", esquerda: true },
  ]} tint={colors.accent} />
);

export const S04Madeira: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="HIDROVIA DO MADEIRA" lugares={[
    { nome: "Porto Velho", lat: -8.76, lon: -63.9, cue: "porto", esquerda: true },
    { nome: "Itacoatiara", lat: -3.14, lon: -58.44, cue: "itacoatiara", abaixo: true },
    { nome: "Santarém", lat: -2.44, lon: -54.71, cue: "santar" },
  ]} tint={colors.accent} />
);

export const S05Seca: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Seca de 2024 · Amport", titulo: "Carga reduzida nos comboios", linhas: [
    { rotulo: "Rio Madeira", valor: `−50${NB}%`, cue: "50", destaque: true },
    { rotulo: "Rio Tapajós", valor: `−40${NB}%`, cue: "40" },
  ], tint: "accent" }} />
);

export const S06Fila: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="PORTO VELHO · 2025 · FILAS DE CAMINHÕES" valor={11000} cue="11" sufixo=" caminhões" sep="."
    nota={{ texto: "atrasando o escoamento da soja", cue: "11" }} />
);
