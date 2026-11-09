"""VÍDEO DO DVIDS (Departamento de Defesa dos EUA) — 04/10/2026, pedido do usuário: vídeo sem o bloqueio do YouTube.

O DVIDS é a fonte ORIGINAL do material militar que os canais repostam no YouTube (sem logo de canal, sem
apresentador, em qualidade original). Conteúdo em domínio público quase sempre; o crédito do autor é pedido
("credit" vai para o attribution.md) e não pode sugerir endosso do DoD. Item com outro status de copyright é pulado.
Serve para: forças armadas, navios, porta-aviões, aviões, guarda costeira, resgate, desastres com ajuda militar,
bases, exercícios — e também muita AMBIENTAÇÃO (mar, tempestade, helicóptero, hospital de campanha).

Chave: grátis, cadastro em https://www.dvidshub.net (o USUÁRIO faz) -> salvar em %USERPROFILE%\\.dvids_key
Entra no MESMO trilho do Pexels: data/stock_api_pool.json com chave "dv:ID" -> data/cand_dvids.json ->
probe_sheet.py data/cand_dvids.json qa/probe_dv -> eu julgo -> data/api_review.json -> source_review -> make_clips.
Só arquivo mp4 >= 1920x1080 (regra: sem fallback < 1080p).

Uso: python fetch_dvids.py data/dvids_queries_<tema>.txt [N por tag, padrão 8]
     arquivo de buscas: uma por linha, "tag: busca" (ex.: "conves: USS Gerald R. Ford flight operations")
"""
import json, re, sys, time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prioridade  # noqa: E402,F401

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
API = "https://api.dvidshub.net"
KEY = Path.home() / ".dvids_key"


def chave():
    if not KEY.exists() or not KEY.read_text("utf-8").strip():
        print("[DVIDS] sem chave configurada — etapa opcional ignorada")
        sys.exit(0)
    return KEY.read_text("utf-8").strip()


def busca(q, k, n=25):
    r = requests.get(f"{API}/search", params={"q": q, "type": "video", "hd": 1, "aspect_ratio": "16:9",
                                              "max_results": n, "sort": "score", "api_key": k}, timeout=60)
    r.raise_for_status()
    return r.json().get("results", [])


def arquivo(vid, k):
    r = requests.get(f"{API}/asset", params={"id": vid, "api_key": k}, timeout=60)
    r.raise_for_status()
    a = r.json().get("results", r.json())
    if isinstance(a, list):
        a = a[0] if a else {}
    files = [f for f in a.get("files", []) if f.get("type") == "video/mp4" and (f.get("width") or 0) >= 1920
             and (f.get("height") or 0) >= 1080]
    if not files:
        return None, a
    return min(files, key=lambda f: f.get("width") or 9999), a


def main():
    qfile = Path(sys.argv[1])
    n_tag = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    k = chave()
    linhas = [l.strip() for l in qfile.read_text("utf-8").splitlines() if l.strip() and ":" in l and not l.startswith("#")]
    pool_p = D / "stock_api_pool.json"
    pool = json.loads(pool_p.read_text("utf-8")) if pool_p.exists() else {}
    side = json.loads((D / "source_side.json").read_text("utf-8")) if (D / "source_side.json").exists() else {}
    seen = set(side)
    for p in D.glob("probe_round*.json"):
        seen |= {s["key"] for s in json.loads(p.read_text("utf-8"))}
    cand, por_tag = [], {}
    for l in linhas:
        tag, q = [x.strip() for x in l.split(":", 1)]
        try:
            res = busca(q, k)
        except requests.HTTPError as ex:
            print(f"[dvids] {q}: HTTP {ex.response.status_code}", flush=True)
            continue
        novos = 0
        for v in res:
            if por_tag.get(tag, 0) >= n_tag:
                break
            vid = v.get("id", "")
            sk = "dv:" + vid.split(":")[-1]
            if sk in seen or not (6 <= (v.get("duration") or 0) <= 900):
                continue
            if sk not in pool:
                try:
                    f, a = arquivo(vid, k)
                except requests.HTTPError:
                    continue
                time.sleep(0.3)
                cop = str(a.get("copyright") or a.get("license") or "")
                if f is None or (cop and not re.search(r"public domain|domínio público|none", cop, re.I)):
                    continue
                credit = a.get("credit") or v.get("credit") or "DVIDS"
                credit = credit if isinstance(credit, str) else ", ".join(c.get("name", "") for c in credit if isinstance(c, dict))
                if re.match(r"\s*courtesy", credit, re.I):   # 04/10: "Courtesy" = material de terceiros cedido, pode não ser domínio público
                    continue
                pool[sk] = {"site": "DVIDS", "page": v.get("url"), "desc": v.get("title"), "file": f["src"],
                            "width": f.get("width"), "height": f.get("height"), "duration": v.get("duration"),
                            "author": credit, "author_url": v.get("url"), "license": "Domínio público (DVIDS/DoD)",
                            "license_url": "https://www.dvidshub.net/about/copyright", "queries": [q]}
            seen.add(sk)
            por_tag[tag] = por_tag.get(tag, 0) + 1
            novos += 1
            e = pool[sk]
            cand.append({"key": sk, "url": e["file"], "duration": e["duration"], "tag": tag,
                         "label": f"[{tag}] DVIDS {str(e['author'])[:24]} | {(e['desc'] or '')[:70]} [{e['width']}x{e['height']}]"})
        print(f"[dvids] {tag}: '{q}' -> {novos} candidatos", flush=True)
        time.sleep(0.5)
    pool_p.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    (D / "cand_dvids.json").write_text(json.dumps(cand, ensure_ascii=False, indent=1), "utf-8")
    print(f"[dvids] {len(cand)} candidatos -> data/cand_dvids.json | próximo: python scripts/probe_sheet.py data/cand_dvids.json qa/probe_dv")


if __name__ == "__main__":
    main()
