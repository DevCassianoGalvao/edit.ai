// As 7 animações de "Revendas de máquinas agrícolas no vermelho" (pt, 22,5 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Painel (2), Barras (2), Documento, Odometro (2).
// Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES (grafia do Whisper: "R $ 9 ,5" -> cue "9";
// "1 .263" -> cue "263"; "36 ,8" -> "36"; "Iagco" no lugar de Ágco).
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. Automob ----------------
export const R01Automob = painel({
  kicker: "Automob · desde 2021",
  titulo: "Crescimento agressivo",
  linhas: [
    { rotulo: "Aquisições", valor: "pelo menos 7", cue: "sete" },
    { rotulo: "Lojas", valor: "de 14 para 120", cue: "120" },
    { rotulo: "Receita", valor: "de R$ 700 milhões para R$ 9,5 bilhões (projeção)", cue: "9" },
    { rotulo: "Máquinas agrícolas", valor: "R$ 3,2 bilhões por ano", cue: "3", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 2. prejuízo que dobra ----------------
export const R02Prejuizo: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Automob · 2º trimestre de 2026"
    titulo="Vende mais, perde mais"
    tint={colors.danger}
    max={87.5}
    barras={[
      { rotulo: "Prejuízo ajustado · antes", valor: "R$ 36,8 milhões", v: 36.8, cue: "36", cor: colors.textDim },
      { rotulo: "Prejuízo ajustado · agora", valor: "R$ 87,5 milhões", v: 87.5, cue: "87", cor: colors.danger },
    ]}
    nota={{ texto: "Receita +12 % · geração de caixa +25 %", cue: "dobrou" }}
  />
);

// ---------------- 3. covenants ----------------
export const R03Covenants: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="covenants"
    chave={5}
    linhas={[
      "CRA SLC MÁQUINAS — R$ 600 MILHÕES",
      "Cláusulas de proteção (covenants)",
      "",
      "1. Liquidez corrente: no mínimo 0,9 vez",
      "2. Endividamento: até 2,5 vezes o patrimônio líquido",
      "3. Dívida líquida: até 4 vezes a geração de caixa",
      "Quebra de qualquer regra = vencimento antecipado",
    ]}
    carimbo={{ texto: "RISCO DE VENCIMENTO", cue: "antecipado" }}
  />
);

// ---------------- 4. Tecnomaac ----------------
export const R04Tecnomaac: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="GRUPO TECNOMAAC · MARACAJU (MS) · RECUPERAÇÃO JUDICIAL"
    valor={276}
    cue="276"
    prefixo="R$ "
    sufixo=" milhões"
    sep="."
    nota={{ texto: "352 credores · cobranças suspensas por 180 dias.", cue: "180" }}
  />
);

// ---------------- 5. Abimaq ----------------
export const R05Abimaq = painel({
  kicker: "Abimaq · máquinas agrícolas",
  titulo: "O mercado encolheu",
  linhas: [
    { rotulo: "Janeiro a julho de 2026", valor: "R$ 26,2 bilhões", cue: "26" },
    { rotulo: "Queda", valor: "−25,8 %", cue: "25", destaque: true },
    { rotulo: "Só em julho", valor: "R$ 4,86 bilhões (−27,5 %)", cue: "27" },
    { rotulo: "Tratores vendidos em julho", valor: "6.981", cue: "981" },
  ],
  tint: "danger",
});

// ---------------- 6. produtores em recuperação ----------------
export const R06Recuperacao: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="PRODUTORES RURAIS EM RECUPERAÇÃO JUDICIAL · 1º SEMESTRE DE 2026"
    valor={1263}
    cue="263"
    sep="."
    nota={{ texto: "+66 % em apenas um ano.", cue: "66" }}
  />
);

// ---------------- 7. Plano Safra ----------------
export const R07PlanoSafra: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Plano Safra · julho de 2026 · agricultura empresarial"
    titulo="Para comprar máquina, quase nada"
    tint={colors.accent}
    max={28.2}
    barras={[
      { rotulo: "Total contratado", valor: "R$ 28,2 bilhões", v: 28.2, cue: "28", cor: colors.textDim },
      { rotulo: "CPRs", valor: "R$ 18,8 bilhões", v: 18.8, cue: "18", cor: colors.textDim },
      { rotulo: "Custeio", valor: "R$ 6,5 bilhões", v: 6.5, cue: "6", cor: colors.textDim },
      { rotulo: "Investimento (máquinas)", valor: "R$ 568 milhões — 2 %", v: 0.568, cue: "568", cor: colors.danger },
    ]}
  />
);
