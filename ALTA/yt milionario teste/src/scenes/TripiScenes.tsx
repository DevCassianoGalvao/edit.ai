// Animações de "Como Vivem os Marinheiros do Maior Porta-Contêineres do Mundo" (pt) — painel 20261104-135350 (baia b1, enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. o casco (p02)
export const T01Casco: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MSC IRINA · COMPRIMENTO DO CASCO" valor={399} cue="399" sufixo=" metros" sep="."
    nota={{ texto: `e 99${NB}centímetros · quase 400${NB}metros`, cue: "400" }} />
);

// 2. os três gigantes chineses de 2023 (p06)
export const T02Tres: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "COMEÇO DE 2023 · TODOS DE ESTALEIROS CHINESES", titulo: "Os três maiores porta-contêineres", linhas: [
    { rotulo: "MSC Irina · Yangzi Xinfu (Jingjiang)", valor: `24.346${NB}TEU`, cue: "400", destaque: true },
    { rotulo: "OOCL Spain · Nantong", valor: `24.188${NB}TEU`, cue: "24" },
    { rotulo: "MSC Tessa · Hudong-Zhonghua (Xangai)", valor: `24.116${NB}TEU`, cue: "24" },
  ], tint: "accent" }} />
);

// 3. a Convenção do Trabalho Marítimo (p12)
export const T03Descanso: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="10" linhas={[
    "CONVENÇÃO DO TRABALHO MARÍTIMO · 2006",
    "DESCANSO MÍNIMO DE CADA MARINHEIRO",
    "· 10 horas em cada 24 horas",
    "· 77 horas em cada 7 dias",
    "REGISTRADO EM PLANILHA E CONFERIDO NO PORTO",
  ]} chave={3} carimbo={{ texto: "DESCANSO MÍNIMO", cue: "77" }} />
);

// 4. o peso declarado errado (p17)
export const T04Peso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "DECLARAÇÃO ERRADA DE PESO", titulo: "Um contêiner, duas contas", linhas: [
    { rotulo: "Peso declarado", valor: `10${NB}toneladas`, cue: "10" },
    { rotulo: "Peso de verdade", valor: `20${NB}toneladas`, cue: "20", destaque: true },
  ], tint: "accent" }} />
);

// 5. o ponto cego da proa (p26)
export const T05PontoCego: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "CONVENÇÃO SOLAS · VISÃO DO PASSADIÇO", titulo: "Mar escondido à frente da proa", linhas: [
    { rotulo: "Limite da regra", valor: `2× o comprimento ou 500${NB}m`, cue: "500" },
    { rotulo: "Navio de quase 400 m · 2× o comprimento", valor: `quase 800${NB}m`, cue: "800" },
    { rotulo: "Vale o limite menor", valor: `500${NB}m`, cue: "800", destaque: true },
  ], tint: "accent" }} />
);

// 6. MAPA: da China a Malaca (p40)
export const T06Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="A ROTA · DA CHINA AO ESTREITO DE MALACA" lugares={[
    { nome: "Xangai", lat: 31.23, lon: 121.47, cue: "xangai" },
    { nome: "", lat: 22.0, lon: 116.5, cue: "singapura" },
    { nome: "", lat: 10.0, lon: 109.8, cue: "singapura" },
    { nome: "Singapura", lat: 1.26, lon: 103.82, cue: "singapura", abaixo: true },
    { nome: "Estreito de Malaca", lat: 4.2, lon: 99.6, cue: "malac", esquerda: true },
  ]} linhas={[
    { pontos: [[31.6, 121.9], [30.0, 122.1], [28.0, 121.2], [26.0, 119.7], [24.5, 118.5], [23.0, 116.6], [22.4, 114.2],
      [21.5, 111.0], [21.4, 109.5], [20.2, 110.0], [19.0, 108.7], [21.0, 107.5], [18.5, 105.8], [16.0, 108.2], [12.5, 109.3],
      [10.4, 107.2], [8.6, 104.8], [10.3, 104.3], [12.5, 102.5], [13.4, 100.6], [11.0, 99.4], [8.2, 100.4], [6.5, 100.2],
      [4.0, 100.7], [2.5, 101.6], [1.4, 103.6], [1.3, 104.2]] },
    { pontos: [[5.6, 95.3], [4.2, 98.0], [2.8, 99.8], [1.6, 101.4], [0.8, 103.2], [-1.0, 104.5], [-3.5, 105.9]] },
  ]} tint={colors.accent} />
);

