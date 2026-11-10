// ESTILOS NOSTALGIA / MARCAS ANTIGAS (04/10/2026) — cartões de tela cheia para o canal "TV Nostalgia"
// (colapso de marcas e indústrias brasileiras, propaganda antiga, TV dos anos 70-90, preços de outra moeda).
//   TvTubo          — televisor de tubo com gabinete de madeira numa sala escura: liga com a linha branca, foto curva + OSD do canal.
//   AnuncioRevista  — anúncio de revista em página dupla amarelada: foto em retícula, chamada, marca, selo de preço e ano.
//   Polaroids       — 2 a 4 fotos instantâneas caem na mesa, quicam, revelam a cor e ganham legenda à caneta.
//   EvolucaoMarca   — linha do tempo da marca: cursor corre pelo trilho, cada ano mostra o letreiro na tipografia da época; FIM em vermelho.
//   EtiquetaPreco   — etiqueta de maquininha de supermercado: preço antigo riscado à caneta, novo carimbado, multiplicador contando.
// Mesmas regras do estilos5.tsx: todo texto vem das props (todo número tem de ser DITO na narração), entrada nos
// primeiros ~20 quadros, tudo legível até ~45, saída por exit(f, p.dur).
import React from "react";
import {
  AbsoluteFill, Img, cancelRender, continueRender, delayRender, interpolate, random, spring, staticFile, useCurrentFrame,
} from "remotion";
import { Easing } from "remotion";
import { type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, MAO, SERIFA, Traco, clamp, src } from "./arquivo";

const MONO = "'Courier Prime', 'Courier New', monospace";
const ent = (f: number, a: number, b = a + 14) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: EXPO });
const INOUT = Easing.inOut(Easing.cubic);

// Fontes de época que já estão em public/fonts (locais, sem rede). Carregadas uma vez, como em design/tokens.ts.
const ANTON = "'Anton', 'Oswald', Impact, sans-serif";
const ARCHIVO = "'Archivo Black', 'Arial Black', sans-serif";
const BEBAS = "'Bebas Neue', 'Oswald', sans-serif";
const SCRIPT = "'Brush Script MT', 'Segoe Script', cursive";   // fonte do Windows (como MAO)
const PLEX = "'IBM Plex Sans', 'Segoe UI', sans-serif";
if (typeof document !== "undefined" && typeof FontFace !== "undefined") {
  const w = window as unknown as { __fontesNostalgia?: boolean };
  if (!w.__fontesNostalgia) {
    w.__fontesNostalgia = true;
    const h = delayRender("fontes nostalgia");
    Promise.all(([["Anton", "Anton.ttf"], ["Archivo Black", "ArchivoBlack.ttf"], ["Bebas Neue", "BebasNeue.ttf"]] as const).map(
      ([fam, file]) => new FontFace(fam, `url(${staticFile(`fonts/${file}`)}) format("truetype")`).load().then((l) => document.fonts.add(l)),
    )).then(() => continueRender(h)).catch((err) => cancelRender(err));
  }
}

/** Grão leve de filme/papel (sem vinheta nem feixe). */
const Grao: React.FC<{ forca?: number; id: string }> = ({ forca = 1, id }) => {
  const f = useCurrentFrame();
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, opacity: 0.14 * forca, mixBlendMode: "overlay",
      pointerEvents: "none" }}>
      <filter id={`${id}${f % 5}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f % 89} /></filter>
      <rect width="100%" height="100%" filter={`url(#${id}${f % 5})`} />
    </svg>
  );
};

/** Tamanho de fonte que cabe em `largura` (k = largura média do caractere em em). */
const caber = (t: string, largura: number, max: number, k: number, min = 34) =>
  Math.max(min, Math.min(max, largura / (Math.max(1, t.length) * k)));

// ================================================================================================ TV DE TUBO
export type TvTuboProps = SceneProps & { src: string; canal?: string; legenda?: string };
/** Televisor de tubo com gabinete de madeira, antena e botões numa sala escura. Liga com o ponto e a linha branca,
 *  abre a foto com curvatura, linhas de varredura e brilho; OSD verde do canal; legenda embaixo. Desliga no fim. */
