// ARQUIVO — animações "dark doc" (26/09/2026, pedido do usuário com referências: quadro de provas com polaroides,
// checklist manuscrito sobre foto de época e ficha com nome circulado + tarjas pretas). Mesma regra da biblioteca:
// recebem DADOS + CUES, cada elemento entra no quadro em que a palavra é dita (shared.cue), tudo em JavaScript.
//   QuadroProvas  — polaroides caem e são presas com tacha, fio vermelho liga as provas, etiqueta de papel rasgado
//   Checklist     — cartão sobre foto P&B; itens escritos à mão e marcados (✓, ✗ ou riscado) na hora do cue
//   FichaCirculo  — nome grande circulado à caneta vermelha, seta até a ficha; tarjas pretas censuram ou revelam
// Tratamento de arquivo comum: grão de filme, poeira, vinheta, tremulação de projetor e feixe de luz.
import React from "react";
import { AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame } from "remotion";
import { Easing } from "remotion";
import { type } from "../design/tokens";
import { SceneProps, cue, exit } from "./shared";

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const MAO = "'Segoe Print', 'Segoe Script', 'Comic Sans MS', cursive";   // manuscrito (fonte do Windows)
export const SERIFA = "Georgia, 'Times New Roman', serif";
export const tom = (t: "sepia" | "frio" | "pb") =>
  t === "sepia" ? "grayscale(1) sepia(0.45) contrast(1.08) brightness(0.95)"
    : t === "frio" ? "grayscale(1) contrast(1.15) brightness(0.9) hue-rotate(180deg) sepia(0.12)"
      : "grayscale(1) contrast(1.12)";
export const src = (s: string) => (s.startsWith("http") ? s : staticFile(s));

// ------------------------------------------------------------------------------------------ TRATAMENTO DE ARQUIVO
/** Grão + poeira + vinheta + tremulação. Fica por cima de tudo, sem capturar a imagem. */
export const FilmeVelho: React.FC<{ forca?: number; feixe?: boolean }> = ({ forca = 1, feixe = true }) => {
  const f = useCurrentFrame();
  const flick = 1 + (random(`fl${f}`) - 0.5) * 0.05 * forca;
  const poeira = Array.from({ length: 7 }, (_, i) => ({
    x: random(`px${f}-${i}`) * 1920, y: random(`py${f}-${i}`) * 1080, r: 1 + random(`pr${f}-${i}`) * 3,
    v: random(`pv${f}-${i}`) > 0.55,
  }));
  const fio = random(`fio${Math.floor(f / 5)}`) > 0.7 ? random(`fx${Math.floor(f / 5)}`) * 1920 : -10;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {feixe ? <AbsoluteFill style={{ mixBlendMode: "screen", opacity: 0.22 * forca,
        background: `linear-gradient(${112 + Math.sin(f / 60) * 4}deg, transparent 30%, rgba(255,240,210,0.55) 48%, transparent 64%)` }} /> : null}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(0,0,0,0.78) 100%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.16 * forca, mixBlendMode: "overlay" }}>
        <filter id={`g${f % 6}`}><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={f % 97} /></filter>
        <rect width="100%" height="100%" filter={`url(#g${f % 6})`} />
      </svg>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {poeira.filter((d) => d.v).map((d, i) => <circle key={i} cx={d.x} cy={d.y} r={d.r} fill="rgba(20,16,10,0.55)" />)}
        {fio > 0 ? <line x1={fio} y1={0} x2={fio + 6} y2={1080} stroke="rgba(255,255,255,0.10)" strokeWidth={1.5} /> : null}
      </svg>
      <AbsoluteFill style={{ background: `rgba(0,0,0,${(1 - flick) * 3 + 0.02})` }} />
    </AbsoluteFill>
  );
};

/** Traço SVG desenhado de 0 a 1 (usa pathLength=1, então qualquer forma serve). */
export const Traco: React.FC<{ d: string; p: number; cor: string; w: number; tampa?: "round" | "butt" }> = ({ d, p, cor, w, tampa = "round" }) => (
  <path d={d} pathLength={1} fill="none" stroke={cor} strokeWidth={w} strokeLinecap={tampa} strokeLinejoin="round"
    strokeDasharray={1} strokeDashoffset={1 - Math.max(0, Math.min(1, p))} />
);

