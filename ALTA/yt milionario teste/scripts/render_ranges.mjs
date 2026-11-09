// Remotion SÓ nos trechos que o ffmpeg não reproduz igual (animações, fades, fotos) — parte do render híbrido.
// Lê out/hybrid/plan.json (gerado por scripts/render_hybrid.py) e o bundle verificado (out/bundle_path.txt).
// Cada trecho vira out/hybrid/<nome>.mp4 (mudo, H.264 CRF 16) e só é refeito se faltar ou tiver o nº de quadros errado.
import { openBrowser, renderMedia, selectComposition } from "@remotion/renderer";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const plan = JSON.parse(fs.readFileSync(path.join(root, "out", "hybrid", "plan.json"), "utf8"));
const serveUrl = fs.readFileSync(path.join(root, "out", "bundle_path.txt"), "utf8").trim();
const prog = path.join(root, "out", "hybrid", "progress.txt");
const log = (s) => fs.appendFileSync(prog, `${new Date().toISOString()} ${s}\n`);
const TRIES = 3;

const frames = (file) => {
  try {
    const out = execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-count_packets",
      "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", file], { encoding: "utf8" });
    return parseInt(out.trim(), 10) || 0;
  } catch {
    return 0;
  }
};

// 27/09/2026 (painel): nível de render (pipeline_config "render.qualidade"). alta = igual a antes (crf 16 veryfast).
// "superfast" ainda usa CABAC/High: a junção sem recodificar com os segmentos do ffmpeg continua válida.
let QUAL = "alta";
try {
  QUAL = (JSON.parse(fs.readFileSync(path.join(root, "data", "pipeline_config.json"), "utf8")).render || {}).qualidade || "alta";
} catch {}
const ENC = { alta: [16, "veryfast"], media: [17, "veryfast"], rapida: [19, "superfast"] }[QUAL] || [16, "veryfast"];
const segs = plan.segments.filter((s) => s.engine === "remotion");
// 14/10/2026: 30 s padrão estourou com o PC ocupado ("Timed out ... setting up the headless browser")
const composition = await selectComposition({ serveUrl, id: "Main", inputProps: {}, timeoutInMilliseconds: 120000 });
if (composition.durationInFrames !== plan.durationInFrames) {
  throw new Error(`bundle com ${composition.durationInFrames} quadros, plano com ${plan.durationInFrames}: refazer o bundle`);
}
// 29/09/2026: UM navegador para o filme inteiro (antes cada trecho abria e fechava o Chrome: ~60 trechos por filme)
const browser = await openBrowser("chrome", { shouldDumpIo: false });
const t0 = Date.now();
log(`remotion inicio: ${segs.length} trechos, ${segs.reduce((n, s) => n + s.end - s.start, 0)} quadros`);
for (const seg of segs) {
  const file = path.join(root, seg.file);
  const n = seg.end - seg.start;
  if (fs.existsSync(file) && frames(file) === n) {
    log(`${seg.name} já pronto`);
    continue;
  }
  for (let k = 1; ; k++) {
    try {
      await renderMedia({
        serveUrl,
        composition,
        codec: "h264",
        crf: ENC[0],
        // 24/09/2026: x264 "veryfast" no lugar do padrão "medium" — contra uma referência quase sem perda, mesma
        // qualidade (PSNR 41,69 x 41,64 dB), ~10 % mais rápido e CPU do sistema de ~58 % para ~40 %.
        x264Preset: ENC[1],
        muted: true,
        frameRange: [seg.start, seg.end - 1],
        outputLocation: file,
        inputProps: {},
        concurrency: 3, // modo leve: 5 abas + cache de 2 GB pesavam num PC de 16 GB
        timeoutInMilliseconds: 300000,
        offthreadVideoCacheSizeInBytes: 1 * 1024 * 1024 * 1024,
        puppeteerInstance: browser,
      });
      const got = frames(file);
      if (got !== n) throw new Error(`${seg.name} com ${got} quadros, esperado ${n}`);
      log(`${seg.name} remotion ok (${n} quadros) decorrido=${((Date.now() - t0) / 60000).toFixed(1)}min`);
      break;
    } catch (e) {
      log(`${seg.name} tentativa ${k} FALHOU: ${String(e.message || e).slice(0, 300)}`);
      fs.rmSync(file, { force: true });
      if (k >= TRIES) throw e;
    }
  }
}
await browser.close({ silent: true }).catch(() => {});
log(`remotion FIM ${((Date.now() - t0) / 60000).toFixed(1)}min`);
