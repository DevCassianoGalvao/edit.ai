// As 12 animações de "Aquarius — dez dias no último laboratório submarino habitado" (pt, 45 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — MapaRota, MapaCampanha,
// Painel (3), Odometro (2), Colunas (2), Lista (2), Barras, Documento. Todo número é DITO na narração; cues em
// scripts/build_plan.py -> CUES (grafia do Whisper: "nove" por extenso; "Saint Croix" saiu "San Juan" -> cue "1988").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. Key Largo -> Conch Reef (MAPA) ----------------
export const Q01Rota: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="DO CAIS DE KEY LARGO ATÉ O RECIFE DA CONCHA · CERCA DE NOVE QUILÔMETROS"
    tint={colors.cool}
    lugares={[
      { nome: "Key Largo", lat: 25.09, lon: -80.44, cue: "largo" },
      { nome: "Conch Reef", lat: 24.95, lon: -80.46, cue: "conch", abaixo: true },
    ]}
  />
);

// ---------------- 2. a casa de aço ----------------
export const Q02Casa = painel({
  kicker: "Aquarius · Conch Reef",
  titulo: "Uma casa de aço no fundo do mar",
  linhas: [
    { rotulo: "Comprimento", valor: "cerca de 13 metros", cue: "13" },
    { rotulo: "Diâmetro", valor: "menos de três metros", cue: "diametro" },
    { rotulo: "O cilindro", valor: "perto de 80 toneladas", cue: "80" },
    { rotulo: "A base de aço", valor: "mais de 100 toneladas", cue: "100", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 3. saturação ----------------
export const Q03Saturacao: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="PARA VOLTAR À SUPERFÍCIE COM SEGURANÇA"
    valor={17}
    cue="17"
    sufixo=" horas de descompressão"
    nota={{ texto: "Depois de um dia inteiro, o corpo satura de nitrogênio", cue: "saturacao" }}
  />
);

// ---------------- 4. a planta da casa ----------------
export const Q04Planta: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="O habitat · três áreas"
    tint={colors.cool}
    cols={[
      { titulo: "Varanda molhada", texto: "Por onde se entra e se sai.", cue: "varanda" },
      { titulo: "Câmara intermediária", texto: "Chuveiro, vaso, equipamentos.", cue: "intermediaria" },
      { titulo: "Câmara principal", texto: "Cozinha, mesa, computadores.", cue: "principal" },
      { titulo: "O quarto", texto: "Seis beliches. Nenhuma porta.", cue: "beliches", cor: colors.accent },
    ]}
  />
);

// ---------------- 5. a mesa de vigia ----------------
export const Q05Vigia = painel({
  kicker: "Key Largo · mesa de vigia",
  titulo: "Nunca estão sozinhos",
  linhas: [
    { rotulo: "Vigilância", valor: "24 horas por dia", cue: "24" },
    { rotulo: "Câmeras", valor: "dentro do habitat", cue: "cameras" },
    { rotulo: "Sensores", valor: "oxigênio, gás carbônico, umidade", cue: "oxigenio" },
    { rotulo: "Alarmes", valor: "fumaça, ar pesado, desmaio", cue: "fumaca", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 6. tempo de trabalho ----------------
export const Q06Tempo: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Tempo útil no fundo · por dia"
    titulo="Por que morar lá embaixo"
    tint={colors.accent}
    max={10}
    barras={[
      { rotulo: "Mergulhador comum", valor: "duas ou três horas", v: 2.5, cue: "conta", cor: colors.textDim },
      { rotulo: "Aquanauta saturado", valor: "até nove horas", v: 9, cue: "nove", cor: colors.accent },
    ]}
    nota={{ texto: "Dez dias = meses de mergulhos comuns.", cue: "meses" }}
  />
);

// ---------------- 7. os postos de gasolina ----------------
export const Q07Postos: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Espalhados pelo recife"
    titulo="Os postos de gasolina"
    tint={colors.cool}
    itens={[
      { titulo: "Sino ou cúpula preso ao fundo", cue: "sino" },
      { titulo: "Uma bolha de ar e reservas de gás", cue: "bolha" },
      { titulo: "Regulador falhou, mangueira soltou", cue: "regulador", cor: colors.danger },
      { titulo: "Enfiar a cabeça, respirar, esperar ajuda", cue: "esperar" },
    ]}
  />
);

// ---------------- 8. a cadeia do ar ----------------
export const Q08Ar: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Cada respiração depende de uma cadeia de máquinas"
    tint={colors.cool}
    cols={[
      { titulo: "A boia", texto: "Capta e comprime o ar.", cue: "captado" },
      { titulo: "A mangueira", texto: "Leva o ar até o habitat.", cue: "mangueira" },
      { titulo: "Os filtros", texto: "Resfriam e secam o ar.", cue: "filtros" },
      { titulo: "Gás carbônico", texto: "Removido o tempo todo.", cue: "removido", cor: colors.danger },
    ]}
  />
);

// ---------------- 9. NEEMO ----------------
export const Q09Neemo: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="2001"
    chave={4}
    linhas={[
      "NASA — NEEMO",
      "Extreme Environment Mission Operations",
      "",
      "Desde 2001 · Aquarius, Florida Keys",
      "Simulação de operações espaciais",
      "Astronautas, engenheiros e cientistas",
      "De uma a três semanas no habitat",
    ]}
    carimbo={{ texto: "AMBIENTE EXTREMO", cue: "fatal", cor: colors.danger }}
  />
);

// ---------------- 10. de Saint Croix às Florida Keys (MAPA) ----------------
export const Q10Viagem: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="A VIAGEM DA AQUARIUS"
    pontos={[
      { nome: "Saint Croix", lat: 17.75, lon: -64.73, data: "1988 · FURACÃO HUGO EM 1989", cue: "1988" },
      { nome: "Conch Reef", lat: 24.95, lon: -80.46, data: "1993 · ATÉ HOJE", cue: "1993" },
    ]}
    setas={[{ de: 0, para: 1, cue: "1993" }]}
  />
);

// ---------------- 11. Missão 31 ----------------
export const Q11Missao31: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="FABIEN COUSTEAU · MISSÃO 31 · 2014"
    valor={31}
    cue="31"
    sufixo=" dias no fundo do mar"
    nota={{ texto: "Um a mais do que o avô, Jacques Cousteau, 50 anos antes", cue: "avo" }}
  />
);

// ---------------- 12. a volta ----------------
export const Q12Volta = painel({
  kicker: "Dia dez · a volta",
  titulo: "A casa vira câmara de descompressão",
  linhas: [
    { rotulo: "Duração", valor: "cerca de 17 horas", cue: "17" },
    { rotulo: "Nitrogênio", valor: "sai dos tecidos sem bolhas", cue: "nitrogenio" },
    { rotulo: "Oxigênio puro", valor: "respirado por máscaras", cue: "oxigenio" },
    { rotulo: "Onde estão", valor: "ainda a 20 metros de profundidade", cue: "20", destaque: true },
  ],
  tint: "cool",
});
