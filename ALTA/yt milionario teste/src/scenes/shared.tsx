import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame } from "remotion";
import { EASE_IN_OUT, EASE_OUT_EXPO, colors, fmtEs, springs } from "../design/tokens";
import { Easing } from "remotion";

/** dur = duração do beat; t0 = quadro absoluto de início; cues = quadro LOCAL em que cada palavra-chave é dita. */
export type SceneProps = { dur: number; t0: number; cues?: Record<string, number> };

/** Quadro local de uma palavra-chave; se o cue não existir, usa a fração `fallback` da duração. */
export const cue = (p: SceneProps, key: string, fallback: number) => {
  const v = p.cues?.[key];
  return typeof v === "number" ? Math.max(0, Math.min(p.dur - 20, v)) : Math.round(p.dur * fallback);
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Entrada escalonada: opacidade + deslocamento com expo-out. */
export function enter(frame: number, delay: number, distance = 40, len = 20) {
  const l = frame - delay;
  const o = interpolate(l, [0, len], [0, 1], { ...clamp, easing: EASE_OUT_EXPO });
  const y = interpolate(l, [0, len], [distance, 0], { ...clamp, easing: Easing.spring(springs.snappy) });
  return { opacity: o, translate: `0px ${y}px` };
}

/** Saída deliberada nos últimos `len` quadros do beat. */
export function exit(frame: number, dur: number, len = 14) {
  return {
    opacity: interpolate(frame, [dur - len, dur], [1, 0], { ...clamp, easing: EASE_IN_OUT }),
  };
}

export const prog = (frame: number, a: number, b: number, easing = EASE_OUT_EXPO) =>
  interpolate(frame, [a, Math.max(b, a + 1)], [0, 1], { ...clamp, easing }); // cues no mesmo quadro nunca geram intervalo vazio

/** Fundo em 3 camadas: gradiente naval, grade técnica em deriva e grão determinístico. */
export const SceneBackground: React.FC<{ tint?: string; grid?: boolean }> = ({ tint = colors.cool, grid = true }) => {
  const frame = useCurrentFrame();
  const drift = frame * 0.25;
  return (
    <AbsoluteFill style={{ background: colors.bg }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at ${50 + Math.sin(frame / 90) * 6}% 35%, ${colors.bgElevated} 0%, ${colors.bg} 68%)`,
        }}
      />
      {grid ? (
        <AbsoluteFill
          style={{
            opacity: 0.22,
            backgroundImage: `linear-gradient(${colors.line} 1px, transparent 1px), linear-gradient(90deg, ${colors.line} 1px, transparent 1px)`,
            backgroundSize: "80px 80px",
            backgroundPosition: `${drift}px ${drift * 0.5}px`,
            maskImage: "radial-gradient(ellipse at center, black 30%, transparent 75%)",
          }}
        />
      ) : null}
      <AbsoluteFill style={{ background: `linear-gradient(180deg, transparent 55%, ${tint}1f 100%)` }} />
      <Grain />
      <AbsoluteFill style={{ boxShadow: "inset 0 0 260px rgba(0,0,0,0.85)" }} />
    </AbsoluteFill>
  );
};

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const seed = Math.floor(frame / 2);
  const dots = new Array(90).fill(0).map((_, i) => ({
    x: random(`gx${seed}-${i}`) * 1920,
    y: random(`gy${seed}-${i}`) * 1080,
    o: 0.04 + random(`go${seed}-${i}`) * 0.06,
  }));
  return (
    <svg width={1920} height={1080} style={{ position: "absolute" }}>
      {dots.map((d, i) => (
        <rect key={i} x={d.x} y={d.y} width={2} height={2} fill="#fff" opacity={d.o} />
      ))}
    </svg>
  );
};

/** Número que conta com expo-out, formatado em espanhol. */
export const Count: React.FC<{
  to: number;
  from?: number;
  start: number;
  len?: number;
  style?: React.CSSProperties;
  fmt?: (n: number) => string;
}> = ({ to, from = 0, start, len = 45, style, fmt = fmtEs }) => {
  const frame = useCurrentFrame();
  const v = from + (to - from) * prog(frame, start, start + len);
  return <span style={{ fontVariantNumeric: "tabular-nums", ...style }}>{fmt(v)}</span>;
};

/** Rótulo pequeno em caixa alta com barra de acento que cresce. */
export const Kicker: React.FC<{ text: string; delay: number; color?: string }> = ({ text, delay, color = colors.accent }) => {
  const frame = useCurrentFrame();
  const w = prog(frame, delay, delay + 24) * 70;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 18, ...enter(frame, delay, 20) }}>
      <div style={{ width: w, height: 5, background: color }} />
      <div style={{ fontFamily: "inherit", letterSpacing: 6, fontSize: 26, color, textTransform: "uppercase" }}>{text}</div>
    </div>
  );
};

/** Converte um tempo absoluto do áudio (s) em quadro local da cena. */
export const localFrame = (sec: number, t0: number) => Math.round(sec * 30) - t0;
