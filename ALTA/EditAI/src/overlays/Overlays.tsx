// Motion graphics SOBREPOSTOS: o gráfico entra POR CIMA do vídeo, sem trocar a imagem por uma cartela.
// Quatro tipos, os que resolvem problema real de documentário: selo de dado, contador, apontamento e rótulo
// de lugar. Todos entram e saem sozinhos dentro da própria sequência e todos respeitam a regra: número que
// aparece é número dito na narração.
import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EASE_OUT_EXPO, colors, depth, motion, springs, type } from "../design/tokens";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** opacidade 0 -> 1 na entrada e 1 -> 0 nos últimos quadros */
const vida = (frame: number, dur: number, entra: number, sai = 16) =>
  Math.min(
    interpolate(frame, [entra, entra + 12], [0, 1], clamp),
    interpolate(frame, [dur - sai, dur], [1, 0], clamp),
  );

/** 1. SELO DE DADO — cartão no canto com rótulo pequeno e número grande. */
export const SeloDado: React.FC<{
  rotulo: string;
  valor: string;
  nota?: string;
  entra?: number;
  dur: number;
  lado?: "esquerda" | "direita";
}> = ({ rotulo, valor, nota, entra = 18, dur, lado = "esquerda" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - entra, fps, config: springs.snappy });
  const x = interpolate(s, [0, 1], [lado === "esquerda" ? -60 : 60, 0]);
  return (
    <AbsoluteFill style={{ opacity: vida(frame, dur, entra) }}>
      <div
        style={{
          position: "absolute",
          [lado === "esquerda" ? "left" : "right"]: 96,
          bottom: 110,
          translate: `${x}px 0`,
          padding: "26px 34px 30px",
          background: "rgba(7,11,18,0.82)",
          borderLeft: `6px solid ${colors.accent}`,
          borderRadius: depth.radiusSm,
          boxShadow: depth.shadowSoft,
          backdropFilter: "blur(2px)",
        }}
      >
        <div style={{ ...type.bodyMedium, fontSize: 24, letterSpacing: 2.5, color: colors.textDim, textTransform: "uppercase" }}>
          {rotulo}
        </div>
        <div style={{ ...type.display, fontSize: 104, lineHeight: 1.02, color: colors.accent, marginTop: 6 }}>{valor}</div>
        {nota ? (
          <div style={{ ...type.bodyMedium, fontSize: 26, color: colors.text, marginTop: 8, maxWidth: 620 }}>{nota}</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/** 2. CONTADOR — o número sobe até o valor dito, com uma régua que enche junto. */
export const Contador: React.FC<{
  rotulo: string;
  ate: number;
  sufixo?: string;
  casas?: number;
  entra?: number;
  subida?: number;
  dur: number;
}> = ({ rotulo, ate, sufixo = "", casas = 0, entra = 14, subida = 46, dur }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [entra, entra + subida], [0, 1], { ...clamp, easing: EASE_OUT_EXPO });
  const v = (ate * t).toFixed(casas).replace(".", ",");
  return (
    <AbsoluteFill style={{ opacity: vida(frame, dur, entra) }}>
      <div
        style={{
          position: "absolute", right: 104, top: 96, textAlign: "right",
          padding: "20px 28px 24px", background: "rgba(7,11,18,0.72)", borderRadius: depth.radiusSm,
          boxShadow: depth.shadowSoft,
        }}
      >
        <div style={{ ...type.bodyMedium, fontSize: 24, letterSpacing: 2.5, color: colors.text, textTransform: "uppercase" }}>
          {rotulo}
        </div>
        <div style={{ ...type.display, fontSize: 150, lineHeight: 1, color: colors.text, textShadow: depth.shadowHard }}>
          {v}
          <span style={{ color: colors.accent }}>{sufixo}</span>
        </div>
        <div style={{ width: 380, height: 8, background: "rgba(238,242,246,0.18)", borderRadius: 4, marginTop: 10, marginLeft: "auto" }}>
          <div style={{ width: `${t * 100}%`, height: "100%", background: colors.accent, borderRadius: 4 }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** 3. APONTAMENTO — círculo que se desenha em volta da coisa, linha guia e etiqueta. */
export const Apontamento: React.FC<{
  x: number;
  y: number;
  raio?: number;
  texto: string;
  ladoTexto?: "esquerda" | "direita";
  entra?: number;
  dur: number;
  /** o mesmo zoom do corte (motion.videoDrift): o círculo cresce junto e não escorrega da coisa */
  deriva?: number;
}> = ({ x: x0, y: y0, raio: raio0 = 150, texto, ladoTexto = "direita", entra = 20, dur, deriva = motion.videoDrift }) => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [0, dur], [1, 1 + deriva], clamp);
  const x = 960 + (x0 - 960) * z;
  const y = 540 + (y0 - 540) * z;
  const raio = raio0 * z;
  const perim = 2 * Math.PI * raio;
  const desenho = interpolate(frame, [entra, entra + 26], [0, 1], { ...clamp, easing: EASE_OUT_EXPO });
  const linha = interpolate(frame, [entra + 18, entra + 34], [0, 1], clamp);
  const dir = ladoTexto === "direita" ? 1 : -1;
  const xFim = x + dir * (raio + 190);
  const yFim = y - 120;
  return (
    <AbsoluteFill style={{ opacity: vida(frame, dur, entra) }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle
          cx={x}
          cy={y}
          r={raio}
          fill="none"
          stroke={colors.accent}
          strokeWidth={6}
          strokeDasharray={perim}
          strokeDashoffset={perim * (1 - desenho)}
          transform={`rotate(-90 ${x} ${y})`}
          opacity={0.95}
        />
        <line
          x1={x + dir * raio * 0.72}
          y1={y - raio * 0.72}
          x2={x + dir * raio * 0.72 + (xFim - (x + dir * raio * 0.72)) * linha}
          y2={y - raio * 0.72 + (yFim - (y - raio * 0.72)) * linha}
          stroke={colors.accent}
          strokeWidth={5}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          left: ladoTexto === "direita" ? xFim : undefined,
          right: ladoTexto === "esquerda" ? 1920 - xFim : undefined,
          top: yFim - 46,
          padding: "12px 22px",
          background: colors.accent,
          borderRadius: depth.radiusSm,
          ...type.display,
          fontSize: 40,
          color: "#0B0A06",
          letterSpacing: 0.5,
          opacity: linha,
          whiteSpace: "nowrap",
        }}
      >
        {texto}
      </div>
    </AbsoluteFill>
  );
};

/** 4. RÓTULO DE LUGAR — faixa inferior dizendo ONDE é (o espectador não adivinha). */
export const RotuloLugar: React.FC<{ lugar: string; detalhe?: string; entra?: number; dur: number }> = ({
  lugar,
  detalhe,
  entra = 12,
  dur,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - entra, fps, config: springs.snappy });
  const largura = interpolate(s, [0, 1], [0, 1]);
  return (
    <AbsoluteFill style={{ opacity: vida(frame, dur, entra) }}>
      <div style={{ position: "absolute", left: 96, bottom: 120, display: "flex", alignItems: "stretch" }}>
        <div style={{ width: 8, background: colors.cool, transform: `scaleY(${largura})`, transformOrigin: "bottom" }} />
        <div
          style={{
            overflow: "hidden",
            background: "rgba(7,11,18,0.8)",
            padding: "18px 30px 20px",
            transform: `scaleX(${largura})`,
            transformOrigin: "left",
            boxShadow: depth.shadowSoft,
          }}
        >
          <div style={{ ...type.display, fontSize: 62, color: colors.text, lineHeight: 1.05 }}>{lugar}</div>
          {detalhe ? (
            <div style={{ ...type.bodyMedium, fontSize: 28, color: colors.cool, letterSpacing: 1.5, marginTop: 4 }}>
              {detalhe}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};
