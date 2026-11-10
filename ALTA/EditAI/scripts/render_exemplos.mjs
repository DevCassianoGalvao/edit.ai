// Renderiza os EXEMPLOS de animação (src/exemplos) em out/exemplos/*.mp4 + folha. Bundle próprio.
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.join(root, "out", "exemplos");
fs.mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(root, "src", "index.ts"), onProgress: () => {} });
for (const [id, still] of [["ExMapaRota", 175], ["ExOdometro", 140], ["ExDocumento", 165], ["ExTermometro", 160]]) {
  const composition = await selectComposition({ serveUrl, id, inputProps: {} });
  await renderMedia({ serveUrl, composition, codec: "h264", crf: 20, x264Preset: "veryfast", concurrency: 3,
    outputLocation: path.join(out, `${id}.mp4`), inputProps: {} });
  await renderStill({ serveUrl, composition, frame: still, output: path.join(out, `${id}.png`), inputProps: {} });
  console.log("ok", id);
}