export const TvTubo: React.FC<TvTuboProps> = (p) => {
  const f = useCurrentFrame();
  const CW = 1180, CH = 690, CX = (1920 - CW) / 2, CY = 120;          // gabinete
  const SX = 64, SY = 58, SW = 768, SH = 574;                         // tela (relativa ao gabinete), 4:3
  const PX = SX + SW + 70;                                            // painel lateral
  const PW = CW - PX - 52;
  // liga: ponto (6) → linha (8-14) → abre (14-22) | desliga: fecha (dur-16) → linha → ponto
  const lw = interpolate(f, [7, 13], [0.004, 1], { ...clamp, easing: EXPO }) * interpolate(f, [p.dur - 10, p.dur - 6], [1, 0.004], clamp);
  const lh = interpolate(f, [13, 22], [0.008, 1], { ...clamp, easing: EXPO }) * interpolate(f, [p.dur - 16, p.dur - 10], [1, 0.008], clamp);
  const ligada = f >= 6 && f < p.dur - 4;
  const branco = interpolate(f, [13, 24], [1, 0], clamp) + interpolate(f, [p.dur - 16, p.dur - 10], [0, 1], clamp);
  const flash = interpolate(f, [14, 20, 34], [2.2, 1.35, 1], clamp);
  const flick = 1 + (random(`tv${f}`) - 0.5) * 0.05;
  const brilho = (ligada ? 1 : 0) * interpolate(f, [12, 24], [0, 1], clamp);
  const push = interpolate(f, [0, p.dur], [1, 1.045], clamp);
  const sala = ent(f, 0, 10);
  const knob = spring({ frame: f - 20, fps: 30, config: { damping: 11, stiffness: 140 } });
  const osd = f >= 22 && f < p.dur * 0.62 ? (f < 30 ? (f % 4 < 2 ? 1 : 0.3) : 1) : 0;
  const leg = p.legenda ?? "";
  const legFs = caber(leg, 1500, 46, 0.6);
  const banda = ((f * 9) % (SH + 200)) - 100;
  return (
    <AbsoluteFill style={{ background: "#0b0705", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: sala, transform: `scale(${push})`, transformOrigin: `960px ${CY + SY + SH / 2}px` }}>
        {/* sala: papel de parede listrado, abajur à esquerda, rodapé e piso */}
        <AbsoluteFill style={{ background: "#2a1b12", backgroundImage:
          "repeating-linear-gradient(90deg, rgba(255,214,160,0.05) 0 30px, rgba(0,0,0,0.06) 30px 34px, transparent 34px 64px)" }} />
        <AbsoluteFill style={{ background: "radial-gradient(circle at 7% 22%, rgba(255,178,92,0.42), rgba(255,150,70,0.12) 22%, transparent 46%)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 850, bottom: 0,
          background: "linear-gradient(180deg, #3a2618 0, #3a2618 10px, #1a110b 10px, #0d0805)" }} />
        <AbsoluteFill style={{ background: `radial-gradient(ellipse 900px 520px at 960px ${CY + SY + SH / 2}px, rgba(150,185,255,${0.2 * brilho * flick}), transparent 70%)`,
          mixBlendMode: "screen" }} />
        {/* antena "orelha de coelho" */}
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
          <defs><linearGradient id="nosCromo" x1="0" x2="1"><stop offset="0" stopColor="#6f6a63" /><stop offset="0.5" stopColor="#e9e4da" />
            <stop offset="1" stopColor="#7b756c" /></linearGradient></defs>
          {[[-1, 330, -20], [1, 330, -20]].map(([s, dx]) => {
            const bx = CX + CW * 0.66, by = CY - 26;
            return <g key={s}><line x1={bx} y1={by} x2={bx + s * dx} y2={-20} stroke="url(#nosCromo)" strokeWidth={6} strokeLinecap="round" /></g>;
          })}
          <ellipse cx={CX + CW * 0.66} cy={CY - 12} rx={70} ry={22} fill="#1d1a17" />
          <ellipse cx={CX + CW * 0.66} cy={CY - 20} rx={56} ry={14} fill="#38332d" />
        </svg>
        {/* pés palito */}
        {[CX + 110, CX + CW - 150].map((x, i) => (
          <div key={i} style={{ position: "absolute", left: x, top: CY + CH - 6, width: 40, height: 74, background: "linear-gradient(90deg, #2b1a0f, #5a3b24 45%, #2b1a0f)",
            clipPath: i ? "polygon(0 0, 100% 0, 92% 100%, 62% 100%)" : "polygon(0 0, 100% 0, 38% 100%, 8% 100%)" }} />
        ))}
        {/* gabinete de madeira */}
        <div style={{ position: "absolute", left: CX, top: CY, width: CW, height: CH, borderRadius: 26, overflow: "hidden",
          boxShadow: "0 40px 70px rgba(0,0,0,0.75), inset 0 3px 0 rgba(255,220,170,0.25), inset 0 -6px 0 rgba(0,0,0,0.4)",
          background: "linear-gradient(180deg, rgba(255,230,190,0.10), rgba(0,0,0,0.30)), repeating-linear-gradient(91deg, #5c3b22 0 4px, #6d472a 4px 11px, #50331d 11px 13px, #66432a 13px 23px)" }}>
          <svg width={CW} height={CH} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply", opacity: 0.55 }}>
            <filter id="nosMadeira"><feTurbulence type="fractalNoise" baseFrequency="0.0025 0.09" numOctaves={3} seed={7} />
              <feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.28  0 0 0 0 0.15  0 0 0 1.4 -0.2" /></filter>
            <rect width="100%" height="100%" filter="url(#nosMadeira)" />
          </svg>
          {/* reflexo da luz do abajur no verniz */}
          <div style={{ position: "absolute", inset: 0, background: "linear-gradient(110deg, rgba(255,200,140,0.22), transparent 30%)" }} />
          {/* moldura da tela */}
          <div style={{ position: "absolute", left: SX - 30, top: SY - 30, width: SW + 60, height: SH + 60, borderRadius: "84px / 72px",
            background: "linear-gradient(160deg, #3a3631, #121110 55%, #23201d)",
            boxShadow: "inset 0 4px 10px rgba(255,255,255,0.12), inset 0 -8px 18px rgba(0,0,0,0.8), 0 2px 0 rgba(255,220,170,0.15)" }} />
          {/* tela */}
          <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, borderRadius: "70px / 60px", overflow: "hidden",
            background: "radial-gradient(ellipse at 45% 40%, #2a302c, #0f1210 75%)",
            boxShadow: `0 0 ${50 * brilho}px ${10 * brilho}px rgba(160,190,255,${0.25 * brilho})` }}>
            {ligada ? (
              <div style={{ position: "absolute", inset: 0,
                clipPath: `inset(${((1 - lh) * 50).toFixed(3)}% ${((1 - lw) * 50).toFixed(3)}% round 12px)` }}>
                <Img src={src(p.src)} style={{ position: "absolute", left: -SW * 0.04, top: -SH * 0.04, width: SW * 1.08, height: SH * 1.08,
                  objectFit: "cover", filter: `saturate(1.35) contrast(1.12) brightness(${flash * flick}) blur(0.7px)` }} />
                <Img src={src(p.src)} style={{ position: "absolute", left: -SW * 0.04 + 4, top: -SH * 0.04, width: SW * 1.08, height: SH * 1.08,
                  objectFit: "cover", mixBlendMode: "screen", opacity: 0.22, filter: "grayscale(1) sepia(1) hue-rotate(-40deg) saturate(5) blur(1px)" }} />
                <Img src={src(p.src)} style={{ position: "absolute", left: -SW * 0.04, top: -SH * 0.04, width: SW * 1.08, height: SH * 1.08,
                  objectFit: "cover", mixBlendMode: "screen", opacity: 0.32, filter: "blur(14px) brightness(1.1)" }} />
                <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: Math.min(1, branco) }} />
                {/* máscara de fósforo + varredura + faixa de rolagem */}
                <div style={{ position: "absolute", inset: 0, backgroundImage:
                  "repeating-linear-gradient(90deg, rgba(255,60,60,0.07) 0 1px, rgba(60,255,60,0.07) 1px 2px, rgba(60,60,255,0.07) 2px 3px)" }} />
                <div style={{ position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(rgba(0,0,0,0.32) 0 2px, transparent 2px 4px)" }} />
                <div style={{ position: "absolute", left: 0, right: 0, top: banda, height: 90,
                  background: "linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0.07), rgba(255,255,255,0))" }} />
                {p.canal ? (
                  <div style={{ position: "absolute", right: 56, top: 44, fontFamily: MONO, fontWeight: 700, fontSize: 64, color: "#86ff74",
                    letterSpacing: 2, opacity: osd, textShadow: "0 0 14px rgba(134,255,116,0.85), 4px 4px 0 rgba(0,0,0,0.85)" }}>{p.canal}</div>
                ) : null}
              </div>
            ) : null}
            {/* ponto de luz ao ligar e ao desligar */}
            {f >= 5 && f < 10 || f >= p.dur - 8 && f < p.dur - 3 ? (
              <div style={{ position: "absolute", left: SW / 2 - 9, top: SH / 2 - 9, width: 18, height: 18, borderRadius: 9, background: "#fff",
                boxShadow: "0 0 30px 12px rgba(220,235,255,0.9)" }} />
            ) : null}
            {/* curvatura: vinheta forte + reflexo do vidro */}
            <div style={{ position: "absolute", inset: 0, borderRadius: "70px / 60px",
              background: "radial-gradient(ellipse 62% 64% at 50% 50%, transparent 62%, rgba(0,0,0,0.72) 100%)",
              boxShadow: "inset 0 0 40px 8px rgba(0,0,0,0.75)" }} />
            <div style={{ position: "absolute", left: "6%", top: "4%", width: "62%", height: "40%", borderRadius: "50%",
              background: "radial-gradient(ellipse at 40% 35%, rgba(255,255,255,0.16), transparent 70%)" }} />
            <div style={{ position: "absolute", inset: 0, background: "linear-gradient(155deg, rgba(255,240,220,0.10) 0%, transparent 28%)" }} />
          </div>
          {/* painel: botões, luz de força e grade do alto-falante */}
          <div style={{ position: "absolute", left: PX, top: SY - 30, width: PW, height: SH + 60, borderRadius: 18,
            background: "linear-gradient(180deg, #2a2420, #15110e)", boxShadow: "inset 0 2px 6px rgba(255,255,255,0.08), inset 0 -4px 10px rgba(0,0,0,0.6)" }}>
            {[{ y: 120, r: 74, rot: -40 + 70 * knob }, { y: 300, r: 54, rot: 30 }].map((k, i) => (
              <div key={i} style={{ position: "absolute", left: PW / 2 - k.r, top: k.y - k.r, width: 2 * k.r, height: 2 * k.r }}>
                <svg width={2 * k.r + 40} height={2 * k.r + 40} style={{ position: "absolute", left: -20, top: -20 }}>
                  {Array.from({ length: i ? 7 : 12 }, (_, j) => {
                    const a = ((i ? -120 + j * 40 : j * 30) * Math.PI) / 180, R1 = k.r + 8, R2 = k.r + 16;
                    return <line key={j} x1={k.r + 20 + R1 * Math.sin(a)} y1={k.r + 20 - R1 * Math.cos(a)} x2={k.r + 20 + R2 * Math.sin(a)}
                      y2={k.r + 20 - R2 * Math.cos(a)} stroke="rgba(230,215,190,0.55)" strokeWidth={3} strokeLinecap="round" />;
                  })}
                </svg>
                <div style={{ position: "absolute", inset: 0, borderRadius: "50%", transform: `rotate(${k.rot}deg)`,
                  background: "conic-gradient(from 0deg, #8f8a82, #d9d3c8, #6e6a63, #c9c2b6, #7a756d, #e2dccf, #8f8a82)",
                  boxShadow: "0 8px 14px rgba(0,0,0,0.7), inset 0 0 0 6px rgba(0,0,0,0.25)" }}>
                  <div style={{ position: "absolute", left: "50%", top: 8, width: 8, marginLeft: -4, height: k.r * 0.7, borderRadius: 4, background: "#1b1714" }} />
                  <div style={{ position: "absolute", inset: k.r * 0.32, borderRadius: "50%", background: "radial-gradient(circle at 35% 30%, #4a4540, #191613)" }} />
                </div>
              </div>
            ))}
            <div style={{ position: "absolute", left: PW / 2 - 9, top: 400, width: 18, height: 18, borderRadius: 9,
              background: ligada ? "#ff3b2a" : "#4a1410", boxShadow: ligada ? "0 0 16px 4px rgba(255,59,42,0.75)" : "none" }} />
            <div style={{ position: "absolute", left: 24, right: 24, top: 448, bottom: 26, borderRadius: 10,
              backgroundImage: "repeating-linear-gradient(0deg, #0c0a08 0 6px, #3a332c 6px 9px)", boxShadow: "inset 0 3px 8px rgba(0,0,0,0.8)" }} />
          </div>
        </div>
        <Grao id="nosGtv" forca={0.8} />
        <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.7) 100%)" }} />
      </AbsoluteFill>
      {leg ? (
        <div style={{ position: "absolute", left: 120, right: 120, top: 916, textAlign: "center", opacity: ent(f, 22, 36),
          transform: `translateY(${(1 - ent(f, 22, 36)) * 16}px)` }}>
          <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: legFs, color: "#f3e3c3", lineHeight: 1.2,
            textShadow: "0 3px 10px rgba(0,0,0,0.9)" }}>{leg}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ================================================================================================ ANÚNCIO DE REVISTA
