"""Render HÍBRIDO: o ffmpeg monta os cortes secos de vídeo (zoom linear 1 -> 1+videoDrift pelo centro, igual ao
VideoCut do Remotion) e o Remotion renderiza só o que o ffmpeg não reproduz igual: animações, fades de entrada
(fadeIn), quadros de cauda (tail) e fotos. Tem que bater quadro a quadro com o render 100% Remotion
(validar com scripts/compare_render.py).

Etapas (retomáveis: segmento só é refeito se faltar ou tiver o nº de quadros errado):
  1. plano   -> out/hybrid/plan.json (segmentos contíguos cobrindo [0, durationInFrames))
  2. Remotion -> node scripts/render_ranges.mjs (bundle verificado em out/bundle_path.txt; roda SOZINHO)
  3. ffmpeg  -> cada lote de até MAX_PIECES cortes vira um mp4 (pool de WORKERS processos)
  4. junção sem recodificar + narração + trilha -> --out (padrão out/final.mp4), conferida com ffprobe

Uso: python render_hybrid.py [--out out/final.mp4] [--plan-only] [--skip-remotion] [--workers 3]
"""
import json, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D, HY = ROOT / "data", ROOT / "out" / "hybrid"
PROG = HY / "progress.txt"
# prioridade do render: NORMAL por padrão (pedido do usuário, 19/09); "--prio baixa" deixa o Windows atender o usuário antes.
# O que travava o PC não era a prioridade e sim 3 ffmpeg sem teto de threads: o teto (-threads 4, 2 lotes) é o que resolve.
LOW = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0) if "baixa" in sys.argv else 0
FOTO_FF = "--fotos-remotion" not in sys.argv  # 21/09: fotos no ffmpeg (ver photo_filter)
MIN_FF = 30        # trecho de ffmpeg menor que isso entre dois do Remotion vai para o Remotion
MAX_PIECES = 20    # cortes por mp4 do ffmpeg (cada corte abre um decodificador)
# mesmos parâmetros dos blocos do Remotion (lidos de out/chunks/part_00.mp4): junção sem recodificar
# base de tempo 1/90000 igual à do Remotion: misturando 1/15360 a junção sem recodificar estraga os tempos
# (teste do CN: 3 trechos de 105,27 s viraram 563 s; o filme inteiro dizia 8032 s em vez de 1923 s)
_COMUM = ["-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuvj420p", "-color_range", "pc",
          "-colorspace", "bt470bg", "-video_track_timescale", "90000"]
_X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "16"] + _COMUM
# 21/09/2026: NVENC da GPU. Medido em 360 quadros de foto com zoom: x264 crf16 12,1 s / 13,1 MB / SSIM 0,9599 x
# nvenc p7 qp18 5,0 s / 13,6 MB / SSIM 0,9574 — mesmo tamanho e mesma qualidade, 2,4x mais rápido, e ainda
# libera a CPU (o que travava o PC). O H.264 de cada segmento continua High@4.0, então a junção SEM RECODIFICAR
# com os blocos x264 do Remotion segue válida (testado: SSIM 1,000 no segmento depois da junção).
# 10/10/2026: p4 no lugar do p7 — mesma imagem (SSIM 0,8453 x 0,8456 contra sem perda, qp 18 fixo) e 3x mais rápido
_NVENC = ["-c:v", "h264_nvenc", "-preset", "p4", "-tune", "hq", "-rc", "constqp", "-qp", "18"] + _COMUM


def _tem_nvenc():
    if "--cpu" in sys.argv:
        return False
    # 24/09/2026: o teste era 64x64, abaixo do mínimo do NVENC da RTX 2050 ("Frame Dimension less than the minimum
    # supported value") — a checagem falhava e TODO render caía calado no x264 da CPU. Testa em 256x256.
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=256x256:d=0.1",
                        "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True, text=True)
    return r.returncode == 0


X264 = _NVENC if _tem_nvenc() else _X264  # nome mantido: é a lista de parâmetros do codificador dos segmentos
if X264 is _X264 and "--cpu" not in sys.argv:
    print("[render] AVISO: NVENC indisponível — codificando no x264 da CPU (mais lento e mais pesado)", flush=True)
