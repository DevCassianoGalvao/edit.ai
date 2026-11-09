"""Decisões da revisão de FONTES na folha de contato (probe_sheet) -> data/source_side.json
Tema: a vida a bordo de um porta-conteineres (pt).

Cada fonte aprovada lista os QUADROS da folha que prestam (0..7, posições 6%..94% da duração)
com as tags do que o quadro mostra. A janela de cada quadro é centrada nele, com comprimento
min(12, max(7, espaçamento)) s (ou "win" da fonte), sem sobrepor a anterior.
Mescla com o disco (nunca reescreve da memória).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

T = lambda *tags: list(tags)
REVIEW = {}   # tema navio: o Commons nao tem video util (so Popeye, cabo de guerra e NASA)
YT_REVIEW = {}   # tema navio: as decisoes estao em data/yt_review.json (por ID)
API_REVIEW = {  # "px:ID" | "pb:ID": {quadro: [tags]} — Pexels/Pixabay (decisões das folhas em data/api_review.json)
}
WIN = {}
ERA_OLD = set()
SUB1080 = set()  # ids do YouTube sem arquivo >=1080p
REJECT_NOTES = {"cm": "rodada 1", "yt": "rodada 1", "api": "rodada 1"}

def windows(dur, tiles, win=None):
    sp = dur * 0.88 / 7
    L = win or min(12.0, max(7.0, sp))
    out, last_end = [], -1e9
    for i in sorted(tiles):
        t = dur * (0.06 + 0.88 * i / 7)
        s, e = max(0.5, t - L / 2), min(dur - 0.5, t + L / 2)
        if s < last_end or e - s < 4.5:
            continue
        out.append([round(s, 2), round(e, 2), tiles[i]])
        last_end = e
    return out


def main():
    jl = lambda n: json.loads((D / n).read_text("utf-8")) if (D / n).exists() else {}
    cm = jl("commons_video_pool.json")
    yt = jl("yt_pool.json")  # filme sem YouTube: pool ausente
    p = D / "source_side.json"
    side = json.loads(p.read_text("utf-8")) if p.exists() else {}
    probe = []
    # só probe_roundN.json (folhas revisadas); "probe_round2_candidates.json" NÃO conta
    for rp in sorted(p for p in D.glob("probe_round*.json") if p.stem[len("probe_round"):].isdigit()):
        probe += json.loads(rp.read_text("utf-8"))
    for s in probe:  # tudo que foi sondado e não aprovado = reject (não volta a ser sondado)
        side.setdefault(s["key"], {"verdict": "reject", "note": REJECT_NOTES["cm" if s["key"].startswith("cm:") else "api" if s["key"].startswith(("px:", "pb:", "dv:")) else "yt"]})
    if (D / "cm_review.json").exists():  # decisões das folhas qa/probe1 (Commons) gravadas por índice
        for k, t in json.loads((D / "cm_review.json").read_text("utf-8")).items():
            REVIEW.setdefault(k, {int(q): v for q, v in t.items()})
    for key, tiles in list(REVIEW.items()):
        if key[3:] not in cm:  # rótulo da folha trunca o título: resolver pelo prefixo, exigindo resultado único
            base = key[3:].removesuffix(".webm")
            hits = [t for t in cm if t.startswith(base)]
            if len(hits) != 1:
                raise SystemExit(f"Commons ambíguo/ausente: {key} -> {len(hits)}")
            del REVIEW[key]
            key = "cm:" + hits[0]
            REVIEW[key] = tiles
        e = cm[key[3:]]
        tags = sorted({t for v in tiles.values() for t in v})
        side[key] = {"verdict": "ok", "tags": tags, "windows": windows(e["duration"], tiles), "round": 1,
                     "era": "old" if key in ERA_OLD else "modern"}
        cropj = json.loads((D / "cm_crop.json").read_text("utf-8")) if (D / "cm_crop.json").exists() else {}
        if key in cropj:  # telemetria queimada nas bordas (ROV Victor 6000): recorte w:h:x:y antes da escala
            side[key]["crop"] = cropj[key]
    if (D / "yt_review.json").exists():  # decisões das folhas qa/probe_yt gravadas por chave ("yt:ID": {quadro: [tags]})
        for k, t in json.loads((D / "yt_review.json").read_text("utf-8")).items():
            e = yt.get(k[3:]) if isinstance(yt, dict) else None
            if e is None:
                raise SystemExit(f"YT ausente do pool: {k}")
            tiles = {int(q): v for q, v in t.items()}
            tags = sorted({x for v in tiles.values() for x in v})
            side[k] = {"verdict": "ok", "tags": tags, "windows": windows(float(e["duration"]), tiles, WIN.get(k)), "round": 2,
                       "era": "old" if k in ERA_OLD else "modern"}
    for (ch, title), tiles in YT_REVIEW.items():
        hits = [e for e in yt.values() if e["channel"] == ch and e["title"].startswith(title)]
        if len(hits) > 1:  # mesmo canal e prefixo: vale o vídeo que estava na folha revisada
            probed = {s["key"] for s in probe}
            hits = [e for e in hits if f"yt:{e['id']}" in probed]
        if len(hits) != 1:
            raise SystemExit(f"YT ambíguo/ausente: {ch} {title} -> {len(hits)}")
        e = hits[0]
        key = f"yt:{e['id']}"
        tags = sorted({t for v in tiles.values() for t in v})
        side[key] = {"verdict": "ok", "tags": tags, "windows": windows(e["duration"], tiles, WIN.get((ch, title))), "round": 1,
                     "era": "old" if key in ERA_OLD else "modern"}
    api = json.loads((D / "stock_api_pool.json").read_text("utf-8")) if (D / "stock_api_pool.json").exists() else {}
    if (D / "api_review.json").exists():  # decisões das folhas qa/probe4 (quadro como texto no JSON)
        for k, t in json.loads((D / "api_review.json").read_text("utf-8")).items():
            API_REVIEW.setdefault(k, {int(q): v for q, v in t.items()})
    for key, tiles in API_REVIEW.items():  # Pexels/Pixabay (liberados pelo usuário)
        e = api[key]
        tags = sorted({t for v in tiles.values() for t in v})
        side[key] = {"verdict": "ok", "tags": tags, "windows": windows(float(e["duration"]), tiles), "round": 4, "era": "modern"}
    # janelas extras escolhidas nas folhas densas (qa/dense, 16 quadros com segundo impresso) de fontes JÁ aprovadas
    xp = D / "extra_windows.json"  # {key: [[inicio_s, fim_s, [tags]], ...]}
    for key, wins in (json.loads(xp.read_text("utf-8")) if xp.exists() else {}).items():
        if side.get(key, {}).get("verdict") != "ok":
            continue
        cur = side[key]["windows"]
        for s, e, tags in wins:
            if all(e <= a or s >= b for a, b, *_ in cur):  # nunca sobrepor janela existente
                cur.append([s, e, tags])
        cur.sort(key=lambda w: w[0])
        side[key]["tags"] = sorted({t for w in cur for t in (w[2] if len(w) > 2 else side[key]["tags"])})
        side[key]["max"] = max(side[key].get("max", 12), len(cur))
    for vid in SUB1080:
        side[f"yt:{vid}"] = {"verdict": "reject", "note": "sem formato mp4 >=1080p (slice_dl)"}
    p.write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    ok = [k for k, v in side.items() if v["verdict"] == "ok"]
    nw = sum(len(side[k]["windows"]) for k in ok)
    print(f"fontes ok {len(ok)} (cm {sum(k.startswith('cm:') for k in ok)}, yt {sum(k.startswith('yt:') for k in ok)}), janelas {nw}")


if __name__ == "__main__":
    main()
