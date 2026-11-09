"""Corta as JANELAS aprovadas na folha de contato em arquivos prontos para o Remotion.

Entrada: data/source_side.json
  {"yt:ID" | "cm:File:...": {"verdict": "ok"|"reject", "tags": [...], "note": "...",
     "windows": [[inicio_s, fim_s] | [inicio_s, fim_s, [tags]], ...]}}
Saída: public/stock/<clip>.mp4 (1920x1080, 30 fps, mudo, H.264) + data/clips.json (mesclado com o disco)
  - YouTube: scripts/slice_dl.py (faixa de bytes; corta 12% da borda e reajusta 16:9)
  - Commons: arquivo local (data/commons_files.json), recorte por ffmpeg, sem corte de borda
MAX_PER_SOURCE limita janelas por fonte (fontes aprovadas no olho podem subir via "max" no side).
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import hashlib, json, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from local_yt import local_yt

# 21/09/2026: corte de clipe no NVENC da GPU (2-3x mais rápido que o x264 e sem ocupar os 12 núcleos).
# Cai para o x264 se a GPU não estiver disponível (ou com --cpu).
def _tem_nvenc():
    if "--cpu" in sys.argv:
        return False
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=256x256:d=0.1",
                        "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True, text=True)
    return r.returncode == 0


ENC = (["-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq", "-rc", "constqp", "-qp", "19"]
       if _tem_nvenc() else ["-c:v", "libx264", "-preset", "medium", "-crf", "18"])


ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "public" / "stock"
MAX_PER_SOURCE = 12
MIN_GAP_S = 6.0  # distância mínima entre janelas da mesma fonte


def jload(p, default):
    return json.loads(p.read_text("utf-8")) if p.exists() else default


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", str(path)],
                       capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    return st.get("width"), st.get("height"), float(j.get("format", {}).get("duration", 0))


def valid(out, s, e):
    """Arquivo já cortado só é reaproveitado se estiver íntegro (corte interrompido/duas rodadas simultâneas deixam lixo)."""
    if not out.exists():
        return False
    w, h, dur = probe(out)
    return (w, h) == (1920, 1080) and dur >= (e - s) - 0.5


def clip_id(key, s):
    return "v" + hashlib.md5(f"{key}@{s:.2f}".encode()).hexdigest()[:8]


def fps_fonte(src):
    """Quadros por segundo da fonte (0 se não der para ler)."""
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                            "-of", "csv=p=0", str(src)], capture_output=True, text=True, timeout=60).stdout.strip()
        n, d = (r.split("/") + ["1"])[:2]
        return float(n) / float(d or 1)
    except Exception:  # noqa: BLE001
        return 0.0


def cut_commons(src, s, e, out, crop=None):
    vf = "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,fps=30"
    # 16/10/2026 FILME TREMIDO (tanques es): filme de arquivo a 24 q/s virava 30 q/s repetindo 1 quadro a cada 5 —
    # soluço contínuo no movimento. Fonte de 12-28 q/s agora vai a 30 q/s por interpolação (framerate: quadros
    # intermediários misturados), mesma duração e mesmo tempo, sem quadro repetido.
    q = fps_fonte(src)
    if 12 <= q < 28:
        vf = "framerate=fps=30," + vf
    if crop:  # "w:h:x:y" — tira texto queimado nas bordas (telemetria do ROV) antes da escala
        vf = f"crop={crop}," + vf
    ua = ["-user_agent", "Mozilla/5.0 abismo-pipeline/1.0 (seu-email@exemplo.com)",
          "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5"] if str(src).startswith("http") else []
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ua, "-ss", f"{s:.3f}", "-i", src,
                    "-t", f"{e - s:.3f}", "-an", "-vf", vf, *ENC,
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)


def main():
    side = jload(D / "source_side.json", {})
    cm_files = jload(D / "commons_files.json", {})
    cm_pool = jload(D / "commons_video_pool.json", {})
    yt_pool = jload(D / "yt_pool.json", {})
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for key, sd in side.items():
        if sd.get("verdict") != "ok":
            continue
        wins = sorted(sd.get("windows", []), key=lambda w: w[0])
        kept = []
        for w in wins:
            if kept and w[0] < kept[-1][1]:  # janelas da mesma fonte nunca se sobrepõem
                continue
            kept.append(w)
        for w in kept[: sd.get("max", MAX_PER_SOURCE)]:
            s, e = float(w[0]), float(w[1])
            if key.startswith("yt:"):
                # regra de classe: os últimos 10% do vídeo do YouTube trazem cartão final / logo / fade com texto
                d = (yt_pool.get(key[3:], {}) or {}).get("duration") or 0
                if d and e > 0.90 * d:
                    continue
            tags = w[2] if len(w) > 2 else sd["tags"]
            jobs.append((key, s, e, tags, sd))
    lib = {c["id"]: c for c in jload(D / "clips.json", {"clips": []})["clips"]}
    todo_yt = [j for j in jobs if j[0].startswith("yt:")]
    todo_cm = [j for j in jobs if j[0].startswith("cm:")]
    todo_api = [j for j in jobs if j[0].startswith(("px:", "pb:", "dv:"))]
    api_pool = jload(D / "stock_api_pool.json", {})
    done = []

    def meta(key, sd):
        if key.startswith("yt:"):
            e = yt_pool.get(key[3:], {})
            return {"channel": e.get("channel"), "url": e.get("url"), "title": e.get("title"),
                    "manual": bool(e.get("manual")),  # baixado a mao pelo usuario: credita por titulo + canal
                    "license": "YouTube (uso justo, trecho curto e mudo)"}
        if key.startswith(("px:", "pb:", "dv:")):
            e = api_pool.get(key, {})
            return {"title": e.get("desc"), "url": e.get("page"), "license": e.get("license"), "artist": e.get("author"),
                    "credit": f"{e.get('author')} / {e.get('site')}"}
        e = cm_pool.get(key[3:], {})
        return {"title": key[3:], "url": e.get("descurl"), "license": e.get("license"), "artist": e.get("artist"), "credit": e.get("credit")}

    def finish(key, s, e, tags, sd, out):
        w, h, dur = probe(out)
        if (w, h) != (1920, 1080) or dur < (e - s) - 0.5:
            print(f"[verificação FALHOU] {out.name} {w}x{h} {dur:.1f}s", flush=True)
            return None
        c = {"id": out.stem, "kind": "video", "file": f"stock/{out.name}", "dur": int(dur * 30) - 2, "tags": tags,
             "source": key, "window": [s, e], "era": sd.get("era", "modern"), **meta(key, sd)}
        done.append(c)
        return c

    def do_cm(job):
        key, s, e, tags, sd = job
        out = OUT / f"{clip_id(key, s)}.mp4"
        src = cm_files.get(key[3:])
        if not src:  # sem arquivo local: corta direto da URL do Commons (sequencial, -ss antes do -i)
            src = (cm_pool.get(key[3:]) or {}).get("url", "").split("?")[0]
            if not src:
                print(f"[sem arquivo local nem URL] {key[:80]}", flush=True); return
        if not valid(out, s, e):
            try:
                cut_commons(src, s, e, out, sd.get("crop"))
            except subprocess.CalledProcessError as ex:
                print(f"[ffmpeg] {key[:60]} {ex}", flush=True); return
        finish(key, s, e, tags, sd, out)

    with ThreadPoolExecutor(1) as ex:  # Commons pela URL: sequencial (429 em acesso paralelo)
        list(ex.map(do_cm, todo_cm))

    def do_api(job):  # Pexels/Pixabay: recorte direto do mp4 no CDN (sem marca -> sem corte de borda)
        key, s, e, tags, sd = job
        out = OUT / f"{clip_id(key, s)}.mp4"
        src = (api_pool.get(key) or {}).get("file")
        if not src:
            print(f"[api sem arquivo] {key}", flush=True); return
        if not valid(out, s, e):
            try:
                cut_commons(src, s, e, out)
            except subprocess.CalledProcessError as ex:
                print(f"[ffmpeg api] {key} {s}: {ex}", flush=True); return
        finish(key, s, e, tags, sd, out)

    with ThreadPoolExecutor(2) as ex:
        list(ex.map(do_api, todo_api))
    slices = jload(D / "yt_slices.json", {})  # janelas baixadas pelo yt_win_dl (só o trecho aprovado)

    def corta_yt(job):
        """Corta a janela do arquivo local (trecho do yt_win_dl ou vídeo inteiro). 3 em paralelo.

        21/09/2026: tentei cortar direto da URL do stream (sem extração), mas o YouTube estrangula leituras
        longas sem o nsig decifrado: 3 janelas levaram 7m42 e terminaram em 403. Quadro solto (a folha de
        sondagem) funciona porque são poucos KB; janela de 10 s, não. Por isso a janela continua vindo pelo
        yt_win_dl (yt-dlp), que gasta 1 extração por vídeo.
        """
        key, s, e, tags, sd = job
        out = OUT / f"{clip_id(key, s)}.mp4"
        if valid(out, s, e):
            return key, s, e, tags, sd, out
        sl = next((x for x in slices.get(key, []) if abs(x["s"] - s) < 0.01 and (ROOT / x["file"]).exists()), None)
        loc = ROOT / sl["file"] if sl else local_yt(key[3:])
        s_loc, e_loc = (sl["offset"], sl["offset"] + (e - s)) if sl else (s, e)
        if loc:
            # fonte 720p: corte de borda leve (90%) para não ampliar demais; 1080p+: 76% como o slice_dl
            k = 0.90 if (probe(loc)[1] or 1080) < 1000 else 0.76
            # 26/09/2026 (Alang): marca d'água no rodapé central (WildFilmsIndia) -> data/yt_crop.json {"yt:ID": "top"}
            # ancora o recorte no topo e corta 30 % de baixo em vez do recorte centrado
            ytcrop = jload(D / "yt_crop.json", {}).get(key)
            if ytcrop == "top":
                k = 0.70
            vf = ("scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,fps=30"
                  if sd.get("nocrop") else
                  f"crop=iw*{k}:ih*{k}:(iw-iw*{k})/2:0,scale=1920:1080:flags=lanczos,setsar=1,fps=30" if ytcrop == "top"
                  else f"crop=iw*{k}:ih*{k},scale=1920:1080:flags=lanczos,setsar=1,fps=30")
            try:
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{s_loc:.3f}",
                                "-i", str(loc), "-t", f"{e_loc - s_loc:.3f}", "-an", "-vf", vf, *ENC,
                                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
            except subprocess.CalledProcessError as ex:
                print(f"[ffmpeg local] {key} {s}: {ex}", flush=True)
        return key, s, e, tags, sd, out

    with ThreadPoolExecutor(3) as ex:  # 3 cortes ao mesmo tempo (o stream aguenta; mais que isso dá I/O error)
        feitos = [r for r in ex.map(corta_yt, todo_yt) if r]
    for i, (key, s, e, tags, sd, out) in enumerate(feitos):
        if not valid(out, s, e):  # último recurso: faixa de bytes pelo slice_dl (gasta extração)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "slice_dl.py"), key[3:], f"{s}", f"{e - s}", str(out)]
                               + (["--nocrop"] if sd.get("nocrop") else []), capture_output=True, text=True)
            if r.returncode != 0:
                print(f"[slice_dl] {key} {s}: {r.stderr.strip().splitlines()[-1:]}", flush=True)
                continue
            time.sleep(3.5)
        finish(key, s, e, tags, sd, out)
        if (i + 1) % 10 == 0:
            print(f"[yt] {i + 1}/{len(feitos)}", flush=True)
    disk = {c["id"]: c for c in jload(D / "clips.json", {"clips": []})["clips"]}  # mescla com o disco
    disk.update(lib)
    for c in done:
        disk[c["id"]] = c
    (D / "clips.json").write_text(json.dumps({"clips": sorted(disk.values(), key=lambda c: c["id"])}, ensure_ascii=False, indent=1), "utf-8")
    print(f"[done] {len(done)} clipes nesta rodada, {len(disk)} na biblioteca")


if __name__ == "__main__":
    from trava import media   # 07/10/2026: render exclusivo (ver trava.py)
    with media("make_clips"):
        main()