# 27/09/2026 (painel): nível de render — pipeline_config "render.qualidade": alta (padrão, igual a antes) | media | rapida.
# Só o preset/qp mudam: perfil High@4.0, pix_fmt e base de tempo ficam iguais, a junção sem recodificar continua valendo.
try:
    _QUAL = (json.loads((ROOT / "data" / "pipeline_config.json").read_text("utf-8")).get("render") or {}).get("qualidade", "alta")
except Exception:  # noqa: BLE001
    _QUAL = "alta"
if _QUAL in ("media", "rapida"):
    _troca = {"media": {"p7": "p5", "18": "19", "medium": "fast", "16": "17"},
              "rapida": {"p7": "p3", "18": "21", "medium": "veryfast", "16": "19"}}[_QUAL]
    X264 = [(_troca.get(v, v) if k and X264[k - 1] in ("-preset", "-qp", "-crf") else v) for k, v in enumerate(X264)]


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def log(s):
    HY.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')}Z {s}"
    print(line, flush=True)
    with PROG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    m = re.search(r"\d+", r.stdout)  # arquivo do Remotion sai "697," (vírgula no fim): int() direto dava 0
    return int(m.group(0)) if m else 0


def video_drift():
    m = re.search(r"videoDrift:\s*([0-9.]+)", (ROOT / "src/design/tokens.ts").read_text("utf-8"))
    if not m:
        raise SystemExit("videoDrift não encontrado em src/design/tokens.ts")
    return float(m.group(1))


def photo_push():
    m = re.search(r"photoPush:\s*([0-9.]+)", (ROOT / "src/design/tokens.ts").read_text("utf-8"))
    if not m:
        raise SystemExit("photoPush não encontrado em src/design/tokens.ts")
    return float(m.group(1))


