"""EFEITOS E AMBIÊNCIAS POR TEMA (modo ULTRA, seção 7) -> data/sfx_pool.json + assets/sfx/

Fonte: Freesound com a faceta "Creative Commons 0" (sem crédito, uso comercial), lendo o HTML da busca porque
a API exige token. Baixa a PRÉVIA (mp3 128 kbps): para hit grave, riser, whoosh e ambiência isso é suficiente.
Cada item guarda a página do som (rastro para sfx_credits.md). BBC Sound Effects nunca (licença não comercial).
Uso: python fetch_sfx.py [N_por_termo]
"""
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "assets" / "sfx"
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
# duração por papel (s): hit curto, riser médio, ambiência longa
DUR = {"hit": "[0.5 TO 4]", "riser": "[3 TO 12]", "whoosh": "[0.3 TO 3]", "ambiencia": "[30 TO 600]", "diegetico": "[0.5 TO 20]"}


def busca(termo, dur, page=1):
    r = S.get("https://freesound.org/search/", timeout=90,
              params={"q": termo, "f": f'license:"Creative Commons 0" duration:{dur}', "page": page, "s": "score desc"})
    if r.status_code != 200:
        return []
    out = []
    for b in re.split(r'<div class="bw-search__result', r.text)[1:]:
        m_id = re.search(r'/people/([^/"]+)/sounds/(\d+)/', b)
        m_prev = re.search(r'https://cdn\.freesound\.org/previews/[^"\']+?-lq\.mp3', b)
        m_title = re.search(r'title="([^"]{3,120})"', b)
        if m_id and m_prev:
            out.append({"user": m_id.group(1), "id": m_id.group(2), "preview": m_prev.group(0),
                        "title": (m_title.group(1) if m_title else f"freesound {m_id.group(2)}")})
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    cfg = json.loads((D / "tema_config.json").read_text("utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    pool = json.loads((D / "sfx_pool.json").read_text("utf-8")) if (D / "sfx_pool.json").exists() else {}
    for papel, termos in cfg["sfx_termos"].items():
        for termo in termos:
            try:
                res = busca(termo, DUR[papel])
            except Exception as e:  # noqa: BLE001
                print("[fs erro]", termo, e); continue
            got = 0
            for x in res:
                if got >= n:
                    break
                key = f"fs_{x['id']}"
                if key in pool:
                    got += 1; continue
                dst = OUT / f"{key}.mp3"
                try:
                    rr = S.get(x["preview"], timeout=120); rr.raise_for_status()
                    dst.write_bytes(rr.content)
                except Exception as e:  # noqa: BLE001
                    print("[fs falhou]", key, e); continue
                pool[key] = {"file": str(dst.relative_to(ROOT)).replace("\\", "/"), "title": x["title"], "papel": papel,
                             "termo": termo, "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                             "page": f"https://freesound.org/people/{x['user']}/sounds/{x['id']}/", "fonte": "Freesound (CC0)"}
                got += 1
                time.sleep(0.5)
            print(f"[sfx] {papel}/{termo}: {got}")
            time.sleep(1.0)
    (D / "sfx_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    por = {}
    for v in pool.values():
        por[v["papel"]] = por.get(v["papel"], 0) + 1
    print(f"[sfx] pool {len(pool)} -> data/sfx_pool.json | {por}")


if __name__ == "__main__":
    main()
