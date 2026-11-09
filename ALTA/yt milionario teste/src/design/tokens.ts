import { Easing, cancelRender, continueRender, delayRender, staticFile } from "remotion";

// Fontes LOCAIS (public/fonts, baixadas por scripts/fetch_fonts.mjs): o render não depende do Google a cada aba.
// Falha ao carregar derruba o render (cancelRender) em vez de sair com fonte errada.
const UNICODE = {
  latin: "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
  "latin-ext": "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF",
};
const LOCAL_FONTS: [family: string, file: string, weights: string[]][] = [
  ["Oswald", "Oswald", ["500", "700"]],
  ["IBM Plex Sans", "IBMPlexSans", ["400", "500", "700"]],
  ["Courier Prime", "CourierPrime", ["400", "700"]],
];
if (typeof document !== "undefined" && typeof FontFace !== "undefined") {
  const handle = delayRender("carregando fontes locais");
  const faces = LOCAL_FONTS.flatMap(([family, file, weights]) =>
    weights.flatMap((w) =>
      Object.entries(UNICODE).map(
        ([sub, range]) =>
          new FontFace(family, `url(${staticFile(`fonts/${file}-${w}-${sub}.woff2`)}) format("woff2")`, {
            weight: w,
            style: "normal",
            unicodeRange: range,
          }),
      ),
    ),
  );
  Promise.all(faces.map((f) => f.load().then((loaded) => document.fonts.add(loaded))))
    .then(() => continueRender(handle))
    .catch((err) => cancelRender(err));
}

// Palette: naval / steel-at-sea documentary.
// Near-black navy ground (ocean at night, steel hull), haze-gray text,
// flight-deck amber as the primary accent (money, numbers, danger on deck),
// signal-teal as a sparing secondary accent (reactor, technology, water).
export const colors = {
  bg: "#070B12",
  bgElevated: "#0F1622",
  line: "#223044",
  accent: "#F4B63F",
  accentDim: "#6B5220",
  cool: "#4FC3D9",
  coolDim: "#1E4F5A",
  danger: "#E4573D",
  text: "#EEF2F6",
  textDim: "#8C99A8",
};

export const displayFont = "Oswald";
// 21/09/2026: o usuário escolheu a máquina de escrever como fonte PRINCIPAL de texto em todos os filmes.
// O display condensado (Oswald) continua nas palavras grandes — é assim nas referências que ele mandou.
export const textFont = "Courier Prime";
export const typeFont = "Courier Prime";
export const sansFont = "IBM Plex Sans"; // sobrou para parágrafo longo, onde a monoespaçada cansa

export const type = {
  display: { fontFamily: displayFont, fontWeight: 700 as const },
  displayMedium: { fontFamily: displayFont, fontWeight: 500 as const },
  body: { fontFamily: textFont, fontWeight: 400 as const },
  bodyMedium: { fontFamily: textFont, fontWeight: 500 as const },
  bodyBold: { fontFamily: textFont, fontWeight: 700 as const },
  scale: { mega: 220, hero: 120, h1: 76, h2: 50, body: 34, small: 26, micro: 20 },
};

export const springs = {
  snappy: { damping: 200, stiffness: 120, mass: 0.8 },
  gentle: { damping: 26, stiffness: 60, mass: 1 },
  bouncy: { damping: 12, stiffness: 100, mass: 0.9 },
};

export const EASE_OUT_EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IN_OUT = Easing.bezier(0.65, 0, 0.35, 1);

export const depth = {
  shadowSoft: "0 20px 60px rgba(0,0,0,0.45)",
  shadowHard: "0 8px 24px rgba(0,0,0,0.6)",
  radiusSm: 6,
  radiusMd: 14,
  radiusLg: 24,
};

export const motion = {
  videoDrift: 0.04, // Ken Burns máx. em vídeo
  photoPush: 0.12, // push-in em foto (sempre com movimento)
  crossfade: 8, // quadros de fusão entre cortes de stock
};

/** Formata número em espanhol (separador de milhar ".") de forma determinística. */
export const fmtEs = (n: number) =>
  Math.round(n)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ".");

/** Formata número em inglês (separador de milhar ",") de forma determinística. */
export const fmtEn = (n: number) =>
  Math.round(n)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
