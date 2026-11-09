// CINCO CARTÕES DO TEMA MILITAR / NAVAL / GUERRA (04/10/2026) — arquivos da 2ª Guerra, porta-aviões, submarinos, resgates.
//   DossieSecreto      — pasta parda abre, carimbo de classificação, linhas datilografadas e tarjas pretas que saem ([[...]])
//   Sonar              — console de sonar âmbar: tela PPI circular com pings, contatos com rumo/distância, cascata e profundímetro
//   ComparaForcas      — ordem de batalha: lados em colunas, ícones de unidade entrando um a um e números contando
//   Periscopio         — a foto vista pelo periscópio (ou binóculo): retículo graduado, fita de rumo, telêmetro e água
//   PlacaIdentificacao — placa(s) de identificação de metal na corrente, girando em 3D, linhas gravadas e legenda
// Mesmas regras de estilos5.tsx: tomam o quadro inteiro, todo texto vem das props e todo número escrito tem de ser DITO.
import React from "react";
import { AbsoluteFill, Img, interpolate, random, spring, useCurrentFrame } from "remotion";
import { fmtEs, type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, FilmeVelho, SERIFA, clamp, src } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });
const p3 = (g: number) => ("00" + String(Math.round(((g % 360) + 360) % 360))).slice(-3);

// ================================================================================================ DOSSIÊ SECRETO
export type DossieProps = SceneProps & {
  titulo: string;
  linhas: string[];          // trechos entre [[...]] nascem sob tarja preta e são revelados
  classificacao: string;     // "ULTRASSECRETO", "TOP SECRET", "CONFIDENCIAL"
  data: string;
  origem?: string;
};
type Parte = { t: string; oculto: boolean };
const partes = (s: string): Parte[] => {
  const out: Parte[] = [];
  const re = /\[\[(.+?)\]\]/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push({ t: s.slice(last, m.index), oculto: false });
    out.push({ t: m[1], oculto: true });
    last = m.index + m[0].length;
  }
  if (last < s.length) out.push({ t: s.slice(last), oculto: false });
  return out;
};

/** Pasta parda que se abre sobre a mesa: folha datilografada com carimbo, tarjas pretas que deslizam e revelam
 *  as palavras-chave, rodapé de classificação e clipe de papel. */
export const DossieSecreto: React.FC<DossieProps> = (p) => {
  const f = useCurrentFrame();
  const VERM = "#9b1c17";
  const TINTA = "#231d14";
  const g = spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 90 } });
  const abre = ent(f, 5, 24);
  const folha = ent(f, 12, 30);
  const selo = spring({ frame: f - 20, fps: 30, config: { damping: 10, stiffness: 190 } });
  const linhas = p.linhas.map(partes);
  const maxLen = Math.max(1, ...linhas.map((l) => l.reduce((s, x) => s + x.t.length, 0)));
  const fs = Math.round(Math.max(34, Math.min(42, 1270 / (maxLen * 0.6))));
  const passo = 6;
  const revBase = Math.max(44, Math.round(p.dur * 0.26));
  const revPasso = Math.max(6, Math.round(p.dur * 0.05));
  let k = 0;
  const FX = 170, FY = 100, FW = 1580, FH = 900;
  const SX = 250, SY = 140, SW = 1420, SH = 830;
  const cam = interpolate(f, [0, p.dur], [1, 1.035], clamp);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 45% 35%, #3b2b1d 0%, #1a120b 60%, #0b0806 100%)", overflow: "hidden",
      ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.35, backgroundImage:
        "repeating-linear-gradient(92deg, rgba(0,0,0,0.25) 0 2px, transparent 2px 18px, rgba(255,220,170,0.05) 18px 20px, transparent 20px 41px)" }} />
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        <div style={{ position: "absolute", inset: 0, transform: `translateY(${(1 - g) * 140}px) rotate(${-1.2 + (1 - g) * 3}deg)` }}>
          {/* fundo da pasta + aba */}
          <div style={{ position: "absolute", left: FX + 60, top: FY - 40, width: 400, height: 70, borderRadius: "16px 16px 0 0",
            background: "linear-gradient(180deg, #d4ae72, #c49d62)" }} />
          <div style={{ position: "absolute", left: FX, top: FY, width: FW, height: FH, borderRadius: 8,
            background: "linear-gradient(170deg, #d7b276 0%, #c59f63 55%, #b38d55 100%)", boxShadow: "0 40px 90px rgba(0,0,0,0.75)" }} />
          {/* folha */}
          <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, background: "#efe6cf",
            boxShadow: "0 10px 26px rgba(0,0,0,0.35)", transform: `translateY(${(1 - folha) * 50}px)`, color: TINTA,
            backgroundImage: "radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.35), transparent 60%), radial-gradient(ellipse at 85% 90%, rgba(120,90,40,0.18), transparent 55%)" }}>
            {/* carimbo de cabeçalho */}
            <div style={{ position: "absolute", left: 0, right: 0, top: 46, display: "flex", justifyContent: "center" }}>
              <div style={{ ...type.display, fontSize: 70, letterSpacing: 12, color: VERM, border: `7px solid ${VERM}`, padding: "2px 36px",
                textTransform: "uppercase", opacity: f >= 20 ? 0.86 : 0, mixBlendMode: "multiply",
                transform: `rotate(-3deg) scale(${interpolate(selo, [0, 1], [2.1, 1])})` }}>{p.classificacao}</div>
            </div>
            {/* origem / data */}
            <div style={{ position: "absolute", left: 70, right: 70, top: 190, display: "flex", justifyContent: "space-between",
              fontFamily: MONO, fontSize: 34, fontWeight: 700, letterSpacing: 2, borderBottom: "2px solid rgba(60,48,30,0.55)",
              paddingBottom: 12, opacity: ent(f, 14) }}>
              <span>{p.origem ?? ""}</span><span>{p.data}</span>
            </div>
            {/* título */}
            <div style={{ position: "absolute", left: 70, right: 70, top: 262, ...type.display, fontSize: 60, letterSpacing: 2,
              textTransform: "uppercase", lineHeight: 1.05, clipPath: `inset(0 ${100 - ent(f, 12, 30) * 100}% 0 0)` }}>{p.titulo}</div>
            {/* linhas datilografadas */}
            <div style={{ position: "absolute", left: 70, right: 70, top: 384, fontFamily: MONO, fontSize: fs, lineHeight: 1.72 }}>
              {linhas.map((ps, i) => {
                const t0 = 16 + i * passo;
                const total = ps.reduce((s, x) => s + x.t.length, 0);
                const n = interpolate(f, [t0, t0 + 14], [0, total], clamp);
                let off = 0;
                const digitando = n > 0 && n < total;
                return (
                  <div key={i} style={{ minHeight: fs * 1.72 }}>
                    {ps.map((x, j) => {
                      const ini = off;
                      off += x.t.length;
                      if (!x.oculto) return <span key={j}>{x.t.slice(0, Math.max(0, Math.floor(n - ini)))}</span>;
                      const idx = k++;
                      if (n <= ini) return null;
                      const at = revBase + idx * revPasso;
                      const rev = interpolate(f, [at, at + 12], [0, 1], { ...clamp, easing: EXPO });
                      return (
                        <span key={j} style={{ position: "relative", display: "inline-block", whiteSpace: "pre" }}>
                          <span style={{ fontWeight: 700, color: rev > 0.4 ? VERM : TINTA,
                            boxShadow: `inset 0 -${Math.round(rev * 10)}px 0 rgba(155,28,23,0.14)` }}>{x.t}</span>
                          <span style={{ position: "absolute", left: -5, right: -5, top: fs * 0.18, bottom: fs * 0.12, background: "#121010",
                            clipPath: `inset(0 0 0 ${rev * 100}%)`, transform: `translateX(${rev * 24}px)` }} />
                        </span>
                      );
                    })}
                    {digitando ? <span style={{ opacity: f % 6 < 3 ? 1 : 0 }}>▌</span> : null}
                  </div>
                );
              })}
            </div>
            {/* rodapé de classificação */}
            <div style={{ position: "absolute", left: 70, right: 70, bottom: 40, display: "flex", alignItems: "center", gap: 28,
              opacity: ent(f, 26) }}>
              <div style={{ flex: 1, height: 3, background: VERM, opacity: 0.7 }} />
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: 8, color: VERM, textTransform: "uppercase" }}>
                {p.classificacao}</div>
              <div style={{ flex: 1, height: 3, background: VERM, opacity: 0.7 }} />
            </div>
          </div>
          {/* clipe de papel */}
          <svg width={90} height={230} style={{ position: "absolute", left: SX + 110, top: SY - 62, opacity: ent(f, 18),
            transform: `translateY(${(1 - folha) * 50}px)`, filter: "drop-shadow(3px 5px 3px rgba(0,0,0,0.45))" }}>
            <defs><linearGradient id="clipe" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor="#f4f6f8" /><stop offset="0.5" stopColor="#8f969c" /><stop offset="1" stopColor="#d5d9dc" /></linearGradient></defs>
            <path d="M30,200 L30,40 A22,22 0 0 1 74,40 L74,180 A14,14 0 0 1 46,180 L46,60" fill="none" stroke="url(#clipe)" strokeWidth={7}
              strokeLinecap="round" />
          </svg>
          {/* capa da pasta abrindo */}
          <div style={{ position: "absolute", left: FX, top: FY, width: FW, height: FH, borderRadius: 8, transformOrigin: "0% 50%",
            transform: `perspective(2600px) rotateY(${-abre * 105}deg)`, opacity: interpolate(abre, [0.4, 0.75], [1, 0], clamp),
            background: "linear-gradient(165deg, #dcb87d 0%, #c9a366 60%, #b8925a 100%)", boxShadow: "0 30px 70px rgba(0,0,0,0.6)",
            display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ ...type.display, fontSize: 84, letterSpacing: 14, color: VERM, border: `8px solid ${VERM}`, padding: "4px 44px",
              transform: "rotate(-4deg)", opacity: 0.8, textTransform: "uppercase" }}>{p.classificacao}</div>
          </div>
        </div>
        <AbsoluteFill style={{ mixBlendMode: "screen", background: "radial-gradient(ellipse at 38% 28%, rgba(255,214,150,0.16), transparent 60%)" }} />
      </AbsoluteFill>
      <FilmeVelho feixe={false} forca={0.45} />
    </AbsoluteFill>
  );
};

