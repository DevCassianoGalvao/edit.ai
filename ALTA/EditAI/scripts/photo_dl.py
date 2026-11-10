"""Baixa em PARALELO (pausa curta, recua no 429) as fotos do data/photo_pool.json.
Mesmo nome de arquivo do fetch_images/fetch_images_cat. Mescla com o disco ao gravar.
(19/09/2026: o download em fila do fetch_images levava ~1 foto a cada 10 s — 725 fotos = 2 h.)

24/09/2026 — MINIATURA PRIMEIRO. Baixar 2.200 fotos em resolução cheia (7,5 GB, ~45 min) para aprovar 400 e usar
~180 era o passo mais lento do filme. Agora são dois modos:
  --miniaturas   500 px -> assets/thumbs/ (campo "thumb_file"); é o que o prefilter e a folha de contato usam.
                 SÓ ATÉ A COTA de cada tag (demanda.py): max(18, 3 x cota) candidatas por tag (25/09: era 4x/24;
                 a cota já desconta o que o banco serviu — tag coberta pelo banco não baixa nada), na ordem de
                 relevância da busca, sem os títulos da lista de rejeição (photo_sheet.REJ_GLOBAL + beats.json).
                 --mais tag1,tag2 dobra o limite dessas tags; --todas baixa o pool inteiro.
  MEDIDO em 24/09/2026: o gargalo do Commons é o NÚMERO de pedidos (429 com Retry-After ~11 s quando a
  miniatura não está no cache deles), não o tamanho — ~52 fotos/min tanto em 500 px quanto em 3840 px. Por isso
  o ganho de tempo vem de pedir MENOS fotos (a cota), e o 429 respeita o Retry-After em vez de esperar 20-120 s.
  --aprovadas    resolução cheia SÓ do que a folha aprovou (data/photo_side.json verdict ok) -> assets/photos/.
                 É o que o make_photos, o banco e as miniaturas do YouTube usam.
Sem flag: comportamento antigo (resolução cheia de tudo que falta).

Uso: python photo_dl.py [--miniaturas | --aprovadas]
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
D, DIR, MINI = ROOT / "data", ROOT / "assets" / "photos", ROOT / "assets" / "thumbs"
OUT = D / "photo_pool.json"
S = requests.Session()
S.headers["User-Agent"] = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
pool = json.loads(OUT.read_text("utf-8"))
MODO = "mini" if "--miniaturas" in sys.argv else "aprovadas" if "--aprovadas" in sys.argv else "cheia"
CAMPO = "thumb_file" if MODO == "mini" else "file"
PASTA = MINI if MODO == "mini" else DIR
PASTA.mkdir(parents=True, exist_ok=True)


def mini_url(u, w=500):
    """URL da miniatura de w px no Commons. 500 é um dos tamanhos padrão (20/40/60/120/250/330/500/960/1280...)
    — tamanho fora da lista pode ser recusado. Vale para a URL original e para a de miniatura (/thumb/.../NNNpx-)."""
    u = u.split("?")[0]
    if "/thumb/" in u:
        return re.sub(r"/\d+px-([^/]+)$", rf"/{w}px-\1", u)
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/([^/]+)$", u)
    if not m:
        return u
    base, h, name = m.groups()
    ext = name.rsplit(".", 1)[-1].lower()
    suf = ".jpg" if ext in ("tif", "tiff") else ".png" if ext in ("svg", "xcf") else ""
    return f"{base}/thumb/{h}/{name}/{w}px-{name}{suf}"


def dst_of(t):
    """24/09/2026: o nome era só o ASCII do título — título em cirílico/grego/chinês virava "_02.JPG" e 71 fotos
    do filme de Yakutsk dividiam o MESMO arquivo (a folha mostrava a foto de outro título). Agora leva um trecho
    do md5 do título: único por título."""
    import hashlib
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", t[5:])[:90]
    stem, ext = (base.rsplit(".", 1) + [""])[:2] if "." in base else (base, "")
    ext = "." + ext.lower() if ext.lower() in ("jpg", "jpeg", "png") else ".jpg"
    return PASTA / f"{stem}_{hashlib.md5(t.encode()).hexdigest()[:6]}{ext}"


def one(t):
    e = pool[t]
    d = dst_of(t)
    if d.exists():
        e[CAMPO] = str(d)
        return "já"
    url = (e.get("mini_url") or mini_url(e["url"])) if MODO == "mini" else e["url"]   # mini_url: Pexels/Pixabay
    for k in range(6):
        try:
            r = S.get(url, timeout=120)
        except requests.RequestException:
            time.sleep(10 * (k + 1))
            continue
        if r.status_code == 429:
            ra = r.headers.get("retry-after")
            time.sleep((float(ra) + 1) if ra and ra.replace(".", "").isdigit() else 5 * (k + 1))
            continue
        if r.ok and r.content.lstrip()[:1] == b"<":   # 08/10/2026: URL de página (não de imagem) -> HTML; não grava
            return "html"
        if r.ok:
            d.write_bytes(r.content)
            e[CAMPO] = str(d)
            time.sleep(0.05 if MODO == "mini" else 0.1)
            return "ok"
        return f"http {r.status_code}"
    return "falhou"


def alvo():
    if MODO == "aprovadas":
        side = json.loads((D / "photo_side.json").read_text("utf-8"))
        ok = [t for t, s in side.items() if s.get("verdict") == "ok" and t in pool]
        return [t for t in ok if not pool[t].get("file") or not Path(pool[t]["file"]).exists()]
    faltam = [t for t, e in pool.items() if not e.get(CAMPO) or not Path(e[CAMPO]).exists()]
    if MODO == "mini" and "--api" in sys.argv:   # só as do Pexels/Pixabay (fetch_photos_api), sem cota: CDN sem 429
        return [t for t in faltam if pool[t].get("mini_url")]
    if MODO != "mini" or "--todas" in sys.argv or not (D / "beats.json").exists():
        return faltam
    sys.path.insert(0, str(ROOT / "scripts"))
    import math
    from demanda import cotas
    from photo_sheet import REJ_GLOBAL
    q = cotas()
    rej = re.compile("|".join([REJ_GLOBAL] + json.loads((D / "beats.json").read_text("utf-8")).get("rejeita_titulo", [])), re.I)
    mais = set(sys.argv[sys.argv.index("--mais") + 1].split(",")) if "--mais" in sys.argv else set()
    lim_p = D / "photo_dl_limite.json"
    lim = json.loads(lim_p.read_text("utf-8")) if lim_p.exists() else {}
    por_tag = {}
    for t, e in pool.items():            # ordem do pool = ordem de relevância de cada busca
        if not rej.search(t):
            por_tag.setdefault(e["tags"][0], []).append(t)
    escolhidas = []
    for tag, ts in por_tag.items():
        base = max(18, math.ceil(3 * q[tag])) if q.get(tag, 0) > 0 else 0   # 25/09: 3x (era 4x/24)
        lim[tag] = max(lim.get(tag, base), base) * (2 if tag in mais else 1)
        escolhidas += ts[:lim[tag]]
    lim_p.write_text(json.dumps(lim, indent=1), "utf-8")
    ja = set(escolhidas)
    print(f"[photo_dl] cota: {len(ja)} de {len(pool)} candidatas ({len(por_tag)} tags; "
          f"{sum(1 for t in pool if rej.search(t))} fora pelo título)", flush=True)
    return [t for t in faltam if t in ja]


todo = alvo()
workers = int(os.environ.get("PDL_WORKERS", "4"))
print(f"[photo_dl] modo {MODO}: {len(todo)} para baixar ({workers} conexões)", flush=True)
n, falhas, trava = 0, [], threading.Lock()
with ThreadPoolExecutor(workers) as ex:
    for t, res in zip(todo, ex.map(one, todo)):
        n += 1
        if res not in ("ok", "já"):
            falhas.append((t, res))
        if n % (200 if MODO == "mini" else 50) == 0:
            print(f"[photo_dl] {n}/{len(todo)}", flush=True)
disk = json.loads(OUT.read_text("utf-8"))
for t, e in pool.items():
    if e.get(CAMPO):
        disk.setdefault(t, e)[CAMPO] = e[CAMPO]
OUT.write_text(json.dumps(disk, ensure_ascii=False, indent=1), "utf-8")
com = sum(1 for e in disk.values() if e.get(CAMPO) and Path(e[CAMPO]).exists())
print(f"[photo_dl] fim ({MODO}): {com}/{len(disk)} com arquivo | {len(falhas)} falhas"
      + (f" — ex.: {falhas[0][1]} {falhas[0][0][5:60]}" if falhas else ""), flush=True)
