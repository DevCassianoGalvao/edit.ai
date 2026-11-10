// Animações de "Dentro de un tanque de guerra: cómo comían, dormían y soportaban el calor" (es, enxuto) — painel
// 20261016-161735-audio-guerra (baia b1). REGRA: biblioteca + MAPA; motion curto (cues <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro, FotoMedidor } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
export const FOTO_FRIO = "stock/pce49a6a4.jpg";

// 1. três tanques médios (p01)
export const T01Peso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Tanques medios · Segunda Guerra Mundial", titulo: "Casi todo era acero", linhas: [
    { rotulo: "Estados Unidos", valor: "Sherman", cue: "sherman" },
    { rotulo: "Alemania", valor: "Panzer IV", cue: "panzer" },
    { rotulo: "Unión Soviética", valor: "T-34", cue: "soviético" },
    { rotulo: "Tripulación", valor: `5${NB}hombres`, cue: "cinco" },
    { rotulo: "Peso", valor: `30 a 40${NB}toneladas`, cue: "40", destaque: true },
  ], tint: "accent" }} />
);

// 2. MAPA do calor (p09)
export const T02Calor: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker={`VERANO · MÁS DE 50${NB}°C DENTRO DEL TANQUE`} lugares={[
    { nome: "Norte de África", lat: 30.83, lon: 28.95, cue: "áfrica", abaixo: true },
    { nome: "Sur de Italia", lat: 40.68, lon: 14.77, cue: "italia", esquerda: true },
    { nome: "Estepa rusa", lat: 51.73, lon: 36.19, cue: "estepas" },
  ]} tint={colors.danger} />
);

// 3. gases da pólvora (p16)
export const T03Gases: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "La torreta cerrada · después de cada disparo", titulo: "Un gas invisible", linhas: [
    { rotulo: "Gas", valor: "monóxido de carbono", cue: "invisible" },
    { rotulo: "Poca dosis", valor: "dolor de cabeza y náuseas", cue: "náuseas" },
    { rotulo: "Mucha dosis", valor: "desmayo", cue: "desmayo", destaque: true },
  ], tint: "accent" }} />
);

// 4. a ração (p25)
export const T04Racion: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="latas" chave={2} linhas={[
    "RACIÓN DE CAMPAÑA · CONTENIDO",
    "",
    "Latas de carne en conserva",
    "Galletas duras",
    "Queso · chocolate",
    "Café o té en polvo · azúcar",
    "Cigarrillos",
  ]} carimbo={{ texto: "RACIÓN ENVASADA", cue: "cigarrillos" }} />
);

// 5. Pervitin (p31)
export const T05Pervitin: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="tabletas" chave={3} linhas={[
    "EJÉRCITO ALEMÁN · ESTIMULANTES",
    "",
    "Tabletas de metanfetamina",
    "Nombre comercial: Pervitin",
    "Mantenían despiertos a los hombres",
  ]} carimbo={{ texto: "A COSTA DE SU SALUD", cue: "salud" }} />
);

// 6. microsono (p38)
export const T06Sueno: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Agotamiento acumulado", titulo: "Microsueños", linhas: [
    { rotulo: "Sueño por noche", valor: `3 o 4${NB}horas`, cue: "cuatro" },
    { rotulo: "Microsueño", valor: "unos segundos", cue: "segundos" },
    { rotulo: "La mente", valor: "se apaga sin avisar", cue: "apaga", destaque: true },
  ], tint: "cool" }} />
);

// 7. frio do leste (p50)
export const T07Frio: React.FC<SceneProps> = (p) => (
  <FotoMedidor {...p} foto={FOTO_FRIO} de={0} ate={-40} unidade={`${NB}°C`} cue="40" efeito="gelo"
    legenda="Frente del este · invierno ruso · 30 o 40 grados bajo cero" />
);

// 8. MAPA: verão africano x inverno russo (p56)
export const T08Estaciones: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DOS ESTACIONES · ¿CUÁL ERA PEOR?" lugares={[
    { nome: "Verano africano", lat: 30.83, lon: 28.95, cue: "africano", abaixo: true },
    { nome: "Invierno ruso", lat: 55.75, lon: 37.62, cue: "ruso" },
  ]} tint={colors.cool} />
);

// 9. o sono depois (p68)
export const T09Dormir: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="AL LLEGAR A UN LUGAR SEGURO · HORAS SEGUIDAS DE SUEÑO" valor={14} cue="14" prefixo="12 o "
    sufixo={`${NB}horas`} sep="." nota={{ texto: "sin soñar, sin moverse", cue: "moverse" }} />
);
