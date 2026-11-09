# -*- coding: utf-8 -*-
"""Colhe os 20% de VIDEO do filme: banco publico primeiro, YouTube depois.

    py scripts/fetch_video.py                 todas as partes com `video` no plano
    py scripts/fetch_video.py --partes 3,17   so estas
    py scripts/fetch_video.py --por-parte 2   quantos clipes por parte (padrao 1)

Ordem, como manda o prompt: Wikimedia Commons e NASA primeiro (licenca limpa,
download direto, sem bloqueio); YouTube so para o que os bancos nao tem, e
sempre em TRECHO (youtube.baixar_trecho corta no servidor, nunca baixa o video
inteiro). Cada clipe vai para downloads/video/ e entra em
data/video_manifest.json com parte, fonte, canal, URL, trecho e licenca - e
esse manifesto e o que permite contestar uma reivindicacao de Content ID.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
import bancos  # noqa: E402
import youtube  # noqa: E402

DEST = os.path.join(AQUI, "downloads", "video")
MANIFESTO = os.path.join(AQUI, "data", "video_manifest.json")
REJEITOS = os.path.join(AQUI, "data", "video_rejects.json")
SEGUNDOS = 10          # tamanho do trecho baixado; a montagem usa 6 a 8 s
ALTURA_BANCO = 480     # cinejornal de arquivo e baixo de origem; upscale e normal
ALTURA_YT = 700        # do YouTube exige-se material moderno de verdade

ap = argparse.ArgumentParser()
ap.add_argument("--partes", default="")
ap.add_argument("--por-parte", type=int, default=1, dest="por_parte")
ap.add_argument("--so-banco", action="store_true", dest="so_banco",
                help="nao usa o YouTube (quando ele comeca a bloquear)")
args = ap.parse_args()

plano = json.load(open(os.path.join(AQUI, "plano.json"), encoding="utf-8"))
so = {int(x) for x in args.partes.split(",") if x.strip()}
os.makedirs(DEST, exist_ok=True)
os.makedirs(os.path.dirname(MANIFESTO), exist_ok=True)

# manifesto e rejeicoes MESCLAM com o disco, nunca reescrevem da memoria
manifesto = json.load(open(MANIFESTO, encoding="utf-8")) if os.path.exists(MANIFESTO) else {"clipes": []}
rejeitados = set()
if os.path.exists(REJEITOS):
    rejeitados = {x.get("url") for x in json.load(open(REJEITOS, encoding="utf-8")).get("itens", [])}
ja_no_manifesto = {c["arquivo"] for c in manifesto["clipes"]}
urls_usadas = {c.get("url") for c in manifesto["clipes"]}


def slug(txt, n=42):
    t = re.sub(r"[^\w\- ]+", "_", str(txt or "clip"))
    return re.sub(r"[\s_]+", "_", t).strip("_")[:n] or "clip"


def probe(caminho):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height:format=duration",
                        "-of", "default=nw=1:nk=1", caminho], capture_output=True, text=True)
    vals = [v.strip() for v in (r.stdout or "").splitlines() if v.strip()]
    try:
        return int(vals[0]), int(vals[1]), float(vals[2])
    except Exception:
        return 0, 0, 0.0


def baixar_banco(item, destino):
    req = urllib.request.Request(item["videoUrl"], headers={"User-Agent": bancos.UA_WIKI})
    with urllib.request.urlopen(req, timeout=120) as r, open(destino, "wb") as f:
        while True:
            pedaco = r.read(1 << 16)
            if not pedaco:
                break
            f.write(pedaco)
    return destino


novos, falhas = [], []
for parte in plano["partes"]:
    n = parte["n"]
    consultas = parte.get("video") or []
    if not consultas or (so and n not in so):
        continue
    quantos = int(parte.get("video_n") or args.por_parte)
    ja = sum(1 for c in manifesto["clipes"] if c["parte"] == n)
    if ja >= quantos:
        continue

    for q in consultas:
        if sum(1 for c in manifesto["clipes"] if c["parte"] == n) >= quantos:
            break
        print(" parte %02d  banco  | %s" % (n, q), flush=True)
        achados = []
        try:
            achados = bancos.wikimedia_videos(q, 6)
        except Exception as e:
            print("   ! commons falhou: %s" % str(e)[:80])
        for it in achados:
            if it["videoUrl"] in urls_usadas or it["videoUrl"] in rejeitados:
                continue
            ext = os.path.splitext(it["videoUrl"].split("?")[0])[1].lower() or ".webm"
            nome = "p%02d_%s%s" % (n, slug(it["title"]), ext)
            caminho = os.path.join(DEST, nome)
            try:
                baixar_banco(it, caminho)
            except Exception as e:
                print("   ! download: %s" % str(e)[:80])
                continue
            w, h, dur = probe(caminho)
            if h < ALTURA_BANCO or dur < 3:
                os.remove(caminho)
                print("   - descartado (%dx%d, %.1fs)" % (w, h, dur))
                continue
            manifesto["clipes"].append({
                "parte": n, "arquivo": os.path.relpath(caminho, AQUI).replace("\\", "/"),
                "fonte": it["source"], "canal": "", "url": it["videoUrl"],
                "titulo": it["title"], "inicio": 0, "segundos": round(dur, 1),
                "largura": w, "altura": h, "licenca": "Wikimedia Commons (ver pagina do arquivo)",
                "busca": q})
            urls_usadas.add(it["videoUrl"])
            novos.append(caminho)
            print("   + banco: %s (%dx%d, %.1fs)" % (nome, w, h, dur))
            break

    if args.so_banco:
        continue
    for q in consultas:
        if sum(1 for c in manifesto["clipes"] if c["parte"] == n) >= quantos:
            break
        print(" parte %02d  youtube| %s" % (n, q), flush=True)
        try:
            achados = youtube.buscar(q, num=6, minimo=12, maximo=1800)
        except Exception as e:
            print("   ! busca falhou: %s" % str(e)[:90])
            continue
        if achados.get("erro"):
            print("   ! %s" % achados["erro"][:120])
        for v in achados.get("videos", []):
            if v["videoUrl"] in urls_usadas or v["videoUrl"] in rejeitados:
                continue
            nome = "p%02d_%s" % (n, slug(v["title"], 36))
            r = youtube.baixar_trecho(v["ytId"], DEST, nome, inicio=v.get("inicio"),
                                      segundos=SEGUNDOS, duracao_fonte=v.get("duration") or 0)
            if not r.get("ok"):
                print("   - %s" % str(r.get("message"))[:110])
                if r.get("bloqueio"):
                    falhas.append("bloqueio do YouTube na parte %02d" % n)
                continue
            if (r.get("height") or 0) < ALTURA_YT:
                os.remove(r["path"])
                print("   - baixa resolucao (%sp)" % r.get("height"))
                continue
            manifesto["clipes"].append({
                "parte": n, "arquivo": os.path.relpath(r["path"], AQUI).replace("\\", "/"),
                "fonte": "youtube.com", "canal": v.get("channel", ""), "url": v["videoUrl"],
                "titulo": v.get("title", ""), "inicio": r.get("inicio"), "segundos": r.get("duration"),
                "largura": r.get("width"), "altura": r.get("height"),
                "licenca": "YouTube - trecho curto, mudo, uso justo (contestar com canal+URL)",
                "busca": q})
            urls_usadas.add(v["videoUrl"])
            novos.append(r["path"])
            print("   + youtube: %s (%sx%s, %.1fs) canal=%s"
                  % (os.path.basename(r["path"]), r.get("width"), r.get("height"),
                     r.get("duration") or 0, v.get("channel", "")[:30]))
            time.sleep(1.0)     # educacao com o servidor
            break

json.dump(manifesto, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total = len(manifesto["clipes"])
segundos = sum(min(float(c.get("segundos") or 0), 8) for c in manifesto["clipes"])
print("")
print("clipes novos: %d | no manifesto: %d | ~%.0f s de video (%.0f%% de um filme de %.0f min)"
      % (len(novos), total, segundos, 0, 0) if False else
      "clipes novos: %d | no manifesto: %d | ~%.0f s de video utilizavel" % (len(novos), total, segundos))
por_fonte = {}
for c in manifesto["clipes"]:
    por_fonte[c["fonte"]] = por_fonte.get(c["fonte"], 0) + 1
print("por fonte:", por_fonte)
if falhas:
    print("AVISOS:", sorted(set(falhas))[:5])
