// Blocos reaproveitáveis das animações (saíram de MojaveScenes.tsx em 21/09/2026 para não serem reescritos a
// cada filme): moldura com kicker, colunas, linha do tempo, barras e lista numerada.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { Kicker, SceneBackground, SceneProps, cue, enter, exit, prog } from "./shared";

export const Frame: React.FC<{
  p: SceneProps; kicker: string; tint: string; grid?: boolean; children: React.ReactNode;
}> = ({ p, kicker, tint, grid = false, children }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={exit(frame, p.dur)}>
      <SceneBackground tint={tint} grid={grid} />
      <div style={{ position: "absolute", left: 140, top: 84, ...type.bodyMedium }}>
        <Kicker text={kicker} delay={2} color={tint} />
      </div>
      {children}
    </AbsoluteFill>
  );
};

/** Colunas lado a lado, cada uma entra no cue da palavra em que a narração fala dela. */
export type Col = { titulo: string; texto: string; cue: string; cor?: string };
export const Colunas: React.FC<SceneProps & {
  kicker: string; cols: Col[]; tint: string; nota?: { texto: string; cue: string };
}> = (p) => {
  const frame = useCurrentFrame();
  const n = p.cols.length;
  const w = (1620 - (n - 1) * 40) / n;
  const notaAt = p.nota ? cue(p, p.nota.cue, 0.85) : 0;
  return (
    <Frame p={p} kicker={p.kicker} tint={p.tint} grid>
      {p.cols.map((c, i) => {
        const at = cue(p, c.cue, 0.15 + i * 0.2);
        const cor = c.cor ?? p.tint;
        return (
          <div key={i} style={{ position: "absolute", left: 150 + i * (w + 40), top: 300, width: w, ...enter(frame, at, 30) }}>
            <div style={{ height: 6, width: w, background: cor, marginBottom: 26 }} />
            <div style={{ ...type.display, fontSize: n >= 4 ? 48 : n === 3 ? 58 : 72, color: cor, lineHeight: 1.05 }}>{c.titulo}</div>
            <div style={{ ...type.bodyMedium, fontSize: n >= 4 ? 26 : 30, color: colors.text, marginTop: 20, lineHeight: 1.35 }}>{c.texto}</div>
          </div>
        );
      })}
      {p.nota ? (
        <div style={{ position: "absolute", left: 150, top: 860, width: 1620, ...type.bodyMedium, fontSize: 30,
                      color: colors.textDim, ...enter(frame, notaAt, 20) }}>
          {p.nota.texto}
        </div>
      ) : null}
    </Frame>
  );
};

/** Linha do tempo horizontal: cada marco acende no cue em que é dito. */
export type Marco = { ano: string; texto: string; cue: string; cor?: string };
export const LinhaDoTempo: React.FC<SceneProps & { kicker: string; marcos: Marco[]; tint: string }> = (p) => {
  const frame = useCurrentFrame();
  const n = p.marcos.length;
  const x0 = 220, x1 = 1700;
  const xs = p.marcos.map((_, i) => x0 + ((x1 - x0) * i) / Math.max(1, n - 1));
  const ats = p.marcos.map((m, i) => cue(p, m.cue, 0.15 + (0.7 * i) / Math.max(1, n - 1)));
  return (
    <Frame p={p} kicker={p.kicker} tint={p.tint} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <line x1={x0} y1={560} x2={x0 + (x1 - x0) * prog(frame, 6, 40)} y2={560} stroke={colors.line} strokeWidth={6} />
        {xs.map((x, i) => (
          <circle key={i} cx={x} cy={560} r={18} fill={p.marcos[i].cor ?? p.tint} opacity={prog(frame, ats[i], ats[i] + 12)} />
        ))}
      </svg>
      {p.marcos.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: xs[i] - 170, width: 340, top: i % 2 ? 610 : 340,
                              textAlign: "center", ...enter(frame, ats[i], 24) }}>
          <div style={{ ...type.display, fontSize: 52, color: m.cor ?? p.tint, lineHeight: 1 }}>{m.ano}</div>
          <div style={{ ...type.bodyMedium, fontSize: 25, color: colors.text, marginTop: 12, lineHeight: 1.3 }}>{m.texto}</div>
        </div>
      ))}
    </Frame>
  );
};

