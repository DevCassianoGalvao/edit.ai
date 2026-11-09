"""Decisões da revisão das FOLHAS DE FOTOS (qa/photos) -> data/photo_side.json — tema vivir en Noruega.

Índice = número "#N" impresso na folha (qa/photos/index.json liga N -> título do arquivo).
Só entram fotos que MOSTRAM o que o beat pede (câmara hiperbárica, sino, mergulhador comercial/militar,
SEALAB/época, pesca de caranguejo, exame médico), sem texto/cerimônia/recreativo. Tudo que apareceu nas
folhas revisadas e não foi aprovado vira "reject". Mescla com o disco.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

T = lambda *tags: list(tags)
APPROVE = {  # n: [tags]
}
REVIEWED_RANGES = []  # [(n0, n1), ...] faixas de índice exibidas nas folhas revisadas
ERA_OLD = set()  # índices de fotos de época
NOTES = "rodada 1"


def main():
    index = {int(k): v for k, v in json.loads((ROOT / "qa/photos/index.json").read_text("utf-8")).items()}
    p = D / "photo_side.json"
    side = json.loads(p.read_text("utf-8")) if p.exists() else {}
    ap = D / "photo_approve.json"  # decisões por índice gravadas fora do código (várias rodadas de folhas)
    if ap.exists():
        j = json.loads(ap.read_text("utf-8"))
        for k, v in j.get("approve", {}).items():
            APPROVE.setdefault(int(k), v)
        REVIEWED_RANGES.extend(tuple(r) for r in j.get("ranges", []))
        ERA_OLD.update(j.get("era_old", []))
    for a, b in REVIEWED_RANGES:
        for n in range(a, b + 1):
            t = index.get(n)
            if t and t not in side:
                side[t] = {"verdict": "reject", "note": NOTES}
    for n, tags in APPROVE.items():
        if side.get(index[n], {}).get("note") == "painel":   # 27/09: decisão feita no painel (painel/) vale mais
            continue
        side[index[n]] ={"verdict": "ok", "tags": tags, "sheet_index": n, "era": "old" if n in ERA_OLD else "modern"}
    p.write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    ok = [v for v in side.values() if v["verdict"] == "ok"]
    from collections import Counter
    print(f"[fotos] aprovadas {len(ok)} | por tag {dict(Counter(v['tags'][0] for v in ok))}")


if __name__ == "__main__":
    main()