def build_plan():
    meta = json.loads((D / "source_meta.json").read_text("utf-8"))
    total = meta["durationInFrames"]
    items = sorted(json.loads((D / "timeline.json").read_text("utf-8"))["items"], key=lambda it: it["from"])
    remo = bytearray(total)

    def mark(a, b):
        for f in range(max(0, a), min(total, b)):
            remo[f] = 1

    top = [None] * total  # item visível por cima em cada quadro (sem contar tail/fade, que já vão pro Remotion)
    for it in items:
        a, dur, tail, fade = it["from"], it["dur"], it.get("tail", 0), it.get("fadeIn", 0)
        # corte com motion graphic sobreposto (campo ov) não pode ser corte seco do ffmpeg: vai para o Remotion
        # 21/09/2026: FOTO também é corte seco do ffmpeg (photo_filter reproduz o PhotoCut) — antes o Remotion
        # desenhava 74-86 % dos quadros do filme só por causa delas. "--fotos-remotion" volta ao comportamento antigo.
        is_ff = it["type"] == "cut" and not it.get("ov") and (
            (it.get("kind") == "video" and not it.get("move")) or (it.get("kind") == "photo" and FOTO_FF))
        if not is_ff:
            mark(a, a + dur + tail)
        if fade > 0:
            mark(a, a + fade)
        if tail > 0:
            mark(a + dur, a + dur + tail)
        for f in range(max(0, a), min(total, a + dur)):
            top[f] = it
    if any(t is None for t in top):
        raise SystemExit(f"timeline com buraco no quadro {top.index(None)}")
    runs, f = [], 0
    while f < total:  # trechos contíguos por motor
        g = f
        while g < total and remo[g] == remo[f]:
            g += 1
        runs.append(["remotion" if remo[f] else "ffmpeg", f, g])
        f = g
    for r in runs:  # trecho curto de ffmpeg entre dois do Remotion não compensa
        if r[0] == "ffmpeg" and r[2] - r[1] < MIN_FF and 0 < runs.index(r) < len(runs) - 1:
            r[0] = "remotion"
    merged = []
    for r in runs:
        if merged and merged[-1][0] == r[0]:
            merged[-1][2] = r[2]
        else:
            merged.append(list(r))
    drift = video_drift()
    leads = {}

    def lead(src):
        # O Remotion escolhe o quadro do clipe pelo TEMPO; o trim do ffmpeg, pelo ÍNDICE. Clipe cujo 1º quadro está em
        # 0,033 s (os do YouTube via slice_dl) mostra o quadro índice (t·30 − 1), com o 1º quadro repetido no início.
        # Medido no filme CN: c001015 SSIM 0,886 com o índice direto -> 0,992 com um quadro de atraso.
        if src not in leads:
            r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=start_time",
                                "-of", "csv=p=0", str(ROOT / "public" / src)], capture_output=True, text=True)
            m = re.search(r"-?\d+(?:\.\d+)?", r.stdout)  # alguns clipes saem "0.000000," (vírgula no fim)
            leads[src] = round(float(m.group(0)) * 30) if m else 0
        return leads[src]

    segs = []
    for engine, a, b in merged:
        if engine == "remotion":
            segs.append({"engine": "remotion", "start": a, "end": b})
            continue
        pieces, f = [], a
        while f < b:  # pedaços = trechos de um mesmo corte (cortes secos: fronteira de corte é fronteira livre)
            it = top[f]
            g = min(b, it["from"] + it["dur"])
            f0 = f - it["from"]
            idx = 0 if it.get("kind") == "photo" else it.get("trimBefore", 0) + f0 - lead(it["src"])
            foto = it.get("kind") == "photo"
            pieces.append({"id": it["id"], "src": it["src"], "start": f, "end": g, "f0": f0,
                           "src_frame": 0 if foto else max(0, idx), "clone": 0 if foto else max(0, -idx),
                           "seq": it["dur"] + it.get("tail", 0), "kind": it.get("kind", "video"),
                           "move": it.get("move"), "lado": it.get("lado", "quente")})
            f = g
        for k in range(0, len(pieces), MAX_PIECES):
            chunk = pieces[k:k + MAX_PIECES]
            segs.append({"engine": "ffmpeg", "start": chunk[0]["start"], "end": chunk[-1]["end"], "pieces": chunk})
    for i, s in enumerate(segs):
        s["name"] = f"s{i:03d}_{s['engine'][0]}_{s['start']}"
        s["file"] = f"out/hybrid/{s['name']}.mp4"
    pos = 0
    for s in segs:  # tiling exato
        if s["start"] != pos or s["end"] <= s["start"]:
            raise SystemExit(f"plano sem tiling em {s['name']}")
        pos = s["end"]
    if pos != total:
        raise SystemExit(f"plano termina em {pos}, filme tem {total}")
    plan = {"durationInFrames": total, "videoDrift": drift, "segments": segs}
    HY.mkdir(parents=True, exist_ok=True)
    (HY / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), "utf-8")
    nr = sum(s["end"] - s["start"] for s in segs if s["engine"] == "remotion")
    log(f"plano: {len(segs)} segmentos | Remotion {nr} quadros ({100 * nr / total:.1f}%) | ffmpeg {total - nr} quadros")
    return plan


def grade_filter(lado):
    """Grade de cor do tema (modo ULTRA, seção 5): contraste +12 %, saturação −10 %, tinte nas sombras e o oposto
    nos realces, vinheta forte. Mesmos números do CSS do Remotion (src/stock/StockClip.tsx) para foto e vídeo
    parecerem da mesma câmera. Fora do modo ULTRA devolve string vazia."""
    cfg = json.loads((D / "pipeline_config.json").read_text("utf-8")) if (D / "pipeline_config.json").exists() else {}
    if cfg.get("modo") != "ultra" or not (D / "tema_config.json").exists():
        return ""
    g = json.loads((D / "tema_config.json").read_text("utf-8"))["grade"]
    sh = g["frio_sombras"] if lado == "frio" else g["quente_sombras"]
    hi = g["frio_realces"] if lado == "frio" else g["quente_realces"]
    return (f"eq=contrast={g.get('contraste', 1.12)}:saturation={g.get('saturacao', 0.9)},"
            f"colorbalance=rs={sh[0]}:gs={sh[1]}:bs={sh[2]}:rh={hi[0]}:gh={hi[1]}:bh={hi[2]},"
            f"vignette=angle={g.get('vinheta', 'PI/4.5')}")


