// Baixa UMA vez as fontes das cenas para public/fonts, para o render não buscar no Google a cada aba do Chrome
// (render híbrido do filme CN: um trecho falhou com delayRender "Fetching IBM Plex Sans font" estourando 58 s).
// Os endereços vêm do próprio @remotion/google-fonts instalado (mesma versão que as cenas usavam).
// Uso: node scripts/fetch_fonts.mjs  -> public/fonts/<Família>-<peso>-<subconjunto>.woff2
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(import.meta.url);
const WANT = [
  ["Oswald", ["500", "700"]],
  ["IBMPlexSans", ["400", "500", "700"]],
  ["CourierPrime", ["400", "700"]], // máquina de escrever: cartões/fichas (pedido do usuário, 21/09/2026)
];
const SUBSETS = ["latin", "latin-ext"];
const dir = path.join(root, "public", "fonts");
fs.mkdirSync(dir, { recursive: true });
let n = 0;
for (const [name, weights] of WANT) {
  const info = require(path.join(root, "node_modules", "@remotion", "google-fonts", "dist", "cjs", `${name}.js`)).getInfo();
  for (const w of weights) {
    for (const s of SUBSETS) {
      const url = info.fonts?.normal?.[w]?.[s];
      if (!url) throw new Error(`${name} ${w} ${s}: sem endereço no pacote`);
      const out = path.join(dir, `${name}-${w}-${s}.woff2`);
      if (fs.existsSync(out) && fs.statSync(out).size > 1000) {
        console.log(`já existe ${path.basename(out)}`);
        continue;
      }
      const r = await fetch(url);
      if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
      const buf = Buffer.from(await r.arrayBuffer());
      fs.writeFileSync(out, buf);
      n++;
      console.log(`${path.basename(out)} ${buf.length} bytes`);
    }
  }
}
console.log(`[fonts] ${n} baixadas -> public/fonts`);
