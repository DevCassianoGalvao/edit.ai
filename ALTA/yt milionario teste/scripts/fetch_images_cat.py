"""Fotos do Commons por CATEGORIA (precisão que a busca por texto não dá).

A busca livre por "ultralight" devolve museu e LSA europeu com matrícula no leme — e o roteiro é sobre
aeronave AMERICANA do Part 103, que por lei não tem matrícula. Categoria do modelo resolve: cada aeronave
do roteiro tem (ou não) a sua, e o que vem de lá é a máquina certa.

Regras do pool iguais às do fetch_images: licença PD/CC0/CC-BY/CC-BY-SA (NC/ND nunca), paisagem,
largura >= 1600 px. Mescla com data/photo_pool.json.
Uso: python fetch_images_cat.py
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
DIR = ROOT / "assets" / "photos"
OUT = D / "photo_pool.json"
API = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers["User-Agent"] = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"

# categoria do Commons -> tag do beat (as que não existirem são ignoradas em silêncio)
CATS = {  # 06/11/2026 pescadores de lagosta do Ceará (pt, baia b1)
    "Category:Icapuí": "icapui",
    "Category:Beaches of Icapuí": "icapui",
    "Category:Redonda (Icapuí)": "redonda",
    "Category:Ponta Grossa (Icapuí)": "turismo",
    "Category:Canoa Quebrada": "falesia",
    "Category:Morro Branco": "falesia",
    "Category:Jangadas": "jangada",
    "Category:Jangada": "jangada",
    "Category:Panulirus argus": "lagosta",
    "Category:Panulirus laevicauda": "lagosta",
    "Category:Lobster traps": "manzua",
    "Category:Hookah diving": "mergulho",
    "Category:Surface-supplied diving": "mergulho",
    "Category:Hyperbaric chambers": "camara",
    "Category:Recompression chambers": "camara",
    "Category:Hyperbaric medicine": "camara",
    "Category:LPG cylinders": "botijao",
    "Category:Gas cylinders in Brazil": "botijao",
    "Category:Artificial reefs": "marambaia",
    "Category:Fortaleza": "fortaleza",
    "Category:Mucuripe": "fortaleza",
    "Category:Natal, Rio Grande do Norte": "natal",
    "Category:Rio do Fogo": "rn_costa",
    "Category:São Miguel do Gostoso": "rn_costa",
    "Category:IBAMA": "ibama",
    "Category:Polícia Federal": "policia",
    "Category:Tartu (D636)": "guerra",
    "Category:Lobster War": "guerra",
    "Category:Fishing boats in Brazil": "barco_pesca",
    "Category:Fishermen in Brazil": "pescador",
    "Category:Aracati": "praia",
    "Category:Beaches of Ceará": "praia",
    "Category:Wheelchairs": "cadeira",
    "Category:Lockheed P-2 Neptune in Brazilian Air Force service": "aviao",
    "Category:Spiny lobsters as food": "lagosta_pescada",
}






NC_ND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
OK_LIC = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[- ]by(-sa)?[- ]\d)", re.I)
BAD = re.compile(r"(scale model|model railway|miniature|lego|diorama|render|3d model|diagram|drawing|patent|logo|poster|\bmap\b|chart|toy|model car|matchbox|"
                 r"model ship|scale model|miniature|lego|diorama|render|3d model|diagram|drawing|"
                 r"patent|logo|poster|\bmap\b|chart|shipwreck|titanic|replica|"
                 r"fishing boat|trawler|outboard|motorcycle|car engine)", re.I)
strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()


def meta(em, key):
    if isinstance(em, list):
        em = next((x for x in em if isinstance(x, dict)), {})
    if not isinstance(em, dict):
        return ""
    v = em.get(key)
    if isinstance(v, list):
        v = v[0] if v else None
    if isinstance(v, dict):
        v = v.get("value")
    return strip(v if isinstance(v, str) else None)


def api(params):
    for i in range(5):
        r = S.post(API, data={**params, "format": "json", "formatversion": 2}, timeout=90)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(5 * (i + 1)); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("API falhou")


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    save = lambda: OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    novos = 0
    for cat, tag in CATS.items():
        try:
            j = api({"action": "query", "generator": "categorymembers", "gcmtitle": cat, "gcmtype": "file",
                     "gcmlimit": "60", "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": "2400",
                     "iiextmetadatafilter": "LicenseShortName|UsageTerms|Artist|Credit|ImageDescription|DateTimeOriginal"})
        except Exception as e:  # noqa: BLE001
            print("[erro]", cat, e); continue
        pages = (j.get("query") or {}).get("pages") or []
        got = 0
        for p in pages:
            t = p.get("title", "")
            ii = (p.get("imageinfo") or [None])[0]
            if not ii:
                continue
            if t in pool:
                if tag not in pool[t]["tags"]:
                    pool[t]["tags"].append(tag)
                continue
            em = ii.get("extmetadata", {})
            lic = meta(em, "LicenseShortName")
            w, h = ii.get("width", 0), ii.get("height", 0)
            if NC_ND.search(lic + " " + meta(em, "UsageTerms")) or not OK_LIC.search(lic):
                continue
            if w < 1600 or w < 1.3 * h or BAD.search(t):
                continue
            pool[t] = {"title": t, "tags": [tag], "query": cat, "url": ii.get("thumburl") or ii["url"],
                       "descurl": ii.get("descriptionurl"), "width": w, "height": h, "license": lic,
                       "artist": meta(em, "Artist"), "credit": meta(em, "Credit"),
                       "desc": meta(em, "ImageDescription")[:400], "date": meta(em, "DateTimeOriginal")}
            got += 1; novos += 1
        print(f"[cat] {cat[9:]}: {len(pages)} arquivos, +{got}", flush=True)
        save()
        time.sleep(0.4)
    if "--sem-download" in sys.argv:  # downloads ficam para o photo_dl.py (paralelo)
        save(); print(f"[cat] +{novos} fotos novas; pool {len(pool)} (sem download)"); return
    # downloads em fila
    for i, (t, e) in enumerate(pool.items()):
        if e.get("file"):
            continue
        dst = DIR / (re.sub(r"[^A-Za-z0-9._-]+", "_", t[5:])[:100])
        if dst.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            dst = dst.with_suffix(".jpg")
        if dst.exists():
            e["file"] = str(dst); continue
        for k in range(4):
            try:
                r = S.get(e["url"], timeout=120)
            except requests.RequestException:
                time.sleep(15 * (k + 1)); continue
            if r.status_code == 429:
                time.sleep(15 * (k + 1)); continue
            if r.ok:
                dst.write_bytes(r.content); e["file"] = str(dst)
            break
        if i % 20 == 0:
            save()
        time.sleep(0.8)
    save()
    print(f"[cat] +{novos} fotos novas; pool {len(pool)}")


if __name__ == "__main__":
    main()
