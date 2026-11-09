// SEIS CARTÕES DE ARQUEOLOGIA / HISTÓRIA ANTIGA (04/10/2026) — Egito, múmias, pré-história, paleoforense (canais ES/PT).
//   Estratigrafia        — corte do solo: camadas se desenham de cima para baixo, régua lateral com rótulo e data, achado destacado
//   Papiro               — folha de papiro desenrolando; texto original em glifos se revela, tradução datilografada embaixo
//   EtiquetaMuseu        — vitrine de museu: foto sob spot em veludo preto, reflexo do vidro e etiqueta elegante
//   DatacaoCarbono       — laudo de radiocarbono: curva de decaimento do C-14, ponto deslizando, contador de anos ± margem
//   Escaneamento3D       — varredura 3D: nuvem de pontos e malha varrendo a foto, pontos medidos, HUD científico
//   QuadriculaEscavacao  — quadrícula de escavação vista de cima (A–F / 1–6), quadras com achados acendem, norte e escala
// Mesma convenção de estilos5.tsx: tomam o quadro inteiro, vivem ~150 quadros, entram nos primeiros ~20 e estão legíveis
// até o quadro ~45. Todo texto vem das props (todo número escrito tem de ser DITO na narração).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, spring, useCurrentFrame } from "remotion";
import { fmtEs, type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, Traco, clamp, src } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const SANS = "'IBM Plex Sans', 'Segoe UI', sans-serif";
const SERIFA = "'Palatino Linotype', 'Book Antiqua', Georgia, serif";
const GLIFO = "'Segoe UI Historic', 'Palatino Linotype', Georgia, serif";   // Segoe UI Historic tem hieróglifos egípcios
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });
const suave = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
const chars = (s: string) => Array.from(s);

/** Grão fino (sem vinheta nem poeira — acabamento limpo, não de arquivo velho). */
const Grao: React.FC<{ o?: number; id: string }> = ({ o = 0.1, id }) => {
  const f = useCurrentFrame();
  const fid = `${id}${f % 4}`;
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, opacity: o, mixBlendMode: "overlay", pointerEvents: "none" }}>
      <filter id={fid}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f % 53} /></filter>
      <rect width="100%" height="100%" filter={`url(#${fid})`} />
    </svg>
  );
};

