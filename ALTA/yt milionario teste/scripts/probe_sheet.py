"""Folha de sondagem de FONTES: 8 quadros por fonte, tirados direto do stream
(ffmpeg -ss por faixa HTTP — nada é baixado inteiro). 6 fontes por folha.

Uso: python probe_sheet.py sources.json OUTDIR
  sources.json = [{"key": "yt:ID" | "cm:File:...", "url": stream_or_page, "duration": s, "label": "..."}]
Saída: OUTDIR/sheet_NN.jpg + OUTDIR/index.json (linha -> fonte)
"""
import json, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prefilter

TXT = False

TW, TH, COLS, ROWS = 400, 225, 8, 6
UA_CM = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)


CM_FILES = Path(__file__).resolve().parent.parent / "data" / "commons_files.json"


_URLS = {}  # folha densa: várias linhas da mesma fonte gastam 1 extração (a URL do googlevideo vale horas)
_URLS_LOCK = __import__("threading").Lock()


def stream_url(src):
    with _URLS_LOCK:
        if src["key"] not in _URLS:
            _URLS[src["key"]] = _stream_url(src)
        return _URLS[src["key"]]


UA_YT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def _stream_url(src):
    if src["key"].startswith("yt:"):
        # 21/09/2026: o yt_probe_stream.py já entrega a URL DIRETA do stream (uma extração por vídeo, sem baixar).
        # Usar essa URL é o que permite sondar sem baixar 10-15 GB — e evita uma segunda extração por fonte.
        if "googlevideo.com" in src["url"]:
            return src["url"], UA_YT
        from local_yt import local_yt
        loc = local_yt(src["key"][3:])  # baixado à mão em input/youtube
        if loc:
            return loc, None
        # só https progressivo/DASH mp4 — HLS (m3u8) não aceita -ss rápido
        import yt_quota
        yt_quota.acquire(f"probe {src['key']}")  # cota compartilhada entre sessões
        p = subprocess.run(yt_quota.ytdlp("-g", "--no-warnings", "-f",
                                          "bestvideo[height<=1080][ext=mp4][protocol=https]", src["url"]),
                           capture_output=True, text=True, timeout=120)
        yt_quota.report(p.stderr)
        return p.stdout.strip().splitlines()[0] if p.stdout.strip() else None, None
    if src["key"].startswith(("px:", "pb:", "dv:")):  # Pexels/Pixabay: arquivo mp4 no CDN aceita -ss por faixa HTTP
        return src["url"], None
    # Commons: só arquivo local (upload.wikimedia.org dá 429 em acesso paralelo)
    files = json.loads(CM_FILES.read_text("utf-8")) if CM_FILES.exists() else {}
    loc = files.get(src["key"][3:])
    # sem arquivo local (filme do abismo: 1080p do Ifremer de até 1 GB cada), lê direto do upload.wikimedia.org —
    # a folha é sequencial, um quadro por vez, então não cai no 429 do acesso paralelo
    return (loc or src["url"].split("?")[0]), (None if loc else UA_CM)


def grab(url, ua, t, out):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if ua:
        cmd += ["-user_agent", ua]
    if str(url).startswith("http"):  # CDN (Pexels/Pixabay) derruba conexões sob carga: reconectar
        cmd += ["-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5"]
    cmd += ["-ss", f"{t:.2f}", "-i", url, "-frames:v", "1", "-vf",
            f"scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH},format=yuvj420p",
            "-strict", "unofficial", str(out)]
    p = None
    for k in range(3):  # "I/O error" do CDN é passageiro: até 3 tentativas com espera
        try:
            p = subprocess.run(cmd, timeout=180, capture_output=True, text=True, errors="replace")
        except subprocess.TimeoutExpired:
            print(f"[grab] timeout {t:.0f}s {url[:80]}", flush=True)
            return None
        if out.exists():
            return out
        time.sleep(3 * (k + 1))
    if not out.exists():
        print(f"[grab] falhou {t:.0f}s {url[:80]}: {p.stderr.strip().splitlines()[-1:] }", flush=True)
    return out if out.exists() else None


def row(src, td):
    try:
        url, ua = stream_url(src)
    except Exception:  # noqa: BLE001
        url, ua = None, None
    d = float(src.get("duration") or 60)
    # folha densa: "t0"/"t1" restringem a linha a um trecho da fonte (8 quadros por trecho em vez de 8 no vídeo todo)
    t0, t1 = float(src.get("t0", 0)), float(src.get("t1", d))
    tiles = []
    for i in range(COLS):
        t = t0 + (t1 - t0) * (0.06 + 0.88 * i / (COLS - 1))
        f = Path(td) / f"{abs(hash((src['key'], t0)))}_{i}.jpg"
        tiles.append(grab(url, ua, t, f) if url else None)
    return tiles


def main():
    srcs = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    global TXT
    TXT = "--sem-aviso-texto" not in sys.argv and prefilter.disponivel()
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    index = []
    # fontes em CDN (Pexels/Pixabay) com 6 threads recebem "I/O error" em massa → 2 threads
    workers = 2 if any(s["key"].startswith(("px:", "pb:", "dv:")) for s in srcs) else 6
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(workers) as ex:
        rows = list(ex.map(lambda s: row(s, td), srcs))
        for si in range(0, len(srcs), ROWS):
            sheet = Image.new("RGB", (TW * COLS, (TH + 34) * ROWS), (20, 20, 20))
            dr = ImageDraw.Draw(sheet)
            for r, (src, tiles) in enumerate(zip(srcs[si:si + ROWS], rows[si:si + ROWS])):
                y = r * (TH + 34)
                n = si + r
                dr.text((6, y + 4), f"#{n}  {src['label'][:150]}", fill=(255, 220, 0), font=FONT)
                for c, tpath in enumerate(tiles):
                    if tpath and Path(tpath).exists():  # 10/10: ladrilho que o ffmpeg não gravou derrubava a folha
                        sheet.paste(Image.open(tpath), (c * TW, y + 34))
                        # 21/09/2026: aviso automático de texto queimado (legenda/ficha/marca d'água) — o olho
                        # continua decidindo, mas o ladrilho marcado já entra com suspeita.
                        if TXT and prefilter.tem_texto(str(tpath))[0]:
                            dr.rectangle([c * TW + TW - 54, y + 38, c * TW + TW - 6, y + 62], fill=(150, 0, 0))
                            dr.text((c * TW + TW - 49, y + 40), "TXT", fill=(255, 255, 255), font=FONT)
                    else:
                        dr.rectangle([c * TW, y + 34, c * TW + TW - 2, y + 34 + TH], fill=(90, 0, 0))
                index.append({"n": n, "sheet": si // ROWS, "key": src["key"], "ok_tiles": sum(t is not None and Path(t).exists() for t in tiles)})
            p = out / f"sheet_{si // ROWS:02d}.jpg"
            sheet.save(p, quality=82)
            print("[sheet]", p, flush=True)
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), "utf-8")


if __name__ == "__main__":
    main()