export type AnuncioRevistaProps = SceneProps & { src: string; chamada: string; marca: string; preco?: string; ano: string; rodape?: string };
/** Página dupla de revista antiga: foto em retícula à esquerda; à direita chamada retrô, letreiro da marca com
 *  faixas setentistas, selo estourado com o preço na moeda da época, letra miúda e o ano no canto. Canto dobrado. */
export const AnuncioRevista: React.FC<AnuncioRevistaProps> = (p) => {
  const f = useCurrentFrame();
  const W = 1620, H = 900, X = (1920 - W) / 2, Y = 92, PG = W / 2;
  const g = spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 70 } });
  const cam = interpolate(f, [0, p.dur], [1, 1.03], clamp);
  const pan = interpolate(f, [0, p.dur], [0, -14], clamp);
  const IN = 74;                                                      // margem interna da página direita
  const largTexto = PG - 2 * IN;
  const chFs = p.chamada.length <= 22 ? 104 : p.chamada.length <= 44 ? 86 : p.chamada.length <= 70 ? 70 : 58;
  const SEL = 270;                                                    // selo estourado do preço
  const larguraMarca = p.preco ? largTexto - SEL - 30 : largTexto;
  const mFs = caber(p.marca, larguraMarca, 120, 0.78, 44);
  const selo = spring({ frame: f - 30, fps: 30, config: { damping: 9, stiffness: 160 } });
  const pFs = p.preco ? caber(p.preco, SEL - 70, 64, 0.46, 34) : 0;
  const tinta = (a: number) => ({ opacity: ent(f, a, a + 10), filter: `blur(${(1 - ent(f, a, a + 10)) * 6}px)` });
  const DOBRA = 120;
  const estrela = Array.from({ length: 48 }, (_, i) => {
    const a = (i / 48) * Math.PI * 2, r = (i % 2 ? 0.85 : 1) * (SEL / 2 - 2);
    return `${SEL / 2 + r * Math.cos(a)},${SEL / 2 + r * Math.sin(a)}`;
  }).join(" ");
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 55% 45%, #3a3129, #14100d 75%)", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${cam}) translateX(${pan}px)`, perspective: 2200 }}>
        <div style={{ position: "absolute", left: X, top: Y, width: W, height: H, opacity: ent(f, 0, 8),
          transform: `translateY(${(1 - g) * 140}px) rotateX(${(1 - g) * 16}deg) rotate(${-0.8 + (1 - g) * -3}deg)`, transformOrigin: "50% 100%" }}>
          {/* sombra da revista na mesa */}
          <div style={{ position: "absolute", inset: 0, boxShadow: "0 40px 80px rgba(0,0,0,0.75), 0 8px 18px rgba(0,0,0,0.5)" }} />
          {/* página esquerda: foto sangrada em retícula */}
          <div style={{ position: "absolute", left: 0, top: 0, width: PG, height: H, overflow: "hidden", background: "#e9dcb9" }}>
            <Img src={src(p.src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
              filter: "sepia(0.28) saturate(0.95) contrast(1.18) brightness(1.03) hue-rotate(-6deg)",
              transform: `scale(${interpolate(f, [0, p.dur], [1.08, 1.0], clamp)})` }} />
            <AbsoluteFill style={{ backgroundImage: "radial-gradient(circle, rgba(40,26,12,0.36) 1.1px, transparent 1.7px)",
              backgroundSize: "6px 6px", mixBlendMode: "multiply" }} />
            <AbsoluteFill style={{ background: "#f0d9a0", mixBlendMode: "multiply", opacity: 0.22 }} />
            <AbsoluteFill style={{ background: "linear-gradient(90deg, transparent 80%, rgba(0,0,0,0.45))" }} />
            <svg width={PG} height={H} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply", opacity: 0.4 }}>
              <rect width="100%" height="100%" filter="url(#nosPapel)" />
            </svg>
          </div>
          {/* página direita: papel amarelado */}
          <div style={{ position: "absolute", left: PG, top: 0, width: PG, height: H, overflow: "hidden",
            clipPath: `polygon(0 0, 100% 0, 100% calc(100% - ${DOBRA}px), calc(100% - ${DOBRA}px) 100%, 0 100%)`,
            background: "radial-gradient(ellipse at 45% 40%, #f4e9cc, #e8d6a8 70%, #d6bd85)" }}>
            <AbsoluteFill style={{ background: "linear-gradient(270deg, transparent 84%, rgba(60,40,15,0.38))" }} />
            {/* ano no canto */}
            <div style={{ position: "absolute", right: IN, top: 54, fontFamily: MONO, fontWeight: 700, fontSize: 38, color: "#3a2e1f",
              border: "3px solid #3a2e1f", padding: "2px 16px", letterSpacing: 3, ...tinta(16) }}>{p.ano}</div>
            {/* chamada */}
            <div style={{ position: "absolute", left: IN, top: 150, width: largTexto, fontFamily: SERIFA, fontWeight: 700, fontStyle: "italic",
              fontSize: chFs, lineHeight: 1.04, color: "#1f1a14", letterSpacing: -1, ...tinta(12) }}>{p.chamada}</div>
            {/* letreiro da marca + faixas */}
            <div style={{ position: "absolute", left: IN, bottom: 250, width: larguraMarca, ...tinta(22) }}>
              <div style={{ fontFamily: ARCHIVO, fontSize: mFs, lineHeight: 1, color: "#b02a22", letterSpacing: -2, textTransform: "uppercase",
                whiteSpace: "nowrap" }}>{p.marca}</div>
              {["#e0882a", "#c4471f", "#7a3417"].map((c, i) => (
                <div key={i} style={{ height: 11, marginTop: i ? 5 : 16, background: c,
                  width: `${100 * ent(f, 24 + i * 3, 40 + i * 3)}%` }} />
              ))}
            </div>
            {/* letra miúda */}
            {p.rodape ? (
              <div style={{ position: "absolute", left: IN, right: IN + 40, bottom: 70, fontFamily: MONO, fontSize: 34, lineHeight: 1.18,
                color: "#4a3d2b", ...tinta(32) }}>{p.rodape}</div>
            ) : null}
            <svg width={PG} height={H} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply", opacity: 0.35 }}>
              <filter id="nosPapel"><feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves={3} seed={3} />
                <feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.42  0 0 0 0 0.25  0 0 0 0.5 0" /></filter>
              <rect width="100%" height="100%" filter="url(#nosPapel)" />
              {[0, 1, 2, 3, 4].map((i) => <circle key={i} cx={random(`fx${i}`) * PG} cy={random(`fy${i}`) * H} r={4 + random(`fr${i}`) * 9}
                fill="rgba(140,90,30,0.35)" />)}
            </svg>
          </div>
          {/* selo do preço */}
          {p.preco ? (
            <div style={{ position: "absolute", left: W - IN - SEL + 10, top: H - 250 - SEL * 0.62, width: SEL, height: SEL, opacity: f >= 30 ? 1 : 0,
              transform: `scale(${interpolate(selo, [0, 1], [1.8, 1])}) rotate(${-12 + (1 - selo) * 30}deg)` }}>
              <svg width={SEL} height={SEL} style={{ position: "absolute", filter: "drop-shadow(4px 6px 0 rgba(90,30,10,0.35))" }}>
                <polygon points={estrela} fill="#f2c230" stroke="#b02a22" strokeWidth={5} />
                <circle cx={SEL / 2} cy={SEL / 2} r={SEL * 0.36} fill="none" stroke="#b02a22" strokeWidth={3} strokeDasharray="2 8" />
              </svg>
              <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: ANTON, fontSize: pFs, color: "#9e1d17", textAlign: "center", lineHeight: 1, padding: 30 }}>{p.preco}</div>
            </div>
          ) : null}
          {/* canto dobrado */}
          <div style={{ position: "absolute", left: W - DOBRA, top: H - DOBRA, width: DOBRA, height: DOBRA,
            background: "linear-gradient(315deg, transparent 50%, #c9b27c 50%, #efe1bd 78%, #d8c08a)",
            filter: "drop-shadow(-6px -6px 8px rgba(0,0,0,0.35))" }} />
          {/* lombada */}
          <div style={{ position: "absolute", left: PG - 70, top: 0, width: 140, height: H,
            background: "linear-gradient(90deg, transparent, rgba(0,0,0,0.30) 46%, rgba(255,240,210,0.18) 52%, transparent)" }} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 60%, rgba(0,0,0,0.55) 100%)" }} />
      <Grao id="nosGrev" forca={0.7} />
    </AbsoluteFill>
  );
};

