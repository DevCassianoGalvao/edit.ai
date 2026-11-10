"""Colhe METADADOS de candidatos do YouTube (ytsearch30, flat, nada baixado).

Regras de classe (não por arquivo): jogos/simuladores, fábricas de explainer/IA,
canais de "arquivo" que carimbam o quadro, broadcasters e agências de notícia.
Saída: data/yt_pool.json (mescla com o disco).
Uso: python fetch_video.py [queries.txt]
"""
import json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "yt_pool.json"
BANNED = ROOT / "banned_videos.json"

QUERIES = [  # tema: Toyota Tundra V35A (pl)
    'Toyota Tundra 2022 driving',
    'Toyota Tundra TRD Pro review drive',
    'Toyota Tundra towing trailer',
    'Toyota Tundra 2014 5.7 V8 drive',
    'Toyota Tundra engine bay V35A',
    'twin turbo V6 engine running',
    'engine crankshaft bearing damage',
    'metal shavings in engine oil',
    'engine assembly line factory',
    'engine block machining CNC',
    'mechanic removing engine from truck',
    'pickup truck on lift service bay',
    'engine oil change pickup truck',
    'OBD scanner diagnostic car technician',
    'V8 engine running dyno',
    'turbocharger cutaway spinning',
    'pickup trucks dealership lot',
    'american highway pickup trucks driving',
]

B = chr(92) + "b"
D = chr(92) + "d"
BAN_TITLE = re.compile(
    r"(gameplay|game|dcs\b|battlefield|world of warships|simulator|modern warships|arma ?3|\bvr\b|minecraft|roblox|"
    r"nuclear option|no man'?s|trailer|reaction|react|explained|how (the|an?|do|does|navy|us|u\.s\.)|why\b|"
    r"crazy|insane|\$\d|billion|top \d+|\d+ (best|most)|vs\.?\b|ranking|documentary|podcast|interview|"
    r"news|breaking|live\b|stream|shorts|#shorts|ai generated|animation|\b3d\b(?![ -]?print)|render|cgi|lego|model kit|rc\b|"
    r"hd stock footage|stock footage|archival|ww2|wwii|world war|\(19\d\d\)|black and white|tiktok|"
    r"flight simulator|" + B + r"sim" + B + r"|minecraft|roblox|"
    r"war|missile|rocket attack|soldier|idf|hamas|hezbollah|protest|politic|"
    r"prophecy|bible study|end times|apocalypse|sermon|"
    r"how much (do|does|i)|i went|my trip|vlog " + D + r"|storytime|"
    r"recipe|cooking|salt bath home|spa treatment at home|asmr)", re.I)
BAN_CHANNEL = re.compile(
    r"(criticalpast|business insider|cnn|fox|nbc|abc news|cbs|reuters|associated press|\bap\b|bloomberg|"
    r"sky news|bbc|al jazeera|wion|guardian|telegraph|times|insider|munchies|vice|"
    r"fluctus|beyond facts|daily navy|navy media|inside navy|fleet files|wartech|yachtory|military show|"
    r"navy channel|the navy way|warship galley|not what you think|beyond explained|mega projects|"
    r"gaming|games|gamer|play|dcs|simulator|story game|brand|motors|car technology|"
    r"wavy|13news|wtkr|wvec|wtvr|virginian-pilot|news ?\d*$|tv ?\d+|usni news|navy lookout|"
    r"archive|moments \d+|patriotism|awl you need|defense updates|military news|military power|military evo|"
    r"media magik|san diego web cam|daily aviation|usa military channel|airailimages|aitelly|rudyx|aircraft class|"
    r"fortress x|us aviation|ultimate military channel|"
    r"megaprojects|storified|joe scott|3d living|crew extreme|behind the shift|simply scuba|infographics|"
    r"real engineering|wendover|half as interesting|mustard|lemmino|bright side|zack d|dark docs|fern|"
    r"mrballen|scary interesting|nexpo|the infographics show|business insider|insider business|seeker|vice|"
    r"pov: becoming|life at sea|job unknown|paid to risk|natural world facts|relaxation|scenic|national geographic|"
    r"periscopefilm|akshay suresh|henry baring|captainhowto|licet studios|crew culture)", re.I)


API_KEY_FILE = ROOT / "data" / "youtube_api_key.txt"


def _iso_dur(s):
    """PT1H2M3S -> segundos."""
    import re as _re
    m = _re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups()) if m else (0, 0, 0, 0)
    return d * 86400 + h * 3600 + mi * 60 + se


