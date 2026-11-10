// As 9 animações de "El Hierro, la isla que vive del viento y del agua" (es, ULTRA). Pedido do painel (automático).
// REGRA (25/09 + 26/09/2026): biblioteca + MAPA — MapaCampanha, Odometro, Painel, Lista, Barras, Colunas, LinhaDoTempo,
// MapaRota. Todo número é DITO na narração; cues na grafia do Whisper ("punta de horchilla", "6.000" -> "6",
// "380 mil" -> "380", "2,3" -> cue "megavatios").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, Colunas, LinhaDoTempo, Lista } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. MAPA: o meridiano zero de Orchilla (p02) ----------------
const IBERIA: [number, number][] = [
  [43.4, -1.6], [43.5, -3.8], [43.6, -8.0], [42.9, -9.3], [42.0, -8.9], [40.0, -8.9], [38.7, -9.5], [37.0, -8.9],
  [37.0, -7.4], [36.0, -5.6], [36.7, -4.4], [37.6, -0.7], [39.5, -0.3], [41.4, 2.2], [42.4, 3.2], [43.3, 5.0],
  [43.7, 7.3], [44.4, 8.9], [42.0, 12.0], [40.6, 14.5], [38.0, 15.6], [40.0, 18.5], [41.9, 15.9], [44.0, 12.5],
  [45.6, 13.7], [42.6, 18.0], [40.0, 19.8], [38.0, 21.5], [37.0, 22.8], [38.0, 24.0], [40.6, 23.0], [41.0, 29.0],
];
const FRANCIA: [number, number][] = [
  [43.4, -1.6], [45.5, -1.2], [47.3, -2.5], [48.4, -4.8], [48.7, -1.6], [49.7, -1.9], [49.4, 0.1], [50.9, 1.6], [51.4, 3.5],
];
const BRETANA: [number, number][] = [
  [50.1, -5.6], [50.7, -2.0], [51.1, 1.4], [52.9, 1.7], [53.6, 0.1], [55.9, -2.3], [58.6, -3.0], [57.5, -6.2],
  [55.8, -5.0], [54.6, -3.5], [53.3, -4.6], [51.7, -5.0], [50.1, -5.6],
];
const AFRICA: [number, number][] = [
  [21.0, -17.0], [23.7, -15.9], [26.0, -14.5], [28.5, -11.1], [31.5, -9.8], [34.0, -6.8], [35.8, -5.9], [35.2, -2.0],
  [36.8, 3.0], [37.0, 10.0], [33.8, 10.9], [32.9, 13.2], [30.3, 19.5], [32.8, 22.0], [31.2, 29.9],
];
export const H01Meridiano: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="EL FIN DEL MUNDO CONOCIDO · EL MERIDIANO CERO"
    pontos={[
      { nome: "El Hierro", lat: 27.72, lon: -18.15, data: "PUNTA DE ORCHILLA · MERIDIANO CERO", cue: "horchilla" },
      { nome: "Greenwich", lat: 51.48, lon: 0.0, data: "EL MERIDIANO QUE VINO DESPUÉS", cue: "greenwich" },
      { nome: "Alejandría", lat: 31.2, lon: 29.9, data: "PTOLOMEO · HACE CASI 2.000 AÑOS", cue: "ptolomeo", lado: "esq" },
    ]}
    setas={[
      { de: 2, para: 0, cue: "occidental" },
      { de: 0, para: 1, cue: "greenwich", cor: "#b3161b" },
    ]}
    costa={[IBERIA, FRANCIA, BRETANA, AFRICA]}
  />
);

// ---------------- 2. o gasóleo de cada ano (p09) ----------------
export const H02Gasoleo: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="GASÓLEO QUEMADO CADA AÑO · SOLO PARA LA ELECTRICIDAD"
    valor={6000}
    cue="6"
    sep="."
    sufixo=" toneladas"
    nota={{ texto: "Reserva de la Biosfera de la Unesco desde el año 2000", cue: "2000" }}
  />
);

// ---------------- 7. a central é dos herreños (p14) ----------------
export const H07Cabildo: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Gorona del Viento · la central hidroeólica",
      titulo: "Una central de los propios herreños",
      linhas: [
        { rotulo: "Puesta en marcha", valor: "verano de 2014", cue: "2014" },
        { rotulo: "Funcionamiento pleno", valor: "2015", cue: "2015" },
        { rotulo: "Coste", valor: "82 millones de euros", cue: "82" },
        { rotulo: "Cabildo de El Hierro", valor: "dos tercios", cue: "tercios", destaque: true },
      ],
      tint: "accent",
    }}
  />
);

