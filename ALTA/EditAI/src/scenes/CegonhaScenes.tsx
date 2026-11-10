// As animações de "Navio-cegonha: 8 mil carros sem arranhar nenhum" (pt, arquivo dark) — painel 20261005-231331 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. oito mil carros, doze andares (p00)
export const C01OitoMil: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="UM ÚNICO NAVIO" valor={8000} cue="8" sep="." sufixo=" carros"
    nota={{ texto: "12 andares de aço empilhados no escuro", cue: "12" }} />
);

// 2. as medidas (p04)
export const C02Medidas: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Os maiores navios-cegonha", titulo: "Um estacionamento que flutua", linhas: [
    { rotulo: "Comprimento", valor: `mais de 200${NB}m`, cue: "200" },
    { rotulo: "Largura", valor: `cerca de 38${NB}m`, cue: "38" },
    { rotulo: "Conveses", valor: `até 14`, cue: "14", destaque: true },
  ], tint: "accent" }} />
);

// 3. a ordem dos portos (p21)
export const C03Portos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "1ª regra · a ordem dos portos", titulo: "Quem sai primeiro, fica na frente", linhas: [
    { rotulo: "Descem na Alemanha", valor: `500 carros`, cue: "500" },
    { rotulo: "Presos atrás de", valor: `2${NB}mil · Inglaterra`, cue: "2", destaque: true },
  ], tint: "accent" }} />
);

// 4. o espaçamento (p26)
export const C04Espaco: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "4ª regra · o espaçamento", titulo: "Assustadoramente pequeno", linhas: [
    { rotulo: "Entre as laterais", valor: `~10${NB}cm`, cue: "10", destaque: true },
    { rotulo: "Traseira e dianteira", valor: `~30${NB}cm`, cue: "30" },
  ], tint: "accent" }} />
);

// 5. a sequência depois de estacionar (p40)
export const C05Sequencia: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="cambio" chave={6} linhas={[
    "PROCEDIMENTO · CARRO ESTACIONADO",
    "1. Câmbio engatado (ou P)",
    "2. Freio de mão puxado com firmeza",
    "3. Rodas retas",
    "4. Vidros fechados",
    "5. Motor desligado",
    "6. Chave no lugar padronizado",
  ]} carimbo={{ texto: "CONFERIDO", cue: "chave" }} />
);

// 6. o balanço (p48)
export const C06Inclina: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mar agitado", titulo: "Um carro solto vira projétil", linhas: [
    { rotulo: "Convés inclina", valor: `20 a 30 graus`, cue: "20" },
    { rotulo: "Carro de", valor: `1,5 tonelada`, cue: "30" },
    { rotulo: "Do vizinho", valor: `a 10${NB}cm`, cue: "10", destaque: true },
  ], tint: "accent" }} />
);

// 7. MAPA: Cougar Ace (p63)
export const C07Cougar: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="COUGAR ACE · JULHO DE 2006" lugares={[
    { nome: "Japão · carros da Mazda", lat: 34.39, lon: 132.46, cue: "japao" },
    { nome: "Sul das Ilhas Aleutas · 60° de inclinação", lat: 48.2, lon: -176.5, cue: "inclinar", abaixo: true },
  ]} tint={colors.accent} />
);

// 8. MAPA: Felicity Ace (p75)
export const C08Felicity: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="FELICITY ACE · FEVEREIRO DE 2022" lugares={[
    { nome: "Oceano Atlântico · fogo a bordo", lat: 36.6, lon: -33.5, cue: "atlantico", abaixo: true },
    { nome: "Arquipélago dos Açores", lat: 38.6, lon: -28.0, cue: "acores" },
  ]} tint={colors.accent} />
);

// 9. os danos (p85)
export const C09Danos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="DANOS EM OPERAÇÕES BEM CONDUZIDAS" valor={1} cue="1" prefixo="< " sufixo=" %" sep="."
    nota={{ texto: `Num navio com 8${NB}mil carros, a imensa maioria desembarca como saiu da fábrica`, cue: "8" }} />
);
