// CINCO ESTILOS DE CARTÃO POR GÊNERO (04/10/2026, pedido do usuário: "mais estilos que combinem com cada tipo de vídeo").
//   PlantaTecnica  — carros, motores, máquinas, navios, engenharia: planta azul com cotas e chamadas sobre a foto.
//   CadernoCampo   — arqueologia, Egito, pré-história, história antiga: página de caderno de escavação com foto colada.
//   PainelMercado  — economia, mercado de carros, agro, crises: terminal com gráfico desenhando e letreiro de cotação.
//   RadarTatico    — guerra, marinha, aviação, submarinos, resgate: visão noturna com alvos marcados + radar varrendo.
//   VhsRetro       — nostalgia, marcas antigas, propaganda dos anos 80-90: fita VHS com PLAY, data e slogan de comercial.
// Entram como cartão do DOSSIE (src/overlays/Arquivo.tsx), tomam o quadro inteiro por `fica` quadros. Todo número
// escrito neles tem de ser DITO na narração (regra do usuário).
import React from "react";
import { AbsoluteFill, Img, interpolate, random, spring, useCurrentFrame } from "remotion";
import { type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, FilmeVelho, MAO, Traco, clamp, src } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });

// ================================================================================================ PLANTA TÉCNICA
export type Cota = { x1: number; y1: number; x2: number; y2: number; rotulo: string };
export type Chamada = { x: number; y: number; rotulo: string };
export type PlantaProps = SceneProps & { src: string; titulo: string; cotas?: Cota[]; chamadas?: Chamada[]; folha?: string };
/** Foto vira planta: fundo azul quadriculado, foto em ciano, linhas de cota que se desenham e chamadas numeradas.
 *  x/y das cotas e chamadas em 0-1 dentro da foto. */
