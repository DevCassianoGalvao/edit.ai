// As animações de "A Regra Que Expulsou a Subaru do Brasil Aperta em 2027" (pt, arquivo dark) — painel
// 20261009-092623 (baia 1). REGRA: biblioteca + MAPA; motion CURTO; todo número é dito; milhar com ponto.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. mais de trinta anos de Brasil (p00)
export const P01Anos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="Subaru no Brasil · fim das vendas de zero quilômetro" valor={30} cue="30" sep="."
    sufixo={`${NB}anos`} prefixo="mais de " />
);

// 2. MAPA: para onde a matriz japonesa olhava (p07)
export const P02Matriz: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="Onde a matriz preferiu investir" lugares={[
    { nome: "Brasil · mercado pequeno", lat: -23.55, lon: -46.63, cue: "brasil" },
    { nome: "Japão · a fábrica", lat: 35.68, lon: 139.69, cue: "jap", abaixo: true },
    { nome: "Austrália", lat: -33.87, lon: 151.21, cue: "austr", abaixo: true },
    { nome: "Estados Unidos", lat: 39.0, lon: -98.0, cue: "estados" },
  ]} tint={colors.accent} />
);

// 3. o teto médio de emissões (p15)
export const P03Teto: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Proconve L8 · limite médio das fabricantes" titulo="O teto baixa a cada dois anos"
    tint={colors.accent} max={50} barras={[
    { rotulo: "2025", valor: "50", v: 50, cue: "50", cor: colors.textDim },
    { rotulo: "2027", valor: "40", v: 40, cue: "40" },
    { rotulo: "2029", valor: "30", v: 30, cue: "30" },
  ]} />
);

// 4. o corte de potência da Hyundai (p25)
export const P04Hyundai: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Hyundai · motor 1.0 turbo", titulo: "Cinco cavalos a menos", linhas: [
    { rotulo: "Potência antes", valor: `120${NB}cv`, cue: "120" },
    { rotulo: "Potência depois", valor: `115${NB}cv`, cue: "115", destaque: true },
    { rotulo: "Torque (igual)", valor: `17,5${NB}kgfm`, cue: "17" },
  ], tint: "accent" }} />
);

// 5. o carro que você já tem (p45)
export const P05Frota: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="quinta" chave={3} linhas={[
    "PROCONVE L8 · PRIMEIRA ETAPA",
    "",
    "Vale para o carro fabricado e vendido novo",
    "Carros fabricados até 31 de dezembro de 2024",
    "ficam fora da norma",
    "",
    "O seu carro continua legal,",
    "continua circulando e pode ser vendido usado.",
  ]} carimbo={{ texto: "NÃO AFETADO", cue: "31", cor: "#2f7d4f" }} />
);

// 6. o resumo da norma em janeiro de 2027 (p53)
export const P06Janeiro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Proconve L8 · janeiro de 2027", titulo: "A regra aperta de verdade", linhas: [
    { rotulo: "Teto médio hoje", valor: "50", cue: "50" },
    { rotulo: "Teto médio na segunda etapa", valor: "40", cue: "40", destaque: true },
    { rotulo: "Margem do teste de rua", valor: `2× → 1,5×`, cue: "meia" },
  ], tint: "accent" }} />
);

// 7. trinta e quatro anos (p65)
export const P07Anos34: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="Subaru no Brasil · a história que acabou" valor={34} cue="34" sep="."
    sufixo={`${NB}anos`} />
);
