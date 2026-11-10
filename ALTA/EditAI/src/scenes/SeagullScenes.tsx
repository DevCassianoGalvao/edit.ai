// As animações de "Engenheiros Americanos Desmontaram o BYD Mais Barato da China" (pt, arquivo dark) — painel
// 20261009-191652 (baia 1). REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { Documento, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: Caresoft em Livonia, colada em Detroit (p01)
export const C01Livonia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CARESOFT GLOBAL · AUTÓPSIA INDUSTRIAL" lugares={[
    { nome: "Livonia · Caresoft Global", lat: 42.37, lon: -83.35, cue: "livon" },
    { nome: "Detroit · capital do carro americano", lat: 42.33, lon: -83.05, cue: "detroit", abaixo: true },
  ]} tint={colors.accent} />
);

// 2. a balança (p14)
export const C02Balanca: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A balança da Caresoft", titulo: "Seagull contra Chevrolet Bolt", linhas: [
    { rotulo: "BYD Seagull", valor: `2.734${NB}libras`, cue: "2" },
    { rotulo: "Em quilos", valor: `cerca de 1.240${NB}kg`, cue: "1" },
    { rotulo: "Mais leve que o Bolt", valor: `900${NB}libras`, cue: "900" },
    { rotulo: "Diferença", valor: `cerca de 400${NB}kg`, cue: "400", destaque: true },
  ], tint: "accent" }} />
);

// 3. a tarifa americana (p21)
export const C03Tarifa: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="EUA · tarifa sobre elétricos chineses" titulo="O muro antes do carro"
    tint={colors.danger} max={100} barras={[
    { rotulo: "Na época", valor: `27,5${NB}%`, v: 27.5, cue: "27", cor: colors.textDim },
    { rotulo: "Anunciada", valor: `100${NB}%`, v: 100, cue: "100" },
  ]} />
);

// 4. o corte de preço na China (p28)
export const C04Yuan: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "China · abril de 2025 · linha Ocean", titulo: "O Seagull ficou ainda mais barato", linhas: [
    { rotulo: "Antes", valor: `69.800${NB}yuans`, cue: "69" },
    { rotulo: "Depois", valor: `56.800${NB}yuans`, cue: "56", destaque: true },
    { rotulo: "Em dólares", valor: `cerca de US$${NB}7.800`, cue: "7" },
  ], tint: "accent" }} />
);

// 5. o imposto de importação (p34)
export const C05Imposto: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="importa" chave={4} linhas={[
    "IMPOSTO DE IMPORTAÇÃO · CARROS ELÉTRICOS",
    "",
    "Elétrico importado pronto:",
    "subiu em degraus, ano após ano",
    `35${NB}% em julho de 2026`,
    "",
    "Kits montados em Camaçari:",
    "alíquota cheia a partir de janeiro de 2027",
  ]} carimbo={{ texto: `35${NB}%`, cue: "35" }} />
);

// 6. a venda direta (p39)
export const C06VendaDireta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Venda direta · empresas e produtores rurais", titulo: "O espaço escondido no preço", linhas: [
    { rotulo: "Desconto", valor: `10${NB}%`, cue: "10" },
    { rotulo: "Dolphin Mini sai por", valor: `R$${NB}107.091`, cue: "107", destaque: true },
  ], tint: "accent" }} />
);

// 7. a pergunta (p54)
export const C07Pergunta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O mesmo carro", titulo: "Você pagaria?", linhas: [
    { rotulo: "No Brasil", valor: `R$${NB}119.990`, cue: "119" },
    { rotulo: "O equivalente na China", valor: `R$${NB}43.000`, cue: "43", destaque: true },
  ], tint: "danger" }} />
);