def zoom_filter(p, drift):
    s = f"(1+{drift}*((in)+{p['f0']})/{p['seq']})"
    a = f"((1-1/{s})/2)"
    return (f"perspective=x0='W*{a}':y0='H*{a}':x1='W*(1-{a})':y1='H*{a}':"
            f"x2='W*{a}':y2='H*(1-{a})':x3='W*(1-{a})':y3='H*(1-{a})':interpolation=linear:eval=frame")


# --------------------------------------------------------------------------------------- foto no ffmpeg (21/09/2026)
# O PhotoCut do Remotion faz: t = bezier(0.65,0,0.35,1) do tempo; escala 1+p*t (in) / 1+p-p*t (out) / 1+p (pan),
# e translada (t-0.5)*±p*0.8 da largura nos modos left/right (p = motion.photoPush).
# Para reproduzir no ffmpeg é preciso INVERTER a bezier: x(u) = 1.9u³ − 2.85u² + 1.95u e y(u) = 3u² − 2u³.
# 3 passos de Newton (a derivada 5.7u²−5.7u+1.95 nunca zera) dão erro 2e-7 — menos de 1/1000 de pixel.
# (in)-1: o contador "in" do perspective começa em 1 no primeiro quadro — medido com SSIM contra o Remotion
# (offset 0 -> 0,948; offset -1 -> 0,980).
NEWTON = ("st(1,clip(((in)-1+{f0})/{seq},0,1));st(2,ld(1));"
          + 3 * "st(2,ld(2)-(1.9*ld(2)^3-2.85*ld(2)^2+1.95*ld(2)-ld(1))/(5.7*ld(2)^2-5.7*ld(2)+1.95));"
          + "st(3,3*ld(2)^2-2*ld(2)^3);")  # ld(3) = t (progresso já suavizado)


def photo_filter(p, push):
    """Mesmo movimento do PhotoCut, em perspective com eval=frame (janela centrada = zoom pelo centro)."""
    pre = NEWTON.format(f0=p["f0"], seq=p["seq"])
    move = p.get("move") or "in"
    s = {"in": f"(1+{push}*ld(3))", "out": f"(1+{push}-{push}*ld(3))"}.get(move, f"(1+{push})")
    u = {"left": f"((ld(3)-0.5)*-{push}*0.8)", "right": f"((ld(3)-0.5)*{push}*0.8)"}.get(move, "0")
    xl = f"{pre}W*(0.5-(0.5+{u})/{s})"
    xr = f"{pre}W*(0.5+(0.5-{u})/{s})"
    yt = f"{pre}H*((1-1/{s})/2)"
    yb = f"{pre}H*(1-(1-1/{s})/2)"
    return (f"perspective=x0='{xl}':y0='{yt}':x1='{xr}':y1='{yt}':"
            f"x2='{xl}':y2='{yb}':x3='{xr}':y3='{yb}':interpolation=linear:eval=frame")


