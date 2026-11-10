// CINCO CARTÕES DE ECONOMIA / CRISE / AGRO (04/10/2026) — dívida bancária, crédito rural, falências, preços, fatia de mercado.
//   CupomFiscal     — cupom térmico saindo da impressora no topo do quadro, linha a linha, TOTAL marcado a marca-texto.
//   RankingBarras   — barras horizontais em papel claro (editorial de revista de economia), item em destaque na cor de acento.
//   Rosca           — rosca grande enchendo até `pct`, número contando no meio, fundo bordô de pôster.
//   PilhaDinheiro   — maços de cédulas genéricas caindo e formando pilhas crescentes, valor contando no topo.
//   ContratoCarimbo — contrato sobre a mesa, assinatura se desenhando e carimbo batendo com tinta e tremor.
// Mesma regra dos outros cartões: todo texto vem das props; todo número escrito tem de ser DITO na narração.
import React from "react";
import { AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame } from "remotion";
import { sansFont, type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, FilmeVelho, SERIFA, Traco, clamp } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const SANS = `'${sansFont}', 'Segoe UI', sans-serif`;
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });
const lim = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));

/** Número no formato brasileiro: 1.234.567,8 */
const fmtBR = (n: number, dec: number, sep = ".", vir = ",") => {
  const s = Math.abs(n).toFixed(dec);
  const [i, d] = s.split(".");
  return (n < 0 ? "−" : "") + i.replace(/\B(?=(\d{3})+(?!\d))/g, sep) + (d ? vir + d : "");
};
const casas = (n: number) => {
  const s = String(n);
  const k = s.indexOf(".");
  return k < 0 ? 0 : Math.min(2, s.length - k - 1);
};
/** Separa "4,7 bilhões" em prefixo / número / sufixo para contar só o número. */
const partirValor = (v: string) => {
  const m = v.match(/^([^\d]*)(\d[\d.]*(?:,\d+)?)(.*)$/);
  if (!m) return null;
  const txt = m[2];
  // 10/10/2026: decimal em inglês ("2.37 million", "7.5 million") — ponto com 1-2 casas no fim = decimal, não milhar
  if (/^\d+\.\d{1,2}$/.test(txt)) {
    const dec = txt.length - txt.indexOf(".") - 1;
    return { pre: m[1], num: parseFloat(txt), dec, suf: m[3], en: true };
  }
  const dec = txt.indexOf(",") >= 0 ? txt.length - txt.indexOf(",") - 1 : 0;
  const num = parseFloat(txt.replace(/\./g, "").replace(",", "."));
  return isFinite(num) ? { pre: m[1], num, dec, suf: m[3] } : null;
};

