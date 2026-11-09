// Animações de "Como 7 Homens Cruzam 360 km do Pantanal a Cavalo com 1.350 Bois numa Comitiva" (pt) — painel
// 20261023-234309 (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// rios do Pantanal (lat, lon) — aproximados para o mapa
const RIO_PARAGUAI: [number, number][] = [[-16.07, -57.68], [-16.6, -57.75], [-17.3, -57.55], [-17.85, -57.5], [-18.4, -57.55],
  [-19.0, -57.65], [-19.6, -57.45], [-20.2, -57.95], [-20.9, -57.85], [-21.7, -57.88]];
const RIO_TAQUARI: [number, number][] = [[-18.49, -54.75], [-18.6, -55.2], [-18.75, -55.7], [-18.9, -56.2], [-19.05, -56.8],
  [-19.15, -57.45]];
const RIO_AQUIDAUANA: [number, number][] = [[-20.47, -55.4], [-20.47, -55.79], [-20.2, -56.3], [-19.95, -56.8], [-19.75, -57.3]];
const RIO_CUIABA: [number, number][] = [[-15.6, -56.1], [-16.4, -56.4], [-17.0, -56.6], [-17.4, -56.9], [-17.85, -57.5]];

// 1. o valor da boiada (p03)
export const A01Valor: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="O QUE ANDA NO MEIO DO MATO" valor={4000000} cue="4" prefixo="R$ " sep="." sufixo=""
    nota={{ texto: `cerca de 3 mil reais por animal · 1.350 animais`, cue: "3" }} />
);

// 2. MAPA: onde o caminhão não entra (p10)
export const A02Regioes: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="PANTANAL · ONDE MAIS EXISTE GADO" lugares={[
    { nome: "Paiaguás", lat: -18.3, lon: -56.6, cue: "paiagu" },
    { nome: "Nhecolândia", lat: -19.35, lon: -56.2, cue: "necol", abaixo: true },
    { nome: "Rio Taquari", lat: -18.85, lon: -55.9, cue: "taquari", abaixo: true },
  ]} linhas={[{ pontos: RIO_PARAGUAI }, { pontos: RIO_TAQUARI }, { pontos: RIO_CUIABA }]}
    tint={colors.accent} />
);

// 3. o comitiveiro (p15)
export const A03Pantaleao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quem estava no comando", titulo: "Pantaleão Flores", linhas: [
    { rotulo: "Idade na viagem", valor: "67 anos", cue: "67", destaque: true },
    { rotulo: "Conduzindo boiadas", valor: "50 anos", cue: "50" },
    { rotulo: "Começou com", valor: "15 anos", cue: "15" },
  ], tint: "accent" }} />
);

// 4. os sete postos (p22)
export const A04Postos: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="estas" linhas={[
    "A COMITIVA DE PANTALEÃO · 7 HOMENS",
    "PONTEIRO · NA FRENTE, COM O BERRANTE",
    "CAPATAZ · O BRAÇO DIREITO DO CHEFE",
    "4 PEÕES · LATERAIS E CULATRA",
    "COZINHEIRO · SAI ANTES DE TODOS",
  ]} chave={1} carimbo={{ texto: "CADA UM NO SEU POSTO", cue: "cozinheiro" }} />
);

// 5. MAPA: a rota da comitiva (p32)
export const A05Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DE AQUIDAUANA AO PAIAGUÁS · MATO GROSSO DO SUL" lugares={[
    { nome: "Aquidauana", lat: -20.47, lon: -55.79, cue: "aquidauana", abaixo: true },
    { nome: "", lat: -19.4, lon: -56.4, cue: "janeiro" },
    { nome: "Paiaguás", lat: -18.3, lon: -56.75, cue: "10" },
  ]} marca={{ nome: "Corumbá", lat: -19.01, lon: -57.65, cue: "10" }}
    linhas={[{ pontos: RIO_PARAGUAI }, { pontos: RIO_TAQUARI }, { pontos: RIO_AQUIDAUANA }]}
    tint={colors.accent} />
);

// 6. Nelore x Brangus (p41)
export const A06Ritmo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Quanto uma boiada anda por dia", titulo: "Nelore x Brangus", linhas: [
    { rotulo: "Boiada de Nelore", valor: `18 a 20${NB}km/dia`, cue: "18" },
    { rotulo: "Brangus de Pantaleão", valor: `cerca de 9${NB}km/dia`, cue: "9", destaque: true },
  ], tint: "accent" }} />
);

// 7. o fundo que engole (p53)
export const A07Atoleiro: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="coricho" linhas={[
    "O RISCO DA TRAVESSIA",
    "CORIXO · CANAL QUE LIGA UMA ÁREA ALAGADA À OUTRA",
    "FUNDO · FIRME NUM PONTO, LAMA MOLE ADIANTE",
    "ATOLEIRO · O ANIMAL GASTA FORÇA PARA SAIR",
    "BOIADA · ESPERA OU SE ESPALHA",
  ]} chave={2} carimbo={{ texto: "ATOLEIRO", cue: "atola" }} />
);

// 8. a cozinha de comitiva (p61)
export const A08Cozinha: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="carreteiro" linhas={[
    "O CARDÁPIO DA COMITIVA",
    "ARROZ CARRETEIRO · ARROZ COM CARNE SECA",
    "MACARRÃO DE COMITIVA · FRITO NA BANHA",
    "PAÇOCA · CARNE SECA SOCADA COM FARINHA",
    "QUEBRA-TORTO · A 1ª REFEIÇÃO DO DIA",
  ]} chave={4} carimbo={{ texto: "SEM GELADEIRA", cue: "quebra" }} />
);

// 9. o que ficou no caminho (p77)
export const A09Perda: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="O QUE FICOU NO MEIO DO PANTANAL" valor={90000} cue="90" prefixo="R$ " sep="."
    nota={{ texto: "30 animais a 3 mil reais cada um", cue: "30" }} />
);

// 10. a conta real (p89)
export const A10Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Os números reais da travessia", titulo: "A conta da chegada", linhas: [
    { rotulo: "Distância percorrida", valor: `cerca de 400${NB}km`, cue: "400" },
    { rotulo: "Dias de viagem", valor: "46 dias", cue: "46" },
    { rotulo: "Ritmo médio", valor: `perto de 9${NB}km/dia`, cue: "9", destaque: true },
  ], tint: "accent" }} />
);

// 11. a outra comitiva (p99)
export const A11JotaEle: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pantanal · 2026", titulo: "Comitiva Jota Ele", linhas: [
    { rotulo: "Comitiveiro João Luiz", valor: "53 anos", cue: "53" },
    { rotulo: "Boiada", valor: "cerca de 1.200 cabeças", cue: "1", destaque: true },
    { rotulo: "Na estrada", valor: "uns 50 dias", cue: "50" },
    { rotulo: "Previsão", valor: "mais de 60 dias", cue: "60" },
  ], tint: "accent" }} />
);
