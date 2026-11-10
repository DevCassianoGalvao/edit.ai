// As animações de "A virada da Subaru" (pt, arquivo dark) — painel 20261004-231747 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o plano original (p02)
export const S01Plano: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O plano original da Subaru", titulo: "Eletrificação até o fim da década", linhas: [
    { rotulo: "Investimento", valor: `1,5${NB}trilhão de ienes`, cue: "1", destaque: true },
    { rotulo: "Em dólares", valor: `cerca de US$${NB}9,7${NB}bilhões`, cue: "9" },
  ], tint: "accent" }} />
);

// 2. Uncharted Sport/GT (p08)
export const S02Uncharted: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Uncharted · Sport e GT", titulo: "Números de esportivo", linhas: [
    { rotulo: "Potência", valor: `até 338${NB}cv`, cue: "338", destaque: true },
    { rotulo: "0 a 100${NB}km/h", valor: `cerca de 5${NB}s`, cue: "5" },
  ], tint: "accent" }} />
);

// 3. Getaway (p15)
export const S03Getaway: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Getaway · sete lugares", titulo: "Preço esperado", linhas: [
    { rotulo: "Faixa", valor: `US$${NB}40 a 50${NB}mil`, cue: "40" },
    { rotulo: "Potência", valor: `400${NB}cv`, cue: "400", destaque: true },
  ], tint: "accent" }} />
);

// 4. Forester híbrido (p24)
export const S04Forester: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Forester Strong Hybrid", titulo: "Boxer + dois motores elétricos", linhas: [
    { rotulo: "Potência combinada", valor: `194${NB}cv`, cue: "194" },
    { rotulo: "Consumo médio", valor: `quase 15${NB}km/l`, cue: "15" },
    { rotulo: "Autonomia", valor: `mais de 930${NB}km`, cue: "930", destaque: true },
  ], tint: "accent" }} />
);

// 5. Fuji Heavy Industries (p30)
export const S05Fuji: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Fuji Heavy Industries", titulo: "De onde vem o nome Subaru", linhas: [
    { rotulo: "Fundação", valor: "1953", cue: "1953", destaque: true },
    { rotulo: "Cinco empresas", valor: "+ uma sexta", cue: "cinco" },
  ], tint: "accent" }} />
);

// 6. MAPA: produzido no Japão, vendido nos EUA (p39)
export const S06Exporta: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="O TERCEIRO RISCO · TARIFAS E CÂMBIO" lugares={[
    { nome: "Estados Unidos · maior mercado", lat: 40.4, lon: -86.9, cue: "estados" },
    { nome: "Japão · produção exportada", lat: 36.3, lon: 139.4, cue: "japao", abaixo: true },
  ]} tint={colors.accent} />
);

// 7. o que muda para o consumidor (p49)
export const S07Cliente: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Para o consumidor", titulo: "Mais opções", linhas: [
    { rotulo: "Elétrico de 375${NB}cv", valor: `menos de US$${NB}40${NB}mil`, cue: "375", destaque: true },
    { rotulo: "Forester híbrido", valor: `mais de 900${NB}km por tanque`, cue: "900" },
  ], tint: "accent" }} />
);
