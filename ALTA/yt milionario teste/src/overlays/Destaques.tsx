// DESTAQUES sobrepostos à imagem (21/09/2026, pedido do usuário): motion graphic que NÃO toma a tela inteira.
// A animação de tela cheia continua existindo para o que precisa de explicação; o destaque entra por cima do
// vídeo/foto quando a narração cita um lugar, uma data, um nome, um número ou um fato curto.
//
// ESTILO por filme (data/pipeline_config.json -> "estilo_destaque"):
//   "documentario" (padrão) — versalete branco, fio fino, sem caixa; entra em fade + 12 px. Sóbrio, tipo HISTORY.
//   "dinamico"              — barra de cor entrando da esquerda com a palavra em caixa alta; mais rápido e pop.
//   "tecnico"               — moldura fina com cantos, rótulo entre colchetes; cara de relatório/engenharia.
//
// Todos respeitam a área segura (6 % da largura, 10 % da altura) e somem antes do corte terminar.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { colors, displayFont, textFont } from "../design/tokens";
import config from "../../data/pipeline_config.json";

export type Estilo = "documentario" | "dinamico" | "tecnico";
export const ESTILO: Estilo = ((config as { estilo_destaque?: Estilo }).estilo_destaque || "documentario");
// contexto só para a PRÉVIA (src/overlays/DemoDestaques.tsx) mostrar os três estilos no mesmo bundle;
// no filme ninguém provê o contexto e vale o estilo do pipeline_config.
export const EstiloCtx = React.createContext<Estilo | null>(null);
const useEstilo = (): Estilo => React.useContext(EstiloCtx) || ESTILO;

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const BRANCO = "#F4F1EA";
const SOMBRA = "0 2px 0 rgba(0,0,0,0.55), 0 2px 14px rgba(0,0,0,0.45)";
const MX = Math.round(1920 * 0.06);
const MY = Math.round(1080 * 0.10);

/** posições possíveis do destaque (o build_overlays alterna para não repetir o mesmo canto) */
export type Canto = "baixo-esq" | "baixo-dir" | "alto-esq" | "alto-dir" | "centro-esq";

const lugar = (canto: Canto): React.CSSProperties => {
  switch (canto) {
    case "baixo-dir": return { right: MX, bottom: MY, textAlign: "right" };
    case "alto-esq": return { left: MX, top: MY };
    case "alto-dir": return { right: MX, top: MY, textAlign: "right" };
    case "centro-esq": return { left: MX, top: 430 };
    default: return { left: MX, bottom: MY };
  }
};

/** entra (fade + deslocamento), fica, sai (fade) — em quadros */
const vida = (frame: number, entra: number, fica: number, dx = 0, dy = 12) => {
  const o = Math.min(interpolate(frame, [entra, entra + 10], [0, 1], clamp),
                     interpolate(frame, [entra + fica - 10, entra + fica], [1, 0], clamp));
  const t = interpolate(frame, [entra, entra + 12], [1, 0], clamp);
  return { opacity: o, transform: `translate(${dx * t}px, ${dy * t}px)` };
};

/** DESTAQUE: o cartão principal — rótulo pequeno em cima, palavra/ número grande embaixo. */
export const Destaque: React.FC<{
  titulo: string; sub?: string; canto?: Canto; entra?: number; fica?: number; cor?: string;
}> = ({ titulo, sub, canto = "baixo-esq", entra = 8, fica = 110, cor }) => {
  const frame = useCurrentFrame();
  const acento = cor || colors.accent;
  const dir = canto.endsWith("dir");
  const est = useEstilo();
  if (est === "dinamico") {
    const v = vida(frame, entra, fica, dir ? 40 : -40, 0);
    const w = interpolate(frame, [entra, entra + 14], [0, 1], clamp);
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        <div style={{ position: "absolute", ...lugar(canto), ...v }}>
          {sub ? <div style={{ fontFamily: textFont, fontWeight: 700, fontSize: 26, letterSpacing: "0.12em",
                               textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA, marginBottom: 10 }}>{sub}</div> : null}
          <div style={{ display: "inline-block", background: acento, padding: "10px 26px 12px",
                        transform: `scaleX(${w})`, transformOrigin: dir ? "right center" : "left center" }}>
            <span style={{ fontFamily: displayFont, fontWeight: 700, fontSize: 72, lineHeight: 1,
                           color: "#0B0F16", opacity: w > 0.9 ? 1 : 0 }}>{titulo}</span>
          </div>
        </div>
      </AbsoluteFill>
    );
  }
  if (est === "tecnico") {
    const v = vida(frame, entra, fica, 0, 10);
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        <div style={{ position: "absolute", ...lugar(canto), ...v, border: `2px solid ${acento}`, padding: "14px 22px",
                      background: "rgba(8,12,18,0.55)" }}>
          {sub ? <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 24, letterSpacing: "0.14em",
                               textTransform: "uppercase", color: acento }}>[ {sub} ]</div> : null}
          <div style={{ fontFamily: displayFont, fontWeight: 700, fontSize: 60, lineHeight: 1.05, color: BRANCO,
                        marginTop: sub ? 6 : 0 }}>{titulo}</div>
        </div>
      </AbsoluteFill>
    );
  }
  // documentário (padrão): fio + versalete, sem caixa
  const v = vida(frame, entra, fica);
  const fio = interpolate(frame, [entra + 4, entra + 20], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", ...lugar(canto), ...v }}>
        <div style={{ height: 3, width: 96 * fio, background: acento, marginBottom: 14,
                      marginLeft: dir ? "auto" : 0 }} />
        {sub ? <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 26, letterSpacing: "0.10em",
                             textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA, opacity: 0.92 }}>{sub}</div> : null}
        <div style={{ fontFamily: displayFont, fontWeight: 500, fontSize: 62, lineHeight: 1.05, color: BRANCO,
                      textShadow: SOMBRA, marginTop: 4, letterSpacing: 1 }}>{titulo}</div>
      </div>
    </AbsoluteFill>
  );
};