// ================================================================================================ SONAR
export type ContatoSonar = { ang: number; dist: number; rotulo: string; distancia?: string };
export type SonarProps = SceneProps & {
  titulo: string;
  contatos: ContatoSonar[];  // ang em graus (0 = proa/norte, horário); dist 0-1 do centro à borda; distancia = texto opcional ("14 km")
  profundidade?: string;     // "−180 m"
};

/** Console de sonar em fósforo âmbar: tela PPI com pings que se expandem, contatos acendendo com rumo e distância,
 *  cascata (rumo x tempo) correndo e profundímetro. */
export const Sonar: React.FC<SonarProps> = (p) => {
  const f = useCurrentFrame();
  const AMB = "#ffb547";
  const GLOW = "0 0 14px rgba(255,160,50,0.55)";
  const CX = 560, CY = 585, R = 340;
  const WX = 1060, WY = 235, WW = 600, WH = 480;
  const GX = 1730, GW = 56;
  const cs = p.contatos;
  const tC = cs.map((_, i) => 14 + i * Math.max(6, Math.round(p.dur * 0.06)));
  const P = Math.max(36, Math.round(p.dur / 4));
  const idade = ((f - 4) % P + P) % P;
  const onda = f >= 4 ? (idade / (P * 0.8)) * R : -1;
  const ondaOp = f >= 4 ? Math.max(0, 1 - idade / (P * 0.8)) : 0;
  // posições e rótulos (rótulo sempre virado para o centro, empurrado para não sobrepor)
  const pos = cs.map((c, i) => {
    const a = (c.ang * Math.PI) / 180;
    const r = Math.min(1, Math.max(0, c.dist)) * R * 0.9;
    const x = CX + r * Math.sin(a), y = CY - r * Math.cos(a);
    const l2 = `${p3(c.ang)}°${c.distancia ? `  ${c.distancia}` : ""}`;
    const w = Math.max(c.rotulo.length, l2.length) * 20.4 + 32;
    return { i, x, y, r, dir: x >= CX ? -1 : 1, ly: y - 34, l2, w };
  });
  const caixa = (q: (typeof pos)[number]) => (q.dir === 1 ? [q.x + 40, q.x + 40 + q.w] : [q.x - 40 - q.w, q.x - 40]);
  // cada rótulo procura a posição vertical mais próxima da sua que não bata em rótulo já posto nem em outro contato
  const postos: typeof pos = [];
  [...pos].sort((a, b) => a.ly - b.ly).forEach((q) => {
    const [a0, a1] = caixa(q);
    const livre = (ly: number) => ly >= CY - R + 40 && ly <= CY + R - 100
      && postos.every((o) => { const [b0, b1] = caixa(o); return !(a0 < b1 + 10 && b0 < a1 + 10 && Math.abs(ly - o.ly) < 100); })
      && pos.every((o) => o === q || o.x < a0 - 24 || o.x > a1 + 24 || o.y < ly - 32 - 24 || o.y > ly + 58 + 24);
    const base = q.ly;
    for (let d = 0; d <= 600; d += 10) {
      if (livre(base + d)) { q.ly = base + d; break; }
      if (livre(base - d)) { q.ly = base - d; break; }
    }
    postos.push(q);
  });
  // cursor do operador: gira até o contato mais novo
  let cur = cs.length ? cs[0].ang : 0;
  cs.forEach((c, i) => {
    if (!i) return;
    const dif = ((c.ang - cur + 540) % 360) - 180;
    cur += dif * ent(f, tC[i] - 8, tC[i] + 2);
  });
  const cura = (cur * Math.PI) / 180;
  const cols = 75, rows = 60, cw = WW / cols, rh = WH / rows;
  const tick = Math.floor(f / 2);
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) {
    const tau = tick - r;
    for (let c = 0; c < cols; c++) {
      let v = Math.pow(random(`sn${tau}-${c}`), 6) * 0.4;
      cs.forEach((ct, i) => {
        if (tau * 2 < tC[i]) return;
        const bc = (((ct.ang % 360) + 360) % 360) / 360 * cols + Math.sin(tau / 9 + i) * 0.6;
        v += Math.exp(-((c - bc) * (c - bc)) / 1.6) * (0.8 + 0.2 * random(`sc${tau}-${i}`));
      });
      if (v > 0.06) cells.push(<rect key={`${r}-${c}`} x={WX + c * cw} y={WY + r * rh} width={cw + 0.5} height={rh + 0.5}
        fill={AMB} opacity={Math.min(1, v)} />);
    }
  }
  const prof = 0.18 + 0.5 * ent(f, 8, 50) + Math.sin(f / 18) * 0.01;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 40% 50%, #1a1006 0%, #0a0603 55%, #040201 100%)", ...exit(f, p.dur) }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <filter id="snGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <radialGradient id="snFundo"><stop offset="0" stopColor="#ff9a2e" stopOpacity={0.1} /><stop offset="1" stopColor="#ff9a2e" stopOpacity={0.02} /></radialGradient>
        </defs>
        {/* ---------- PPI */}
        <g opacity={ent(f, 0, 12)}>
          <circle cx={CX} cy={CY} r={R} fill="url(#snFundo)" stroke={AMB} strokeOpacity={0.7} strokeWidth={2.5} />
          {[0.25, 0.5, 0.75].map((k) => <circle key={k} cx={CX} cy={CY} r={R * k} fill="none" stroke={AMB} strokeOpacity={0.22}
            strokeWidth={1.5} strokeDasharray="4 8" />)}
          {Array.from({ length: 36 }, (_, i) => {
            const a = (i * 10 * Math.PI) / 180, lg = i % 3 === 0 ? 18 : 9;
            return <line key={i} x1={CX + R * Math.sin(a)} y1={CY - R * Math.cos(a)} x2={CX + (R + lg) * Math.sin(a)}
              y2={CY - (R + lg) * Math.cos(a)} stroke={AMB} strokeOpacity={0.6} strokeWidth={2} />;
          })}
          {Array.from({ length: 12 }, (_, i) => {
            const a = (i * 30 * Math.PI) / 180;
            return <text key={i} x={CX + (R + 40) * Math.sin(a)} y={CY - (R + 40) * Math.cos(a)} textAnchor="middle" dominantBaseline="central"
              fill={AMB} fillOpacity={0.75} style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>{p3(i * 30)}</text>;
          })}
          <line x1={CX - R} x2={CX + R} y1={CY} y2={CY} stroke={AMB} strokeOpacity={0.14} />
          <line x1={CX} x2={CX} y1={CY - R} y2={CY + R} stroke={AMB} strokeOpacity={0.14} />
        </g>
        {/* ping */}
        {onda >= 0 && onda <= R ? (
          <g filter="url(#snGlow)">
            <circle cx={CX} cy={CY} r={onda} fill="none" stroke={AMB} strokeWidth={3} opacity={ondaOp * 0.9} />
            <circle cx={CX} cy={CY} r={Math.max(0, onda - 10)} fill="none" stroke={AMB} strokeWidth={14} opacity={ondaOp * 0.12} />
          </g>
        ) : null}
        {/* cursor */}
        {cs.length ? <line x1={CX} y1={CY} x2={CX + R * Math.sin(cura)} y2={CY - R * Math.cos(cura)} stroke={AMB} strokeWidth={2}
          strokeDasharray="10 8" opacity={0.55 * ent(f, tC[0] - 4)} /> : null}
        <path d={`M${CX},${CY - 14} L${CX + 10},${CY + 10} L${CX},${CY + 4} L${CX - 10},${CY + 10} Z`} fill={AMB} filter="url(#snGlow)" />
        {/* contatos */}
        {pos.map((q) => {
          const c = cs[q.i];
          const at = tC[q.i];
          const k = ent(f, at, at + 8);
          if (k <= 0) return null;
          const boost = onda >= 0 ? Math.max(0, 1 - Math.abs(onda - q.r) / 34) : 0;
          const lx = q.x + q.dir * 54;
          const bx = q.dir === 1 ? lx - 14 : lx - q.w + 14;
          const lk = ent(f, at + 4, at + 14);
          return (
            <g key={q.i}>
              <circle cx={q.x} cy={q.y} r={11 + 5 * boost} fill={AMB} opacity={k * (0.65 + 0.35 * boost)} filter="url(#snGlow)" />
              <circle cx={q.x} cy={q.y} r={22 + (1 - k) * 40} fill="none" stroke={AMB} strokeWidth={2} opacity={k * 0.6} />
              <polyline points={`${q.x + q.dir * 22},${q.y} ${lx - q.dir * 4},${q.ly + 18}`} fill="none" stroke={AMB} strokeWidth={2}
                opacity={lk * 0.8} />
              <g opacity={lk}>
                <rect x={bx} y={q.ly - 32} width={q.w} height={90} fill="rgba(10,6,2,0.82)" stroke={AMB} strokeOpacity={0.45} strokeWidth={1.5} />
                <text x={q.dir === 1 ? lx : lx} y={q.ly} textAnchor={q.dir === 1 ? "start" : "end"} fill={AMB}
                  style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, textShadow: GLOW }}>{c.rotulo}</text>
                <text x={lx} y={q.ly + 40} textAnchor={q.dir === 1 ? "start" : "end"} fill="#ffd9a0"
                  style={{ fontFamily: MONO, fontSize: 34 }}>{q.l2}</text>
              </g>
            </g>
          );
        })}
        {/* ---------- cascata */}
        <g opacity={ent(f, 4, 18)}>
          <rect x={WX} y={WY} width={WW} height={WH} fill="rgba(255,150,40,0.03)" />
          {cells}
          {[0.25, 0.5, 0.75].map((k) => <line key={k} x1={WX + WW * k} x2={WX + WW * k} y1={WY} y2={WY + WH} stroke={AMB}
            strokeOpacity={0.18} strokeDasharray="3 6" />)}
          <rect x={WX} y={WY} width={WW} height={WH} fill="none" stroke={AMB} strokeOpacity={0.6} strokeWidth={2} />
          {[0, 90, 180, 270, 360].map((d, i) => <text key={d} x={WX + (d / 360) * WW} y={WY - 18}
            textAnchor={i === 0 ? "start" : i === 4 ? "end" : "middle"} fill={AMB} fillOpacity={0.75}
            style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>{d === 360 ? "360" : p3(d)}</text>)}
          {cs.map((c, i) => f >= tC[i] ? <path key={i} d={`M${WX + ((((c.ang % 360) + 360) % 360) / 360) * WW - 9},${WY - 2} l9,12 l9,-12 Z`}
            fill={AMB} /> : null)}
        </g>
        {/* ---------- profundímetro */}
        <g opacity={ent(f, 6, 20)}>
          <rect x={GX} y={WY} width={GW} height={WH} fill="none" stroke={AMB} strokeOpacity={0.6} strokeWidth={2} />
          <rect x={GX + 6} y={WY + 6} width={GW - 12} height={Math.max(0, prof * WH - 6)} fill={AMB} opacity={0.22} />
          {Array.from({ length: 21 }, (_, i) => <line key={i} x1={GX} x2={GX + (i % 5 === 0 ? 22 : 11)} y1={WY + (i * WH) / 20}
            y2={WY + (i * WH) / 20} stroke={AMB} strokeOpacity={0.7} strokeWidth={2} />)}
          <path d={`M${GX - 6},${WY + prof * WH} l-22,-14 l0,28 Z`} fill={AMB} filter="url(#snGlow)" />
        </g>
      </svg>
      <div style={{ position: "absolute", left: 90, top: 86, right: 90, fontFamily: MONO, fontSize: 44, fontWeight: 700, color: AMB,
        letterSpacing: 4, textTransform: "uppercase", textShadow: GLOW, opacity: ent(f, 0), whiteSpace: "nowrap", overflow: "hidden",
        textOverflow: "ellipsis" }}>{p.titulo}</div>
      {p.profundidade ? (
        <div style={{ position: "absolute", left: WX, top: WY + WH + 46, display: "flex", alignItems: "center", gap: 26, opacity: ent(f, 14) }}>
          <svg width={50} height={60}><path d="M5,10 L45,10 L25,50 Z" fill="none" stroke={AMB} strokeWidth={4} strokeLinejoin="round" /></svg>
          <div style={{ ...type.display, fontSize: 104, lineHeight: 1, color: AMB, textShadow: GLOW, letterSpacing: 2 }}>{p.profundidade}</div>
        </div>
      ) : null}
      <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.32) 0 2px, transparent 2px 4px)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(0,0,0,0.8) 100%)" }} />
      <AbsoluteFill style={{ background: `rgba(255,170,60,${f % 47 < 2 ? 0.03 : 0})` }} />
    </AbsoluteFill>
  );
};

