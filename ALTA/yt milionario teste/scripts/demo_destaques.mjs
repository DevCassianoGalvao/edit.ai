// Gera as PNGs de prévia dos destaques (out/demo/*.png). Bundle próprio, não mexe no out/bundle do filme.
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.join(root, "out", "demo");
fs.mkdirSync(out, { recursive: true });

const CASOS = [
  ["01-documentario", { fundo: "f002100.jpg", estilo: "documentario", variante: "destaque" }],
  ["02-dinamico", { fundo: "f002100.jpg", estilo: "dinamico", variante: "destaque" }],
  ["03-tecnico", { fundo: "f002100.jpg", estilo: "tecnico", variante: "destaque" }],
  ["04-etiqueta", { fundo: "f003015.jpg", estilo: "documentario", variante: "etiqueta" }],
  ["05-numero", { fundo: "f000410.jpg", estilo: "documentario", variante: "numero" }],
  ["06-faixa", { fundo: "f003640.jpg", estilo: "documentario", variante: "faixa" }],
  ["07-comparativo", { fundo: "f004005.jpg", estilo: "tecnico", variante: "comparativo" }],
  ["08-cartao", { fundo: "f004005.jpg", estilo: "documentario", variante: "cartao" }],
  ["09-comparacao", { fundo: "f000410.jpg", estilo: "documentario", variante: "comparacao" }],
  ["10-fichas", { fundo: "f003640.jpg", estilo: "documentario", variante: "fichas" }],
  ["11-palavra", { fundo: "f002100.jpg", estilo: "documentario", variante: "palavra" }],
];

const serveUrl = await bundle({ entryPoint: path.join(root, "src", "index.ts"), onProgress: () => {} });
for (const [nome, props] of CASOS) {
  const composition = await selectComposition({ serveUrl, id: "DemoDestaques", inputProps: props });
  await renderStill({ serveUrl, composition, inputProps: props, frame: 60,
    output: path.join(out, `${nome}.png`), timeoutInMilliseconds: 120000 });
  console.log("ok", nome);
}
