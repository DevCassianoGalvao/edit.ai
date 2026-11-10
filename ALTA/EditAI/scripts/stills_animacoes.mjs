// 10/10/2026 — REVISÃO ANTES DO RENDER: foto (still) de quadros escolhidos do Remotion (cartões, mapas, animações).
// Uso: node scripts/stills_animacoes.mjs <lista.json com [quadros]> <pasta de saída>
// Usa o bundle de out/bundle_path.txt (feito por scripts/bundle.mjs). Um navegador só para todas as fotos.
import { openBrowser, renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [lista, outDir] = process.argv.slice(2);
const quadros = JSON.parse(fs.readFileSync(lista, "utf8"));
const serveUrl = fs.readFileSync(path.join(root, "out", "bundle_path.txt"), "utf8").trim();
fs.mkdirSync(outDir, { recursive: true });
const composition = await selectComposition({ serveUrl, id: "Main", inputProps: {} });
const browser = await openBrowser("chrome", { shouldDumpIo: false });
const t0 = Date.now();
let ok = 0;
for (const f of quadros) {
  try {
    await renderStill({
      serveUrl, composition, frame: f, inputProps: {}, imageFormat: "jpeg", jpegQuality: 80, scale: 0.5,
      output: path.join(outDir, `f${String(f).padStart(6, "0")}.jpg`), puppeteerInstance: browser,
      timeoutInMilliseconds: 120000,
    });
    ok++;
  } catch (e) {
    console.log(`quadro ${f} FALHOU: ${String(e.message || e).slice(0, 200)}`);
  }
}
await browser.close({ silent: true }).catch(() => {});
console.log(JSON.stringify({ fotos: ok, de: quadros.length, segundos: Math.round((Date.now() - t0) / 1000) }));
process.exit(0);
