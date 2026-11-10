// CINCO CARTÕES DO TEMA CARROS / ENGENHARIA AUTOMOTIVA (04/10/2026) — crises da indústria, recalls, fábricas e motores.
//   Velocimetro    — painel de instrumentos: ponteiro varre até o valor, mostrador digital conta, luzes de aviso piscam.
//   RaioX          — a foto do carro vira raio-X azul; uma linha de varredura passa e revela as peças com chamadas.
//   TesteColisao   — câmera de alta velocidade de teste de impacto: alvos amarelo/preto, contador de quadros, clarão e tremor.
//   AvisoRecall    — carta oficial de recall: timbre da marca, modelo, defeito, unidades contando e carimbo vermelho.
//   LinhaMontagem  — linha de montagem: esteira com carrocerias, robôs soldando com faíscas e contador de produção
//                    (descendo = fábrica fechando: a esteira para, a luz fica vermelha e o número cai).
// Mesmo contrato dos outros cartões (estilos5.tsx): SceneProps + dados, tudo cronometrado por p.dur, saída com exit().
// Todo número escrito neles tem de ser DITO na narração (regra do usuário). Rótulos fixos têm prop opcional para traduzir.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, spring, useCurrentFrame } from "remotion";
import { type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, SERIFA, Traco, clamp, src } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });
/** Milhar sem depender do locale do Chrome headless ("." no pt-BR, espaço fino no polonês). */
const milhar = (n: number, sep = ".") => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep);
const rad = (g: number) => (g * Math.PI) / 180;

// ================================================================================================ VELOCÍMETRO
export type VelocimetroProps = SceneProps & {
  titulo: string; valor: number; max: number; unidade: string; rotulo?: string; luzes?: string[];
  sep?: string;            // separador de milhar (padrão ".")
};
/** Quadro de instrumentos: mostrador analógico grande, ponteiro varre até `valor` (de `max`), leitura digital conta,
 *  luzes de aviso acendem no teste de ignição e depois piscam. */