// ================================================================================================ POLAROIDS
export type PolaroidFoto = { src: string; legenda: string };
export type PolaroidsProps = SceneProps & { fotos: PolaroidFoto[]; titulo?: string };
/** Mesa de madeira vista de cima sob luz de abajur: 2 a 4 fotos instantâneas caem uma a uma (sombra encolhe, quique),
 *  a imagem revela a cor e a legenda é escrita à caneta na borda branca. Título opcional em fita crepe. */
export const Polaroids: React.FC<PolaroidsProps> = (p) => {
  const f = useCurrentFrame();
  const fotos = p.fotos.slice(0, 4);
  const n = Math.max(1, fotos.length);
  const W = n <= 2 ? 520 : n === 3 ? 460 : 390;
  const M = W * 0.06, FOTO = W - 2 * M, BASE = W * 0.28, H = M + FOTO + BASE;
  const cy0 = p.titulo ? 590 : 545;
  const span = n <= 2 ? 1180 : 1640;
  const cam = interpolate(f, [0, p.dur], [1.04, 1.0], clamp);
  return (
    <AbsoluteFill style={{ background: "#1a0f08", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `scale(${cam}) rotate(${interpolate(f, [0, p.dur], [0.6, 0], clamp)}deg)` }}>
        {/* mesa de madeira */}
        <AbsoluteFill style={{ background: "#4a2e1a", backgroundImage:
          "repeating-linear-gradient(0deg, transparent 0 266px, rgba(0,0,0,0.5) 266px 269px, rgba(255,210,160,0.06) 269px 271px)" }} />
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "multiply", opacity: 0.75 }}>
          <filter id="nosMesa"><feTurbulence type="fractalNoise" baseFrequency="0.0018 0.05" numOctaves={4} seed={11} />
            <feColorMatrix values="0 0 0 0 0.42  0 0 0 0 0.25  0 0 0 0 0.13  0 0 0 1.5 -0.25" /></filter>
          <rect width="100%" height="100%" filter="url(#nosMesa)" />
          <circle cx={1660} cy={180} r={92} fill="none" stroke="rgba(60,30,10,0.35)" strokeWidth={10} />
          <circle cx={1664} cy={184} r={84} fill="none" stroke="rgba(60,30,10,0.18)" strokeWidth={4} />
        </svg>
        <AbsoluteFill style={{ background: "radial-gradient(ellipse 1100px 760px at 48% 50%, rgba(255,196,120,0.30), transparent 70%)" }} />
        {fotos.map((ft, i) => {
          const at = 3 + i * 8;
          const s = spring({ frame: f - at, fps: 30, config: { damping: 9, stiffness: 130, mass: 0.8 } });
          const sinal = i % 2 ? 1 : -1;
          const rot = sinal * (3 + random(`pr${i}`) * 5);
          const cx = 960 + (n === 1 ? 0 : (i / (n - 1) - 0.5) * (span - W));
          const cy = cy0 + (i % 2 ? 26 : -22);
          const alto = 1 - s;                                         // altura da queda: 1 = perto da câmera
          const rev = interpolate(f, [at + 6, at + 34], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
          const esc = ent(f, at + 12, at + 26);
          // legenda: 1 linha se couber; senão 2 linhas (Segoe Print ≈ 0,55 em por caractere)
          const L = Math.max(4, ft.legenda.length);
          const umaLinha = Math.min(W * 0.11, BASE * 0.6, (FOTO * 0.95) / (L * 0.55));
          const fs = umaLinha >= 38 ? umaLinha : Math.max(34, Math.min(BASE / 2.5, (2.6 * FOTO) / L));
          return (
            <div key={i} style={{ position: "absolute", left: cx - W / 2, top: cy - H / 2, width: W, height: H, opacity: ent(f, at, at + 4),
              transform: `translate(${alto * sinal * -60}px, ${alto * -90}px) scale(${1 + alto * 0.45}) rotate(${rot + alto * sinal * 14}deg)` }}>
              <div style={{ position: "absolute", inset: 0, background: "linear-gradient(160deg, #fbf8f0, #ece6d8)",
                boxShadow: `${10 + alto * 50}px ${14 + alto * 70}px ${14 + alto * 60}px rgba(0,0,0,${0.55 - alto * 0.25}), 0 1px 2px rgba(0,0,0,0.4)` }} />
              <div style={{ position: "absolute", left: M, top: M, width: FOTO, height: FOTO, overflow: "hidden", background: "#2e3833" }}>
                <Img src={src(ft.src)} style={{ width: "100%", height: "100%", objectFit: "cover",
                  filter: `sepia(${0.2 + (1 - rev) * 0.5}) saturate(${0.25 + rev * 0.9}) contrast(${0.75 + rev * 0.3}) brightness(${0.55 + rev * 0.5})` }} />
                <AbsoluteFill style={{ background: "#33433d", opacity: (1 - rev) * 0.85 }} />
                <AbsoluteFill style={{ background: "linear-gradient(140deg, rgba(255,190,110,0.16), rgba(60,110,130,0.14))", mixBlendMode: "screen" }} />
                <AbsoluteFill style={{ boxShadow: "inset 0 0 40px rgba(0,0,0,0.45)" }} />
              </div>
              <div style={{ position: "absolute", left: M, right: M, top: M + FOTO, height: BASE, display: "flex", alignItems: "center",
                justifyContent: "center", textAlign: "center", fontFamily: MAO, fontSize: fs, lineHeight: 1.08, color: "#1e2a5c",
                clipPath: `inset(0 ${100 - esc * 100}% 0 0)`, transform: `rotate(${-sinal * 1.2}deg)` }}>{ft.legenda}</div>
            </div>
          );
        })}
        {p.titulo ? (() => {
          const t = ent(f, 0, 12);
          const fs = caber(p.titulo, 1100, 64, 0.58, 40);
          return (
            <div style={{ position: "absolute", left: 0, right: 0, top: 96, display: "flex", justifyContent: "center", opacity: t }}>
              <div style={{ background: "rgba(228,214,170,0.94)", padding: "10px 70px 16px", transform: `rotate(-1.6deg) scaleX(${0.6 + 0.4 * t})`,
                boxShadow: "0 6px 14px rgba(0,0,0,0.4)", fontFamily: MAO, fontSize: fs, color: "#2a2620", whiteSpace: "nowrap",
                clipPath: "polygon(1% 8%, 4% 0, 97% 4%, 100% 14%, 98% 40%, 100% 66%, 97% 100%, 3% 94%, 0 70%, 2% 38%)" }}>{p.titulo}</div>
            </div>
          );
        })() : null}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 48%, transparent 50%, rgba(0,0,0,0.72) 100%)" }} />
      <Grao id="nosGpol" forca={0.6} />
    </AbsoluteFill>
  );
};