def render_ff(seg, drift):
    out = ROOT / seg["file"]
    n = seg["end"] - seg["start"]
    if out.exists() and frames(out) == n:
        return f"{seg['name']} já pronto"
    cmd, parts = ["ffmpeg", "-hide_banner", "-v", "error", "-y"], []
    push = photo_push()
    for k, p in enumerate(seg["pieces"]):
        L = p["end"] - p["start"]
        foto = p.get("kind") == "photo"
        if foto:  # 24/09/2026: a foto é decodificada UMA vez e o quadro é clonado na memória (tpad) — antes o
            # "-loop 1" redecodificava o JPEG 1920x1080 a cada quadro. "-framerate 30" é obrigatório: sem ele a
            # imagem entra a 25 q/s e o fps=30 do fim descarta 1 quadro por foto (medido: 169 em vez de 170).
            cmd += ["-framerate", "30"]
        cmd += ["-i", str(ROOT / "public" / p["src"])]
        clone = p.get("clone", 0)  # 1º quadro repetido no início (clipe que começa depois de t=0, ver lead())
        pad = f"tpad=start={clone}:start_mode=clone," if clone else ""
        # setpts DEPOIS do tpad: com o tempo zerado antes, o quadro repetido nascia com PTS negativo e o fps o descartava
        gr = grade_filter(p.get("lado", "quente"))
        mov = photo_filter(p, push) if foto else zoom_filter(p, drift)
        fonte = (f"[{k}:v]tpad=stop={L}:stop_mode=clone,trim=end_frame={L}," if foto else
                 f"[{k}:v]trim=start_frame={p['src_frame']}:end_frame={p['src_frame'] + L - clone},{pad}")
        # 16/10/2026 FILME TREMIDO (tanques es): a foto entra com timebase 1/25 e o setpts=N/30/TB arredondava os
        # tempos — no quadro ~122 de TODA foto o ffmpeg pulava 1 quadro e repetia o seguinte (soluço a cada corte).
        # settb=1/30 antes do setpts deixa o tempo exato (medido: 0 congelados em 3 fotos x 499 quadros).
        parts.append(f"{fonte}settb=1/30,setpts=N,{mov},{gr + ',' if gr else ''}setsar=1[v{k}]")
    graph = ";".join(parts) + ";" + "".join(f"[v{k}]" for k in range(len(parts))) + \
        f"concat=n={len(parts)}:v=1:a=0,fps=30,tpad=stop=3:stop_mode=clone,format=yuvj420p[out]"  # 16/10: concat+fps perdia 1 quadro (s029 Roadster); -frames:v corta no n
    gfile = HY / f"{seg['name']}.filter.txt"
    gfile.write_text(graph, "utf-8")
    tmp = out.with_suffix(".part.mp4")
    # MODO LEVE (19/09/2026: 3 ffmpeg sem teto de threads + filtro perspective por quadro travaram o PC de 12 núcleos/16 GB):
    # cada ffmpeg fica com 4 threads de codificação. 24/09/2026: filtro de 2 -> 6 threads — medido em 20 fotos x 170
    # quadros: 51 -> 115 q/s com a CPU média do processo em ~18 % (antes 17 %), saída idêntica (SSIM 1,0000). O
    # perspective era o gargalo e fatia a imagem entre as threads; a codificação é da GPU (NVENC).
    cmd += ["-filter_complex_threads", "6", "-/filter_complex", str(gfile), "-map", "[out]", "-frames:v", str(n),
            *X264, "-threads", "4", "-an", str(tmp)]
    r = subprocess.run(cmd, capture_output=True, text=True, creationflags=LOW)
    if r.returncode != 0:
        raise RuntimeError(f"{seg['name']}: {r.stderr[-400:]}")
    got = frames(tmp)
    if got != n:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{seg['name']} com {got} quadros, esperado {n} (clipe curto demais para trimBefore+dur?)")
    tmp.replace(out)
    return f"{seg['name']} ffmpeg ok ({n} quadros)"