export const Velocimetro: React.FC<VelocimetroProps> = (p) => {
  const f = useCurrentFrame();
  const CX = 640, CY = 560, R = 370;
  const A0 = 135, VARRE = 270;
  const max = Math.max(1, p.max);
  const alvo = Math.max(0, Math.min(1, p.valor / max));
  const mola = spring({ frame: f - 12, fps: 30, config: { damping: 13, stiffness: 38, mass: 1.1 } });
  const tremido = mola > 0.98 ? Math.sin(f / 2.3) * 0.003 + (random(`v${f}`) - 0.5) * 0.002 : 0;
  const pos = Math.max(0, alvo * mola + tremido);
  const angP = A0 + VARRE * Math.min(1.04, pos);
  const leitura = Math.min(p.valor, p.valor * mola);
  // escala "bonita"
  const bruto = max / 6, mag = Math.pow(10, Math.floor(Math.log10(bruto))), n = bruto / mag;
  const passo = (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
  const mult = max >= 10000 ? 1000 : 1;
  const maiores = Math.floor(max / passo + 1e-9);
  const pt = (a: number, r: number) => [CX + r * Math.cos(rad(a)), CY + r * Math.sin(rad(a))];
  const arco = (a1: number, a2: number, r: number) => {
    const [x1, y1] = pt(a1, r), [x2, y2] = pt(a2, r);
    return `M${x1},${y1} A${r},${r} 0 ${a2 - a1 > 180 ? 1 : 0},1 ${x2},${y2}`;
  };
  const surge = ent(f, 0, 18);
  const txt = String(milhar(leitura, p.sep));
  const tamDig = Math.min(180, 640 / Math.max(1, milhar(p.valor, p.sep).length * 0.5));
  const luzes = p.luzes ?? [];
  const PX = 1180;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 34% 52%, #1b1e24 0%, #0a0b0d 62%, #050506 100%)", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.35, backgroundImage:
        "repeating-linear-gradient(45deg, rgba(255,255,255,0.025) 0 6px, transparent 6px 12px), repeating-linear-gradient(-45deg, rgba(0,0,0,0.25) 0 6px, transparent 6px 12px)" }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${CX}px ${CY}px, rgba(255,140,40,${0.10 + 0.12 * pos}) 0, transparent 430px)` }} />
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: surge, transform: `scale(${0.94 + 0.06 * surge})`,
        transformOrigin: `${CX}px ${CY}px` }}>
        <defs>
          <radialGradient id="vFace" cx="50%" cy="40%" r="60%">
            <stop offset="0" stopColor="#1d2128" /><stop offset="0.85" stopColor="#0c0d10" /><stop offset="1" stopColor="#050506" />
          </radialGradient>
          <linearGradient id="vAro" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#9aa2ad" /><stop offset="0.45" stopColor="#2b2f36" /><stop offset="1" stopColor="#6c737d" />
          </linearGradient>
          <linearGradient id="vArc" x1="0" y1="1" x2="1" y2="0">
            <stop offset="0" stopColor="#ff7a18" stopOpacity={0.3} /><stop offset="1" stopColor="#ffb547" />
          </linearGradient>
          <radialGradient id="vHub" cx="40%" cy="35%" r="70%">
            <stop offset="0" stopColor="#d9dde3" /><stop offset="0.5" stopColor="#4a4f57" /><stop offset="1" stopColor="#15171a" />
          </radialGradient>
          <filter id="vGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" /></filter>
        </defs>
        <circle cx={CX} cy={CY} r={R + 34} fill="url(#vAro)" />
        <circle cx={CX} cy={CY} r={R + 20} fill="url(#vFace)" stroke="#000" strokeWidth={4} />
        {/* zona vermelha */}
        <path d={arco(A0 + VARRE * 0.85, A0 + VARRE, R - 14)} stroke="#d62a1e" strokeWidth={22} fill="none" opacity={0.9} />
        {/* arco de progresso */}
        <path d={arco(A0, Math.max(A0 + 0.5, angP), R - 14)} stroke="url(#vArc)" strokeWidth={10} fill="none" filter="url(#vGlow)" />
        <path d={arco(A0, Math.max(A0 + 0.5, angP), R - 14)} stroke="#ffb547" strokeWidth={4} fill="none" />
        {/* marcas */}
        {Array.from({ length: maiores * 5 + 1 }, (_, i) => {
          const v = (i * passo) / 5;
          if (v > max + 1e-9) return null;
          const a = A0 + VARRE * (v / max);
          const maior = i % 5 === 0;
          const [x1, y1] = pt(a, R - (maior ? 52 : 34));
          const [x2, y2] = pt(a, R - 2);
          const aceso = v / max <= pos + 0.001;
          return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={v / max >= 0.85 ? "#ff5040" : aceso ? "#ffe2b8" : "#8b929c"}
            strokeWidth={maior ? 6 : 2.5} strokeLinecap="butt" />;
        })}
        {Array.from({ length: maiores + 1 }, (_, i) => {
          const v = i * passo;
          const a = A0 + VARRE * (v / max);
          const [x, y] = pt(a, R - 100);
          const lv = v / mult;
          const rot = Number.isInteger(lv) ? String(lv) : lv.toFixed(1).replace(".", ",");
          return <text key={i} x={x} y={y + 13} textAnchor="middle" fill={v / max >= 0.85 ? "#ff6a5a" : "#e9ecf0"}
            style={{ ...type.displayMedium, fontSize: 40 }}>{rot}</text>;
        })}
        {mult > 1 ? <text x={CX} y={CY + 140} textAnchor="middle" fill="#8b929c" style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>
          ×{milhar(mult, p.sep)}</text> : null}
        <text x={CX} y={CY + 190} textAnchor="middle" fill="#8b929c" style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700,
          letterSpacing: 3 }}>{p.unidade.toUpperCase()}</text>
        {/* ponteiro */}
        <g transform={`rotate(${angP} ${CX} ${CY})`}>
          <polygon points={`${CX - 60},${CY - 9} ${CX + R - 40},${CY - 2} ${CX + R - 40},${CY + 2} ${CX - 60},${CY + 9}`} fill="#ff3d1f" filter="url(#vGlow)" opacity={0.8} />
          <polygon points={`${CX - 60},${CY - 9} ${CX + R - 40},${CY - 2} ${CX + R - 40},${CY + 2} ${CX - 60},${CY + 9}`} fill="#ff5a2a" />
        </g>
        <circle cx={CX} cy={CY} r={46} fill="url(#vHub)" stroke="#000" strokeWidth={3} />
        <circle cx={CX} cy={CY} r={14} fill="#0b0c0e" />
        {/* reflexo do vidro */}
        <path d={`M${CX - R + 40},${CY - 120} Q${CX},${CY - R - 60} ${CX + R - 40},${CY - 120} Q${CX},${CY - R + 90} ${CX - R + 40},${CY - 120} Z`}
          fill="#ffffff" opacity={0.045} />
      </svg>
      {/* painel direito */}
      <div style={{ position: "absolute", left: PX, right: 90, top: 200 }}>
        <div style={{ ...type.display, fontSize: 60, lineHeight: 1.08, color: "#f1f3f6", letterSpacing: 3, textTransform: "uppercase",
          opacity: ent(f, 4), transform: `translateX(${(1 - ent(f, 4)) * 40}px)` }}>{p.titulo}</div>
        {p.rotulo ? <div style={{ fontFamily: MONO, fontSize: 34, color: "#9aa2ad", marginTop: 14, opacity: ent(f, 10) }}>{p.rotulo}</div> : null}
        <div style={{ marginTop: 34, padding: "18px 30px 10px", background: "linear-gradient(180deg, #0d0f0c, #151a12)",
          border: "2px solid #2c3326", borderRadius: 14, boxShadow: "inset 0 0 40px rgba(0,0,0,0.9), 0 18px 40px rgba(0,0,0,0.6)",
          opacity: ent(f, 8), position: "relative", overflow: "hidden" }}>
          <div style={{ ...type.display, fontSize: tamDig, lineHeight: 1.05, color: "#ffb547", fontVariantNumeric: "tabular-nums",
            textShadow: "0 0 18px rgba(255,150,40,0.75), 0 0 2px #fff2d8", whiteSpace: "nowrap" }}>{txt}</div>
          <div style={{ fontFamily: MONO, fontSize: 36, fontWeight: 700, color: "#c9873a", letterSpacing: 4, paddingBottom: 8 }}>
            {p.unidade.toUpperCase()}</div>
          <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.22) 0 2px, transparent 2px 5px)" }} />
        </div>
        {luzes.length ? (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 18, marginTop: 40 }}>
            {luzes.map((l, i) => {
              const teste = f >= 6 && f < 20;
              const pisca = f >= 30 && ((f + i * 7) % 24) < 14;
              const aceso = teste || pisca;
              const cor = i % 2 === 0 ? "#ffa51f" : "#ff4a3a";
              return (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, padding: "10px 20px 10px 14px", borderRadius: 10,
                  background: aceso ? `${cor}22` : "rgba(255,255,255,0.03)", border: `2px solid ${aceso ? cor : "#2a2d33"}`,
                  boxShadow: aceso ? `0 0 26px ${cor}66` : "none", opacity: ent(f, 6 + i * 2) }}>
                  <svg width={44} height={40}>
                    <polygon points="22,3 42,37 2,37" fill="none" stroke={aceso ? cor : "#3a3e45"} strokeWidth={4} strokeLinejoin="round" />
                    <rect x={20} y={14} width={4} height={12} fill={aceso ? cor : "#3a3e45"} />
                    <rect x={20} y={29} width={4} height={4} fill={aceso ? cor : "#3a3e45"} />
                  </svg>
                  <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: aceso ? cor : "#4a4f57", letterSpacing: 2 }}>{l}</div>
                </div>
              );
            })}
          </div>
        ) : null}
      </div>
      <AbsoluteFill style={{ boxShadow: "inset 0 0 220px rgba(0,0,0,0.9)" }} />
    </AbsoluteFill>
  );
};

// ================================================================================================ RAIO-X
export type PecaRaioX = { x: number; y: number; rotulo: string };
export type RaioXProps = SceneProps & { src: string; titulo: string; pecas: PecaRaioX[]; legenda?: string };
/** A foto vira chapa de raio-X (invertida, azul e branca); a linha de varredura cruza da esquerda para a direita e cada
 *  peça ganha marcador e chamada quando a linha passa por ela. x/y das peças em 0-1 dentro da foto. */
export const RaioX: React.FC<RaioXProps> = (p) => {
  const f = useCurrentFrame();
  const X0 = 140, Y0 = 170, W = 1640, H = 820;
  const T0 = 8, SPAN = Math.min(40, p.dur * 0.28);
  const s = interpolate(f, [T0, T0 + SPAN], [0, 1], { ...clamp, easing: (t) => t });
  const lx = X0 + s * W;
  const varrendo = f >= T0 && f <= T0 + SPAN + 2;
  const CIANO = "#8fd3ff";
  const foto = { width: "100%", height: "100%", objectFit: "cover" as const, position: "absolute" as const,
    transform: `scale(${interpolate(f, [0, p.dur], [1.02, 1.08], clamp)})` };
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, #0b1524 0%, #03060b 75%)", ...exit(f, p.dur) }}>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id="rxBorda" colorInterpolationFilters="sRGB">
          <feColorMatrix type="matrix" values="0.3 0.59 0.11 0 0  0.3 0.59 0.11 0 0  0.3 0.59 0.11 0 0  0 0 0 1 0" />
          <feConvolveMatrix order="3" kernelMatrix="-1 -1 -1  -1 8 -1  -1 -1 -1" preserveAlpha="true" />
          <feColorMatrix type="matrix" values="3.2 0 0 0 0  3.6 0 0 0 0.02  4 0 0 0 0.05  0 0 0 1 0" />
        </filter>
      </svg>
      <div style={{ position: "absolute", left: X0, top: Y0, width: W, height: H, overflow: "hidden", opacity: ent(f, 0, 10),
        background: "#02050a" }}>
        {/* foto comum, apagada, à direita da linha */}
        <Img src={src(p.src)} style={{ ...foto, filter: "grayscale(1) brightness(0.38) contrast(1.1)" }} />
        {/* chapa de raio-X à esquerda da linha */}
        <div style={{ position: "absolute", inset: 0, clipPath: `inset(0 ${(1 - s) * 100}% 0 0)` }}>
          <Img src={src(p.src)} style={{ ...foto, filter: "grayscale(1) invert(1) contrast(1.5) brightness(0.55)" }} />
          <AbsoluteFill style={{ background: "#2a7fff", mixBlendMode: "multiply", opacity: 0.95 }} />
          <Img src={src(p.src)} style={{ ...foto, filter: "url(#rxBorda)", mixBlendMode: "screen", opacity: 0.95 }} />
          <Img src={src(p.src)} style={{ ...foto, filter: "url(#rxBorda) blur(5px)", mixBlendMode: "screen", opacity: 0.6 }} />
          <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, rgba(170,220,255,0.18), transparent 70%)", mixBlendMode: "screen" }} />
          <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.18) 0 1px, transparent 1px 4px)" }} />
        </div>
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.7))" }} />
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="rxRastro" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor={CIANO} stopOpacity={0} /><stop offset="1" stopColor={CIANO} stopOpacity={0.35} />
          </linearGradient>
          <filter id="rxGlow" x="-200%" y="-10%" width="500%" height="120%"><feGaussianBlur stdDeviation="8" /></filter>
        </defs>
        {/* moldura em colchetes */}
        {[[X0, Y0, 1, 1], [X0 + W, Y0, -1, 1], [X0, Y0 + H, 1, -1], [X0 + W, Y0 + H, -1, -1]].map(([x, y, sx, sy], i) => (
          <path key={i} d={`M${x + sx * 70},${y - sy * 14} L${x - sx * 14},${y - sy * 14} L${x - sx * 14},${y + sy * 70}`}
            stroke={CIANO} strokeWidth={4} fill="none" opacity={ent(f, 2)} />
        ))}
        {/* régua inferior */}
        {Array.from({ length: 41 }, (_, i) => (
          <line key={i} x1={X0 + (i * W) / 40} x2={X0 + (i * W) / 40} y1={Y0 + H + 22} y2={Y0 + H + (i % 5 === 0 ? 46 : 34)}
            stroke={CIANO} strokeOpacity={0.55} strokeWidth={2} opacity={ent(f, 6)} />
        ))}
        {/* linha de varredura */}
        {varrendo ? (
          <g>
            <rect x={Math.max(X0, lx - 160)} y={Y0} width={Math.min(160, lx - X0)} height={H} fill="url(#rxRastro)" />
            <rect x={lx - 6} y={Y0 - 30} width={12} height={H + 60} fill={CIANO} filter="url(#rxGlow)" />
            <rect x={lx - 2} y={Y0 - 30} width={4} height={H + 60} fill="#ffffff" />
          </g>
        ) : null}
        {/* peças */}
        {(() => {
          const caixas: { x: number; y: number; w: number }[] = [];
          return p.pecas.map((pc, i) => {
          const t0 = T0 + pc.x * SPAN;
          const k = ent(f, t0, t0 + 14);
          if (f < t0) return null;
          const x = X0 + pc.x * W, y = Y0 + pc.y * H;
          const dir = pc.x > 0.55 ? -1 : 1;
          const sobe = pc.y > 0.45 ? -1 : 1;
          const larg = pc.rotulo.length * 20.4 + 96;
          let ey = Math.max(Y0 + 50, Math.min(Y0 + H - 50, y + sobe * 130));
          const ex = x + dir * 110;
          let bx = dir > 0 ? ex : ex - larg;
          bx = Math.max(X0 + 20, Math.min(X0 + W - larg - 20, bx));
          for (let n = 0; n < 8 && caixas.some((c) => bx < c.x + c.w + 20 && c.x < bx + larg + 20 && Math.abs(c.y - ey) < 84); n++) {
            ey += sobe * 90;
            if (ey < Y0 + 50 || ey > Y0 + H - 50) { ey = Math.max(Y0 + 50, Math.min(Y0 + H - 50, ey)); break; }
          }
          caixas.push({ x: bx, y: ey, w: larg });
          const fimX = dir > 0 ? bx : bx + larg;
          const by = ey - 34;
          const pulso = (f - t0) % 30 / 30;
          return (
            <g key={i}>
              <circle cx={x} cy={y} r={11} fill="#ffffff" opacity={k} />
              <circle cx={x} cy={y} r={18 + 26 * pulso} fill="none" stroke={CIANO} strokeWidth={3} opacity={(1 - pulso) * k} />
              <Traco d={`M${x},${y} L${ex},${ey} L${fimX},${ey}`} p={k} cor={CIANO} w={3} />
              <g opacity={ent(f, t0 + 6, t0 + 16)}>
                <rect x={bx} y={by} width={larg} height={68} fill="rgba(3,10,20,0.82)" stroke={CIANO} strokeWidth={2.5} />
                <rect x={bx} y={by} width={58} height={68} fill={CIANO} />
                <text x={bx + 29} y={by + 46} textAnchor="middle" fill="#03101e" style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>
                  {String(i + 1).padStart(2, "0")}</text>
                <text x={bx + 76} y={by + 46} fill="#eaf6ff" style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700 }}>{pc.rotulo}</text>
              </g>
            </g>
          );
        });
        })()}
      </svg>
      <div style={{ position: "absolute", left: X0 - 14, top: 66, ...type.display, fontSize: 60, color: "#eaf6ff", letterSpacing: 4,
        textTransform: "uppercase", opacity: ent(f, 3), textShadow: "0 0 24px rgba(120,190,255,0.45)" }}>{p.titulo}</div>
      <div style={{ position: "absolute", right: 1920 - X0 - W - 14, top: 82, fontFamily: MONO, fontSize: 34, fontWeight: 700,
        color: CIANO, letterSpacing: 3, opacity: ent(f, 6), fontVariantNumeric: "tabular-nums" }}>
        {p.legenda ?? "SCAN"} {String(Math.round(s * 100)).padStart(3, " ")}%</div>
    </AbsoluteFill>
  );
};

// ================================================================================================ TESTE DE COLISÃO
export type MarcaColisao = { x: number; y: number };
export type TesteColisaoProps = SceneProps & {
  src: string; titulo: string; velocidade: string; resultado?: string; nota?: string;
  rotulo?: string;              // sobre a velocidade (padrão "VELOCIDADE DE IMPACTO")
  marcas?: MarcaColisao[];      // alvos amarelo/preto, x/y 0-1 da TELA (a foto cobre o quadro inteiro)
  cadencia?: number;            // quadros por segundo da câmera rápida (padrão 1000)
};
/** Câmera de alta velocidade de teste de impacto: a foto avança, bate (clarão, tremor, aberração), o contador de quadros
 *  desacelera para câmera lenta e entra a leitura da velocidade com faixa zebrada. */
export const TesteColisao: React.FC<TesteColisaoProps> = (p) => {
  const f = useCurrentFrame();
  const IMP = Math.round(Math.min(22, p.dur * 0.15));
  const fps = p.cadencia ?? 1000;
  const porQuadro = fps / 30;
  const quadros = f < IMP ? f * porQuadro : IMP * porQuadro + (f - IMP) * 1.2;
  const ms = (quadros / fps) * 1000;
  const pos = f - IMP;
  const choque = pos >= 0 ? Math.exp(-pos / 5) : 0;
  const shx = (random(`sx${f}`) - 0.5) * 60 * choque, shy = (random(`sy${f}`) - 0.5) * 40 * choque;
  const zoom = f < IMP ? interpolate(f, [0, IMP], [1.0, 1.1], { ...clamp, easing: (t) => t * t }) : 1.16 + 0.04 * ent(f, IMP, p.dur);
  const flash = pos >= 0 ? interpolate(pos, [0, 1, 7], [0.95, 0.8, 0], clamp) : 0;
  const marcas = p.marcas ?? [{ x: 0.22, y: 0.5 }, { x: 0.5, y: 0.36 }, { x: 0.74, y: 0.6 }];
  const AM = "#ffd21f";
  const pn = ent(f, IMP + 4, IMP + 20);
  const BAR = 118;
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `translate(${shx}px, ${shy}px) scale(${zoom})` }}>
        <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover",
          filter: "grayscale(0.75) contrast(1.25) brightness(0.82)" }} />
        {choque > 0.05 ? <>
          <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", mixBlendMode: "screen",
            opacity: 0.5 * choque, transform: `translateX(${14 * choque}px)`, filter: "grayscale(1) sepia(1) hue-rotate(-50deg) saturate(6)" }} />
          <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", mixBlendMode: "screen",
            opacity: 0.5 * choque, transform: `translateX(${-14 * choque}px)`, filter: "grayscale(1) sepia(1) hue-rotate(170deg) saturate(6)" }} />
        </> : null}
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(10,30,40,0.25), rgba(0,0,0,0.15))", mixBlendMode: "multiply" }} />
        {/* alvos de teste de impacto */}
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          {marcas.map((m, i) => {
            const k = spring({ frame: f - 3 - i * 3, fps: 30, config: { damping: 12, stiffness: 160 } });
            const cx = m.x * 1920, cy = m.y * 1080, r = 34 * k;
            return (
              <g key={i}>
                <circle cx={cx} cy={cy} r={r + 4} fill="#fff" />
                <path d={`M${cx},${cy} L${cx + r},${cy} A${r},${r} 0 0,1 ${cx},${cy + r} Z M${cx},${cy} L${cx - r},${cy} A${r},${r} 0 0,1 ${cx},${cy - r} Z`} fill={AM} />
                <path d={`M${cx},${cy} L${cx},${cy + r} A${r},${r} 0 0,1 ${cx - r},${cy} Z M${cx},${cy} L${cx},${cy - r} A${r},${r} 0 0,1 ${cx + r},${cy} Z`} fill="#111" />
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 50%, rgba(0,0,0,0.75))" }} />
      {/* retícula da câmera */}
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.55 }}>
        <line x1={960} x2={960} y1={500} y2={580} stroke="#fff" strokeWidth={2} />
        <line x1={920} x2={1000} y1={540} y2={540} stroke="#fff" strokeWidth={2} />
        {[[90, BAR + 30], [1830, BAR + 30], [90, 1080 - BAR - 30], [1830, 1080 - BAR - 30]].map(([x, y], i) => (
          <g key={i}>{[0, 1, 2, 3].map((j) => <rect key={j} x={x - 24 + (j % 2) * 24} y={y - 24 + Math.floor(j / 2) * 24} width={24} height={24}
            fill={(j === 0 || j === 3) ? "#fff" : "#000"} />)}</g>
        ))}
      </svg>
      <AbsoluteFill style={{ background: "#fff", opacity: flash }} />
      {/* barras de cinema com HUD */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: BAR, background: "#000", display: "flex", alignItems: "center",
        justifyContent: "space-between", padding: "0 90px", boxSizing: "border-box" }}>
        <div style={{ ...type.display, fontSize: 54, color: "#fff", letterSpacing: 4, textTransform: "uppercase", opacity: ent(f, 2),
          whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: 1240 }}>{p.titulo}</div>
        <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: "#fff", letterSpacing: 2, display: "flex", gap: 26, alignItems: "center" }}>
          <span>{milhar(fps)} FPS</span>
          <span style={{ color: "#ff3b30", opacity: f % 24 < 15 ? 1 : 0.25 }}>● REC</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: BAR, background: "#000", display: "flex", alignItems: "center",
        justifyContent: "space-between", padding: "0 90px", boxSizing: "border-box", fontFamily: MONO, fontSize: 36, fontWeight: 700,
        color: AM, letterSpacing: 2, fontVariantNumeric: "tabular-nums" }}>
        <span>T+ {(ms / 1000).toFixed(3).replace(".", ",")} s</span>
        <div style={{ flex: 1, margin: "0 50px", height: 22, backgroundImage: `linear-gradient(90deg, ${AM} 0 50%, #111 50% 100%)`,
          backgroundSize: "60px 100%", backgroundRepeat: "round", opacity: 0.85 }} />
        <span>FRAME {String(Math.floor(quadros)).padStart(5, "0")}</span>
      </div>
      {/* leitura */}
      <div style={{ position: "absolute", left: 90, bottom: BAR + 60, width: 820, opacity: pn, transform: `translateX(${(1 - pn) * -60}px)`,
        background: "rgba(8,8,8,0.88)", boxShadow: "0 20px 50px rgba(0,0,0,0.7)" }}>
        <div style={{ height: 26, backgroundImage: `repeating-linear-gradient(-45deg, ${AM} 0 22px, #111 22px 44px)` }} />
        <div style={{ padding: "22px 36px 30px" }}>
          <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: "#cfcfcf", letterSpacing: 3 }}>{p.rotulo ?? "VELOCIDADE DE IMPACTO"}</div>
          <div style={{ ...type.display, fontSize: 150, lineHeight: 1, color: AM, marginTop: 6, whiteSpace: "nowrap" }}>{p.velocidade}</div>
          {p.resultado ? <div style={{ fontFamily: MONO, fontSize: 38, fontWeight: 700, color: "#fff", marginTop: 16, lineHeight: 1.2,
            opacity: ent(f, IMP + 14) }}>{p.resultado}</div> : null}
          {p.nota ? <div style={{ display: "inline-block", marginTop: 20, padding: "8px 18px", background: "#e0261b", color: "#fff",
            ...type.display, fontSize: 40, letterSpacing: 3, textTransform: "uppercase", opacity: ent(f, IMP + 22),
            transform: `scale(${1.3 - 0.3 * ent(f, IMP + 22)})`, transformOrigin: "0 50%" }}>{p.nota}</div> : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ================================================================================================ AVISO DE RECALL
export type RotulosRecall = { cabecalho?: string; modelo?: string; defeito?: string; unidades?: string; data?: string };
export type AvisoRecallProps = SceneProps & {
  marca: string; modelo: string; defeito: string; unidades: number; data: string; carimbo?: string;
  rotulos?: RotulosRecall; sep?: string;
};
/** Carta oficial de recall sobre a mesa: timbre da marca, modelo, defeito, unidades afetadas contando e carimbo
 *  vermelho que bate no papel. */
export const AvisoRecall: React.FC<AvisoRecallProps> = (p) => {
  const f = useCurrentFrame();
  const r = { cabecalho: "COMUNICADO DE SEGURANÇA", modelo: "MODELO", defeito: "DEFEITO", unidades: "UNIDADES AFETADAS",
    data: "DATA", ...(p.rotulos ?? {}) };
  const g = spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 70 } });
  const push = interpolate(f, [0, p.dur], [1, 1.05], clamp);
  const CT = 22, CL = Math.max(30, p.dur * 0.3);
  const conta = interpolate(f, [CT, CT + CL], [0, 1], { ...clamp, easing: EXPO });
  const BATE = Math.round(Math.min(40, p.dur * 0.26));
  const st = spring({ frame: f - BATE, fps: 30, config: { damping: 11, stiffness: 210, mass: 0.8 } });
  const tranco = f >= BATE ? Math.exp(-(f - BATE) / 3) * 7 : 0;
  const carimbo = p.carimbo ?? "RECALL";
  const PL = 400, PT = 60, PW = 1120;
  const VERM = "#b3170f";
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 48% 40%, #2c2f33 0%, #121315 60%, #070708 100%)", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${push}) translateY(${tranco}px)`, transformOrigin: "50% 40%" }}>
        <div style={{ position: "absolute", left: PL, top: PT, width: PW, height: 1100, background: "#f3f0e8",
          boxShadow: "0 40px 90px rgba(0,0,0,0.75), 0 0 0 1px rgba(0,0,0,0.2)",
          transform: `translateY(${(1 - g) * 220}px) rotate(${-1.2 + (1 - g) * 4}deg)`, opacity: Math.min(1, g * 1.6),
          backgroundImage: "radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.7), transparent 60%), linear-gradient(180deg, rgba(0,0,0,0) 70%, rgba(80,60,30,0.08))" }}>
          <div style={{ padding: "70px 90px 0" }}>
            {/* timbre */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
              <div style={{ ...type.display, fontSize: 84, lineHeight: 1, color: "#111", letterSpacing: 10, textTransform: "uppercase" }}>{p.marca}</div>
              <div style={{ textAlign: "right", fontFamily: MONO, fontSize: 34, fontWeight: 700, color: "#3a3a3a", lineHeight: 1.25 }}>
                <div>{r.data}</div><div style={{ color: "#111" }}>{p.data}</div></div>
            </div>
            <div style={{ height: 6, background: "#111", marginTop: 22 }} />
            <div style={{ height: 2, background: "#111", marginTop: 6 }} />
            <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: VERM, letterSpacing: 6, marginTop: 18 }}>{r.cabecalho}</div>
            {/* modelo */}
            <div style={{ marginTop: 44, opacity: ent(f, 10) }}>
              <div style={{ fontFamily: MONO, fontSize: 34, color: "#6b6760", letterSpacing: 4 }}>{r.modelo}</div>
              <div style={{ ...type.display, fontSize: 72, lineHeight: 1.05, color: "#111", textTransform: "uppercase" }}>{p.modelo}</div>
            </div>
            {/* defeito */}
            <div style={{ marginTop: 30, opacity: ent(f, 14), maxWidth: 900 }}>
              <div style={{ fontFamily: MONO, fontSize: 34, color: "#6b6760", letterSpacing: 4 }}>{r.defeito}</div>
              <div style={{ fontFamily: SERIFA, fontSize: 42, lineHeight: 1.25, color: "#1a1a1a", marginTop: 6,
                clipPath: `inset(0 ${100 - ent(f, 14, 40) * 100}% 0 0)` }}>{p.defeito}</div>
            </div>
            {/* unidades */}
            <div style={{ marginTop: 36, opacity: ent(f, CT - 4) }}>
              <div style={{ fontFamily: MONO, fontSize: 34, color: "#6b6760", letterSpacing: 4 }}>{r.unidades}</div>
              <div style={{ position: "relative", display: "inline-block" }}>
                <div style={{ ...type.display, fontSize: 150, lineHeight: 1.05, color: VERM, fontVariantNumeric: "tabular-nums" }}>
                  {milhar(p.unidades * conta, p.sep)}</div>
                <svg width={760} height={40} style={{ position: "absolute", left: -10, bottom: -18 }}>
                  <Traco d="M5,22 C180,8 420,34 740,14" p={ent(f, CT + CL * 0.6, CT + CL * 0.6 + 16)} cor={VERM} w={7} />
                </svg>
              </div>
            </div>
          </div>
        </div>
        {/* carimbo */}
        {f >= BATE ? (
          <div style={{ position: "absolute", left: PL + PW - 600, top: 700, transform: `rotate(-12deg) scale(${2.4 - 1.4 * st})`,
            opacity: Math.min(1, st * 2) * 0.95, mixBlendMode: "multiply", transformOrigin: "50% 50%" }}>
            <svg width={560} height={200} style={{ overflow: "visible" }}>
              <defs>
                <filter id="rcTinta"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={7} result="n" />
                  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.55" result="m" />
                  <feComposite in="SourceGraphic" in2="m" operator="in" result="t" />
                  <feDisplacementMap in="t" in2="n" scale="5" /></filter>
              </defs>
              <g filter="url(#rcTinta)">
                <rect x={8} y={8} width={544} height={184} rx={10} fill="none" stroke="#c4170c" strokeWidth={10} />
                <rect x={24} y={24} width={512} height={152} rx={6} fill="none" stroke="#c4170c" strokeWidth={4} />
                <text x={280} y={100 + Math.min(130, 900 / Math.max(1, carimbo.length)) * 0.36} textAnchor="middle" fill="#c4170c"
                  style={{ ...type.display, fontSize: Math.min(130, 900 / Math.max(1, carimbo.length)), letterSpacing: 8 }}>{carimbo}</text>
              </g>
            </svg>
          </div>
        ) : null}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 45% 35%, transparent 50%, rgba(0,0,0,0.6) 100%)" }} />
    </AbsoluteFill>
  );
};

