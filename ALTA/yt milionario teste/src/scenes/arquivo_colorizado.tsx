// ESTILO "ARQUIVO COLORIZADO" (04/11/2026 — pedido do usuário, vídeo de referência painel/referencias/20261104-*-okeanos-cuba).
// Documentário de história 1890-1960: fotos de arquivo impressas sobre mesa escura (scripts/moldura.py faz as fotos),
// recriações coloridas de época em tela cheia, e estas peças de tela cheia em serifa clássica + laranja de carimbo:
//   Polaroids        1-4 cópias com legenda datilografada caindo na mesa escura, uma por cue (coleção de provas)
//   LinhaDoTempoAC   linha fina com marcos: data laranja (Oswald) em cima, fato datilografado embaixo
//   BarrasAC         título serifado + ano laranja, 2-3 barras creme/laranja crescendo com o valor escrito em cima
//   DadoAC           título serifado + período + um número grande sublinhado ("MAIS DE 4.000 / SOLDADOS MORTOS")
//   CitacaoAC        trecho de documento/lei em versalete serifado, a frase-chave sobre tarja laranja
//   MapaPergaminho   mar verde-azulado, terra bege, nomes em versalete, rotas azul/vermelha, linha pontilhada de distância
// Todo número/data na tela tem de ser DITO na narração. Cada peça conta como animação de tela cheia.
import React from "react";
import { AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { SceneProps, cue, exit } from "./shared";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const AC = { laranja: "#C45634", creme: "#ECE2CC", tinta: "#E9DFC9", fundo: "#17120E", texto: "#E8DCC4", dim: "#A89A82",
  mar: "#5E8A78", terra: "#D9C79A", borda: "#3E5F52" };
const SERIF = "Garamond Arquivo";
const MAQ = "Courier Prime";
const DISP = "Oswald";

if (typeof document !== "undefined" && typeof FontFace !== "undefined") {
  const h = delayRender("garamond");
  Promise.all([
    new FontFace(SERIF, `url(${staticFile("fonts/Garamond.ttf")})`, { weight: "400" }).load(),
    new FontFace(SERIF, `url(${staticFile("fonts/Garamond-Bold.ttf")})`, { weight: "700" }).load(),
  ]).then((fs) => { fs.forEach((f) => document.fonts.add(f)); continueRender(h); }).catch(() => continueRender(h));
}

const src = (s: string) => (/^https?:|^data:/.test(s) ? s : staticFile(s));

/** mesa escura esfumaçada (igual ao fundo das fotos impressas do moldura.py) */
export const MesaEscura: React.FC<{ papel?: boolean }> = ({ papel }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: papel ? "#DCCAA4" : AC.fundo }}>
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: papel ? 0.22 : 0.34 }}>
        <filter id="fumaca"><feTurbulence type="fractalNoise" baseFrequency="0.0035 0.006" numOctaves={4} seed={3 + Math.floor(f / 240)} />
          <feColorMatrix values={papel ? "0 0 0 0 0.55  0 0 0 0 0.48  0 0 0 0 0.36  0 0 0 0.9 0" : "0 0 0 0 0.42  0 0 0 0 0.35  0 0 0 0 0.27  0 0 0 1.1 -0.15"} /></filter>
        <rect width={1920} height={1080} filter="url(#fumaca)" transform={`translate(${-f * 0.15},0)`} />
      </svg>
      {papel ? <AbsoluteFill style={{ opacity: 0.18, backgroundImage: "linear-gradient(#9C8A66 1px, transparent 1px), linear-gradient(90deg, #9C8A66 1px, transparent 1px)", backgroundSize: "48px 48px" }} /> : null}
      <AbsoluteFill style={{ boxShadow: `inset 0 0 ${papel ? 260 : 380}px rgba(0,0,0,${papel ? 0.55 : 0.92})` }} />
    </AbsoluteFill>
  );
};

/** etiqueta laranja do canto (LUGAR · DATA / nome do bloco) */
export const Etiqueta: React.FC<{ texto: string; ano?: string; delay?: number }> = ({ texto, ano, delay = 4 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [delay, delay + 12], [0, 1], clamp);
  const box = { fontFamily: SERIF, fontWeight: 700, fontSize: 26, letterSpacing: 2.5, textTransform: "uppercase" as const,
    padding: "5px 14px 3px", color: "#FAF0E4" };
  return (
    <div style={{ position: "absolute", left: 60, top: 52, display: "flex", gap: 6, opacity: o }}>
      {ano ? <div style={{ ...box, background: AC.laranja }}>{ano}</div> : null}
      <div style={{ ...box, background: ano ? "#100E0C" : AC.laranja }}>{texto}</div>
    </div>
  );
};

