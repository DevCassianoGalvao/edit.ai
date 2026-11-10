"""Busca imagens em fontes indexadas pelo Openverse e integra ao pool de fotos da baia.

Uso: python scripts/busca_openverse.py data/buscas_openverse.json
O JSON é um objeto {"tag": ["consulta", ...]}; as tags vêm de beats.json.
A ferramenta apenas cadastra candidatos: o fluxo de seleção existente decide o uso.
"""
import hashlib
import ipaddress
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
POOL = DATA / "photo_pool.json"
API = "https://api.openverse.org/v1/images/"
LICENCAS = {"cc0", "pdm", "by", "by-sa"}


def http_url(valor):
    try:
        u = urlsplit(valor or "")
        host = (u.hostname or "").lower().rstrip(".")
        if u.scheme not in ("http", "https") or not host or u.username or u.password:
            return False
        if host == "localhost" or host.endswith((".localhost", ".local")):
            return False
        try:
            return ipaddress.ip_address(host).is_global
        except ValueError:
            return True
    except ValueError:
        return False


def procurar(queries, pool, sessao=requests):
    adicionadas, erros = 0, []
    for tag, termos in queries.items():
        if not isinstance(tag, str) or not isinstance(termos, list):
            continue
        for termo in termos[:3]:
            if not isinstance(termo, str) or not termo.strip():
                continue
            try:
                r = sessao.get(API, params={"q": termo[:200], "page_size": 20,
                    "license": "cc0,pdm,by,by-sa", "aspect_ratio": "wide"},
                    headers={"User-Agent": "EditAI/1.0 (local media research)"}, timeout=25)
                r.raise_for_status()
                resultados = r.json().get("results", [])
            except (requests.RequestException, ValueError, KeyError) as exc:
                erros.append(f"{tag}: {str(exc)[:120]}")
                continue
            for item in resultados:
                if not isinstance(item, dict) or item.get("license") not in LICENCAS:
                    continue
                url, mini, pagina = item.get("url"), item.get("thumbnail"), item.get("foreign_landing_url")
                if not http_url(url) or not http_url(pagina):
                    continue
                if mini and not http_url(mini):
                    mini = None
                try:
                    largura, altura = int(item.get("width") or 0), int(item.get("height") or 0)
                except (TypeError, ValueError):
                    continue
                if largura < 960 or altura <= 0 or largura / altura < 1.3:
                    continue
                ident = str(item.get("id") or "")
                if not ident or len(ident) > 80:
                    continue
                titulo = str(item.get("title") or termo).replace("\n", " ")[:100]
                chave = f"File:Openverse {ident} {titulo}.jpg"
                if chave in pool:
                    tags = pool[chave].setdefault("tags", [])
                    if tag not in tags:
                        tags.append(tag)
                    continue
                pool[chave] = {"title": chave, "tags": [tag], "query": termo, "url": url,
                    "mini_url": mini or url, "descurl": pagina, "width": largura, "height": altura,
                    "license": item.get("license_url") or item["license"],
                    "artist": item.get("creator") or "", "credit": item.get("attribution") or "",
                    "source": "Openverse", "source_page": pagina}
                adicionadas += 1
    return adicionadas, erros


def procurar_google(queries, pool, chave, sessao=requests, limite=6):
    """Pesquisa Google Imagens por SerpAPI quando há chave configurada (máximo seis consultas)."""
    adicionadas, erros, feitas = 0, [], 0
    if not chave:
        return adicionadas, erros
    for tag, termos in queries.items():
        if not isinstance(tag, str) or not isinstance(termos, list):
            continue
        for termo in termos[:3]:
            if feitas >= limite:
                return adicionadas, erros
            if not isinstance(termo, str) or not termo.strip():
                continue
            feitas += 1
            try:
                resposta = sessao.get("https://serpapi.com/search.json", params={
                    "engine": "google_images", "q": termo[:200], "api_key": chave,
                    "safe": "active"}, timeout=30)
                resposta.raise_for_status()
                dados = resposta.json()
                if dados.get("error"):
                    erros.append(f"{tag}: serviço recusou a busca; confira a chave e a cota")
                    continue
            except (requests.RequestException, ValueError):
                # Nunca mostrar a URL da requisição: ela contém a chave.
                erros.append(f"{tag}: busca indisponível; confira a conexão, chave e cota")
                continue
            for item in dados.get("images_results", [])[:30]:
                if not isinstance(item, dict) or item.get("unsafe"):
                    continue
                url, pagina, mini = item.get("original"), item.get("link"), item.get("thumbnail")
                if not http_url(url) or not http_url(pagina):
                    continue
                try:
                    largura = int(item.get("original_width") or 0)
                    altura = int(item.get("original_height") or 0)
                except (ValueError, TypeError):
                    continue
                if largura < 960 or altura <= 0 or largura / altura < 1.3:
                    continue
                ident = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
                titulo = str(item.get("title") or termo).replace("\n", " ")[:100]
                nome = f"File:Web {ident} {titulo}.jpg"
                if nome in pool:
                    tags = pool[nome].setdefault("tags", [])
                    if tag not in tags:
                        tags.append(tag)
                    continue
                pool[nome] = {"title": nome, "tags": [tag], "query": termo, "url": url,
                    "mini_url": mini if http_url(mini) else url, "descurl": pagina,
                    "width": largura, "height": altura, "license": "Não informada — conferir origem",
                    "artist": "", "credit": item.get("source") or "", "source": "Google Imagens / SerpAPI",
                    "source_page": pagina, "license_url": item.get("license_details_url") or ""}
                adicionadas += 1
    return adicionadas, erros


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/busca_openverse.py data/buscas_openverse.json")
    queries = json.loads(Path(sys.argv[1]).read_text("utf-8"))
    if not isinstance(queries, dict):
        raise SystemExit("O arquivo de buscas deve conter um objeto de tags e listas de consultas.")
    DATA.mkdir(parents=True, exist_ok=True)
    pool = json.loads(POOL.read_text("utf-8")) if POOL.exists() else {}
    novas, erros = procurar(queries, pool)
    alta = ROOT.parent.parent if ROOT.parent.name.lower() == "baias" else ROOT.parent
    chave_path = alta / "chaves" / "serpapi.txt"
    try:
        chave = chave_path.read_text("utf-8-sig").strip()
    except OSError:
        chave = ""
    web_novas, web_erros = procurar_google(queries, pool, chave)
    erros += web_erros
    tmp = POOL.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    tmp.replace(POOL)
    print(f"[busca visual] Openverse: {novas}; Google Imagens: {web_novas}; falhas: {len(erros)}")
    for erro in erros:
        print("[Openverse]", erro)


if __name__ == "__main__":
    main()
