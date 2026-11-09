// ARQUIVO 2 — efeitos "dark doc" que viraram REGRA de todo filme (26/09/2026, pedido do usuário):
//   Manchete (jornal girando) · Teletipo (telex batido) · Lupa (círculo vermelho + mergulho no detalhe)
//   AntesDepois (cortina) · RoloFilme (fotogramas com perfuração) · Revela (polaroide revelando) · Paralaxe 2.5D
// Todos usam o tratamento de arquivo (FilmeVelho) e as mesmas ferramentas de src/scenes/arquivo.tsx.
import React from "react";
import { AbsoluteFill, Img, interpolate, random, spring, useCurrentFrame } from "remotion";
import { Easing } from "remotion";
import { type } from "../design/tokens";
import { SceneProps, exit } from "./shared";
import { EXPO, FilmeVelho, MAO, SERIFA, Traco, clamp, src, tom } from "./arquivo";

// ================================================================================================ MANCHETE DE JORNAL
export type MancheteProps = SceneProps & { jornal: string; data: string; titulo: string; sub?: string; foto?: string };
/** Página de jornal entra girando até parar na tela (clássico de documentário), depois empurra devagar. */
export const Manchete: React.FC<MancheteProps> = (p) => {
  const f = useCurrentFrame();
  const g = spring({ frame: f - 2, fps: 30, config: { damping: 18, stiffness: 55 } });
  const push = interpolate(f, [30, p.dur], [1, 1.06], clamp);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #2a241c, #0b0906 75%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: 960 - 560, top: 540 - 470, width: 1120, height: 940, background: "#e9e2cf",
        boxShadow: "0 40px 90px rgba(0,0,0,0.75)", padding: "40px 56px", boxSizing: "border-box", color: "#16130f",
        transform: `rotate(${(1 - g) * 720 - 2}deg) scale(${(0.08 + 0.92 * g) * push})`, filter: `blur(${(1 - g) * 6}px)` }}>
        <div style={{ fontFamily: SERIFA, fontWeight: 700, fontSize: 88, textAlign: "center", letterSpacing: 2,
          borderBottom: "4px double #16130f", paddingBottom: 8 }}>{p.jornal}</div>
        <div style={{ ...type.body, fontSize: 22, textAlign: "center", padding: "8px 0", borderBottom: "2px solid #16130f",
          letterSpacing: 3 }}>{p.data}</div>
        <div style={{ fontFamily: SERIFA, fontWeight: 900, fontSize: p.titulo.length > 38 ? 66 : 84, lineHeight: 1.02,
          textAlign: "center", margin: "26px 0 16px", textTransform: "uppercase" }}>{p.titulo}</div>
        {p.sub ? <div style={{ fontFamily: SERIFA, fontStyle: "italic", fontSize: 32, textAlign: "center", marginBottom: 18 }}>{p.sub}</div> : null}
        <div style={{ display: "flex", gap: 30 }}>
          {p.foto ? <Img src={src(p.foto)} style={{ width: 520, height: 330, objectFit: "cover", filter: tom("pb") }} /> : null}
          <div style={{ flex: 1 }}>
            {Array.from({ length: 11 }, (_, i) => <div key={i} style={{ height: 12, margin: "0 0 16px",
              background: "rgba(22,19,15,0.28)", width: `${70 + random(`l${i}`) * 30}%` }} />)}
          </div>
        </div>
      </div>
      <FilmeVelho feixe={false} forca={0.7} />
    </AbsoluteFill>
  );
};

