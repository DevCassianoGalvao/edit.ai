"""DEMANDA de fotos por tag — quantas fotos aprovadas cada tag precisa ANTES de abrir a folha de contato.

24/09/2026: no filme dos motores eu julguei ~110 folhas e aprovei 397 fotos para o filme usar 174 cortes de foto.
A folha já vem ordenada pelo CLIP (prefilter), então as primeiras folhas de cada tag são as que valem — faltava
saber ONDE parar. Esta conta dá a cota por tag; a photo_sheet --demanda só gera as folhas que a cota pede.

Conta (calibrada contra o timeline real do filme dos motores e do agro):
  segundos de foto do beat = (duração do parágrafo - animação estimada) x photo_share
  cortes de foto           = segundos / SEG_POR_CORTE
  1ª tag do beat leva PESO_TAG0, a 2ª o resto
  cota                     = ceil(cortes x MARGEM) + 2   (variedade + o que cai na folha final)

25/09/2026 — BANCO PRIMEIRO: foto servida pelo banco (banco.py servir-beats) já entra aprovada no photo_side e
é DESCONTADA da cota (bruta=True devolve a cota sem desconto). Tag coberta pelo banco: cota 0, sem download
nem folha.

Uso: python demanda.py            -> tabela no terminal
     from demanda import cotas    -> {tag: cota}
"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
SEG_POR_CORTE = 5.6   # média real: 5,6 s (motores, 80 % foto) e 5,8 s (agro, 100 % foto)
ANIM_SEG = 22.0       # animação de tela cheia fica ~20-24 s dentro do parágrafo
PESO_TAG0 = 0.65
MARGEM = 1.2


def cotas(verbose=False, bruta=False):
    beats = json.loads((D / "beats.json").read_text("utf-8"))["beats"]
    paras = json.loads((D / "master_transcript.json").read_text("utf-8"))["paragraphs"]
    cfg = json.loads((D / "pipeline_config.json").read_text("utf-8"))
    share = float(cfg.get("photo_share", 0.5))
    cortes = {}
    for b in beats:
        p = paras[b["para"]]
        seg = max(0.0, p["endSec"] - p["startSec"] - (min(ANIM_SEG, 0.7 * (p["endSec"] - p["startSec"])) if b.get("anim") else 0))
        n = seg * share / SEG_POR_CORTE
        tags = b["tags"]
        pesos = [PESO_TAG0, 1 - PESO_TAG0] if len(tags) > 1 else [1.0]
        for t, w in zip(tags, pesos):
            cortes[t] = cortes.get(t, 0.0) + n * w
    out = {t: math.ceil(c * MARGEM) + 2 for t, c in cortes.items()}
    banco = {}
    sp = D / "photo_side.json"
    if not bruta and sp.exists():
        for v in json.loads(sp.read_text("utf-8")).values():
            if v.get("verdict") == "ok" and v.get("tags"):   # banco + rodadas anteriores dos juízes
                banco[v["tags"][0]] = banco.get(v["tags"][0], 0) + 1
        out = {t: max(0, c - banco.get(t, 0)) for t, c in out.items()}
    if verbose:
        tot = sum(cortes.values())
        print(f"[demanda] photo_share {share:.2f} | ~{tot:.0f} cortes de foto | cota total {sum(out.values())}"
              + (f" | já aprovadas (banco + rodadas): {sum(banco.values())}" if banco else ""))
        for t, c in sorted(out.items(), key=lambda x: -x[1]):
            print(f"  {t:22s} ~{cortes[t]:5.1f} cortes -> cota {c}" + (f"  (já {banco[t]})" if banco.get(t) else ""))
    return out


if __name__ == "__main__":
    cotas(verbose=True)
