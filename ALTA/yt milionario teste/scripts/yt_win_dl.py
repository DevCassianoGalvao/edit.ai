"""Baixa SÓ AS JANELAS APROVADAS de cada vídeo do YouTube (depois da folha de sondagem).

Entrada: data/source_side.json (o que o source_review.py grava) + data/yt_pool.json
Saída: input/youtube/slices/<ID>_<inicio>.mp4 + data/yt_slices.json {"yt:ID": [{"s","e","file"}]}

Uma extração por vídeo (todas as seções na mesma chamada do yt-dlp, respeitando a cota compartilhada).
--force-keyframes-at-cuts: o trecho começa EXATAMENTE no segundo pedido (conferido: o quadro em 5 s do trecho
300-315 é igual ao quadro em 0 s do trecho 305-320). Sem isso o corte nasceria no keyframe anterior e todos os
tempos do make_clips sairiam deslocados.

Uso: python yt_win_dl.py [--margem 1.0]
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, subprocess, sys, time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_quota

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "input" / "youtube" / "slices"
MAX_PER_SOURCE = 12   # mesmo teto do make_clips
FMT = ("bestvideo[height=1080][vcodec^=avc1][ext=mp4]/bestvideo[height=1080][ext=mp4]/bestvideo[height=1080]/"
       "best[height=1080][vcodec^=avc1][ext=mp4]/best[height=1080]/"   # 25/09/2026: cliente web_safari entrega
       "bestvideo[height=720][vcodec^=avc1][ext=mp4]/bestvideo[height=720]/best[height=720]")  # 1080p só em HLS muxado


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def janelas(sd, dur):
    wins, kept = sorted(sd.get("windows", []), key=lambda w: w[0]), []
    for w in wins:
        if kept and w[0] < kept[-1][1]:
            continue
        if dur and float(w[1]) > 0.90 * dur:  # últimos 10% = cartão final/logo (mesma regra do make_clips)
            continue
        kept.append(w)
    return kept[: sd.get("max", MAX_PER_SOURCE)]


def main():
    margem = arg("--margem", 1.0)
    side = json.loads((D / "source_side.json").read_text("utf-8"))
    pool = json.loads((D / "yt_pool.json").read_text("utf-8")) if (D / "yt_pool.json").exists() else {}
    slices = json.loads((D / "yt_slices.json").read_text("utf-8")) if (D / "yt_slices.json").exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    fontes = [(k, sd) for k, sd in side.items() if k.startswith("yt:") and sd.get("verdict") == "ok"]
    baixados = 0
    trava = threading.Lock()   # 21/09: 2 downloads em paralelo — a espera de 45 s da cota continua serializando
                               # as EXTRAÇÕES (yt_quota._locked é lock de arquivo); o que passa a andar junto é o
                               # download de um vídeo com a espera do outro.

    def uma(par):
        nonlocal baixados
        n, (key, sd) = par
        vid = key[3:]
        dur = (pool.get(vid) or {}).get("duration") or 0
        wins = janelas(sd, dur)
        faltam = [w for w in wins if not any(abs(x["s"] - float(w[0])) < 0.01 for x in slices.get(key, []))]
        if not faltam:
            print(f"[{n}/{len(fontes)}] {vid} já tem as {len(wins)} janelas", flush=True)
            return
        secoes = []
        for w in faltam:
            s, e = max(0.0, float(w[0]) - margem), float(w[1]) + margem
            secoes += ["--download-sections", f"*{s:.2f}-{e:.2f}"]
        info = D / "yt_info" / f"{vid}.json"
        base = ["--no-playlist", "--no-progress", "--no-warnings", "--force-keyframes-at-cuts", *secoes,
                "-f", FMT, "--no-part", "-o", str(OUT / f"{vid}_%(section_start)d.%(ext)s")]
        r = None
        if info.exists() and time.time() - info.stat().st_mtime < 5 * 3600:   # URL do stream vale ~6 h
            # sem extração: usa o JSON da sonda (não conta na cota — o YouTube só vê o download dos bytes)
            r = subprocess.run(yt_quota.ytdlp(*base, "--load-info-json", str(info)),
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode != 0:
                print(f"[{n}/{len(fontes)}] {vid}: JSON da sonda não serviu ({(r.stderr.strip().splitlines() or ['?'])[-1][:80]}) — extrai de novo", flush=True)
                r = None
            else:
                time.sleep(4)
        if r is None:
            try:
                yt_quota.acquire(vid)
            except yt_quota.SemOrcamento as e:   # 06/11: sem cota = pula esta fonte e segue as outras
                print(f"[{n}/{len(fontes)}] {vid}: pulado ({str(e)[:60]})", flush=True)
                return
            r = subprocess.run(yt_quota.ytdlp(*base, f"https://www.youtube.com/watch?v={vid}"),
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            yt_quota.report(r.stdout + r.stderr)
        except yt_quota.Blocked as e:
            print(f"[PARADO] {e}", flush=True)
            return
        with trava:
            feitos = slices.setdefault(key, [])
        for w in faltam:
            s = max(0.0, float(w[0]) - margem)
            f = OUT / f"{vid}_{int(s)}.mp4"
            if not f.exists():
                print(f"[{n}/{len(fontes)}] {vid} janela {w[0]:.0f}s NÃO veio", flush=True)
                continue
            with trava:
                feitos.append({"s": float(w[0]), "e": float(w[1]), "file": str(f.relative_to(ROOT)).replace("\\", "/"),
                               "offset": round(float(w[0]) - s, 3)})
                baixados += 1
        with trava:
            (D / "yt_slices.json").write_text(json.dumps(slices, ensure_ascii=False, indent=1), "utf-8")
        print(f"[{n}/{len(fontes)}] {vid}: {len(faltam)} janela(s) baixada(s)", flush=True)

    with ThreadPoolExecutor(2) as ex:
        list(ex.map(uma, enumerate(fontes, 1)))
    (D / "yt_slices.json").write_text(json.dumps(slices, ensure_ascii=False, indent=1), "utf-8")
    mb = sum(f.stat().st_size for f in OUT.glob("*.mp4")) / 1048576
    print(f"[janelas] {baixados} novas | {len(list(OUT.glob('*.mp4')))} arquivos, {mb:.0f} MB em input/youtube/slices", flush=True)


if __name__ == "__main__":
    main()
