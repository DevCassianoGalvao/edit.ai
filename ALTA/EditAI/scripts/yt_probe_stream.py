"""SONDA o YouTube SEM BAIXAR: pega a URL direta do stream de cada vídeo e monta a lista da folha de contato.

Antes (até 20/09/2026) o pipeline baixava os 35 vídeos INTEIROS (10-15 GB, 50-70 min) para usar 2-3 janelas de
10 s de cada um. Agora: 1 extração por vídeo só para pegar metadados + URL do stream, a folha de sondagem tira os
8 quadros por faixa HTTP (probe_sheet já faz isso) e só as janelas aprovadas são baixadas (yt_win_dl.py).

Saída: data/yt_pool.json (mesclado) + OUT.json para o probe_sheet
Uso: python yt_probe_stream.py lista.txt [data/probe_round1.json]
  lista.txt = uma linha por vídeo: ID  [prioridade]  [comentário]

A URL do stream expira em algumas horas: rodar a folha logo depois (o make_clips/yt_win_dl busca de novo).
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_quota

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
MIN_H = 720        # abaixo disso não entra no filme (mesma regra do ingest_local_yt)
MIN_RATIO = 1.5    # vertical/4:3 fora (o filme é 16:9)


def escolhe(info):
    """Melhor formato só-vídeo até 1080p, avc1 na frente (decodifica rápido e é o que o ffmpeg corta melhor)."""
    fs = [f for f in info.get("formats", []) if f.get("vcodec", "none") != "none" and f.get("height")
          and f["height"] <= 1080 and f.get("url")]
    if not fs:
        return None
    fs.sort(key=lambda f: (f["height"], str(f.get("vcodec", "")).startswith("avc1"), f.get("tbr") or 0), reverse=True)
    return fs[0]


def main():
    ids = [l.split()[0] for l in Path(sys.argv[1]).read_text("utf-8").splitlines()
           if l.strip() and not l.startswith("#")]
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else D / "probe_round1.json"
    pool = json.loads((D / "yt_pool.json").read_text("utf-8")) if (D / "yt_pool.json").exists() else {}
    fora, lista = [], []
    for n, vid in enumerate(ids, 1):
        if vid in pool and pool[vid].get("stream"):
            print(f"[{n}/{len(ids)}] {vid} já sondado", flush=True)
        else:
            yt_quota.acquire(vid)
            cmd = yt_quota.ytdlp("--no-playlist", "--no-warnings", "-J", f"https://www.youtube.com/watch?v={vid}")
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            try:
                yt_quota.report(r.stdout + r.stderr)
            except yt_quota.Blocked as e:
                print(f"[PARADO] {e}", flush=True)
                break
            if r.returncode != 0 or not r.stdout.strip():
                print(f"[{n}/{len(ids)}] {vid} FALHOU: {r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else '?'}", flush=True)
                continue
            info = json.loads(r.stdout)
            # 22/09/2026: o JSON inteiro fica guardado — o yt_win_dl baixa as janelas com --load-info-json e
            # NÃO extrai de novo (era 1 extração por vídeo na sonda + 1 no download; agora é só a da sonda)
            (D / "yt_info").mkdir(exist_ok=True)
            (D / "yt_info" / f"{vid}.json").write_text(r.stdout, "utf-8")
            f = escolhe(info)
            if not f:
                print(f"[{n}/{len(ids)}] {vid} sem formato <=1080p", flush=True)
                continue
            # 24/09/2026: MESCLA com a entrada da busca (antes substituía e apagava "queries"/"class_reject")
            pool[vid] = {**pool.get(vid, {}), "id": vid, "channel": info.get("channel"), "title": info.get("title"),
                         "url": f"https://www.youtube.com/watch?v={vid}", "duration": info.get("duration"),
                         "width": f.get("width"), "height": f.get("height"), "stream": f["url"]}
            print(f"[{n}/{len(ids)}] [ok] {vid} {f.get('height')}p {info.get('duration')}s {str(info.get('title'))[:60]}", flush=True)
        e = pool[vid]
        w, h = e.get("width") or 0, e.get("height") or 0
        if h < MIN_H or (h and w / h < MIN_RATIO):
            fora.append(f"{vid} ({w}x{h})")
            continue
        lista.append({"key": f"yt:{vid}", "url": e["stream"], "duration": e.get("duration") or 0,
                      "label": f"{e.get('channel')} — {e.get('title')}"})
        (D / "yt_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    (D / "yt_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    out_path.write_text(json.dumps(lista, ensure_ascii=False, indent=1), "utf-8")
    print(f"[sonda] {len(lista)} fontes -> {out_path}" + (f" | fora do padrão: {', '.join(fora)}" if fora else ""), flush=True)


if __name__ == "__main__":
    main()
