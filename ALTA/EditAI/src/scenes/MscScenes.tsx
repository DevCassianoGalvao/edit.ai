// Animações de "Os Maiores Navios Porta-Contêineres Feitos na China" (pt) — painel 20261031-111153 (baia b1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto; todo número é dito; milhar com ponto (pt).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. o que é um TEU (p02)
export const S01TEU: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "A MEDIDA DO COMÉRCIO MUNDIAL", titulo: "TEU · unidade equivalente a 20 pés", linhas: [
    { rotulo: "Contêiner curto · vale 1 TEU", valor: `20${NB}pés · ≈${NB}6${NB}m`, cue: "20", destaque: true },
    { rotulo: "Contêiner comum nos portos · vale 2 TEU", valor: `40${NB}pés · ≈${NB}12${NB}m`, cue: "40" },
  ], tint: "accent" }} />
);

// 2. dois irmãos, dois estaleiros (p08)
export const S02Irmaos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "MESMO DIA DE ENTREGA · DOIS ESTALEIROS CHINESES", titulo: "Capacidade informada", linhas: [
    { rotulo: "MSC Tessa · Hudong-Zhonghua (Xangai)", valor: `24.116${NB}TEU`, cue: "116" },
    { rotulo: "MSC Irina · Yangzi Xinfu (Jingjiang)", valor: `24.346${NB}TEU`, cue: "346", destaque: true },
  ], tint: "accent" }} />
);

// 3. o endereço de cada caixa (p29)
export const S03Enderecos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "O ENDEREÇO DE CADA CAIXA", titulo: "Plano de estiva · três números", linhas: [
    { rotulo: "Primeiro número · baia", valor: "posição de proa a popa", cue: "baia" },
    { rotulo: "Segundo número · fileira", valor: "da linha central para os lados", cue: "fileira" },
    { rotulo: "Terceiro número · camada", valor: "a altura", cue: "camada", destaque: true },
  ], tint: "accent" }} />
);

// 4. o lastro compensa (p42)
export const S04Lastro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "UMA DANÇA ENTRE A CARGA E A ÁGUA", titulo: "Enquanto o guindaste trabalha", linhas: [
    { rotulo: "O guindaste coloca", valor: `20${NB}toneladas à direita`, cue: "20", destaque: true },
    { rotulo: "O navio tende a", valor: "inclinar para a direita", cue: "inclinar" },
    { rotulo: "Os oficiais bombeiam água para", valor: "tanques da esquerda", cue: "esquerdo" },
  ], tint: "accent" }} />
);

// 5. a maior carga já transportada (p51)
export const S05Recorde: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="MAIOR CARGA JÁ TRANSPORTADA POR UM SÓ NAVIO" valor={22233} cue="22" sufixo=" TEU" sep="."
    nota={{ texto: "numa única viagem · Singapura → Felixstowe", cue: "singapura" }} />
);

// 6. MAPA: os canais por onde os gigantes passam (p70)
export const S06Canais: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="CANAIS QUE LIMITAM O TAMANHO DO NAVIO" lugares={[
    { nome: "Canal do Panamá", lat: 9.08, lon: -79.68, cue: "panam", esquerda: true },
    { nome: "Canal de Suez", lat: 30.46, lon: 32.35, cue: "suez" },
  ]} tint={colors.accent} />
);

// 7. o peso verificado (p77)
export const S07Peso: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="2016" linhas={[
    "A PARTIR DE 2016 · REGRA INTERNACIONAL",
    "TODO CONTÊINER TEM O PESO VERIFICADO",
    "· pesando a caixa inteira",
    "· ou somando tudo que está dentro",
    "SEM O NÚMERO CONFIRMADO, NÃO EMBARCA",
  ]} chave={1} carimbo={{ texto: "PESO VERIFICADO", cue: "confirmado" }} />
);

// 8. os números do MSC Irina (p87)
export const S08Recap: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "OS NÚMEROS DO GIGANTE", titulo: "MSC Irina", linhas: [
    { rotulo: "Comprimento", valor: `quase 400${NB}m`, cue: "400" },
    { rotulo: "Largura", valor: `61,3${NB}m`, cue: "61" },
    { rotulo: "Capacidade", valor: `24.346${NB}TEU`, cue: "24", destaque: true },
    { rotulo: "Entregue em", valor: `9${NB}de março de 2023`, cue: "9" },
  ], tint: "accent", colunas: false }} />
);