// 7. MAPA: a última viagem do MSC Zoe antes da tempestade (p50)
export const T07Zoe: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="MSC ZOE · JANEIRO DE 2019" lugares={[
    { nome: "Sines", lat: 37.95, lon: -8.87, cue: "sines", esquerda: true },
    { nome: "", lat: 43.2, lon: -9.9, cue: "bremerhaven" },
    { nome: "", lat: 48.6, lon: -5.8, cue: "bremerhaven" },
    { nome: "", lat: 50.9, lon: 1.4, cue: "bremerhaven" },
    { nome: "", lat: 53.6, lon: 4.6, cue: "bremerhaven" },
    { nome: "Bremerhaven", lat: 53.55, lon: 8.58, cue: "bremerhaven" },
  ]} linhas={[
    { pontos: [[37.0, -8.9], [38.7, -9.5], [41.1, -8.7], [42.9, -9.3], [43.5, -8.0], [43.5, -3.8], [43.4, -1.6], [46.2, -1.2],
      [47.3, -2.5], [48.4, -4.8], [48.7, -1.6], [49.6, -1.6], [49.4, 0.2], [50.0, 1.4], [50.9, 1.6], [51.3, 3.1], [51.9, 4.1],
      [52.9, 4.7], [53.4, 6.2], [53.6, 8.0], [53.9, 8.7], [54.5, 8.8], [55.5, 8.1]] },
    { pontos: [[50.1, -5.6], [50.6, -3.4], [50.7, -1.2], [50.8, 0.3], [51.1, 1.3], [51.4, 1.4], [52.0, 1.3], [52.9, 1.7]] },
  ]} marca={{ nome: "Ilhas Wadden", lat: 53.45, lon: 5.4, cue: "waden" }} tint={colors.accent} />
);

// 8. ONE Apus (p56)
export const T08Apus: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ONE APUS · NOVEMBRO DE 2020" valor={1816} cue="1" sufixo=" contêineres perdidos" sep="."
    nota={{ texto: `64 com carga perigosa · 54 com fogos de artifício`, cue: "54" }} />
);

// 9. MAPA: os portos do Norte da Europa (p70)
export const T09Portos: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O DESTINO · PORTOS DO NORTE DA EUROPA" lugares={[
    { nome: "Roterdã", lat: 51.95, lon: 4.05, cue: "rotterdam" },
    { nome: "Antuérpia", lat: 51.26, lon: 4.4, cue: "antu", abaixo: true },
    { nome: "Hamburgo", lat: 53.55, lon: 9.99, cue: "hamburgo" },
    { nome: "Bremerhaven", lat: 53.55, lon: 8.58, cue: "bremerhaven", esquerda: true },
    { nome: "Felixstowe", lat: 51.96, lon: 1.35, cue: "felixstowe", esquerda: true },
  ]} linhas={[
    { pontos: [[51.0, 2.0], [51.3, 3.0], [51.6, 3.6], [52.0, 4.1], [52.9, 4.7], [53.4, 6.2], [53.5, 7.2], [53.6, 8.0], [53.9, 8.7], [54.4, 8.9]] },
    { pontos: [[53.9, 10.9], [54.1, 11.8], [54.2, 12.6]] },
    { pontos: [[52.9, 1.7], [52.5, 1.75], [51.95, 1.35], [51.4, 1.4], [51.1, 1.3]] },
  ]} tint={colors.accent} />
);

// 10. os números do MSC Irina (p76)
export const T10Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "OS NÚMEROS DO GIGANTE", titulo: "MSC Irina", linhas: [
    { rotulo: "Comprimento", valor: `quase 400${NB}m`, cue: "400" },
    { rotulo: "Largura", valor: `61,3${NB}m`, cue: "61" },
    { rotulo: "Capacidade", valor: `24.346${NB}TEU`, cue: "24", destaque: true },
  ], tint: "accent", colunas: false }} />
);
