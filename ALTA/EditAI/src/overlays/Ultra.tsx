// Texto na tela do MODO ULTRA (PROMPT_v_ULTRA, seção 4): versalete branco #F4F1EA, sombra 0/2 px preta a 60 %,
// sem caixa, sem faixa. Oswald 500 na linha principal, IBM Plex Sans 500 em caixa alta com +0,08 em na secundária.
// Canto inferior esquerdo, margem 6 % da largura e 12 % da altura. Entrada: fade + 12 px em 10 quadros; saída: fade em 8.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { displayFont, textFont } from "../design/tokens";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const BRANCO = "#F4F1EA";
const SOMBRA = "0 2px 0 rgba(0,0,0,0.6), 0 2px 12px rgba(0,0,0,0.45)";
const X = 1920 * 0.06;
const Y = 1080 * 0.12;

const principal = { fontFamily: displayFont, fontWeight: 500 as const, color: BRANCO, textShadow: SOMBRA, letterSpacing: 1 };
const secundaria = { fontFamily: textFont, fontWeight: 500 as const, color: BRANCO, textShadow: SOMBRA,
                     letterSpacing: "0.08em", textTransform: "uppercase" as const };

/** fade + deslizamento de 12 px na entrada, fade na saída; `fica` = quadros em tela */
const vida = (frame: number, entra: number, fica: number) => {
  const o = Math.min(interpolate(frame, [entra, entra + 10], [0, 1], clamp),
                     interpolate(frame, [entra + fica - 8, entra + fica], [1, 0], clamp));
  const y = interpolate(frame, [entra, entra + 10], [12, 0], clamp);
  return { opacity: o, transform: `translateY(${y}px)` };
};

/** a) SLATE lugar/data — 2 linhas, entra 1 s depois do corte, fica 4 s */
export const Slate: React.FC<{ linha1: string; linha2: string; entra?: number; fica?: number }> = ({
  linha1, linha2, entra = 30, fica = 120,
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: X, bottom: Y, ...vida(frame, entra, fica) }}>
        <div style={{ ...secundaria, fontSize: 26, opacity: 0.92 }}>{linha1}</div>
        <div style={{ ...principal, fontSize: 44, marginTop: 4 }}>{linha2}</div>
      </div>
    </AbsoluteFill>
  );
};

/** b) CARTELA DE CAPÍTULO — 2–4 palavras, 2,5 s, sobre a imagem escurecida 35 % */
export const CartelaCapitulo: React.FC<{ nome: string; lugar?: string; entra?: number; fica?: number }> = ({ nome, lugar, entra = 6, fica = 100 }) => {
  // 26/09/2026 (regra do usuário): todo capítulo abre com CARIMBO de lugar/data batido à máquina ("KURSK — JULHO DE 1943")
  const frame = useCurrentFrame();
  const v = vida(frame, entra, fica);
  const letras = lugar ? Math.floor(Math.max(0, Math.min(lugar.length, (frame - entra - 8) / 1.4))) : 0;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: "rgba(0,0,0,0.45)", opacity: v.opacity }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 420, textAlign: "center", ...v }}>
        <div style={{ ...principal, fontSize: 86, letterSpacing: 6 }}>{nome}</div>
        <div style={{ width: 120, height: 3, background: BRANCO, margin: "18px auto 0", opacity: 0.8 }} />
        {lugar ? <div style={{ display: "inline-block", marginTop: 26, background: "rgba(239,231,214,0.92)", color: "#1A1714",
          fontFamily: "Courier Prime", fontWeight: 700, fontSize: 34, letterSpacing: 5, padding: "10px 24px",
          textTransform: "uppercase", minWidth: 40 }}>{lugar.slice(0, letras)}{letras < lugar.length && frame % 14 < 7 ? "▌" : ""}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

/** c) CARTÃO DE CITAÇÃO — frase curta entre aspas; fundo = imagem escurecida 55 % + vinheta */
export const QuoteCard: React.FC<{ frase: string; autor: string; entra?: number; fica: number }> = ({
  frase, autor, entra = 4, fica,
}) => {
  const frame = useCurrentFrame();
  const v = vida(frame, entra, fica);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0.45) 30%, rgba(0,0,0,0.75) 100%)", opacity: v.opacity }} />
      <div style={{ position: "absolute", left: 200, right: 200, top: 400, textAlign: "center", ...v }}>
        <div style={{ ...principal, fontSize: 44, lineHeight: 1.35 }}>“{frase}”</div>
        <div style={{ ...secundaria, fontSize: 24, marginTop: 22, opacity: 0.9 }}>— {autor}</div>
      </div>
    </AbsoluteFill>
  );
};

/** d) LOWER THIRD de espécie/lugar na primeira menção — 3,5 s, mesma tipografia */
export const LowerThird: React.FC<{ nome: string; detalhe?: string; entra?: number; fica?: number }> = ({
  nome, detalhe, entra = 12, fica = 105,
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: X, bottom: Y, ...vida(frame, entra, fica) }}>
        <div style={{ ...principal, fontSize: 46 }}>{nome}</div>
        {detalhe ? <div style={{ ...secundaria, fontSize: 22, marginTop: 4, opacity: 0.85 }}>{detalhe}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
