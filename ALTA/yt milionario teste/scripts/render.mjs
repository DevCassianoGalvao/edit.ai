// O ÚNICO render de vídeo do projeto. Usa o bundle verificado (out/bundle_path.txt).
// Render em BLOCOS com retomada: cada bloco (CHUNK quadros, mudo) vira out/chunks/part_NN.mp4 e só é
// refeito se faltar ou estiver incompleto; bloco que falha (ex.: delayRender estourado por máquina
// ocupada) é tentado de novo até 3 vezes, sem perder os blocos prontos. No fim: concat sem recodificar
// + áudio original (public/audio.mp3) -> out/final.mp4.
// Grava progresso em out/render_progress.txt (a tarefa agendada roda sem console).
import { renderMedia, selectComposition } from "@remotion/renderer";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const serveUrl = fs.readFileSync(path.join(root, "out", "bundle_path.txt"), "utf8").trim();
const prog = path.join(root, "out", "render_progress.txt");
const log = (s) => fs.appendFileSync(prog, `${new Date().toISOString()} ${s}\n`);
const CHUNK = 6000; // 200 s por bloco
const TRIES = 3;
const chunkDir = path.join(root, "out", "chunks");
fs.mkdirSync(chunkDir, { recursive: true });

const frames = (file) => {
  try {
    const out = execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-count_packets",
      "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", file], { encoding: "utf8" });
    return parseInt(out.trim(), 10) || 0;
  } catch {
    return 0;
  }
};

log(`inicio (blocos de ${CHUNK}) serveUrl=${serveUrl}`);
const composition = await selectComposition({ serveUrl, id: "Main", inputProps: {} });
const total = composition.durationInFrames;
const parts = [];
const t0 = Date.now();
for (let a = 0, n = 0; a < total; a += CHUNK, n++) {
  const b = Math.min(total, a + CHUNK) - 1;
  const file = path.join(chunkDir, `part_${String(n).padStart(2, "0")}.mp4`);
  parts.push(file);
  if (fs.existsSync(file) && frames(file) === b - a + 1) {
    log(`bloco ${n} [${a}-${b}] já pronto`);
    continue;
  }
  for (let k = 1; ; k++) {
    try {
      let last = -1;
      await renderMedia({
        serveUrl,
        composition,
        codec: "h264",
        crf: 16,
        muted: true,
        frameRange: [a, b],
        outputLocation: file,
        inputProps: {},
        concurrency: 5,  // Chrome do usuário fechado, 12 núcleos, CPU a 7% com 2 (a queda com 3 foi com Chrome aberto)
        timeoutInMilliseconds: 300000,
        offthreadVideoCacheSizeInBytes: 2 * 1024 * 1024 * 1024,
        onProgress: ({ progress }) => {
          const p = Math.floor(progress * 10) * 10;
          if (p !== last) {
            last = p;
            const done = a + progress * (b - a + 1);
            const el = (Date.now() - t0) / 1000;
            log(`bloco ${n} ${p}% | filme ${((100 * done) / total).toFixed(1)}% decorrido=${(el / 60).toFixed(1)}min`);
          }
        },
      });
      const got = frames(file);
      if (got !== b - a + 1) throw new Error(`bloco ${n} com ${got} quadros, esperado ${b - a + 1}`);
      break;
    } catch (e) {
      log(`bloco ${n} tentativa ${k} FALHOU: ${String(e.message || e).slice(0, 300)}`);
      fs.rmSync(file, { force: true });
      if (k >= TRIES) throw e;
    }
  }
}
const list = path.join(chunkDir, "list.txt");
fs.writeFileSync(list, parts.map((p) => `file '${p.replace(/\\/g, "/").replace(/'/g, "'\\''")}'`).join("\n"));
// concat direto no mux final (sem out/video_only.mp4 intermediário: economiza ~5 GB de disco no pico)
const video = list;
// blocos são mudos: o áudio final = narração + trilha (public/music.m4a, já com volume guiado pela fala), sem normalizar
const music = path.join(root, "public", "music.m4a");
const cfgPath = path.join(root, "data", "pipeline_config.json");
const cfg = fs.existsSync(cfgPath) ? JSON.parse(fs.readFileSync(cfgPath, "utf8")) : {};
const audioArgs = cfg.music !== false && fs.existsSync(music) // "music": false = filme sem trilha
  ? ["-i", music, "-filter_complex", "[1:a][2:a]amix=inputs=2:normalize=0:duration=first[a]", "-map", "0:v:0", "-map", "[a]"]
  : ["-map", "0:v:0", "-map", "1:a:0"];
const finalTmp = path.join(root, "out", "final_tmp.mp4");
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", video, "-i", path.join(root, "public", "audio.mp3"), ...audioArgs,
  "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", finalTmp]);
fs.renameSync(finalTmp, path.join(root, "out", "final.mp4"));  // final.mp4 só aparece inteiro
log(`FIM out/final.mp4 (${parts.length} blocos, ${((Date.now() - t0) / 60000).toFixed(1)}min)`);
