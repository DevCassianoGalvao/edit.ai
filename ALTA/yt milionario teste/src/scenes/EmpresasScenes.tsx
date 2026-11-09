// As 9 animações de "A onda silenciosa: 9,1 milhões de empresas com o nome sujo" (pt, padrão). Pedido do painel
// (automático, baia 1). REGRA (25/09 + 26/09/2026): biblioteca + MAPA — Odometro, Barras, Lista, MapaCampanha.
// Todo número é DITO na narração; cues na grafia do Whisper ("9 milhões e 100 mil" -> "9", "1.725" -> "1725").
import React from "react";
import { colors } from "../design/tokens";
import { Barras, Lista } from "./blocos";
import { Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. 9,1 milhões de empresas (p01) ----------------
export const E01Nove: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="SERASA EXPERIAN · JUNHO DE 2026"
    valor={9100000}
    cue="9"
    sep="."
    sufixo=" empresas"
    nota={{ texto: "com contas atrasadas, protestos e dívidas negativadas", cue: "protestos" }}
  />
);

// ---------------- 2. quase tudo é micro e pequena (p02) ----------------
export const E02Pequenas: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="EMPRESAS NEGATIVADAS · VIRADA DE 2025 PARA 2026"
    titulo="Quem são as empresas com o nome sujo"
    tint={colors.danger}
    max={100}
    barras={[
      { rotulo: "Micro e pequenas empresas", valor: "cerca de 95 %", v: 95, cue: "95", cor: colors.danger },
      { rotulo: "Médias e grandes", valor: "cerca de 5 %", v: 5, cue: "95" },
    ]}
    nota={{ texto: "mais de 210 bilhões de reais em dívidas negativadas", cue: "210" }}
  />
);

// ---------------- 3. a escada das recuperações judiciais (p05) ----------------
export const E03Escada: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="EMPRESAS EM RECUPERAÇÃO JUDICIAL · SERASA EXPERIAN"
    titulo="Uma escada que só sobe"
    tint={colors.danger}
    max={2600}
    barras={[
      { rotulo: "2023", valor: "1.725", v: 1725, cue: "1" },
      { rotulo: "2024", valor: "2.178", v: 2178, cue: "2" },
      { rotulo: "2025", valor: "2.466 · recorde", v: 2466, cue: "2", cor: colors.danger },
    ]}
  />
);

// ---------------- 4. os setores (p07) ----------------
export const E04Setores: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="RECUPERAÇÕES JUDICIAIS EM 2025 · POR SETOR"
    titulo="A crise não escolheu um alvo"
    tint={colors.accent}
    max={35}
    barras={[
      { rotulo: "Serviços", valor: "30 %", v: 30, cue: "30" },
      { rotulo: "Comércio", valor: "pouco mais de 21 %", v: 21, cue: "21" },
      { rotulo: "Indústria", valor: "pouco mais de 18 %", v: 18, cue: "18" },
      { rotulo: "Agropecuária", valor: "cerca de 30 %", v: 30, cue: "agropecuaria", cor: colors.danger },
    ]}
  />
);

// ---------------- 9. as falências que "caíram" (p09) ----------------
export const E09Falencias: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="PEDIDOS DE FALÊNCIA · 2025"
    valor={19}
    cue="19"
    prefixo="−"
    sufixo=" %"
    nota={{ texto: "o número esconde o que acontece com as pequenas", cue: "esconde" }}
  />
);

// ---------------- 5. Selic x o juro do pequeno (p15) ----------------
export const E05Juros: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="O CUSTO DO DINHEIRO · JUROS AO ANO"
    titulo="A Selic não é o juro do pequeno empresário"
    tint={colors.danger}
    max={50}
    barras={[
      { rotulo: "Selic no pico", valor: "15 %", v: 15, cue: "15" },
      { rotulo: "Selic em 2026", valor: "acima de 13 %", v: 13, cue: "13" },
      { rotulo: "Capital de giro da pequena empresa", valor: "30 % a 50 %", v: 50, cue: "mundo", cor: colors.danger },
    ]}
  />
);

// ---------------- 6. famílias endividadas (p21) ----------------
export const E06Familias: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="CONFEDERAÇÃO NACIONAL DO COMÉRCIO · JULHO DE 2026"
    valor={82}
    cue="82"
    sufixo=" % das famílias endividadas"
    nota={{ texto: "a renda já chega comprometida com parcelas", cue: "comprometida" }}
  />
);

// ---------------- 7. a tempestade perfeita (p29) ----------------
export const E07Fatores: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="A TEMPESTADE PERFEITA"
    titulo="Tudo ao mesmo tempo"
    tint={colors.danger}
    itens={[
      { titulo: "Juros entre os mais altos do mundo", cue: "juros" },
      { titulo: "Crédito mais restrito", cue: "credito" },
      { titulo: "Cliente endividado", cue: "cliente" },
      { titulo: "Dívidas antigas da pandemia", cue: "pandemia" },
      { titulo: "Custos subindo", cue: "custos" },
      { titulo: "Incerteza tributária", cue: "incerteza", cor: colors.danger },
    ]}
  />
);

// ---------------- 8. MAPA: o interior que vive da safra (p34) ----------------
const BRASIL: [number, number][] = [
  [4.4, -51.6], [2.0, -50.0], [-0.1, -49.0], [-1.2, -46.5], [-2.8, -42.0], [-2.9, -39.5], [-4.8, -37.2],
  [-5.2, -35.3], [-8.0, -34.8], [-10.9, -37.0], [-13.0, -38.5], [-15.8, -38.9], [-18.9, -39.7], [-21.0, -40.8],
  [-22.9, -42.0], [-23.0, -43.9], [-23.9, -46.3], [-25.5, -48.4], [-28.3, -48.7], [-30.3, -50.3], [-33.7, -53.4],
  [-30.2, -57.6], [-27.3, -55.6], [-25.6, -54.6], [-22.3, -55.7], [-19.9, -58.0], [-16.3, -58.3], [-15.5, -60.2],
  [-13.5, -61.0], [-11.0, -65.3], [-9.8, -67.3], [-9.5, -72.5], [-7.4, -73.8], [-4.2, -69.9], [-1.5, -69.4],
  [1.7, -67.3], [0.9, -63.7], [4.2, -60.1], [2.3, -56.1], [4.4, -51.6],
];
export const E08Interior: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="MUNICÍPIOS PEQUENOS E MÉDIOS · O INTERIOR"
    pontos={[
      { nome: "Mato Grosso", lat: -12.5, lon: -55.7, data: "CIDADES QUE VIVEM DA SAFRA", cue: "interior" },
      { nome: "Goiás", lat: -17.8, lon: -50.9, data: "COMÉRCIO LOCAL", cue: "mercadinho" },
      { nome: "Paraná", lat: -24.9, lon: -51.5, data: "REVENDA AGRÍCOLA", cue: "revenda", lado: "esq" },
      { nome: "Brasília", lat: -15.8, lon: -47.9, data: "O DINHEIRO PARA DE CIRCULAR", cue: "circular" },
    ]}
    setas={[]}
    costa={[BRASIL]}
  />
);
