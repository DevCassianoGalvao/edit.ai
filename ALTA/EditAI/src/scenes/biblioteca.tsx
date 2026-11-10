// BIBLIOTECA de animações fixas do pipeline (25/09/2026 — regra do usuário: animação é JavaScript/Remotion,
// After Effects só para peça-assinatura única). Saíram dos exemplos de src/exemplos/Exemplos.tsx e agora
// recebem DADOS + CUES: cada elemento entra no quadro em que a palavra é dita (shared.cue), igual a blocos.tsx.
//   MapaRota     — rota/linha/rio crescendo entre lugares reais (lat/lon), contador de km acompanha
//   Odometro     — número forte rolando dígito a dígito + barras de comparação (anos, países, empresas)
//   Documento    — fonte primária encenada: papel entra, texto datilografado, marca-texto, carimbo
//   FotoMedidor  — foto real com push + medidor (temperatura, profundidade, pressão, velocidade) e efeito
// Todo número aqui tem de ser DITO na narração (regra de sempre). Cada uma conta como animação de tela cheia
// (teto: 1 a cada 3 min).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, spring, staticFile, useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { SceneProps, cue, exit } from "./shared";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const EXPO = Easing.bezier(0.16, 1, 0.3, 1);

/** Separador de milhar por idioma sem toLocaleString (o Chrome do render não garante o ICU): "," en; "." pt/it/es/de; " " pl/fr. */
export const fmtSep = (n: number, sep = ",") =>   // espaço vira NBSP: "1 000" nunca quebra em duas linhas (pl, 25/09)
  Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep === " " ? " " : sep);

// ================================================================================================ MAPA COM ROTA
export type Lugar = { nome: string; lat: number; lon: number; valor?: number; cue: string; abaixo?: boolean;
  esquerda?: boolean };   // 11/10/2026: rótulo à esquerda do ponto (lugar na borda direita)
export type MapaRotaProps = SceneProps & {
  kicker: string;                    // rótulo em cima do contador (ex.: "AMUR–YAKUTSK MAINLINE")
  lugares: Lugar[];                  // na ordem da rota; o traço chega em cada um no seu cue
  unidade?: string;                  // "km" -> contador usa `valor` de cada lugar; sem unidade = sem contador
  sep?: string;
  linhas?: { pontos: [number, number][]; cor?: string }[];   // rio, fronteira, costa (lat, lon)
  marca?: { nome: string; lat: number; lon: number; nota?: string; cue: string };  // destino fora da rota
  tint?: string;
};