// ================================================================================================ EVOLUÇÃO DA MARCA
export type MarcaItem = { ano: string; rotulo: string; src?: string; fim?: boolean };
export type EvolucaoMarcaProps = SceneProps & { titulo: string; itens: MarcaItem[] };

type Era = { bg: string; cor: string; fonte: string; peso: number; italico?: boolean; caixa?: "upper" | "lower" | "none";
  k: number; max: number; extra?: React.CSSProperties; borda?: string; foto: string; deco?: "faixas" | "neon" | "onda" };
/** Tipografia/cor do letreiro conforme a década do ano (o ano pode vir como "1975", "anos 80"...). */
const eraDe = (ano: string, i: number): Era => {
  const m = ano.match(/\d{4}/) ?? ano.match(/\d{2}/);
  let y = m ? parseInt(m[0], 10) : 1950 + i * 10;
  if (y < 100) y += 1900;
  if (y < 1960) return { bg: "#efe3c6", cor: "#7a1f1a", fonte: SERIFA, peso: 700, italico: true, k: 0.7, max: 72,
    borda: "6px double #7a1f1a", foto: "grayscale(1) sepia(0.5) contrast(1.1)" };
  if (y < 1970) return { bg: "#cfe6dc", cor: "#c2362f", fonte: SCRIPT, peso: 400, k: 0.5, max: 100, borda: "3px solid #c2362f",
    foto: "sepia(0.45) saturate(0.7) contrast(1.05)" };
  if (y < 1980) return { bg: "#f1d5a0", cor: "#5a2c12", fonte: ARCHIVO, peso: 400, caixa: "lower", k: 0.74, max: 74, deco: "faixas",
    foto: "sepia(0.3) saturate(1.1) contrast(1.05) hue-rotate(-8deg)" };
  if (y < 1990) return { bg: "#15132a", cor: "#7fe8ff", fonte: BEBAS, peso: 400, caixa: "upper", k: 0.5, max: 100, deco: "neon",
    extra: { transform: "skewX(-9deg)", textShadow: "0 0 10px rgba(127,232,255,0.8), 3px 3px 0 #ff4fa3" }, foto: "saturate(1.4) contrast(1.1)" };
  return { bg: "#f5f5f2", cor: "#1d4ea8", fonte: PLEX, peso: 700, k: 0.64, max: 72, deco: "onda", foto: "saturate(1.05)" };
};

/** Trilho horizontal com os anos da marca; o cursor corre de nó em nó e acende o letreiro de cada época
 *  (serifa, script, setentista, neon oitentista, sem serifa). O item com `fim` leva carimbo FIM vermelho. */
