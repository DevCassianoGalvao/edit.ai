"""Fotos EM ALTA de navio gigante para as miniaturas do titulo
"Por Que um Navio de Aco de 200 Mil Toneladas Nao Afunda | Documentario".

O pedido do usuario: mais ENFASE NO NAVIO, e a foto nao precisa vir dos videos do filme.
Busca no Commons (licenca livre, NC/ND nunca — regra permanente), so paisagem, largura >= 2600 px,
e baixa a versao de 3200 px em APAGAR_navio-2026-09-16/fotos_thumb.
Uso: python fetch_fotos_thumb_navio.py [N_por_consulta]
"""
import json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "APAGAR_navio-2026-09-16" / "fotos_thumb"
API = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers["User-Agent"] = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"

QUERIES = [  # navio ENORME, de perto, com agua no quadro
    "Emma Maersk container ship", "Ever Given container ship", "HMM Algeciras",
    "Maersk Triple E class ship", "MSC container ship sea", "CMA CGM container ship",
    "ultra large container vessel", "container ship aerial view sea",
    "container ship bow wave", "bulbous bow container ship", "loaded container ship underway",
    "very large crude carrier underway", "capesize bulk carrier sea", "container ship tugboat harbour",
]
NC_ND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
OK_LIC = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[- ]by(-sa)?[- ]\d)", re.I)
BAD = re.compile(r"(model|miniature|lego|\btoy|diorama|painting|drawing|render|3d|\bcgi\b|diagram|"
                 r"\bmap\b|logo|poster|stamp|coat of arms|cruise|yacht|regatta|sailing)", re.I)
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    DIR.mkdir(parents=True, exist_ok=True)
    ficha, vistos = {}, set()
    for q in QUERIES:
        try:
            j = api({"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {q}",
                     "gsrnamespace": "6", "gsrlimit": str(n * 3), "prop": "imageinfo",
                     "iiprop": "url|size|extmetadata", "iiurlwidth": "3200"})
        except Exception as e:
            print("[erro]", q, e); continue
        got = 0
        for p in (j.get("query", {}) or {}).get("pages", []) or []:
            if got >= n:
                break
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = meta(em, "LicenseShortName")
            titulo = p.get("title", "")
            w, h = ii.get("width", 0), ii.get("height", 0)
            if not lic or NC_ND.search(lic) or not OK_LIC.search(lic):
                continue
            if w < 2600 or w < h * 1.3 or BAD.search(titulo):
                continue
            url = ii.get("thumburl") or ii.get("url")
            if not url or url in vistos:
                continue
            vistos.add(url)
            nome = re.sub(r"[^A-Za-z0-9_.-]+", "_", titulo.replace("File:", ""))[:70]
            nome = Path(nome).stem + ".jpg"
            dst = DIR / nome
            if not dst.exists():
                try:
                    r = S.get(url, timeout=180); r.raise_for_status()
                    dst.write_bytes(r.content)
                except Exception as e:
                    print("[falhou]", nome, e); continue
                time.sleep(0.4)
            ficha[nome] = {"consulta": q, "titulo": titulo, "licenca": lic,
                           "autor": meta(em, "Artist"), "orig_px": [w, h],
                           "pagina": ii.get("descriptionurl", "")}
            got += 1
            print(f"[ok] {nome}  {w}x{h}  {lic}")
    (DIR / "ficha.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1), "utf-8")
    print("total", len(ficha), "->", DIR)


if __name__ == "__main__":
    main()
