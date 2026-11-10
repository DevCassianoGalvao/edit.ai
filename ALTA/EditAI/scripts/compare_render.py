"""Compara dois renders QUADRO A QUADRO (SSIM e PSNR por quadro) e aponta onde diferem.

Uso: python compare_render.py REF.mp4 TESTE.mp4 [--limit 0.97]
- mesmo nº de quadros e mesma duração são exigidos
- trechos contíguos com SSIM < limit são listados com o item da timeline e o motor (plan.json do render híbrido)
Saída: out/hybrid/compare.json + resumo no console.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HY = ROOT / "out" / "hybrid"


def frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    m = re.search(r"\d+", r.stdout)  # arquivo do Remotion sai "697," (vírgula no fim)
    return int(m.group(0)) if m else 0


def main():
    ref, test = Path(sys.argv[1]), Path(sys.argv[2])
    limit = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0.97
    nref, ntest = frames(ref), frames(test)
    print(f"quadros: referência {nref} | teste {ntest}")
    if nref != ntest:
        raise SystemExit("nº de quadros diferente: não dá para comparar quadro a quadro")
    HY.mkdir(parents=True, exist_ok=True)
    ssim_log, psnr_log = HY / "ssim.log", HY / "psnr.log"
    # setpts=N/30/TB: pareia os quadros pela POSIÇÃO, não pelo tempo gravado (com tempos errados o ssim do ffmpeg
    # comparava quadros trocados — 103726 linhas para 57700 quadros no teste do CN)
    graph = ("[0:v]setpts=N/30/TB,format=yuv420p,split[r1][r2];[1:v]setpts=N/30/TB,format=yuv420p,split[t1][t2];"
             f"[r1][t1]ssim=stats_file={ssim_log.relative_to(ROOT).as_posix()}[s];"
             f"[r2][t2]psnr=stats_file={psnr_log.relative_to(ROOT).as_posix()}[p]")
    gfile = HY / "compare.filter.txt"
    gfile.write_text(graph, "utf-8")
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(ref), "-i", str(test), "-/filter_complex", str(gfile),
                    "-map", "[s]", "-f", "null", "-", "-map", "[p]", "-f", "null", "-"], cwd=ROOT, check=True)
    ssim = [float(re.search(r"All:([0-9.]+)", l).group(1)) for l in ssim_log.read_text().splitlines() if "All:" in l]
    psnr = []
    for l in psnr_log.read_text().splitlines():
        m = re.search(r"psnr_avg:([0-9.]+|inf)", l)
        if m:
            psnr.append(99.0 if m.group(1) == "inf" else float(m.group(1)))
    items = json.loads((ROOT / "data" / "timeline.json").read_text("utf-8"))["items"]
    plan = json.loads((HY / "plan.json").read_text("utf-8")) if (HY / "plan.json").exists() else {"segments": []}

    def where(f):
        it = next((x for x in items if x["from"] <= f < x["from"] + x["dur"]), None)
        sg = next((s for s in plan["segments"] if s["start"] <= f < s["end"]), None)
        return (it or {}).get("id"), (sg or {}).get("engine")

    bad, f = [], 0
    while f < len(ssim):
        if ssim[f] < limit:
            g = f
            while g < len(ssim) and ssim[g] < limit:
                g += 1
            item, engine = where(f)
            bad.append({"from": f, "to": g - 1, "min_ssim": round(min(ssim[f:g]), 4), "item": item, "engine": engine})
            f = g
        else:
            f += 1
    by_engine = {}
    for i, v in enumerate(ssim):
        e = where(i)[1] if plan["segments"] else "?"
        by_engine.setdefault(e, []).append(v)
    res = {"frames": len(ssim), "ssim_avg": round(sum(ssim) / len(ssim), 5), "ssim_min": round(min(ssim), 5),
           "ssim_min_frame": ssim.index(min(ssim)), "psnr_avg": round(sum(psnr) / len(psnr), 2), "psnr_min": round(min(psnr), 2),
           "ssim_avg_by_engine": {k: round(sum(v) / len(v), 5) for k, v in by_engine.items()},
           "limit": limit, "runs_below_limit": bad}
    (HY / "compare.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), "utf-8")
    print(f"SSIM médio {res['ssim_avg']} | mínimo {res['ssim_min']} (quadro {res['ssim_min_frame']}) | "
          f"PSNR médio {res['psnr_avg']} dB | mínimo {res['psnr_min']} dB")
    print("SSIM médio por motor:", res["ssim_avg_by_engine"])
    print(f"trechos com SSIM < {limit}: {len(bad)}")
    for b in bad[:25]:
        print(f"  quadros {b['from']}–{b['to']} ({(b['to'] - b['from'] + 1)}q) min {b['min_ssim']} item {b['item']} motor {b['engine']}")


if __name__ == "__main__":
    main()