// ================================================================================================ COMPARA FORÇAS
export type IconeUnidade = "navio" | "aviao" | "tanque" | "soldado" | "submarino";
export type ItemForca = { rotulo: string; n: number; icone: IconeUnidade };
export type LadoForca = { nome: string; itens: ItemForca[]; cor?: string };
export type ComparaProps = SceneProps & { titulo: string; lados: LadoForca[] };

const GLIFO: Record<IconeUnidade, { w: number; el: React.ReactNode }> = {
  navio: { w: 100, el: <>
    <path d="M2,30 L98,30 L91,42 L9,42 Z" />
    <path d="M28,30 L28,22 L38,22 L38,13 L47,13 L47,22 L60,22 L60,30 Z" />
    <path d="M42,13 L42,3 M36,7 L48,7" strokeWidth={2} stroke="currentColor" />
    <path d="M68,30 L68,25 L78,25 L78,30 Z M78,26 L92,24 L92,26.5 L78,28 Z M12,30 L12,26 L21,26 L21,30 Z M4,27.5 L12,26.5 L12,28 L4,29 Z" />
  </> },
  submarino: { w: 100, el: <>
    <path d="M4,32 Q4,24 20,24 L80,24 Q97,25 97,32 Q97,39 80,40 L20,40 Q4,40 4,32 Z" />
    <path d="M38,24 L41,11 L57,11 L60,24 Z" />
    <path d="M50,11 L50,3 M45,11 L45,6" strokeWidth={2} stroke="currentColor" />
    <path d="M2,32 L-2,26 L-2,38 Z" />
  </> },
  aviao: { w: 90, el: <>
    <path d="M6,25 Q8,22.5 14,22.5 L74,22 Q88,23 89,25 Q88,27 74,28 L14,27.5 Q8,27.5 6,25 Z" />
    <path d="M38,23 L50,3 L58,3 L54,23 Z M38,27 L50,47 L58,47 L54,27 Z" />
    <path d="M10,23 L4,13 L11,13 L18,23 Z M10,27 L4,37 L11,37 L18,27 Z" />
  </> },
  tanque: { w: 100, el: <>
    <path d="M10,32 Q5,32 5,37.5 Q5,44 13,44 L87,44 Q95,44 95,37.5 Q95,32 90,32 Z" />
    <path d="M13,31 L18,23 L82,23 L88,31 Z" />
    <path d="M32,23 L37,13 L62,13 L67,23 Z" />
    <path d="M64,16 L98,15.5 L98,19 L64,19.5 Z" />
  </> },
  soldado: { w: 44, el: <>
    <circle cx={22} cy={12} r={5.5} />
    <path d="M12,10 Q22,-1 32,10 L34,11.5 L10,11.5 Z" />
    <path d="M15,18 L29,18 L32,33 L28,33 L28,49 L23.5,49 L22,35 L20.5,49 L16,49 L16,33 L12,33 Z" />
    <path d="M33,9 L38,47" stroke="currentColor" strokeWidth={2.5} />
  </> },
};
const Glifo: React.FC<{ tipo: IconeUnidade; h: number; cor: string }> = ({ tipo, h, cor }) => {
  const g = GLIFO[tipo] ?? GLIFO.navio;
  return (
    <svg width={(h * g.w) / 50} height={h} viewBox={`0 0 ${g.w} 50`} style={{ color: cor, overflow: "visible", display: "block" }}>
      <g fill={cor}>{g.el}</g>
    </svg>
  );
};