// ================================================================================================ QUADRO DE PROVAS
export type Prova = { src: string; x: number; y: number; rot: number; legenda?: string; cue: string; w?: number };
export type QuadroProvasProps = SceneProps & {
  titulo: string; tituloCue: string;          // etiqueta de papel rasgado ("INTELLIGENCE", "SUSPEITOS")
  provas: Prova[];                            // até 5 polaroides; x/y = centro
  fio?: boolean;                              // barbante vermelho ligando as tachas, na ordem
  tom?: "sepia" | "frio" | "pb";
};

export const QuadroProvas: React.FC<QuadroProvasProps> = (p) => {
  const f = useCurrentFrame();
  const t = p.tom ?? "sepia";
  const push = interpolate(f, [0, p.dur], [1, 1.07], clamp);
  const drift = interpolate(f, [0, p.dur], [0, -30], clamp);
  const ats = p.provas.map((pr, i) => cue(p, pr.cue, 0.06 + i * 0.16));
  const etiquetaAt = cue(p, p.tituloCue, 0.02);
  const pinos = p.provas.map((pr) => ({ x: pr.x - 6, y: pr.y - (pr.w ?? 420) * 0.62 }));
  return (
    <AbsoluteFill style={{ background: "#15110b", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${push}) translateX(${drift}px)` }}>
        {/* papel pautado do quadro */}
        <AbsoluteFill style={{ background: t === "frio" ? "#c9ccc8" : "#d9ccb2", filter: "brightness(0.72)",
          backgroundImage: "repeating-linear-gradient(0deg, rgba(60,45,25,0.13) 0 2px, transparent 2px 46px)" }} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 45% 40%, rgba(255,245,220,0.35), transparent 60%)" }} />
        {/* fio vermelho */}
        {p.fio ? (
          <svg width={1920} height={1080} style={{ position: "absolute" }}>
            {pinos.slice(1).map((b, i) => {
              const a = pinos[i];
              const pr = interpolate(f, [ats[i + 1] + 14, ats[i + 1] + 38], [0, 1], { ...clamp, easing: EXPO });
              const mx = (a.x + b.x) / 2, my = Math.max(a.y, b.y) + 60;
              return <Traco key={i} d={`M${a.x},${a.y} Q${mx},${my} ${b.x},${b.y}`} p={pr} cor="#9e1b16" w={4} />;
            })}
          </svg>
        ) : null}
        {/* polaroides */}
        {p.provas.map((pr, i) => {
          const at = ats[i];
          const s = spring({ frame: f - at, fps: 30, config: { damping: 14, stiffness: 90 } });
          const w = pr.w ?? 420;
          const vis = f >= at ? 1 : 0;
          const pino = spring({ frame: f - at - 10, fps: 30, config: { damping: 8, stiffness: 220 } });
          return (
            <div key={i} style={{ position: "absolute", left: pr.x - w / 2, top: pr.y - w * 0.62, width: w, opacity: vis,
              transform: `translateY(${(1 - s) * -160}px) scale(${1.25 - 0.25 * s}) rotate(${pr.rot + (1 - s) * 9}deg)`,
              transformOrigin: "50% 0%" }}>
              <div style={{ background: "#f3efe6", padding: `${w * 0.045}px ${w * 0.045}px ${w * 0.16}px`,
                boxShadow: `0 ${10 + 22 * s}px ${30 + 30 * s}px rgba(0,0,0,${0.35 + 0.25 * s})` }}>
                <Img src={src(pr.src)} style={{ width: "100%", height: w * 0.72, objectFit: "cover", filter: tom(t) }} />
                {pr.legenda ? <div style={{ fontFamily: MAO, fontSize: w * 0.07, color: "#2a2118", marginTop: w * 0.03,
                  textAlign: "center" }}>{pr.legenda}</div> : null}
              </div>
              <div style={{ position: "absolute", left: w / 2 - 17, top: -14, width: 34, height: 34, borderRadius: "50%",
                transform: `scale(${pino})`, background: "radial-gradient(circle at 35% 30%, #d8d2c4, #6d6556 55%, #2e2a23)",
                boxShadow: "3px 6px 8px rgba(0,0,0,0.55)" }} />
            </div>
          );
        })}
        {/* etiqueta de papel rasgado */}
        {(() => {
          const s = spring({ frame: f - etiquetaAt, fps: 30, config: { damping: 12, stiffness: 120 } });
          const lw = Math.min(1600, 160 + p.titulo.length * 64);
          const letras = Math.floor(interpolate(f, [etiquetaAt + 6, etiquetaAt + 6 + p.titulo.length * 2.2], [0, p.titulo.length], clamp));
          return (
            <div style={{ position: "absolute", left: 960 - lw / 2, top: 70, width: lw, height: 150, opacity: f >= etiquetaAt ? 1 : 0,
              transform: `rotate(${-4 + (1 - s) * -8}deg) scale(${0.8 + 0.2 * s})`,
              background: "#ece5d6", boxShadow: "0 18px 30px rgba(0,0,0,0.45)",
              clipPath: "polygon(2% 12%, 7% 4%, 14% 9%, 22% 2%, 31% 8%, 43% 3%, 55% 9%, 66% 2%, 78% 8%, 89% 3%, 98% 10%, 96% 38%, 100% 62%, 97% 90%, 88% 97%, 76% 92%, 63% 99%, 51% 93%, 38% 98%, 26% 92%, 14% 98%, 4% 91%, 1% 66%, 3% 40%)",
              display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ fontFamily: SERIFA, fontWeight: 700, fontSize: 72, letterSpacing: 10, color: "#3a3128" }}>
                {p.titulo.slice(0, letras)}</span>
            </div>
          );
        })()}
      </AbsoluteFill>
      <FilmeVelho />
    </AbsoluteFill>
  );
};

// ================================================================================================ CHECKLIST MANUSCRITO
export type ItemCheck = { texto: string; cue: string; marca: "check" | "x" | "risco" | "vazio" };
export type ChecklistProps = SceneProps & {
  fundo: string;                              // foto de época (public/...), vai em P&B com Ken Burns
  titulo: string;                             // "2ND SS PANZER CORPS", "ALVOS", "PROMESSAS"
  itens: ItemCheck[];                         // até 5
  cor?: string;                               // barra do cabeçalho e tinta das marcas
  lado?: "direita" | "esquerda";
};

export const Checklist: React.FC<ChecklistProps> = (p) => {
  const f = useCurrentFrame();
  const cor = p.cor ?? "#8e1f1a";
  const entra = spring({ frame: f - 6, fps: 30, config: { damping: 16, stiffness: 80 } });
  const esq = p.lado === "esquerda";
  const kb = interpolate(f, [0, p.dur], [1.08, 1.0], clamp);
  // 26/09/2026: todos os itens têm de terminar de ser escritos dentro do cartão (5 itens em 5 s cortavam os dois últimos)
  const n = p.itens.length;
  const ats = p.itens.map((it, i) => Math.max(cue(p, it.cue, 0.12 + (i * 0.56) / Math.max(1, n)), 18 + i * 8));
  const esc = (t: string) => Math.min(10 + t.length * 1.6, p.dur * 0.14);
  return (
    <AbsoluteFill style={{ background: "#0c0b0a", overflow: "hidden", ...exit(f, p.dur) }}>
      <Img src={src(p.fundo)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
        filter: `${tom("pb")} brightness(0.62)`, transform: `scale(${kb})` }} />
      <div style={{ position: "absolute", top: 150, [esq ? "left" : "right"]: 190, width: 760, paddingBottom: 10,
        background: "#f1e3dc", boxShadow: "18px 22px 0 rgba(90,20,15,0.55), 0 40px 70px rgba(0,0,0,0.6)",
        transform: `translateX(${(1 - entra) * (esq ? -900 : 900)}px) rotate(${(1 - entra) * 6 - 0.6}deg)` } as React.CSSProperties}>
        <div style={{ background: cor, color: "#fff", ...type.display, fontSize: 46, letterSpacing: 2, padding: "22px 34px" }}>
          {p.titulo}</div>
        <div style={{ padding: "30px 40px" }}>
          {p.itens.map((it, i) => {
            const at = ats[i];
            const escreve = interpolate(f, [at, at + esc(it.texto)], [0, 1], clamp);
            const marca = interpolate(f, [at + 2 + esc(it.texto), at + 14 + esc(it.texto)], [0, 1], { ...clamp, easing: EXPO });
            const risco = it.marca === "risco";
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", height: 92, opacity: f >= at - 4 ? 1 : 0 }}>
                <svg width={56} height={56} style={{ flex: "none", marginRight: 26 }}>
                  <rect x={4} y={4} width={44} height={44} fill="none" stroke={cor} strokeWidth={3.5} />
                  {it.marca === "check" ? <Traco d="M11,28 L23,40 L50,6" p={marca} cor={cor} w={6} /> : null}
                  {it.marca === "x" ? <><Traco d="M10,10 L44,44" p={marca * 2} cor={cor} w={6} />
                    <Traco d="M44,10 L10,44" p={marca * 2 - 1} cor={cor} w={6} /></> : null}
                </svg>
                <div style={{ position: "relative", fontFamily: MAO, fontSize: 46, color: "#241c16", whiteSpace: "nowrap" }}>
                  <span style={{ display: "inline-block", clipPath: `inset(0 ${100 - escreve * 100}% 0 0)` }}>{it.texto}</span>
                  {risco ? <svg width={it.texto.length * 26} height={20} style={{ position: "absolute", left: -6, top: 30 }}>
                    <Traco d={`M0,12 Q${it.texto.length * 6},4 ${it.texto.length * 13},11 T${it.texto.length * 26},8`} p={marca} cor={cor} w={6} />
                  </svg> : null}
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <FilmeVelho feixe={false} forca={0.8} />
    </AbsoluteFill>
  );
};

// ================================================================================================ FICHA COM NOME CIRCULADO
export type Campo = { rotulo: string; valor: string; tarja?: boolean };
export type FichaCirculoProps = SceneProps & {
  nome: string; nomeCue: string;              // "GEORGY ZHUKOV" — circulado à caneta
  orgao: string;                              // cabeçalho da ficha ("SOVIET HIGH COMMAND")
  campos: Campo[];                            // até 6; tarja = censurado
  relatorio?: number;                         // linhas de relatório (tarjas)
  foto?: string;
  carimbo?: string;                           // selo redondo ("STAVKA CONFIDENTIAL")
  modo?: "censurar" | "revelar";              // revelar = as tarjas saem e mostram o valor
  revelaCue?: string;
};

export const FichaCirculo: React.FC<FichaCirculoProps> = (p) => {
  const f = useCurrentFrame();
  const nomeAt = cue(p, p.nomeCue, 0.03);
  const nome = spring({ frame: f - nomeAt, fps: 30, config: { damping: 15, stiffness: 110 } });
  const circ = interpolate(f, [nomeAt + 14, nomeAt + 40], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const seta = interpolate(f, [nomeAt + 38, nomeAt + 56], [0, 1], { ...clamp, easing: EXPO });
  const ficha = spring({ frame: f - nomeAt - 34, fps: 30, config: { damping: 18, stiffness: 70 } });
  const tarjaAt = nomeAt + 58;
  const revAt = p.revelaCue ? cue(p, p.revelaCue, 0.6) : Math.round(p.dur * 0.6);
  const selo = spring({ frame: f - tarjaAt - 30, fps: 30, config: { damping: 9, stiffness: 200 } });
  const cam = interpolate(f, [0, p.dur], [1, 1.05], clamp);
  const larg = Math.min(1500, 90 + p.nome.length * 70);
  const Tarja: React.FC<{ i: number; w: number; texto?: string }> = ({ i, w, texto }) => {
    const cresce = interpolate(f, [tarjaAt + i * 4, tarjaAt + i * 4 + 12], [0, 1], { ...clamp, easing: EXPO });
    const some = p.modo === "revelar" ? interpolate(f, [revAt + i * 5, revAt + i * 5 + 14], [0, 1], { ...clamp, easing: EXPO }) : 0;
    return (
      <span style={{ position: "relative", display: "inline-block", width: w, height: 26, verticalAlign: "middle" }}>
        {texto ? <span style={{ position: "absolute", left: 0, top: -4, whiteSpace: "nowrap" }}>{texto}</span> : null}
        <span style={{ position: "absolute", top: 0, height: 26, background: "#0d0c0b",
          left: `${some * 100}%`, width: `${cresce * (1 - some) * 100}%` }} />
      </span>
    );
  };
  return (
    <AbsoluteFill style={{ background: "#dcdcd8", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${cam})` }}>
        <AbsoluteFill style={{ backgroundImage:
          "linear-gradient(rgba(90,90,90,0.18) 1px, transparent 1px), linear-gradient(90deg, rgba(90,90,90,0.18) 1px, transparent 1px)",
          backgroundSize: "34px 34px" }} />
        {/* nome */}
        <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center", ...type.display,
          fontSize: 150, letterSpacing: 4, color: "#161412", opacity: f >= nomeAt ? 1 : 0,
          transform: `scale(${1.3 - 0.3 * nome})`, filter: `blur(${(1 - nome) * 8}px)` }}>{p.nome}</div>
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <Traco d={`M${960 - larg / 2 - 20},300 C${960 - larg / 2 - 40},150 ${960 + larg / 2 + 50},140 ${960 + larg / 2 + 40},275
            C${960 + larg / 2 + 30},405 ${960 - larg / 2 - 70},415 ${960 - larg / 2 + 10},255`} p={circ} cor="#b3161b" w={9} />
          <Traco d={`M${960 + larg / 2 + 40},320 C${960 + larg / 2 + 80},380 ${960 + larg / 2 + 50},450 ${960 + larg / 2 - 20},520`} p={seta} cor="#b3161b" w={8} />
          {seta > 0.95 ? <path d={`M${960 + larg / 2 - 44},500 L${960 + larg / 2 - 20},522 L${960 + larg / 2 - 2},494`}
            fill="none" stroke="#b3161b" strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" /> : null}
        </svg>
        {/* ficha */}
        <div style={{ position: "absolute", left: 360, top: 370, width: 1200, height: 560, background: "#e4d3a8",
          boxShadow: "0 30px 60px rgba(0,0,0,0.4)", padding: "36px 56px", boxSizing: "border-box",
          transform: `translateY(${(1 - ficha) * 700}px)`, color: "#231d14", ...type.body, fontSize: 25 }}>
          <AbsoluteFill style={{ opacity: 0.3, backgroundImage: "repeating-linear-gradient(90deg, rgba(0,0,0,0.04) 0 3px, transparent 3px 9px)" }} />
          <div style={{ ...type.bodyBold, fontSize: 30, letterSpacing: 3, borderBottom: "2px solid #6b5a3a", paddingBottom: 14 }}>{p.orgao}</div>
          <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", rowGap: 16, marginTop: 24, width: 780 }}>
            {p.campos.map((c, i) => (
              <React.Fragment key={i}>
                <div style={{ opacity: 0.75 }}>{c.rotulo}</div>
                <div style={{ ...type.bodyBold }}>{c.tarja ? <Tarja i={i} w={Math.max(160, c.valor.length * 17)} texto={p.modo === "revelar" ? c.valor : undefined} /> : c.valor}</div>
              </React.Fragment>
            ))}
          </div>
          {p.relatorio ? <div style={{ marginTop: 26, borderTop: "2px solid #6b5a3a", paddingTop: 16 }}>
            <div style={{ ...type.bodyBold, marginBottom: 12 }}>Report</div>
            {Array.from({ length: p.relatorio }, (_, i) => <div key={i} style={{ marginBottom: 10 }}><Tarja i={p.campos.length + i} w={i % 2 ? 760 : 1040} /></div>)}
          </div> : null}
          {p.foto ? <div style={{ position: "absolute", right: 56, top: 110, width: 190, height: 240, background: "#f4efe4",
            padding: 8, transform: "rotate(2deg)", boxShadow: "0 8px 16px rgba(0,0,0,0.35)" }}>
            <Img src={src(p.foto)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: tom("sepia") }} />
            <div style={{ position: "absolute", left: 80, top: -22, width: 26, height: 70, border: "4px solid #8d8f93",
              borderRadius: 14 }} /></div> : null}
          {p.carimbo ? <div style={{ position: "absolute", right: 280, top: 20, width: 150, height: 150, borderRadius: "50%",
            border: "5px solid rgba(120,40,30,0.75)", color: "rgba(120,40,30,0.8)", display: "flex", alignItems: "center",
            justifyContent: "center", textAlign: "center", ...type.bodyBold, fontSize: 19, letterSpacing: 2, lineHeight: 1.2,
            opacity: f >= tarjaAt + 30 ? 0.9 : 0, transform: `scale(${interpolate(selo, [0, 1], [2.2, 1])}) rotate(-14deg)`,
            mixBlendMode: "multiply" }}>{p.carimbo}</div> : null}
        </div>
      </AbsoluteFill>
      <FilmeVelho feixe={false} forca={0.6} />
    </AbsoluteFill>
  );
};
