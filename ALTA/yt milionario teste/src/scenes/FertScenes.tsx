// As 8 animações de "A maior produtora de fertilizantes do Brasil sem caixa" (pt, 22,5 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — MapaCampanha, MapaRota,
// Painel (3), Barras (3). Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "US $ 69", "1 .200", "3 ,1" -> cues em palavra ou no número inteiro; "171,2 bi" saiu truncado — fora da tela).
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras } from "./blocos";
import { MapaRota } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. o tamanho da Mosaic ----------------
export const F01Mosaic = painel({
  kicker: "Mosaic Fertilizantes",
  titulo: "A principal fonte nacional de fósforo",
  linhas: [
    { rotulo: "Controladora", valor: "The Mosaic Company · bolsa de Nova York", cue: "americana" },
    { rotulo: "Rocha fosfática do país", valor: "mais de 70 %", cue: "70" },
    { rotulo: "Fosfatados em 2025", valor: "cerca de 3,1 milhões de toneladas", cue: "2025", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 2. a margem ----------------
export const F02Margem: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Mosaic no Brasil · caixa operacional −35 %"
    titulo="Margem bruta por tonelada"
    tint={colors.danger}
    max={80}
    barras={[
      { rotulo: "Um ano antes", valor: "US$ 69", v: 69, cue: "69", cor: colors.textDim },
      { rotulo: "Agora", valor: "US$ 22", v: 22, cue: "22", cor: colors.danger },
    ]}
    nota={{ texto: "Menos de um terço do que ficava um ano antes.", cue: "terco" }}
  />
);

// ---------------- 3. preço x custo ----------------
export const F03Preco = painel({
  kicker: "O paradoxo",
  titulo: "Mais caro para o produtor, menos lucro para a empresa",
  linhas: [
    { rotulo: "Preço médio ao cliente", valor: "US$ 452 → US$ 527 por tonelada", cue: "527" },
    { rotulo: "O produtor", valor: "pagando mais", cue: "pagando" },
    { rotulo: "A empresa", valor: "ganhando menos", cue: "ganhando" },
    { rotulo: "Por quê", valor: "o custo sobe mais rápido que o preço", cue: "custo", destaque: true },
  ],
  tint: "danger",
});

// ---------------- 4. o caixa ----------------
export const F04Caixa: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Mosaic Fertilizantes · segundo trimestre"
    titulo="Geração de caixa operacional"
    tint={colors.danger}
    max={170}
    barras={[
      { rotulo: "Um ano antes", valor: "US$ 159 milhões", v: 159, cue: "159", cor: colors.textDim },
      { rotulo: "Agora", valor: "US$ 60 milhões", v: 60, cue: "60", cor: colors.danger },
    ]}
    nota={{ texto: "Queda de 62,3 %.", cue: "62" }}
  />
);

// ---------------- 5. os cortes (MAPA) ----------------
export const F05Cortes: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="A PARTIR DE 8 DE JULHO DE 2026 · PAUSAS, HIBERNAÇÕES E REDUÇÕES"
    pontos={[
      { nome: "Araxá e Patrocínio", lat: -19.59, lon: -46.94, data: "CERCA DE 1.200 TRABALHADORES", cue: "araxa" },
      { nome: "Catalão", lat: -18.17, lon: -47.94, data: "CERCA DE 650 EM SUSPENSÃO", cue: "catalao" },
      { nome: "Candeias", lat: -12.67, lon: -38.55, data: "CERCA DE 500", cue: "candeias" },
      { nome: "Uberaba", lat: -19.75, lon: -47.93, data: "REDUÇÃO", cue: "uberaba" },
      { nome: "Sorriso", lat: -12.55, lon: -55.71, data: "REDUÇÃO", cue: "sorriso" },
    ]}
    setas={[]}
  />
);

// ---------------- 6. o enxofre (MAPA) ----------------
export const F06Ormuz: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="CERCA DE 60 % DO ENXOFRE DERIVADO DE PETRÓLEO PASSA POR ORMUZ"
    tint={colors.danger}
    lugares={[
      { nome: "Estreito de Ormuz", lat: 26.57, lon: 56.25, cue: "hormuz" },
      { nome: "Brasil", lat: -25.52, lon: -48.51, cue: "panico", abaixo: true },
    ]}
  />
);

// ---------------- 7. Heringer ----------------
export const F07Heringer = painel({
  kicker: "Fertilizantes Heringer · primeiro semestre de 2026",
  titulo: "Os números do desespero",
  linhas: [
    { rotulo: "Receita", valor: "−55 %, para 316,5 milhões de reais", cue: "55" },
    { rotulo: "Volume no segundo trimestre", valor: "274 mil t → 103 mil t", cue: "103" },
    { rotulo: "Prejuízo no segundo trimestre", valor: "37 milhões de reais", cue: "37" },
    { rotulo: "Passivo total", valor: "813 milhões de reais", cue: "813", destaque: true },
  ],
  tint: "danger",
});

// ---------------- 8. o mercado ----------------
export const F08Mercado: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Consumo de fertilizantes no Brasil · milhões de toneladas"
    titulo="O mercado encolhe"
    tint={colors.accent}
    max={50}
    barras={[
      { rotulo: "2025 · recorde", valor: "cerca de 49", v: 49, cue: "49", cor: colors.textDim },
      { rotulo: "2026 · estimativa", valor: "entre 42 e 45", v: 43.5, cue: "42", cor: colors.danger },
      { rotulo: "Rabobank", valor: "45,1 (−8,2 %)", v: 45.1, cue: "rabobank", cor: colors.accent },
    ]}
    nota={{ texto: "O menor volume desde 2022.", cue: "2022" }}
  />
);
