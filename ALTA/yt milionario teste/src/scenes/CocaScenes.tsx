// Animações de "Como é a Vida num Submarino de Cocaína?" (pt) — painel 20261022-125356
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// costas (lat, lon) para o mapa do Atlântico
const AMERICA_SUL: [number, number][] = [[10.6, -66.9], [10.5, -61.5], [8.5, -59.8], [6.8, -58.2], [5.8, -55.2], [4.9, -52.3],
  [4.2, -51.6], [1.8, -50.0], [0.0, -50.0], [-0.7, -48.5], [-1.3, -48.5], [-0.6, -47.3], [-2.5, -44.3], [-2.9, -41.5],
  [-3.7, -38.5], [-5.2, -35.5], [-8.0, -34.9], [-10.9, -37.0], [-13.0, -38.5]];
const AFRICA: [number, number][] = [[35.8, -5.9], [33.6, -7.6], [31.5, -9.8], [30.4, -9.6], [28.0, -12.0], [26.1, -14.5],
  [24.0, -15.9], [21.0, -17.0], [18.0, -16.0], [14.7, -17.4], [12.5, -16.7], [10.5, -15.0], [8.5, -13.2], [6.3, -10.8],
  [4.4, -7.5], [5.2, -4.0], [5.6, -0.2], [6.4, 3.4]];
const IBERIA: [number, number][] = [[36.1, -5.35], [36.5, -6.3], [37.2, -7.4], [37.0, -8.0], [37.0, -9.0], [38.0, -8.9],
  [38.7, -9.45], [39.4, -9.4], [40.6, -8.75], [41.15, -8.7], [41.9, -8.88], [42.9, -9.3], [43.4, -8.4], [43.75, -7.7],
  [43.55, -5.7], [43.45, -3.8], [43.35, -1.8], [44.6, -1.2], [46.2, -1.4], [47.3, -2.5], [47.8, -4.3], [48.4, -4.8]];
// Rías Baixas: ría de Vigo (sul e norte), Morrazo, ría de Aldán, ría de Pontevedra
const RIAS: [number, number][] = [[42.12, -8.85], [42.17, -8.82], [42.21, -8.77], [42.24, -8.72], [42.27, -8.66], [42.29, -8.61],
  [42.27, -8.70], [42.255, -8.78], [42.26, -8.85], [42.25, -8.875], [42.29, -8.875], [42.285, -8.82], [42.30, -8.86],
  [42.33, -8.85], [42.33, -8.79], [42.39, -8.70], [42.43, -8.64], [42.40, -8.81], [42.45, -8.90], [42.49, -8.86]];

// 1. o casco (p04)
export const A01Casco: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Semissubmersível · fibra de vidro feita à mão", titulo: "O casco do Che", linhas: [
    { rotulo: "Comprimento", valor: `cerca de 20${NB}m`, cue: "20", destaque: true },
    { rotulo: "Outros relatos", valor: `21,5 a 22${NB}m`, cue: "21" },
    { rotulo: "Largura", valor: `cerca de 3${NB}m`, cue: "3" },
  ], tint: "accent" }} />
);

// 2. o preço x a carga (p08)
export const A02Preco: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VALOR DA CARGA · JUSTIÇA ESPANHOLA" valor={123244573} cue="123" prefixo="€ " sep="."
    nota={{ texto: "o submarino custou cerca de 1 milhão de euros", cue: "1" }} />
);

// 3. a evolução dos narcossubmarinos (p13)
export const A03Evolucao: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="cartagena" linhas={[
    "MARINHA DA COLÔMBIA · NARCOSSUBMARINOS",
    "1993 · O PRIMEIRO APREENDIDO, NA COLÔMBIA",
    "CARTAGENA · AMARELO, LARGO, QUASE UMA BANHEIRA",
    "1995 / 1996 · MAIS COMPRIDO E CILÍNDRICO",
    "2019 · O CHE ATRAVESSA O ATLÂNTICO",
  ]} chave={4} carimbo={{ texto: "EVOLUÇÃO", cue: "amarelo" }} />
);