// ================================================================================================ LINHA DE MONTAGEM
export type LinhaMontagemProps = SceneProps & {
  titulo: string; total: number; unidade: string; sub?: string;
  descendo?: boolean;   // true = fábrica fechando: conta de `total` até `fim`, a esteira para e a luz fica vermelha
  fim?: number;         // valor final quando descendo (padrão 0)
  status?: string;      // plaquinha no canto ("LINHA 1 · EM OPERAÇÃO")
  sep?: string;
};
const CARRO = "M10,118 L10,90 Q12,72 40,66 L112,58 Q150,22 200,18 L292,18 Q322,20 352,52 L404,62 Q432,68 434,92 L434,118 Z";
/** Linha de montagem: carrocerias deslizam na esteira, robôs soldam com faíscas, contador grande de produção. */
export const LinhaMontagem: React.FC<LinhaMontagemProps> = (p) => {
  const f = useCurrentFrame();
  const desc = !!p.descendo;
  const T = p.dur * 0.7;
  const v0 = 7;
  const tt = Math.min(f, T);
  const andou = desc ? v0 * (tt - (tt * tt) / (2 * T)) + 0 : v0 * f;
  const vel = desc ? Math.max(0, 1 - f / T) : 1;
  const C0 = 12, C1 = Math.max(50, p.dur * 0.5);
  const k = desc
    ? interpolate(f, [18, Math.max(60, p.dur * 0.72)], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.25, 1) })
    : interpolate(f, [C0, C1], [0, 1], { ...clamp, easing: EXPO });
  const de = desc ? p.total : 0, ate = desc ? (p.fim ?? 0) : p.total;
  const num = de + (ate - de) * k;
  const verm = desc ? interpolate(f, [p.dur * 0.25, p.dur * 0.6], [0, 1], clamp) : 0;
  const LUZ = verm > 0.5 ? "#ff3a2a" : "#ffb23a";
  const BELT = 840, ESP = 620, CW = 444;
  const carros = Array.from({ length: 5 }, (_, i) => {
    const x = ((i * ESP + andou) % (ESP * 5)) - ESP;
    return x;
  });
  const BRACOS = [1180, 1640];
  const L1 = 190, L2 = 170, VIGA = 470;
  return (
    <AbsoluteFill style={{ background: "#07080a", overflow: "hidden", ...exit(f, p.dur) }}>
      {/* parede da fábrica: janelas altas e névoa */}
      <AbsoluteFill style={{ opacity: 0.22, backgroundImage:
        "linear-gradient(90deg, rgba(160,180,200,0.35) 0 4px, transparent 4px), linear-gradient(rgba(160,180,200,0.35) 0 4px, transparent 4px)",
        backgroundSize: "160px 120px", maskImage: "linear-gradient(180deg, black 0%, transparent 75%)" }} />
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 75% 30%, ${desc ? `rgba(255,60,40,${0.08 + 0.18 * verm})` : "rgba(255,190,110,0.16)"}, transparent 60%)` }} />
      <AbsoluteFill style={{ background: "linear-gradient(105deg, transparent 40%, rgba(255,230,190,0.06) 55%, transparent 62%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="lmCarro" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#a9b0b9" /><stop offset="0.5" stopColor="#5d646d" /><stop offset="1" stopColor="#2a2e34" />
          </linearGradient>
          <linearGradient id="lmPiso" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#1a1c20" /><stop offset="1" stopColor="#060607" />
          </linearGradient>
          <filter id="lmGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" /></filter>
          <linearGradient id="lmCone" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={LUZ} stopOpacity={0.22} /><stop offset="1" stopColor={LUZ} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="lmNevoa" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#9fb0c4" stopOpacity={0} /><stop offset="1" stopColor="#9fb0c4" stopOpacity={0.10} />
          </linearGradient>
        </defs>
        {[160, 560, 960, 1360, 1760].map((x, i) => (
          <polygon key={`c${i}`} points={`${x - 14},${VIGA + 50} ${x + 14},${VIGA + 50} ${x + 230},${BELT + 30} ${x - 230},${BELT + 30}`}
            fill="url(#lmCone)" opacity={desc && verm > 0.5 ? (f % 20 < 11 ? 0.9 : 0.3) : 0.8} />
        ))}
        <rect x={0} y={BELT - 260} width={1920} height={260} fill="url(#lmNevoa)" />
        {/* viga do pórtico */}
        <rect x={0} y={VIGA - 26} width={1920} height={40} fill="#1c1f24" />
        <rect x={0} y={VIGA + 14} width={1920} height={12} fill="url(#lmZebra)" />
        <pattern id="lmZebra" width={40} height={12} patternUnits="userSpaceOnUse" patternTransform="skewX(-40)">
          <rect width={20} height={12} fill="#e0a21a" /><rect x={20} width={20} height={12} fill="#141414" />
        </pattern>
        {[160, 560, 960, 1360, 1760].map((x, i) => (
          <g key={i}>
            <circle cx={x} cy={VIGA + 46} r={10} fill={LUZ} opacity={desc && verm > 0.5 ? (f % 20 < 11 ? 1 : 0.25) : 0.9} />
            <circle cx={x} cy={VIGA + 46} r={26} fill={LUZ} opacity={0.35} filter="url(#lmGlow)" />
          </g>
        ))}
        {/* piso e esteira */}
        <rect x={0} y={BELT} width={1920} height={240} fill="url(#lmPiso)" />
        <rect x={0} y={BELT} width={1920} height={34} fill="#2a2d31" />
        {Array.from({ length: 34 }, (_, i) => {
          const x = ((i * 60 + andou) % 2040) - 60;
          return <rect key={i} x={x} y={BELT + 4} width={6} height={26} fill="#16181b" />;
        })}
        <rect x={0} y={BELT + 34} width={1920} height={10} fill="#e0a21a" opacity={0.85} />
        {Array.from({ length: 21 }, (_, i) => {
          const cx = i * 96 + 20, cy = BELT + 78;
          const a = (andou / 30) * (180 / Math.PI);
          return (
            <g key={i}>
              <circle cx={cx} cy={cy} r={28} fill="#22252a" stroke="#3a3e45" strokeWidth={3} />
              <line x1={cx} y1={cy} x2={cx + 24 * Math.cos(rad(a))} y2={cy + 24 * Math.sin(rad(a))} stroke="#555b63" strokeWidth={4} />
            </g>
          );
        })}
        {/* carrocerias */}
        {carros.map((x, i) => {
          const y = BELT - 148;
          return (
            <g key={i} transform={`translate(${x},${y})`}>
              <ellipse cx={CW / 2} cy={150} rx={CW / 2} ry={8} fill="#000" opacity={0.6} />
              <path d={CARRO} fill="url(#lmCarro)" stroke="#d9dee5" strokeOpacity={0.5} strokeWidth={2} />
              <path d="M130,58 Q160,30 200,27 L242,27 L242,58 Z" fill="#0d0f12" opacity={0.9} />
              <path d="M252,27 L290,27 Q314,29 338,56 L252,58 Z" fill="#0d0f12" opacity={0.9} />
              <line x1={246} y1={60} x2={246} y2={116} stroke="#2a2e34" strokeWidth={3} />
              <path d="M40,80 L420,80" stroke="#ffffff" strokeOpacity={0.18} strokeWidth={3} />
              <path d="M40,66 L112,58 Q150,22 200,18 L292,18 Q322,20 352,52 L404,62" fill="none" stroke="#ffffff" strokeOpacity={0.6} strokeWidth={3} />
              <path d="M420,74 L433,78 L433,90 L414,88 Z" fill="#e8eef5" opacity={0.85} />
              <path d="M10,82 L22,76 L24,92 L10,94 Z" fill="#c0261c" opacity={0.9} />
              <path d="M126,62 L126,112 M368,64 L368,92" stroke="#2a2e34" strokeWidth={2} />
              {[95, 352].map((wx) => <g key={wx}><circle cx={wx} cy={118} r={30} fill="#0b0c0e" stroke="#4c525a" strokeWidth={4} />
                <circle cx={wx} cy={118} r={11} fill="#6a717a" /></g>)}
            </g>
          );
        })}
        {/* robôs */}
        {BRACOS.map((bx, i) => {
          const ativo = vel > 0.25;
          const tx = bx + 50 * Math.sin(f / 11 + i * 2) * Math.max(0.2, vel), ty = BELT - 136 - 30 * (1 - vel);
          const dx = tx - bx, dy = ty - VIGA;
          const d = Math.min(L1 + L2 - 1, Math.hypot(dx, dy));
          const cosE = (d * d - L1 * L1 - L2 * L2) / (2 * L1 * L2);
          const e = Math.acos(Math.max(-1, Math.min(1, cosE)));
          const base = Math.atan2(dy, dx) - Math.atan2(L2 * Math.sin(e), L1 + L2 * Math.cos(e));
          const jx = bx + L1 * Math.cos(base), jy = VIGA + L1 * Math.sin(base);
          const px = jx + L2 * Math.cos(base + e), py = jy + L2 * Math.sin(base + e);
          const soldando = ativo && Math.sin(f / 4 + i * 1.7) > -0.3;
          const fa = Array.from({ length: soldando ? 26 : 0 }, (_, j) => {
            const nasce = f - (j % 13);
            const idade = f - nasce + random(`id${i}-${j}`) * 0.9;
            const vx = (random(`fx${i}-${nasce}-${j}`) - 0.5) * 26, vy = -random(`fy${i}-${nasce}-${j}`) * 14 - 2;
            const x = px + vx * idade, y = py + vy * idade + 1.6 * idade * idade;
            const ox = px + vx * (idade - 0.8), oy = py + vy * (idade - 0.8) + 1.6 * (idade - 0.8) ** 2;
            return { x, y, ox, oy, o: Math.max(0, 1 - idade / 13) };
          });
          const COR = "#e2701c";
          return (
            <g key={i}>
              <rect x={bx - 46} y={VIGA - 34} width={92} height={40} rx={6} fill="#2b2f35" />
              <line x1={bx} y1={VIGA} x2={jx} y2={jy} stroke={COR} strokeWidth={40} strokeLinecap="round" />
              <line x1={bx} y1={VIGA} x2={jx} y2={jy} stroke="#ffb06a" strokeOpacity={0.35} strokeWidth={8} strokeLinecap="round" transform="translate(-8,-6)" />
              <line x1={jx} y1={jy} x2={px} y2={py} stroke={COR} strokeWidth={30} strokeLinecap="round" />
              <circle cx={bx} cy={VIGA} r={28} fill="#3a3f46" stroke="#111" strokeWidth={4} />
              <circle cx={jx} cy={jy} r={22} fill="#3a3f46" stroke="#111" strokeWidth={4} />
              <circle cx={px} cy={py} r={12} fill="#cfd4da" />
              {soldando ? <>
                <circle cx={px} cy={py + 6} r={40} fill="#bfe3ff" opacity={0.55} filter="url(#lmGlow)" />
                <circle cx={px} cy={py + 6} r={9} fill="#ffffff" />
              </> : null}
              {fa.map((s, j) => <line key={j} x1={s.ox} y1={s.oy} x2={s.x} y2={s.y} stroke={j % 3 ? "#ffd27a" : "#ffffff"}
                strokeWidth={3} strokeLinecap="round" opacity={s.o} />)}
            </g>
          );
        })}
      </svg>
      {/* contador */}
      <div style={{ position: "absolute", left: 90, top: 70, right: 90 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ ...type.display, fontSize: 52, color: desc ? "#ff8a7a" : "#ffc266", letterSpacing: 5, textTransform: "uppercase",
            opacity: ent(f, 2), transform: `translateY(${(1 - ent(f, 2)) * 20}px)` }}>{p.titulo}</div>
          {p.status ? <div style={{ display: "flex", alignItems: "center", gap: 14, fontFamily: MONO, fontSize: 34, fontWeight: 700,
            color: "#e9ecf0", border: `2px solid ${LUZ}`, padding: "8px 20px", opacity: ent(f, 8) }}>
            <span style={{ width: 18, height: 18, borderRadius: 9, background: LUZ, boxShadow: `0 0 14px ${LUZ}`,
              opacity: f % 30 < 18 ? 1 : 0.3 }} />{p.status}</div> : null}
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 26, marginTop: 6, opacity: ent(f, 6) }}>
          <div style={{ ...type.display, fontSize: 190, lineHeight: 1, color: "#f4f6f8", fontVariantNumeric: "tabular-nums",
            textShadow: "0 10px 40px rgba(0,0,0,0.8)" }}>{milhar(num, p.sep)}</div>
          <div style={{ ...type.displayMedium, fontSize: 56, color: "#9aa2ad", textTransform: "uppercase", letterSpacing: 3 }}>{p.unidade}</div>
        </div>
        {p.sub ? <div style={{ fontFamily: MONO, fontSize: 36, fontWeight: 700, color: "#c9ced5", marginTop: 8, opacity: ent(f, 14) }}>{p.sub}</div> : null}
      </div>
      <AbsoluteFill style={{ boxShadow: "inset 0 0 240px rgba(0,0,0,0.9)" }} />
    </AbsoluteFill>
  );
};