// ================================================================================================ TELEX / TELEGRAMA
export type TeletipoProps = SceneProps & { cabecalho: string; data: string; linhas: string[] };
/** Tira de papel de telex subindo enquanto o texto é batido em maiúsculas. */
export const Teletipo: React.FC<TeletipoProps> = (p) => {
  const f = useCurrentFrame();
  const total = p.linhas.join("").length;
  const fim = Math.max(40, p.dur * 0.72);
  const digitado = Math.floor(interpolate(f, [12, fim], [0, total], clamp));
  let resto = digitado;
  let linhaAtual = p.linhas.length - 1;
  { let r = digitado; for (let i = 0; i < p.linhas.length; i++) { if (r <= p.linhas[i].length) { linhaAtual = i; break; } r -= p.linhas[i].length; } }
  const sobe = -Math.max(0, linhaAtual - 3) * 70;
  const trepida = f < fim && f % 3 === 0 ? 1.5 : 0;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 60%, #221c14, #080604 80%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: 960 - 520, top: 170 + sobe, width: 1040, minHeight: 1200, background: "#efe8d2",
        padding: "46px 64px", boxSizing: "border-box", boxShadow: "0 30px 60px rgba(0,0,0,0.6)", transform: `translateX(${trepida}px)` }}>
        <div style={{ ...type.bodyBold, fontSize: 30, letterSpacing: 6, borderBottom: "3px dashed #3a3026", paddingBottom: 14 }}>{p.cabecalho}</div>
        <div style={{ ...type.body, fontSize: 24, letterSpacing: 3, margin: "12px 0 26px", opacity: 0.8 }}>{p.data}</div>
        {p.linhas.map((l, i) => {
          const vis = l.slice(0, Math.max(0, resto));
          resto -= l.length;
          return <div key={i} style={{ ...type.bodyBold, fontSize: 38, lineHeight: "70px", letterSpacing: 2, textTransform: "uppercase",
            color: "#1d1812" }}>{vis}{i === linhaAtual && f % 14 < 7 ? "▌" : ""}</div>;
        })}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 190, background: "linear-gradient(transparent, #0b0906 60%)" }} />
      <FilmeVelho feixe={false} forca={0.7} />
    </AbsoluteFill>
  );
};

// ================================================================================================ LUPA NO DETALHE
export type LupaProps = SceneProps & { src: string; x: number; y: number; r?: number; rotulo: string; t?: "sepia" | "frio" | "pb" | "cor" };
/** Foto inteira; a caneta circula o detalhe (x,y em 0–1 da tela) e a câmera mergulha nele. */
export const Lupa: React.FC<LupaProps> = (p) => {
  const f = useCurrentFrame();
  const r = p.r ?? 0.12;
  const circ = interpolate(f, [p.dur * 0.1, p.dur * 0.3], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const zoom = interpolate(f, [p.dur * 0.34, p.dur * 0.6], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const k = 1 + zoom * 1.4;
  const cx = p.x * 1920, cy = p.y * 1080, R = r * 1080;
  const tx = (960 - cx) * zoom, ty = (540 - cy) * zoom;
  const rot = interpolate(f, [p.dur * 0.58, p.dur * 0.7], [0, 1], { ...clamp, easing: EXPO });
  const filtro = p.t === "cor" ? "contrast(1.05)" : tom(p.t ?? "pb");
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${k})`, transformOrigin: `${cx}px ${cy}px` }}>
        <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: filtro }} />
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <Traco d={`M${cx - R},${cy + 8} C${cx - R},${cy - R * 1.1} ${cx + R * 1.1},${cy - R} ${cx + R},${cy} C${cx + R},${cy + R * 1.1} ${cx - R * 1.15},${cy + R} ${cx - R * 0.92},${cy - R * 0.2}`}
            p={circ} cor="#c3171d" w={9 / k} />
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 50%, transparent ${30 + (1 - zoom) * 60}%, rgba(0,0,0,${0.55 * zoom}) 78%)` }} />
      <div style={{ position: "absolute", left: 120, bottom: 120, background: "#c3171d", color: "#fff", ...type.display, fontSize: 46,
        letterSpacing: 2, padding: "12px 26px", transform: `translateX(${(1 - rot) * -900}px)` }}>{p.rotulo}</div>
      <FilmeVelho feixe={false} forca={0.6} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ANTES / DEPOIS
