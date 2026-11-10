// Prévia das peças do estilo ARQUIVO COLORIZADO: still de cada exemplo em painel/previas/ac_*.png (+ mp4 com --mp4)
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.join(root, "painel", "previas");
const serveUrl = await bundle({ entryPoint: path.join(root, "src", "exemplos", "ac_entry.tsx"), onProgress: () => {} });
const mp4 = process.argv.includes("--mp4");
for (const id of ["ExACPolaroids", "ExACLinha", "ExACBarras", "ExACDado", "ExACCitacao", "ExACMapa"]) {
  const composition = await selectComposition({ serveUrl, id, inputProps: {} });
  await renderStill({ serveUrl, composition, frame: 150, output: path.join(out, `ac_${id.slice(4).toLowerCase()}.png`), inputProps: {} });
  if (mp4) await renderMedia({ serveUrl, composition, codec: "h264", crf: 24, x264Preset: "veryfast", concurrency: 3,
    outputLocation: path.join(out, `ac_${id.slice(4).toLowerCase()}.mp4`), inputProps: {} });
  console.log("ok", id);
}