export const PlantaTecnica: React.FC<PlantaProps> = (p) => {
  const f = useCurrentFrame();
  const W = 1360, H = 765, X0 = (1920 - W) / 2, Y0 = 170;
  const P = (x: number, y: number) => [X0 + x * W, Y0 + y * H];
  const cotas = p.cotas ?? [];
  const cham = p.chamadas ?? [];
  const passo = Math.max(10, (p.dur * 0.5) / Math.max(1, cotas.length + cham.length));
  return (
    <AbsoluteFill style={{ background: "#0c2744", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.55, backgroundImage:
        "linear-gradient(rgba(140,190,255,0.16) 1px, transparent 1px), linear-gradient(90deg, rgba(140,190,255,0.16) 1px, transparent 1px)," +
        "linear-gradient(rgba(140,190,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(140,190,255,0.07) 1px, transparent 1px)",
        backgroundSize: "120px 120px, 120px 120px, 24px 24px, 24px 24px" }} />
      <div style={{ position: "absolute", left: X0, top: Y0, width: W, height: H, overflow: "hidden", opacity: ent(f, 0, 18),
        border: "2px solid rgba(200,225,255,0.85)" }}>
        <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover",
          filter: "grayscale(1) contrast(1.35) brightness(1.05)", transform: `scale(${interpolate(f, [0, p.dur], [1.04, 1.0], clamp)})` }} />
        <AbsoluteFill style={{ background: "#2f7dd6", mixBlendMode: "multiply", opacity: 0.85 }} />
        <AbsoluteFill style={{ background: "linear-gradient(transparent 50%, rgba(12,39,68,0.35))" }} />
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {cotas.map((c, i) => {
          const t0 = 20 + i * passo;
          const pr = ent(f, t0, t0 + 18);
          const [ax, ay] = P(c.x1, c.y1);
          const [bx, by] = P(c.x2, c.y2);
          const ang = Math.atan2(by - ay, bx - ax);
          const nx = -Math.sin(ang) * 12, ny = Math.cos(ang) * 12;
          return (
            <g key={`c${i}`}>
              <Traco d={`M${ax},${ay} L${bx},${by}`} p={pr} cor="#ffffff" w={3} />
              <Traco d={`M${ax - nx},${ay - ny} L${ax + nx},${ay + ny}`} p={pr * 3} cor="#ffffff" w={3} />
              <Traco d={`M${bx - nx},${by - ny} L${bx + nx},${by + ny}`} p={(pr - 0.66) * 3} cor="#ffffff" w={3} />
              <text x={(ax + bx) / 2 + nx * 2.2} y={(ay + by) / 2 + ny * 2.2 + 10} textAnchor="middle" fill="#ffffff"
                style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, opacity: ent(f, t0 + 12) }}>{c.rotulo}</text>
            </g>
          );
        })}
        {cham.map((c, i) => {
          const t0 = 20 + (cotas.length + i) * passo;
          const [x, y] = P(c.x, c.y);
          const lx = x + (c.x > 0.6 ? -220 : 220), ly = y - 120;
          const pr = ent(f, t0, t0 + 16);
          return (
            <g key={`h${i}`} style={{ opacity: ent(f, t0, t0 + 6) }}>
              <circle cx={x} cy={y} r={10 + 6 * Math.sin(f / 6)} fill="none" stroke="#ffd166" strokeWidth={3} />
              <Traco d={`M${x},${y} L${lx},${ly}`} p={pr} cor="#ffd166" w={2.5} />
              <circle cx={lx} cy={ly} r={24} fill="#ffd166" opacity={pr} />
              <text x={lx} y={ly + 10} textAnchor="middle" fill="#0c2744" style={{ fontFamily: MONO, fontSize: 28, fontWeight: 700, opacity: pr }}>{i + 1}</text>
              <text x={lx + (c.x > 0.6 ? -36 : 36)} y={ly + 10} textAnchor={c.x > 0.6 ? "end" : "start"} fill="#ffffff"
                style={{ fontFamily: MONO, fontSize: 30, fontWeight: 700, opacity: ent(f, t0 + 10) }}>{c.rotulo}</text>
            </g>
          );
        })}
      </svg>
      <div style={{ position: "absolute", left: X0, top: 70, ...type.display, fontSize: 58, color: "#e8f2ff", letterSpacing: 4,
        textTransform: "uppercase", opacity: ent(f, 4) }}>{p.titulo}</div>
      <div style={{ position: "absolute", right: X0, bottom: 52, fontFamily: MONO, fontSize: 24, color: "rgba(220,235,255,0.8)",
        border: "2px solid rgba(220,235,255,0.6)", padding: "8px 18px", letterSpacing: 3, opacity: ent(f, 10) }}>
        {p.folha ?? "PLANTA · FOLHA 01"}</div>
    </AbsoluteFill>
  );
};

// ================================================================================================ CADERNO DE CAMPO
export type CadernoProps = SceneProps & { src: string; titulo: string; local: string; data: string; notas?: string[];
  achado?: string; circulo?: { x: number; y: number; r?: number }; escala?: string };