export type AntesDepoisProps = SceneProps & { a: { src: string; rotulo: string }; b: { src: string; rotulo: string }; sepiaA?: boolean };
/** Cortina vertical: a imagem B (depois) avança da esquerda por cima da A (antes), com linha guia e os dois rótulos. */
export const AntesDepois: React.FC<AntesDepoisProps> = (p) => {
  const f = useCurrentFrame();
  const w = interpolate(f, [p.dur * 0.22, p.dur * 0.68], [0.02, 0.98], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const X = w * 1920;
  const kb = interpolate(f, [0, p.dur], [1.06, 1], clamp);
  const lab = (t: string, lado: "l" | "r", o: number) => (
    <div style={{ position: "absolute", top: 70, [lado === "l" ? "left" : "right"]: 80, background: "rgba(10,9,8,0.82)",
      color: "#f1ece2", ...type.bodyBold, fontSize: 30, letterSpacing: 5, padding: "10px 22px", opacity: o } as React.CSSProperties}>{t}</div>
  );
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden", ...exit(f, p.dur) }}>
      <Img src={src(p.a.src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
        transform: `scale(${kb})`, filter: p.sepiaA === false ? "none" : tom("sepia") }} />
      <div style={{ position: "absolute", inset: 0, clipPath: `inset(0 ${1920 - X}px 0 0)` }}>
        <Img src={src(p.b.src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${kb})` }} />
      </div>
      <div style={{ position: "absolute", top: 0, bottom: 0, left: X - 3, width: 6, background: "#f3eee3", boxShadow: "0 0 24px rgba(0,0,0,0.7)" }} />
      <div style={{ position: "absolute", top: 510, left: X - 30, width: 60, height: 60, borderRadius: "50%", background: "#f3eee3",
        boxShadow: "0 6px 16px rgba(0,0,0,0.6)" }} />
      {lab(p.a.rotulo, "r", interpolate(w, [0.6, 0.9], [1, 0.35], clamp))}
      {lab(p.b.rotulo, "l", interpolate(w, [0.1, 0.35], [0, 1], clamp))}
      <FilmeVelho feixe={false} forca={0.5} />
    </AbsoluteFill>
  );
};

// ================================================================================================ ROLO DE FILME
export type RoloProps = SceneProps & { fotos: string[]; titulo?: string };
/** Fotogramas com perfuração lateral atravessam a tela, desaceleram e param na foto do meio. */
export const RoloFilme: React.FC<RoloProps> = (p) => {
  const f = useCurrentFrame();
  const n = p.fotos.length;
  const W = 820, gap = 60;
  const alvo = Math.floor((n - 1) / 2);
  const corre = interpolate(f, [0, p.dur * 0.55], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const x0 = 1920 + 200, x1 = 960 - W / 2 - 30 - alvo * (W + gap);
  const x = x0 + (x1 - x0) * corre;
  const flick = 0.9 + random(`rf${f}`) * 0.1;
  return (
    <AbsoluteFill style={{ background: "#070605", overflow: "hidden", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", top: 540 - 330, left: x, height: 660, display: "flex", gap, padding: "0 30px",
        background: "#141210", filter: `brightness(${flick})` }}>
        {p.fotos.map((s, i) => (
          <div key={i} style={{ position: "relative", width: W, height: 660, display: "flex", alignItems: "center" }}>
            {[0, 1].map((lado) => (
              <div key={lado} style={{ position: "absolute", left: 0, right: 0, [lado ? "bottom" : "top"]: 18, height: 34, display: "flex",
                justifyContent: "space-around" } as React.CSSProperties}>
                {Array.from({ length: 8 }, (_, k) => <div key={k} style={{ width: 44, height: 30, borderRadius: 5, background: "#e9e4d8", opacity: 0.85 }} />)}
              </div>
            ))}
            <Img src={src(s)} style={{ width: W, height: 500, objectFit: "cover", filter: tom("pb") }} />
          </div>
        ))}
      </div>
      {p.titulo ? <div style={{ position: "absolute", left: 0, right: 0, bottom: 70, textAlign: "center", ...type.bodyBold, fontSize: 34,
        letterSpacing: 8, color: "#e9e4d8", opacity: interpolate(f, [p.dur * 0.5, p.dur * 0.6], [0, 1], clamp) }}>{p.titulo}</div> : null}
      <FilmeVelho forca={0.9} />
    </AbsoluteFill>
  );
};

// ================================================================================================ POLAROIDE REVELANDO
export type RevelaProps = SceneProps & { src: string; legenda?: string };
/** A foto nasce escura e "revela" como polaroide sobre a mesa; a legenda é escrita à mão no fim. */
export const Revela: React.FC<RevelaProps> = (p) => {
  const f = useCurrentFrame();
  const cai = spring({ frame: f, fps: 30, config: { damping: 15, stiffness: 80 } });
  const rev = interpolate(f, [p.dur * 0.1, p.dur * 0.62], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const esc = interpolate(f, [p.dur * 0.62, p.dur * 0.8], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #3a2d1f, #0d0a07 80%)", ...exit(f, p.dur) }}>
      <div style={{ position: "absolute", left: 960 - 430, top: 60, width: 860, background: "#f2eee4", padding: "34px 34px 120px",
        boxShadow: "0 40px 70px rgba(0,0,0,0.65)", transform: `translateY(${(1 - cai) * -900}px) rotate(${(1 - cai) * 14 - 2.5}deg)` }}>
        <div style={{ position: "relative", width: "100%", height: 640, background: "#241c14" }}>
          <Img src={src(p.src)} style={{ width: "100%", height: "100%", objectFit: "cover",
            filter: `${tom("sepia")} brightness(${0.2 + 0.8 * rev}) contrast(${0.6 + 0.5 * rev}) blur(${(1 - rev) * 5}px)`, opacity: 0.15 + 0.85 * rev }} />
          <AbsoluteFill style={{ background: `rgba(90,60,30,${0.6 * (1 - rev)})`, mixBlendMode: "multiply" }} />
        </div>
        {p.legenda ? <div style={{ position: "absolute", left: 40, right: 40, bottom: 34, fontFamily: MAO, fontSize: 44, color: "#2a2118",
          textAlign: "center", clipPath: `inset(0 ${100 - esc * 100}% 0 0)` }}>{p.legenda}</div> : null}
      </div>
      <FilmeVelho feixe={false} forca={0.8} />
    </AbsoluteFill>
  );
};

// ================================================================================================ PARALAXE 2.5D
export type ParalaxeProps = SceneProps & { src: string; fg: string; dir?: 1 | -1 };
/** Foto separada em 2 camadas (fundo + recorte do sujeito, feito por scripts/paralaxe.py): o fundo anda devagar,
 * o sujeito anda mais e cresce — sensação de câmera real entrando na foto. */
export const Paralaxe: React.FC<ParalaxeProps> = (p) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, p.dur], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const d = p.dir ?? 1;
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <Img src={src(p.src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
        transform: `scale(${1.12 + 0.03 * t}) translateX(${d * (t - 0.5) * 22}px)`, filter: "blur(1.5px) brightness(0.9)" }} />
      <Img src={src(p.fg)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
        transform: `scale(${1.12 + 0.1 * t}) translateX(${d * (t - 0.5) * 70}px)`, filter: "drop-shadow(0 18px 24px rgba(0,0,0,0.45))" }} />
    </AbsoluteFill>
  );
};

// ================================================================================================ MAPA DE CAMPANHA
export type Ponto = { nome: string; lat: number; lon: number; data?: string; cue: string; lado?: "esq" };  // lado "esq": rótulo à esquerda do ponto (28/09: Japão x Coreia se sobrepunham)
export type Seta = { de: number; para: number; cor?: string; cue: string };
export type MapaCampanhaProps = SceneProps & { kicker: string; pontos: Ponto[]; setas: Seta[];
  costa?: [number, number][][] };
/** Mapa de campanha: pontos com data e setas grossas avançando entre eles (movimento de tropas, rotas, expansão). */
export const MapaCampanha: React.FC<MapaCampanhaProps> = (p) => {
  const f = useCurrentFrame();
  const todos = [...p.pontos.map((q) => [q.lat, q.lon] as [number, number]), ...(p.costa ?? []).flat()];
  const lat0 = todos.reduce((a, [la]) => a + la, 0) / todos.length;
  const k = Math.cos((lat0 * Math.PI) / 180);
  const xs = todos.map(([, lo]) => lo * k), ys = todos.map(([la]) => -la);
  const [a, b, c, d] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const box = { x: 220, y: 200, w: 1480, h: 760 };
  const e = Math.min(box.w / Math.max(b - a, 1e-6), box.h / Math.max(d - c, 1e-6));
  const ox = box.x + (box.w - (b - a) * e) / 2, oy = box.y + (box.h - (d - c) * e) / 2;
  const pj = (la: number, lo: number) => ({ x: ox + (lo * k - a) * e, y: oy + (-la - c) * e });
  const P = p.pontos.map((q) => pj(q.lat, q.lon));
  const atP = p.pontos.map((q, i) => (p.cues?.[q.cue] !== undefined ? Math.max(0, p.cues[q.cue]) : Math.round(p.dur * (0.05 + i * 0.08))));
  return (
    <AbsoluteFill style={{ background: "#1b1812", overflow: "hidden", ...exit(f, p.dur) }}>
      <AbsoluteFill style={{ background: "#cbbd98", filter: "brightness(0.78)", backgroundImage:
        "linear-gradient(rgba(60,45,25,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(60,45,25,0.12) 1px, transparent 1px)",
        backgroundSize: "80px 80px" }} />
      <div style={{ position: "absolute", left: 80, top: 60, ...type.bodyBold, fontSize: 30, letterSpacing: 6, color: "#2b2217" }}>{p.kicker}</div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {(p.costa ?? []).map((ln, i) => <path key={i} d={ln.map(([la, lo], j) => { const q = pj(la, lo); return `${j ? "L" : "M"}${q.x},${q.y}`; }).join(" ")}
          fill="none" stroke="rgba(43,34,23,0.7)" strokeWidth={3} />)}
        {p.setas.map((s, i) => {
          const at = p.cues?.[s.cue] !== undefined ? p.cues[s.cue] : Math.round(p.dur * (0.2 + i * 0.14));
          const pr = interpolate(f, [at, at + 26], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
          const A = P[s.de], B = P[s.para];
          const mx = (A.x + B.x) / 2 + (B.y - A.y) * 0.18, my = (A.y + B.y) / 2 - (B.x - A.x) * 0.18;
          const cor = s.cor ?? "#b3161b";
          const ang = Math.atan2(B.y - my, B.x - mx);
          return (
            <g key={i}>
              <Traco d={`M${A.x},${A.y} Q${mx},${my} ${B.x},${B.y}`} p={pr} cor={cor} w={16} tampa="butt" />
              {pr > 0.97 ? <path d={`M${B.x + Math.cos(ang) * 10},${B.y + Math.sin(ang) * 10} L${B.x - Math.cos(ang - 0.5) * 44},${B.y - Math.sin(ang - 0.5) * 44} L${B.x - Math.cos(ang + 0.5) * 44},${B.y - Math.sin(ang + 0.5) * 44} Z`} fill={cor} /> : null}
            </g>
          );
        })}
        {P.map((q, i) => {
          const s = spring({ frame: f - atP[i], fps: 30, config: { damping: 10, stiffness: 160 } });
          return <circle key={i} cx={q.x} cy={q.y} r={14 * s} fill="#1d1812" stroke="#efe6cf" strokeWidth={4} />;
        })}
      </svg>
      {P.map((q, i) => {
        const o = interpolate(f, [atP[i] + 4, atP[i] + 14], [0, 1], clamp);
        const pt = p.pontos[i];
        return (
          <div key={i} style={{ position: "absolute", left: pt.lado === "esq" ? q.x - 22 : q.x + 22, top: q.y - 30, opacity: o, color: "#1d1812",
            ...(pt.lado === "esq" ? { transform: "translateX(-100%)", textAlign: "right" as const } : {}) }}>
            <div style={{ ...type.display, fontSize: 38, textTransform: "uppercase" }}>{pt.nome}</div>
            {pt.data ? <div style={{ ...type.bodyBold, fontSize: 24, letterSpacing: 2, color: "#8e1f1a" }}>{pt.data}</div> : null}
          </div>
        );
      })}
      <FilmeVelho feixe={false} forca={0.7} />
    </AbsoluteFill>
  );
};
