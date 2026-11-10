import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { EASE_IN_OUT, motion } from "../design/tokens";
import { GRADE, Lado } from "../design/grade";
import config from "../../data/pipeline_config.json";

// 21/09/2026: grade.ts fica com ativo:true depois de um filme ULTRA e NÃO é regerado no modo padrão. Resultado:
// o Remotion aplicava contraste/saturação/tinte/vinheta nas FOTOS enquanto o ffmpeg (que só grade no modo ultra)
// deixava os VÍDEOS crus — dois visuais no mesmo filme. Agora os dois lados olham para o mesmo interruptor.
const GRADE_ON = GRADE.ativo && (config as { modo?: string }).modo === "ultra";

export type Cut = {
  kind: "video" | "photo";
  src: string; // relativo a public/
  from: number; // quadro de início dentro do segmento pai (absoluto no filme)
  dur: number;
  trimBefore?: number; // quadros pulados no arquivo de vídeo
  move?: "in" | "out" | "left" | "right";
  lado?: Lado; // lado do grade (modo ULTRA): quente = base do tema, frio = clímax
};


/** Grade de cor do tema (modo ULTRA, PROMPT_v_ULTRA §5) — aproximação em CSS do eq+colorbalance+vignette do ffmpeg:
 *  contraste/saturação por filter; sombras tingidas por `lighten` (levanta o preto na cor das sombras);
 *  realces tingidos por `multiply` (tira do branco a cor oposta); vinheta radial. */
const cor = (v: readonly number[], base: number) =>
  `rgb(${v.map((x) => Math.round(Math.min(255, Math.max(0, base + x * 255)))).join(",")})`;
export const Grade: React.FC<{ lado?: Lado }> = ({ lado = "quente" }) => {
  if (!GRADE_ON) return null;
  const sombras = cor(GRADE.sombras[lado], 0);       // ex.: rgb(0,10,26) — preto azulado
  const realces = cor(GRADE.realces[lado], 255);     // ex.: rgb(255,255,240) — branco levemente quente
  return (
    <>
      <AbsoluteFill style={{ background: sombras, mixBlendMode: "lighten", pointerEvents: "none" }} />
      <AbsoluteFill style={{ background: realces, mixBlendMode: "multiply", pointerEvents: "none" }} />
      {/* vinheta = cos(PI/4.5 · r)^4 do ffmpeg (r = 1 no canto): 0,94 · 0,78 · 0,56 · 0,34 em r = ¼ ½ ¾ 1 */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse farthest-corner at center, rgba(0,0,0,0) 0%, rgba(0,0,0,0.04) 25%, rgba(0,0,0,0.16) 50%, rgba(0,0,0,0.36) 75%, rgba(0,0,0,0.58) 100%)", pointerEvents: "none" }} />
    </>
  );
};
const GRADE_FILTER = GRADE_ON ? `contrast(${GRADE.contraste}) saturate(${GRADE.saturacao})` : undefined;

/** Vídeo em tela cheia, sempre mudo, com Ken Burns sutil. */
export const VideoCut: React.FC<{ cut: Cut }> = ({ cut }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, cut.dur], [1, 1 + motion.videoDrift], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <OffthreadVideo
        src={staticFile(cut.src)}
        muted
        trimBefore={cut.trimBefore ?? 0}
        style={{ width: "100%", height: "100%", objectFit: "cover", scale, filter: GRADE_FILTER }}
      />
      <Grade lado={cut.lado} />
    </AbsoluteFill>
  );
};

/** Foto em tela cheia, sempre em movimento (push-in / pull-out / pan). */
export const PhotoCut: React.FC<{ cut: Cut }> = ({ cut }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, cut.dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE_IN_OUT,
  });
  const p = motion.photoPush;
  const move = cut.move ?? "in";
  const scale = move === "out" ? 1 + p - p * t : move === "in" ? 1 + p * t : 1 + p;
  const pan = move === "left" ? (t - 0.5) * -p * 100 * 0.8 : move === "right" ? (t - 0.5) * p * 100 * 0.8 : 0;
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#000" }}>
      <Img
        src={staticFile(cut.src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          scale,
          translate: `${pan}% 0`,
          filter: GRADE_FILTER,
        }}
      />
      <Grade lado={cut.lado} />
    </AbsoluteFill>
  );
};

/** Fade de entrada curto sobre o corte anterior (o anterior continua montado por baixo). */
export const FadeIn: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const frame = useCurrentFrame();
  const opacity = frames <= 0 ? 1 : interpolate(frame, [0, frames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};