/** Página de caderno de escavação: foto colada com fita, título e notas à mão, régua de escala e etiqueta do achado. */
export const CadernoCampo: React.FC<CadernoProps> = (p) => {
  const f = useCurrentFrame();
  const notas = p.notas ?? [];
  const g = spring({ frame: f - 2, fps: 30, config: { damping: 16, stiffness: 70 } });
  const FX = 150, FY = 190, FW = 960, FH = 620;
  const c = p.circulo;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #2a2117, #0c0906 80%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: 70, top: 50, width: 1780, height: 980, background: "#e6d9b8",
        boxShadow: "0 30px 80px rgba(0,0,0,0.7)", transform: `translateY(${(1 - g) * 60}px) rotate(-0.6deg)`,
        backgroundImage: "repeating-linear-gradient(transparent 0 46px, rgba(70,90,140,0.22) 46px 48px)" }}>
        <div style={{ position: "absolute", left: 1150, top: 0, bottom: 0, width: 3, background: "rgba(170,40,40,0.45)" }} />
        <div style={{ position: "absolute", left: FX, top: FY, width: FW, height: FH, background: "#f4efe2", padding: 14,
          boxSizing: "border-box", boxShadow: "0 6px 14px rgba(0,0,0,0.35)", transform: `rotate(${-2.2 * g}deg)`, opacity: ent(f, 4) }}>
          <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "sepia(0.35) contrast(1.05)" }} />
          {[[-30, -20, -35], [FW - 120, -18, 32], [-26, FH - 40, 28], [FW - 110, FH - 36, -30]].map(([x, y, r], i) => (
            <div key={i} style={{ position: "absolute", left: x, top: y, width: 150, height: 46, background: "rgba(235,225,180,0.75)",
              transform: `rotate(${r}deg)`, boxShadow: "0 1px 3px rgba(0,0,0,0.2)" }} />
          ))}
          {c ? (
            <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0 }}>
              <Traco d={`M${c.x * FW + (c.r ?? 0.12) * FW},${c.y * FH} a${(c.r ?? 0.12) * FW},${(c.r ?? 0.12) * FW * 0.8} 0 1,1 -2,-6`}
                p={ent(f, p.dur * 0.35, p.dur * 0.55)} cor="#b3261e" w={6} />
            </svg>
          ) : null}
        </div>
        <div style={{ position: "absolute", left: FX + 40, top: FY + FH + 40, display: "flex", alignItems: "center", gap: 0, opacity: ent(f, 20) }}>
          {Array.from({ length: 10 }, (_, i) => (
            <div key={i} style={{ width: 46, height: 18, background: i % 2 ? "#e6d9b8" : "#1d1812", border: "2px solid #1d1812" }} />
          ))}
          <div style={{ fontFamily: MONO, fontSize: 24, marginLeft: 16, color: "#1d1812" }}>{p.escala ?? "ESCALA"}</div>
        </div>
        <div style={{ position: "absolute", left: 1200, top: 120, right: 70, fontFamily: MAO, color: "#22304f" }}>
          <div style={{ fontSize: 56, lineHeight: 1.1, clipPath: `inset(0 ${100 - ent(f, 8, 40) * 100}% 0 0)` }}>{p.titulo}</div>
          <div style={{ fontSize: 30, marginTop: 18, opacity: ent(f, 30) }}>{p.local}</div>
          <div style={{ fontSize: 30, opacity: ent(f, 36) }}>{p.data}</div>
          {notas.map((n, i) => {
            const t0 = 50 + i * Math.max(14, (p.dur * 0.45) / Math.max(1, notas.length));
            return <div key={i} style={{ fontSize: 34, marginTop: 22, lineHeight: 1.2,
              clipPath: `inset(0 ${100 - ent(f, t0, t0 + 24) * 100}% 0 0)` }}>— {n}</div>;
          })}
        </div>
        {p.achado ? (
          <div style={{ position: "absolute", right: 120, bottom: 110, width: 360, padding: "22px 26px", background: "#d9c08a",
            borderRadius: "6px 30px 6px 6px", boxShadow: "0 8px 18px rgba(0,0,0,0.35)", transform: `rotate(${6 - 3 * ent(f, 60)}deg)`,
            opacity: ent(f, 60), fontFamily: MONO, fontSize: 30, fontWeight: 700, color: "#2b2114", letterSpacing: 2 }}>
            <div style={{ width: 22, height: 22, borderRadius: 11, background: "#e6d9b8", border: "2px solid #2b2114", marginBottom: 12 }} />
            {p.achado}
          </div>
        ) : null}
      </div>
      <FilmeVelho feixe={false} forca={0.55} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PAINEL DE MERCADO
export type MercadoProps = SceneProps & { titulo: string; serie: number[]; rotulos?: string[]; valor: string; variacao?: string;
  sobe?: boolean; ticker?: string[]; unidade?: string };