/** Ordem de batalha: um lado por coluna; em cada linha, ícones da unidade entram um a um (proporcionais entre os lados)
 *  e o número conta até o total. Ícone vale 1 unidade até 12; acima disso a legenda mostra quanto vale cada ícone. */
export const ComparaForcas: React.FC<ComparaProps> = (p) => {
  const f = useCurrentFrame();
  const LATAO = "#c9a45c";
  const CORES = ["#9cc3e6", "#e0694f", "#c8c27a", "#b9a3d6"];
  const n = Math.max(1, p.lados.length);
  const GAP = n > 2 ? 70 : 110;
  const colW = (1740 - GAP * (n - 1)) / n;
  const maxItens = Math.max(1, ...p.lados.map((l) => l.itens.length));
  const s = Math.min(1, 660 / maxItens / 166);
  const iconH = Math.round(44 * s), slotPad = 10;
  const numW = n > 2 ? 170 : 220;
  // valor de cada ícone por LINHA (mesmo rótulo + ícone vale o mesmo em todos os lados, para a comparação ser honesta);
  // 1 ícone = 1 unidade quando cabe; senão um valor redondo (2, 5, 10, 25, 50...)
  const chave = (it: ItemForca) => `${it.rotulo.trim().toLowerCase()}|${it.icone}`;
  const REDONDOS = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 25000, 50000, 100000];
  const unidade: Record<string, number> = {};
  const porLinha: Record<string, number> = {};
  p.lados.forEach((l) => l.itens.forEach((it) => {
    const k = chave(it);
    const w = ((GLIFO[it.icone] ?? GLIFO.navio).w * iconH) / 50 + slotPad;
    const caben = Math.max(2, Math.floor((colW - numW - 20) / w));
    porLinha[k] = caben;
    const maxN = Math.max(1, ...p.lados.flatMap((o) => o.itens.filter((x) => chave(x) === k).map((x) => x.n)));
    const bruto = maxN / (caben * 2);
    unidade[k] = REDONDOS.find((r) => r >= bruto) ?? Math.ceil(bruto);
  }));
  const rowH = 166 * s;
  const Y0 = 300;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, #1c211d 0%, #0f1210 55%, #070807 100%)", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.5, backgroundImage:
        "repeating-linear-gradient(45deg, rgba(255,255,255,0.012) 0 2px, transparent 2px 6px), repeating-linear-gradient(-45deg, rgba(0,0,0,0.12) 0 2px, transparent 2px 6px)" }} />
      <div style={{ position: "absolute", left: 90, right: 90, top: 86, display: "flex", alignItems: "center", gap: 30, opacity: ent(f, 0) }}>
        <div style={{ height: 2, flex: 1, background: `linear-gradient(90deg, transparent, ${LATAO})`, transform: `scaleX(${ent(f, 2, 20)})`,
          transformOrigin: "100% 50%" }} />
        <div style={{ ...type.display, fontSize: 56, letterSpacing: 6, color: "#efe7d4", textTransform: "uppercase", whiteSpace: "nowrap" }}>
          {p.titulo}</div>
        <div style={{ height: 2, flex: 1, background: `linear-gradient(90deg, ${LATAO}, transparent)`, transform: `scaleX(${ent(f, 2, 20)})`,
          transformOrigin: "0% 50%" }} />
      </div>
      {p.lados.map((lado, li) => {
        const cor = lado.cor ?? CORES[li % CORES.length];
        const X = 90 + li * (colW + GAP);
        return (
          <div key={li} style={{ position: "absolute", left: X, top: 190, width: colW }}>
            <div style={{ position: "absolute", left: -30, right: -30, top: -40, height: 420, opacity: 0.5 * ent(f, 4, 30),
              background: `radial-gradient(ellipse 50% 50% at 50% 50%, ${cor}2e, transparent)` }} />
            <div style={{ ...type.display, fontSize: 54, letterSpacing: 4, color: cor, textTransform: "uppercase", lineHeight: 1,
              opacity: ent(f, 4 + li * 3), transform: `translateY(${(1 - ent(f, 4 + li * 3)) * 20}px)`, whiteSpace: "nowrap" }}>{lado.nome}</div>
            <div style={{ height: 4, background: cor, marginTop: 14, transform: `scaleX(${ent(f, 6 + li * 3, 26)})`, transformOrigin: "0 50%" }} />
            {lado.itens.map((it, ri) => {
              const u = unidade[chave(it)] ?? 1;
              const qtd = it.n > 0 ? Math.max(1, Math.round(it.n / u)) : 0;
              const t0 = 12 + ri * 7;
              const dt = Math.min(2.5, 22 / Math.max(1, qtd));
              const fim = t0 + 6 + qtd * dt;
              const cnt = interpolate(f, [t0, fim], [0, it.n], { ...clamp, easing: EXPO });
              const cl = porLinha[chave(it)] ?? 6;
              return (
                <div key={ri} style={{ position: "absolute", left: 0, width: colW, top: Y0 - 190 + ri * rowH, height: rowH }}>
                  <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: "rgba(239,231,212,0.82)", letterSpacing: 1,
                    display: "flex", alignItems: "center", gap: 14, opacity: ent(f, t0 - 4), whiteSpace: "nowrap" }}>
                    <span>{it.rotulo}</span>
                    {u > 1 ? <span style={{ display: "flex", alignItems: "center", gap: 8, color: "rgba(239,231,212,0.6)", fontWeight: 400 }}>
                      · <Glifo tipo={it.icone} h={26} cor="rgba(239,231,212,0.6)" /> = {fmtEs(u)}</span> : null}
                  </div>
                  <div style={{ position: "absolute", top: 48 * s, left: 0, right: numW, display: "flex", flexWrap: "wrap",
                    rowGap: 6 * s, columnGap: slotPad, maxHeight: iconH * 2 + 6 * s + 2 }}>
                    {Array.from({ length: Math.min(qtd, cl * 2) }, (_, j) => {
                      const k = ent(f, t0 + j * dt, t0 + j * dt + 8);
                      return <div key={j} style={{ opacity: k, transform: `translateY(${(1 - k) * 12}px) scale(${0.7 + 0.3 * k})` }}>
                        <Glifo tipo={it.icone} h={iconH} cor={cor} /></div>;
                    })}
                    {qtd === 0 ? <div style={{ height: iconH, display: "flex", alignItems: "center", opacity: ent(f, t0) }}>
                      <div style={{ width: 120, height: 3, background: cor, opacity: 0.5 }} /></div> : null}
                  </div>
                  <div style={{ position: "absolute", right: 0, top: 40 * s, ...type.display, fontSize: 84 * Math.max(0.8, s), lineHeight: 1.1,
                    color: cor, fontVariantNumeric: "tabular-nums", opacity: ent(f, t0) }}>{fmtEs(cnt)}</div>
                  <div style={{ position: "absolute", left: 0, right: 0, bottom: 8, height: 1, background: "rgba(201,164,92,0.22)" }} />
                </div>
              );
            })}
          </div>
        );
      })}
      {Array.from({ length: n - 1 }, (_, i) => (
        <div key={i} style={{ position: "absolute", left: 90 + (i + 1) * colW + i * GAP + GAP / 2, top: 200, height: 760 * ent(f, 4, 30),
          width: 1, background: `linear-gradient(${LATAO}, transparent)`, opacity: 0.6 }} />
      ))}
      <FilmeVelho feixe={false} forca={0.35} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PERISCÓPIO / BINÓCULO