def search_api(q):
    """Busca pela YouTube Data API v3 (22/09/2026): NÃO gasta extração do yt-dlp. search.list custa 100 unidades
    e videos.list 1 — a cota gratuita de 10.000/dia dá ~95 consultas de 30 resultados por dia.
    Devolve dicionários no MESMO formato do ytsearch (id, title, channel, channel_id, duration)."""
    import requests
    key = API_KEY_FILE.read_text("utf-8").strip()
    r = requests.get("https://www.googleapis.com/youtube/v3/search", timeout=60, params={
        "part": "snippet", "q": q, "type": "video", "maxResults": 30, "videoDefinition": "high",
        "safeSearch": "none", "key": key})
    if r.status_code == 403 and "quota" in r.text.lower():
        raise RuntimeError("cota da API do YouTube esgotada hoje")
    r.raise_for_status()
    ids = [it["id"]["videoId"] for it in r.json().get("items", []) if it.get("id", {}).get("videoId")]
    if not ids:
        return
    v = requests.get("https://www.googleapis.com/youtube/v3/videos", timeout=60, params={
        "part": "snippet,contentDetails", "id": ",".join(ids), "key": key})
    v.raise_for_status()
    for it in v.json().get("items", []):
        sn = it.get("snippet", {})
        yield {"id": it["id"], "title": sn.get("title", ""), "channel": sn.get("channelTitle", ""),
               "channel_id": sn.get("channelId"), "duration": _iso_dur(it.get("contentDetails", {}).get("duration"))}


def search(q):
    if API_KEY_FILE.exists():
        try:
            yield from search_api(q)
            return
        except Exception as ex:  # noqa: BLE001 — sem API (cota do dia, chave inválida): cai no yt-dlp
            print(f"[api] {q!r}: {ex} -> yt-dlp", flush=True)
    import yt_quota
    yt_quota.acquire(f"busca {q}")  # cota compartilhada entre sessões
    p = subprocess.run(yt_quota.ytdlp(f"ytsearch30:{q}", "--flat-playlist", "--no-warnings", "-j"),
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    yt_quota.report(p.stderr)
    for line in p.stdout.splitlines():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass


def reclass():
    """Reaplica as regras de classe ao pool no disco (sem nova busca)."""
    pool = json.loads(OUT.read_text("utf-8"))
    for e in pool.values():
        t, ch, dur = e["title"], e["channel"], e["duration"] or 0
        m1, m2 = BAN_TITLE.search(t), BAN_CHANNEL.search(ch)
        e["class_reject"] = ("title:" + m1.group(0)) if m1 else ("channel:" + m2.group(0)) if m2 else \
            (None if 25 <= dur <= 4 * 3600 else f"duration:{dur}")
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    print(f"[reclass] {sum(1 for e in pool.values() if not e['class_reject'])} de {len(pool)} passam")


def main():
    if "--reclass" in sys.argv:
        return reclass()
    qs = QUERIES
    if len(sys.argv) > 1:
        qs = [l.strip() for l in Path(sys.argv[1]).read_text("utf-8").splitlines() if l.strip()]
    pool = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    banned = set(json.loads(BANNED.read_text("utf-8"))) if BANNED.exists() else set()
    import yt_quota
    done_q = {x for e in pool.values() for x in e.get("queries", [])}
    for q in qs:
        if q in done_q:  # retomada: consulta já colhida numa rodada anterior não gasta cota de novo
            print(f"[yt] '{q}': já no pool, pulando", flush=True)
            continue
        n = 0
        try:
            found = list(search(q))
        except yt_quota.Blocked as ex:  # cota cheia/pausa: grava o que já foi colhido em vez de perder a busca inteira
            print(f"[parado] {ex}", flush=True)
            break
        for j in found:
            vid = j.get("id")
            if not vid or vid in banned:
                continue
            title, ch, dur = j.get("title") or "", j.get("channel") or j.get("uploader") or "", j.get("duration") or 0
            reason = None
            if BAN_TITLE.search(title):
                reason = "title:" + BAN_TITLE.search(title).group(0)
            elif BAN_CHANNEL.search(ch):
                reason = "channel:" + BAN_CHANNEL.search(ch).group(0)
            elif not (25 <= dur <= 4 * 3600):
                reason = f"duration:{dur}"
            e = pool.setdefault(vid, {"id": vid, "title": title, "channel": ch, "channel_id": j.get("channel_id"),
                                      "duration": dur, "url": f"https://www.youtube.com/watch?v={vid}",
                                      "queries": []})
            if q not in e["queries"]:
                e["queries"].append(q)
            e["class_reject"] = reason
            n += reason is None
        print(f"[yt] {q!r}: {n} aceitos pela regra de classe", flush=True)
        time.sleep(2.0)
    if OUT.exists():  # mescla com o disco
        disk = json.loads(OUT.read_text("utf-8"))
        for k, v in pool.items():
            if k in disk:
                v["queries"] = sorted(set(v["queries"]) | set(disk[k].get("queries", [])))
            disk[k] = v
        pool = disk
    OUT.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    ok = [e for e in pool.values() if not e["class_reject"]]
    print(f"[done] {len(pool)} candidatos, {len(ok)} passam a regra de classe")


if __name__ == "__main__":
    main()
