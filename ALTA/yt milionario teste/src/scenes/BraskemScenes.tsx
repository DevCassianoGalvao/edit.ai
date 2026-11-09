// Animações de "A maior petroquímica do Brasil deve R$ 56 bilhões" (pt, enxuto) — painel 20261017-003146 (baia b1).
// REGRA: biblioteca + MAPA; motion curto (cues <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. a dívida (p00)
export const K01Divida: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BRASKEM · CRÉDITOS NA RECUPERAÇÃO EXTRAJUDICIAL" valor={56} cue="56" prefixo="R$ "
    sufixo={`${NB}bilhões`} sep="." nota={{ texto: "prazo para salvar a empresa: 24 de novembro", cue: "24" }} />
);

// 2. a remoção em Maceió (p09)
export const K02Remocao: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MACEIÓ · IMÓVEIS DESOCUPADOS, SEGUNDO A PREFEITURA" valor={14000} cue="14" prefixo="mais de "
    sufixo={`${NB}imóveis`} sep="." nota={{ texto: "cerca de 55 mil pessoas afetadas", cue: "55" }} />
);

// 3. os prejuízos de 2025 (p19)
export const K03Prejuizo: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Braskem · prejuízo em 2025" titulo="E aí veio o golpe" tint={colors.danger} max={10.2}
    barras={[
      { rotulo: "2º trimestre", valor: "R$ 267 milhões", v: 0.267, cue: "267", cor: colors.textDim },
      { rotulo: "3º trimestre", valor: "R$ 26 milhões", v: 0.026, cue: "26", cor: colors.textDim },
      { rotulo: "4º trimestre", valor: "R$ 10,2 bilhões", v: 10.2, cue: "10", cor: colors.danger },
    ]} />
);

// 4. quem manda hoje (p26)
export const K04Controle: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ações com direito a voto", titulo: "Quem manda na Braskem", linhas: [
    { rotulo: "Fundo Shine I · IG4", valor: "50,11%", cue: "50", destaque: true },
    { rotulo: "Petrobras", valor: "47,3%", cue: "47" },
  ], tint: "accent" }} />
);

// 5. a linha de adesão (p38)
export const K05Adesao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Recuperação extrajudicial", titulo: "A primeira linha", linhas: [
    { rotulo: "A lei exige", valor: "um terço das dívidas", cue: "exige" },
    { rotulo: "A Braskem chegou com", valor: "39,6%", cue: "39", destaque: true },
    { rotulo: "Proteção", valor: `90${NB}dias`, cue: "90" },
  ], tint: "cool" }} />
);

// 6. MAPA dos polos (p47)
export const K06Polos: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="POLOS PETROQUÍMICOS · CIDADES INTEIRAS EM VOLTA" lugares={[
    { nome: "Camaçari · Bahia", lat: -12.70, lon: -38.32, cue: "camassari" },
    { nome: "Triunfo · Rio Grande do Sul", lat: -29.94, lon: -51.72, cue: "triunfo", abaixo: true },
    { nome: "São Paulo", lat: -23.55, lon: -46.63, cue: "paulo", abaixo: true },
    { nome: "Alagoas", lat: -9.67, lon: -35.74, cue: "alagoas" },
  ]} tint={colors.accent} />
);

// 7. o que os credores pedem (p57)
export const K07Credores: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Credores · 65% liderados por donos de títulos", titulo: "Dinheiro novo", linhas: [
    { rotulo: "Pedido à Petrobras e à IG4", valor: `US$ 3${NB}bilhões`, cue: "3" },
    { rotulo: "Elliott e Contrarian", valor: `até US$ 4${NB}bilhões`, cue: "4", destaque: true },
  ], tint: "danger" }} />
);

// 8. o prazo (p64)
export const K08Prazo: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="24" chave={2} linhas={[
    "PETROBRAS · WILLIAM FRANÇA",
    "",
    "“Temos até 24 de novembro",
    "para fechar o acordo",
    "de recuperação extrajudicial",
    "com os credores, porque",
    "o prazo é de 90 dias.”",
  ]} carimbo={{ texto: "90 DIAS", cue: "90" }} />
);