// ---------------- 3. os cinco molinos (p16) ----------------
export const H03Gorona: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="GORONA DEL VIENTO · EL PARQUE EÓLICO"
    titulo="Cinco molinos para una isla"
    tint={colors.cool}
    itens={[
      { titulo: "Cinco aerogeneradores blancos", cue: "aerogeneradores" },
      { titulo: "2,3 megavatios cada uno", cue: "megavatios" },
      { titulo: "Más de 11 megavatios en total", cue: "11" },
      { titulo: "El sobrante sube el agua montaña arriba", cue: "bombas", cor: colors.accent },
    ]}
  />
);

// ---------------- 4. os dois depósitos (p17) ----------------
export const H04Depositos: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="LA CALDERA DE LA HOYA DEL MORCILLO"
    titulo="Dos depósitos de agua"
    tint={colors.cool}
    max={400}
    barras={[
      { rotulo: "Depósito superior · el cráter", valor: "380.000 m³", v: 380, cue: "380", cor: colors.cool },
      { rotulo: "Depósito inferior · junto a la central", valor: "150.000 m³", v: 150, cue: "150" },
    ]}
    nota={{ texto: "más de 650 metros de diferencia de altura", cue: "650" }}
  />
);

// ---------------- 5. o ciclo: o vento guardado em água (p18) ----------------
export const H05Ciclo: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="CUANDO EL VIENTO SE CALMA"
    tint={colors.accent}
    cols={[
      { titulo: "Se abren las compuertas", texto: "del depósito superior", cue: "compuertas", cor: colors.cool },
      { titulo: "Cuatro turbinas Pelton", texto: "el agua baja con una fuerza tremenda", cue: "pelton", cor: colors.cool },
      { titulo: "Electricidad a la red", texto: "el viento, guardado en forma de agua", cue: "inyectan", cor: colors.accent },
    ]}
    nota={{ texto: "la energía del viento, guardada en agua elevada", cue: "elevada" }}
  />
);

// ---------------- 6. os 24 dias (p23) ----------------
export const H06Dias: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="VERANO DE 2019 · SOLO ENERGÍA RENOVABLE"
    valor={24}
    cue="24"
    sufixo=" días seguidos"
    nota={{ texto: "11.000 personas sin quemar petróleo para la luz", cue: "personas" }}
  />
);

// ---------------- 8. Tagoro, o vulcão submarino (p46) ----------------
export const H08Tagoro: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="TAGORO · EL VOLCÁN SUBMARINO DE LA RESTINGA"
    tint={colors.accent}
    marcos={[
      { ano: "Tagoro", texto: "el nombre del volcán", cue: "tagoro" },
      { ano: "2012", texto: "deja de estar activo", cue: "2012" },
      { ano: "Pocos años", texto: "la vida vuelve al mar", cue: "vida" },
      { ano: "Hoy", texto: "uno de los volcanes submarinos más estudiados", cue: "estudiados", cor: colors.accent },
    ]}
  />
);

// ---------------- 9. MAPA: a Bajada, da Dehesa a Valverde (p48) ----------------
const ISLA: [number, number][] = [
  [27.85, -17.99], [27.83, -17.93], [27.82, -17.88], [27.78, -17.88], [27.76, -17.89], [27.72, -17.97], [27.64, -17.98],
  [27.67, -18.02], [27.70, -18.05], [27.71, -18.15], [27.74, -18.16], [27.76, -18.10], [27.76, -18.06], [27.79, -18.02],
  [27.85, -17.99],
];
export const H09Bajada: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="BAJADA DE LA VIRGEN DE LOS REYES · CADA CUATRO AÑOS"
    lugares={[
      { nome: "La Dehesa · santuario", lat: 27.72, lon: -18.12, valor: 0, cue: "dehesa" },
      { nome: "Valverde", lat: 27.81, lon: -17.915, valor: 44, cue: "44" },
    ]}
    unidade="km"
    linhas={[{ pontos: ISLA }]}
    tint={colors.accent}
  />
);
