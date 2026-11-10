// Animações de "Motor de Popa Elétrico Dá Conta de Pescaria?" (pt, enxuto) — painel 20261029-132218 (b1).
// REGRA: biblioteca (Painel); motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { colors } from "../design/tokens";
import { SceneProps } from "./shared";

const NB = " ";

// 1. Preços na classe de 6 cavalos (p02)
export const P01Precos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Classe de 6${NB}cavalos · gasolina custava US$${NB}1.900`, titulo: "Quanto custava o elétrico", linhas: [
    { rotulo: "ePropulsion, com bateria e carregador", valor: `US$${NB}6.100`, cue: "6" },
    { rotulo: "Torqeedo, com bateria e carregador", valor: `US$${NB}7.896`, cue: "7", destaque: true },
    { rotulo: "Só de diferença sobre a gasolina", valor: `US$${NB}4.200 a 6.000`, cue: "4" },
  ], tint: "accent" }} />
);

// 2. Tempo de recarga (p18)
export const P02Recarga: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Torqeedo Cruise · carregador padrão de 350${NB}W`, titulo: "Quanto leva para encher a bateria", linhas: [
    { rotulo: "Carregador padrão", valor: `12${NB}horas`, cue: "12", destaque: true },
    { rotulo: "Carregadores mais rápidos", valor: `4 a 6${NB}horas`, cue: "4" },
  ], tint: "cool" }} />
);

// 3. Gasto de combustível: 1 ano e 10 anos (p23)
export const P03Gasto: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mercury a gasolina x Torqeedo elétrico", titulo: "Energia gasta no uso", linhas: [
    { rotulo: "Gasolina · 1 ano", valor: `US$${NB}600`, cue: "600" },
    { rotulo: "Eletricidade · 1 ano", valor: `US$${NB}24`, cue: "24" },
    { rotulo: "Gasolina · 10 anos", valor: `US$${NB}6.006`, cue: "6", destaque: true },
    { rotulo: "Eletricidade · 10 anos", valor: `US$${NB}240`, cue: "240" },
  ], tint: "cool" }} />
);

// 4. Manutenção do a gasolina (p31)
export const P04Manut: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Motor a gasolina · manutenção", titulo: "O que o a gasolina cobra", linhas: [
    { rotulo: `Revisão a cada 100 a 150${NB}horas`, valor: `US$${NB}200`, cue: "100" },
    { rotulo: `Impelidor a cada 300${NB}horas`, valor: `US$${NB}200`, cue: "300" },
    { rotulo: "Estimativa por ano", valor: `US$${NB}300`, cue: "300", destaque: true },
  ], tint: "accent" }} />
);

// 5. Peso do conjunto (p37)
export const P05Peso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Peso do conjunto pronto para pescar", titulo: "Gasolina x elétrico", linhas: [
    { rotulo: "A gasolina, com o tanque", valor: `37${NB}kg`, cue: "37" },
    { rotulo: "O elétrico, com a bateria", valor: `57${NB}kg`, cue: "57", destaque: true },
    { rotulo: "Diferença", valor: `20${NB}kg`, cue: "20" },
  ], tint: "cool" }} />
);

// 6. A conta do pescador de rio (p65)
export const P06Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: `Pescador de rio · 6${NB}horas por dia`, titulo: "A conta da gasolina", linhas: [
    { rotulo: "Galões por dia", valor: "3", cue: "3" },
    { rotulo: "Combustível por dia", valor: `US$${NB}12`, cue: "12" },
    { rotulo: "Dias de pesca por ano", valor: "200", cue: "200" },
    { rotulo: "Gasolina por ano", valor: `US$${NB}2.400`, cue: "2", destaque: true },
  ], tint: "accent" }} />
);

// 7. Motor e bateria do Torqeedo Cruise (p69)
export const P07Bateria: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Torqeedo Cruise · o custo escondido", titulo: "A bateria pesa no preço", linhas: [
    { rotulo: "Motor", valor: `US$${NB}5.759`, cue: "5" },
    { rotulo: "Bateria sozinha", valor: `US$${NB}4.019`, cue: "4", destaque: true },
    { rotulo: "Bateria do ePropulsion", valor: `48${NB}volts`, cue: "48" },
  ], tint: "danger" }} />
);

// 8. Exemplo completo: represa, 8 km (p78)
export const P08Exemplo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Exemplo completo · represa grande", titulo: "Os dados do trajeto", linhas: [
    { rotulo: "Distância até a enseada", valor: `8${NB}km`, cue: "8" },
    { rotulo: "Barco de alumínio", valor: `5${NB}m`, cue: "5" },
    { rotulo: "Pescadores a bordo", valor: "2", cue: "2" },
    { rotulo: "Motor elétrico", valor: `3${NB}kW`, cue: "3", destaque: true },
  ], tint: "cool" }} />
);

// 9. Motores maiores (p89)
export const P09Grandes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Motores maiores · preço de compra", titulo: "Gasolina x elétrico", linhas: [
    { rotulo: `40${NB}cavalos a gasolina`, valor: `US$${NB}8.346`, cue: "8" },
    { rotulo: "Elétrico Deep Blue, com bateria", valor: `US$${NB}29.000`, cue: "29", destaque: true },
    { rotulo: `80${NB}cavalos a gasolina`, valor: `US$${NB}12.744`, cue: "12" },
    { rotulo: "Elétrico equivalente", valor: `US$${NB}37.900`, cue: "37", destaque: true },
  ], tint: "danger" }} />
);

// contorno aproximado do Brasil, só como referência do mapa
const BRASIL: [number, number][] = [[5.2, -60.0], [4.4, -51.6], [2.0, -50.8], [-0.5, -48.0], [-1.5, -44.7], [-2.8, -40.5], [-5.0, -35.5],
  [-8.0, -34.8], [-13.0, -38.5], [-18.0, -39.7], [-23.0, -41.8], [-23.5, -45.5], [-25.5, -48.5], [-29.0, -49.8], [-32.0, -52.5],
  [-33.7, -53.4], [-30.0, -57.6], [-28.0, -56.0], [-25.5, -54.5], [-22.0, -57.8], [-19.0, -58.0], [-16.0, -60.0], [-13.0, -60.5],
  [-10.5, -65.5], [-9.8, -70.5], [-7.5, -73.9], [-4.0, -70.0], [-1.0, -69.5], [1.2, -69.6], [2.0, -67.0], [4.2, -64.0], [5.2, -60.7]];

// 10. MAPA: o elétrico chega ao Brasil (p40)
export const P10Brasil: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="YAMAHA NÁUTICA · MOTORES ELÉTRICOS TORQEEDO NO BRASIL" lugares={[
    { nome: "Brasil", lat: -14.2, lon: -51.9, cue: "brasil" },
  ]} linhas={[{ pontos: BRASIL }]} tint={colors.accent} />
);
