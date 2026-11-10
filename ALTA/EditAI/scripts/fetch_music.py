"""TRILHA POR TEMA (modo ULTRA, seção 6) -> data/music_pool.json + qa/music_sheet.md + assets/music/

Fontes desta rodada (regra de POOL: só licença explícita, NC/ND nunca):
  1. Internet Archive, API advancedsearch, mediatype:audio com licenseurl CC0 ou domínio público, buscando os
     termos de tema_config.trilha_termos. Cada item traz a URL da página e a licenseurl — é o rastro exigido.
  2. Freesound, faceta "Creative Commons 0", só sons LONGOS (>= 60 s): drones/ambiências que servem de CAMA.
     Baixa a prévia (mp3 128 kbps, suficiente para cama a −30 LUFS sob a fala). A página do som é o rastro.
Pixabay Music devolveu 403 para script neste PC (registrado no decisions_log); YouTube Audio Library só existe
dentro do Studio. Fica como reserva humana: se você baixar faixas de lá em assets/music/manual/, o music_mix
lê da mesma forma (ver ingest no fim deste arquivo).
Uso: python fetch_music.py [N_por_termo]
"""
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "assets" / "music"
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
OK_LIC = re.compile(r"(publicdomain/zero|publicdomain/mark|licenses/publicdomain|/by/|/by-sa/)", re.I)
NC_ND = re.compile(r"(by-nc|by-nd|nc-sa|nc-nd)", re.I)
MIN_S, MAX_S = 60, 900


def baixar_audio(url, destino, limite=50 * 1024 * 1024):
    """Baixa com limite de tamanho; uma falha não deixa arquivo parcial válido."""
    parcial = destino.with_suffix(destino.suffix + ".part")
    try:
        with S.get(url, timeout=(10, 30), stream=True) as resposta:
            resposta.raise_for_status()
            total = 0
            with parcial.open("wb") as f:
                for bloco in resposta.iter_content(64 * 1024):
                    total += len(bloco)
                    if total > limite:
                        raise ValueError("arquivo excede o limite de 50 MB")
                    f.write(bloco)
            if total == 0:
                raise ValueError("arquivo vazio")
        parcial.replace(destino)
    finally:
        parcial.unlink(missing_ok=True)


def ia_search(termo, rows=12):
    # Evita expressões complexas que o catálogo pode rejeitar com HTTP 200.
    palavras = re.findall(r"[^\W_]+", termo, flags=re.UNICODE)[:12]
    if not palavras:
        return []
    termos = " ".join(palavras)
    q = (f"mediatype:audio AND licenseurl:*publicdomain* AND "
         f"(title:({termos}) OR subject:({termos}))")
    r = S.get("https://archive.org/advancedsearch.php",
              params={"q": q, "fl[]": ["identifier", "title", "licenseurl", "creator"],
                      "rows": max(20, rows), "output": "json", "sort[]": "downloads desc"}, timeout=30)
    r.raise_for_status()
    result = r.json()
    if "response" not in result:
        raise RuntimeError("Internet Archive: " + str(result.get("error", "resposta inválida"))[:200])
    return result["response"].get("docs", [])


def ia_files(identifier):
    r = S.get(f"https://archive.org/metadata/{identifier}", timeout=90)
    r.raise_for_status()
    j = r.json()
    files = [f for f in j.get("files", []) if f.get("name", "").lower().endswith((".mp3", ".ogg", ".flac", ".wav"))]
    return j.get("metadata", {}), files


