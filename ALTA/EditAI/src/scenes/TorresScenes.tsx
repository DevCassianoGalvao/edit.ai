// Animações de "Como Vivem os Vigias de Torres de Transmissão" (pt, enxuto) — painel 20261027-140006 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Alturas do mastro KVLY (p02)
export const T01Alturas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mastro KVLY · Dakota do Norte", titulo: "Altura do mastro hoje", linhas: [
    { rotulo: "Altura total (desde 2019)", valor: `605,6${NB}m`, cue: "605", destaque: true },
    { rotulo: "Treliça de aço", valor: `590${NB}m`, cue: "590" },
    { rotulo: "Antenas no topo", valor: `16${NB}m`, cue: "16" },
  ], tint: "cool" }} />
);

// 2. MAPA: o mastro de Varsóvia, perto de Gąbin (p09)
export const T02Polonia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MASTRO DE VARSÓVIA · POLÔNIA" lugares={[
    { nome: "Gąbin · Konstantynów", lat: 52.4, lon: 19.78, cue: "gombim" },
  ]} linhas={[
    { pontos: [[54.8, 18.3], [54.4, 19.6], [54.3, 23.0], [52.5, 23.9], [50.8, 24.1], [49.5, 22.7], [49.0, 22.5], [49.4, 19.0],
      [50.1, 18.9], [50.9, 15.0], [51.1, 14.8], [52.5, 14.6], [53.9, 14.2], [54.8, 18.3]] },
  ]} tint={colors.accent} />
);

// 3. A queda de 1991 (p15)
export const T03Queda: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mastro de Varsóvia · o dia da queda", titulo: "8 de agosto de 1991", linhas: [
    { rotulo: "Dia", valor: `8${NB}de agosto`, cue: "8" },
    { rotulo: "Horário (local)", valor: `cerca de 17${NB}h`, cue: "5", destaque: true },
    { rotulo: "Mortos", valor: "ninguém" },
  ], tint: "danger" }} />
);

// 4. Incêndio de Ostankino (p21)
export const T04Moscou: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Torre de Ostankino · Moscou", titulo: "Incêndio de 2000", linhas: [
    { rotulo: "Dia do incêndio", valor: `27${NB}de agosto`, cue: "27" },
    { rotulo: "Altura do fogo (Meduza)", valor: `460${NB}m`, cue: "460", destaque: true },
    { rotulo: "Outras fontes", valor: `475${NB}m`, cue: "475" },
  ], tint: "danger" }} />
);

// 5. Mortes de escaladores nos EUA (p25)
export const T05Mortes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ESCALADORES DE TORRE MORTOS NO TRABALHO · EUA · 9 ANOS" valor={100} prefixo="quase " cue="100"
    sep="." barras={[
      { rotulo: "Em torres de celular", v: 50, cue: "50" },
      { rotulo: "Em outros tipos de torre", v: 43, cue: "43", destaque: true },
    ]} nota={{ texto: `categoria inteira: no máximo 10.000 trabalhadores`, cue: "10" }} />
);

// 6. Salário (p32)
export const T06Salarios: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Escalador de torre · Estados Unidos", titulo: "Quanto se ganha por hora", linhas: [
    { rotulo: "Novato (2007)", valor: `US$${NB}12`, cue: "12" },
    { rotulo: "Veterano com 15 anos", valor: `US$${NB}30`, cue: "30", destaque: true },
    { rotulo: "Média citada depois", valor: `US$${NB}20 a 25`, cue: "20" },
  ], tint: "accent" }} />
);

// 7. Tempestade de gelo de 1997 (p41)
export const T07Gelo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TEMPESTADE DE GELO · 6 DE ABRIL DE 1997 · RAJADAS" valor={113} sufixo={`${NB}km/h`} cue="113"
    sep="." nota={{ texto: "mais de 10 cm de gelo sobre o aço", cue: "113" }} />
);

// 8. Raios por ano (p45)
export const T08Raios: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="EMPIRE STATE BUILDING · RAIOS POR ANO" valor={23} cue="23" sep="."
    nota={{ texto: "Torre de Toronto: cerca de 75 por ano, segundo os operadores", cue: "75" }} />
);

// 9. Torre de TV de Brasília (p48)
export const T09Brasilia: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Torre de TV de Brasília · fontes divergem", titulo: "Altura total", linhas: [
    { rotulo: "Jornal de 1986", valor: `217${NB}m`, cue: "217" },
    { rotulo: "Guias de turismo", valor: `230${NB}m`, cue: "230" },
    { rotulo: "Outras fontes", valor: `244${NB}m`, cue: "244", destaque: true },
  ], tint: "cool" }} />
);

// 10. Os números da resposta (p65)
export const T10Numeros: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Uma torre de seiscentos metros", titulo: "Números extremos", linhas: [
    { rotulo: "Altura", valor: `600${NB}m`, cue: "600" },
    { rotulo: "Aço", valor: `392${NB}toneladas`, cue: "392" },
    { rotulo: "Subida de elevador", valor: `45${NB}minutos`, cue: "45" },
    { rotulo: "Gelo sobre o aço", valor: `10${NB}cm`, cue: "10", destaque: true },
  ], tint: "accent" }} />
);
