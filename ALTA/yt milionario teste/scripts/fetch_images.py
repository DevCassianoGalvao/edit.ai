"""FOTOS do Commons — tema: os tres golpes do agro brasileiro (pt).

Regras de pool: licença PD/CC0/CC-BY/CC-BY-SA (NC/ND nunca), paisagem (largura >= 1.3x altura),
largura >= 1600 px, título sem cerimônia/recreativo/ficção. Baixa em FILA (429 em paralelo)
a versão de 2400 px e grava data/photo_pool.json (mescla com o disco).
Uso: python fetch_images.py [N_por_consulta]
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
UA = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
S = requests.Session()
S.headers["User-Agent"] = UA

QUERIES = {  # 06/11/2026 pescadores de lagosta do Ceará (pt, baia b1)
    "icapui": ["Icapuí", "Icapuí Ceará", "Icapuí praia", "Icapuí falésias", "Icapuí litoral"],
    "redonda": ["Praia de Redonda", "Redonda Icapuí", "Redonda Ceará barcos", "Praia da Redonda Icapuí"],
    "falesia": ["falésias Ceará", "Canoa Quebrada falésias", "Morro Branco falésias", "falésia Icapuí"],
    "praia": ["praia Ceará coqueiros", "praia Ceará barcos de pesca", "Aracati praia", "litoral leste Ceará"],
    "jangada": ["jangada", "jangada Ceará", "jangadeiros", "jangada Mucuripe"],
    "barco_pesca": ["barco de pesca Ceará", "barco lagosteiro", "barco pesca artesanal Nordeste", "fishing boat Ceará"],
    "pescador": ["pescador Ceará", "pescador artesanal Nordeste", "pescadores Ceará praia", "fisherman Ceará Brazil"],
    "vila": ["vila de pescadores Ceará", "comunidade pesqueira Ceará", "fishing village Ceará"],
    "lagosta": ["Panulirus argus", "Caribbean spiny lobster", "Panulirus laevicauda", "spiny lobster reef"],
    "lagosta_pescada": ["lagosta pescada", "lobster tails", "spiny lobster catch", "lagostas mercado"],
    "manzua": ["covo lagosta", "lobster trap wooden", "manzuá", "lobster pots boat"],
    "mergulho": ["hookah diving", "surface supplied diving hose", "diver air hose underwater", "mergulhador pesca"],
    "mangueira": ["diving hose boat", "air hose coiled deck", "hookah diving hose boat"],
    "compressor": ["belt driven air compressor", "air compressor engine", "hookah compressor"],
    "botijao": ["botijão de gás", "LPG cylinder Brazil", "gas cylinders LPG", "botijões de gás"],
    "motor": ["fishing boat diesel engine", "boat engine room small", "motor de barco"],
    "fundo": ["rocky reef underwater", "reef crevice", "Fernando de Noronha underwater reef", "underwater rocks Brazil"],
    "marambaia": ["artificial reef tires", "artificial reef underwater scrap", "artificial reef drums", "recife artificial"],
    "sucata": ["metal drums scrap", "pile of tires", "scrap metal yard", "crushed barrels"],
    "bolhas": ["underwater bubbles", "air bubbles water", "soda bubbles bottle"],
    "camara": ["hyperbaric chamber", "recompression chamber", "hyperbaric oxygen therapy", "decompression chamber navy"],
    "hospital": ["hospital emergency room Brazil", "Hospital Naval de Natal", "intensive care unit bed", "hospital corridor"],
    "cadeira": ["wheelchair", "man in wheelchair", "spinal cord injury rehabilitation", "physiotherapy rehabilitation"],
    "medula": ["spine MRI", "spine X-ray", "spinal cord anatomy"],
    "mar": ["mar Ceará", "sea Ceará", "mar verde Nordeste", "Atlantic ocean waves Brazil"],
    "amanhecer": ["amanhecer praia Ceará", "sunrise fishing boats Brazil", "nascer do sol mar barcos"],
    "fortaleza": ["Fortaleza Ceará", "Mucuripe", "Fortaleza beira-mar", "Fortaleza skyline"],
    "natal": ["Natal Rio Grande do Norte", "Natal RN", "Base Naval de Natal", "Ponte Newton Navarro"],
    "rn_costa": ["Rio do Fogo", "São Miguel do Gostoso", "Rio do Fogo Rio Grande do Norte", "litoral Rio Grande do Norte"],
    "ibama": ["Ibama fiscalização", "Ibama apreensão", "Ibama agentes", "Ibama pesca ilegal"],
    "policia": ["Polícia Federal operação", "Polícia Federal agentes", "Polícia Federal viatura"],
    "marinha": ["Marinha do Brasil navio patrulha", "Marinha do Brasil", "Brazilian Navy patrol vessel", "Grupamento de Patrulha Naval do Nordeste"],
    "guerra": ["Tartu destroyer", "Guerra da Lagosta", "French destroyer T 47", "contratorpedeiro Pará Marinha", "Fletcher class Brazil"],
    "aviao": ["P-15 Neptune FAB", "B-17 FAB", "Lockheed Neptune Brazil", "FAB 1960"],
    "lancha": ["lancha mar", "speedboat sea", "patrol boat fast"],
    "fogo": ["boat fire", "barco pegando fogo", "burning boat"],
    "multidao": ["multidão praia Nordeste", "crowd beach Brazil"],
    "defeso": ["barcos parados praia", "barcos de pesca ancorados Ceará", "fishing boats beach Brazil"],
    "restaurante": ["lagosta grelhada", "grilled lobster plate", "lagosta prato restaurante"],
    "fabrica": ["seafood processing plant", "frozen lobster tails packing", "fish processing workers"],
    "porto": ["Porto do Pecém", "Porto do Mucuripe", "reefer containers port"],
    "dinheiro": ["notas de real", "dinheiro reais"],
    "turismo": ["Canoa Quebrada", "Ponta Grossa Icapuí", "turistas praia Ceará"],
    "roca": ["roça sertão", "plantação de milho Nordeste", "agricultura familiar Ceará"],
    "familia": ["família de pescadores", "criança escola Nordeste", "escola rural Ceará"],
    "eua": ["lobster restaurant New York", "lobster dinner restaurant"],
    "documento": ["Diário Oficial da União", "decree document stamp"],
}





NC_ND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
OK_LIC = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[- ]by(-sa)?[- ]\d)", re.I)
BAD = re.compile(r"(scale model|miniature|\blego\b|diecast|model kit|\btoys?\b|diorama|render|3d model|\bcgi\b|"
                 r"clip ?art|infographic|\bchart\b|world map|\blogo\b|poster|coat of arms|flag of|"
                 r"cartoon|comic|caricature|painting|drawing of|illustration|"
                 r"video ?game|gameplay|simulator|"
                 r"boxing|punch|martial|"
                 r"\bzoo\b|wedding|protest|carnival|football|soccer|toy car|model car|matchbox|diecast|police)", re.I)
strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()


def meta(em, key):
    """extmetadata devolve {"campo": {"value": ...}} na maioria dos arquivos, mas às vezes o BLOCO INTEIRO
    (ou o campo) vem como LISTA — 15/09 quebrou a coleta na tag damage_control."""
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    DIR.mkdir(parents=True, exist_ok=True)
    save = lambda: OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    for tag, qs in QUERIES.items():
        got = 0
        for q in qs:
            try:
                d = api({"action": "query", "generator": "search", "gsrnamespace": 6, "gsrlimit": n,
                         "gsrsearch": f"{q} filetype:bitmap", "prop": "imageinfo", "iiprop": "url|size|extmetadata",
                         "iiurlwidth": 2400, "iiextmetadatafilter": "LicenseShortName|UsageTerms|Artist|Credit|ImageDescription|DateTimeOriginal"})
            except RuntimeError:   # 27/10: Commons 503 intermitente -> pula a busca em vez de derrubar a coleta
                print(f"[erro] busca '{q}' API falhou", flush=True); continue
            for p in (d.get("query") or {}).get("pages", []):
                t = p["title"]
                ii = (p.get("imageinfo") or [None])[0]
                if not ii or t in pool:
                    if t in pool and tag not in pool[t]["tags"]:
                        pool[t]["tags"].append(tag)
                    continue
                em = ii.get("extmetadata", {})
                lic = meta(em, "LicenseShortName")
                desc = meta(em, "ImageDescription")
                w, h = ii.get("width", 0), ii.get("height", 0)
                if NC_ND.search(lic + " " + meta(em, "UsageTerms")) or not OK_LIC.search(lic):
                    continue
                if w < 1600 or w < 1.3 * h:
                    continue
                if BAD.search(t):
                    continue
                pool[t] = {"title": t, "tags": [tag], "query": q, "url": ii.get("thumburl") or ii["url"],
                           "descurl": ii.get("descriptionurl"), "width": w, "height": h, "license": lic,
                           "artist": meta(em, "Artist"), "credit": meta(em, "Credit"),
                           "desc": desc[:400], "date": meta(em, "DateTimeOriginal")}
                got += 1
            time.sleep(0.5)
        print(f"[fotos] {tag}: +{got}", flush=True)
        save()  # grava a cada tag: erro no meio da coleta não joga fora o que já veio
    save()  # metadados gravados ANTES dos downloads (queda de conexão não perde o pool)
    if "--sem-download" in sys.argv:  # downloads ficam para o photo_dl.py (paralelo)
        print(f"[fotos] pool {len(pool)} (sem download)", flush=True)
        return
    for i, (t, e) in enumerate(pool.items()):  # downloads em fila
        dst = DIR / (re.sub(r"[^A-Za-z0-9._-]+", "_", t[5:])[:100])
        if dst.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            dst = dst.with_suffix(".jpg")
        if dst.exists():
            e["file"] = str(dst); continue
        for k in range(5):
            try:
                r = S.get(e["url"], timeout=120)
            except requests.RequestException:  # conexão resetada pelo servidor: espera e tenta de novo
                time.sleep(20 * (k + 1)); continue
            if r.status_code == 429:
                time.sleep(15 * (k + 1)); continue
            if r.ok:
                dst.write_bytes(r.content); e["file"] = str(dst)
            break
        if i % 25 == 0:
            save()
        time.sleep(1.0)
    if OUT.exists():  # mescla com o disco
        disk = json.loads(OUT.read_text("utf-8"))
        disk.update(pool); pool = disk
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    from collections import Counter
    c = Counter(t for e in pool.values() if e.get("file") for t in e["tags"])
    print("[fotos] baixadas por tag:", dict(c))


if __name__ == "__main__":
    main()