def freesound_search(termo, pages=2):
    """Faceta CC0 + duração longa, lendo o HTML da busca (a API exige token). Devolve (id, título, url da prévia)."""
    out = []
    for page in range(1, pages + 1):
        r = S.get("https://freesound.org/search/", timeout=90,
                  params={"q": termo, "f": 'license:"Creative Commons 0" duration:[60 TO 900]', "page": page, "s": "score desc"})
        if r.status_code != 200:
            break
        blocos = re.split(r'<div class="bw-search__result', r.text)[1:]
        for b in blocos:
            m_id = re.search(r'/people/([^/"]+)/sounds/(\d+)/', b)
            m_prev = re.search(r'https://cdn\.freesound\.org/previews/[^"\']+?-lq\.mp3', b)
            m_title = re.search(r'title="([^"]{3,120})"', b)
            if m_id and m_prev:
                out.append({"user": m_id.group(1), "id": m_id.group(2), "preview": m_prev.group(0),
                            "title": (m_title.group(1) if m_title else f"freesound {m_id.group(2)}")})
        time.sleep(1.0)
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    cfg = json.loads((D / "tema_config.json").read_text("utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    pool = json.loads((D / "music_pool.json").read_text("utf-8")) if (D / "music_pool.json").exists() else {}
    termos = cfg["trilha_termos"] + cfg.get("trilha_reserva", [])
    for termo in termos:
        # ---- Internet Archive
        try:
            docs = ia_search(termo, rows=n * 2)
        except Exception as e:  # noqa: BLE001
            print("[ia erro]", termo, e); docs = []
        got = 0
        for d in docs:
            if got >= n:
                break
            lic = d.get("licenseurl") or ""
            if not OK_LIC.search(lic) or NC_ND.search(lic):
                continue
            try:
                meta, files = ia_files(d["identifier"])
            except Exception:  # noqa: BLE001
                continue
            for f in files[:3]:
                dur = float(f.get("length") or 0) if str(f.get("length", "")).replace(".", "", 1).isdigit() else 0
                if dur and not (MIN_S <= dur <= MAX_S):
                    continue
                key = f"ia_{d['identifier']}_{re.sub(r'[^A-Za-z0-9]+', '_', f['name'])[:40]}"
                if key in pool:
                    got += 1; continue
                dst = OUT / (key + Path(f["name"]).suffix.lower())
                url = f"https://archive.org/download/{d['identifier']}/{requests.utils.quote(f['name'])}"
                try:
                    baixar_audio(url, dst)
                except Exception as e:  # noqa: BLE001
                    print("[ia falhou]", key, e); continue
                pool[key] = {"file": str(dst.relative_to(ROOT)).replace("\\", "/"), "title": f"{d.get('title')} — {f['name']}",
                             "license": lic, "page": f"https://archive.org/details/{d['identifier']}",
                             "fonte": "Internet Archive", "termo": termo, "dur_s": dur, "clima": "cama", "reserva": termo in cfg.get("trilha_reserva", [])}
                got += 1
                print(f"[ia] {termo}: {f['name'][:50]} ({dur:.0f}s) {lic}")
                break
        # ---- Freesound CC0 (drone/ambiência longa como cama)
        try:
            fs = freesound_search(termo, pages=1)
        except Exception as e:  # noqa: BLE001
            print("[fs erro]", termo, e); fs = []
        for x in fs[:n]:
            key = f"fs_{x['id']}"
            if key in pool:
                continue
            dst = OUT / f"{key}.mp3"
            try:
                baixar_audio(x["preview"], dst)
            except Exception as e:  # noqa: BLE001
                print("[fs falhou]", key, e); continue
            pool[key] = {"file": str(dst.relative_to(ROOT)).replace("\\", "/"), "title": x["title"],
                         "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                         "page": f"https://freesound.org/people/{x['user']}/sounds/{x['id']}/",
                         "fonte": "Freesound (CC0)", "termo": termo, "clima": "cama", "reserva": False}
            print(f"[fs] {termo}: {x['title'][:50]}")
            time.sleep(0.6)
    # ---- faixas colocadas à mão (YouTube Audio Library / Pixabay baixados pelo usuário)
    manual = OUT / "manual"
    if manual.exists():
        for f in sorted(manual.glob("*")):
            if f.suffix.lower() in (".mp3", ".m4a", ".wav", ".ogg", ".flac"):
                key = "manual_" + re.sub(r"[^A-Za-z0-9]+", "_", f.stem)[:40]
                pool.setdefault(key, {"file": str(f.relative_to(ROOT)).replace("\\", "/"), "title": f.stem,
                                      "license": "MANUAL — conferir na página de origem", "page": "", "fonte": "manual",
                                      "termo": "", "clima": "cama", "reserva": False})
    (D / "music_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    linhas = ["# music_sheet.md — trilha por tema (modo ULTRA)", "", f"tema: {cfg['tema']} | faixas: {len(pool)}", "",
              "| chave | título | fonte | licença | termo | reserva |", "|---|---|---|---|---|---|"]
    for k, v in pool.items():
        linhas.append(f"| {k} | {v['title'][:60]} | {v['fonte']} | {v['license']} | {v['termo']} | {'sim' if v.get('reserva') else ''} |")
    (ROOT / "qa").mkdir(exist_ok=True)
    (ROOT / "qa" / "music_sheet.md").write_text("\n".join(linhas) + "\n", "utf-8")
    print(f"[music] pool {len(pool)} faixas -> data/music_pool.json, qa/music_sheet.md")


if __name__ == "__main__":
    main()
