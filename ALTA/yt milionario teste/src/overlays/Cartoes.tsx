// CARTÕES E FICHAS (21/09/2026, pedido do usuário com referências): família de gráficos SOBREPOSTOS em papel,
// tipografia de máquina de escrever (Courier Prime), que entram animados por cima do vídeo/foto.
//   CartaoFoto   — foto emoldurada tipo polaroide, com legenda batida a máquina e etiqueta de canto
//   Comparacao   — dois cartões lado a lado (antes/depois, modelo A x modelo B), entram por lados opostos
//   Fichas       — 2 a 4 papéis espetados com alfinete vermelho ("EXHIBIT A"), entram um a um
//   PalavraCheia — palavra grande sobre a imagem escurecida + linha fina no centro (abertura de capítulo)
// Nada disso toma a tela por inteiro além do escurecimento da PalavraCheia: o plano continua rodando atrás.
import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, displayFont, typeFont } from "../design/tokens";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const PAPEL = "#EFE7D6"; // papel creme das referências
const TINTA = "#1A1714"; // tinta da máquina de escrever
const BRANCO = "#F4F1EA";
const SOMBRA_TXT = "0 2px 0 rgba(0,0,0,0.55), 0 2px 14px rgba(0,0,0,0.45)";
const SOMBRA_PAPEL = "0 18px 40px rgba(0,0,0,0.55), 0 2px 6px rgba(0,0,0,0.4)";

const img = (s: string) => (/^(https?:|data:|blob:|\/)/.test(s) ? s : staticFile(s));

/** entrada com assentamento (mola curta) + saída em fade */
const useVida = (entra: number, fica: number) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - entra, fps, config: { damping: 18, mass: 0.6, stiffness: 120 }, durationInFrames: 22 });
  const o = Math.min(
    interpolate(frame, [entra, entra + 8], [0, 1], clamp),
    interpolate(frame, [entra + fica - 10, entra + fica], [1, 0], clamp),
  );
  return { frame, p, o };
};

const Legenda: React.FC<{ texto: string; tam?: number }> = ({ texto, tam = 26 }) => (
  <div
    style={{
      fontFamily: typeFont, fontWeight: 700, fontSize: tam, letterSpacing: "0.06em",
      textTransform: "uppercase", color: TINTA, textAlign: "center", padding: "14px 10px 4px",
    }}
  >
    {texto}
  </div>
);

/** etiqueta pequena de canto, caixa escura + letra de máquina (referência: "PRIYA'S CAR") */
export const EtiquetaMaquina: React.FC<{ texto: string; entra?: number; fica?: number; dir?: boolean }> = ({
  texto, entra = 6, fica = 150, dir = false,
}) => {
  const { frame, o } = useVida(entra, fica);
  const dx = interpolate(frame, [entra, entra + 12], [dir ? 24 : -24, 0], clamp);
  return (
    <div
      style={{
        position: "absolute", top: 54, [dir ? "right" : "left"]: 60, opacity: o,
        transform: `translateX(${dx}px)`, background: "rgba(12,10,8,0.82)", padding: "10px 18px",
      }}
    >
      <span style={{ fontFamily: typeFont, fontWeight: 700, fontSize: 24, letterSpacing: "0.18em",
                     textTransform: "uppercase", color: BRANCO }}>{texto}</span>
    </div>
  );
};

