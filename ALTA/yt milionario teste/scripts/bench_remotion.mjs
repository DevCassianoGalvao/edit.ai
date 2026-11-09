// 07/10/2026 — BANCO DE TESTE do Remotion (não faz parte do pipeline): renderiza o mesmo trecho com configurações
// diferentes e mede quadros/s e memória livre mínima. Uso:
//   node scripts/bench_remotion.mjs <pasta do bundle> <inicio> <fim> <saida.mp4> <gl|-> <concurrency>
import { openBrowser, renderMedia, selectComposition } from "@remotion/renderer";
import os from "node:os";

const [serveUrl, ini, fim, saida, gl, conc] = process.argv.slice(2);
const chromiumOptions = gl && gl !== "-" ? { gl } : {};
const composition = await selectComposition({ serveUrl, id: "Main", inputProps: {}, chromiumOptions });
const browser = await openBrowser("chrome", { shouldDumpIo: false, chromiumOptions });
let minLivre = os.freemem();
const amostra = setInterval(() => { minLivre = Math.min(minLivre, os.freemem()); }, 500);
const t0 = Date.now();
await renderMedia({
  serveUrl, composition, codec: "h264", crf: 16, x264Preset: "veryfast", muted: true,
  frameRange: [Number(ini), Number(fim) - 1], outputLocation: saida, inputProps: {},
  concurrency: Number(conc), timeoutInMilliseconds: 300000,
  offthreadVideoCacheSizeInBytes: 1024 * 1024 * 1024, puppeteerInstance: browser, chromiumOptions,
});
clearInterval(amostra);
const s = (Date.now() - t0) / 1000;
console.log(JSON.stringify({ gl: gl || "-", conc: Number(conc), quadros: fim - ini, segundos: Math.round(s),
  qps: +((fim - ini) / s).toFixed(2), memLivreMinGB: +(minLivre / 2 ** 30).toFixed(1) }));
await browser.close({ silent: true }).catch(() => {});
process.exit(0);
