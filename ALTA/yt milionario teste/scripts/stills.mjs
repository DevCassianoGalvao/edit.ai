// Renderiza vários stills com UM bundle (npx remotion still em loop recopia public/ a cada chamada).
// Uso: node scripts/stills.mjs jobs.json
//   jobs.json = { "public": true|false, "jobs": [{ "comp": "Main", "frame": 123, "out": "qa/x.jpg", "props": {} }] }
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const spec = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const t0 = Date.now();
// "public": "audio" → bundle com public mínima (só audio.mp3): stills de animação não precisam dos clipes,
// e bundle() copia a public inteira (vários GB) a cada chamada.
let publicDir = path.join(root, "public");
if (spec.public === "audio") {
  publicDir = path.join(root, "qa", "_public_min");
  fs.mkdirSync(publicDir, { recursive: true });
  const dst = path.join(publicDir, "audio.mp3");
  fs.copyFileSync(path.join(root, "public", "audio.mp3"), dst); // sempre: o áudio muda a cada filme
  // fontes locais (tokens.ts carrega de public/fonts; sem elas o render é cancelado)
  const fontsSrc = path.join(root, "public", "fonts");
  if (fs.existsSync(fontsSrc)) fs.cpSync(fontsSrc, path.join(publicDir, "fonts"), { recursive: true });
}
// outDir FIXO e limpo a cada chamada: sem ele o bundle() cria uma pasta nova em %TEMP% com a public inteira
// e nunca apaga (15/09: 3457 pastas remotion-webpack-bundle-*, 137 GB, disco zerado no meio da folha do filme)
const outDir = path.join(root, "out", "stills_bundle");
fs.rmSync(outDir, { recursive: true, force: true });
const serveUrl = await bundle({
  entryPoint: path.join(root, "src/index.ts"),
  publicDir,
  outDir,
  onProgress: () => {},
});
console.log(`[stills] bundle ${((Date.now() - t0) / 1000).toFixed(0)}s`);
const comps = new Map();
let i = 0;
for (const j of spec.jobs) {
  const key = j.comp + JSON.stringify(j.props ?? {});
  if (!comps.has(key)) {
    comps.set(key, await selectComposition({ serveUrl, id: j.comp, inputProps: j.props ?? {} }));
  }
  const composition = comps.get(key);
  const out = path.join(root, j.out);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  // retomada: still já renderizado nesta rodada não é refeito
  if (spec.resume && fs.existsSync(out) && fs.statSync(out).size > 0) {
    if (++i % 20 === 0) console.log(`[stills] ${i}/${spec.jobs.length}`);
    continue;
  }
  // filme das máquinas: 1 "Failed to fetch .../proxy?src=...mp4" (arquivo íntegro) derrubava 360 stills → até 3 tentativas
  for (let k = 1; ; k++) {
    try {
      await renderStill({
        serveUrl,
        composition,
        frame: j.frame,
        output: out,
        imageFormat: "jpeg",
        jpegQuality: 80,
        inputProps: j.props ?? {},
        scale: j.scale ?? 0.5,
        timeoutInMilliseconds: 120000,
      });
      break;
    } catch (e) {
      console.log(`[stills] quadro ${j.frame} tentativa ${k} falhou: ${String(e.message || e).slice(0, 160)}`);
      if (k >= 3) throw e;
      await new Promise((r) => setTimeout(r, 3000 * k));
    }
  }
  if (++i % 20 === 0) console.log(`[stills] ${i}/${spec.jobs.length}`);
}
console.log(`[stills] done ${spec.jobs.length} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
