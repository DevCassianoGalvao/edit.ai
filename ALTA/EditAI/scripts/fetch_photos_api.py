"""FOTOS do Pexels e do Pixabay pelas APIs oficiais (chaves liberadas pelo usuário em 13/09/2026) -> photo_pool.

25/09/2026 (filme dos piratas): o Commons quase não tem tripulação MERCANTE, arame farpado em navio, família de
marinheiro, ponte de comando por dentro — só US Navy e navio-museu. O banco livre tem essas cenas. Entra no MESMO
fluxo: miniatura (campo mini_url) -> juízes -> conferência -> photo_dl --aprovadas.
Licenças: Pexels License / Pixabay Content License (uso comercial, sem atribuição obrigatória; registramos autor).
Chaves: %USERPROFILE%\\.pexels_key e .pixabay_key (nunca impressas nem gravadas).

Uso: python fetch_photos_api.py [N_por_busca]   (QUERIES abaixo, por tema)
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = D / "photo_pool.json"
HOME = Path.home()
N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20

QUERIES = {
  "training": [
    "military soldier training"
  ],
  "radio": [
    "military radio"
  ]
}





def chave(nome):
    p = HOME / nome
    return p.read_text("utf-8").strip() if p.exists() else None


def pexels(q, k):
    r = requests.get("https://api.pexels.com/v1/search", headers={"Authorization": k},
                     params={"query": q, "per_page": N, "orientation": "landscape"}, timeout=30)
    r.raise_for_status()
    for ph in r.json().get("photos", []):
        if ph["width"] < 1600 or ph["width"] < 1.3 * ph["height"]:
            continue
        alt = (ph.get("alt") or q).strip()[:80]
        yield f"File:Pexels {ph['id']} {alt}.jpg", {
            "url": ph["src"]["original"], "mini_url": ph["src"]["medium"], "descurl": ph["url"],
            "width": ph["width"], "height": ph["height"], "license": "Pexels License",
            "artist": ph.get("photographer"), "credit": f"{ph.get('photographer')} / Pexels"}


def pixabay(q, k):
    r = requests.get("https://pixabay.com/api/", params={"key": k, "q": q, "per_page": max(3, N), "image_type": "photo",
                     "orientation": "horizontal", "min_width": 1600, "safesearch": "true"}, timeout=30)
    r.raise_for_status()
    for h in r.json().get("hits", []):
        if h["imageWidth"] < 1.3 * h["imageHeight"]:
            continue
        yield f"File:Pixabay {h['id']} {h.get('tags', q)[:80]}.jpg", {
            "url": h["largeImageURL"], "mini_url": h["webformatURL"], "descurl": h["pageURL"],
            "width": h["imageWidth"], "height": h["imageHeight"], "license": "Pixabay Content License",
            "artist": h.get("user"), "credit": f"{h.get('user')} / Pixabay"}


def main():
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    kp, kb = chave(".pexels_key"), chave(".pixabay_key")
    for tag, qs in QUERIES.items():
        novos = 0
        for q in qs:
            for nome, fn, k in (("pexels", pexels, kp), ("pixabay", pixabay, kb)):
                if not k:
                    continue
                try:
                    for t, e in fn(q, k):
                        if t not in pool:
                            pool[t] = {"title": t, "tags": [tag], "query": q, **e}
                            novos += 1
                except requests.RequestException as ex:
                    print(f"[api] {nome} '{q}': {str(ex)[:80]}")
                time.sleep(0.4)
        print(f"[fotos-api] {tag}: +{novos}", flush=True)
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    print(f"[fotos-api] pool {len(pool)}")


if __name__ == "__main__":
    main()
