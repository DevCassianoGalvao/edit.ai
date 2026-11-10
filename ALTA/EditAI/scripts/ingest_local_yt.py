"""Ingere os vídeos do YouTube baixados à mão (input/youtube) para a sondagem.

- Confere resolução (>=1080p de altura, ou largura >=1920) e duração com ffprobe.
- Garante a entrada no data/yt_pool.json (canal/título do pool; se o ID não estiver lá, canal vem do nome
  "ID__Canal.mp4" e o título é o nome do arquivo) com url https://www.youtube.com/watch?v=ID.
- Escreve OUT.json (lista de sondagem para probe_sheet) só com fontes ainda não decididas em source_side.
Uso: python ingest_local_yt.py data/probe_round2.json
"""
import json, subprocess, sys
from pathlib import Path
from local_yt import local_files, split_name

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", str(path)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    return st.get("width") or 0, st.get("height") or 0, float(j.get("format", {}).get("duration", 0) or 0)


def main():
    out = Path(sys.argv[1])
    pool_p = D / "yt_pool.json"
    pool = json.loads(pool_p.read_text("utf-8"))
    side = json.loads((D / "source_side.json").read_text("utf-8")) if (D / "source_side.json").exists() else {}
    srcs, low, unknown = [], [], []
    for p in local_files():
        vid, channel, _title = split_name(p, pool)
        if not vid:
            unknown.append(p.name)
            continue
        w, h, dur = probe(p)
        if h < 1080 and w < 1920:  # regra ≥1080p (usuário liberou 720p e voltou atrás no mesmo dia)
            low.append(f"{p.name} ({w}x{h})")
            continue
        e = pool.get(vid)
        if not e:
            manual = vid.startswith("L") and len(vid) == 11 and not any(c.isupper() for c in vid[1:])
            e = pool[vid] = {"id": vid, "channel": channel or "(canal nao informado)", "title": p.stem,
                             "url": "" if manual else f"https://www.youtube.com/watch?v={vid}",
                             "duration": dur, "manual": True}
        e["duration"] = dur  # duração real do arquivo baixado
        e.setdefault("url", "")
        key = f"yt:{vid}"
        if key in side:
            continue
        srcs.append({"key": key, "url": str(p), "duration": dur, "label": f"{e['channel']} | {e['title']} [{w}x{h}]"})
    pool_p.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    out.write_text(json.dumps(srcs, ensure_ascii=False, indent=1), "utf-8")
    print(f"[ingest] {len(srcs)} fontes novas -> {out}")
    if low:
        print("[ingest] abaixo de 720p (ignorados):", "; ".join(low))
    if unknown:
        print("[ingest] sem ID reconhecido (renomear para ID__Canal.mp4):", "; ".join(unknown))


if __name__ == "__main__":
    main()
