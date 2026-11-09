"""Baixa arquivos de vídeo do Commons em FILA (upload.wikimedia.org devolve 429 em paralelo).

Uso: python fetch_commons_video.py sources.json   (usa as entradas com key "cm:...")
Grava em assets/commons/<nome seguro> e mescla data/commons_files.json {title: path}.
"""
import hashlib, json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "assets" / "commons"
IDX = ROOT / "data" / "commons_files.json"
UA = "YTMilionarioPipeline/1.0 (seu-email@exemplo.com)"
MAX_BYTES = 600 * 1024 * 1024


def safe(title):
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", title[5:])[:90]
    return f"{hashlib.md5(title.encode()).hexdigest()[:8]}_{stem}"


def transcode_1080(url):
    """https://upload.wikimedia.org/wikipedia/commons/a/ab/Nome.webm ->
    https://upload.wikimedia.org/wikipedia/commons/transcoded/a/ab/Nome.webm/Nome.webm.1080p.vp9.webm"""
    base = url.split("?")[0]
    marker = "/wikipedia/commons/"
    if marker not in base or "/transcoded/" in base:
        return None
    head, tail = base.split(marker, 1)
    name = tail.rsplit("/", 1)[-1]
    return f"{head}{marker}transcoded/{tail}/{name}.1080p.vp9.webm"


def load():
    return json.loads(IDX.read_text("utf-8")) if IDX.exists() else {}


def save_entry(title, path):
    idx = load()  # mescla com o disco, nunca da memória
    idx[title] = path
    IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=1), "utf-8")


def fetch(title, url):
    out = DIR / safe(title)
    if out.exists() and out.stat().st_size > 0:
        return out
    tmp = out.with_suffix(out.suffix + ".part")
    for attempt in range(6):
        try:
            with requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=120) as r:
                if r.status_code == 429:
                    wait = int(r.headers.get("Retry-After", 0) or 0) or 20 * (attempt + 1)
                    print(f"[429] esperando {wait}s", flush=True)
                    time.sleep(wait); continue
                r.raise_for_status()
                if int(r.headers.get("Content-Length", 0)) > MAX_BYTES:
                    # original grande demais (4K): usar a transcodificação 1080p do próprio Commons
                    alt = transcode_1080(url)
                    if alt and alt != url:
                        print(f"[1080p] original grande, usando transcode: {title[:70]}", flush=True)
                        url = alt
                        continue
                    print(f"[skip] grande demais: {title}"); return None
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
            tmp.replace(out)
            return out
        except requests.RequestException as ex:
            print(f"[erro] {title}: {ex}", flush=True)
            time.sleep(10 * (attempt + 1))
    return None


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    srcs = [s for s in json.loads(Path(sys.argv[1]).read_text("utf-8")) if s["key"].startswith("cm:")]
    idx = load()
    for i, s in enumerate(srcs):
        title = s["key"][3:]
        if title in idx and Path(idx[title]).exists():
            continue
        t0 = time.time()
        p = fetch(title, s["url"])
        if p:
            save_entry(title, str(p))
            print(f"[{i + 1}/{len(srcs)}] {p.stat().st_size / 1e6:.0f} MB {time.time() - t0:.0f}s {title[:70]}", flush=True)
        time.sleep(2.0)


if __name__ == "__main__":
    main()