// 4. o pagamento dos primos (p19)
export const A04Pagamento: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O preço de uma vida na operação", titulo: "Pagamento de cada primo", linhas: [
    { rotulo: "Prometido", valor: `55 mil dólares`, cue: "55", destaque: true },
    { rotulo: "Adiantado", valor: `5 mil dólares`, cue: "5" },
    { rotulo: "Só depois da entrega", valor: `50 mil dólares`, cue: "50" },
  ], tint: "accent" }} />
);

// 5. MAPA: o plano da travessia (p26)
export const A05Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O PLANO: DA FOZ DO AMAZONAS AO ALTO-MAR DE LISBOA" lugares={[
    { nome: "Foz do Amazonas", lat: 0.0, lon: -50.0, cue: "rio", abaixo: true },
    { nome: "", lat: 20.0, lon: -33.0, cue: "oceano" },
    { nome: "Encontro · 269 milhas", lat: 38.7, lon: -15.2, cue: "269", esquerda: true },
  ]} marca={{ nome: "Lisboa", lat: 38.72, lon: -9.14, cue: "269" }}
    linhas={[{ pontos: AMERICA_SUL }, { pontos: AFRICA }, { pontos: IBERIA }]}
    tint={colors.accent} />
);

// 6. a cabine (p37)
export const A06Cabine: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="barulho" linhas={[
    "DENTRO DA CABINE · A ROTINA",
    `ESPAÇO · 2${NB}m² PARA TRÊS HOMENS`,
    "COMIDA · SARDINHA, ARROZ E BOLACHA",
    "BANHEIRO · UMA SACOLA PLÁSTICA",
    "AR · FUMAÇA E GASES DO DIESEL",
    "UMIDADE · NEOPRENE QUE ABRE FERIDAS",
    `BARULHO · MOTOR DE 240${NB}CV SEM PARAR`,
  ]} chave={6} carimbo={{ texto: "NENHUM DESCANSO", cue: "descanso" }} />
);

// 7. o encontro (p49)
export const A07Encontro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Alto-mar, ao largo de Portugal", titulo: "O ponto de encontro", linhas: [
    { rotulo: "Distância de Lisboa", valor: "269 milhas", cue: "269", destaque: true },
    { rotulo: "Chegada do Che", valor: "9 dias de atraso", cue: "nove" },
  ], tint: "accent" }} />
);

// 8. o plano desmorona (p55)
export const A08Plano: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="primeiro" linhas={[
    "OPERAÇÃO CHE · O QUE DEU ERRADO",
    "· ATRASO NA PARTIDA, SEM CAPITÃO",
    "· TEMPESTADES DOBRAM A VIAGEM",
    "· LANCHA QUEBRADA",
    "· LANCHAS SEM COMBUSTÍVEL",
    "· TELEFONEMA ENTREGA A POSIÇÃO",
    "· NINGUÉM BUSCA A CARGA NA GALÍCIA",
  ]} chave={5} carimbo={{ texto: "FRACASSO", cue: "combustível" }} />
);

// 9. MAPA: Punta Couso e a ría de Aldán (p67)
export const A09Aldan: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O NAUFRÁGIO · PENÍNSULA DO MORRAZO, GALÍCIA" lugares={[
    { nome: "", lat: 42.31, lon: -8.97, cue: "pedras" },
    { nome: "Punta Couso", lat: 42.30, lon: -8.86, cue: "couso", esquerda: true },
    { nome: "Ría de Aldán", lat: 42.285, lon: -8.83, cue: "aldan", abaixo: true },
  ]} linhas={[{ pontos: RIAS }]}
    tint={colors.accent} />
);

// 10. a conta da travessia (p78)
export const A10Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Do Brasil até a Galícia", titulo: "A conta da travessia", linhas: [
    { rotulo: "Distância", valor: "mais de 3.500 milhas", cue: "3", destaque: true },
    { rotulo: "Em quilômetros", valor: "cerca de 6.500 km", cue: "6" },
    { rotulo: "Duração", valor: "27 dias", cue: "27" },
  ], tint: "accent" }} />
);

// 11. a conta final (p84)
export const A11Final: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quem vai no submarino é a peça mais barata", titulo: "A conta final", linhas: [
    { rotulo: "Dentro da caixa de fibra", valor: "27 dias", cue: "27" },
    { rotulo: "Pena de cada tripulante", valor: "11 anos", cue: "11", destaque: true },
  ], tint: "accent" }} />
);