// ================================================================================================ CUPOM FISCAL
export type LinhaCupom = { rotulo: string; valor: string };
export type CupomFiscalProps = SceneProps & { titulo: string; linhas: LinhaCupom[]; total: string; rodape?: string; rotuloTotal?: string };
/** Cupom térmico desenrolando da impressora no topo do quadro; itens com pontilhado, TOTAL em negrito e marca-texto. */
export const CupomFiscal: React.FC<CupomFiscalProps> = (p) => {
  const f = useCurrentFrame();
  const PW = 900, PX = (1920 - PW) / 2, PY = 66, PAD = 56, CW = PW - 2 * PAD, ZIG = 22;
  const n = Math.max(1, p.linhas.length);
  const maior = Math.max(10, ...p.linhas.map((l) => l.rotulo.length + l.valor.length + 3));
  const fs = lim(Math.floor(CW / (maior * 0.6)), 34, 38);
  const tfs = 42;
  const tLinhas = Math.max(1, Math.ceil(p.titulo.length / Math.floor(CW / (tfs * 0.6))));
  const totFs = lim(Math.floor(CW / ((p.total.length + 7) * 0.6)), 44, 62);
  // altura: o papel inteiro tem de caber acima de 1080 - 50
  const fixo = 40 + tLinhas * 52 + 34 + 40 + totFs * 1.5 + (p.rodape ? 34 + 50 : 0) + 40;
  const rowH = Math.min(fs * 1.62, (1080 - 50 - PY - ZIG - fixo) / n);
  let y = 40;
  const yTit = y; y += tLinhas * 52 + 10;
  const ySep1 = y; y += 24;
  const yLin = p.linhas.map((_, i) => y + i * rowH); y += n * rowH + 6;
  const ySep2 = y; y += 34;
  const yTot = y; y += totFs * 1.5;
  const ySep3 = y; y += p.rodape ? 30 : 0;
  const yRod = y; y += p.rodape ? 50 : 0;
  const H = y + 40;
  const E = Math.round(Math.min(46, p.dur * 0.32));
  // impressora avança aos trancos (térmica): avanço linear com micro-paradas
  const lin = interpolate(f, [5, E], [0, 1], clamp);
  const tranco = lin < 1 ? Math.sin(lin * Math.PI * 2 * (n + 3)) * 0.004 : 0;
  const L = H * lim(lin + tranco, 0, 1);
  const zig = Array.from({ length: 31 }, (_, i) => `${((30 - i) / 30) * PW}px ${L + (i % 2 ? ZIG : 0)}px`).join(", ");
  const marca = ent(f, E + 4, E + 18);
  const sway = Math.sin(f / 22) * 0.25;
  const push = interpolate(f, [0, p.dur], [1, 1.035], clamp);
  const tinta = "#232327";
  const pont = "3px dotted rgba(35,35,39,0.5)";
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, #34302c 0%, #171513 55%, #090807 100%)", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: "50% 0%" }}>
        {/* luz de cima */}
        <AbsoluteFill style={{ background: "radial-gradient(ellipse 38% 70% at 50% 0%, rgba(255,236,205,0.16), transparent 70%)" }} />
        {/* papel */}
        <div style={{ position: "absolute", left: PX, top: PY, width: PW, height: H + ZIG,
          filter: "drop-shadow(0 26px 30px rgba(0,0,0,0.55))", transform: `rotate(${sway}deg)`, transformOrigin: "50% 0%" }}>
          <div style={{ position: "absolute", inset: 0, clipPath: `polygon(0px 0px, ${PW}px 0px, ${zig})`,
            background: "linear-gradient(90deg, #e2e0da 0%, #f8f7f3 9%, #fdfcf9 50%, #f6f5f0 91%, #dfddd6 100%)",
            fontFamily: MONO, color: tinta }}>
            <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 70,
              background: "linear-gradient(rgba(0,0,0,0.28), transparent)" }} />
            <div style={{ position: "absolute", left: PAD, width: CW, top: yTit, textAlign: "center", fontSize: tfs, fontWeight: 700,
              lineHeight: "52px", letterSpacing: 1, textTransform: "uppercase" }}>{p.titulo}</div>
            <div style={{ position: "absolute", left: PAD, width: CW, top: ySep1, borderTop: "3px dashed rgba(35,35,39,0.55)" }} />
            {p.linhas.map((l, i) => (
              <div key={i} style={{ position: "absolute", left: PAD, width: CW, top: yLin[i], height: rowH, display: "flex",
                alignItems: "center", fontSize: fs }}>
                <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", flexShrink: 1 }}>{l.rotulo}</span>
                <span style={{ flex: 1, minWidth: 30, borderBottom: pont, margin: "0 12px", transform: "translateY(10px)" }} />
                <span style={{ whiteSpace: "nowrap", fontWeight: 700 }}>{l.valor}</span>
              </div>
            ))}
            <div style={{ position: "absolute", left: PAD, width: CW, top: ySep2, height: 9, borderTop: `3px solid ${tinta}`,
              borderBottom: `3px solid ${tinta}` }} />
            <div style={{ position: "absolute", left: PAD - 14, width: CW + 28, top: yTot - 4, height: totFs * 1.32,
              background: "rgba(255,206,40,0.72)", mixBlendMode: "multiply", transform: `scaleX(${marca}) skewX(-6deg)`,
              transformOrigin: "0% 50%", borderRadius: 6 }} />
            <div style={{ position: "absolute", left: PAD, width: CW, top: yTot, display: "flex", justifyContent: "space-between",
              alignItems: "baseline", fontSize: totFs, fontWeight: 700, lineHeight: 1.2 }}>
              <span>{p.rotuloTotal ?? "TOTAL"}</span><span style={{ whiteSpace: "nowrap" }}>{p.total}</span>
            </div>
            {p.rodape ? <>
              <div style={{ position: "absolute", left: PAD, width: CW, top: ySep3, borderTop: "3px dashed rgba(35,35,39,0.55)" }} />
              <div style={{ position: "absolute", left: PAD, width: CW, top: yRod, textAlign: "center", fontSize: 34, letterSpacing: 2,
                whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{p.rodape}</div>
            </> : null}
          </div>
        </div>
        {/* boca da impressora */}
        <div style={{ position: "absolute", left: PX - 80, width: PW + 160, top: -30, height: 104, borderRadius: "0 0 22px 22px",
          background: "linear-gradient(180deg, #4a4a4e 0%, #2a2a2d 55%, #161618 100%)",
          boxShadow: "0 18px 34px rgba(0,0,0,0.6), inset 0 -2px 0 rgba(255,255,255,0.12)" }}>
          <div style={{ position: "absolute", left: 60, right: 60, bottom: 10, height: 8, borderRadius: 4, background: "#050506",
            boxShadow: "0 1px 0 rgba(255,255,255,0.15)" }} />
          <div style={{ position: "absolute", right: 34, top: 50, width: 12, height: 12, borderRadius: 6,
            background: f < E ? (f % 8 < 5 ? "#5dff8a" : "#1d5a2f") : "#5dff8a", boxShadow: "0 0 10px #5dff8a" }} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ================================================================================================ RANKING EM BARRAS
export type ItemRanking = { rotulo: string; valor: number; destaque?: boolean };
export type RankingBarrasProps = SceneProps & { titulo: string; itens: ItemRanking[]; unidade: string; fonte?: string; sep?: string; virgula?: string };
/** Ranking editorial em papel claro: barras crescendo uma a uma (maior em cima), item em destaque em vermelho. */
export const RankingBarras: React.FC<RankingBarrasProps> = (p) => {
  const f = useCurrentFrame();
  const itens = p.itens.map((it, i) => ({ ...it, i })).sort((a, b) => b.valor - a.valor || a.i - b.i);
  const n = Math.max(1, itens.length);
  const max = Math.max(1e-9, ...itens.map((it) => it.valor));
  const dec = Math.max(0, ...itens.map((it) => casas(it.valor)));
  const ACENTO = "#c62f26", TINTA = "#1b1a17";
  const XR = 96, XL = 156, XB = 780, BMAX = 1830 - XB - 200;
  const TOPO = 322, FUNDO = p.fonte ? 930 : 990;
  const rowH = Math.min(102, (FUNDO - TOPO) / n);
  const barH = Math.min(56, rowH * 0.6);
  const passo = Math.min(4, 26 / n);
  const fim = 12 + (n - 1) * passo + 20;
  const apaga = ent(f, fim, fim + 14);
  const temDestaque = itens.some((it) => it.destaque);
  const tfs = p.titulo.length > 46 ? 54 : 66;
  return (
    <AbsoluteFill style={{ background: "#f3efe6", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.55), transparent 60%)" }} />
      <div style={{ position: "absolute", left: XR, top: 88, width: 92, height: 12, background: ACENTO, transform: `scaleX(${ent(f, 0)})`,
        transformOrigin: "0% 50%" }} />
      <div style={{ position: "absolute", left: XR, right: 90, top: 116, fontFamily: SERIFA, fontWeight: 700, fontSize: tfs, color: TINTA,
        lineHeight: 1.08, opacity: ent(f, 2), transform: `translateY(${(1 - ent(f, 2)) * 18}px)` }}>{p.titulo}</div>
      <div style={{ position: "absolute", left: XR, top: 116 + tfs * 1.08 + 18, fontFamily: SANS, fontSize: 36, color: "#6d675c",
        opacity: ent(f, 6) }}>{p.unidade}</div>
      <div style={{ position: "absolute", left: XR, right: 90, top: TOPO - 26, height: 2, background: TINTA,
        transform: `scaleX(${ent(f, 4, 24)})`, transformOrigin: "0% 50%" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {[0.25, 0.5, 0.75, 1].map((k) => <line key={k} x1={XB + k * BMAX} x2={XB + k * BMAX} y1={TOPO} y2={TOPO + n * rowH}
          stroke="#d6d0c3" strokeWidth={1.5} strokeDasharray="4 6" opacity={ent(f, 8)} />)}
      </svg>
      {itens.map((it, k) => {
        const t0 = 12 + k * passo;
        const g = ent(f, t0, t0 + 20);
        const w = g > 0.001 ? Math.max(4, (it.valor / max) * BMAX * g) : 0;
        const cy = TOPO + k * rowH + rowH / 2;
        const dest = !!it.destaque;
        const cor = dest ? ACENTO : temDestaque
          ? `rgb(${Math.round(110 + 68 * apaga)},${Math.round(140 + 52 * apaga)},${Math.round(163 + 42 * apaga)})` : "#6e8ca3";
        return (
          <React.Fragment key={k}>
            <div style={{ position: "absolute", left: XR, top: cy - 26, lineHeight: "52px", fontFamily: SANS, fontSize: 34, color: "#9b9488",
              opacity: ent(f, t0 - 4) }}>{k + 1}</div>
            <div style={{ position: "absolute", left: XL, width: XB - XL - 30, top: cy - 26, fontFamily: SANS, fontSize: 38,
              fontWeight: dest ? 700 : 500, color: dest ? TINTA : "#3a3731", whiteSpace: "nowrap", overflow: "hidden",
              textOverflow: "ellipsis", lineHeight: "52px", opacity: ent(f, t0 - 4) }}>{it.rotulo}</div>
            <div style={{ position: "absolute", left: XB, top: cy - barH / 2, width: w, height: barH, background: cor,
              boxShadow: dest ? `0 6px 18px ${ACENTO}55` : "none" }} />
            <div style={{ position: "absolute", left: XB + w + 18, top: cy - 26, lineHeight: "52px", fontFamily: SANS, fontSize: 38,
              fontWeight: 700, color: dest ? ACENTO : "#3a3731", whiteSpace: "nowrap", opacity: ent(f, t0 + 2),
              fontVariantNumeric: "tabular-nums" }}>{fmtBR(it.valor * g, dec, p.sep, p.virgula)}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: XB - 2, top: TOPO - 8, width: 3, height: n * rowH + 16, background: TINTA,
        opacity: ent(f, 8) }} />
      {p.fonte ? <div style={{ position: "absolute", left: XR, bottom: 90, fontFamily: SANS, fontSize: 34, color: "#7a7468",
        opacity: ent(f, 20) }}>{p.fonte}</div> : null}
    </AbsoluteFill>
  );
};

// ================================================================================================ ROSCA (PERCENTUAL)
export type RoscaProps = SceneProps & { titulo: string; pct: number; rotulo: string; sub?: string; cor?: string };
/** Pôster bordô: rosca enorme enchendo até `pct` com o número contando no meio; título, rótulo e subtexto à direita. */
export const Rosca: React.FC<RoscaProps> = (p) => {
  const f = useCurrentFrame();
  const cor = p.cor ?? "#f0b54a";
  const CREME = "#f6ead8";
  const CX = 600, CY = 545, R = 318, ESP = 72;
  const pct = lim(p.pct, 0, 100);
  const g = interpolate(f, [8, 46], [0, 1], { ...clamp, easing: Easing.bezier(0.33, 0, 0.15, 1) });
  const v = pct * g;
  const ang = ((-90 + 3.6 * v) * Math.PI) / 180;
  const fimEnche = 46;
  const pulso = f >= fimEnche ? interpolate(f, [fimEnche, fimEnche + 22], [0, 1], clamp) : -1;
  const dec = casas(pct);
  const NT = 120;
  const rfs = p.rotulo.length > 70 ? 52 : p.rotulo.length > 40 ? 60 : 68;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 30% 50%, #45161a 0%, #240b0d 50%, #0f0506 100%)", ...exit(f, p.dur) }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <filter id="roscaBrilho" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation={14} /></filter>
          <linearGradient id="roscaArco" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor={cor} /><stop offset="1" stopColor={cor} stopOpacity={0.78} />
          </linearGradient>
        </defs>
        {[1.55, 1.95, 2.4].map((k, i) => <circle key={i} cx={CX} cy={CY} r={R * k} fill="none" stroke={CREME}
          strokeOpacity={0.04} strokeWidth={2} />)}
        {Array.from({ length: NT }, (_, i) => {
          const a = ((i / NT) * 360 - 90) * (Math.PI / 180);
          const maj = i % 10 === 0;
          const r1 = R + ESP / 2 + 22, r2 = r1 + (maj ? 30 : 16);
          const aceso = i / NT < v / 100;
          return <line key={i} x1={CX + r1 * Math.cos(a)} y1={CY + r1 * Math.sin(a)} x2={CX + r2 * Math.cos(a)} y2={CY + r2 * Math.sin(a)}
            stroke={aceso ? cor : CREME} strokeOpacity={(aceso ? 0.95 : 0.18) * ent(f, 2, 20)} strokeWidth={maj ? 4 : 2.5} />;
        })}
        <circle cx={CX} cy={CY} r={R} fill="none" stroke={CREME} strokeOpacity={0.08 * ent(f, 0, 12) + 0.02} strokeWidth={ESP} />
        <circle cx={CX} cy={CY} r={R - ESP / 2 - 16} fill="none" stroke={CREME} strokeOpacity={0.12} strokeWidth={2} />
        {v > 0.4 ? <>
          <circle cx={CX} cy={CY} r={R} fill="none" stroke={cor} strokeWidth={ESP} pathLength={100} strokeDasharray={`${v} 100`}
            transform={`rotate(-90 ${CX} ${CY})`} filter="url(#roscaBrilho)" opacity={0.55} />
          <circle cx={CX} cy={CY} r={R} fill="none" stroke="url(#roscaArco)" strokeWidth={ESP} pathLength={100}
            strokeDasharray={`${v} 100`} transform={`rotate(-90 ${CX} ${CY})`} />
          <line x1={CX + (R - ESP / 2) * Math.cos(ang)} y1={CY + (R - ESP / 2) * Math.sin(ang)} x2={CX + (R + ESP / 2 + 56) * Math.cos(ang)}
            y2={CY + (R + ESP / 2 + 56) * Math.sin(ang)} stroke="#fff8ec" strokeWidth={5} strokeLinecap="round" />
        </> : null}
        {pulso >= 0 ? <circle cx={CX} cy={CY} r={R + pulso * 120} fill="none" stroke={cor} strokeOpacity={(1 - pulso) * 0.6}
          strokeWidth={ESP * (1 - pulso) * 0.6 + 1} /> : null}
      </svg>
      <div style={{ position: "absolute", left: CX - 260, width: 520, top: CY - 110, height: 220, display: "flex",
        alignItems: "center", justifyContent: "center", color: CREME, opacity: ent(f, 4) }}>
        <span style={{ ...type.display, fontSize: 190, lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{fmtBR(v, dec)}</span>
        <span style={{ ...type.displayMedium, fontSize: 92, lineHeight: 1, marginLeft: 6, color: cor, alignSelf: "flex-start",
          marginTop: 28 }}>%</span>
      </div>
      <div style={{ position: "absolute", left: 1090, right: 96, top: 140, bottom: 140, display: "flex", flexDirection: "column",
        justifyContent: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, opacity: ent(f, 4) }}>
          <div style={{ width: 80 * ent(f, 4, 22), height: 6, background: cor }} />
          <div style={{ ...type.displayMedium, fontSize: 40, letterSpacing: 6, color: cor, textTransform: "uppercase" }}>{p.titulo}</div>
        </div>
        <div style={{ fontFamily: SERIFA, fontSize: rfs, lineHeight: 1.16, color: CREME, marginTop: 30, opacity: ent(f, 10, 28),
          transform: `translateY(${(1 - ent(f, 10, 28)) * 24}px)`, textWrap: "balance" } as React.CSSProperties}>{p.rotulo}</div>
        {p.sub ? <div style={{ fontFamily: SANS, fontSize: 36, lineHeight: 1.38, color: "rgba(246,234,216,0.7)", marginTop: 34,
          paddingTop: 28, borderTop: "2px solid rgba(246,234,216,0.18)", opacity: ent(f, 18, 34), textWrap: "pretty" } as React.CSSProperties}>{p.sub}</div> : null}
      </div>
      <FilmeVelho feixe={false} forca={0.3} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PILHA DE DINHEIRO
export type PilhaDinheiroProps = SceneProps & { valor: string; moeda: string; rotulo: string; sub?: string; pilhas?: number };
type Maco = { x: number; y0: number; w: number; dx: number; dy: number; t: number; D: number; moeda: string };
/** Face de cima do maço: cédula genérica (guilhoché, medalhão com o símbolo da moeda) + cinta de papel kraft. */
const Cedula: React.FC<Maco> = ({ x, y0, w, dx, dy, D, moeda }) => (
  <g transform={`matrix(1,0,${-dx / D},${dy / D},${x + dx},${y0 - dy})`}>
    <rect x={0} y={0} width={w} height={D} fill="#a8bfae" />
    <rect x={7} y={7} width={w - 14} height={D - 14} fill="none" stroke="#56725f" strokeWidth={2} />
    {Array.from({ length: 6 }, (_, i) => (
      <path key={i} d={`M12,${18 + i * ((D - 36) / 5)} ${Array.from({ length: 12 }, (_, k) =>
        `Q${12 + (k + 0.5) * ((w - 24) / 12)},${18 + i * ((D - 36) / 5) + (k % 2 ? 7 : -7)} ${12 + (k + 1) * ((w - 24) / 12)},${18 + i * ((D - 36) / 5)}`).join(" ")}`}
        fill="none" stroke="#7c9a85" strokeWidth={1.3} opacity={0.75} />
    ))}
    <circle cx={w * 0.22} cy={D / 2} r={D * 0.3} fill="#cddccf" stroke="#56725f" strokeWidth={2} />
    <circle cx={w * 0.22} cy={D / 2} r={D * 0.24} fill="none" stroke="#7c9a85" strokeWidth={1.2} strokeDasharray="3 3" />
    <text x={w * 0.22} y={D / 2 + D * 0.11} textAnchor="middle" fill="#3f5a48" style={{ ...type.display, fontSize: D * 0.3 }}>{moeda}</text>
    <text x={w - 18} y={D * 0.3} textAnchor="end" fill="#3f5a48" style={{ ...type.display, fontSize: D * 0.2 }}>{moeda}</text>
    <rect x={w * 0.62} y={D * 0.5} width={w * 0.28} height={D * 0.26} fill="#94ae9b" />
    <rect x={w * 0.43} y={0} width={w * 0.14} height={D} fill="#c9a160" />
    <line x1={w * 0.445} x2={w * 0.445} y1={0} y2={D} stroke="#8a6630" strokeWidth={1.5} />
    <line x1={w * 0.555} x2={w * 0.555} y1={0} y2={D} stroke="#8a6630" strokeWidth={1.5} />
  </g>
);
const MacoSvg: React.FC<Maco> = (m) => {
  const { x, y0, w, dx, dy, t } = m;
  return (
    <g>
      <rect x={x} y={y0} width={w} height={t} fill="url(#pdBorda)" />
      <rect x={x} y={y0} width={w} height={t} fill="url(#pdSombraFrente)" />
      <rect x={x + w * 0.43} y={y0} width={w * 0.14} height={t} fill="#b58b4b" />
      <polygon points={`${x + w},${y0} ${x + w + dx},${y0 - dy} ${x + w + dx},${y0 - dy + t} ${x + w},${y0 + t}`} fill="url(#pdLado)" />
      <Cedula {...m} />
    </g>
  );
};
/** Maços de cédulas genéricas caem e empilham em colunas crescentes; o valor conta no topo. */
export const PilhaDinheiro: React.FC<PilhaDinheiroProps> = (p) => {
  const f = useCurrentFrame();
  const n = Math.round(lim(p.pilhas ?? 5, 1, 7));
  const gap = 34, dx = 64, dy = 44, t = 34;
  const w = Math.min(270, (1920 - 280 - (n - 1) * gap) / n - dx);
  const D = w * 0.46;
  const largura = n * (w + dx) + (n - 1) * gap;
  const X0 = (1920 - largura) / 2;
  const BASE = 972, M = 11;
  const queda = 5;
  const pilhas = Array.from({ length: n }, (_, i) => {
    const fr = n === 1 ? 1 : 0.36 + 0.64 * (i / (n - 1));
    const k = Math.max(1, Math.round(M * fr));
    const s0 = 8 + i * 3;
    return { x: X0 + i * (w + dx + gap), k, s0 };
  });
  const passo = 2.1;
  const ultimo = Math.max(...pilhas.map((s) => s.s0 + (s.k - 1) * passo + queda));
  const cont = interpolate(f, [8, ultimo], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const pv = partirValor(p.valor);
  const push = interpolate(f, [0, p.dur], [1, 1.04], clamp);
  return (
    <AbsoluteFill style={{ background: "#0d0b09", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: "50% 80%" }}>
        {/* parede e mesa */}
        <AbsoluteFill style={{ background: "linear-gradient(180deg, #1a1612 0%, #121010 58%, #2b221a 58.2%, #1d1712 100%)" }} />
        <AbsoluteFill style={{ background: "repeating-linear-gradient(178deg, rgba(0,0,0,0.0) 0 9px, rgba(0,0,0,0.13) 9px 11px)",
          clipPath: "inset(58.2% 0 0 0)" }} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse 60% 75% at 50% 18%, rgba(255,226,170,0.22), transparent 70%)" }} />
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <defs>
            <pattern id="pdBorda" width={10} height={4} patternUnits="userSpaceOnUse">
              <rect width={10} height={4} fill="#e3e6d6" /><rect y={3} width={10} height={1} fill="#9ba892" />
            </pattern>
            <pattern id="pdLado" width={10} height={4} patternUnits="userSpaceOnUse">
              <rect width={10} height={4} fill="#9ea891" /><rect y={3} width={10} height={1} fill="#6d7863" />
            </pattern>
            <linearGradient id="pdSombraFrente" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#000" stopOpacity={0.18} /><stop offset="0.5" stopColor="#000" stopOpacity={0} />
              <stop offset="1" stopColor="#000" stopOpacity={0.12} />
            </linearGradient>
            <filter id="pdSombra" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation={16} /></filter>
          </defs>
          {pilhas.map((s, i) => (
            <ellipse key={`s${i}`} cx={s.x + (w + dx) / 2} cy={BASE - dy / 2 + 8} rx={(w + dx) * 0.62} ry={dy * 0.9} fill="#000"
              opacity={0.55 * ent(f, s.s0, s.s0 + 10)} filter="url(#pdSombra)" />
          ))}
          {pilhas.map((s, i) => (
            <g key={i}>
              {Array.from({ length: s.k }, (_, j) => {
                const land = s.s0 + j * passo + queda;
                if (f < land - queda) return null;
                const e = interpolate(f, [land - queda, land], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
                const jit = (random(`pj${i}-${j}`) - 0.5) * 8;
                const y0 = BASE - (j + 1) * t - (1 - e) * 70;
                return <g key={j} opacity={lim(e * 3, 0, 1)}>
                  <MacoSvg x={s.x + jit} y0={y0} w={w} dx={dx} dy={dy} t={t} D={D} moeda={p.moeda} />
                </g>;
              })}
            </g>
          ))}
        </svg>
        {/* valor */}
        <div style={{ position: "absolute", left: 90, right: 90, top: 78, textAlign: "center", color: "#f4ead6", opacity: ent(f, 2),
          transform: `translateY(${(1 - ent(f, 2)) * -20}px)` }}>
          <div style={{ display: "inline-flex", alignItems: "baseline", gap: 22, whiteSpace: "nowrap" }}>
            <span style={{ ...type.displayMedium, fontSize: 78, color: "#e9b85c" }}>{p.moeda}</span>
            <span style={{ ...type.display, fontSize: 158, lineHeight: 1, fontVariantNumeric: "tabular-nums",
              textShadow: "0 10px 30px rgba(0,0,0,0.6)" }}>
              {pv ? `${pv.pre}${(pv as { en?: boolean }).en ? (pv.num * cont).toFixed(pv.dec) : fmtBR(pv.num * cont, pv.dec)}` : p.valor}</span>
            {pv && pv.suf.trim() ? <span style={{ ...type.displayMedium, fontSize: 78 }}>{pv.suf.trim()}</span> : null}
          </div>
          <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 46, lineHeight: 1.2, marginTop: 14, opacity: ent(f, 10) }}>{p.rotulo}</div>
          {p.sub ? <div style={{ fontFamily: MONO, fontSize: 36, color: "rgba(233,184,92,0.9)", marginTop: 12, opacity: ent(f, 18) }}>{p.sub}</div> : null}
        </div>
      </AbsoluteFill>
      <FilmeVelho feixe={false} forca={0.35} />
    </AbsoluteFill>
  );
};

// ================================================================================================ CONTRATO + CARIMBO
export type ContratoCarimboProps = SceneProps & { titulo: string; partes: string[]; valor: string; carimbo: string; data: string;
  clausula?: string };
/** Contrato sobre a mesa: cláusulas e partes, assinatura se desenhando, carimbo batendo com tinta falhada e tremor. */
export const ContratoCarimbo: React.FC<ContratoCarimboProps> = (p) => {
  const f = useCurrentFrame();
  const DW = 1360, DH = 900, DX = (1920 - DW) / 2, DY = 92;
  const g = spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 80 } });
  const S = Math.round(Math.min(46, p.dur * 0.3));
  const desce = interpolate(f, [S - 7, S], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const pos = f - S;
  const amp = pos >= 0 ? 16 * Math.exp(-pos / 3.2) : 0;
  const sx = (random(`cx${f}`) - 0.5) * amp, sy = (random(`cy${f}`) - 0.5) * amp;
  const ass = interpolate(f, [16, 40], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const cfs = lim(Math.floor(940 / (p.carimbo.length * 0.52)), 84, 136);
  const push = interpolate(f, [0, p.dur], [1, 1.045], clamp);
  const negrito = (s: string) => {
    const k = s.indexOf(":");
    return k > 0 ? <><b>{s.slice(0, k + 1)}</b>{s.slice(k + 1)}</> : <>{s}</>;
  };
  const respingos = Array.from({ length: 6 }, (_, i) => ({
    x: (random(`rx${i}`) - 0.5) * 1000, y: (random(`ry${i}`) - 0.5) * 300, r: 1.5 + random(`rr${i}`) * 3 }));
  return (
    <AbsoluteFill style={{ background: "#1e140d", overflow: "hidden", ...exit(f, p.dur) }}>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id="ccTinta" x="-5%" y="-10%" width="110%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves={2} seed={7} result="dist" />
          <feDisplacementMap in="SourceGraphic" in2="dist" scale={8} xChannelSelector="R" yChannelSelector="G" result="borrado" />
          <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves={3} seed={3} result="grao" />
          <feColorMatrix in="grao" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.6 2.05" result="mascara" />
          <feComposite in="borrado" in2="mascara" operator="in" />
        </filter>
      </svg>
      <AbsoluteFill style={{ transform: `scale(${push}) translate(${sx}px, ${sy}px)` }}>
        {/* mesa de madeira */}
        <AbsoluteFill style={{ background:
          "repeating-linear-gradient(91deg, rgba(0,0,0,0.16) 0 3px, transparent 3px 13px, rgba(255,190,130,0.05) 13px 15px, transparent 15px 31px)," +
          "linear-gradient(180deg, #3b2616, #2a1a0f)" }} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 38% 28%, rgba(255,214,160,0.28), transparent 62%)" }} />
        {/* documento */}
        <div style={{ position: "absolute", left: DX, top: DY, width: DW, height: DH, background: "#f1ead9",
          boxShadow: "0 40px 70px rgba(0,0,0,0.6), inset 0 0 90px rgba(130,95,50,0.22)",
          transform: `translateY(${(1 - g) * 760}px) rotate(${-1.1 - (1 - g) * 5}deg)`, color: "#2a241d", fontFamily: MONO,
          boxSizing: "border-box", padding: "54px 80px" }}>
          <svg width={DW} height={DH} style={{ position: "absolute", left: 0, top: 0, opacity: 0.09, mixBlendMode: "multiply" }}>
            <filter id="ccPapel"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves={2} seed={11} /></filter>
            <rect width="100%" height="100%" filter="url(#ccPapel)" />
          </svg>
          <div style={{ position: "absolute", right: 110, bottom: 170, width: 230, height: 230, borderRadius: "50%", transform: "scaleY(0.93) rotate(20deg)",
            background: "radial-gradient(circle, transparent 60%, rgba(140,90,40,0.15) 63%, rgba(140,90,40,0.05) 67%, transparent 70%)" }} />
          <div style={{ fontFamily: SERIFA, fontWeight: 700, fontSize: 50, letterSpacing: 6, textAlign: "center",
            textTransform: "uppercase", opacity: ent(f, 6) }}>{p.titulo}</div>
          <div style={{ marginTop: 18, height: 7, borderTop: "3px solid #2a241d", borderBottom: "1.5px solid #2a241d",
            transform: `scaleX(${ent(f, 6, 22)})` }} />
          <div style={{ marginTop: 30 }}>
            {p.partes.map((s, i) => <div key={i} style={{ fontSize: 36, lineHeight: 1.45, opacity: ent(f, 9 + i * 3),
              whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{negrito(s)}</div>)}
          </div>
          <div style={{ marginTop: 30, textAlign: "center", opacity: ent(f, 14) }}>
            <span style={{ display: "inline-block", border: "3px solid #2a241d", padding: "10px 36px", fontSize: 64, fontWeight: 700,
              letterSpacing: 1, background: "rgba(255,255,255,0.35)" }}>{p.valor}</span>
          </div>
          {p.clausula ? <div style={{ marginTop: 30, fontSize: 34, lineHeight: 1.36, color: "#3b342b",
            opacity: ent(f, 18), display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
            {p.clausula}</div> : null}
          <div style={{ position: "absolute", left: 80, right: 80, bottom: 56, display: "flex", justifyContent: "space-between",
            alignItems: "flex-end" }}>
            <div style={{ fontSize: 34, opacity: ent(f, 20) }}>{p.data}</div>
            <div style={{ position: "relative", width: 520, height: 120 }}>
              <svg width={520} height={120} style={{ position: "absolute", left: 0, top: -6 }}>
                <Traco d="M24,88 C30,40 52,14 66,28 C80,44 52,92 44,96 C60,70 84,46 98,58 C108,68 96,90 112,86 C130,80 140,52 156,56 C170,60 160,88 176,84 C196,78 204,34 222,24 C238,16 238,60 228,88 C244,62 262,54 274,62 C286,72 276,88 294,84 C316,78 330,58 352,60 C370,62 364,84 384,80 C410,74 430,52 470,44"
                  p={ass * 1.25} cor="#1d2b64" w={4.5} />
                <Traco d="M120,104 C220,92 340,96 496,84" p={(ass - 0.8) * 5} cor="#1d2b64" w={4} />
              </svg>
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 3, background: "#2a241d",
                transform: `scaleX(${ent(f, 12, 26)})`, transformOrigin: "0% 50%" }} />
            </div>
          </div>
          {/* sombra do carimbo descendo */}
          {f < S ? <div style={{ position: "absolute", left: DW / 2 - 560, top: 500, width: 1120, height: 290, background: "#000",
            borderRadius: 24, filter: "blur(40px)", opacity: desce * 0.35, transform: `rotate(-9deg) scale(${1.35 - 0.35 * desce})` }} /> : null}
          {/* carimbo */}
          <div style={{ position: "absolute", left: 0, right: 0, top: 500, display: "flex", justifyContent: "center",
            opacity: f >= S - 2 ? 1 : 0, transform: `rotate(-9deg) scale(${f < S ? 1.6 - 0.6 * desce : 1})` }}>
            <div style={{ filter: "url(#ccTinta)", mixBlendMode: "multiply", color: "#b3202a", border: "12px solid #b3202a",
              padding: 8, borderRadius: 10 }}>
              <div style={{ border: "4px solid #b3202a", borderRadius: 4, padding: "6px 46px", ...type.display, fontSize: cfs,
                lineHeight: 1.08, letterSpacing: 8, whiteSpace: "nowrap", textTransform: "uppercase" }}>{p.carimbo}</div>
            </div>
          </div>
          {pos >= 0 ? <svg width={DW} height={DH} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply" }}>
            {respingos.map((r, i) => <circle key={i} cx={DW / 2 + r.x} cy={620 + r.y} r={r.r} fill="#b3202a"
              opacity={0.45 * interpolate(pos, [0, 3], [0, 1], clamp)} />)}
          </svg> : null}
        </div>
      </AbsoluteFill>
      <FilmeVelho feixe={false} forca={0.4} />
    </AbsoluteFill>
  );
};