/** ETIQUETA: marcador pequeno de canto (lugar/trecho), para orientar sem roubar a cena. */
export const Etiqueta: React.FC<{ texto: string; canto?: Canto; entra?: number; fica?: number; cor?: string }> = ({
  texto, canto = "alto-dir", entra = 8, fica = 120, cor,
}) => {
  const frame = useCurrentFrame();
  const acento = cor || colors.cool;
  const v = vida(frame, entra, fica, 0, 8);
  const dir = canto.endsWith("dir");
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", ...lugar(canto), ...v, display: "flex", alignItems: "center",
                    flexDirection: dir ? "row-reverse" : "row", gap: 12 }}>
        <div style={{ width: 4, height: 30, background: acento }} />
        <div style={{ fontFamily: textFont, fontWeight: 700, fontSize: 28, letterSpacing: "0.12em",
                      textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA }}>{texto}</div>
      </div>
    </AbsoluteFill>
  );
};

/** NÚMERO: um dado solto por cima da imagem (sem parar o filme numa animação inteira). */
export const NumeroSobreposto: React.FC<{
  valor: string; rotulo?: string; canto?: Canto; entra?: number; fica?: number; cor?: string;
}> = ({ valor, rotulo, canto = "baixo-dir", entra = 8, fica = 110, cor }) => {
  const frame = useCurrentFrame();
  const acento = cor || colors.accent;
  const v = vida(frame, entra, fica, 0, 14);
  const dir = canto.endsWith("dir");
  const escala = interpolate(frame, [entra, entra + 12], [0.88, 1], clamp);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", ...lugar(canto), ...v }}>
        <div style={{ fontFamily: displayFont, fontWeight: 700, fontSize: 116, lineHeight: 1, color: acento,
                      textShadow: SOMBRA, transform: `scale(${escala})`, transformOrigin: dir ? "right bottom" : "left bottom" }}>
          {valor}
        </div>
        {rotulo ? <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 28, letterSpacing: "0.10em",
                                textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA, marginTop: 8 }}>{rotulo}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

/** FAIXA: uma frase curta na base, para um fato que não merece animação inteira. */
export const Faixa: React.FC<{ texto: string; entra?: number; fica?: number; cor?: string }> = ({
  texto, entra = 8, fica = 130, cor,
}) => {
  const frame = useCurrentFrame();
  const acento = cor || colors.accent;
  const v = vida(frame, entra, fica, 0, 10);
  const w = interpolate(frame, [entra, entra + 16], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: MX, right: MX, bottom: MY, ...v }}>
        <div style={{ height: 3, background: acento, transform: `scaleX(${w})`, transformOrigin: "left center", marginBottom: 14 }} />
        <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 36, lineHeight: 1.3, color: BRANCO,
                      textShadow: SOMBRA, maxWidth: 1300 }}>{texto}</div>
      </div>
    </AbsoluteFill>
  );
};

/** COMPARATIVO: duas barras pequenas por cima da imagem (versão de canto das barras de tela cheia). */
export const Comparativo: React.FC<{
  titulo?: string; a: { rotulo: string; valor: string; v: number }; b: { rotulo: string; valor: string; v: number };
  canto?: Canto; entra?: number; fica?: number;
}> = ({ titulo, a, b, canto = "baixo-esq", entra = 8, fica = 140 }) => {
  const frame = useCurrentFrame();
  const v = vida(frame, entra, fica, 0, 12);
  const max = Math.max(a.v, b.v) || 1;
  const cr = (i: number) => (i ? colors.danger : colors.cool);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", ...lugar(canto), ...v, width: 620 }}>
        {titulo ? <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 24, letterSpacing: "0.12em",
                                textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA, marginBottom: 12 }}>{titulo}</div> : null}
        {[a, b].map((x, i) => {
          const w = interpolate(frame, [entra + 6 + i * 8, entra + 28 + i * 8], [0, x.v / max], clamp);
          return (
            <div key={i} style={{ marginTop: i ? 16 : 0 }}>
              <div style={{ fontFamily: textFont, fontWeight: 500, fontSize: 22, letterSpacing: "0.08em",
                            textTransform: "uppercase", color: BRANCO, opacity: 0.85, textShadow: SOMBRA }}>{x.rotulo}</div>
              <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 6 }}>
                <div style={{ height: 22, width: 420 * w, background: cr(i) }} />
                <div style={{ fontFamily: displayFont, fontWeight: 700, fontSize: 34, color: cr(i), textShadow: SOMBRA }}>{x.valor}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
