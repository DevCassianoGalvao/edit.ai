"""07/10/2026 — RAIO-X dos canais do usuário (YouTube Data API, chave em data/youtube_api_key.txt): inscritos, nº de
vídeos e os últimos ~50 vídeos com views, duração e dias no ar. Saída: painel/pautas/raio_x_<handle>.json + resumo.
Uso: python painel/canais_raio_x.py @handle1 @handle2 ..."""
import json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
import urllib.parse, urllib.request

HERE = Path(__file__).resolve().parent
KEY = (HERE.parent / "data" / "youtube_api_key.txt").read_text("utf-8").strip()
OUT = HERE / "pautas"
OUT.mkdir(exist_ok=True)


def api(rota, **p):
    p["key"] = KEY
    url = f"https://www.googleapis.com/youtube/v3/{rota}?" + urllib.parse.urlencode(p)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def iso_dur(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def raio_x(handle):
    ch = api("channels", part="snippet,statistics,contentDetails", forHandle=handle.lstrip("@"))["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = [i["contentDetails"]["videoId"] for i in api("playlistItems", part="contentDetails", playlistId=up, maxResults=50)["items"]]
    vids = api("videos", part="snippet,statistics,contentDetails", id=",".join(ids))["items"] if ids else []
    agora = datetime.now(timezone.utc)
    lista = []
    for v in vids:
        pub = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
        lista.append({"titulo": v["snippet"]["title"], "views": int(v["statistics"].get("viewCount", 0)),
                      "min": round(iso_dur(v["contentDetails"]["duration"]) / 60, 1), "dias": (agora - pub).days,
                      "id": v["id"]})
    d = {"handle": handle, "nome": ch["snippet"]["title"], "inscritos": int(ch["statistics"].get("subscriberCount", 0)),
         "videos": int(ch["statistics"].get("videoCount", 0)), "lang": ch["snippet"].get("defaultLanguage"),
         "descricao": ch["snippet"].get("description", "")[:500], "ultimos": lista}
    (OUT / f"raio_x_{handle.lstrip('@')}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf-8")
    return d


if __name__ == "__main__":
    for h in sys.argv[1:]:
        try:
            d = raio_x(h)
        except Exception as e:  # noqa: BLE001
            print(f"== {h}: ERRO {e}"); continue
        vs = sorted(d["ultimos"], key=lambda x: -x["views"])
        med = sorted(x["views"] for x in d["ultimos"])[len(d["ultimos"]) // 2] if d["ultimos"] else 0
        print(f"== {d['nome']} ({h}) | {d['inscritos']} inscritos | {d['videos']} vídeos | mediana {med} views "
              f"(últimos {len(d['ultimos'])})")
        for x in vs[:6]:
            print(f"   {x['views']:>8} views  {x['min']:>5} min  {x['dias']:>3} d  {x['titulo'][:95]}")
        time.sleep(0.3)
