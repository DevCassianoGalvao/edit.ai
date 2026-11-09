// Animações de "Bajaron una sonda a 700 metros bajo el desierto de Atacama" (es) — painel 20261014-141825 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com ponto (es).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Colunas } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: Santiago -> Copiapó -> mina San José (p01)
export const M01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="REGIÓN DE ATACAMA · NORTE DE CHILE" lugares={[
    { nome: "Santiago", lat: -33.45, lon: -70.67, cue: "días", esquerda: true },
    { nome: "Copiapó", lat: -27.37, lon: -70.33, cue: "agosto", abaixo: true },
    { nome: "Mina San José", lat: -27.16, lon: -70.50, cue: "mina", esquerda: true },
  ]} tint={colors.accent} />
);

// 2. atrapados (p07)
export const M02Atrapados: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mina San José · 5 de agosto de 2010", titulo: "Atrapados", linhas: [
    { rotulo: "Hombres bajo tierra", valor: "33", cue: "33", destaque: true },
    { rotulo: "Profundidad", valor: `unos 700${NB}m`, cue: "700" },
    { rotulo: "Hasta la entrada por la rampa", valor: `unos 5${NB}km`, cue: "5" },
  ], tint: "accent" }} />
);

// 3. o que havia no refúgio (p15)
export const M03Racion: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="atún" chave={2} linhas={[
    "REFUGIO · MINA SAN JOSÉ · INVENTARIO",
    "",
    "Latas de atún",
    "Leche",
    "Unas galletas",
    "Un durazno en conserva",
  ]} carimbo={{ texto: "ESO ERA TODO", cue: "todo" }} />
);

// 4. o furo da sonda (p28)
export const M04Agujero: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Los sondajes · agosto de 2010", titulo: "Una aguja en la roca", linhas: [
    { rotulo: "Diámetro del agujero", valor: `unos 15${NB}cm`, cue: "15" },
    { rotulo: "Más o menos", valor: "una mano abierta", cue: "mano" },
    { rotulo: "Profundidad", valor: `casi 700${NB}m`, cue: "700", destaque: true },
  ], tint: "accent" }} />
);

// 5. onde a 10B rompeu (p45)
export const M05Galeria: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sonda 10B · 22 de agosto de 2010", titulo: "Atravesó la roca", linhas: [
    { rotulo: "Profundidad", valor: `unos 688${NB}m`, cue: "688" },
    { rotulo: "Distancia al refugio", valor: `unos 20${NB}m`, cue: "20", destaque: true },
  ], tint: "accent" }} />
);

// 6. três planos ao mesmo tempo (p74)
export const M06Planes: React.FC<SceneProps> = (p) => (
  <Colunas {...p} kicker="TRES PLANES AL MISMO TIEMPO" tint={colors.accent} cols={[
    { titulo: "PLAN A", texto: "Strata 950 · pozo vertical nuevo", cue: "tres" },
    { titulo: "PLAN B", texto: "Schramm · agrandar la sonda 6C", cue: "mismo" },
    { titulo: "PLAN C", texto: "Torre de perforación petrolera", cue: "compitiendo" },
  ]} nota={{ texto: "Si uno fallaba, quedaban los otros dos", cue: "fallaba" }} />
);

// 7. a cápsula Fénix (p85)
export const M07Fenix: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cápsula Fénix 2 · Armada de Chile", titulo: "Un tubo de acero", linhas: [
    { rotulo: "Largo", valor: `unos 4${NB}m`, cue: "cuatro" },
    { rotulo: "Diámetro", valor: `54${NB}cm`, cue: "cincuenta", destaque: true },
  ], tint: "accent" }} />
);

// 8. os viajes da Fénix 2 (p114)
export const M08Viajes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CÁPSULA FÉNIX 2 · VIAJES DE IDA Y VUELTA" valor={39} cue="39" sep="."
    nota={{ texto: `unos 50${NB}km por un agujero del ancho de los hombros`, cue: "50" }} />
);

// 9. a justiça (p123)
export const M09Justicia: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="2013" chave={4} linhas={[
    "CAUSA PENAL · MINA SAN JOSÉ",
    "",
    "Agosto de 2013",
    "Tres años después del derrumbe",
    "La investigación se cierra",
  ]} carimbo={{ texto: "SIN ACUSADOS", cue: "nadie" }} />
);
