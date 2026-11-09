// Bundle VERIFICADO antes do render: todo asset citado na timeline existe no bundle com o
// mesmo tamanho do original em public/. Grava o caminho em out/bundle_path.txt.
// Uso: node scripts/bundle.mjs
import { bundle } from "@remotion/bundler";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const timeline = JSON.parse(fs.readFileSync(path.join(root, "data/timeline.json"), "utf8"));
const outDir = path.join(root, "out", "bundle");
fs.rmSync(outDir, { recursive: true, force: true });
const t0 = Date.now();
const serveUrl = await bundle({
  entryPoint: path.join(root, "src/index.ts"),
  publicDir: path.join(root, "public"),
  outDir,
  onProgress: () => {},
});
const needed = new Set(["audio.mp3"]);
if (fs.existsSync(path.join(root, "public", "music.m4a"))) needed.add("music.m4a");
for (const it of timeline.items) if (it.type === "cut" && it.src) needed.add(it.src);
let bad = 0;
for (const rel of needed) {
  const a = path.join(root, "public", rel);
  const b = path.join(serveUrl, "public", rel);
  const sa = fs.existsSync(a) ? fs.statSync(a).size : -1;
  const sb = fs.existsSync(b) ? fs.statSync(b).size : -2;
  if (sa !== sb) {
    bad++;
    console.log(`[bundle] DIVERGE ${rel}: public ${sa} / bundle ${sb}`);
  }
}
console.log(`[bundle] ${needed.size} assets verificados, ${bad} divergentes, ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${serveUrl}`);
fs.writeFileSync(path.join(root, "out", "bundle_path.txt"), serveUrl);
process.exit(bad ? 1 : 0);