export const EvolucaoMarca: React.FC<EvolucaoMarcaProps> = (p) => {
  const f = useCurrentFrame();
  const itens = p.itens.slice(0, 6);
  const n = Math.max(1, itens.length);
  const TY = 810, VAO = 34;
  const CWd = Math.min(n > 1 ? 340 : 440, (1720 - (n - 1) * VAO) / n);   // cartões cabem entre 100 e 1820 px
  const X0 = 100 + CWd / 2, X1 = 1820 - CWd / 2;
  const passo = n > 1 ? (X1 - X0) / (n - 1) : 0;
  const xs = itens.map((_, i) => (n > 1 ? X0 + i * passo : 960));
  const T0 = 12, T1 = T0 + Math.max(28, Math.min(60, p.dur * 0.24));
  const seg = n > 1 ? (T1 - T0) / (n - 1) : 1;
  const chega = (i: number) => T0 + i * seg;
  // cursor: anda segmento a segmento, com leve parada em cada nó
  const k = Math.max(0, Math.min(n - 1, (f - T0) / seg));
  const ki = Math.floor(k), kf = k - ki;
  const cursorX = n > 1 ? (ki >= n - 1 ? xs[n - 1] : xs[ki] + (xs[ki + 1] - xs[ki]) * INOUT(Math.min(1, kf * 1.25))) : 960;
  const ultimoFim = itens.length > 0 && itens[itens.length - 1].fim;
  const corTrilho = (i: number) => (itens[i]?.fim ? "#d8352a" : "#f0b43c");
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, #2b221b, #120d0a 78%)", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ opacity: 0.5, backgroundImage:
        "repeating-linear-gradient(0deg, rgba(255,230,190,0.025) 0 1px, transparent 1px 4px), repeating-linear-gradient(90deg, rgba(255,230,190,0.02) 0 1px, transparent 1px 4px)" }} />
      {/* título */}
      <div style={{ position: "absolute", left: 110, top: 86, opacity: ent(f, 0), transform: `translateX(${(1 - ent(f, 0)) * -40}px)` }}>
        <div style={{ ...type.display, fontSize: caber(p.titulo, 1600, 70, 0.5, 44), color: "#f3e6cb", letterSpacing: 4, textTransform: "uppercase" }}>{p.titulo}</div>
        <div style={{ height: 6, width: 160 * ent(f, 4, 22), background: "#f0b43c", marginTop: 8 }} />
      </div>
      {/* letreiros */}
      {itens.map((it, i) => {
        const e = eraDe(it.ano, i);
        const t = chega(i);
        const sobe = spring({ frame: f - t + 2, fps: 30, config: { damping: 13, stiffness: 120 } });
        const vis = f >= t - 2 ? 1 : 0;
        const fimS = spring({ frame: f - t - 10, fps: 30, config: { damping: 9, stiffness: 200 } });
        const apaga = it.fim ? ent(f, t + 10, t + 26) : 0;
        const texto = e.caixa === "upper" ? it.rotulo.toUpperCase() : e.caixa === "lower" ? it.rotulo.toLowerCase() : it.rotulo;
        const fotoH = it.src ? Math.round(CWd * 0.7) : 0;
        const rotH = it.src ? 170 : 240;
        // cabe numa linha ou, se tiver espaço, em duas (limitado pela palavra mais longa e pela altura da faixa)
        const larg = CWd - 44, maiorPalavra = Math.max(...texto.split(/\s+/).map((w) => w.length));
        const uma = larg / (Math.max(1, texto.length) * e.k);
        const duas = Math.min(larg / (Math.max(1, maiorPalavra) * e.k), (1.8 * larg) / (Math.max(1, texto.length) * e.k));
        const fs = Math.max(34, Math.min(e.max, (rotH - 50) / (uma >= 44 || !texto.includes(" ") ? 1.1 : 2.2), Math.max(uma, texto.includes(" ") ? duas : 0)));
        const h = fotoH + rotH;
        const base = TY - 64;
        return (
          <React.Fragment key={i}>
            {/* luz de vitrine sobre o item aceso */}
            <div style={{ position: "absolute", left: xs[i] - CWd, top: base - h - 140, width: CWd * 2, height: h + 260, opacity: vis * ent(f, t, t + 16) * (1 - apaga * 0.7),
              background: "radial-gradient(ellipse 48% 46% at 50% 48%, rgba(255,214,150,0.22), transparent 100%)" }} />
            <div style={{ position: "absolute", left: xs[i] - 2, top: base, width: 4, height: 64 - 22, background: "rgba(240,180,60,0.6)",
              opacity: vis, transform: `scaleY(${sobe})`, transformOrigin: "50% 100%" }} />
            <div style={{ position: "absolute", left: xs[i] - CWd / 2, top: base - h, width: CWd, height: h, opacity: vis * Math.min(1, sobe * 1.5),
              transform: `translateY(${(1 - sobe) * 60}px) scale(${0.9 + 0.1 * sobe})`, transformOrigin: "50% 100%" }}>
              <div style={{ position: "absolute", inset: 0, background: e.bg, border: e.borda, boxSizing: "border-box",
                boxShadow: "0 18px 34px rgba(0,0,0,0.6)", overflow: "hidden",
                filter: apaga ? `grayscale(${apaga}) brightness(${1 - apaga * 0.45}) contrast(${1 - apaga * 0.2})` : undefined }}>
                {it.src ? <Img src={src(it.src)} style={{ position: "absolute", left: 0, top: 0, width: "100%", height: fotoH, objectFit: "cover",
                  filter: e.foto }} /> : null}
                <div style={{ position: "absolute", left: 18, right: 18, top: fotoH, height: rotH - (e.deco === "faixas" ? 34 : 0), display: "flex",
                  alignItems: "center", justifyContent: "center", textAlign: "center" }}>
                  <span style={{ fontFamily: e.fonte, fontWeight: e.peso, fontStyle: e.italico ? "italic" : "normal", fontSize: fs, color: e.cor,
                    lineHeight: 1.02, ...e.extra }}>{texto}</span>
                </div>
                {e.deco === "faixas" ? (
                  <div style={{ position: "absolute", left: 0, right: 0, bottom: 14 }}>
                    {["#e0882a", "#c4471f", "#7a3417"].map((c, j) => <div key={j} style={{ height: 7, marginTop: j ? 4 : 0, background: c }} />)}
                  </div>
                ) : null}
                {e.deco === "neon" ? <div style={{ position: "absolute", inset: 8, border: "3px solid #ff4fa3",
                  boxShadow: "0 0 12px rgba(255,79,163,0.8), inset 0 0 12px rgba(255,79,163,0.5)" }} /> : null}
                {e.deco === "onda" ? (
                  <svg width={CWd} height={40} style={{ position: "absolute", left: 0, bottom: 14 }}>
                    <path d={`M${CWd * 0.18},26 Q${CWd * 0.5},2 ${CWd * 0.82},22`} fill="none" stroke="#e23b2e" strokeWidth={7} strokeLinecap="round" />
                  </svg>
                ) : null}
              </div>
              {it.fim ? (
                <div style={{ position: "absolute", left: "50%", top: "50%", opacity: f >= t + 10 ? 1 : 0,
                  transform: `translate(-50%, -50%) rotate(-14deg) scale(${interpolate(fimS, [0, 1], [2.4, 1])})`,
                  border: "9px solid #e3352a", borderRadius: 10, color: "#e3352a", padding: "0 30px 0 38px", ...type.display,
                  fontSize: Math.min(110, CWd * 0.34), letterSpacing: 10, lineHeight: 1.12, background: "rgba(255,240,230,0.10)",
                  boxShadow: "0 0 0 4px rgba(227,53,42,0.3), 0 10px 30px rgba(0,0,0,0.5)", textShadow: "0 2px 0 rgba(0,0,0,0.25)" }}>FIM</div>
              ) : null}
            </div>
          </React.Fragment>
        );
      })}
      {/* trilho, nós e cursor */}
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs><linearGradient id="nosLatao" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#7c6440" /><stop offset="0.5" stopColor="#3d311f" />
          <stop offset="1" stopColor="#251d12" /></linearGradient></defs>
        <rect x={X0 - 60} y={TY - 6} width={X1 - X0 + 120} height={12} rx={6} fill="url(#nosLatao)" opacity={ent(f, 2, 16)} />
        {xs.slice(1).map((x, i) => {
          const pr = Math.max(0, Math.min(1, (cursorX - xs[i]) / Math.max(1, x - xs[i])));
          return <line key={i} x1={xs[i]} x2={xs[i] + (x - xs[i]) * pr} y1={TY} y2={TY} stroke={corTrilho(i + 1)} strokeWidth={8} strokeLinecap="round"
            strokeDasharray={itens[i + 1]?.fim ? "14 10" : undefined} />;
        })}
        {xs.map((x, i) => {
          const aceso = f >= chega(i);
          const pulso = aceso ? ((f - chega(i)) % 40) / 40 : 0;
          const cor = corTrilho(i);
          return (
            <g key={i} opacity={ent(f, 2 + i * 2, 14 + i * 2)}>
              {aceso ? <circle cx={x} cy={TY} r={20 + pulso * 26} fill="none" stroke={cor} strokeOpacity={0.7 * (1 - pulso)} strokeWidth={3} /> : null}
              <circle cx={x} cy={TY} r={17} fill={aceso ? cor : "#1d1712"} stroke={aceso ? "#fff3d6" : "#7c6440"} strokeWidth={4} />
            </g>
          );
        })}
        {f >= T0 - 4 ? (
          <g opacity={ent(f, T0 - 4, T0 + 4) * (ultimoFim && f > T1 + 12 ? 0.4 : 1)}>
            <circle cx={cursorX} cy={TY} r={46} fill="rgba(255,214,120,0.18)" />
            <circle cx={cursorX} cy={TY} r={10} fill="#fff6dc" />
            <path d={`M${cursorX - 16},${TY - 44} L${cursorX + 16},${TY - 44} L${cursorX},${TY - 24} Z`} fill="#fff6dc" />
          </g>
        ) : null}
      </svg>
      {/* anos */}
      {itens.map((it, i) => {
        const aceso = f >= chega(i);
        return (
          <div key={i} style={{ position: "absolute", left: xs[i] - 160, width: 320, top: TY + 38, textAlign: "center", fontFamily: MONO, fontWeight: 700,
            fontSize: caber(it.ano, Math.min(300, CWd), 50, 0.6, 34), letterSpacing: 2, opacity: ent(f, 4 + i * 2, 16 + i * 2) * (aceso ? 1 : 0.45),
            color: aceso ? (it.fim ? "#ff6a5c" : "#f3e6cb") : "#a8977a" }}>{it.ano}</div>
        );
      })}
      <Grao id="nosGevo" forca={0.6} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ETIQUETA DE PREÇO
