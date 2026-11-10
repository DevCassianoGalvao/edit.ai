// Prévias dos 3 estilos de destaque para o painel (painel/previas/dest_*.png). Bundle próprio em out/painel_bundle —
// não mexe no out/bundle do filme. Fundo: public/demo/trem.jpg (o gera_previas.py copia antes).
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.join(root, "painel", "previas");
fs.mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(root, "src", "index.ts"), outDir: path.join(root, "out", "painel_bundle"),
  onProgress: () => {} });
for (const estilo of ["documentario", "dinamico", "tecnico"]) {
  const props = { fundo: "trem.jpg", estilo, variante: "destaque" };
  const composition = await selectComposition({ serveUrl, id: "DemoDestaques", inputProps: props });
  await renderStill({ serveUrl, composition, inputProps: props, frame: 60, scale: 0.5,
    output: path.join(out, `dest_${estilo}.png`), timeoutInMilliseconds: 120000 });
  console.log("ok", estilo);
}
