// As 7 animações de "O motor a gasolina chinês que ameaça o carro elétrico" (pt, 23,5 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Colunas, Barras (3), Painel (2), Documento.
// Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES.
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas } from "./blocos";
import { Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. para onde vai a energia ----------------
export const A01Energia: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="De cada 100 reais de gasolina, cerca de 70 viram calor"
    tint={colors.danger}
    cols={[
      { titulo: "Escapamento", texto: "O calor sai pelo cano.", cue: "escapamento" },
      { titulo: "Radiador", texto: "Esquenta o sistema de arrefecimento.", cue: "radiador" },
      { titulo: "Atrito", texto: "Entre as peças do motor.", cue: "atrito" },
      { titulo: "Movimento", texto: "Só 25 a 35 % viram movimento.", cue: "vinte", cor: colors.accent },
    ]}
  />
);

// ---------------- 2. a corrida da eficiência ----------------
export const A02Corrida: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Eficiência térmica de motores a gasolina de série"
    titulo="A China entrou acelerando"
    tint={colors.accent}
    max={48.41}
    barras={[
      { rotulo: "Toyota e Honda", valor: "41 a 42 %", v: 42, cue: "maio", cor: colors.textDim },
      { rotulo: "BYD, 5ª geração — maio de 2024", valor: "46,06 %", v: 46.06, cue: "46", cor: colors.cool },
      { rotulo: "Geely", valor: "46,5 %", v: 46.5, cue: "geely", cor: colors.accent },
    ]}
    nota={{ texto: "Nessa faixa, ganhar um único ponto exige anos de pesquisa.", cue: "engenheiros" }}
  />
);

// ---------------- 3. a taxa de compressão ----------------
export const A03Compressao: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Taxa de compressão"
    titulo="Espremer mais a mistura, sem detonar o motor"
    tint={colors.accent}
    max={15.5}
    barras={[
      { rotulo: "Motor comum a gasolina", valor: "10 a 12 : 1", v: 12, cue: "comum", cor: colors.textDim },
      { rotulo: "Motor da Geely", valor: "15,5 : 1", v: 15.5, cue: "geely", cor: colors.danger },
    ]}
    nota={{ texto: "Compressão alta demais provoca a detonação — uma queima descontrolada.", cue: "detonacao" }}
  />
);

// ---------------- 4. o híbrido ----------------
export const A04Hibrido = painel({
  kicker: "O novo híbrido da Geely — dois motores elétricos",
  titulo: "O motor de tração",
  linhas: [
    { rotulo: "Potência", valor: "230 kW", cue: "230", destaque: true },
    { rotulo: "Em cavalos", valor: "cerca de 308 cv", cue: "308" },
    { rotulo: "Contra os híbridos japoneses típicos", valor: "1,72 vez mais", cue: "japoneses" },
    { rotulo: "Unidade integrada", valor: "11 componentes em 1", cue: "onze|11" },
  ],
  tint: "cool",
});

// ---------------- 5. o recorde Guinness ----------------
export const A05Guinness: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="levou"
    chave={5}
    linhas={[
      "GUINNESS WORLD RECORDS",
      "Geely Emgrand — prova de consumo em rodovia",
      "",
      "Sedã de tamanho normal, sem tomada, sem cabo.",
      "Resultado:",
      "2,22 litros a cada 100 km — cerca de 45 km/l",
    ]}
    carimbo={{ texto: "RECORDE", cue: "quilometros" }}
  />
);

// ---------------- 6. a bateria ----------------
export const A06Bateria: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Tamanho da bateria, em quilowatts-hora"
    titulo="Cinquenta, sessenta vezes menos bateria"
    tint={colors.cool}
    max={80}
    barras={[
      { rotulo: "Carro elétrico de médio porte", valor: "50 a 80 kWh", v: 80, cue: "cinquenta|50", cor: colors.accent },
      { rotulo: "Novo híbrido da Geely", valor: "cerca de 1 kWh", v: 1, cue: "geely", cor: colors.danger },
    ]}
    nota={{ texto: "Menos matéria-prima, menos peso, menos custo, menos mineração.", cue: "mineracao" }}
  />
);

// ---------------- 7. o domínio das baterias ----------------
export const A07Baterias = painel({
  kicker: "China — o domínio das baterias",
  titulo: "A maior indústria de elétricos do mundo",
  linhas: [
    { rotulo: "Mercado global de baterias", valor: "cerca de 70 %", cue: "setenta|70" },
    { rotulo: "Das 10 maiores fabricantes", valor: "7 são chinesas — 72,6 %", cue: "sete|7" },
    { rotulo: "CATL, sozinha", valor: "40,2 %", cue: "sozinha", destaque: true },
    { rotulo: "Células de bateria do mundo", valor: "mais de 80 %", cue: "celulas" },
  ],
  tint: "danger",
});
