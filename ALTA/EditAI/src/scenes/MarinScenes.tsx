// Animações de "Como Vivem os Marinheiros do Navio que Conserta a Internet no Fundo do Mar" (pt) — painel 20261102-015158 (baia b1, enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. as falhas por ano (p03)
export const C01Falhas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "CABOS SUBMARINOS · COMITÊ INTERNACIONAL DE PROTEÇÃO", titulo: "Quantas vezes eles quebram", linhas: [
    { rotulo: "Falhas por ano · mínimo", valor: `150`, cue: "150" },
    { rotulo: "Falhas por ano · máximo", valor: `200`, cue: "200", destaque: true },
    { rotulo: "Origem humana · mínimo", valor: `70${NB}%`, cue: "70" },
    { rotulo: "Origem humana · máximo", valor: `80${NB}%`, cue: "80" },
  ], tint: "danger", colunas: false }} />
);

// 2. MAPA: a costa que ele cobre (p10)
export const C02Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DE MADAGASCAR ATÉ GANA · O ÚNICO NAVIO FIXO NA ÁFRICA" lugares={[
    { nome: "Madagascar", lat: -18.77, lon: 46.87, cue: "Madagascar", esquerda: true },
    { nome: "Gana", lat: 5.6, lon: -0.19, cue: "Gana" },
  ]} tint={colors.accent} />
);

// 3. o custo por dia (p18)
export const C03Custo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MANTER UM NAVIO DE REPARO NO MAR · ORANGE MARINE · POR DIA" valor={120} cue="120" prefixo={`US$${NB}`}
    sufixo={`${NB}mil`}
    barras={[{ rotulo: "Navio mais barato", v: 70, cue: "70" }, { rotulo: "Navio mais caro", v: 120, cue: "120", destaque: true }]} />
);

// 4. o cânion do Congo (p43)
export const C04Congo: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="CÂNION DO CONGO · FUNDO DO ATLÂNTICO · SE ESTENDE POR" valor={280} cue="280" sufixo={`${NB}km`} />
);

// 5. quanto dura uma emenda (p51)
export const C05Emenda: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A EMENDA · NAVIO PARADO, CABO SUSPENSO NA ÁGUA", titulo: "Quanto tempo leva", linhas: [
    { rotulo: "Emenda típica · mínimo", valor: `12${NB}horas`, cue: "12" },
    { rotulo: "Emenda típica · máximo", valor: `24${NB}horas`, cue: "24" },
    { rotulo: "Reparo em Gana · passou de", valor: `48${NB}horas`, cue: "48", destaque: true },
  ], tint: "accent", colunas: false }} />
);

// 6. a conta do reparo (p57)
export const C06Reparo: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A CONTA DO NAVIO NO MAR · DÓLARES", titulo: "Quanto custa o relógio", linhas: [
    { rotulo: "Diária · a partir de", valor: `US$${NB}70${NB}mil`, cue: "70" },
    { rotulo: "Um mês de reparo", valor: `US$${NB}2,1 a 3,6${NB}milhões`, cue: "2" },
    { rotulo: "Viagem de uns 120 dias · 2023", valor: `US$${NB}8 a 14${NB}milhões`, cue: "8", destaque: true },
  ], tint: "danger", colunas: false }} />
);

// 7. o turno (p63)
export const C07Turno: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TURNO A BORDO · SEMANAS SEGUIDAS ATÉ O CABO FICAR PRONTO" valor={12} cue="12" sufixo={`${NB}horas`} />
);

// 8. a frota (p79)
export const C08Frota: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="NAVIOS DE REPARO DE CABOS NO MUNDO · REST OF WORLD" valor={62} cue="62" sufixo={`${NB}navios`}
    nota={{ texto: "para cuidar de mais de 99 % do tráfego internacional de dados", cue: "99" }} />
);

// 9. o crescimento dos cabos (p84)
export const C09Cabos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="COMPRIMENTO TOTAL DOS CABOS EM DEZ ANOS · UNIÃO INTERNACIONAL DE TELECOMUNICAÇÕES" valor={70} cue="70" prefixo="+"
    sufixo={`${NB}%`} nota={{ texto: "e as falhas seguem em 150 a 200 por ano", cue: "150" }} />
);

// 10. o balanço (p92)
export const C10Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "COMO VIVEM · O RESUMO", titulo: "A vida no Léon Thévenin", linhas: [
    { rotulo: "Turnos", valor: `12${NB}horas`, cue: "12" },
    { rotulo: "Comprimento do navio", valor: `107${NB}metros`, cue: "107" },
    { rotulo: "Refeições quentes por dia", valor: `3`, cue: "três", destaque: true },
  ], tint: "accent", colunas: false }} />
);
