// As animações de "A Toyota desmontou 4 carros da BYD" (pt, arquivo dark) — painel 20261006-113311 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Documento, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. os quatro carros (p01)
export const T01QuatroCarros: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Os quatro carros desmontados", titulo: "Um corte da BYD inteira", linhas: [
    { rotulo: "Han", valor: "sedã elétrico de luxo", cue: "han" },
    { rotulo: "Tang DM", valor: `híbrido de 7${NB}lugares`, cue: "tang" },
    { rotulo: "Dolphin", valor: "hatch elétrico compacto", cue: "dolphin" },
    { rotulo: "Yuan Plus", valor: `o Atto${NB}3`, cue: "yuan", destaque: true },
  ], tint: "accent" }} />
);

// 2. a Toyota em 2024 (p04)
export const T02Toyota2024: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Toyota · primeiros 8 meses de 2024", titulo: "A maior montadora do mundo", linhas: [
    { rotulo: "Veículos vendidos", valor: `quase 6${NB}milhões e 600${NB}mil`, cue: "6" },
    { rotulo: `100${NB}% elétricos`, valor: `menos de 1,5${NB}%`, cue: "1", destaque: true },
  ], tint: "accent" }} />
);

// 3. MAPA: o ginásio de Gifu (p10)
export const T03Gifu: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="OUTUBRO DE 2024 · UM ATTO 3 ESPALHADO NO CHÃO" lugares={[
    { nome: "Gifu · o ginásio", lat: 35.42, lon: 136.76, cue: "gifu" },
    { nome: "Nagoya · coração da Toyota", lat: 35.18, lon: 136.91, cue: "nagoya", abaixo: true },
  ]} tint={colors.accent} />
);

// 4. o manual da Nikkei (p14)
export const T04Nikkei: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="nikkei" chave={4} linhas={[
    "NIKKEI · RELATÓRIO DE DESMONTAGEM",
    "",
    "Veículo: BYD Seal, sedã esportivo elétrico",
    "Desmontagem completa, peça por peça",
    "Manual de cerca de 350 páginas",
    "",
    "Prefácio: a BYD já superou a Tesla",
    "e tem visão para ditar o padrão global.",
  ]} carimbo={{ texto: "350 PÁGINAS", cue: "350" }} />
);

// 5. a bateria colada (p18)
export const T05Cola: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Equipe chinesa de desmontagem de baterias", titulo: "A nova bateria lâmina", linhas: [
    { rotulo: "Pacotes já abertos", valor: `mais de 20`, cue: "20" },
    { rotulo: "Para separar este", valor: `cerca de 8${NB}horas`, cue: "8", destaque: true },
    { rotulo: "Antes", valor: "congelado por dezenas de horas", cue: "congel" },
  ], tint: "danger" }} />
);

// 6. MAPA: a joint venture (p22)
export const T06JointVenture: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="2020 · TOYOTA + BYD · EMPRESA CONJUNTA" lugares={[
    { nome: "Toyota City · Japão", lat: 35.08, lon: 137.16, cue: "trabalhar" },
    { nome: "Shenzhen · a joint venture", lat: 22.54, lon: 114.06, cue: "shenzhen", abaixo: true },
  ]} tint={colors.accent} />
);

// 7. o leque de baterias (p26)
export const T07Baterias: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O novo plano de baterias da Toyota", titulo: "A mesma língua química", linhas: [
    { rotulo: "Lítio, ferro e fosfato", valor: "carros populares", cue: "populares" },
    { rotulo: "Alto desempenho", valor: "modelos mais caros", cue: "desempenho" },
    { rotulo: "Estado sólido", valor: "aposta de longo prazo", cue: "longo", destaque: true },
  ], tint: "accent" }} />
);

// 8. a Toyota já se reinventou (p30)
export const T08Reinvencao: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A Toyota já se reinventou antes", titulo: "Três viradas", linhas: [
    { rotulo: "Dos teares", valor: "aos automóveis", cue: "teares" },
    { rotulo: "Superou", valor: "os americanos", cue: "americanos" },
    { rotulo: "Criou", valor: "o híbrido", cue: "criou", destaque: true },
  ], tint: "accent" }} />
);