// ======================================================================================== POLAROIDS
export type FotoMesa = { src: string; legenda: string; cue: string };
export type PolaroidsProps = SceneProps & { fotos: FotoMesa[]; etiqueta?: string };

const LUGARES: Record<number, [number, number, number][]> = {   // x, y (centro), rotação por quantidade de fotos
  1: [[960, 520, -3]],
  2: [[700, 500, -4], [1220, 540, 3]],
  3: [[560, 470, -5], [1000, 600, 4], [1420, 470, -2]],
  4: [[520, 430, -5], [900, 620, 3], [1300, 420, -3], [1520, 660, 5]],
};

export const Polaroids: React.FC<PolaroidsProps> = (p) => {
  const f = useCurrentFrame();
  const n = Math.min(4, p.fotos.length);
  const pos = LUGARES[n] ?? LUGARES[4];
  const larg = n === 1 ? 760 : n === 2 ? 620 : 500;
  const cam = interpolate(f, [0, p.dur], [1.0, 1.05], clamp);
  return (
    <AbsoluteFill style={{ overflow: "hidden", ...exit(f, p.dur) }}>
      <MesaEscura />
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        {p.fotos.slice(0, n).map((ft, i) => {
          const at = cue(p, ft.cue, 0.05 + 0.6 * (i / Math.max(1, n)));
          const s = spring({ frame: f - at, fps: 30, config: { damping: 14, stiffness: 120, mass: 0.8 } });
          const [x, y, r] = pos[i];
          return (
            <div key={i} style={{ position: "absolute", left: x - larg / 2, top: y + 60 - larg * 0.42, width: larg,
              background: "#F3EEE2", padding: "16px 16px 52px", boxShadow: "0 22px 45px rgba(0,0,0,0.7)",
              opacity: interpolate(f - at, [0, 6], [0, 1], clamp),
              transform: `translate(${(1 - s) * 60}px, ${(1 - s) * -90}px) rotate(${r + (1 - s) * 9}deg) scale(${1.25 - 0.25 * s})` }}>
              <Img src={src(ft.src)} style={{ width: "100%", height: larg * 0.64, objectFit: "cover", filter: "grayscale(0.85) sepia(0.25) contrast(1.05)" }} />
              <div style={{ position: "absolute", left: 22, bottom: 14, fontFamily: MAQ, fontWeight: 700, fontSize: n > 2 ? 17 : 20,
                letterSpacing: 2, color: "#2A2520", textTransform: "uppercase" }}>{ft.legenda}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      {p.etiqueta ? <Etiqueta texto={p.etiqueta} /> : null}
    </AbsoluteFill>
  );
};

// ======================================================================================== LINHA DO TEMPO
export type Marco = { data: string; texto: string; cue: string };
export type LinhaDoTempoACProps = SceneProps & { etiqueta?: string; marcos: Marco[] };

export const LinhaDoTempoAC: React.FC<LinhaDoTempoACProps> = (p) => {
  const f = useCurrentFrame();
  const n = p.marcos.length;
  const x0 = n <= 2 ? 560 : n === 3 ? 400 : 300, x1 = n <= 2 ? 1360 : n === 3 ? 1520 : 1620, y = 560;
  const ats = p.marcos.map((m, i) => cue(p, m.cue, 0.08 + 0.7 * (i / Math.max(1, n - 1))));
  const xs = p.marcos.map((_, i) => (n === 1 ? (x0 + x1) / 2 : x0 + ((x1 - x0) * i) / (n - 1)));
  const fim = interpolate(f, [ats[0], ats[n - 1] + 10], [xs[0], xs[n - 1]], { ...clamp, easing: Easing.inOut(Easing.quad) });
  return (
    <AbsoluteFill style={{ ...exit(f, p.dur) }}>
      <MesaEscura />
      {p.etiqueta ? <Etiqueta texto={p.etiqueta} /> : null}
      <div style={{ position: "absolute", left: xs[0], top: y, width: Math.max(0, fim - xs[0]), height: 2, background: "#B8A98E" }} />
      {p.marcos.map((m, i) => {
        const o = interpolate(f, [ats[i], ats[i] + 12], [0, 1], clamp);
        const dy = interpolate(f, [ats[i], ats[i] + 14], [14, 0], { ...clamp, easing: EXPO });
        const atual = i === n - 1 || f < (ats[i + 1] ?? 1e9);
        return (
          <div key={i} style={{ position: "absolute", left: xs[i] - 220, top: y - 78, width: 440, textAlign: "center", opacity: o }}>
            <div style={{ fontFamily: DISP, fontWeight: 500, fontSize: atual ? 44 : 38, color: AC.laranja, letterSpacing: 1,
              translate: `0 ${dy}px` }}>{m.data}</div>
            <div style={{ margin: "14px auto 0", width: 18, height: 18, borderRadius: 9, background: AC.laranja, border: "3px solid #E9C9B6" }} />
            <div style={{ marginTop: 18, fontFamily: MAQ, fontWeight: 700, fontSize: 25, letterSpacing: 2, color: AC.texto,
              textTransform: "uppercase", lineHeight: 1.25 }}>{m.texto}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ======================================================================================== BARRAS
export type BarraAC = { valor: number; rotulo: string; texto: string; cue: string; destaque?: boolean };
export type BarrasACProps = SceneProps & { titulo: string; subtitulo?: string; barras: BarraAC[] };

export const BarrasAC: React.FC<BarrasACProps> = (p) => {
  const f = useCurrentFrame();
  const max = Math.max(...p.barras.map((b) => b.valor), 1);
  const n = p.barras.length, lb = 170, gap = 210, base = 860, hmax = 560;
  const x0 = 960 - (n * lb + (n - 1) * gap) / 2;
  return (
    <AbsoluteFill style={{ ...exit(f, p.dur) }}>
      <MesaEscura />
      <div style={{ position: "absolute", top: 120, width: "100%", textAlign: "center", opacity: interpolate(f, [2, 16], [0, 1], clamp) }}>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 64, letterSpacing: 4, color: AC.creme, textTransform: "uppercase" }}>{p.titulo}</div>
        {p.subtitulo ? <div style={{ fontFamily: SERIF, fontSize: 30, letterSpacing: 3, color: AC.laranja }}>{p.subtitulo}</div> : null}
      </div>
      <div style={{ position: "absolute", left: x0 - 60, top: base, width: n * lb + (n - 1) * gap + 120, height: 2, background: "#8C7E66" }} />
      {p.barras.map((b, i) => {
        const at = cue(p, b.cue, 0.15 + 0.5 * (i / Math.max(1, n)));
        const t = interpolate(f, [at, at + 28], [0, 1], { ...clamp, easing: EXPO });
        const h = (hmax * b.valor) / max * t;
        const x = x0 + i * (lb + gap);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: base - h, width: lb, height: h, background: b.destaque ? AC.laranja : "#E2D6BE" }} />
            <div style={{ position: "absolute", left: x - 140, width: lb + 280, top: base - h - 58, textAlign: "center", opacity: t,
              fontFamily: DISP, fontWeight: 500, fontSize: 34, color: "#F1E8D8", textTransform: "uppercase" }}>{b.texto}</div>
            <div style={{ position: "absolute", left: x - 140, width: lb + 280, top: base + 18, textAlign: "center",
              fontFamily: SERIF, fontWeight: 700, fontSize: 24, letterSpacing: 3, color: AC.dim, textTransform: "uppercase" }}>{b.rotulo}</div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

// ======================================================================================== DADO (número grande)
export type DadoACProps = SceneProps & { titulo: string; periodo?: string; numero: string; texto: string; cueNumero: string };

export const DadoAC: React.FC<DadoACProps> = (p) => {
  const f = useCurrentFrame();
  const at = cue(p, p.cueNumero, 0.3);
  const t = interpolate(f, [at, at + 20], [0, 1], { ...clamp, easing: EXPO });
  return (
    <AbsoluteFill style={{ ...exit(f, p.dur) }}>
      <MesaEscura />
      <div style={{ position: "absolute", top: 150, width: "100%", textAlign: "center", opacity: interpolate(f, [2, 16], [0, 1], clamp) }}>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 60, letterSpacing: 4, color: AC.creme, textTransform: "uppercase" }}>{p.titulo}</div>
        {p.periodo ? <div style={{ fontFamily: SERIF, fontSize: 28, letterSpacing: 3, color: AC.laranja }}>{p.periodo}</div> : null}
      </div>
      <div style={{ position: "absolute", left: 560, top: 640, opacity: t, translate: `0 ${(1 - t) * 20}px` }}>
        <div style={{ fontFamily: DISP, fontWeight: 700, fontSize: 52, color: "#F1E8D8", textTransform: "uppercase" }}>{p.numero}</div>
        <div style={{ width: 800 * t, height: 2, background: "#B8A98E", margin: "8px 0 12px" }} />
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 28, letterSpacing: 3, color: AC.dim, textTransform: "uppercase" }}>{p.texto}</div>
      </div>
    </AbsoluteFill>
  );
};

// ======================================================================================== CITAÇÃO
export type CitacaoACProps = SceneProps & { linhas: string[]; destaque: string; cueDestaque: string };

export const CitacaoAC: React.FC<CitacaoACProps> = (p) => {
  const f = useCurrentFrame();
  const at = cue(p, p.cueDestaque, 0.6);
  const est = { fontFamily: SERIF, fontWeight: 700, fontSize: 46, letterSpacing: 2.5, lineHeight: 1.45, textTransform: "uppercase" as const };
  return (
    <AbsoluteFill style={{ ...exit(f, p.dur), justifyContent: "center", alignItems: "center" }}>
      <MesaEscura />
      <div style={{ position: "relative", width: 1400, textAlign: "center" }}>
        {p.linhas.map((l, i) => (
          <div key={i} style={{ ...est, color: AC.creme, opacity: interpolate(f, [4 + i * 10, 18 + i * 10], [0, 1], clamp) }}>{l}</div>
        ))}
        <div style={{ ...est, display: "inline-block", marginTop: 4, padding: "0 18px", color: "#FFF4E8",
          background: `linear-gradient(90deg, ${AC.laranja} ${interpolate(f, [at, at + 16], [0, 100], clamp)}%, transparent 0)`,
          opacity: interpolate(f, [at - 6, at + 4], [0, 1], clamp) }}>{p.destaque}</div>
      </div>
    </AbsoluteFill>
  );
};

// ======================================================================================== MAPA PERGAMINHO
export type LugarAC = { nome: string; lat: number; lon: number; cue?: string; ponto?: boolean; grande?: boolean; circulo?: boolean };
export type RotaAC = { pontos: [number, number][]; cor?: "azul" | "vermelho"; cue: string; seta?: boolean };
export type MapaPergaminhoProps = SceneProps & {
  titulo: string; ano?: string;
  terras: [number, number][][];          // contornos de terra (lat, lon) — costa simplificada, preenchida de bege
  enquadra?: [number, number][];         // pontos extras que definem a área do mapa (cantos)
  lugares?: LugarAC[]; rotas?: RotaAC[];
  distancia?: { de: [number, number]; ate: [number, number]; texto: string; cue: string };
};

export const MapaPergaminho: React.FC<MapaPergaminhoProps> = (p) => {
  const f = useCurrentFrame();
  const todos = [...p.terras.flat(), ...(p.enquadra ?? []), ...(p.lugares ?? []).map((l) => [l.lat, l.lon] as [number, number])];
  const lat0 = todos.reduce((a, [la]) => a + la, 0) / todos.length;
  const k = Math.cos((lat0 * Math.PI) / 180);
  const pts = p.enquadra?.length ? [...p.enquadra, ...(p.lugares ?? []).map((l) => [l.lat, l.lon] as [number, number])] : todos;
  const xs = pts.map(([, lo]) => lo * k), ys = pts.map(([la]) => -la);
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const box = { x: 80, y: 120, w: 1760, h: 860 };
  const esc = Math.min(box.w / Math.max(maxX - minX, 1e-6), box.h / Math.max(maxY - minY, 1e-6));
  const ox = box.x + (box.w - (maxX - minX) * esc) / 2, oy = box.y + (box.h - (maxY - minY) * esc) / 2;
  const pr = (la: number, lo: number) => [ox + (lo * k - minX) * esc, oy + (-la - minY) * esc];
  const path = (c: [number, number][], fecha = true) => c.map(([la, lo], i) => `${i ? "L" : "M"}${pr(la, lo).join(",")}`).join(" ") + (fecha ? " Z" : "");
  const cam = interpolate(f, [0, p.dur], [1.0, 1.07], clamp);
  const tOn = interpolate(f, [4, 20], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: AC.mar, overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <filter id="perg"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves={3} seed={9} />
            <feColorMatrix values="0 0 0 0 0.2  0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0.35 0" /></filter>
          {p.terras.map((t, i) => (
            <g key={i}>
              <path d={path(t)} fill="none" stroke={AC.borda} strokeWidth={10} opacity={0.35} />
              <path d={path(t)} fill={AC.terra} stroke="#7A6A48" strokeWidth={2} />
            </g>
          ))}
          <rect width={1920} height={1080} filter="url(#perg)" />
          {p.distancia ? (() => {
            const a = pr(...p.distancia.de), b = pr(...p.distancia.ate), at = cue(p, p.distancia.cue, 0.4);
            const t = interpolate(f, [at, at + 24], [0, 1], { ...clamp, easing: EXPO });
            return (
              <g>
                <line x1={a[0]} y1={a[1]} x2={a[0] + (b[0] - a[0]) * t} y2={a[1] + (b[1] - a[1]) * t} stroke={AC.laranja} strokeWidth={3} strokeDasharray="8 8" />
                <text x={(a[0] + b[0]) / 2 + 24} y={(a[1] + b[1]) / 2} fill={AC.laranja} opacity={t}
                  style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 30, letterSpacing: 3 }}>{p.distancia.texto}</text>
              </g>
            );
          })() : null}
          {(p.rotas ?? []).map((r, i) => {
            const at = cue(p, r.cue, 0.3 + 0.2 * i);
            const q = r.pontos.map(([la, lo]) => pr(la, lo));
            const L = q.slice(1).reduce((a, c, j) => a + Math.hypot(c[0] - q[j][0], c[1] - q[j][1]), 0);
            const t = interpolate(f, [at, at + 40], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
            const cor = r.cor === "vermelho" ? "#C9483A" : "#8FC3E0";
            const d = q.map((c, j) => `${j ? "L" : "M"}${c.join(",")}`).join(" ");
            return (
              <g key={i}>
                <path d={d} fill="none" stroke="#FFFFFF" strokeWidth={9} opacity={0.35} strokeDasharray={L} strokeDashoffset={L * (1 - t)} />
                <path d={d} fill="none" stroke={cor} strokeWidth={5} strokeDasharray={L} strokeDashoffset={L * (1 - t)} strokeLinecap="round" />
              </g>
            );
          })}
        </svg>
        {(p.lugares ?? []).map((l, i) => {
          const at = l.cue ? cue(p, l.cue, 0.2) : 8 + i * 4;
          const o = interpolate(f, [at, at + 12], [0, 1], clamp);
          const [x, y] = pr(l.lat, l.lon);
          const r = spring({ frame: f - at, fps: 30, config: { damping: 15 } });
          return (
            <React.Fragment key={i}>
              {l.circulo ? <div style={{ position: "absolute", left: x - 34 * r, top: y - 34 * r, width: 68 * r, height: 68 * r,
                borderRadius: "50%", border: "3px solid #F4EBDA", opacity: o }} /> : null}
              {l.ponto !== false ? <div style={{ position: "absolute", left: x - 6, top: y - 6, width: 12, height: 12, borderRadius: 6,
                background: l.circulo ? AC.laranja : "#2C2218", opacity: o }} /> : null}
              <div style={{ position: "absolute", left: x + (l.ponto === false ? -200 : 16), top: y - (l.grande ? 26 : 18),
                width: l.ponto === false ? 400 : undefined, textAlign: l.ponto === false ? "center" : undefined, whiteSpace: "nowrap",
                fontFamily: SERIF, fontWeight: 700, fontSize: l.grande ? 46 : 28, letterSpacing: l.grande ? 8 : 3,
                color: l.grande ? "rgba(60,50,34,0.75)" : "#2C2218", textTransform: "uppercase", opacity: o,
                textShadow: "0 1px 0 rgba(255,245,220,0.5)" }}>{l.nome}</div>
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 50, opacity: tOn }}>
        {p.ano ? <div style={{ fontFamily: SERIF, fontSize: 26, letterSpacing: 6, color: "rgba(250,244,230,0.75)" }}>{p.ano}</div> : null}
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 54, letterSpacing: 4, color: "#FAF4E6", textTransform: "uppercase",
          textShadow: "0 2px 10px rgba(0,0,0,0.35)" }}>{p.titulo}</div>
        <div style={{ width: 420 * tOn, height: 2, background: "rgba(250,244,230,0.7)", marginTop: 6 }} />
      </div>
      <AbsoluteFill style={{ boxShadow: "inset 0 0 300px rgba(20,30,24,0.75)" }} />
    </AbsoluteFill>
  );
};
