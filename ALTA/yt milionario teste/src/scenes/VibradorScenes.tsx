// As 8 animações de "O vibrador — a peça que zumbia no rádio do carro" (pt, 29 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Barras, Lista (2), Odometro, Painel, Documento,
// Colunas (2). Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES (grafia do Whisper: "6", "115").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. a equação ingrata ----------------
export const A01Tensao: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Tensão, em volts"
    titulo="Uma equação ingrata"
    tint={colors.danger}
    max={300}
    barras={[
      { rotulo: "Bateria do carro (corrente contínua)", valor: "6 V", v: 6, cue: "6", cor: colors.cool },
      { rotulo: "Placa das válvulas", valor: "centenas de volts", v: 300, cue: "centenas", cor: colors.danger },
    ]}
    nota={{ texto: "E no meio, um espaço minúsculo atrás do painel, que sacudia, esquentava e congelava.", cue: "minusculo" }}
  />
);

// ---------------- 2. o dinamotor ----------------
export const A02Dinamotor: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="A segunda solução: o dinamotor"
    titulo="Robusto — mas exagerado para o motorista comum"
    tint={colors.accent}
    itens={[
      { titulo: "Pesado", cue: "pesado" },
      { titulo: "Consumia bastante corrente", cue: "consumia" },
      { titulo: "Ruído de rotação constante", cue: "ruido" },
      { titulo: "Custava caro", cue: "caro", cor: colors.danger },
    ]}
  />
);

// ---------------- 3. o ciclo da palheta ----------------
export const A03Ciclo: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Como o vibrador funcionava"
    titulo="Uma campainha elétrica que nunca para"
    tint={colors.cool}
    itens={[
      { titulo: "A corrente passa pela bobina", cue: "bobina" },
      { titulo: "A bobina puxa a palheta de metal", cue: "puxava" },
      { titulo: "A palheta abre o próprio contato", cue: "abria" },
      { titulo: "A mola devolve a palheta e fecha o contato", cue: "voltava", cor: colors.accent },
    ]}
    nota={{ texto: "Sem parar: um vaivém contínuo.", cue: "sozinha" }}
  />
);

// ---------------- 4. a frequência ----------------
export const A04Frequencia: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="UM VIBRADOR TÍPICO DE RÁDIO DE CARRO"
    valor={115}
    cue="115"
    prefixo="~"
    sufixo=" vezes por segundo"
    nota={{ texto: "Mais de 100 batidas a cada segundo, enquanto o rádio estivesse ligado.", cue: "batidas" }}
  />
);

// ---------------- 5. o vibrador síncrono ----------------
export const A05Sincrono = painel({
  kicker: "O vibrador síncrono",
  titulo: "Uma peça, duas funções",
  linhas: [
    { rotulo: "Segundo conjunto de contatos", valor: "no secundário do transformador", cue: "segundo" },
    { rotulo: "Inversão no instante exato", valor: "a cada troca de polaridade", cue: "polaridade" },
    { rotulo: "Saída", valor: "já retificada", cue: "retificada", destaque: true },
    { rotulo: "Resultado", valor: "sem válvula retificadora", cue: "economizava" },
  ],
  tint: "cool",
});

// ---------------- 6. os sintomas ----------------
export const A06Sintomas: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="sintomas"
    chave={5}
    linhas={[
      "OFICINA DE RÁDIO — FICHA DE SERVIÇO",
      "Rádio demora para funcionar.",
      "Som cortando. Zumbido irregular e áspero.",
      "Volta a tocar com um tapa no painel.",
      "",
      "Contatos soldados — fusível queimado.",
    ]}
    carimbo={{ texto: "TROCAR VIBRADOR", cue: "fusivel" }}
  />
);

// ---------------- 7. o rádio híbrido ----------------
export const A07Hibrido: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="O rádio híbrido — metade válvula, metade transistor"
    tint={colors.accent}
    cols={[
      { titulo: "Sem transformador", texto: "de alta tensão.", cue: "transformador" },
      { titulo: "Sem retificador", texto: "", cue: "retificador" },
      { titulo: "Sem capacitor", texto: "amortecedor.", cue: "amortecedor" },
      { titulo: "Sem vibrador", texto: "Pela primeira vez em duas décadas.", cue: "vibrador", cor: colors.danger },
    ]}
  />
);

// ---------------- 8. a herança ----------------
export const A08Fonte: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="A mesma ideia, hoje: a fonte chaveada"
    tint={colors.cool}
    cols={[
      { titulo: "Carregador do celular", texto: "Liga e desliga a corrente.", cue: "celular" },
      { titulo: "Fonte do computador", texto: "O mesmo princípio.", cue: "computador" },
      { titulo: "Inversor de 12 V", texto: "Do carro para a tomada.", cue: "inversores" },
      { titulo: "Transistores", texto: "Sem peças móveis, sem faíscas, sem zumbido.", cue: "moveis", cor: colors.accent },
    ]}
  />
);
