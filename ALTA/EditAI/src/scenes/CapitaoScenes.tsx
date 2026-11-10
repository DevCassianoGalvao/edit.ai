// Animações de "Como o Capitão de um Navio de 400 Metros Come, Toma Banho e Dorme" (pt) — painel 20261013-232836
// (baia 1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. MSC Irina (p01)
export const C01Irina: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O maior porta-contêineres do mundo", titulo: "MSC Irina", linhas: [
    { rotulo: "Comprimento", valor: `399,99${NB}m`, cue: "399", destaque: true },
    { rotulo: "Largura", valor: `61,30${NB}m`, cue: "61" },
    { rotulo: "Entregue", valor: "9 de março de 2023", cue: "9" },
  ], tint: "accent" }} />
);

// 2. MAPA: a viagem do contrato (p06)
export const C02Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O CONTRATO DO CAPITÃO · ABRIL DE 2025" lugares={[
    { nome: "Singapura", lat: 1.29, lon: 103.85, cue: "singapura", abaixo: true },
    { nome: "China", lat: 29.9, lon: 121.6, cue: "china", esquerda: true },
    { nome: "Coreia", lat: 35.1, lon: 129.0, cue: "coreia" },
  ]} marca={{ nome: "Vizhinjam · Kerala", lat: 8.38, lon: 76.99, nota: "a casa do capitão", cue: "voltou" }}
    tint={colors.accent} />
);

// 3. a visão da proa (p13)
export const C03Proa: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="DO PASSADIÇO, PELAS REGRAS INTERNACIONAIS" valor={500} cue="500" sufixo={`${NB}m de mar à frente`} sep="."
    nota={{ texto: "por cima de fileiras de contêineres", cue: "fileiras" }} />
);

// 4. quartos de serviço (p21)
export const C04Quartos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quartos de serviço no passadiço", titulo: "4 horas por 8", linhas: [
    { rotulo: "Serviço", valor: "4 horas", cue: "4", destaque: true },
    { rotulo: "Descanso", valor: "8 horas", cue: "8" },
    { rotulo: "Por dia", valor: "2 vezes", cue: "duas" },
  ], tint: "accent" }} />
);

// 5. relatório do meio-dia (p29)
export const C05Relatorio: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="posicao" linhas={[
    "RELATÓRIO DO MEIO-DIA · PARA A EMPRESA EM TERRA",
    "· Posição do navio",
    "· Distância nas últimas 24 horas",
    "· Consumo de combustível",
    "· Velocidade média · tempo · chegada",
  ]} chave={2} carimbo={{ texto: "ENVIADO", cue: "empresa" }} />
);

// 6. refeições por ano (p42)
export const C06Refeicoes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UM COZINHEIRO · UM ANO INTEIRO A BORDO" valor={27375} cue="27" sufixo=" refeições" sep="."
    nota={{ texto: "34 pessoas · quase sozinho na cozinha", cue: "34" }} />
);

// 7. água fervendo no vácuo (p48)
export const C07Vacuo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="GERADOR DE ÁGUA DOCE · A ÁGUA DO MAR FERVE A" valor={40} cue="40" sufixo={`${NB}a 60${NB}°C`} sep="."
    barras={[{ rotulo: "Ao nível do mar (°C)", v: 100, cue: "100" }, { rotulo: "No vácuo (°C)", v: 40, cue: "40", destaque: true }]} />
);

// 8. descanso mínimo (p60)
export const C08Descanso: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Convenção do Trabalho Marítimo", titulo: "Descanso mínimo", linhas: [
    { rotulo: "A cada 24 horas", valor: "10 horas", cue: "10", destaque: true },
    { rotulo: "A cada 7 dias", valor: "77 horas", cue: "77" },
  ], tint: "accent" }} />
);

// 9. meia-volta no Havre (p68)
export const C09Havre: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="LE HAVRE · MEIA-VOLTA DE 180°" valor={700} cue="700" sufixo={`${NB}m de círculo`} sep="."
    nota={{ texto: "rebocadores de 70 a 80 toneladas de força", cue: "70" }} />
);

// 10. internet a bordo (p79)
export const C10Internet: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="25" linhas={[
    "RELATÓRIO DE 2021 · INTERNET A BORDO",
    "· Um marítimo: 25 dólares por 100 megabytes",
    "· Outro: 250 megabytes por mês",
    "",
    "· Nem chamada de vídeo com a família",
  ]} chave={1} carimbo={{ texto: "SEM CONEXÃO", cue: "250" }} />
);

// 11. salário do comandante (p86)
export const C11Salario: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Comandante de porta-contêineres · por mês embarcado", titulo: "Quanto ganha", linhas: [
    { rotulo: "De", valor: `US$${NB}9.200`, cue: "9" },
    { rotulo: "Até", valor: `US$${NB}10.500`, cue: "10", destaque: true },
  ], tint: "accent" }} />
);
