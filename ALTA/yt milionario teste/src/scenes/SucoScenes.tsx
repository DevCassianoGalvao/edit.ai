// Animações de "Como um Único Navio Leva 32 Mil Toneladas de Suco de Laranja" (pt) — painel 20261021-102113
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. a safra do cinturão citrícola (p01)
export const S01Safra: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CINTURÃO CITRÍCOLA · SAFRA 2025/2026 · FUNDECITRUS" valor={292940000} cue="292" sufixo=" caixas" sep="."
    nota={{ texto: "cada caixa: 40,8 kg de laranja", cue: "40" }} />
);

// 2. o sistema a granel (p13)
export const S02Granel: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="1972" linhas={[
    "1972 · PURDUE PATENTEIA O ARMAZENAMENTO ASSÉPTICO A GRANEL",
    "1982 · A CITROSUCO MONTA O SISTEMA INTEGRADO",
    "· fazendas de tanques",
    "· terminal de exportação em Santos",
    "· navios especiais · terminal na Europa",
  ]} chave={1} carimbo={{ texto: "A GRANEL", cue: "1982" }} />
);

// 3. 32 mil toneladas em copos (p20)
export const S03Copos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="32 MIL TONELADAS DE SUCO EM COPOS DE 250 ML" valor={100} cue="100" prefixo="+" sufixo=" milhões de copos" sep="."
    nota={{ texto: "num único navio", cue: "250" }} />
);

// 4. a temperatura do concentrado (p34)
export const S04Frio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A temperatura certa", titulo: "Suco concentrado", linhas: [
    { rotulo: "Viaja a", valor: `−10${NB}°C`, cue: "10", destaque: true },
    { rotulo: "Consistência", valor: "pasta · mingau", cue: "pasta" },
  ], tint: "accent" }} />
);

// 5. a tripulação (p49)
export const S05Tripulacao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quem faz a fábrica funcionar", titulo: "Carlos Fischer", linhas: [
    { rotulo: "Acomodação", valor: "30 pessoas", cue: "30", destaque: true },
    { rotulo: "Navio", valor: `+200${NB}m`, cue: "200" },
    { rotulo: "Tanques de suco refrigerado", valor: "16", cue: "16" },
  ], tint: "accent" }} />
);

// 6. o calado (p61)
export const S06Calado: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quanto o casco afunda carregado", titulo: "Calado", linhas: [
    { rotulo: "Operação normal", valor: `9,5${NB}m`, cue: "9", destaque: true },
    { rotulo: "Limite de projeto", valor: `11,40${NB}m`, cue: "11" },
  ], tint: "accent" }} />
);

// 7. MAPA: os terminais da Citrosuco (p69)
export const S07Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="TERMINAIS MARÍTIMOS DA CITROSUCO" lugares={[
    { nome: "Santos", lat: -23.96, lon: -46.31, cue: "santos", abaixo: true },
    { nome: "Wilmington", lat: 39.72, lon: -75.53, cue: "wilmington", esquerda: true },
    { nome: "Ghent", lat: 51.05, lon: 3.72, cue: "ghent" },
  ]} marca={{ nome: "Toyohashi · Japão", lat: 34.77, lon: 137.39, cue: "toyohashi" }}
    tint={colors.accent} />
);

// 8. biodiesel B24 (p84)
export const S08Biodiesel: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Santos · agosto de 2025", titulo: "Biodiesel B24", linhas: [
    { rotulo: "Carregado", valor: "500 toneladas", cue: "500", destaque: true },
    { rotulo: "Combustível renovável", valor: "24%", cue: "24" },
  ], tint: "accent" }} />
);

// 9. greening (p91)
export const S09Greening: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Fundecitrus · setembro de 2025", titulo: "Greening", linhas: [
    { rotulo: "Laranjeiras contaminadas", valor: "100 milhões", cue: "100", destaque: true },
    { rotulo: "Total do cinturão", valor: "209 milhões", cue: "209" },
  ], tint: "accent" }} />
);

// 10. o motor (p104)
export const S10Motor: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Oitavo: a velocidade", titulo: "Wärtsilä Sulzer", linhas: [
    { rotulo: "Cilindros", valor: "7", cue: "7" },
    { rotulo: "Potência", valor: "38.570 cv", cue: "38", destaque: true },
    { rotulo: "Velocidade", valor: "quase 21 nós", cue: "21" },
  ], tint: "accent" }} />
);
