// Animações de "Os 5 Submarinos Mais Pesados da História" (pt) — painel 20261012-085348 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. Ohio (p01)
export const S01Ohio: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "5º lugar · Marinha dos EUA", titulo: "Classe Ohio", linhas: [
    { rotulo: "Submerso", valor: `≈18.750${NB}t`, cue: "18", destaque: true },
    { rotulo: "Comprimento", valor: `170${NB}m`, cue: "170" },
    { rotulo: "Tripulantes", valor: "155", cue: "155" },
    { rotulo: "Tubos de mísseis", valor: "24", cue: "24" },
  ], tint: "accent" }} />
);

// 2. Azul e Dourada (p13)
export const S02Tripulacoes: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="77" linhas={[
    "MARINHA DOS EUA · CLASSE OHIO · DUAS TRIPULAÇÕES",
    "· Tripulação AZUL e tripulação DOURADA",
    "· 77 dias no mar",
    "· 35 dias de troca, abastecimento e reparos",
    "",
    "· Uma patrulha, a outra treina em terra",
  ]} chave={2} carimbo={{ texto: "SEM VER O SOL", cue: "sol" }} />
);

// 3. Borei (p18)
export const S03Borei: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "4º lugar · Marinha da Rússia", titulo: "Classe Borei", linhas: [
    { rotulo: "Submerso", valor: `≈24.000${NB}t`, cue: "24", destaque: true },
    { rotulo: "Comprimento", valor: `170${NB}m`, cue: "170" },
    { rotulo: "Mísseis Bulava", valor: "16", cue: "16" },
    { rotulo: "Tripulação", valor: "≈107", cue: "107" },
  ], tint: "accent" }} />
);

// 4. a pressão do mar (p24)
export const S04Pressao: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="PRESSÃO DO MAR A 400 M DE PROFUNDIDADE" valor={41} cue="41" sufixo="× o ar" sep="."
    nota={{ texto: "A cada 10 m: mais 1 atmosfera", cue: "100" }}
    barras={[{ rotulo: "A 100 metros", v: 11, cue: "11" }, { rotulo: "A 400 metros", v: 41, cue: "41", destaque: true }]} />
);

// 5. Oscar II (p31)
export const S05Oscar: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="3º LUGAR · OSCAR II · SUBMERSO" valor={24000} cue="24" sufixo={`${NB}t`} sep="."
    nota={{ texto: `Na superfície: ≈14.700${NB}t`, cue: "14" }} />
);

// 6. Belgorod (p42)
export const S06Belgorod: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "2º lugar · números nunca publicados", titulo: "Belgorod: estimativas", linhas: [
    { rotulo: "Na superfície", valor: `≈14.700${NB}t`, cue: "14" },
    { rotulo: "Submerso", valor: `24.000 a 30.000${NB}t`, cue: "24" },
    { rotulo: "Estimativa mais alta", valor: `≈30.000${NB}t`, cue: "30", destaque: true },
  ], tint: "accent" }} />
);

// 7. Typhoon (p54)
export const S07Typhoon: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "1º lugar · Projeto 941", titulo: "Typhoon", linhas: [
    { rotulo: "Comprimento", valor: `175${NB}m`, cue: "175" },
    { rotulo: "Largura", valor: `23${NB}m`, cue: "23" },
    { rotulo: "Calado", valor: `12${NB}m`, cue: "12" },
    { rotulo: "Submerso", valor: `48.000${NB}t`, cue: "48", destaque: true },
  ], tint: "accent" }} />
);

// 8. profundidade de teste (p61)
export const S08Reatores: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="TYPHOON · PROFUNDIDADE DE TESTE" valor={400} cue="400" sufixo={`${NB}m`} sep="."
    nota={{ texto: "Mais de 120 dias submerso", cue: "120" }} />
);

// 9. flutuabilidade de reserva (p69)
export const S09Reserva: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="FLUTUABILIDADE DE RESERVA" valor={48} cue="48" sufixo="%" sep="."
    nota={{ texto: `≈25.000${NB}t de água trocadas por ar`, cue: "25" }}
    barras={[{ rotulo: "Typhoon (%)", v: 48, cue: "48", destaque: true }, { rotulo: "Ohio (%)", v: 12, cue: "12" }]} />
);

// 10. MAPA: Mar de Barents (p76)
export const S10Barents: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="KURSK · 12 DE AGOSTO DE 2000" lugares={[
    { nome: "Frota do Norte", lat: 69.07, lon: 33.42, cue: "barent", abaixo: true },
    { nome: "Kursk", lat: 69.62, lon: 37.58, cue: "kursk", esquerda: true },
  ]} linhas={[{ pontos: [[70.7, 23.0], [70.9, 25.5], [70.1, 28.5], [69.9, 30.0], [69.7, 31.5], [69.4, 33.0], [69.2, 33.5],
    [69.3, 35.0], [69.0, 36.5], [68.6, 38.5], [68.2, 39.8], [67.8, 41.0], [67.2, 41.3], [66.6, 40.5], [66.2, 39.0]] }]}
    tint={colors.accent} />
);

// 11. o bilhete de Kolesnikov (p83)
export const S11Bilhete: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="kolesnikov" linhas={[
    "KURSK · BILHETE DO CAPITÃO-TENENTE D. KOLESNIKOV",
    "· Nono compartimento, na popa",
    "· Somos 23 aqui",
    "",
    "· Nenhum de nós consegue chegar à superfície",
  ]} chave={4} carimbo={{ texto: "NENHUM DE NÓS", cue: "nenhum" }} />
);