/** Barras horizontais comparando grandezas; cada barra cresce no seu cue. */
export type Barra = { rotulo: string; valor: string; v: number; cue: string; cor?: string };
export const Barras: React.FC<SceneProps & {
  kicker: string; titulo?: string; barras: Barra[]; tint: string; max: number; nota?: { texto: string; cue: string };
}> = (p) => {
  const frame = useCurrentFrame();
  const n = p.barras.length;
  const gap = Math.min(150, 560 / n);
  return (
    <Frame p={p} kicker={p.kicker} tint={p.tint} grid>
      {p.titulo ? (
        <div style={{ position: "absolute", left: 150, top: 170, ...type.display, fontSize: 60, color: colors.text,
                      ...enter(frame, 6, 20) }}>{p.titulo}</div>
      ) : null}
      {p.barras.map((b, i) => {
        const at = cue(p, b.cue, 0.15 + i * 0.15);
        const w = 1250 * (b.v / p.max) * prog(frame, at, at + 26);
        const y = 320 + i * gap;
        const cor = b.cor ?? p.tint;
        return (
          <div key={i}>
            <div style={{ position: "absolute", left: 150, top: y - 38, ...type.bodyMedium, fontSize: 25,
                          color: colors.textDim, letterSpacing: 2, ...enter(frame, at, 10) }}>{b.rotulo.toUpperCase()}</div>
            <div style={{ position: "absolute", left: 150, top: y, width: w, height: 56, background: cor }} />
            <div style={{ position: "absolute", left: 170 + w, top: y + 2, ...type.display, fontSize: 46, color: cor,
                          ...enter(frame, at + 14, 10) }}>{b.valor}</div>
          </div>
        );
      })}
      {p.nota ? (
        <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.bodyMedium, fontSize: 30,
                      color: colors.textDim, ...enter(frame, cue(p, p.nota.cue, 0.85), 20) }}>{p.nota.texto}</div>
      ) : null}
    </Frame>
  );
};

/** Lista numerada: um item por linha, cada um entrando no cue da palavra que o nomeia. */
export type Item = { titulo: string; texto?: string; cue: string; cor?: string };
export const Lista: React.FC<SceneProps & {
  kicker: string; titulo?: string; itens: Item[]; tint: string; nota?: { texto: string; cue: string };
}> = (p) => {
  const frame = useCurrentFrame();
  const n = p.itens.length;
  const gap = Math.min(130, 520 / Math.max(1, n));
  return (
    <Frame p={p} kicker={p.kicker} tint={p.tint} grid>
      {p.titulo ? (
        <div style={{ position: "absolute", left: 150, top: 176, width: 1640, ...type.display, fontSize: 64,
                      color: colors.text, ...enter(frame, 6, 20) }}>{p.titulo}</div>
      ) : null}
      {p.itens.map((it, i) => {
        const at = cue(p, it.cue, 0.2 + i * 0.16);
        const cor = it.cor ?? p.tint;
        const y = 330 + i * gap;
        return (
          <div key={i} style={{ position: "absolute", left: 150, top: y, width: 1620, display: "flex",
                                alignItems: "baseline", gap: 26, ...enter(frame, at, 24) }}>
            <div style={{ ...type.display, fontSize: 46, color: cor, width: 74 }}>{String(i + 1).padStart(2, "0")}</div>
            <div>
              <div style={{ ...type.display, fontSize: 52, color: colors.text, lineHeight: 1.05 }}>{it.titulo}</div>
              {it.texto ? (
                <div style={{ ...type.bodyMedium, fontSize: 28, color: colors.textDim, marginTop: 8 }}>{it.texto}</div>
              ) : null}
            </div>
          </div>
        );
      })}
      {p.nota ? (
        <div style={{ position: "absolute", left: 150, top: 930, width: 1620, ...type.bodyMedium, fontSize: 30,
                      color: colors.textDim, ...enter(frame, cue(p, p.nota.cue, 0.85), 20) }}>{p.nota.texto}</div>
      ) : null}
    </Frame>
  );
};
