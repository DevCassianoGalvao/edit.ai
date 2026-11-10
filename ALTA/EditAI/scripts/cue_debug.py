"""Diagnóstico de cues: para cada animação, onde cada cue é dito no PARÁGRAFO e se cai na janela.
Também lista palavras vizinhas para cues não encontrados (grafia do Whisper)."""
import importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.argv = ["build_plan"]  # não executar o plano: só importar CUES/norm/cue_hit
src = (ROOT / "scripts" / "build_plan.py").read_text("utf-8")
ns = {"__file__": str(ROOT / "scripts" / "build_plan.py")}
exec(src.split("def jload")[0], ns)  # cabeçalho: imports, constantes, CUES, norm, cue_hit
norm, cue_hit, CUES, FPS = ns["norm"], ns["cue_hit"], ns["CUES"], ns["FPS"]

tr = json.loads((ROOT / "data/master_transcript.json").read_text("utf-8"))
beats = json.loads((ROOT / "data/beats.json").read_text("utf-8"))["beats"]
items = json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"]
words = [dict(w, f=round(w["s"] * FPS)) for s in tr["sentences"] for w in s["words"]]
anim = {it["scene"]: it for it in items if it["type"] == "animation"}
for b in beats:
    if not b["anim"]:
        continue
    p = tr["paragraphs"][b["para"]]
    it = anim[b["anim"]]
    a, z = p["startFrame"], p["endFrame"]
    ws = [w for w in words if a <= w["f"] < z]
    print(f"\n{b['anim']}  parágrafo {a / 30:.1f}–{z / 30:.1f}s ({(z - a) / 30:.1f}s)  janela {it['from'] / 30:.1f}–{(it['from'] + it['dur']) / 30:.1f}s")
    hits = ns["seq_hits"](CUES[b["anim"]], ws)
    for spec in CUES[b["anim"]]:
        hit = hits.get(spec)
        if hit:
            off = (hit["f"] - it["from"]) / 30
            inside = 0 <= hit["f"] - it["from"] < it["dur"]
            print(f"   {spec:28s} dito em {hit['f'] / 30:7.1f}s  (janela {off:+5.1f}s) {'OK' if inside else 'FORA DA JANELA'}")
        else:
            key = norm(spec.split("|")[0])[:4]
            near = sorted({w["w"] for w in ws if key[:3] and norm(w["w"]).startswith(key[:3])})
            print(f"   {spec:28s} NÃO ENCONTRADO no parágrafo; parecidas: {near[:8]}")
