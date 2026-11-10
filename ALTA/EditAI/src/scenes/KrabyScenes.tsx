// As animações de "Ryzykują Życie dla Fortuny: Łowcy Krabów na Najgroźniejszym Morzu Świata" (pl, arquivo dark) —
// painel 20261010-013501 (baia 1). REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, FotoMedidor } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
export const FOTO_LOD = "stock/p0383903a.jpg";

// arco das Aleutas (lat, lon; a Rússia fica em lon < -180 para o mapa não dar a volta no globo)
const ALEUTY: [number, number][] = [[58.5, -156.0], [56.0, -160.5], [54.6, -163.5], [53.9, -166.5], [52.8, -169.5],
  [52.0, -173.5], [51.8, -177.0], [51.9, -182.0], [52.9, -187.0]];

// 1. o lugar (p01)
export const A01Morze: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MORZE BERINGA · MIĘDZY ALASKĄ A ROSJĄ" lugares={[
    { nome: "Alaska", lat: 61.2, lon: -149.9, cue: "alask" },
    { nome: "Rosja", lat: 64.7, lon: -182.5, cue: "rosj" },
    { nome: "Wyspy Aleuckie", lat: 52.4, lon: -172.0, cue: "aleuck", abaixo: true },
  ]} linhas={[{ pontos: ALEUTY }]} tint={colors.cool} />
);

// 2. a armadilha (p05)
export const A02Klatka: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Klatka na kraby królewskie · dane NOAA", titulo: "Stalowy sześcian", linhas: [
    { rotulo: "Szerokość z każdej strony", valor: `ok. 2,10${NB}m`, cue: "2" },
    { rotulo: "Wysokość", valor: `ok. 90${NB}cm`, cue: "90" },
    { rotulo: "Pusta waży", valor: `ok. 320${NB}kg`, cue: "320", destaque: true },
    { rotulo: "Nowsze klatki", valor: `ponad 350${NB}kg`, cue: "350" },
  ], tint: "cool" }} />
);

// 3. limite do king crab (p08)
export const A03Limit: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Krab królewski czerwony · Zatoka Bristolska", titulo: "Limit połowu na sezon 2026/27", linhas: [
    { rotulo: "Cała flota", valor: `3,41${NB}mln funtów`, cue: "3", destaque: true },
    { rotulo: "To około", valor: `1550${NB}ton`, cue: "1550" },
    { rotulo: "Rok wcześniej", valor: `2,68${NB}mln funtów`, cue: "2" },
  ], tint: "accent" }} />
);

// 4. mortalidade nos anos 90 (p15)
export const A04Smierc: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FLOTA KRABOWA · DRUGA POŁOWA LAT 90." valor={770} cue="770" sep={NB}
    sufixo={`${NB}zgonów`}
    nota={{ texto: `na 100${NB}000 pracowników na pełny etat · średnio 8${NB}osób rocznie`, cue: "8" }} />
);

// 5. a frota encolhe com as cotas (p19)
export const A05Flota: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="STATKI NA ŁOWISKACH KRABOWYCH · ŚREDNIO ROCZNIE" valor={78} cue="78" sep={NB}
    sufixo={`${NB}statków`}
    barras={[{ rotulo: "2001–2004", v: 243, cue: "243" }, { rotulo: "2005–2010", v: 78, cue: "78", destaque: true }]} />
);

// 7. o gelo da Destination (p35)
export const A07Lod: React.FC<SceneProps> = (p) => (
  <FotoMedidor {...p} foto={FOTO_LOD} de={0} ate={150} unidade={`${NB}ton lodu`} cue="150" efeito="gelo" sep={NB}
    legenda={`od ok. 90 do ponad 150${NB}ton · ok. 4${NB}cm na godzinę`} />
);

// 8. o sumiço do caranguejo-das-neves (p54)
export const A08Miliardy: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="KRABY ŚNIEŻNE · WSCHODNIA CZĘŚĆ MORZA BERINGA" valor={10} cue="10" sep={NB}
    prefixo="ponad " sufixo={`${NB}miliardów`}
    nota={{ texto: "zniknęło od 2018 roku · najniższy poziom w 2021", cue: "2021" }} />
);
