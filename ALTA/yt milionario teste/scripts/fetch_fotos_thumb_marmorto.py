"""Fotos EM ALTA do MAR MORTO, para as miniaturas.

Quadro de vídeo 1080p ampliado pelo recorte fica mole. Aqui a fonte é FOTO grande: Commons, largura >= 2400 px,
paisagem, licença livre (PD/CC0/CC-BY/CC-BY-SA — NC/ND nunca), baixada na versão de 3200 px.
Uso: python fetch_fotos_thumb_marmorto.py [N_por_consulta]
"""
import json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "qa" / "thumb_marmorto" / "fotos"
API = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers["User-Agent"] = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"

QUERIES = [
    "Dead Sea floating person", "Dead Sea salt formations", "Dead Sea shore salt",
    "Dead Sea aerial", "Dead Sea sinkhole", "Dead Sea mud bath", "Dead Sea salt crystals",
    "Dead Sea beach Israel", "Dead Sea Jordan shore", "salt pillar Dead Sea",
    "Dead Sea evaporation ponds", "Dead Sea sunrise", "Masada aerial", "Ein Gedi oasis",
    "Dead Sea salt island", "Dead Sea water surface", "halite crust Dead Sea",
    "Dead Sea panorama", "Dead Sea coast desert", "Dead Sea works potash",
]
NC_ND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
OK_LIC = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[- ]by(-sa)?[- ]\d)", re.I)
BAD = re.compile(r"(model|miniature|lego|\btoy|diorama|painting|drawing|engraving|render|3d|\bcgi\b|diagram|"
                 r"\bmap\b|logo|poster|stamp|coat of arms|restaurant|recipe|cooked|boiled|sushi|plate|"
                 r"aquarium|museum|specimen|illustration|chart|graph)", re.I)
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    DIR.mkdir(parents=True, exist_ok=True)
    ficha, vistos = {}, set()
    if (DIR / "ficha.json").exists():
        ficha = json.loads((DIR / "ficha.json").read_text("utf-8"))
    for q in QUERIES:
        try:
            j = api({"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {q}",
                     "gsrnamespace": "6", "gsrlimit": str(n * 3), "prop": "imageinfo",
                     "iiprop": "url|size|extmetadata", "iiurlwidth": "3200"})
        except Exception as e:  # noqa: BLE001
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
            if w < 2400 or w < h * 1.25 or BAD.search(titulo):
                continue
            url = ii.get("thumburl") or ii.get("url")
            if not url or url in vistos:
                continue
            vistos.add(url)
            nome = re.sub(r"[^A-Za-z0-9_.-]+", "_", titulo.replace("File:", ""))[:70]
            dst = DIR / (Path(nome).stem + ".jpg")
            if not dst.exists():
                try:
                    r = S.get(url, timeout=180); r.raise_for_status()
                    dst.write_bytes(r.content)
                except Exception as e:  # noqa: BLE001
                    print("[falhou]", nome, e); continue
                time.sleep(0.4)
            ficha[dst.name] = {"consulta": q, "titulo": titulo, "licenca": lic,
                               "autor": meta(em, "Artist"), "orig_px": [w, h],
                               "pagina": ii.get("descriptionurl", "")}
            got += 1
            print(f"[ok] {dst.name}  {w}x{h}  {lic}", flush=True)
    (DIR / "ficha.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1), "utf-8")
    print("total", len(ficha), "->", DIR)


if __name__ == "__main__":
    main()
