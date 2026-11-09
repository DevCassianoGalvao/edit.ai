"""Aplica a decisão de uma rodada de revisão da folha do filme.

- REJEITADOS no corte: data/segment_rejects.json {cut_id: [clip_id, ...]}  (só aquele corte perde o clipe)
- REJEITADOS no filme: data/window_rejects.json [clip_id, ...]           (o clipe sai da biblioteca inteira)
- TODO o resto que apareceu nas folhas revisadas é TRAVADO em data/image_locks.json {cut_id: clip_id}
  (só os segmentos rejeitados voltam ao casamento; sem trava cada rejeição reembaralha o filme)
Uso: python review_apply.py decisao.json
  decisao.json = {"reviewed_from": F0, "reviewed_to": F1,           # faixa de quadros das folhas revisadas
                  "reject_cut": ["c012345", ...],                  # corte ruim NESTE ponto (clipe pode servir em outro)
                  "reject_clip": ["v1a2b3c4d", ...],               # clipe ruim em qualquer ponto
                  "notes": {"c012345": "motivo"}}
Mescla tudo com o disco (nunca reescreve da memória).
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def jload(name, default):
    p = D / name
    return json.loads(p.read_text("utf-8")) if p.exists() else default


def main():
    dec = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    items = jload("timeline.json", {"items": []})["items"]
    locks = jload("image_locks.json", {})
    srej = jload("segment_rejects.json", {})
    wrej = set(jload("window_rejects.json", []))
    f0, f1 = dec.get("reviewed_from", 0), dec.get("reviewed_to", 10 ** 9)
    rc, rk = set(dec.get("reject_cut", [])), set(dec.get("reject_clip", []))
    # regra de FONTE: se o defeito é da fonte (ex.: X-47B), rejeitar arquivo a arquivo deixa os irmãos voltarem
    lib = jload("clips.json", {"clips": []})["clips"]
    for src in dec.get("reject_source", []):
        hit = {c["id"] for c in lib if c.get("source") == src}
        if not hit:
            raise SystemExit(f"reject_source sem clipes: {src}")
        rk |= hit
    wrej |= rk
    # só trava o que APARECEU na folha revisada (jobs do clip_sheet), nunca a faixa inteira às cegas
    shown = None
    if dec.get("lock_from_jobs"):
        jobs = json.loads((ROOT / dec["lock_from_jobs"]).read_text("utf-8"))["jobs"]
        shown = {Path(j["out"]).stem for j in jobs}
    n_lock = n_rej = 0
    for it in items:
        if it["type"] != "cut" or not it.get("clip") or not (f0 <= it["from"] < f1):
            continue
        if shown is not None and it["id"] not in shown and it["id"] not in rc and it["clip"] not in rk:
            continue
        if it["id"] in rc or it["clip"] in rk:
            srej.setdefault(it["id"], [])
            if it["clip"] not in srej[it["id"]]:
                srej[it["id"]].append(it["clip"])
            locks.pop(it["id"], None)
            n_rej += 1
        else:
            locks[it["id"]] = it["clip"]
            n_lock += 1
    (D / "image_locks.json").write_text(json.dumps(locks, ensure_ascii=False, indent=1), "utf-8")
    (D / "segment_rejects.json").write_text(json.dumps(srej, ensure_ascii=False, indent=1), "utf-8")
    (D / "window_rejects.json").write_text(json.dumps(sorted(wrej), ensure_ascii=False, indent=1), "utf-8")
    log = D / "review_rounds.md"
    prev = log.read_text("utf-8") if log.exists() else "# review_rounds.md\n"
    notes = dec.get("notes", {})
    entry = [f"\n## rodada — quadros {f0}–{f1}: {n_lock} travados, {n_rej} rejeitados, {len(rk)} clipes fora do filme"]
    entry += [f"- {k}: {v}" for k, v in notes.items()]
    log.write_text(prev + "\n".join(entry) + "\n", "utf-8")
    print(f"[review] travados {n_lock} | rejeitados {n_rej} | clipes fora do filme {len(rk)} | locks total {len(locks)}")


if __name__ == "__main__":
    main()
