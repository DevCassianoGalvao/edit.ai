// Animações de "Rio de Janeiro, 1950: como se vivia sem geladeira" (pt) — painel 20261024-145901-narracao-rio-1950
// (baia b1, modo enxuto). REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

// costa do Rio (lat, lon) — aproximada: Leblon -> Copacabana -> Botafogo -> Centro -> porto
const COSTA_RIO: [number, number][] = [[-22.988, -43.225], [-22.986, -43.205], [-22.988, -43.19], [-22.978, -43.185],
  [-22.968, -43.177], [-22.962, -43.166], [-22.955, -43.156], [-22.944, -43.168], [-22.931, -43.172], [-22.916, -43.168],
  [-22.903, -43.171], [-22.895, -43.183], [-22.885, -43.205]];
const NITEROI: [number, number][] = [[-22.94, -43.128], [-22.915, -43.125], [-22.895, -43.118], [-22.875, -43.105]];

// 1. MAPA: a capital em 1950 (p01)
export const R01Mapa: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="RIO DE JANEIRO · 1950 · CAPITAL DO BRASIL" lugares={[
    { nome: "Copacabana", lat: -22.971, lon: -43.183, cue: "copacabana", abaixo: true },
    { nome: "Centro", lat: -22.906, lon: -43.178, cue: "centro" },
    { nome: "Maracanã", lat: -22.912, lon: -43.230, cue: "maracan", esquerda: true },
  ]} linhas={[{ pontos: COSTA_RIO }, { pontos: NITEROI }]} tint={colors.accent} />
);

// 2. a caderneta do armazém (p07)
export const R02Caderneta: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="100" linhas={[
    "ARMAZÉM DA ESQUINA · CADERNETA DO FREGUÊS",
    "100 GRAMAS DE MANTEIGA",
    "200 GRAMAS DE QUEIJO",
    "MEIA DÚZIA DE OVOS",
    "PAGA NO FIM DO MÊS",
  ]} chave={1} carimbo={{ texto: "COMPRAR POUCO", cue: "método" }} />
);

// 3. o leite em lata (p13)
export const R03Lata: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="condensado" linhas={[
    "O LEITE QUE NÃO AZEDAVA",
    "LEITE CONDENSADO · LEITE EM PÓ",
    "ANUNCIADO NA REVISTA O CRUZEIRO",
    "FECHADA · MESES NA PRATELEIRA",
    "ABERTA · VOLTAVA A SER UM PROBLEMA",
  ]} chave={3} carimbo={{ texto: "CONTRA O CALOR", cue: "cruzeiro" }} />
);

// 4. o navio do gelo (p20)
export const R04Madagascar: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Baía de Guanabara", titulo: "O navio Madagascar", linhas: [
    { rotulo: "Chegada ao Rio", valor: "1834", cue: "1834" },
    { rotulo: "Carga", valor: "cerca de 200 toneladas de gelo", cue: "200", destaque: true },
    { rotulo: "Origem", valor: "lagos congelados de Boston", cue: "boston" },
  ], tint: "accent" }} />
);

// 5. o sorvete (p24)
export const R05Sorvete: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O gelo virou indústria", titulo: "O sorvete no Rio", linhas: [
    { rotulo: "1ª fábrica industrial do Brasil", valor: "começo dos anos 40", cue: "40" },
    { rotulo: "Eski-bon, sorvete de palito", valor: "1942", cue: "1942", destaque: true },
    { rotulo: "Carrinhos nas ruas e praias", valor: "1950", cue: "1950" },
  ], tint: "accent" }} />
);

// 6. a casa feita para o calor (p38)
export const R06Casa: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="3" linhas={[
    "A CASA CARIOCA CONTRA O CALOR",
    "PÉ-DIREITO DE 3 METROS OU MAIS",
    "VENEZIANAS DE MADEIRA NAS JANELAS",
    "BANDEIRAS ACIMA DAS PORTAS",
    "TELHAS DE BARRO · VARANDAS E ALPENDRES",
  ]} chave={1} carimbo={{ texto: "SEM AR-CONDICIONADO", cue: "bandeiras" }} />
);

// 7. a luz que faltava (p45)
export const R07Luz: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O ponto fraco da geladeira", titulo: "A luz no Rio", linhas: [
    { rotulo: "Década de 50", valor: "energia instável", cue: "50" },
    { rotulo: "Rotina da cidade", valor: "apagões e racionamento", cue: "apagões" },
    { rotulo: "Carnaval de 1954", valor: "marchinhas contra o escuro", cue: "1954", destaque: true },
  ], tint: "accent" }} />
);