/** CARTÃO DE FOTO: foto emoldurada em papel, legenda a máquina, entra girando de leve. */
export const CartaoFoto: React.FC<{
  src: string; legenda: string; etiqueta?: string; lado?: "centro" | "esq" | "dir";
  pb?: boolean; giro?: number; largura?: number; entra?: number; fica?: number;
}> = ({ src, legenda, etiqueta, lado = "centro", pb = true, giro = -1.4, largura = 860, entra = 8, fica = 150 }) => {
  const { p, o } = useVida(entra, fica);
  const gira = `rotate(${giro * (2 - p)}deg) scale(${0.94 + 0.06 * p})`;
  const pos: React.CSSProperties = lado === "centro"
    ? { left: "50%", top: "50%", transform: `translate(-50%, -50%) ${gira}` }
    : { [lado === "esq" ? "left" : "right"]: 150, top: 150, transform: gira };
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {etiqueta ? <EtiquetaMaquina texto={etiqueta} entra={entra} fica={fica} /> : null}
      <div style={{ position: "absolute", ...pos, opacity: o, width: largura, background: PAPEL,
                    padding: "18px 18px 10px", boxShadow: SOMBRA_PAPEL }}>
        <Img src={img(src)} style={{ width: "100%", height: Math.round(largura * 0.6), objectFit: "cover",
                                     filter: pb ? "grayscale(1) contrast(1.06)" : "none", display: "block" }} />
        <Legenda texto={legenda} />
      </div>
    </AbsoluteFill>
  );
};

/** COMPARAÇÃO: dois cartões entrando por lados opostos, com rótulo em cima de cada um. */
export const Comparacao: React.FC<{
  a: { src: string; legenda: string; rotulo?: string };
  b: { src: string; legenda: string; rotulo?: string };
  titulo?: string; pb?: boolean; entra?: number; fica?: number;
}> = ({ a, b, titulo, pb = true, entra = 8, fica = 170 }) => {
  const { frame, p, o } = useVida(entra, fica);
  const L = 720;
  const dx = (1 - p) * 90;
  const linha = interpolate(frame, [entra + 10, entra + 30], [0, 1], clamp);
  const cartao = (x: { src: string; legenda: string; rotulo?: string }, i: number) => (
    <div style={{ width: L, background: PAPEL, padding: "16px 16px 8px", boxShadow: SOMBRA_PAPEL,
                  transform: `translateX(${i ? dx : -dx}px) rotate(${i ? 1.1 : -1.1}deg)` }}>
      {x.rotulo ? (
        <div style={{ fontFamily: typeFont, fontWeight: 700, fontSize: 22, letterSpacing: "0.18em",
                      textTransform: "uppercase", color: "#7A6A55", padding: "2px 2px 10px" }}>{x.rotulo}</div>
      ) : null}
      <Img src={img(x.src)} style={{ width: "100%", height: Math.round(L * 0.58), objectFit: "cover",
                                     filter: pb ? "grayscale(1) contrast(1.06)" : "none", display: "block" }} />
      <Legenda texto={x.legenda} tam={24} />
    </div>
  );
  return (
    <AbsoluteFill style={{ pointerEvents: "none", alignItems: "center", justifyContent: "center", opacity: o }}>
      {titulo ? (
        <div style={{ position: "absolute", top: 90, fontFamily: typeFont, fontWeight: 700, fontSize: 28,
                      letterSpacing: "0.22em", textTransform: "uppercase", color: BRANCO, textShadow: SOMBRA_TXT }}>
          {titulo}
        </div>
      ) : null}
      <div style={{ display: "flex", alignItems: "center", gap: 48 }}>
        {cartao(a, 0)}
        <div style={{ width: 2, height: 420 * linha, background: colors.danger, opacity: 0.85 }} />
        {cartao(b, 1)}
      </div>
    </AbsoluteFill>
  );
};

