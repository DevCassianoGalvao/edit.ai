// Animações de "A Mercury Fez Parceria com uma Chinesa" (pt, enxuto) — painel 20261027-134817 (baia b1).
// REGRA: biblioteca + MAPA; motion CURTO (cues ditos em <= ~14 s); todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: as fábricas da Jing-Jin (p06)
export const M01Fabricas: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="JING-JIN ELECTRIC · FÁBRICAS" lugares={[
    { nome: "Farmington Hills · Michigan", lat: 42.49, lon: -83.38, cue: "farmington" },
    { nome: "Shandong", lat: 36.67, lon: 117.0, cue: "shandong" },
    { nome: "Xangai", lat: 31.23, lon: 121.47, cue: "xangai", abaixo: true },
  ]} linhas={[
    { pontos: [[49, -123], [48, -95], [49, -89], [47, -84], [45, -83], [43, -82], [42, -79], [44, -76], [45, -71], [47, -67], [44, -67],
      [41, -70], [39, -74], [35, -75], [31, -81], [25, -80], [26, -82], [30, -85], [29, -90], [29, -94], [26, -97], [30, -105],
      [31, -111], [32, -117], [34, -120], [40, -124], [46, -124], [49, -123]] },
    { pontos: [[53, 122], [48, 135], [43, 131], [40, 124], [39, 122], [37, 122], [35, 119], [32, 121], [30, 122], [26, 120],
      [22, 114], [21, 110], [22, 106], [22, 101], [28, 97], [32, 79], [37, 75], [40, 74], [43, 80], [47, 90], [49, 87], [53, 122]] },
  ]} tint={colors.accent} />
);

// 2. Linha Avator: potência e preços (p13)
export const M02Avator: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Mercury · linha Avator · 2023", titulo: "Avator: potência e preço", linhas: [
    { rotulo: "Avator 35e · potência", valor: `3.700${NB}W`, cue: "3" },
    { rotulo: "Avator 20e · preço nos EUA", valor: `US$${NB}3.940`, cue: "3" },
    { rotulo: "Avator 35e · preço nos EUA", valor: `US$${NB}4.930`, cue: "4", destaque: true },
  ], tint: "cool" }} />
);

// 3. O dólar (p26)
export const M03Dolar: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MOTOR ELÉTRICO DE POPA · VITRINE AMERICANA" valor={4000} prefixo={`US$${NB}`} sep="."
    cue="4" nota={{ texto: "+ câmbio, frete, imposto e margem da revenda", cue: "frete" }} />
);

// 4. Vídeo viral (p36)
export const M04Videos: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="VÍDEOS VIRAIS EM INGLÊS · CANAL PEQUENO" valor={4500} sufixo={`${NB}visualizações`} sep="."
    cue="4" nota={{ texto: "em uma semana", cue: "semana" }} />
);

// 5. Sinal 1: motores maiores (p56)
export const M05Sinais: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sinal nº 1 · lançamentos da Mercury", titulo: "Motores elétricos maiores", linhas: [
    { rotulo: "Cavalos equivalentes", valor: `10${NB}cv`, cue: "10" },
    { rotulo: "Cavalos equivalentes", valor: `20${NB}cv`, cue: "20" },
    { rotulo: "Cavalos equivalentes", valor: `40${NB}cv ou mais`, cue: "40", destaque: true },
  ], tint: "accent" }} />
);