// ================================================================================================ ESTRATIGRAFIA
export type Camada = { rotulo: string; data: string };
export type EstratigrafiaProps = SceneProps & { titulo: string; camadas: Camada[]; achado: string; nivel: number };
const CORES_SOLO = ["#3f2c1f", "#8d6c45", "#9a5232", "#6c6457", "#b39560", "#56402e", "#7a6a50"];
/** Corte estratigráfico: camadas desenham de cima para baixo, régua com rótulo/data de cada camada, achado aceso na camada `nivel`. */
export const Estratigrafia: React.FC<EstratigrafiaProps> = (p) => {
  const f = useCurrentFrame();
  const cam = p.camadas.length ? p.camadas : [{ rotulo: "", data: "" }];
  const n = cam.length;
  const nivel = Math.max(0, Math.min(n - 1, Math.round(p.nivel)));
  const X0 = 150, Y0 = 215, W = 940, H = 765, RX = X0 + W + 46, LX = RX + 44, LW = 1830 - LX;
  const pesos = cam.map((_, i) => 0.85 + random(`pe${i}`) * 0.3);
  const soma = pesos.reduce((a, b) => a + b, 0);
  const lim: number[] = [Y0];
  pesos.forEach((w) => lim.push(lim[lim.length - 1] + (w / soma) * H));
  const onda = (i: number, x: number) => (i === 0 || i === n ? 0 : 10 * Math.sin(x / 130 + i * 1.7) + 4 * Math.sin(x / 41 + i * 3.1));
  const borda = (i: number) => Array.from({ length: 49 }, (_, k) => { const x = X0 + (k / 48) * W; return [x, lim[i] + onda(i, x)]; });
  const poly = (i: number) => `M${[...borda(i), ...borda(i + 1).reverse()].map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" L")} Z`;
  const rv = suave(f, 3, 30);
  const frente = Y0 + H * rv;
  const hl = ent(f, 28, 40);
  const yc = cam.map((_, i) => (lim[i] + lim[i + 1]) / 2);
  // rótulos: altura estimada e afastamento mínimo para nunca sobrepor
  const alt = cam.map((c) => 56 + 44 * Math.max(1, Math.ceil(c.rotulo.length / 32)));
  const yl = [...yc];
  for (let i = 1; i < n; i++) yl[i] = Math.max(yl[i], yl[i - 1] + (alt[i - 1] + alt[i]) / 2 + 6);
  const exced = yl[n - 1] + alt[n - 1] / 2 - (Y0 + H + 10);
  if (exced > 0) for (let i = n - 1; i >= 0; i--) { yl[i] -= exced; if (i > 0) yl[i - 1] = Math.min(yl[i - 1], yl[i] - (alt[i - 1] + alt[i]) / 2 - 6); }
  const mx = X0 + W * 0.66, my = yc[nivel];
  const cardY = Math.max(Y0 + 80, Math.min(Y0 + H - 80, my));
  const cardP = ent(f, 32, 46);
  const pulso = f > 30 ? ((f - 30) % 34) / 34 : 0;
  const textura = (i: number) => {
    const t = i % 4, top = lim[i] - 14, alto = lim[i + 1] - lim[i] + 28;
    const R = (k: number, s: string) => random(`${s}${i}-${k}`);
    if (t === 0) return Array.from({ length: 160 }, (_, k) => <circle key={k} cx={X0 + R(k, "a") * W} cy={top + R(k, "b") * alto}
      r={0.8 + R(k, "c") * 2} fill={R(k, "d") > 0.5 ? "#000" : "#f3d9a8"} opacity={0.28} />);
    if (t === 1) return Array.from({ length: 30 }, (_, k) => <ellipse key={k} cx={X0 + R(k, "a") * W} cy={top + R(k, "b") * alto}
      rx={6 + R(k, "c") * 13} ry={4 + R(k, "e") * 8} fill={R(k, "d") > 0.5 ? "#d9c39a" : "#2a1d13"} opacity={0.42}
      stroke="rgba(0,0,0,0.35)" strokeWidth={1.5} transform={`rotate(${R(k, "r") * 40 - 20} ${X0 + R(k, "a") * W} ${top + R(k, "b") * alto})`} />);
    if (t === 2) return Array.from({ length: 9 }, (_, k) => {
      const y = top + 14 + ((k + 0.5) / 9) * (alto - 28);
      return <path key={k} d={`M${X0},${y} ${Array.from({ length: 25 }, (_, j) => `L${X0 + (j / 24) * W},${y + 3 * Math.sin(j * 0.9 + k)}`).join(" ")}`}
        stroke={k % 2 ? "rgba(0,0,0,0.30)" : "rgba(255,230,190,0.22)"} strokeWidth={2} fill="none" />;
    });
    return Array.from({ length: 90 }, (_, k) => <circle key={k} cx={X0 + R(k, "a") * W} cy={top + R(k, "b") * alto}
      r={2 + R(k, "c") * 4.5} fill={R(k, "d") > 0.4 ? "#1e1610" : "#cdbb9a"} opacity={0.4} />);
  };
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 40% 50%, #2a1e14, #0e0a07 75%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: X0, top: 92, ...type.display, fontSize: 62, color: "#f3e7cf", letterSpacing: 3,
        textTransform: "uppercase", opacity: ent(f, 0), transform: `translateY(${(1 - ent(f, 0)) * 20}px)`, maxWidth: 1620,
        whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{p.titulo}</div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <clipPath id="est-rv"><rect x={0} y={0} width={1920} height={frente} /></clipPath>
          {cam.map((_, i) => <clipPath key={i} id={`est-l${i}`}><path d={poly(i)} /></clipPath>)}
          <linearGradient id="est-luz" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ffe9c4" stopOpacity={0.16} /><stop offset="0.5" stopColor="#000" stopOpacity={0} />
            <stop offset="1" stopColor="#000" stopOpacity={0.45} /></linearGradient>
          <filter id="est-solo" x="0" y="0" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.018 0.07" numOctaves={4} seed={11} />
            <feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.42  0 0 0 0 0.32  1.2 0 0 0 -0.35" /></filter>
          <linearGradient id="est-fr" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#ffd28a" stopOpacity={0} /><stop offset="1" stopColor="#ffd28a" stopOpacity={0.55} /></linearGradient>
        </defs>
        <rect x={X0 - 8} y={Y0 - 8} width={W + 16} height={H + 16} fill="#0a0705" opacity={0.7 * ent(f, 0, 8)} />
        <g clipPath="url(#est-rv)">
          {cam.map((_, i) => (
            <g key={i}>
              <path d={poly(i)} fill={CORES_SOLO[i % CORES_SOLO.length]} />
              <g clipPath={`url(#est-l${i})`}>{textura(i)}</g>
              {i !== nivel ? <path d={poly(i)} fill="#000" opacity={0.34 * hl} /> : null}
              {i > 0 ? <path d={`M${borda(i).map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" L")}`} stroke="rgba(0,0,0,0.5)" strokeWidth={2.5} fill="none" /> : null}
            </g>
          ))}
          <rect x={X0} y={Y0} width={W} height={H} filter="url(#est-solo)" opacity={0.55} style={{ mixBlendMode: "overlay" }} />
          <rect x={X0} y={Y0} width={W} height={H} fill="url(#est-luz)" />
          <path d={poly(nivel)} fill="rgba(255,210,130,0.20)" stroke="#f2c46b" strokeWidth={3.5} strokeDasharray="14 9" opacity={hl} />
          {/* régua */}
          <line x1={RX} x2={RX} y1={Y0} y2={Y0 + H} stroke="#d9c7a6" strokeWidth={3} />
          {Array.from({ length: 31 }, (_, k) => (
            <line key={k} x1={RX - (k % 5 === 0 ? 22 : 11)} x2={RX} y1={Y0 + (k / 30) * H} y2={Y0 + (k / 30) * H}
              stroke="#d9c7a6" strokeWidth={k % 5 === 0 ? 3 : 1.5} />
          ))}
        </g>
        {rv > 0.01 && rv < 0.99 ? <rect x={X0} y={frente - 50} width={W} height={50} fill="url(#est-fr)" /> : null}
        {/* fios até os rótulos */}
        {cam.map((_, i) => {
          const o = interpolate(frente - yc[i], [0, 40], [0, 1], clamp);
          const ativo = i === nivel ? hl : 0;
          return (
            <g key={i} opacity={o}>
              <circle cx={RX} cy={yc[i]} r={6 + 3 * ativo} fill={ativo > 0.5 ? "#f2c46b" : "#d9c7a6"} />
              <path d={`M${RX + 6},${yc[i]} L${RX + 20},${yc[i]} L${LX - 16},${yl[i]}`} stroke={ativo > 0.5 ? "#f2c46b" : "rgba(217,199,166,0.6)"}
                strokeWidth={2} fill="none" />
            </g>
          );
        })}
        {/* achado */}
        <g opacity={hl}>
          <circle cx={mx} cy={my} r={44 + pulso * 56} fill="none" stroke="#f2c46b" strokeWidth={3} opacity={1 - pulso} />
          <g transform={`translate(${mx} ${my}) scale(${0.85 + 0.55 * hl}) rotate(-12)`} style={{ filter: "drop-shadow(0 0 12px rgba(242,196,107,0.8))" }}>
            <path d="M-34,-6 L-20,-22 L6,-26 L30,-14 L36,6 L20,22 L-8,24 L-30,14 Z" fill="#e2b14c" stroke="#3a250c" strokeWidth={3} />
            <path d="M-18,-6 L14,-12 M-14,8 L18,4" stroke="#7a521b" strokeWidth={3} />
          </g>
          <Traco d={`M${X0 + 470},${cardY} L${mx - 110},${cardY} L${mx - 58},${my}`} p={cardP} cor="#f2c46b" w={3} />
        </g>
      </svg>
      {/* cartão do achado */}
      <div style={{ position: "absolute", left: X0 + 40, top: cardY, width: 430, transform: `translateY(-50%) translateX(${(1 - cardP) * -30}px)`,
        opacity: cardP, background: "rgba(14,10,6,0.9)", borderLeft: "6px solid #f2c46b", padding: "20px 26px", boxSizing: "border-box",
        boxShadow: "0 18px 40px rgba(0,0,0,0.55)", ...type.display, fontSize: 40, lineHeight: 1.15, color: "#fff6e4" }}>{p.achado}</div>
      {/* rótulos da régua */}
      {cam.map((c, i) => {
        const o = interpolate(frente - yc[i], [0, 40], [0, 1], clamp);
        const ativo = i === nivel;
        return (
          <div key={i} style={{ position: "absolute", left: LX, top: yl[i], width: LW, transform: `translateY(-50%) translateX(${(1 - o) * 20}px)`,
            opacity: o }}>
            <div style={{ ...type.display, fontSize: 44, lineHeight: 1.15, color: ativo && hl > 0.5 ? "#f2c46b" : "#f3e3c3", letterSpacing: 1 }}>{c.data}</div>
            <div style={{ fontFamily: SANS, fontSize: 34, lineHeight: 1.25, color: ativo && hl > 0.5 ? "#f6e6c8" : "#b9a88d" }}>{c.rotulo}</div>
          </div>
        );
      })}
      <Grao id="est-g" o={0.12} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PAPIRO
export type PapiroProps = SceneProps & { original: string; traducao: string; fonte?: string };
/** Papiro desenrolando: texto original em glifos revela da esquerda para a direita, depois a tradução é datilografada embaixo. */
export const Papiro: React.FC<PapiroProps> = (p) => {
  const f = useCurrentFrame();
  const SX = 170, SY = 180, SW = 1540, SH = 500;
  const u = interpolate(f, [0, 20], [0.05, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const orig = chars(p.original);
  // tamanho que cabe na folha (hieróglifos têm avanço ~0,55 em; letras ~0,6 em; + espaçamento 0,14 em)
  const hier = orig.some((c) => { const cp = c.codePointAt(0) ?? 0; return cp >= 0x13000 && cp <= 0x1345f; });
  const av = (hier ? 0.55 : 0.6) + 0.14;
  let fs = hier ? 150 : 112;
  while (fs > 50 && Math.ceil((orig.length * av * fs) / 1300) * 1.3 * fs > SH - 120) fs -= 2;
  const rev = interpolate(f, [12, 34], [-8, 108], clamp);
  const trad = chars(p.traducao);
  const nT = Math.floor(interpolate(f, [28, 47], [0, trad.length], clamp));
  const tfs = trad.length > 120 ? 42 : trad.length > 70 ? 48 : 54;
  const borda = (s: string, base: number, sinal: number) =>
    Array.from({ length: 41 }, (_, k) => `${(k / 40) * 100}% ${base + sinal * random(`${s}${k}`) * 1.8}%`);
  const clip = `polygon(${[...borda("pt", 0.4, 1), ...borda("pb", 99.6, -1).reverse()].join(", ")})`;
  const manchas = [[22, 30, 180], [64, 70, 220], [85, 22, 140], [40, 82, 160]];
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 34%, #3b2a17 0%, #120c07 62%, #070504 100%)", ...exit(f, p.dur) }}>
      {/* folha */}
      <div style={{ position: "absolute", left: SX, top: SY, width: SW * u, height: SH, overflow: "hidden", opacity: ent(f, 0, 6),
        filter: "drop-shadow(0 30px 34px rgba(0,0,0,0.7))" }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: SW, height: SH, clipPath: clip, background: "#d6b97e",
          backgroundImage: [
            ...manchas.map(([x, y, r]) => `radial-gradient(circle ${r}px at ${x}% ${y}%, rgba(120,76,28,0.22), transparent)`),
          ].join(", "), boxShadow: "inset 0 0 90px rgba(80,44,10,0.65)" }}>
          <svg width={SW} height={SH} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply" }}>
            <filter id="pap-fv" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.22 0.004" numOctaves={3} seed={3} />
              <feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.29  0 0 0 0 0.12  1.6 0 0 0 -0.55" /></filter>
            <filter id="pap-fh" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.003 0.16" numOctaves={3} seed={8} />
              <feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.33  0 0 0 0 0.14  1.4 0 0 0 -0.5" /></filter>
            <rect width={SW} height={SH} filter="url(#pap-fv)" opacity={0.75} />
            <rect width={SW} height={SH} filter="url(#pap-fh)" opacity={0.5} />
          </svg>
          {[0.26, 0.52, 0.78].map((k) => <div key={k} style={{ position: "absolute", left: SW * k, top: 0, bottom: 0, width: 5,
            background: "linear-gradient(90deg, rgba(90,56,18,0.25), rgba(255,235,195,0.2), rgba(90,56,18,0.18))" }} />)}
          <AbsoluteFill style={{ background: "radial-gradient(ellipse at 42% 32%, rgba(255,244,214,0.28), transparent 62%)" }} />
          <div style={{ position: "absolute", left: 90, right: 90, top: 50, bottom: 50, display: "flex", alignItems: "center",
            justifyContent: "center", textAlign: "center",
            maskImage: `linear-gradient(90deg, #000 ${rev - 7}%, transparent ${rev + 7}%)`,
            WebkitMaskImage: `linear-gradient(90deg, #000 ${rev - 7}%, transparent ${rev + 7}%)` }}>
            <div style={{ fontFamily: GLIFO, fontSize: fs, lineHeight: 1.3, letterSpacing: "0.14em", color: "rgba(34,18,5,0.9)", filter: "url(#pap-tinta)",
              WebkitTextStroke: hier ? "1.2px rgba(34,18,5,0.85)" : undefined, textShadow: "0 0 2px rgba(34,18,5,0.4)",
              mixBlendMode: "multiply" }}>{p.original}</div>
          </div>
        </div>
      </div>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id="pap-tinta"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves={2} seed={5} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale={6} xChannelSelector="R" yChannelSelector="G" /></filter>
      </svg>
      {/* rolo */}
      <div style={{ position: "absolute", left: SX + SW * u - 14, top: SY - 18, width: 46, height: SH + 36, borderRadius: 23,
        opacity: ent(f, 0, 6), background: "linear-gradient(90deg, #4e3416, #a98349 22%, #efd9a6 48%, #b48f55 70%, #3f2a11)",
        boxShadow: "8px 18px 30px rgba(0,0,0,0.6)" }} />
      {/* tradução + fonte */}
      <div style={{ position: "absolute", left: SX, width: SW, top: SY + SH + 56, display: "flex", flexDirection: "column", alignItems: "center", gap: 34 }}>
        <div style={{ textAlign: "center", fontFamily: SERIFA, fontStyle: "italic", fontSize: tfs, lineHeight: 1.32, color: "#f1e4c6",
          opacity: ent(f, 26, 30) }}>
          <span>“{trad.slice(0, nT).join("")}</span>
          <span style={{ display: "inline-block", width: 3, height: tfs * 0.9, background: "#e0b866", verticalAlign: "-0.12em",
            marginLeft: 2, opacity: nT < trad.length ? (f % 10 < 6 ? 1 : 0) : 0 }} />
          <span style={{ color: "transparent" }}>{trad.slice(nT).join("")}</span>
          <span style={{ opacity: nT >= trad.length ? 1 : 0 }}>”</span>
        </div>
        {p.fonte ? (
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 22, fontFamily: MONO, fontSize: 34, letterSpacing: 4,
            color: "#c9a45c", opacity: ent(f, 40) }}>
            <div style={{ width: 60, height: 2, background: "#c9a45c" }} />{p.fonte}<div style={{ width: 60, height: 2, background: "#c9a45c" }} />
          </div>
        ) : null}
      </div>
      <Grao id="pap-g" o={0.13} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ETIQUETA DE MUSEU
export type EtiquetaMuseuProps = SceneProps & { src: string; nome: string; material: string; data: string; inventario?: string; museu?: string };
/** Vitrine de museu: foto sob spot em veludo preto, reflexo do vidro passando e etiqueta de museu ao lado. */
export const EtiquetaMuseu: React.FC<EtiquetaMuseuProps> = (p) => {
  const f = useCurrentFrame();
  const PX = 220, PY = 130, PS = 740;
  const luz = f < 3 ? 0 : f < 5 ? 0.6 : f < 7 ? 0.25 : ent(f, 7, 22);
  const card = ent(f, 10, 26);
  const reflexo = interpolate(f, [8, p.dur], [-700, 1500], clamp);
  const push = interpolate(f, [0, p.dur], [1.0, 1.04], clamp);
  const nomeFs = p.nome.length > 44 ? 46 : p.nome.length > 26 ? 52 : 60;
  return (
    <AbsoluteFill style={{ background: "#08070a", ...exit(f, p.dur) }}>
      {/* veludo */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 35% 45%, #1a1418, #070609 70%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.22 }}>
        <filter id="mus-vel"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves={1} seed={7} />
          <feColorMatrix values="0 0 0 0 0.20  0 0 0 0 0.14  0 0 0 0 0.18  0 0 0 0.8 0" /></filter>
        <rect width="100%" height="100%" filter="url(#mus-vel)" />
      </svg>
      {/* cone de luz */}
      <AbsoluteFill style={{ opacity: luz, background: "radial-gradient(ellipse 760px 620px at 590px 520px, rgba(255,232,190,0.20), transparent 72%)" }} />
      <AbsoluteFill style={{ opacity: luz, mixBlendMode: "screen",
        background: "radial-gradient(ellipse 420px 980px at 590px 140px, rgba(255,236,200,0.11), transparent 70%)" }} />
      {/* objeto */}
      <div style={{ position: "absolute", left: PX, top: PY, width: PS, height: PS, opacity: luz, transform: `scale(${push})`,
        maskImage: "radial-gradient(ellipse 52% 52% at 50% 48%, #000 62%, transparent 100%)",
        WebkitMaskImage: "radial-gradient(ellipse 52% 52% at 50% 48%, #000 62%, transparent 100%)" }}>
        <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "sepia(0.3) contrast(1.12) brightness(1.02)" }} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 45% 30%, rgba(255,236,200,0.18), transparent 55%, rgba(0,0,0,0.45))" }} />
      </div>
      {/* prateleira de vidro + reflexo */}
      <div style={{ position: "absolute", left: 140, width: 900, top: PY + PS + 6, height: 2, opacity: 0.5 * luz,
        background: "linear-gradient(90deg, transparent, rgba(255,240,215,0.7), transparent)" }} />
      <div style={{ position: "absolute", left: PX, top: PY + PS + 10, width: PS, height: 150, overflow: "hidden", opacity: 0.16 * luz,
        maskImage: "linear-gradient(#000, transparent)", WebkitMaskImage: "linear-gradient(#000, transparent)" }}>
        <Img src={src(p.src)} style={{ width: PS, height: PS, objectFit: "cover", transform: "scaleY(-1)", filter: "sepia(0.3) blur(2px)" }} />
      </div>
      {/* etiqueta */}
      <div style={{ position: "absolute", left: 1110, top: 130, width: 680, height: 820, display: "flex", alignItems: "center", perspective: 1600 }}>
        <div style={{ width: "100%", background: "linear-gradient(160deg, #f4eee2, #e6dcc8)", padding: "46px 52px", boxSizing: "border-box",
          boxShadow: "0 30px 70px rgba(0,0,0,0.75), inset 0 0 0 1px rgba(120,100,60,0.25)", opacity: card,
          transform: `translateX(${(1 - card) * 70}px) rotateY(${-7 * card}deg)`, color: "#1f1a14" }}>
          {p.inventario ? <div style={{ fontFamily: MONO, fontSize: 34, letterSpacing: 3, color: "#7a6a52", marginBottom: 18 }}>{p.inventario}</div> : null}
          <div style={{ fontFamily: SERIFA, fontSize: nomeFs, lineHeight: 1.12, fontVariant: "small-caps", letterSpacing: 1 }}>{p.nome}</div>
          <div style={{ width: 90, height: 3, background: "#a8874a", margin: "28px 0 24px" }} />
          <div style={{ fontFamily: SERIFA, fontStyle: "italic", fontSize: 38, lineHeight: 1.25, color: "#3a332a" }}>{p.material}</div>
          <div style={{ fontFamily: SERIFA, fontSize: 38, lineHeight: 1.25, color: "#3a332a", marginTop: 8 }}>{p.data}</div>
          {p.museu ? <div style={{ fontFamily: SANS, fontSize: 34, letterSpacing: 3, textTransform: "uppercase", color: "#6d604d",
            borderTop: "1px solid rgba(110,95,70,0.45)", marginTop: 30, paddingTop: 20 }}>{p.museu}</div> : null}
        </div>
      </div>
      {/* vidro da vitrine */}
      <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen", background:
        `linear-gradient(112deg, transparent ${reflexo - 160}px, rgba(255,255,255,0.07) ${reflexo - 40}px, rgba(255,255,255,0.13) ${reflexo}px, transparent ${reflexo + 40}px, transparent ${reflexo + 120}px, rgba(255,255,255,0.06) ${reflexo + 150}px, transparent ${reflexo + 200}px)` }} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 40, height: 3, opacity: luz,
        background: "linear-gradient(90deg, transparent, rgba(255,240,215,0.55), transparent)", boxShadow: "0 0 24px rgba(255,236,200,0.4)" }} />
      <div style={{ position: "absolute", left: 60, right: 60, top: 40, bottom: 40, border: "1px solid rgba(255,255,255,0.07)", opacity: luz }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(0,0,0,0.6))" }} />
      <Grao id="mus-g" o={0.08} />
    </AbsoluteFill>
  );
};