def main():
    t0 = time.time()
    plan = build_plan()
    if "--plan-only" in sys.argv:
        return
    # 29/09/2026: Remotion (Chrome, CPU) e ffmpeg (filtro na CPU + NVENC) rodam AO MESMO TEMPO — são trechos diferentes
    # do filme e cada um deixava metade da máquina parada (medido: Remotion 26-34 min + ffmpeg 21-25 min, em fila).
    # Memória: 3 abas + cache de 1 GB + 2 ffmpeg com 4 threads cabem nos 16 GB. "--em-fila" volta ao modo antigo.
    node = None
    if "--skip-remotion" not in sys.argv:
        log("etapa Remotion" + (" (roda sozinha)" if "--em-fila" in sys.argv else " (junto com o ffmpeg)"))
        node = subprocess.Popen(["node", str(ROOT / "scripts" / "render_ranges.mjs")], cwd=ROOT, creationflags=LOW)
        if "--em-fila" in sys.argv:
            node.wait()
    ff = [s for s in plan["segments"] if s["engine"] == "ffmpeg"]
    log(f"etapa ffmpeg: {len(ff)} lotes, {int(arg('--workers', 2))} em paralelo")
    t1 = time.time()
    with ThreadPoolExecutor(int(arg("--workers", 2))) as ex:
        for msg in ex.map(lambda s: render_ff(s, plan["videoDrift"]), ff):
            log(msg)
    log(f"ffmpeg FIM {(time.time() - t1) / 60:.1f}min")
    if node is not None:
        if node.wait() != 0:
            raise SystemExit("render_ranges.mjs falhou (ver out/hybrid/progress.txt)")
    for s in plan["segments"]:  # lote antigo gravado em 1/15360: remux sem recodificar para 1/90000 (ver X264)
        p = ROOT / s["file"]
        tb = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=time_base",
                             "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip().rstrip(",")
        if tb != "1/90000":
            fix = p.with_suffix(".tb90.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-c", "copy", "-video_track_timescale", "90000",
                            "-movflags", "+faststart", str(fix)], check=True)
            fix.replace(p)
            log(f"{s['name']} remux base de tempo {tb} -> 1/90000")
    for s in plan["segments"]:
        # até 3 leituras (o "0 quadros" do teste do CN era o ffprobe devolvendo "697," — já tratado em frames())
        want, got = s["end"] - s["start"], -1
        for k in range(3):
            got = frames(ROOT / s["file"])
            if got == want:
                break
            time.sleep(5 * (k + 1))
        if got != want:
            err = subprocess.run(["ffprobe", "-v", "error", str(ROOT / s["file"])], capture_output=True, text=True).stderr.strip()
            raise SystemExit(f"segmento incompleto: {s['name']} ({got} de {want} quadros) {err[:300]}")
    lst = HY / "list.txt"
    lst.write_text("\n".join(f"file '{(ROOT / s['file']).as_posix()}'" for s in plan["segments"]), "utf-8")
    out = ROOT / arg("--out", "out/final.mp4")
    tmp = out.with_name(out.stem + "_tmp.mp4")
    music = ROOT / "public" / "music.m4a"
    cfg = json.loads((D / "pipeline_config.json").read_text("utf-8")) if (D / "pipeline_config.json").exists() else {}
    with_music = cfg.get("music") is not False and music.exists()  # "music": false = filme sem trilha
    master = ROOT / "public" / "final_audio.m4a"   # modo ULTRA: narração + trilha + efeitos já masterizados a -14 LUFS (music_mix.py)
    # 27/09/2026 (painel): trilha ou efeitos ligados fora do ULTRA também usam o master do music_mix.py — desde que ele
    # seja DESTE filme (mais novo que a narração; o de um filme anterior pode ter ficado em public/)
    master_ok = master.exists() and master.stat().st_mtime > (ROOT / "public" / "audio.mp3").stat().st_mtime
    if master_ok and (cfg.get("modo") == "ultra" or cfg.get("music") or cfg.get("sfx")):
        log("áudio final: master ULTRA (public/final_audio.m4a, copiado sem recodificar)")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(master),
                        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
    else:
        log(f"áudio final: narração{' + trilha' if with_music else ' (sem trilha)'}")
        audio = (["-i", str(music), "-filter_complex", "[1:a][2:a]amix=inputs=2:normalize=0:duration=first[a]", "-map", "0:v:0", "-map", "[a]"]
                 if with_music else ["-map", "0:v:0", "-map", "1:a:0"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(ROOT / "public" / "audio.mp3"),
                        *audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(tmp)], check=True)
    got = frames(tmp)
    if got != plan["durationInFrames"]:
        raise SystemExit(f"junção com {got} quadros, esperado {plan['durationInFrames']} (arquivo mantido em {tmp.name})")
    # contar quadros não basta: no teste do CN os 57700 quadros estavam lá e o arquivo dizia 8032 s (tempos estragados)
    vdur = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                           "-of", "csv=p=0", str(tmp)], capture_output=True, text=True).stdout
    m = re.search(r"[\d.]+", vdur)
    want_s = plan["durationInFrames"] / 30
    if not m or abs(float(m.group(0)) - want_s) > 0.1:
        raise SystemExit(f"junção com duração de vídeo {vdur.strip()} s, esperado {want_s:.3f} s (arquivo mantido em {tmp.name})")
    tmp.replace(out)
    log(f"FIM {out.relative_to(ROOT)} ({got} quadros) total {(time.time() - t0) / 60:.1f}min")


if __name__ == "__main__":
    main()