/** Terminal de mercado: valor grande, variação colorida, gráfico de linha se desenhando e letreiro de cotação correndo. */
export const PainelMercado: React.FC<MercadoProps> = (p) => {
  const f = useCurrentFrame();
  const cor = p.sobe === false ? "#ff5a4f" : p.sobe === true ? "#3ddc84" : "#f0b43c";
  const s = p.serie.length ? p.serie : [0, 1];
  const mn = Math.min(...s), mx = Math.max(...s);
  const GX = 140, GY = 330, GW = 1640, GH = 520;
  const pts = s.map((v, i) => [GX + (i / Math.max(1, s.length - 1)) * GW, GY + GH - ((v - mn) / Math.max(1e-9, mx - mn)) * GH * 0.86 - GH * 0.07]);
  const d = pts.map(([x, y], i) => `${i ? "L" : "M"}${x},${y}`).join(" ");
  const pr = ent(f, 18, Math.max(40, p.dur * 0.6));
  const vis = Math.max(1, Math.floor(pr * (pts.length - 1)) + 1);
  const ult = pts[Math.min(pts.length - 1, vis - 1)];
  const area = `${pts.slice(0, vis).map(([x, y], i) => `${i ? "L" : "M"}${x},${y}`).join(" ")} L${ult[0]},${GY + GH} L${GX},${GY + GH} Z`;
  const tk = (p.ticker ?? []).join("   ▪   ");
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #0a0e13, #05070a)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: GX, top: 70, ...type.display, fontSize: 40, color: "rgba(230,236,245,0.75)",
        letterSpacing: 5, textTransform: "uppercase", opacity: ent(f, 0) }}>{p.titulo}</div>
      <div style={{ position: "absolute", left: GX, top: 130, display: "flex", alignItems: "baseline", gap: 30, opacity: ent(f, 6) }}>
        <div style={{ ...type.display, fontSize: 130, color: "#f2f5f9", lineHeight: 1 }}>{p.valor}<span style={{ fontSize: 56,
          color: "rgba(230,236,245,0.6)", marginLeft: 12 }}>{p.unidade ?? ""}</span></div>
        {p.variacao ? <div style={{ fontFamily: MONO, fontSize: 48, fontWeight: 700, color: "#05070a", background: cor,
          padding: "6px 20px", borderRadius: 8 }}>{p.sobe === false ? "▼" : p.sobe === true ? "▲" : "●"} {p.variacao}</div> : null}
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs><linearGradient id="mgr" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={cor} stopOpacity={0.35} /><stop offset="1" stopColor={cor} stopOpacity={0} /></linearGradient></defs>
        {Array.from({ length: 5 }, (_, i) => <line key={i} x1={GX} x2={GX + GW} y1={GY + (i * GH) / 4} y2={GY + (i * GH) / 4}
          stroke="rgba(255,255,255,0.08)" strokeWidth={1} />)}
        <path d={area} fill="url(#mgr)" />
        <Traco d={d} p={pr} cor={cor} w={6} />
        <circle cx={ult[0]} cy={ult[1]} r={10 + 4 * Math.sin(f / 5)} fill={cor} />
        <circle cx={ult[0]} cy={ult[1]} r={22 + 10 * ((f % 30) / 30)} fill="none" stroke={cor} strokeOpacity={1 - (f % 30) / 30} strokeWidth={3} />
        {(p.rotulos ?? []).map((r, i) => {
          const idx = Math.round((i / Math.max(1, (p.rotulos ?? []).length - 1)) * (pts.length - 1));
          return <text key={i} x={pts[idx][0]} y={GY + GH + 50} textAnchor="middle" fill="rgba(230,236,245,0.6)"
            style={{ fontFamily: MONO, fontSize: 26 }}>{r}</text>;
        })}
      </svg>
      {tk ? (
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 86, background: "#f0b43c", overflow: "hidden" }}>
          <div style={{ position: "absolute", top: 20, left: 1920 - f * 9, whiteSpace: "nowrap", fontFamily: MONO, fontSize: 40,
            fontWeight: 700, color: "#0a0e13", letterSpacing: 2 }}>{`${tk}   ▪   ${tk}   ▪   ${tk}`}</div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ================================================================================================ RADAR TÁTICO