// ================================================================================================ DATAÇÃO POR CARBONO
export type DatacaoCarbonoProps = SceneProps & { titulo: string; anos: number; margem?: number; amostra: string; laboratorio?: string;
  unidade?: string };
const MEIA_VIDA = 5730;
/** Laudo de radiocarbono: curva de decaimento do ¹⁴C se desenha, ponto desliza até a idade enquanto o contador sobe; ± margem. */
export const DatacaoCarbono: React.FC<DatacaoCarbonoProps> = (p) => {
  const f = useCurrentFrame();
  const folha = spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 90 } });
  const SX = 140, SY = 96, SW = 1640, SH = 890;
  const GX = 210, GY = 300, GW = 920, GH = 600;
  const tMax = Math.max(p.anos * 1.5, MEIA_VIDA * 2);
  const N = (t: number) => Math.exp((-Math.LN2 * t) / MEIA_VIDA);
  const px = (t: number) => GX + 14 + (t / tMax) * (GW - 40);
  const py = (n: number) => GY + 30 + (1 - n) * (GH - 50);
  const curva = `M${Array.from({ length: 61 }, (_, k) => { const t = (k / 60) * tMax; return `${px(t).toFixed(1)},${py(N(t)).toFixed(1)}`; }).join(" L")}`;
  const cv = suave(f, 8, 30);
  const k = interpolate(f, [16, 44], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const t = p.anos * k;
  const ptx = px(t), pty = py(N(t));
  const banda = ent(f, 42, 54);
  const mg = p.margem ?? 0;
  const bx0 = px(Math.max(0, p.anos - mg)), bx1 = px(p.anos + mg);
  const num = fmtEs(t);
  const numFs = Math.min(176, 520 / Math.max(3, fmtEs(p.anos).length * 0.5));
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #1d252d, #090c10 75%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, background: "#f5f3ee",
        boxShadow: "0 40px 90px rgba(0,0,0,0.7)", opacity: ent(f, 0, 8), transform: `translateY(${(1 - folha) * 80}px) rotate(-0.35deg)` }}>
        <AbsoluteFill style={{ background: "linear-gradient(170deg, rgba(255,255,255,0.5), transparent 40%, rgba(0,0,0,0.06))" }} />
        {/* cabeçalho */}
        <div style={{ position: "absolute", left: 70, right: 70, top: 56, display: "flex", justifyContent: "space-between", alignItems: "baseline",
          gap: 40, opacity: ent(f, 4) }}>
          <div style={{ ...type.display, fontSize: 42, letterSpacing: 4, textTransform: "uppercase", color: "#18222d", whiteSpace: "nowrap",
            overflow: "hidden", textOverflow: "ellipsis" }}>{p.laboratorio ?? ""}</div>
          <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: "#3c4650", whiteSpace: "nowrap" }}>{p.amostra}</div>
        </div>
        <div style={{ position: "absolute", left: 70, right: 70, top: 124, height: 3, background: "#18222d", transformOrigin: "0 0",
          transform: `scaleX(${ent(f, 2, 20)})` }} />
        <div style={{ position: "absolute", left: 70, right: 70, top: 132, height: 1, background: "#18222d", transformOrigin: "0 0",
          transform: `scaleX(${ent(f, 4, 22)})` }} />
        {/* gráfico: coordenadas de tela, deslocado para dentro da folha (herda a rotação) */}
      <svg width={1920} height={1080} style={{ position: "absolute", left: -SX, top: -SY, opacity: ent(f, 4, 16) }}>
        <defs>
          <pattern id="c14-mm" width={20} height={20} patternUnits="userSpaceOnUse" x={GX} y={GY}>
            <path d="M20,0 L0,0 L0,20" fill="none" stroke="rgba(60,130,90,0.20)" strokeWidth={1} /></pattern>
          <pattern id="c14-cm" width={100} height={100} patternUnits="userSpaceOnUse" x={GX} y={GY}>
            <path d="M100,0 L0,0 L0,100" fill="none" stroke="rgba(60,130,90,0.42)" strokeWidth={1.5} /></pattern>
        </defs>
        <rect x={GX} y={GY} width={GW} height={GH} fill="#eef3ea" />
        <rect x={GX} y={GY} width={GW} height={GH} fill="url(#c14-mm)" />
        <rect x={GX} y={GY} width={GW} height={GH} fill="url(#c14-cm)" />
        <line x1={GX + 14} y1={GY + 10} x2={GX + 14} y2={GY + GH - 20} stroke="#18222d" strokeWidth={3} />
        <line x1={GX + 14} y1={GY + GH - 20} x2={GX + GW - 10} y2={GY + GH - 20} stroke="#18222d" strokeWidth={3} />
        {mg ? <rect x={bx0 - 4} y={GY + 10} width={Math.max(8, bx1 - bx0 + 8)} height={GH - 30} fill="#b3261e" opacity={0.16 * banda} /> : null}
        <Traco d={curva} p={cv} cor="#b3261e" w={5} />
        {k > 0 ? (
          <g>
            <line x1={ptx} y1={pty} x2={ptx} y2={GY + GH - 20} stroke="#18222d" strokeWidth={2} strokeDasharray="8 7" />
            <line x1={GX + 14} y1={pty} x2={ptx} y2={pty} stroke="#18222d" strokeWidth={2} strokeDasharray="8 7" />
            <circle cx={ptx} cy={pty} r={13} fill="#0f151b" />
            <circle cx={ptx} cy={pty} r={22 + 8 * Math.sin(f / 5)} fill="none" stroke="#b3261e" strokeWidth={3} />
          </g>
        ) : null}
        <text x={GX + 4} y={GY - 16} fill="#18222d" style={{ fontFamily: MONO, fontSize: 36, fontWeight: 700 }}>¹⁴C</text>
        {/* código de barras do rodapé */}
        {Array.from({ length: 46 }, (_, i) => (
          <rect key={i} x={1360 + i * 8} y={905} width={random(`bc${i}`) > 0.5 ? 4 : 2} height={50} fill="#18222d" opacity={ent(f, 12)} />
        ))}
      </svg>
        {/* coluna do resultado */}
        <div style={{ position: "absolute", left: 1050, right: 70, top: 190, opacity: ent(f, 8) }}>
          <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 40, lineHeight: 1.2, color: "#18222d" }}>{p.titulo}</div>
          <div style={{ marginTop: 34, borderTop: "2px solid #18222d", borderBottom: "2px solid #18222d", padding: "20px 0 26px" }}>
            <div style={{ ...type.display, fontSize: numFs, lineHeight: 1, color: "#0f151b", fontVariantNumeric: "tabular-nums" }}>{num}</div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 26, marginTop: 14 }}>
              <div style={{ ...type.displayMedium, fontSize: 48, letterSpacing: 5, textTransform: "uppercase", color: "#3c4650" }}>{p.unidade ?? "anos"}</div>
              {mg ? <div style={{ ...type.display, fontSize: 56, color: "#b3261e", opacity: banda }}>± {fmtEs(mg)}</div> : null}
            </div>
          </div>
        </div>
      </div>
      <Grao id="c14-g" o={0.07} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ESCANEAMENTO 3D