/** FICHAS: papéis espetados com alfinete, entram um a um (referência: "EXHIBIT A / B / C"). */
export const Fichas: React.FC<{ itens: { rotulo: string; texto: string }[]; entra?: number; fica?: number }> = ({
  itens, entra = 8, fica = 190,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const o = Math.min(
    interpolate(frame, [entra, entra + 8], [0, 1], clamp),
    interpolate(frame, [entra + fica - 12, entra + fica], [1, 0], clamp),
  );
  const GIRO = [-2.2, 1.4, -1.1, 2];
  const TOPO = [200, 380, 240, 430];
  const largura = 520;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: o }}>
      {itens.slice(0, 4).map((it, i) => {
        const t = entra + i * 9;
        const p = spring({ frame: frame - t, fps, config: { damping: 16, mass: 0.6, stiffness: 130 }, durationInFrames: 20 });
        return (
          <div
            key={i}
            style={{
              position: "absolute", left: 120 + i * (largura * 0.78), top: TOPO[i % 4], width: largura,
              background: PAPEL, padding: "22px 26px 26px", boxShadow: SOMBRA_PAPEL, opacity: p,
              transform: `rotate(${GIRO[i % 4] * (2 - p)}deg) scale(${0.93 + 0.07 * p})`,
            }}
          >
            <div style={{ position: "absolute", top: -9, left: largura / 2 - 9, width: 18, height: 18,
                          borderRadius: 9, background: colors.danger, boxShadow: "0 3px 6px rgba(0,0,0,0.5)" }} />
            <div style={{ fontFamily: typeFont, fontWeight: 700, fontSize: 20, letterSpacing: "0.22em",
                          textTransform: "uppercase", color: "#8A7860" }}>{it.rotulo}</div>
            <div style={{ fontFamily: typeFont, fontWeight: 700, fontSize: 34, lineHeight: 1.25,
                          letterSpacing: "0.02em", textTransform: "uppercase", color: TINTA, marginTop: 10 }}>
              {it.texto}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** PALAVRA CHEIA: uma palavra grande sobre a imagem escurecida, com a linha fina vermelha no centro. */
export const PalavraCheia: React.FC<{ palavra: string; sub?: string; entra?: number; fica?: number }> = ({
  palavra, sub, entra = 6, fica = 120,
}) => {
  const frame = useCurrentFrame();
  const o = Math.min(
    interpolate(frame, [entra, entra + 10], [0, 1], clamp),
    interpolate(frame, [entra + fica - 12, entra + fica], [1, 0], clamp),
  );
  const esc = interpolate(frame, [entra, entra + 14], [0, 0.55], clamp);
  const s = interpolate(frame, [entra, entra + 22], [1.06, 1], clamp);
  const h = interpolate(frame, [entra + 6, entra + 26], [0, 1], clamp);
  // A frase tem de caber DENTRO do quadro: sem largura o div crescia além dos 1920 px e a primeira
  // letra saía cortada na borda ("NONE OF THEM RELY ON LUCK" no filme das vans).
  // Oswald é condensada: ~0,46 x o corpo por caractere. Encolhe até a maior palavra caber em LARG,
  // e de novo se a frase inteira precisar de mais de duas linhas.
  const LARG = 1720;
  const linhas = (fs: number) => {
    const cabe = Math.max(6, Math.floor(LARG / (fs * 0.46)));
    let n = 1;
    let atual = 0;
    for (const w of palavra.split(" ")) {
      const passo = atual === 0 ? w.length : atual + 1 + w.length;
      if (passo > cabe) {
        n += 1;
        atual = w.length;
      } else {
        atual = passo;
      }
    }
    return { n, cabe };
  };
  const maiorPalavra = Math.max(...palavra.split(" ").map((w) => w.length));
  let corpo = 190;
  while (corpo > 78) {
    const { n, cabe } = linhas(corpo);
    if (maiorPalavra <= cabe && n <= 2) break;
    corpo -= 6;
  }
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: "#000", opacity: esc }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: o }}>
        <div style={{ position: "absolute", width: 2, height: `${100 * h}%`, background: colors.danger, opacity: 0.8 }} />
        <div style={{ fontFamily: displayFont, fontWeight: 700, fontSize: corpo, lineHeight: 1.02, color: BRANCO,
                      width: LARG, textAlign: "center", textShadow: SOMBRA_TXT, transform: `scale(${s})`,
                      letterSpacing: 2 }}>{palavra}</div>
        {sub ? (
          <div style={{ fontFamily: typeFont, fontWeight: 700, fontSize: 32, letterSpacing: "0.22em",
                        width: LARG, textAlign: "center", color: BRANCO, textShadow: SOMBRA_TXT,
                        marginTop: 18 }}>{sub}</div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
