// As animações de "Encerrados en la Fábrica Flotante Más Grande del Mundo: La Brutal Realidad de Prelude, 488 Metros"
// (es, arquivo dark) — painel 20261009-093428 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO;
// todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o gancho (p00)
export const F01Ciudad: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "PRELUDE FLNG · SHELL · AUSTRALIA", titulo: "Una ciudad de acero en mitad del océano", linhas: [
    { rotulo: "De largo", valor: `488${NB}metros`, cue: "488", destaque: true },
    { rotulo: "De la ciudad más cercana", valor: `475${NB}kilómetros`, cue: "475" },
    { rotulo: "Personas a bordo", valor: "más de 200", cue: "200" },
  ], tint: "cool" }} />
);

// 2. o frio (p11)
export const F02Frio: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="GAS NATURAL LICUADO · EL TRUCO" valor={162} cue="162" sep="." prefixo="−" sufixo={`${NB}°C`}
    nota={{ texto: "el líquido ocupa unas 600 veces menos espacio que el gas", cue: "600" }} />
);

// 3. as estacas (p25)
export const F03Pilotes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "SISTEMA DE AMARRE · FONDO MARINO", titulo: "Clavada al fondo del océano", linhas: [
    { rotulo: "Pilotes de acero", valor: "16", cue: "16" },
    { rotulo: "Cada pilote", valor: `65${NB}m de largo · 5,5${NB}m de diámetro`, cue: "65" },
    { rotulo: "Profundidad", valor: `250${NB}metros`, cue: "250", destaque: true },
  ], tint: "cool" }} />
);

// 4. a água do mar (p31)
export const F04Agua: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="PRELUDE · REFRIGERACIÓN CON AGUA DE MAR" valor={50} cue="50" sep="." sufixo={`${NB}millones de litros / hora`}
    nota={{ texto: "como vaciar 20 piscinas olímpicas en lo que dura un café", cue: "20" }} />
);

// 5. os passageiros (p38)
export const F05Pasajeros: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="HELICÓPTEROS DESDE BROOME · PRIMEROS MESES" valor={15000} cue="15" sep="." sufixo={`${NB}pasajeros`}
    nota={{ texto: "la única forma de llegar o salir es el aire", cue: "viajes" }} />
);

// 6. os sócios (p47)
export const F06Socios: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "PRELUDE FLNG · PARTICIPACIÓN", titulo: "Cuatro empresas, cuatro países", linhas: [
    { rotulo: "Shell (operadora)", valor: "67,5 %", cue: "67", destaque: true },
    { rotulo: "Inpex · Japón", valor: "17,5 %", cue: "17" },
    { rotulo: "Kogas · Corea del Sur", valor: "10 %", cue: "10" },
    { rotulo: "CPC · Taiwán", valor: "5 %", cue: "5" },
  ], tint: "accent" }} />
);

// 7. o passeio pela coberta (p58)
export const F07Cubierta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "UN PASEO POR LA CUBIERTA", titulo: "Lo que verías en medio kilómetro", linhas: [
    { rotulo: "Módulos de la planta", valor: "14", cue: "14" },
    { rotulo: "Torreta", valor: `93${NB}metros de altura`, cue: "93", destaque: true },
    { rotulo: "En un extremo", valor: "la antorcha", cue: "antorcha" },
  ], tint: "cool" }} />
);

// 8. o custo da greve (p82)
export const F08Huelga: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "COSTO DEL CONFLICTO · CIFRAS DEL SINDICATO", titulo: "Lo que se perdió en once semanas", linhas: [
    { rotulo: "Primero", valor: `más de 1.100${NB}millones de dólares`, cue: "primero" },
    { rotulo: "Más tarde", valor: `1.300${NB}millones`, cue: "tarde" },
    { rotulo: "Después", valor: `1.500${NB}millones de dólares australianos`, cue: "posterior", destaque: true },
  ], tint: "danger" }} />
);

// 9. o custo total (p93)
export const F09Costo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "PRELUDE · COSTO NUNCA PUBLICADO POR SHELL", titulo: "¿Cuánto costó?", linhas: [
    { rotulo: "Noticia de 2021", valor: `al menos 17.500${NB}millones de dólares`, cue: "17" },
    { rotulo: "Baird Maritime", valor: `17.000 a 19.000${NB}millones`, cue: "maritime", destaque: true },
  ], tint: "danger" }} />
);

// 10. MAPA: uma máquina de vários países (p106)
export const F10Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="UNA SOLA MÁQUINA · VARIOS PAÍSES" lugares={[
    { nome: "Geoje · Corea", lat: 34.88, lon: 128.62, cue: "corea" },
    { nome: "Dubái · la torreta", lat: 25.27, lon: 55.29, cue: "dubai", abaixo: true },
    { nome: "Australia", lat: -13.79, lon: 123.31, cue: "australia", abaixo: true },
    { nome: "Asia · Japón", lat: 35.68, lon: 139.69, cue: "asia" },
  ]} tint={colors.cool} />
);