export type Alvo = { x: number; y: number; rotulo: string };
export type RadarProps = SceneProps & { src?: string; titulo: string; coord?: string; hora?: string; alvos?: Alvo[] };
/** Visão noturna da foto com alvos travados (colchetes) e um radar varrendo ao lado, com coordenada e hora. */
export const RadarTatico: React.FC<RadarProps> = (p) => {
  const f = useCurrentFrame();
  const alvos = p.alvos ?? [];
  const W = 1180, H = 860, X0 = 70, Y0 = 110;
  const RX = 1520, RY = 540, R = 300;
  const ang = (f * 4) % 360;
  const VERDE = "#7dff9a";
  return (
    <AbsoluteFill style={{ background: "#020604", ...exit(f, p.dur) }}>
      {p.src ? (
        <div style={{ position: "absolute", left: X0, top: Y0, width: W, height: H, overflow: "hidden", opacity: ent(f, 0, 10),
          border: `2px solid ${VERDE}55` }}>
          <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover",
            filter: "grayscale(1) contrast(1.4) brightness(1.15) sepia(1) hue-rotate(65deg) saturate(2.2)",
            transform: `scale(${interpolate(f, [0, p.dur], [1.0, 1.06], clamp)})` }} />
          <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.28) 0 2px, transparent 2px 4px)" }} />
          <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.75))" }} />
        </div>
      ) : null}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {alvos.map((a, i) => {
          const t0 = 18 + i * 22;
          const k = ent(f, t0, t0 + 12);
          const cx = X0 + a.x * W, cy = Y0 + a.y * H, s = 70 + (1 - k) * 90;
          const L = 24;
          return (
            <g key={i} opacity={k} stroke={VERDE} strokeWidth={4} fill="none">
              {[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([sx, sy], j) => (
                <path key={j} d={`M${cx + sx * s},${cy + sy * s - sy * L} L${cx + sx * s},${cy + sy * s} L${cx + sx * s - sx * L},${cy + sy * s}`} />
              ))}
              <text x={cx + s + 14} y={cy - s + 24} fill={VERDE} stroke="none" style={{ fontFamily: MONO, fontSize: 28, fontWeight: 700 }}>
                {`TGT-${String(i + 1).padStart(2, "0")}  ${a.rotulo}`}</text>
            </g>
          );
        })}
        <circle cx={RX} cy={RY} r={R} fill="rgba(20,60,30,0.35)" stroke={VERDE} strokeOpacity={0.6} strokeWidth={2} />
        {[0.33, 0.66].map((k) => <circle key={k} cx={RX} cy={RY} r={R * k} fill="none" stroke={VERDE} strokeOpacity={0.3} strokeWidth={1.5} />)}
        <line x1={RX - R} x2={RX + R} y1={RY} y2={RY} stroke={VERDE} strokeOpacity={0.25} />
        <line x1={RX} x2={RX} y1={RY - R} y2={RY + R} stroke={VERDE} strokeOpacity={0.25} />
        <path d={`M${RX},${RY} L${RX + R * Math.cos((ang * Math.PI) / 180)},${RY + R * Math.sin((ang * Math.PI) / 180)}
          A${R},${R} 0 0,0 ${RX + R * Math.cos(((ang - 40) * Math.PI) / 180)},${RY + R * Math.sin(((ang - 40) * Math.PI) / 180)} Z`}
          fill={VERDE} fillOpacity={0.22} />
        {alvos.map((a, i) => {
          const ba = (random(`b${i}`) * 360);
          const rr = R * (0.3 + random(`r${i}`) * 0.6);
          const diff = ((ang - ba) % 360 + 360) % 360;
          const brilho = diff < 120 ? 1 - diff / 120 : 0.15;
          return <circle key={i} cx={RX + rr * Math.cos((ba * Math.PI) / 180)} cy={RY + rr * Math.sin((ba * Math.PI) / 180)} r={10}
            fill={VERDE} opacity={brilho * ent(f, 18 + i * 22)} />;
        })}
      </svg>
      <div style={{ position: "absolute", left: X0, top: 40, fontFamily: MONO, fontSize: 34, fontWeight: 700, color: VERDE,
        letterSpacing: 4, opacity: ent(f, 0) }}>{p.titulo}</div>
      <div style={{ position: "absolute", left: RX - R, top: RY + R + 40, width: 2 * R, textAlign: "center", fontFamily: MONO,
        fontSize: 26, color: VERDE, lineHeight: 1.6, opacity: ent(f, 10) }}>
        {p.coord ? <div>{p.coord}</div> : null}
        {p.hora ? <div>{p.hora}</div> : null}
      </div>
      <div style={{ position: "absolute", right: 70, top: 44, fontFamily: MONO, fontSize: 26, color: VERDE, opacity: f % 30 < 18 ? 1 : 0.2 }}>● REC</div>
    </AbsoluteFill>
  );
};

