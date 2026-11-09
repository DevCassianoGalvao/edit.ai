"""Busca do YouTube SEM gastar extração (14/10/2026): lê a página de resultados (ytInitialData) e grava
data/yt_pool.json no mesmo formato do fetch_video.py (aplica as mesmas regras de classe).
Uso: python scripts/_yt_busca_html.py data/yt_queries_<tema>.txt"""
import json, re, sys, time, urllib.parse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_video as fv

OUT = fv.OUT


def dur(s):
    p = [int(x) for x in (s or "0").split(":") if x.isdigit()]
    t = 0
    for x in p:
        t = t * 60 + x
    return t


def busca(q):
    r = requests.get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=EgIQAQ%3D%3D",
                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"},
                     timeout=60)
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", r.text, re.S)
    if not m:
        return []
    out = []

    def walk(o):
        if isinstance(o, dict):
            v = o.get("videoRenderer")
            if v and v.get("videoId"):
                ow = (v.get("ownerText") or {}).get("runs") or [{}]
                out.append({"id": v["videoId"], "title": "".join(x.get("text", "") for x in v.get("title", {}).get("runs", [])),
                            "channel": ow[0].get("text", ""),
                            "channel_id": ow[0].get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseId"),
                            "duration": dur((v.get("lengthText") or {}).get("simpleText"))})
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(json.loads(m.group(1)))
    return out


def main():
    qs = [l.strip() for l in Path(sys.argv[1]).read_text("utf-8").splitlines() if l.strip()]
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    banned = set(json.loads(fv.BANNED.read_text("utf-8"))) if fv.BANNED.exists() else set()
    for q in qs:
        n = 0
        for j in busca(q):
            vid = j["id"]
            if vid in banned:
                continue
            title, ch, d = j["title"], j["channel"], j["duration"]
            reason = None
            if fv.BAN_TITLE.search(title):
                reason = "title:" + fv.BAN_TITLE.search(title).group(0)
            elif fv.BAN_CHANNEL.search(ch):
                reason = "channel:" + fv.BAN_CHANNEL.search(ch).group(0)
            elif not (25 <= d <= 4 * 3600):
                reason = f"duration:{d}"
            e = pool.setdefault(vid, {"id": vid, "title": title, "channel": ch, "channel_id": j["channel_id"],
                                      "duration": d, "url": f"https://www.youtube.com/watch?v={vid}", "queries": []})
            if q not in e["queries"]:
                e["queries"].append(q)
            e["class_reject"] = reason
            n += reason is None
        print(f"[yt-html] {q!r}: {n} aceitos pela regra de classe", flush=True)
        time.sleep(2.0)
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    print(f"[yt-html] pool {len(pool)}")


if __name__ == "__main__":
    main()
