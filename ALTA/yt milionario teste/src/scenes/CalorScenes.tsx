// Animações de "Como a Tripulação Sobrevive ao Calor Extremo dos Navios de Carga da Amazônia" (pt) — painel 20261101-111517 (baia b1, enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o que tem fonte e o que não tem (p03)
export const C01Fonte: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A REGRA DESTE VÍDEO · SÓ O QUE TEM FONTE", titulo: "Temperaturas citadas", linhas: [
    { rotulo: "Dentro de navio na Amazônia · medição publicada", valor: `40${NB}°C · nenhuma`, cue: "40" },
    { rotulo: "Portos do norte · ar de fora", valor: `30 a 35${NB}°C`, cue: "30" },
    { rotulo: "Ponte de navio com defeito", valor: `28${NB}°C`, cue: "28", destaque: true },
    { rotulo: "Casa de máquinas tropical · relato geral · pode passar de", valor: `45${NB}°C`, cue: "45" },
  ], tint: "accent", colunas: false }} />
);

// 2. a viagem leva dias (p20)
export const C02Dias: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "BELÉM — MANAUS · NO RIO", titulo: "Quanto tempo leva", linhas: [
    { rotulo: "Barco de passageiros", valor: `cerca de 5${NB}dias`, cue: "5" },
    { rotulo: "Balsa de carga · descendo", valor: `5 a 6${NB}dias`, cue: "6" },
    { rotulo: "Balsa de carga · subindo, contra a correnteza", valor: `7 a 8${NB}dias`, cue: "7", destaque: true },
    { rotulo: "Distância fluvial · estudo de caso", valor: `1.495${NB}km`, cue: "quilômetros" },
  ], tint: "accent", colunas: false }} />
);

// 3. o que as fontes gerais dizem da casa de máquinas (p31)
export const C03Pode: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "CASA DE MÁQUINAS · NAVIOS TROPICAIS", titulo: "Fontes gerais do setor", linhas: [
    { rotulo: "Pode passar de", valor: `45${NB}°C`, cue: "45", destaque: true },
    { rotulo: "Em condições ruins, pode chegar perto de", valor: `50${NB}°C`, cue: "50" },
    { rotulo: "Medição pública num navio da Amazônia", valor: "não existe", cue: "medição" },
  ], tint: "danger" }} />
);

// 4. descanso mínimo (p50)
export const C04Descanso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "CONVENÇÃO DO TRABALHO MARÍTIMO", titulo: "Descanso mínimo", linhas: [
    { rotulo: "Em qualquer período de 24 horas", valor: `10${NB}horas`, cue: "10", destaque: true },
    { rotulo: "Em qualquer período de 7 dias", valor: `77${NB}horas`, cue: "77" },
  ], tint: "accent" }} />
);

// 5. salários médios (p54)
export const C05Salarios: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "ESTIMATIVA DE SITE SALARIAL · MÉDIA NO BRASIL", titulo: "Salário médio por mês", linhas: [
    { rotulo: "Marinheiro de máquinas", valor: `R$${NB}2.724`, cue: "2" },
    { rotulo: "Segundo oficial de máquinas", valor: `R$${NB}8.239`, cue: "8" },
    { rotulo: "Primeiro oficial de máquinas", valor: `R$${NB}9.946`, cue: "9", destaque: true },
    { rotulo: "Imediato · convés", valor: `R$${NB}8.413`, cue: "imediato" },
  ], tint: "accent", colunas: false }} />
);

// 6. MAPA: Manaus -> Santarém (p65)
export const C06Santarem: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O NAVIO QUE SAÍA DE MANAUS" lugares={[
    { nome: "Manaus", lat: -3.12, lon: -60.02, cue: "Manaus", esquerda: true },
    { nome: "Santarém", lat: -2.44, lon: -54.71, cue: "Santarém" },
  ]} tint={colors.accent} />
);

// 7. a faixa legal contra a ponte (p72)
export const C07Faixa: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "NR-17 · CONFORTO TÉRMICO", titulo: "Releia com calma", linhas: [
    { rotulo: "Faixa legal · ambiente climatizado", valor: `18 a 25${NB}°C`, cue: "18" },
    { rotulo: "Lado de fora · portos do norte", valor: `30 a 35${NB}°C`, cue: "30" },
    { rotulo: "Ponte daquele navio", valor: `28${NB}°C`, cue: "28", destaque: true },
    { rotulo: "Acima do limite superior da faixa", valor: `3${NB}graus`, cue: "3" },
  ], tint: "danger", colunas: false }} />
);

// 8. a seca (p78)
export const C08Seca: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "SECA SEVERA · RIO BAIXO", titulo: "Navio da MSC em Manaus", linhas: [
    { rotulo: "Contêineres que chegaram", valor: `140`, cue: "140" },
    { rotulo: "Da capacidade pôde carregar", valor: `≈${NB}10${NB}%`, cue: "10", destaque: true },
  ], tint: "danger" }} />
);

// 9. o balanço (p82)
export const C09Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O BALANÇO · SÓ O QUE TEM FONTE", titulo: "Temperaturas", linhas: [
    { rotulo: "Medição de 40 °C dentro de navio na Amazônia", valor: "nenhuma", cue: "40" },
    { rotulo: "Portos do norte", valor: `30 a 35${NB}°C`, cue: "30" },
    { rotulo: "Ponte com defeito", valor: `28${NB}°C`, cue: "28", destaque: true },
    { rotulo: "Faixa legal climatizada", valor: `18 a 25${NB}°C`, cue: "18" },
    { rotulo: "Casa de máquinas · pode passar de", valor: `45${NB}°C`, cue: "45" },
  ], tint: "accent", colunas: false }} />
);