// ================================================================================================ VHS RETRÔ
export type VhsProps = SceneProps & { src: string; data: string; slogan: string; marca?: string; hora?: string };
/** Fita VHS de comercial antigo: PLAY, faixa de tracking passando, cor vazando, data no canto e slogan cromado. */
export const VhsRetro: React.FC<VhsProps> = (p) => {
  const f = useCurrentFrame();
  const jit = (random(`j${f}`) - 0.5) * 4;
  const banda = ((f * 7) % 1400) - 200;
  const tremor = f < 10 ? (random(`t${f}`) - 0.5) * 40 : 0;
  const s = spring({ frame: f - 16, fps: 30, config: { damping: 12, stiffness: 120 } });
  return (
    <AbsoluteFill style={{ background: "#000", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `translateX(${jit + tremor}px)` }}>
        <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover",
          filter: "saturate(1.45) contrast(1.1) blur(0.6px)" }} />
        <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", mixBlendMode: "screen",
          opacity: 0.35, transform: "translateX(6px)", filter: "grayscale(1) sepia(1) hue-rotate(-50deg) saturate(6)" }} />
        <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", mixBlendMode: "screen",
          opacity: 0.3, transform: "translateX(-6px)", filter: "grayscale(1) sepia(1) hue-rotate(170deg) saturate(6)" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.25) 0 2px, transparent 2px 4px)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: banda, height: 70, background:
        "linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0.18), rgba(255,255,255,0))", filter: "blur(2px)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 58%, rgba(0,0,0,0.85))", borderRadius: 40 }} />
      <div style={{ position: "absolute", left: 90, top: 70, fontFamily: MONO, fontSize: 52, fontWeight: 700, color: "#fff",
        textShadow: "3px 3px 0 #000", opacity: f % 40 < 30 ? 1 : 0.4 }}>PLAY ▶</div>
      {p.marca ? <div style={{ position: "absolute", right: 90, top: 70, fontFamily: MONO, fontSize: 40, color: "#fff",
        textShadow: "3px 3px 0 #000" }}>{p.marca}</div> : null}
      <div style={{ position: "absolute", right: 90, bottom: 80, fontFamily: MONO, fontSize: 46, fontWeight: 700, color: "#fff",
        textShadow: "3px 3px 0 #000", textAlign: "right", lineHeight: 1.25 }}>
        <div>{p.hora ?? "AM 10:42"}</div><div>{p.data}</div></div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center", transform: `scale(${0.6 + 0.4 * s}) skewX(-8deg)`,
        opacity: ent(f, 16, 26) }}>
        <span style={{ ...type.display, fontSize: p.slogan.length > 22 ? 110 : 150, letterSpacing: 4, textTransform: "uppercase",
          background: "linear-gradient(180deg, #ffffff 0%, #9fd8ff 45%, #2b5fa8 50%, #ffffff 100%)", WebkitBackgroundClip: "text",
          color: "transparent", WebkitTextStroke: "3px #10224a", filter: "drop-shadow(0 8px 0 #e83f8a)" }}>{p.slogan}</span>
      </div>
    </AbsoluteFill>
  );
};
