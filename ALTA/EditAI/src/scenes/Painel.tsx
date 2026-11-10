// Painel de dado: o mesmo desenho para as animações que explicam NÚMERO — rótulo pequeno em cima, valor
// grande embaixo, uma linha por dado, cada uma entrando no cue da palavra em que a narração diz aquele dado.
// As animações de MECANISMO (osmose, empuxo, dolina) têm desenho próprio, em MarMortoScenes.tsx.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { Kicker, SceneBackground, SceneProps, cue, enter, exit, prog } from "./shared";

export type Linha = { rotulo: string; valor: string; cue?: string; destaque?: boolean };
export type PainelSpec = {
  kicker: string;
  titulo?: string;
  linhas: Linha[];
  nota?: string;
  notaCue?: string;
  tint?: "cool" | "accent" | "danger";
  colunas?: boolean;   // dados lado a lado em vez de empilhados
};

export const Painel: React.FC<SceneProps & { spec: PainelSpec }> = (p) => {
  const frame = useCurrentFrame();
  const s = p.spec;
  const tint = s.tint === "danger" ? colors.danger : s.tint === "accent" ? colors.accent : colors.cool;
  const at = (l: Linha, i: number) => (l.cue ? cue(p, l.cue, 0.16 + i * 0.18) : Math.round(p.dur * (0.16 + i * 0.18)));
  const notaAt = s.notaCue ? cue(p, s.notaCue, 0.84) : Math.round(p.dur * 0.84);
  const col = s.colunas === true || (s.colunas !== false && s.linhas.length >= 4 && s.linhas.every((l) => l.valor.length <= 16));
  // Oswald é condensada: ~0,46 x o corpo por caractere. Conta as linhas em que o valor QUEBRA,
  // senão um valor de duas linhas encosta no rótulo de baixo (era o caso das nove recomendações).
  const nLinhas = (valor: string, fs: number, larg: number) => {
    const cabe = Math.max(8, Math.floor(larg / (fs * 0.46)));
    let linhas = 1;
    let atual = 0;
    for (const palavra of valor.split(" ")) {
      const passo = atual === 0 ? palavra.length : atual + 1 + palavra.length;
      if (passo > cabe) {
        linhas += 1;
        atual = palavra.length;
      } else {
        atual = passo;
      }
    }
    return linhas;
  };
  const altura = (l: Linha, larg: number) => {
    const fs = l.destaque ? 92 : 58;
    return 39 + nLinhas(l.valor, fs, larg) * fs * 1.05 + (l.destaque ? 30 : 28);
  };
  return (
    <AbsoluteFill style={exit(frame, p.dur)}>
      <SceneBackground tint={tint} />
      <div style={{ position: "absolute", left: 140, top: 84, ...type.bodyMedium }}>
        <Kicker text={s.kicker} delay={2} color={tint} />
      </div>
      {s.titulo ? (
        <div style={{ position: "absolute", left: 150, top: 176, width: 1640, ...type.display, fontSize: 68, color: colors.text, ...enter(frame, 8, 26) }}>
          {s.titulo}
        </div>
      ) : null}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <line x1={150} y1={286} x2={150 + 1620 * prog(frame, 14, 46)} y2={286} stroke={tint} strokeWidth={5} />
      </svg>
      {s.linhas.map((l, i) => {
        const a = at(l, i);
        const x = col ? 150 + (i % 2) * 860 : 150;
        // empilhado: cada linha ocupa a altura do SEU valor (o destaque de 92 px encostava no rótulo seguinte com passo fixo)
        const larg = col ? 820 : 1620;
        const y = col ? 340 + Math.floor(i / 2) * 250 : 330 + s.linhas.slice(0, i).reduce((acc, q) => acc + altura(q, larg), 0);
        return (
          <div key={l.rotulo} style={{ position: "absolute", left: x, top: y, width: larg }}>
            <div style={{ ...type.bodyMedium, fontSize: 26, letterSpacing: 3, color: colors.textDim, ...enter(frame, a, 14) }}>
              {l.rotulo.toUpperCase()}
            </div>
            <div
              style={{
                ...type.display, fontSize: l.destaque ? 92 : 58, lineHeight: 1.05, marginTop: 8,
                color: l.destaque ? colors.accent : colors.text, ...enter(frame, a + 6, 16),
              }}
            >
              {l.valor}
            </div>
          </div>
        );
      })}
      {s.nota ? (
        <div
          style={{
            position: "absolute", left: 150, bottom: 84, width: 1620, ...type.displayMedium, fontSize: 40,
            color: tint, ...enter(frame, notaAt, 20),
          }}
        >
          {s.nota}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
