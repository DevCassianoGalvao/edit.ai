// Animações de "La autopsia de Ramsés III" (es) — painel 20261031-210711 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com ponto (es).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o reinado (p02)
export const R01Reinado: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "RAMSÉS III · SEGUNDO FARAÓN DE LA DINASTÍA XX", titulo: "Un reinado de treinta y un años", linhas: [
    { rotulo: "Duración", valor: `31${NB}años`, cue: "31" },
    { rotulo: "Comienza", valor: `1186${NB}a.C.`, cue: "1186" },
    { rotulo: "Termina", valor: `1155${NB}a.C.`, cue: "1155", destaque: true },
  ], tint: "accent" }} />
);

// 2. o Papiro Judicial de Turim (p24)
export const R02Papiro: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="registro|tribunal" linhas={[
    "PAPIRO JUDICIAL DE TURÍN · MUSEO EGIPCIO",
    "ESCRITO EN HIERÁTICO",
    "REGISTRO DE TRIBUNAL, NO RELATO LITERARIO",
    "· acusaciones",
    "· veredictos",
    "· castigos",
  ]} chave={2} carimbo={{ texto: "ACTA JUDICIAL", cue: "hierático|hieratico|escrib" }} />
);

// 3. os veredictos (p55)
export const R03Veredictos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="PAPIRO JUDICIAL DE TURÍN · EJECUTADOS" valor={28} cue="28" sufixo=" personas"
    nota={{ texto: "los jefes del complot, entre ellos", cue: "Pebekkamen|Pebek|jefes" }} />
);

// 4. MAPA: o esconderijo de Deir el-Bahari (p67)
const NILO: [number, number][] = [[25.765, 32.640], [25.735, 32.652], [25.710, 32.650], [25.680, 32.640]];
export const R04Escondite: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="TEBAS · ORILLA OCCIDENTAL DEL NILO · EGIPTO" lugares={[
    { nome: "Deir el-Bahari", lat: 25.738, lon: 32.607, cue: "Bahari|Bajari|Bahri|Deir", esquerda: true },
    { nome: "Luxor", lat: 25.700, lon: 32.645, cue: "Luxor|Lúxor" },
  ]} linhas={[{ pontos: NILO }]} tint={colors.accent} />
);

// 5. o corte (p75)
export const R05Corte: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "TOMOGRAFÍA · MOMIA DE RAMSÉS III", titulo: "La herida bajo la laringe", linhas: [
    { rotulo: "Largo del corte", valor: `unos 7${NB}cm`, cue: "7", destaque: true },
    { rotulo: "Profundidad", valor: "hasta el hueso", cue: "hueso" },
  ], tint: "danger" }} />
);

// 6. o Homem Desconhecido E (p103)
export const R06HombreE: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "HOMBRE DESCONOCIDO E · TOMOGRAFÍA", titulo: "Un joven enterrado sin nombre", linhas: [
    { rotulo: "Edad estimada", valor: `entre 18${NB}y${NB}20${NB}años`, cue: "18", destaque: true },
    { rotulo: "Tórax", valor: "inflado, aire retenido", cue: "inflado|tórax|torax" },
  ], tint: "cool" }} />
);

// 7. papiro x osso (p145)
export const R07Dos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "DOS FUENTES INDEPENDIENTES", titulo: "Coinciden en lo esencial", linhas: [
    { rotulo: "Escrita en papiro", valor: "un complot, un juicio", cue: "papiro" },
    { rotulo: "Escrita en hueso", valor: "un rey asesinado", cue: "tomógrafo|tomografo|hueso", destaque: true },
  ], tint: "accent" }} />
);
