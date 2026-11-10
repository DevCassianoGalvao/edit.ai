"""Colhe METADADOS de vídeos do Wikimedia Commons (nada é baixado aqui).

Fontes: busca `filetype:video` por consulta + categorias de vídeo.
Regra de POOL (não lista de rejeitados): licença NC/ND ou desconhecida nunca entra.
Saída: data/commons_video_pool.json  (mescla com o que já está no disco)
"""
import json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "commons_video_pool.json"
API = "https://commons.wikimedia.org/w/api.php"
UA = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
S = requests.Session()
S.headers["User-Agent"] = UA

QUERIES = [
    'container ship',
    'cargo ship',
    'container terminal',
    'gantry crane container',
    'ship engine room',
    'marine diesel engine',
    'tugboat',
    'pilot boat',
    'Suez Canal ship',
    'ship bridge navigation',
    'port of Rotterdam',
    'port of Hamburg',
    'ship deck',
    'lifeboat drill',
    'ship in heavy seas',
    'harbour crane',
    'shipyard',
    'merchant ship',
    'seafarer',
    'ship galley',
]
CATEGORIES = [
    'Category:Videos of container ships',
    'Category:Videos of ships',
    'Category:Videos of cargo ships',
    'Category:Videos of harbours',
    'Category:Videos of ports',
    'Category:Videos of cranes',
    'Category:Videos of tugboats',
    'Category:Videos of the Suez Canal',
    'Category:Videos of marine engines',
    'Category:Videos of the sea',
    'Category:Videos of waves',
    'Category:Videos of shipyards',
    'Category:Videos of container terminals',
    'Category:Videos of seafaring',
]

VIDEO_EXT = re.compile(r"\.(webm|ogv|mp4|mpg|mpeg)$", re.I)
NC_ND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
OK_LIC = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[- ]by(-sa)?[- ]\d)", re.I)


def api(params, tries=5):
    params = {**params, "format": "json", "formatversion": 2}
    for i in range(tries):
        r = S.post(API, data=params, timeout=90)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(5 * (i + 1)); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"API falhou: {params}")


def search_titles(q):
    out, off = [], 0
    while True:
        d = api({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 500,
                 "sroffset": off, "srsearch": f"{q} filetype:video"})
        out += [h["title"] for h in d["query"]["search"]]
        if "continue" not in d or len(out) >= 1500:
            return out
        off = d["continue"]["sroffset"]


def cat_titles(cat):
    out, cont = [], {}
    while True:
        d = api({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmlimit": 500,
                 "cmtype": "file", **cont})
        out += [m["title"] for m in d["query"]["categorymembers"]]
        if "continue" not in d:
            return out
        cont = d["continue"]


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def info(titles):
    d = api({"action": "query", "prop": "imageinfo", "titles": "|".join(titles),
             "iiprop": "url|size|mime|extmetadata|metadata", "iiextmetadatafilter":
             "LicenseShortName|License|Artist|Credit|ImageDescription|DateTimeOriginal|UsageTerms|Categories"})
    res = []
    for p in d["query"]["pages"]:
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            continue
        em = ii.get("extmetadata", {})
        g = lambda k: strip_html(em.get(k, {}).get("value", ""))
        meta = {m["name"]: m["value"] for m in (ii.get("metadata") or []) if isinstance(m, dict) and "name" in m}
        dur = meta.get("playtime_seconds") or meta.get("length") or ii.get("duration")
        res.append({
            "title": p["title"], "url": ii.get("url"), "descurl": ii.get("descriptionurl"),
            "width": ii.get("width"), "height": ii.get("height"), "mime": ii.get("mime"),
            "size": ii.get("size"), "duration": float(dur) if dur else None,
            "license": g("LicenseShortName"), "usage": g("UsageTerms"), "artist": g("Artist"),
            "credit": g("Credit"), "desc": g("ImageDescription")[:600], "date": g("DateTimeOriginal"),
            "categories": g("Categories"),
        })
    return res


def pool_ok(e):
    lic = f"{e['license']} {e['usage']}"
    if NC_ND.search(lic):
        return False
    return bool(OK_LIC.search(e["license"] or "")) or "public domain" in lic.lower()


def save(pool):
    """Mescla com o disco (nunca reescrever da memória) e grava."""
    if OUT.exists():
        disk = json.loads(OUT.read_text("utf-8"))
        disk.update(pool); pool = disk
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    return pool


def main():
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    hits = {}
    queries, cats = QUERIES, CATEGORIES
    if len(sys.argv) > 1:  # arquivo de consultas: uma por linha; "Category:..." = categoria
        lines = [l.strip() for l in Path(sys.argv[1]).read_text("utf-8").splitlines() if l.strip()]
        queries = [l for l in lines if not l.startswith("Category:")]
        cats = [l for l in lines if l.startswith("Category:")]
    for q in queries:
        try:
            ts = search_titles(q)
        except Exception as ex:  # noqa: BLE001
            print("ERR", q, ex); continue
        for t in ts:
            hits.setdefault(t, set()).add(q)
        print(f"[search] {q!r}: {len(ts)}", flush=True)
        time.sleep(0.5)
    for c in cats:
        try:
            ts = cat_titles(c)
        except Exception as ex:  # noqa: BLE001
            print("ERR", c, ex); continue
        for t in ts:
            hits.setdefault(t, set()).add(c)
        print(f"[cat] {c}: {len(ts)}", flush=True)
    todo = [t for t in hits if VIDEO_EXT.search(t) and t not in pool]
    print(f"[info] {len(todo)} novos títulos", flush=True)
    for i in range(0, len(todo), 50):
        for e in info(todo[i:i + 50]):
            e["queries"] = sorted(hits.get(e["title"], []))
            e["pool_ok"] = pool_ok(e)
            pool[e["title"]] = e
        if i % 1000 == 0:
            print(f"[info] {i}/{len(todo)}", flush=True)
            save(pool)
        time.sleep(0.3)
    for t, e in pool.items():  # queries acumuladas
        e["queries"] = sorted(set(e.get("queries", [])) | hits.get(t, set()))
    pool = save(pool)
    ok = [e for e in pool.values() if e["pool_ok"]]
    hd = [e for e in ok if (e["height"] or 0) >= 1080]
    print(f"[done] total {len(pool)} | licença ok {len(ok)} | >=1080p {len(hd)}")


if __name__ == "__main__":
    sys.exit(main())
