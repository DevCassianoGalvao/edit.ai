// Animações de "A BYD Soltou uma BOMBA: Bateria Que Carrega em 5 Minutos Pode Acabar com o Posto" (pt, arquivo dark) —
// painel 20261011-002613 (baia 1). REGRA: biblioteca + MAPA; motion curto; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. os números do telão (p02)
export const F01Telao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Flash Charging · Blade de 2ª geração", titulo: "Os números do telão", linhas: [
    { rotulo: `De 10 a 70${NB}%`, valor: `5${NB}minutos`, cue: "5" },
    { rotulo: `De 10 a 97${NB}%`, valor: `9${NB}minutos`, cue: "9" },
    { rotulo: `De 20 a 97${NB}% a −20${NB}°C`, valor: `12${NB}minutos`, cue: "12", destaque: true },
  ], tint: "accent" }} />
);

// 2. as estações na China (p17)
export const F02Estacoes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ESTAÇÕES DE RECARGA RELÂMPAGO · CHINA · 24 DE SETEMBRO" valor={11586} cue="11" sep="."
    sufixo={`${NB}estações`}
    nota={{ texto: `em 341 cidades`, cue: "341" }} />
);

// 3. as vendas do semestre (p25)
export const F03Vendas: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="BYD · 1º SEMESTRE DE 2026 · CERCA DE" valor={1800000} cue="800" sep="."
    sufixo={`${NB}carros`}
    nota={{ texto: `queda de quase 16${NB}% · faltou bateria Blade`, cue: "16" }} />
);

// 4. MAPA: Brasília x São Paulo (p34)
export const F04Brasilia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="ELETRIFICADOS EMPLACADOS · AGOSTO" lugares={[
    { nome: "Brasília · 5.048", lat: -15.79, lon: -47.88, cue: "brasília" },
    { nome: "São Paulo", lat: -23.55, lon: -46.63, cue: "paulo", abaixo: true },
  ]} tint={colors.accent} />
);

// 5. os postos (p46)
export const F05Postos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="POSTOS DE COMBUSTÍVEIS NO BRASIL · ANP · FIM DE 2024" valor={44678} cue="44" sep="."
    sufixo={`${NB}postos`}
    nota={{ texto: `133,1 bilhões de litros vendidos no ano`, cue: "133" }} />
);

// 6. a resposta (p61)
export const F06Resposta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A resposta", titulo: "Pode acabar com o posto?", linhas: [
    { rotulo: `5${NB}minutos`, valor: `só de 10 a 70${NB}%`, cue: "5" },
    { rotulo: `1.000 carregadores`, valor: "plano para o fim de 2027", cue: "mil" },
    { rotulo: "BYD compatível vendido hoje no Brasil", valor: "nenhum", cue: "nenhum", destaque: true },
  ], tint: "accent" }} />
);
