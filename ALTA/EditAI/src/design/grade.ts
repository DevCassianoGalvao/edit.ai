// GERADO por scripts/theme_pack.py a partir de data/tema_config.json — não editar à mão.
// Grade de cor do tema (modo ULTRA): os mesmos números que scripts/render_hybrid.py aplica no ffmpeg,
// para foto (Remotion) e vídeo (corte seco) parecerem da mesma câmera.
export type Lado = "quente" | "frio";
export const GRADE = {
  ativo: true,
  contraste: 1.1,
  saturacao: 0.95,
  // colorbalance do ffmpeg: [r, g, b] em −1..1 para sombras e realces
  sombras: { quente: [0.05, 0.02, -0.06], frio: [-0.06, 0.0, 0.09] },
  realces: { quente: [0.06, 0.04, -0.03], frio: [-0.02, 0.02, 0.04] },
} as const;