export type PontoScan = { x: number; y: number; rotulo: string };
export type Escaneamento3DProps = SceneProps & { src: string; titulo: string; pontos?: PontoScan[]; hud?: string };
const CIANO = "#79e6ff";
/** Varredura 3D: um plano de laser cruza a foto e deixa nuvem de pontos + malha; pontos medidos ganham rótulo; HUD científico. */
export const Escaneamento3D: React.FC<Escaneamento3DProps> = (p) => {
  const f = useCurrentFrame();
  const PX = 210, PY = 190, PW = 1500, PH = 790;
  const pontos = p.pontos ?? [];
  const sw = suave(f, 6, 40);
  const SWX = PW * sw;
  const COLS = 34, ROWS = 18;
  const vx = (i: number, j: number) => (i / COLS) * PW + (i > 0 && i < COLS ? (random(`mx${i}-${j}`) - 0.5) * 22 : 0);
  const vy = (i: number, j: number) => (j / ROWS) * PH + (j > 0 && j < ROWS ? (random(`my${i}-${j}`) - 0.5) * 22 : 0);
  let malha = "";
  for (let j = 0; j <= ROWS; j++) for (let i = 0; i <= COLS; i++) {
    const x = vx(i, j).toFixed(1), y = vy(i, j).toFixed(1);
    if (i < COLS) malha += `M${x},${y} L${vx(i + 1, j).toFixed(1)},${vy(i + 1, j).toFixed(1)} `;
    if (j < ROWS) malha += `M${x},${y} L${vx(i, j + 1).toFixed(1)},${vy(i, j + 1).toFixed(1)} `;
    if (i < COLS && j < ROWS) malha += `M${x},${y} L${vx(i + 1, j + 1).toFixed(1)},${vy(i + 1, j + 1).toFixed(1)} `;
  }
  const varre = f > 40 ? ((f - 40) * 7) % PH : -100;
  // cubo girando (ícone 3D)
  const a = f * 0.035, b = 0.55;
  const V = [-1, 1].flatMap((x) => [-1, 1].flatMap((y) => [-1, 1].map((z) => [x, y, z])));
  const proj = V.map(([x, y, z]) => {
    const x1 = x * Math.cos(a) + z * Math.sin(a), z1 = -x * Math.sin(a) + z * Math.cos(a);
    const y1 = y * Math.cos(b) - z1 * Math.sin(b);
    return [PX + PW - 90 + x1 * 30, PY + PH - 90 + y1 * 30];
  });
  const arestas = V.flatMap((v, i) => V.map((w, j) => [i, j, v, w] as const)).filter(([i, j, v, w]) =>
    i < j && Math.abs(v[0] - w[0]) + Math.abs(v[1] - w[1]) + Math.abs(v[2] - w[2]) === 2);
  const hud = p.hud ?? "RECONSTRUÇÃO 3D";
  // posição dos rótulos: lado oposto à borda mais próxima; empurra para baixo os que colidem
  const rot = pontos.map((q) => {
    const dir = q.x > 0.6 ? -1 : 1;
    const cx = PX + q.x * PW, cy = PY + q.y * PH;
    const w = 130 + q.rotulo.length * 20;
    const x0 = dir > 0 ? cx + 110 : cx - 110 - w;
    return { dir, cx, cy, x0, x1: x0 + w, ty: Math.max(PY + 30, Math.min(PY + PH - 90, cy - (q.y > 0.25 ? 110 : -60))) };
  });
  const ordem = rot.map((_, i) => i).sort((a2, b2) => rot[a2].ty - rot[b2].ty);
  ordem.forEach((i, k) => {
    for (let m = 0; m < k; m++) {
      const j = ordem[m];
      if (rot[i].x0 < rot[j].x1 && rot[j].x0 < rot[i].x1 && rot[i].ty < rot[j].ty + 70) rot[i].ty = rot[j].ty + 70;
    }
  });
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #0b141c, #030508 75%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: PX, top: PY, width: PW, height: PH, overflow: "hidden", opacity: ent(f, 0, 10),
        transform: `scale(${interpolate(f, [0, p.dur], [1.02, 1], clamp)})` }}>
        <Img src={src(p.src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 25%",
          filter: "grayscale(1) brightness(0.5) contrast(1.1)" }} />
        <div style={{ position: "absolute", left: 0, top: 0, width: SWX, height: PH, overflow: "hidden", background: "#03070b" }}>
          <Img src={src(p.src)} style={{ position: "absolute", width: PW, height: PH, objectFit: "cover", objectPosition: "50% 25%", opacity: 0.42,
            filter: "grayscale(1) contrast(1.25) brightness(0.95)" }} />
          <div style={{ position: "absolute", left: 0, top: 0, width: PW, height: PH,
            maskImage: "radial-gradient(circle, #000 1.3px, transparent 2px)", WebkitMaskImage: "radial-gradient(circle, #000 1.3px, transparent 2px)",
            maskSize: "7px 7px", WebkitMaskSize: "7px 7px" }}>
            <Img src={src(p.src)} style={{ position: "absolute", width: PW, height: PH, objectFit: "cover", objectPosition: "50% 25%",
              filter: "grayscale(1) contrast(2.3) brightness(1.15)" }} />
            <AbsoluteFill style={{ background: "linear-gradient(180deg, #8ff0ff, #5cc8ff 60%, #b59cff)", mixBlendMode: "multiply" }} />
          </div>
          <svg width={PW} height={PH} style={{ position: "absolute", left: 0, top: 0 }}>
            <path d={malha} stroke="rgba(150,232,255,0.26)" strokeWidth={1} fill="none" />
          </svg>
        </div>
        {sw > 0.001 && sw < 0.999 ? (
          <>
            <div style={{ position: "absolute", left: SWX - 240, top: 0, width: 240, height: PH,
              background: "linear-gradient(90deg, transparent, rgba(121,230,255,0.22))" }} />
            <div style={{ position: "absolute", left: SWX - 2, top: 0, width: 4, height: PH, background: "#d8f8ff",
              boxShadow: "0 0 26px 8px rgba(121,230,255,0.75)" }} />
          </>
        ) : null}
        {varre > 0 ? <div style={{ position: "absolute", left: 0, top: varre, width: PW, height: 2, background: "rgba(121,230,255,0.35)",
          boxShadow: "0 0 14px rgba(121,230,255,0.5)" }} /> : null}
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(0,0,0,0.5))" }} />
      </div>
      {/* moldura em cantoneiras */}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {[[PX, PY, 1, 1], [PX + PW, PY, -1, 1], [PX, PY + PH, 1, -1], [PX + PW, PY + PH, -1, -1]].map(([x, y, sx, sy], i) => (
          <path key={i} d={`M${x + sx * 46},${y} L${x},${y} L${x},${y + sy * 46}`} stroke={CIANO} strokeWidth={3} fill="none" opacity={ent(f, 0, 12)} />
        ))}
        {pontos.length > 1 ? (
          <path d={`M${pontos.map((q) => `${PX + q.x * PW},${PY + q.y * PH}`).join(" L")}`} stroke="rgba(255,255,255,0.55)"
            strokeWidth={2} strokeDasharray="6 8" fill="none" opacity={ent(f, 40, 50)} />
        ) : null}
        {pontos.map((q, i) => {
          const t0 = 6 + 34 * Math.max(0, Math.min(1, q.x)) + 2;
          const o = ent(f, t0, t0 + 10);
          const cx = PX + q.x * PW, cy = PY + q.y * PH;
          return (
            <g key={i} opacity={o}>
              <circle cx={cx} cy={cy} r={16 + (1 - o) * 30} fill="none" stroke="#ffffff" strokeWidth={3} />
              <circle cx={cx} cy={cy} r={4} fill="#ffffff" />
              <line x1={cx - 28} x2={cx - 20} y1={cy} y2={cy} stroke="#fff" strokeWidth={2} />
              <line x1={cx + 20} x2={cx + 28} y1={cy} y2={cy} stroke="#fff" strokeWidth={2} />
              <line x1={cx} x2={cx} y1={cy - 28} y2={cy - 20} stroke="#fff" strokeWidth={2} />
              <line x1={cx} x2={cx} y1={cy + 20} y2={cy + 28} stroke="#fff" strokeWidth={2} />
            </g>
          );
        })}
        {/* eixos */}
        <g opacity={ent(f, 10)} transform={`translate(${PX + 110} ${PY + PH - 70})`}>
          <line x1={0} y1={0} x2={70} y2={0} stroke="#ff6b6b" strokeWidth={4} />
          <line x1={0} y1={0} x2={0} y2={-70} stroke="#7dff9a" strokeWidth={4} />
          <line x1={0} y1={0} x2={-34} y2={30} stroke="#6fa8ff" strokeWidth={4} />
          <text x={80} y={12} fill="#ff6b6b" style={{ fontFamily: SANS, fontSize: 34, fontWeight: 700 }}>X</text>
          <text x={-11} y={-80} fill="#7dff9a" style={{ fontFamily: SANS, fontSize: 34, fontWeight: 700 }}>Y</text>
          <text x={-66} y={44} fill="#6fa8ff" style={{ fontFamily: SANS, fontSize: 34, fontWeight: 700 }}>Z</text>
        </g>
        {/* cubo */}
        <g opacity={ent(f, 4)}>
          {arestas.map(([i, j]) => <line key={`${i}-${j}`} x1={proj[i][0]} y1={proj[i][1]} x2={proj[j][0]} y2={proj[j][1]}
            stroke={CIANO} strokeWidth={2} />)}
        </g>
      </svg>
      {/* rótulos dos pontos */}
      {pontos.map((q, i) => {
        const t0 = 6 + 34 * Math.max(0, Math.min(1, q.x)) + 6;
        const o = ent(f, t0, t0 + 12);
        const { dir, cx, cy, ty } = rot[i];
        return (
          <React.Fragment key={i}>
            <svg width={1920} height={1080} style={{ position: "absolute", opacity: o }}>
              <path d={`M${cx + dir * 22},${cy - (cy > ty ? 16 : -16)} L${cx + dir * 70},${ty + 30} L${cx + dir * 110},${ty + 30}`}
                stroke="#ffffff" strokeWidth={2} fill="none" />
            </svg>
            <div style={{ position: "absolute", top: ty, [dir > 0 ? "left" : "right"]: dir > 0 ? cx + 110 : 1920 - (cx - 110),
              opacity: o, transform: `translateX(${(1 - o) * dir * 20}px)`, display: "flex", alignItems: "center", gap: 14,
              background: "rgba(3,7,11,0.78)", borderLeft: `4px solid ${CIANO}`, padding: "6px 18px", whiteSpace: "nowrap" } as React.CSSProperties}>
              <span style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color: CIANO }}>{String(i + 1).padStart(2, "0")}</span>
              <span style={{ fontFamily: SANS, fontSize: 36, fontWeight: 500, color: "#ffffff" }}>{q.rotulo}</span>
            </div>
          </React.Fragment>
        );
      })}
      {/* HUD */}
      <div style={{ position: "absolute", left: PX, top: 92, right: 520, ...type.display, fontSize: 54, letterSpacing: 2, color: "#eef8fb",
        textTransform: "uppercase", opacity: ent(f, 0), whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{p.titulo}</div>
      <div style={{ position: "absolute", right: 1920 - (PX + PW) + 120, top: 96, width: 380, opacity: ent(f, 4) }}>
        <div style={{ fontFamily: SANS, fontSize: 34, fontWeight: 500, letterSpacing: 5, color: CIANO, textAlign: "right", whiteSpace: "nowrap" }}>{hud}</div>
        <div style={{ marginTop: 10, height: 6, background: "rgba(121,230,255,0.18)" }}>
          <div style={{ width: `${sw * 100}%`, height: "100%", background: CIANO, boxShadow: `0 0 12px ${CIANO}` }} /></div>
      </div>
      <Grao id="scan-g" o={0.06} />
    </AbsoluteFill>
  );
};

