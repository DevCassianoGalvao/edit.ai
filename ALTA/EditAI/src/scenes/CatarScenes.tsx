// Animações de "Catar: 99 % del agua potable sale del mar" (es) — painel 20261026-115617-audio-catar-esp
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (es).
import React from "react";
import { colors } from "../design/tokens";
import { Barras } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// contornos (lat, lon): Catar, costa árabe do golfo e costa iraniana
const CATAR: [number, number][] = [[26.17, 51.22], [26.05, 51.36], [25.92, 51.58], [25.62, 51.50], [25.38, 51.56],
  [25.29, 51.53], [25.17, 51.61], [24.99, 51.56], [24.80, 51.52], [24.62, 51.40], [24.55, 51.20], [24.60, 51.05],
  [24.75, 50.84], [25.10, 50.78], [25.43, 50.76], [25.62, 50.83], [25.90, 51.02], [26.17, 51.22]];
const ARABIA: [number, number][] = [[29.40, 47.90], [28.60, 48.40], [27.60, 49.20], [26.90, 49.70], [26.40, 50.15],
  [25.90, 50.20], [25.30, 50.50], [24.75, 50.84], [24.55, 51.20], [24.20, 51.60], [24.10, 52.40], [24.25, 53.50],
  [24.45, 54.40], [25.00, 55.00], [25.27, 55.30], [25.80, 56.00], [26.40, 56.40]];
const IRAN: [number, number][] = [[30.00, 48.90], [29.40, 50.00], [28.97, 50.84], [27.90, 51.50], [27.40, 52.60],
  [26.80, 53.80], [26.60, 54.80], [26.90, 55.70], [27.18, 56.27], [26.90, 57.00], [25.70, 57.80]];
const BAHREIN: [number, number][] = [[26.30, 50.55], [26.20, 50.65], [25.80, 50.60], [26.00, 50.45], [26.30, 50.55]];
const QESHM: [number, number][] = [[26.95, 55.80], [26.75, 56.20], [26.55, 55.70], [26.80, 55.30], [26.95, 55.80]];

// 1. MAPA: la península (p01)
export const A01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`CATAR · MENOS DE 12.000${NB}KM² · NINGÚN RÍO`}
    linhas={[{ pontos: CATAR, cor: colors.accent }, { pontos: ARABIA }, { pontos: IRAN }, { pontos: BAHREIN }]}
    lugares={[{ nome: "Catar", lat: 25.30, lon: 51.20, cue: "qatar", esquerda: true, abaixo: true }]}
    marca={{ nome: "Golfo Pérsico", lat: 27.30, lon: 52.20, cue: "golfo" }} tint={colors.accent} />
);

// 2. energía (p11)
export const A02Energia: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Revisión científica sobre el golfo" titulo="Energía por metro cúbico de agua" tint={colors.accent}
    max={26} barras={[
      { rotulo: "Destilación súbita multietapa · desde", valor: `12,5${NB}kWh`, v: 12.5, cue: "12", cor: colors.textDim },
      { rotulo: "Destilación súbita multietapa · hasta", valor: `24${NB}kWh`, v: 24, cue: "24", cor: colors.danger },
    ]} nota={{ texto: "Ósmosis inversa: hasta 75 % menos energía", cue: "75" }} />
);

// 3. el golfo desala (p17)
export const A03Golfo: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Centro estadístico del Golfo · 2023" titulo="Agua desalada (millones de m³)" tint={colors.accent}
    max={3200} barras={[
      { rotulo: "Arabia Saudita", valor: "3.000", v: 3000, cue: "3", cor: colors.textDim },
      { rotulo: "Emiratos", valor: "1.900", v: 1900, cue: "1", cor: colors.textDim },
      { rotulo: "Kuwait", valor: "800", v: 800, cue: "800", cor: colors.textDim },
      { rotulo: "Catar", valor: "700", v: 700, cue: "700", cor: colors.danger },
    ]} />
);

// 4. capacidad (p21)
export const A04Capacidad: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KAHRAMAA · MAYO DE 2026 · MILLONES DE GALONES AL DÍA" valor={540} cue="540" sep="."
    nota={{ texto: `red de agua desalada: 11.000${NB}km`, cue: "11" }}
    barras={[{ rotulo: "2026", v: 540, cue: "540", destaque: true }, { rotulo: "2019", v: 476, cue: "476" }]} />
);

// 5. MAPA: los megadepósitos (p33)
export const A05Depositos: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`MEGADEPÓSITOS · MÁS DE 650${NB}KM DE TUBERÍAS`} linhas={[{ pontos: CATAR }]} lugares={[
    { nome: "Umm Baraka", lat: 25.62, lon: 51.40, cue: "baraka" },
    { nome: "Umm Salal", lat: 25.42, lon: 51.40, cue: "salal" },
    { nome: "Rawdat Rashid", lat: 25.22, lon: 51.15, cue: "raudat", esquerda: true },
    { nome: "Abu Nakhla", lat: 25.12, lon: 51.33, cue: "abunakla", abaixo: true },
    { nome: "Al Thumama", lat: 25.23, lon: 51.55, cue: "altumama" },
  ]} tint={colors.accent} />
);

// 6. MAPA: la guerra de 2026 (p42)
export const A06Guerra: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="GOLFO PÉRSICO · MARZO DE 2026"
    linhas={[{ pontos: CATAR }, { pontos: ARABIA }, { pontos: IRAN }, { pontos: BAHREIN }, { pontos: QESHM }]}
    lugares={[
      { nome: "Qeshm", lat: 26.75, lon: 55.80, cue: "qeshm", esquerda: true },
      { nome: "Bahréin", lat: 26.10, lon: 50.55, cue: "bahrain", abaixo: true },
    ]} marca={{ nome: "Irán", lat: 29.30, lon: 53.20, cue: "iran" }} tint={colors.danger} />
);

// 7. el futuro (p46)
export const A07Futuro: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Demanda proyectada hacia 2040" titulo="Millones de m³ de agua al año" tint={colors.accent}
    max={2800} barras={[
      { rotulo: "Escenario más bajo", valor: "516", v: 516, cue: "516", cor: colors.textDim },
      { rotulo: "Escenario más alto", valor: "2.718", v: 2718, cue: "2", cor: colors.danger },
    ]} nota={{ texto: "con 500 litros por persona al día", cue: "500" }} />
);