export const MapaRota: React.FC<MapaRotaProps> = (p) => {
  const f = useCurrentFrame();
  const tint = p.tint ?? colors.accent;
  // projeção equirretangular com correção de cos(lat), encaixada numa caixa que deixa o canto do contador livre
  const todos = [...p.lugares.map((l) => [l.lat, l.lon]), ...(p.linhas ?? []).flatMap((l) => l.pontos),
    ...(p.marca ? [[p.marca.lat, p.marca.lon]] : [])] as [number, number][];
  const lat0 = todos.reduce((a, [la]) => a + la, 0) / todos.length;
  const k = Math.cos((lat0 * Math.PI) / 180);
  const xs = todos.map(([, lo]) => lo * k), ys = todos.map(([la]) => -la);
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const box = { x: 520, y: 170, w: 1180, h: 780 };
  const esc = Math.min(box.w / Math.max(maxX - minX, 1e-6), box.h / Math.max(maxY - minY, 1e-6));
  const ox = box.x + (box.w - (maxX - minX) * esc) / 2, oy = box.y + (box.h - (maxY - minY) * esc) / 2;
  const proj = (lat: number, lon: number) => ({ x: ox + (lon * k - minX) * esc, y: oy + (-lat - minY) * esc });

  const pts = p.lugares.map((l) => proj(l.lat, l.lon));
  const seg = pts.slice(1).map((q, i) => Math.hypot(q.x - pts[i].x, q.y - pts[i].y));
  const total = Math.max(1, seg.reduce((a, b) => a + b, 0));
  let acc = 0;
  const frac = pts.map((_, i) => { if (i) acc += seg[i - 1]; return acc / total; });
  // quadro em que o traço chega em cada lugar = cue do lugar (sempre crescente, mínimo 20 quadros entre dois)
  const ats: number[] = [];
  p.lugares.forEach((l, i) => {
    const c = cue(p, l.cue, 0.08 + (0.7 * i) / Math.max(1, p.lugares.length - 1));
    ats.push(i ? Math.max(c, ats[i - 1] + 20) : c);
  });
  const t = ats.length > 1 ? interpolate(f, ats, frac, { ...clamp, easing: Easing.inOut(Easing.quad) }) : 1;
  const d = pts.map((q, i) => `${i ? "L" : "M"}${q.x},${q.y}`).join(" ");
  const valores = p.lugares.map((l) => l.valor ?? 0);
  const contador = Math.round(interpolate(t, frac, valores, clamp));
  const cam = interpolate(f, [0, p.dur], [1.0, 1.06], clamp);
  const mAt = p.marca ? cue(p, p.marca.cue, 0.85) : 0;
  const mq = p.marca ? proj(p.marca.lat, p.marca.lon) : { x: 0, y: 0 };

  return (
    <AbsoluteFill style={{ background: "#05080D", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        <AbsoluteFill style={{ opacity: 0.18, backgroundImage: `linear-gradient(${colors.line} 1px, transparent 1px),
          linear-gradient(90deg, ${colors.line} 1px, transparent 1px)`, backgroundSize: "96px 96px" }} />
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          {(p.linhas ?? []).map((l, i) => (
            <path key={i} d={l.pontos.map(([la, lo], j) => { const q = proj(la, lo); return `${j ? "L" : "M"}${q.x},${q.y}`; }).join(" ")}
              fill="none" stroke={l.cor ?? colors.cool} strokeWidth={7} strokeLinecap="round" opacity={0.75}
              strokeDasharray={3000} strokeDashoffset={interpolate(f, [5, 70], [3000, 0], clamp)} />
          ))}
          <path d={d} fill="none" stroke={tint} strokeWidth={9} strokeLinecap="round"
            strokeDasharray={total} strokeDashoffset={total * (1 - t)} style={{ filter: `drop-shadow(0 0 14px ${tint})` }} />
          <path d={d} fill="none" stroke="#000" strokeWidth={3} strokeDasharray="14 14" strokeDashoffset={-f * 1.5}
            opacity={t > 0 ? 0.55 : 0} />
          {pts.map((q, i) => {
            const on = spring({ frame: f - ats[i], fps: 30, config: { damping: 12, stiffness: 140 } });
            return (
              <g key={i} transform={`translate(${q.x},${q.y}) scale(${on})`}>
                <circle r={34} fill={tint} opacity={0.18 * (1 + Math.sin(f / 6))} />
                <circle r={13} fill={tint} stroke="#000" strokeWidth={3} />
              </g>
            );
          })}
          {p.marca ? (
            <g opacity={interpolate(f, [mAt, mAt + 15], [0, 1], clamp)}>
              <circle cx={mq.x} cy={mq.y} r={11} fill={colors.text} />
              <text x={mq.x - 25} y={mq.y - 24} textAnchor="end" fill={colors.text} style={{ ...type.display, fontSize: 40 }}>
                {p.marca.nome}</text>
              {p.marca.nota ? <text x={mq.x - 25} y={mq.y + 16} textAnchor="end" fill={colors.cool}
                style={{ ...type.body, fontSize: 26 }}>{p.marca.nota}</text> : null}
            </g>
          ) : null}
        </svg>
        {pts.map((q, i) => (
          <div key={i} style={{ position: "absolute", top: q.y + (p.lugares[i].abaixo ? 18 : -22), whiteSpace: "nowrap",
            ...(p.lugares[i].esquerda ? { right: 1920 - q.x + 30, textAlign: "right" as const } : { left: q.x + 30 }),
            ...type.display, fontSize: 36, color: colors.text, letterSpacing: 2, textShadow: "0 2px 12px #000",
            opacity: interpolate(f - ats[i] - 6, [0, 12], [0, 1], clamp),
            translate: `${interpolate(f - ats[i] - 6, [0, 12], [-16, 0], { ...clamp, easing: EXPO })}px 0` }}>
            {p.lugares[i].nome}
          </div>
        ))}
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 120, top: 90 }}>
        <div style={{ ...type.body, fontSize: 28, color: colors.textDim, letterSpacing: 4 }}>{p.kicker}</div>
        {p.unidade ? (
          <div style={{ ...type.display, fontSize: 150, color: tint, lineHeight: 1 }}>
            {fmtSep(contador, p.sep)}<span style={{ fontSize: 60, color: colors.text }}> {p.unidade}</span></div>
        ) : null}
      </div>
      <AbsoluteFill style={{ boxShadow: "inset 0 0 300px rgba(0,0,0,0.9)" }} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ODÔMETRO
const Digito: React.FC<{ v: number; f0: number; h: number }> = ({ v, f0, h }) => {
  const f = useCurrentFrame();
  const pos = interpolate(f, [f0, f0 + 50], [0, (2 + v / 10) * 10], { ...clamp, easing: EXPO });
  return (
    <div style={{ height: h, overflow: "hidden", display: "inline-block" }}>
      <div style={{ transform: `translateY(${-(pos % 10) * h}px)` }}>
        {Array.from({ length: 11 }, (_, i) => (
          <div key={i} style={{ height: h, lineHeight: `${h}px`, textAlign: "center" }}>{i % 10}</div>))}
      </div>
    </div>
  );
};

export type OdometroProps = SceneProps & {
  kicker: string;                    // "PEDIDOS DE RECUPERAÇÃO JUDICIAL · 2025"
  valor: number; cue: string;        // o número rola quando a palavra é dita
  prefixo?: string; sufixo?: string; // "R$", "%", " mil"
  sep?: string;
  nota?: { texto: string; cue: string };
  barras?: { rotulo: string; v: number; cue: string; destaque?: boolean }[];   // no máximo 4
  foto?: string;                     // caminho em public/ (fundo cinza, 22 %)
};

export const Odometro: React.FC<OdometroProps> = (p) => {
  const f = useCurrentFrame();
  const at = cue(p, p.cue, 0.1);
  const txt = fmtSep(p.valor, p.sep ?? ",");
  const H = txt.length > 7 ? 200 : 260;
  const maxV = Math.max(p.valor, ...(p.barras ?? []).map((b) => b.v));
  let n = 0;
  return (
    <AbsoluteFill style={{ background: colors.bg, ...exit(f, p.dur) }}>
      {p.foto ? <Img src={staticFile(p.foto)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover",
        opacity: 0.22, filter: "grayscale(1) contrast(1.2)", transform: `scale(${1.08 - f * 0.0004})` }} /> : null}
      <AbsoluteFill style={{ background: "linear-gradient(90deg, #070B12 35%, transparent 110%)" }} />
      <div style={{ position: "absolute", left: 140, top: 150, ...type.body, fontSize: 34, color: colors.textDim,
        letterSpacing: 3, opacity: interpolate(f, [0, 15], [0, 1], clamp) }}>{p.kicker}</div>
      <div style={{ position: "absolute", left: 130, top: 200, ...type.display, fontSize: H * 0.92, color: colors.accent,
        display: "flex", textShadow: `0 0 40px ${colors.accent}55`, opacity: f >= at ? 1 : 0 }}>
        {p.prefixo ? <span style={{ lineHeight: `${H}px`, fontSize: H * 0.5, marginRight: 20 }}>{p.prefixo}</span> : null}
        {txt.split("").map((c, i) => (/\d/.test(c)
          ? <Digito key={i} v={Number(c)} f0={at + 6 * n++} h={H} />
          : <span key={i} style={{ lineHeight: `${H}px` }}>{c}</span>))}
        {p.sufixo ? <span style={{ lineHeight: `${H}px`, fontSize: H * 0.5, marginLeft: 16 }}>{p.sufixo}</span> : null}
      </div>
      {p.nota ? (() => { const a = cue(p, p.nota.cue, 0.4); return (
        <div style={{ position: "absolute", left: 140, top: 520, ...type.bodyBold, fontSize: 40, color: colors.text,
          opacity: interpolate(f, [a, a + 15], [0, 1], clamp) }}>{p.nota.texto}</div>); })() : null}
      {(p.barras ?? []).slice(0, 4).map((b, i) => {
        const a = cue(p, b.cue, 0.5 + i * 0.1);
        const w = interpolate(f, [a, a + 40], [0, (b.v / maxV) * 900], { ...clamp, easing: EXPO });
        return (
          <div key={i} style={{ position: "absolute", left: 140, top: 640 + i * 100 }}>
            <div style={{ ...type.body, fontSize: 26, color: colors.textDim }}>{b.rotulo}</div>
            <div style={{ height: 38, width: w, marginTop: 6, background: b.destaque ? colors.danger : colors.accentDim }} />
            <div style={{ position: "absolute", left: w + 18, top: 34, ...type.display, fontSize: 34,
              color: b.destaque ? colors.danger : colors.text, opacity: w > 20 ? 1 : 0 }}>{fmtSep(b.v, p.sep ?? ",")}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ================================================================================================ DOCUMENTO + CARIMBO
export type DocumentoProps = SceneProps & {
  linhas: string[];                  // a 1ª é o cabeçalho (órgão, empresa); "" = linha em branco; até ~10 linhas
  cue: string;                       // começa a datilografar
  chave?: number;                    // índice da linha que ganha marca-texto
  carimbo?: { texto: string; cue: string; cor?: string };   // "INVESTIGADA", "CLASSIFIED", "ODRZUCONO"
};

export const Documento: React.FC<DocumentoProps> = (p) => {
  const f = useCurrentFrame();
  const inicio = cue(p, p.cue, 0.05);
  const cAt = p.carimbo ? Math.max(cue(p, p.carimbo.cue, 0.75), inicio + 40) : p.dur;
  const fim = Math.min(cAt - 12, inicio + Math.max(60, p.linhas.join("").length * 0.45));
  const entra = spring({ frame: f, fps: 30, config: { damping: 20, stiffness: 70 } });
  let resto = Math.floor(interpolate(f, [inicio, fim], [0, p.linhas.join("").length], clamp));
  const bate = spring({ frame: f - cAt, fps: 30, config: { damping: 9, stiffness: 180 } });
  const tremor = f >= cAt && f < cAt + 12 ? (random(`t${f}`) - 0.5) * 18 * (1 - (f - cAt) / 12) : 0;
  const marca = interpolate(f, [fim, fim + 16], [0, 1], { ...clamp, easing: EXPO });
  const cor = p.carimbo?.cor ?? colors.danger;
  return (
    <AbsoluteFill style={{ background: "#1a140e", translate: `${tremor}px ${tremor * 0.6}px`, ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #3b2c1c 0%, #120d08 75%)" }} />
      <div style={{ position: "absolute", left: 460, top: 90, width: 1000, height: 900, background: "#EFE6D2",
        boxShadow: "0 40px 90px rgba(0,0,0,0.7)", padding: "80px 90px", boxSizing: "border-box",
        transform: `translateY(${(1 - entra) * 700}px) rotate(${(1 - entra) * 8 - 1.2}deg)` }}>
        <AbsoluteFill style={{ opacity: 0.35, backgroundImage:
          "repeating-linear-gradient(0deg, rgba(0,0,0,0.035) 0 2px, transparent 2px 5px)" }} />
        {p.linhas.map((l, i) => {
          const vis = l.slice(0, Math.max(0, resto));
          resto -= l.length;
          return (
            <div key={i} style={{ ...(i === 0 ? type.bodyBold : type.body), fontSize: i === 0 ? 40 : 31,
              color: "#1f1a14", minHeight: 52, position: "relative", letterSpacing: i === 0 ? 3 : 0 }}>
              {i === p.chave ? <span style={{ position: "absolute", left: -8, top: 6, height: 38,
                width: `${marca * 100}%`, background: "rgba(244,182,63,0.55)" }} /> : null}
              <span style={{ position: "relative" }}>{vis}</span>
              {resto < 0 && resto > -l.length - 1 && f % 16 < 8 ? <span>▌</span> : null}
            </div>
          );
        })}
        {p.carimbo ? (
          <div style={{ position: "absolute", right: 90, bottom: 110, transform:
            `scale(${interpolate(bate, [0, 1], [2.6, 1])}) rotate(-12deg)`, opacity: f >= cAt ? 1 : 0,
            border: `8px solid ${cor}`, color: cor, padding: "10px 34px", ...type.display,
            fontSize: p.carimbo.texto.length > 12 ? 64 : 92, letterSpacing: 6, mixBlendMode: "multiply" }}>
            {p.carimbo.texto}</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

// ================================================================================================ FOTO + MEDIDOR
export type FotoMedidorProps = SceneProps & {
  foto: string;                      // caminho em public/ (foto APROVADA do filme, do país do roteiro)
  de: number; ate: number; unidade: string;   // 0 -> -45 "°C"; 0 -> 11000 " m"; 0 -> 320 " km/h"
  cue: string;                       // o medidor corre quando a palavra é dita
  legenda: string;
  efeito?: "gelo" | "calor" | "fundo" | "nenhum";
  sep?: string;
};

export const FotoMedidor: React.FC<FotoMedidorProps> = (p) => {
  const f = useCurrentFrame();
  const at = cue(p, p.cue, 0.1);
  const v = Math.round(interpolate(f, [at, at + 95], [p.de, p.ate], { ...clamp, easing: Easing.out(Easing.cubic) }));
  const k = interpolate(f, [at + 15, at + 135], [0, 1], clamp);
  const ef = p.efeito ?? "nenhum";
  const tom = ef === "gelo" ? "200,230,255" : ef === "calor" ? "255,120,40" : "0,10,30";
  const cor = ef === "calor" ? colors.danger : colors.cool;
  const nivel = interpolate(v, [Math.min(p.de, p.ate), Math.max(p.de, p.ate)], [8, 100], clamp);  // coluna alta = valor alto
  return (
    <AbsoluteFill style={{ background: "#000", ...exit(f, p.dur) }}>
      <Img src={staticFile(p.foto)} style={{ width: "100%", height: "100%", objectFit: "cover",
        transform: `scale(${1 + f * 0.0006})`,
        filter: `saturate(${1 - k * (ef === "calor" ? -0.3 : 0.5)}) brightness(${1 - k * (ef === "fundo" ? 0.45 : 0.15)})` }} />
      {ef !== "nenhum" ? <AbsoluteFill style={{ background: `radial-gradient(ellipse at center, transparent ${60 - k * 20}%,
        rgba(${tom},${(ef === "fundo" ? 0.8 : 0.55) * k}) 100%)` }} /> : null}
      {ef === "gelo" ? (
        // geada procedural: ruído fractal virado em cristais claros, só nas bordas (máscara que fecha com o frio)
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <defs>
            <filter id="geada" x="0" y="0" width="100%" height="100%">
              <feTurbulence type="fractalNoise" baseFrequency="0.012 0.018" numOctaves={6} seed={7} />
              <feColorMatrix type="matrix" values="0 0 0 0 0.92  0 0 0 0 0.97  0 0 0 0 1  0 0 0 2.6 -1.15" />
            </filter>
            <radialGradient id="borda" cx="50%" cy="50%" r="72%">
              <stop offset={`${95 - k * 45}%`} stopColor="#000" />
              <stop offset="100%" stopColor="#fff" />
            </radialGradient>
            <mask id="m"><rect width={1920} height={1080} fill="url(#borda)" /></mask>
          </defs>
          <rect width={1920} height={1080} filter="url(#geada)" mask="url(#m)" opacity={0.95} />
        </svg>
      ) : null}
      <div style={{ position: "absolute", right: 170, top: 170, width: 70, height: 640, borderRadius: 35,
        background: "rgba(10,20,30,0.55)", border: "4px solid #EAF6FF" }}>
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, borderRadius: 35,
          height: `${nivel}%`, background: cor }} />
      </div>
      <div style={{ position: "absolute", right: 300, top: 360, textAlign: "right", textShadow: "0 4px 30px #000, 0 0 60px #000" }}>
        <div style={{ ...type.display, fontSize: 210, color: "#EAF6FF", lineHeight: 1 }}>
          {v < 0 ? "−" : ""}{fmtSep(Math.abs(v), p.sep)}{p.unidade}</div>
        <div style={{ ...type.body, fontSize: 34, color: colors.text }}>{p.legenda}</div>
      </div>
    </AbsoluteFill>
  );
};