export type PeriscopioProps = SceneProps & {
  src: string;
  titulo: string;
  distancia?: string;        // "4.800 m" — o telêmetro "procura" e trava neste valor
  rumo?: string;             // "072°" — o número centraliza a fita de rumo
  modo?: "periscopio" | "binoculo";
};

/** A foto vista pela ocular: máscara circular (ou dupla, binóculo) que abre como íris, foto balançando com o mar e a
 *  água lavando a lente, retículo graduado, telêmetro que fecha no alvo, fita de rumo correndo e leituras nos cantos. */
export const Periscopio: React.FC<PeriscopioProps> = (p) => {
  const f = useCurrentFrame();
  const CREME = "#ebe4d0";
  const bin = p.modo === "binoculo";
  const CY = 590;
  const lentes = bin ? [{ x: 745, r: 350 }, { x: 1175, r: 350 }] : [{ x: 960, r: 390 }];
  const iris = interpolate(f, [0, 18], [0.04, 1], { ...clamp, easing: EXPO });
  const mask = lentes.map((l) => {
    const r = l.r * iris;
    return `radial-gradient(circle ${r}px at ${l.x}px ${CY}px, #000 ${r * 0.66}px, rgba(0,0,0,0.72) ${r * 0.88}px, rgba(0,0,0,0.35) ${r - 4}px, transparent ${r}px)`;
  }).join(", ");
  const dx = Math.sin(f / 26) * 18 + Math.sin(f / 11) * 4;
  const dy = Math.cos(f / 19) * 10 + Math.sin(f / 14) * 8;
  const roll = Math.sin(f / 33) * 0.8;
  const foco = interpolate(f, [0, 24], [10, 0], clamp);
  const RM = Math.max(...lentes.map((l) => l.r));
  const agua = CY + RM * 0.8 + Math.sin(f / 14) * 32 + Math.sin(f / 5.5) * 6;
  const ondaPath = (y0: number, fase: number) => {
    let d = `M0,${y0}`;
    for (let x = 0; x <= 1920; x += 40) d += ` L${x},${y0 + Math.sin(x / 90 + fase) * 10 + Math.sin(x / 37 - fase * 1.7) * 4}`;
    return `${d} L1920,1080 L0,1080 Z`;
  };
  // fita de rumo
  const base = parseFloat((p.rumo ?? "").replace(",", ".").replace(/[^\d.]/g, "")) || 0;
  const rumoAtual = base + Math.sin(f / 40) * 2.5 + (1 - ent(f, 0, 34)) * -22;
  const TW = 720, TX = 600, PX = 12;
  const ticks: React.ReactNode[] = [];
  for (let d = Math.floor(rumoAtual - 32); d <= Math.ceil(rumoAtual + 32); d++) {
    const x = TW / 2 + (d - rumoAtual) * PX;
    const m10 = ((d % 10) + 10) % 10 === 0, m5 = ((d % 5) + 5) % 5 === 0;
    ticks.push(<line key={`t${d}`} x1={x} x2={x} y1={72 - (m10 ? 24 : m5 ? 15 : 8)} y2={72} stroke={CREME} strokeWidth={m10 ? 2.5 : 1.5}
      opacity={m10 ? 0.95 : 0.6} />);
    if (m10 && Math.abs(x - TW / 2) < TW / 2 - 40) ticks.push(<text key={`n${d}`} x={x} y={34} textAnchor="middle" fill={CREME}
      style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>{p3(d)}</text>);
  }
  // telêmetro
  const fecha = ent(f, 14, 42);
  const trava = f >= 42;
  const flash = trava ? Math.max(0, 1 - (f - 42) / 10) : 0;
  const distTxt = (p.distancia ?? "").split("").map((ch, i) => (!trava && /\d/.test(ch) ? String(Math.floor(random(`pd${f}-${i}`) * 10)) : ch)).join("");
  const RC = bin ? 960 : 960;
  const reticulo: React.ReactNode[] = [];
  const RR = bin ? 300 : RM;
  for (let x = -RR; x <= RR; x += 20) {
    if (Math.abs(x) < 30) continue;
    const lg = x % 100 === 0 ? 22 : 10;
    reticulo.push(<line key={`h${x}`} x1={RC + x} x2={RC + x} y1={CY - lg} y2={CY} />);
  }
  for (let y = -RM; y <= RM; y += 20) {
    if (Math.abs(y) < 30) continue;
    const lg = y % 100 === 0 ? 22 : 10;
    reticulo.push(<line key={`v${y}`} x1={RC} x2={RC + lg} y1={CY + y} y2={CY + y} />);
  }
  const brk = 70 + (1 - fecha) * 190;
  const Icone: React.FC<{ tipo: "rumo" | "dist" }> = ({ tipo }) => (
    <svg width={44} height={44} viewBox="0 0 44 44" style={{ flex: "none" }}>
      {tipo === "rumo" ? <><circle cx={22} cy={22} r={18} fill="none" stroke={CREME} strokeWidth={2.5} />
        <path d="M22,6 L28,26 L22,22 L16,26 Z" fill={CREME} /></>
        : <path d="M4,10 L4,34 M40,10 L40,34 M4,22 L40,22 M10,16 L4,22 L10,28 M34,16 L40,22 L34,28" fill="none" stroke={CREME}
          strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />}
    </svg>
  );
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #101312 0%, #050606 60%, #000 100%)", ...exit(f, p.dur) }}>
      {/* vista pela ocular */}
      <AbsoluteFill style={{ maskImage: mask, WebkitMaskImage: mask }}>
        <Img src={src(p.src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
          filter: `blur(${foco}px) saturate(0.55) contrast(1.18) brightness(0.92)`,
          transform: `translate(${dx}px, ${dy}px) rotate(${roll}deg) scale(${interpolate(f, [0, p.dur], [1.3, 1.38], clamp)})` }} />
        <AbsoluteFill style={{ background: "rgba(40,95,90,0.28)", mixBlendMode: "multiply" }} />
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <path d={ondaPath(agua, f / 6)} fill="rgba(12,48,56,0.55)" />
          <path d={ondaPath(agua + 26, f / 4 + 1)} fill="rgba(6,28,34,0.75)" />
        </svg>
      </AbsoluteFill>
      {/* retículo */}
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: ent(f, 10, 24) }}>
        <defs><clipPath id="pcClip">{lentes.map((l, i) => <circle key={i} cx={l.x} cy={CY} r={l.r * iris} />)}</clipPath></defs>
        <g clipPath="url(#pcClip)">
          {[["rgba(255,255,255,0.35)", 5], ["#0a0d0d", 2]].map(([cor, w], k) => (
            <g key={k} stroke={cor as string} strokeWidth={w as number} fill="none">
              <line x1={RC - RR - 120} x2={RC - 30} y1={CY} y2={CY} /><line x1={RC + 30} x2={RC + RR + 120} y1={CY} y2={CY} />
              <line x1={RC} x2={RC} y1={CY - RM} y2={CY - 30} /><line x1={RC} x2={RC} y1={CY + 30} y2={CY + RM} />
              {reticulo}
              <circle cx={RC} cy={CY} r={6} />
              <path d={`M${RC - 90},${CY - brk} L${RC + 90},${CY - brk} M${RC - 90},${CY + brk} L${RC + 90},${CY + brk}
                M${RC - 90},${CY - brk} l0,18 M${RC + 90},${CY - brk} l0,18 M${RC - 90},${CY + brk} l0,-18 M${RC + 90},${CY + brk} l0,-18`} />
            </g>
          ))}
          {flash > 0 ? <rect x={RC - 96} y={CY - brk - 6} width={192} height={2 * brk + 12} fill="none" stroke="#ffcf6b" strokeWidth={3}
            opacity={flash} /> : null}
        </g>
        {!bin ? <circle cx={lentes[0].x} cy={CY} r={lentes[0].r * iris} fill="none" stroke="rgba(235,228,208,0.18)" strokeWidth={2} /> : null}
      </svg>
      {/* fita de rumo */}
      {p.rumo !== undefined ? (
        <div style={{ position: "absolute", left: TX, top: 90, width: TW, height: 100, opacity: ent(f, 6),
          maskImage: "linear-gradient(90deg, transparent, #000 18%, #000 82%, transparent)",
          WebkitMaskImage: "linear-gradient(90deg, transparent, #000 18%, #000 82%, transparent)" }}>
          <svg width={TW} height={100}>{ticks}
            <path d={`M${TW / 2 - 11},96 L${TW / 2},80 L${TW / 2 + 11},96 Z`} fill="#ffcf6b" /></svg>
        </div>
      ) : null}
      {/* título */}
      <div style={{ position: "absolute", left: 90, top: 90, width: 430, opacity: ent(f, 4), transform: `translateX(${(1 - ent(f, 4)) * -30}px)` }}>
        <div style={{ width: 70, height: 4, background: "#ffcf6b", marginBottom: 18 }} />
        <div style={{ ...type.display, fontSize: 50, lineHeight: 1.08, letterSpacing: 2, color: CREME, textTransform: "uppercase" }}>{p.titulo}</div>
      </div>
      {/* leituras */}
      {p.rumo ? (
        <div style={{ position: "absolute", right: 90, top: 96, display: "flex", alignItems: "center", gap: 18, opacity: ent(f, 10) }}>
          <Icone tipo="rumo" />
          <div style={{ ...type.display, fontSize: 60, color: CREME, letterSpacing: 2, lineHeight: 1 }}>{p.rumo}</div>
        </div>
      ) : null}
      {p.distancia ? (
        <div style={{ position: "absolute", right: 90, bottom: 90, display: "flex", alignItems: "center", gap: 18, opacity: ent(f, 14),
          border: `2px solid rgba(235,228,208,${0.35 + flash * 0.6})`, padding: "12px 26px", background: "rgba(0,0,0,0.45)" }}>
          <Icone tipo="dist" />
          <div style={{ ...type.display, fontSize: 64, lineHeight: 1, letterSpacing: 2, fontVariantNumeric: "tabular-nums",
            color: flash > 0.2 ? "#ffcf6b" : CREME }}>{distTxt}</div>
        </div>
      ) : null}
      <FilmeVelho feixe={false} forca={0.4} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PLACA DE IDENTIFICAÇÃO