// ================================================================================================ QUADRÍCULA DE ESCAVAÇÃO
export type AchadoCelula = { celula: string; rotulo: string };
export type QuadriculaEscavacaoProps = SceneProps & { src: string; titulo: string; achados: AchadoCelula[]; sitio?: string; escala?: string };
const LETRAS = ["A", "B", "C", "D", "E", "F"];
const OURO = "#f0c060";
/** Quadrícula vista de cima: barbantes A–F / 1–6 se esticam sobre a foto do sítio, quadras com achados acendem, lista ao lado. */
export const QuadriculaEscavacao: React.FC<QuadriculaEscavacaoProps> = (p) => {
  const f = useCurrentFrame();
  const GX = 200, GY = 200, G = 780, C = G / 6;
  const PX0 = 1090, PW = 1830 - PX0;
  const cel = p.achados.map((a) => {
    const m = /^\s*([A-Fa-f])\s*([1-6])\s*$/.exec(a.celula);
    return m ? { col: LETRAS.indexOf(m[1].toUpperCase()), row: Number(m[2]) - 1, ...a } : null;
  });
  const n = Math.max(1, p.achados.length);
  const at = (i: number) => 20 + i * Math.min(8, 20 / n);
  const escurece = ent(f, 18, 30);
  const linha = Math.min(70, 470 / n);
  const fios = Array.from({ length: 7 }, (_, k) => k);
  const sag = (k: number, s: string) => 3 + random(`${s}${k}`) * 5;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 30% 50%, #2b2117, #0f0b08 78%)", ...exit(f, p.dur) }}>
      {/* foto do sítio */}
      <div style={{ position: "absolute", left: GX, top: GY, width: G, height: G, overflow: "hidden", opacity: ent(f, 0, 10),
        boxShadow: "0 24px 60px rgba(0,0,0,0.7)" }}>
        <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "sepia(0.55) saturate(1.3) contrast(1.1) brightness(0.92)",
          transform: `scale(${interpolate(f, [0, p.dur], [1.06, 1], clamp)})` }} />
        <AbsoluteFill style={{ background: "#120c07", opacity: 0.45 * escurece }} />
        {cel.map((c, i) => {
          if (!c) return null;
          const o = ent(f, at(i), at(i) + 10);
          return (
            <div key={i} style={{ position: "absolute", left: c.col * C, top: c.row * C, width: C, height: C, opacity: o, overflow: "hidden" }}>
              <Img src={src(p.src)} style={{ position: "absolute", left: -c.col * C, top: -c.row * C, width: G, height: G, objectFit: "cover",
                filter: "sepia(0.4) saturate(1.3) contrast(1.15) brightness(1.18)", transform: `scale(${interpolate(f, [0, p.dur], [1.06, 1], clamp)})`,
                transformOrigin: `${(c.col + 0.5) * C}px ${(c.row + 0.5) * C}px` }} />
              <AbsoluteFill style={{ background: "rgba(240,192,96,0.16)", boxShadow: `inset 0 0 0 4px ${OURO}, inset 0 0 40px rgba(240,192,96,0.55)` }} />
              <div style={{ position: "absolute", left: 8, top: 8, background: OURO, color: "#1c140b", ...type.display, fontSize: 34, lineHeight: 1,
                padding: "6px 10px" }}>{c.col >= 0 ? `${LETRAS[c.col]}${c.row + 1}` : ""}</div>
            </div>
          );
        })}
      </div>
      {/* barbantes */}
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {fios.map((k) => {
          const x = GX + k * C, y = GY + k * C;
          const pv = ent(f, 2 + k * 1.5, 18 + k * 1.5), ph = ent(f, 4 + k * 1.5, 20 + k * 1.5);
          const dv = `M${x},${GY} Q${x + sag(k, "v")},${GY + G / 2} ${x},${GY + G}`;
          const dh = `M${GX},${y} Q${GX + G / 2},${y + sag(k, "h")} ${GX + G},${y}`;
          return (
            <g key={k}>
              <g transform="translate(3 4)" opacity={0.5}><Traco d={dv} p={pv} cor="#000" w={3} /><Traco d={dh} p={ph} cor="#000" w={3} /></g>
              <Traco d={dv} p={pv} cor="#f2ead6" w={2.6} />
              <Traco d={dh} p={ph} cor="#f2ead6" w={2.6} />
            </g>
          );
        })}
        {fios.flatMap((i) => fios.map((j) => {
          const borda = i === 0 || j === 0 || i === 6 || j === 6;
          return <circle key={`${i}-${j}`} cx={GX + i * C} cy={GY + j * C} r={borda ? 7 : 4} fill={borda ? "#3a2a1a" : "#e8dcc0"}
            stroke={borda ? "#e8dcc0" : "none"} strokeWidth={2} opacity={ent(f, 14)} />;
        }))}
        {/* norte e escala, no rodapé do painel */}
        <g opacity={ent(f, 16)} transform={`translate(${PX0 + 40} 925)`}>
          <circle cx={0} cy={0} r={46} fill="none" stroke="#e8dcc0" strokeWidth={2} />
          <path d="M0,-40 L14,10 L0,2 L-14,10 Z" fill={OURO} />
          <path d="M0,40 L14,10 L0,2 L-14,10 Z" fill="#6d5a40" />
          <text x={0} y={-56} textAnchor="middle" fill="#f2ead6" style={{ ...type.display, fontSize: 34 }}>N</text>
        </g>
        <g opacity={ent(f, 18)} transform={`translate(${PX0 + 130} 930)`}>
          {Array.from({ length: 5 }, (_, i) => <rect key={i} x={i * 50} y={0} width={50} height={16} fill={i % 2 ? "#f2ead6" : "#1a130c"}
            stroke="#f2ead6" strokeWidth={2} />)}
          {p.escala ? <text x={270} y={16} fill="#f2ead6" style={{ fontFamily: MONO, fontSize: 34 }}>{p.escala}</text> : null}
        </g>
      </svg>
      {/* letras e números da quadrícula */}
      {LETRAS.map((l, i) => (
        <div key={l} style={{ position: "absolute", left: GX + i * C, width: C, top: GY - 64, textAlign: "center", ...type.display, fontSize: 38,
          color: "#e8dcc0", opacity: ent(f, 6 + i) }}>{l}</div>
      ))}
      {Array.from({ length: 6 }, (_, i) => (
        <div key={i} style={{ position: "absolute", left: GX - 74, width: 50, top: GY + i * C + C / 2 - 26, textAlign: "center", ...type.display,
          fontSize: 38, color: "#e8dcc0", opacity: ent(f, 6 + i) }}>{i + 1}</div>
      ))}
      {/* painel */}
      <div style={{ position: "absolute", left: PX0, top: GY - 10, width: PW, opacity: ent(f, 2), transform: `translateX(${(1 - ent(f, 2)) * 30}px)` }}>
        <div style={{ ...type.display, fontSize: 60, lineHeight: 1.08, color: "#f6ecd6", textTransform: "uppercase", letterSpacing: 2 }}>{p.titulo}</div>
        {p.sitio ? <div style={{ fontFamily: MONO, fontSize: 34, color: "#d2b06a", letterSpacing: 2, marginTop: 14 }}>{p.sitio}</div> : null}
        <div style={{ height: 2, background: "rgba(232,220,192,0.35)", margin: "26px 0 18px" }} />
        {p.achados.map((a, i) => {
          const o = ent(f, at(i) + 2, at(i) + 14);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, height: linha, opacity: o, transform: `translateX(${(1 - o) * 24}px)` }}>
              <div style={{ minWidth: 74, textAlign: "center", background: OURO, color: "#1c140b", ...type.display, fontSize: 36, lineHeight: 1,
                padding: "8px 0" }}>{a.celula.toUpperCase()}</div>
              <div style={{ fontFamily: SANS, fontSize: 36, color: "#f2ead6", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{a.rotulo}</div>
            </div>
          );
        })}
      </div>
      <Grao id="qd-g" o={0.1} />
    </AbsoluteFill>
  );
};