export type EtiquetaPrecoProps = SceneProps & { produto: string; antigo: string; novo: string; ano_antigo: string; ano_novo: string;
  multiplicador?: string };

/** "2.750" → 2750 ; "14,7" → 14.7 ; "×52" → 52 (formato brasileiro). */
const lerNumero = (s: string) => {
  const m = s.match(/\d[\d.,]*/);
  if (!m) return null;
  let t = m[0].replace(/[.,]$/, "");
  if (t.includes(",")) t = t.replace(/\./g, "").replace(",", ".");
  else if (/^\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
  const v = parseFloat(t);
  return Number.isFinite(v) ? { v, casas: t.includes(".") ? t.split(".")[1].length : 0, ini: m.index ?? 0, fim: (m.index ?? 0) + m[0].length } : null;
};
const fmtBR = (v: number, casas: number) => {
  const [i, d] = v.toFixed(casas).split(".");
  return i.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (d ? `,${d}` : "");
};
/** Separa "Cr$ 1.890" em moeda e valor (a moeda sai menor, no alto, como na etiqueta). */
const partirPreco = (s: string) => {
  const m = s.match(/^(\D*?)\s*(\d.*)$/);
  return m ? { moeda: m[1].trim(), valor: m[2] } : { moeda: "", valor: s };
};

/** Etiqueta de maquininha de supermercado: faixa de gôndola com o produto, etiqueta velha com o preço antigo
 *  riscado à caneta, etiqueta nova carimbada com tranco, anos embaixo e o multiplicador contando no meio. */
export const EtiquetaPreco: React.FC<EtiquetaPrecoProps> = (p) => {
  const f = useCurrentFrame();
  const LW = 680, LH = 400, LY = 385;
  const velha = spring({ frame: f - 6, fps: 30, config: { damping: 14, stiffness: 110 } });
  const NOVA = 34;
  const nova = spring({ frame: f - NOVA, fps: 30, config: { damping: 11, stiffness: 220 } });
  const risco = ent(f, 24, 36);
  const tranco = f >= NOVA + 2 && f < NOVA + 8 ? (random(`sh${f}`) - 0.5) * 16 : 0;
  const faixa = ent(f, 0, 14);
  const multAt = 42;
  const mult = spring({ frame: f - multAt, fps: 30, config: { damping: 12, stiffness: 160 } });
  const num = p.multiplicador ? lerNumero(p.multiplicador) : null;
  const multTxt = (() => {
    if (!p.multiplicador) return "";
    if (!num) return p.multiplicador;
    const c = interpolate(f, [multAt, multAt + 26], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
    if (c >= 1) return p.multiplicador;
    const v = Math.min(num.v, (num.v >= 2 ? 1 : 0) + (num.v - (num.v >= 2 ? 1 : 0)) * c);
    return p.multiplicador.slice(0, num.ini) + fmtBR(v, num.casas) + p.multiplicador.slice(num.fim);
  })();
  const multFs = p.multiplicador ? caber(p.multiplicador, 200, 104, 0.48, 40) : 0;
  const bokeh = Array.from({ length: 30 }, (_, i) => ({
    x: random(`bx${i}`) * 1920, y: 60 + random(`by${i}`) * 960, r: 40 + random(`br${i}`) * 110,
    c: ["#d8402f", "#f2c230", "#3f9a5a", "#f4efe2", "#2f6fc0", "#e07a2a"][Math.floor(random(`bc${i}`) * 6)], o: 0.16 + random(`bo${i}`) * 0.22,
  }));
  const etiqueta = (texto: string, eNova = false) => {
    const { moeda, valor } = partirPreco(texto);
    const fs = Math.max(48, Math.min(190, (LW - 90) / ((moeda.length * 0.5 + valor.length) * 0.6)));
    const listra = eNova ? "#d8261e" : "#d9822f";
    // recorte de etiqueta de maquininha: cantos arredondados e um meio-círculo vazado em cada lado
    const r = 26, nc = 22;
    const corte = `path('M${r},0 H${LW - r} Q${LW},0 ${LW},${r} V${LH / 2 - nc} A${nc},${nc} 0 0,0 ${LW},${LH / 2 + nc} V${LH - r} Q${LW},${LH} ${LW - r},${LH}` +
      ` H${r} Q0,${LH} 0,${LH - r} V${LH / 2 + nc} A${nc},${nc} 0 0,0 0,${LH / 2 - nc} V${r} Q0,0 ${r},0 Z')`;
    return (
      <div style={{ position: "absolute", inset: 0, filter: "drop-shadow(0 22px 26px rgba(0,0,0,0.6))" }}>
      <div style={{ position: "absolute", inset: 0, overflow: "hidden", clipPath: corte,
        background: eNova ? "linear-gradient(170deg, #ffffff, #f1efe8)" : "linear-gradient(170deg, #efe0b2, #dcc68e)" }}>
        <div style={{ height: 56, backgroundImage: `repeating-linear-gradient(-45deg, ${listra} 0 18px, transparent 18px 34px)`,
          opacity: eNova ? 0.95 : 0.6, borderBottom: `4px solid ${listra}` }} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 56, bottom: 56, display: "flex", alignItems: "center", justifyContent: "center",
          color: eNova ? "#24183f" : "#3d2f45", fontFamily: MONO, fontWeight: 700, letterSpacing: -2,
          WebkitMaskImage: "radial-gradient(circle, #000 2.9px, transparent 3.4px)", WebkitMaskSize: "7px 7px",
          maskImage: "radial-gradient(circle, #000 2.9px, transparent 3.4px)", maskSize: "7px 7px" } as React.CSSProperties}>
          {moeda ? <span style={{ fontSize: fs * 0.5, alignSelf: "center", marginRight: 14, marginTop: -fs * 0.35 }}>{moeda}</span> : null}
          <span style={{ fontSize: fs, lineHeight: 1 }}>{valor}</span>
        </div>
        <div style={{ position: "absolute", left: 40, right: 40, bottom: 24, height: 10, borderTop: `4px dotted ${listra}`, opacity: 0.7 }} />
        {!eNova ? <AbsoluteFill style={{ background: "radial-gradient(ellipse at 70% 80%, rgba(120,80,20,0.25), transparent 60%)" }} /> : null}
      </div>
      </div>
    );
  };
  const anoStyle: React.CSSProperties = { position: "absolute", width: LW, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 58,
    color: "#f3e6cb", letterSpacing: 4, textShadow: "0 3px 10px rgba(0,0,0,0.8)" };
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #221a14, #0e0a07)", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `translate(${tranco}px, ${tranco * 0.6}px) scale(${interpolate(f, [0, p.dur], [1, 1.035], clamp)})` }}>
        {/* prateleiras desfocadas */}
        <AbsoluteFill style={{ filter: "blur(26px)" }}>
          {bokeh.map((b, i) => (
            <div key={i} style={{ position: "absolute", left: b.x - b.r + Math.sin((f + i * 20) / 40) * 10, top: b.y - b.r, width: 2 * b.r, height: 2 * b.r,
              borderRadius: "50%", background: b.c, opacity: b.o }} />
          ))}
        </AbsoluteFill>
        <AbsoluteFill style={{ background: "rgba(14,10,7,0.45)" }} />
        {/* faixa de gôndola */}
        <div style={{ position: "absolute", left: 120, right: 120, top: 96, height: 128, transform: `translateX(${(1 - faixa) * -1800}px)`,
          background: "linear-gradient(180deg, #d22b22, #a81d17)", borderTop: "12px solid #f2c230", boxShadow: "0 16px 30px rgba(0,0,0,0.55)",
          display: "flex", alignItems: "center", justifyContent: "center" }}>
          <span style={{ ...type.display, fontSize: caber(p.produto, 1560, 84, 0.5, 44), color: "#fff", letterSpacing: 4, textTransform: "uppercase",
            textShadow: "0 3px 0 rgba(0,0,0,0.3)" }}>{p.produto}</span>
        </div>
        {/* etiqueta velha */}
        <div style={{ position: "absolute", left: 130, top: LY, width: LW, height: LH,
          transform: `translateY(${(1 - velha) * 700}px) rotate(${-4 + (1 - velha) * -10}deg)` }}>
          {etiqueta(p.antigo)}
          <svg width={LW + 80} height={LH} style={{ position: "absolute", left: -40, top: 0 }}>
            <Traco d={`M30,${LH * 0.58} C${LW * 0.3},${LH * 0.47} ${LW * 0.6},${LH * 0.54} ${LW + 20},${LH * 0.4}`} p={risco} cor="rgba(212,32,24,0.92)" w={16} />
            <Traco d={`M50,${LH * 0.64} C${LW * 0.35},${LH * 0.55} ${LW * 0.7},${LH * 0.6} ${LW + 10},${LH * 0.47}`} p={risco * 1.4 - 0.4} cor="rgba(212,32,24,0.8)" w={10} />
          </svg>
        </div>
        <div style={{ ...anoStyle, left: 130, top: LY + LH + 46, opacity: ent(f, 14) }}>{p.ano_antigo}</div>
        {/* etiqueta nova, carimbada */}
        <div style={{ position: "absolute", left: 1920 - 130 - LW, top: LY, width: LW, height: LH, opacity: f >= NOVA ? 1 : 0,
          transform: `scale(${interpolate(nova, [0, 1], [1.7, 1])}) rotate(${3 + (1 - nova) * 8}deg)` }}>
          {etiqueta(p.novo, true)}
        </div>
        <div style={{ ...anoStyle, left: 1920 - 130 - LW, top: LY + LH + 46, opacity: ent(f, NOVA + 4) }}>{p.ano_novo}</div>
        {/* multiplicador */}
        {p.multiplicador ? (
          <div style={{ position: "absolute", left: 960 - 130, top: LY + LH / 2 - 130, width: 260, height: 260, borderRadius: "50%",
            background: "radial-gradient(circle at 40% 35%, #2a211a, #0f0b08)", border: "7px solid #f2c230", boxSizing: "border-box",
            boxShadow: "0 18px 40px rgba(0,0,0,0.7), 0 0 0 4px rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center",
            opacity: f >= multAt ? 1 : 0, transform: `scale(${mult}) rotate(${(1 - mult) * -40}deg)` }}>
            <span style={{ fontFamily: ANTON, fontSize: multFs, color: "#f2c230", lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{multTxt}</span>
          </div>
        ) : null}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.6) 100%)" }} />
      <Grao id="nosGeti" forca={0.6} />
    </AbsoluteFill>
  );
};