export type PlacaProps = SceneProps & {
  linhas: string[];          // até 5 linhas curtas gravadas na placa
  legenda?: string;          // frase embaixo ("Soldado da FEB, Monte Castello, 1945")
};

/** Placas de identificação (dog tags) penduradas na corrente de bolinhas, girando de leve em 3D com brilho de metal;
 *  as linhas são cunhadas uma a uma e a legenda entra embaixo. */
export const PlacaIdentificacao: React.FC<PlacaProps> = (p) => {
  const f = useCurrentFrame();
  const linhas = p.linhas.slice(0, 5);
  const W = 820, H = 440, CX = 960, CY = 455;
  const desce = spring({ frame: f, fps: 30, config: { damping: 16, stiffness: 70 } });
  const balanco = spring({ frame: f - 4, fps: 30, config: { damping: 5, stiffness: 45 } });
  const ty = (1 - desce) * -720;
  const rz = interpolate(balanco, [0, 1], [-16, -3]);
  const rotY = Math.sin(f / 38) * 15 * ent(f, 6, 40) + (1 - ent(f, 0, 30)) * 38;
  const rotX = Math.sin(f / 53) * 5;
  const maxLen = Math.max(1, ...linhas.map((l) => l.length));
  const fs = Math.max(36, Math.min(58, 560 / (maxLen * 0.6)));
  const brilho = 50 + rotY * 4;
  const holeX = CX + (CX - W / 2 + 70 - CX) * Math.cos((rotY * Math.PI) / 180);
  const holeY = CY + ty + Math.sin((rz * Math.PI) / 180) * (CX - W / 2 + 70 - CX);
  const contas = (x0: number, y0: number, x1: number, y1: number, curva: number, pref: string) => {
    const pts: React.ReactNode[] = [];
    const len = Math.hypot(x1 - x0, y1 - y0) + Math.abs(curva);
    const nb = Math.floor(len / 14);
    for (let i = 0; i <= nb; i++) {
      const t = i / nb;
      const x = (1 - t) * (1 - t) * x0 + 2 * (1 - t) * t * ((x0 + x1) / 2 + curva) + t * t * x1;
      const y = (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2) + t * t * y1;
      pts.push(<circle key={`${pref}${i}`} cx={x} cy={y} r={5.5} fill="url(#conta)" />);
    }
    return pts;
  };
  const Placa: React.FC<{ fundo?: boolean }> = ({ fundo }) => (
    <div style={{ position: "absolute", left: -W / 2, top: -H / 2, width: W, height: H, borderRadius: 64, overflow: "hidden",
      background: "linear-gradient(135deg, #868c92 0%, #d4d8db 22%, #959ba1 45%, #e3e6e8 62%, #858b91 85%, #b3b8bc 100%)",
      boxShadow: "0 40px 70px rgba(0,0,0,0.6), inset 0 3px 2px rgba(255,255,255,0.75), inset 0 -4px 3px rgba(0,0,0,0.4)",
      filter: fundo ? "brightness(0.55)" : undefined }}>
      <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(90deg, rgba(255,255,255,0.06) 0 1px, transparent 1px 3px, rgba(0,0,0,0.04) 3px 4px)" }} />
      <div style={{ position: "absolute", inset: 18, borderRadius: 48,
        boxShadow: "inset 0 3px 3px rgba(0,0,0,0.35), inset 0 -2px 2px rgba(255,255,255,0.55), 0 2px 1px rgba(255,255,255,0.5)" }} />
      <div style={{ position: "absolute", left: 48, top: H / 2 - 22, width: 44, height: 44, borderRadius: "50%",
        background: "radial-gradient(circle at 50% 40%, #0c0d0e, #1d2022 70%)",
        boxShadow: "inset 0 4px 5px rgba(0,0,0,0.9), 0 2px 1px rgba(255,255,255,0.6)" }} />
      {!fundo ? (
        <div style={{ position: "absolute", left: 140, right: 60, top: 0, bottom: 0, display: "flex", flexDirection: "column",
          justifyContent: "center", fontFamily: MONO, fontWeight: 700, fontSize: fs, lineHeight: 1.22, letterSpacing: 2,
          color: "#454a4f", textTransform: "uppercase" }}>
          {linhas.map((l, i) => {
            const t0 = 14 + i * 5;
            const k = ent(f, t0, t0 + 8);
            return <div key={i} style={{ whiteSpace: "nowrap", opacity: k, transform: `scale(${1.25 - 0.25 * k})`, transformOrigin: "0% 50%",
              textShadow: "0 2px 0 rgba(255,255,255,0.6), 0 -1px 0 rgba(0,0,0,0.5)" }}>{l}</div>;
          })}
        </div>
      ) : null}
      <AbsoluteFill style={{ mixBlendMode: "overlay", background:
        `linear-gradient(105deg, transparent ${brilho - 22}%, rgba(255,255,255,0.85) ${brilho}%, transparent ${brilho + 22}%)` }} />
    </div>
  );
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #2d312b 0%, #141612 55%, #070807 100%)", overflow: "hidden",
      ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.4, backgroundImage:
        "repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0 1px, transparent 1px 4px), repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0 1px, transparent 1px 4px)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, rgba(255,236,200,0.12), transparent 55%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs><radialGradient id="conta" cx="0.35" cy="0.3" r="0.7">
          <stop offset="0" stopColor="#f6f7f8" /><stop offset="0.45" stopColor="#9aa0a5" /><stop offset="1" stopColor="#2c3033" /></radialGradient></defs>
        {contas(holeX + 6, holeY - 4, CX + 180, -30, 60, "b")}
      </svg>
      <div style={{ position: "absolute", left: CX, top: CY, transform: `translateY(${ty}px)`, perspective: 1800 }}>
        <div style={{ position: "absolute", transform: `translate(52px, 64px) rotate(${rz + 7}deg) rotateY(${rotY * 0.8}deg)` }}>
          <Placa fundo />
        </div>
        <div style={{ position: "absolute", transform: `rotate(${rz}deg) rotateY(${rotY}deg) rotateX(${rotX}deg)`, transformStyle: "preserve-3d" }}>
          <Placa />
        </div>
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {contas(holeX, holeY, CX - 260, -30, -40, "a")}
      </svg>
      {p.legenda ? (
        <div style={{ position: "absolute", left: 160, right: 160, top: 812, textAlign: "center", opacity: ent(f, 32, 48) }}>
          <div style={{ width: 120 * ent(f, 30, 50), height: 2, background: "#c9a45c", margin: "0 auto 26px" }} />
          <div style={{ fontFamily: SERIFA, fontStyle: "italic", fontSize: 46, lineHeight: 1.25, color: "#e9dfc8",
            transform: `translateY(${(1 - ent(f, 32, 50)) * 16}px)` }}>{p.legenda}</div>
        </div>
      ) : null}
      <FilmeVelho feixe={false} forca={0.35} />
    </AbsoluteFill>
  );
};

