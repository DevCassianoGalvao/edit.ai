"""PAUTAS AUTOMÁTICAS — do garimpo ao pedido na fila (07/10/2026, pedido do usuário).

Fluxo: no painel (aba Pautas) o usuário marca os canais -> o gerente abre o PESQUISADOR (prompts/pesquisa_pautas.md),
que roda o garimpo de outliers da gringa (YouTube Data API: canal pequeno, vídeo recente, views >> inscritos) e propõe
títulos adaptados a cada canal -> o usuário marca e aperta OK -> para cada pauta aprovada, o gerente abre o ROTEIRISTA
(prompts/roteirista.md), que escreve o roteiro e roda `pautas.py produzir ID` (locução DarkPlanner com a voz do canal +
pedido na fila com a configuração do filme-modelo do canal) -> os funcionários fazem o vídeo como qualquer pedido.

Estado em painel/pautas/pautas.json; canais em painel/canais.json.

  python painel/pautas.py garimpar CANAL [CANAL...] [--dias 21]   # outliers -> painel/pautas/garimpo_<canal>.json
  python painel/pautas.py propor arquivo.json                      # [{canal, titulo, titulo_pt, ideia, fonte:{...}, por_que}]
  python painel/pautas.py lista [--status proposta]
  python painel/pautas.py produzir ID                              # pautas/<ID>/roteiro.txt -> áudio -> pedido na fila
  python painel/pautas.py estado ID STATUS [--msg "..."]
  python painel/pautas.py video URL                                # dados do vídeo modelado (YouTube Data API)
  python painel/pautas.py buscar "termos" [--dias 365]             # vídeos que mais deram certo com esses termos
  python painel/pautas.py analisado ID arquivo.json                # resultado do ANALISTA (tema próprio) -> para aprovar
  python painel/pautas.py outliers MID "busca 1" "busca 2" ... [--dias 90]   # modelagem: canal pequeno + muitas views
  python painel/pautas.py modelado MID arquivo.json                # resultado do MODELADOR -> aba Modelagem

TEMA PRÓPRIO (07/10/2026, pedido do usuário): na aba Pautas, guia "Tema próprio", o usuário cola o LINK do vídeo
modelado ou um TÍTULO, escolhe canal (voz, tamanho, estilo do vídeo) e idioma e liga/desliga "título melhor" e
"clickbait leve" -> o gerente abre o ANALISTA (prompts/tema_proprio.md), que analisa e devolve o título (máx. 100
caracteres, no idioma escolhido, com tradução em português) -> o usuário dá OK -> roteirista -> voz -> fila, igual.
MODELAGEM DE VÍDEO (07/10/2026): guia "Modelagem" — o usuário manda um vídeo que deu certo (link ou título) -> o
MODELADOR (prompts/modelagem.md) disseca o modelo e o nicho e busca no YouTube vídeos do MESMO modelo com muitas views
e poucos inscritos -> lista na guia; cada um pode virar "tema próprio" com um clique.
"""
import json, math, re, shutil, sys, time
import urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PASTA = HERE / "pautas"
ARQ = PASTA / "pautas.json"
CANAIS = HERE / "canais.json"
# 22/10/2026 REGRA DO USUÁRIO: vídeo modelado só se for VIRAL de verdade — no mínimo 60 mil views e no máximo 7 dias no ar
# (a pesquisa estava propondo modelos com 700 a 22 mil views). Vale para garimpo, pesquisa automática e modelagem.
VIRAL_MIN_VIEWS = 60_000
VIRAL_MAX_DIAS = 7


def viral_ok(f):
    """(ok, motivo) da fonte/modelo: views >= VIRAL_MIN_VIEWS e dias <= VIRAL_MAX_DIAS."""
    try:
        v, d = int(f.get("views") or 0), float(f.get("dias") if f.get("dias") is not None else 999)
    except (TypeError, ValueError):
        return False, "sem views/dias do vídeo modelado"
    if v < VIRAL_MIN_VIEWS:
        return False, f"{v:,} views (mín. {VIRAL_MIN_VIEWS:,})".replace(",", ".")
    if d > VIRAL_MAX_DIAS:
        return False, f"{d:g} dias no ar (máx. {VIRAL_MAX_DIAS})"
    return True, ""


STATUS = ["analisando", "proposta", "aprovada", "roteirizando", "na_fila", "descartada", "erro"]
IDIOMAS = {"pt", "en", "es", "pl", "de", "it", "fr"}
RE_YT = re.compile(r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|live/|embed/)|youtu\.be/)([A-Za-z0-9_-]{11})")


def jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def grava(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    for i in range(20):   # Windows: "Acesso negado" se alguém está lendo naquele instante
        try:
            tmp.replace(p)
            return
        except PermissionError:
            time.sleep(0.1 + 0.05 * i)


def canais():
    return {c["id"]: c for c in jl(CANAIS, {"canais": []})["canais"]}


def dados():
    d = jl(ARQ, {})
    d.setdefault("pautas", [])
    d.setdefault("pesquisa", {})
    d.setdefault("modelagens", [])
    d.setdefault("config", {})
    return d


def agora():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


# ------------------------------------------------------------------ garimpo (YouTube Data API)
def _yt(rota, **p):
    kf = ROOT / "data" / "youtube_api_key.txt"
    if not kf.exists() or not kf.read_text("utf-8").strip():
        raise RuntimeError("falta a chave do YouTube Data API — cole na aba Chaves do painel")
    p["key"] = kf.read_text("utf-8").strip()
    url = f"https://www.googleapis.com/youtube/v3/{rota}?" + urllib.parse.urlencode(p)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def _dur(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def garimpar(cid, dias=VIRAL_MAX_DIAS, max_inscritos=200_000, min_views=VIRAL_MIN_VIEWS, min_razao=3.0):
    """Outliers da gringa para o nicho do canal: vídeo com até `dias` dias, ≥ 8 min, canal pequeno e views ≥ razão x
    inscritos. ~100 unidades da cota da API por busca (5 buscas por canal)."""
    c = canais()[cid]
    dias, min_views = min(int(dias), VIRAL_MAX_DIAS), max(int(min_views), VIRAL_MIN_VIEWS)   # 22/10: regra viral
    desde = (datetime.now(timezone.utc) - timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids, erros = [], []
    for q in c.get("buscas_en", []):
        try:
            r = _yt("search", part="id", q=q, type="video", order="viewCount", publishedAfter=desde, maxResults=25,
                    relevanceLanguage="en")
            ids += [i["id"]["videoId"] for i in r.get("items", []) if i.get("id", {}).get("videoId")]
        except Exception as e:  # noqa: BLE001
            erros.append(f"{q}: {e}")
    ids = list(dict.fromkeys(ids))
    vids = []
    for k in range(0, len(ids), 50):
        vids += _yt("videos", part="snippet,statistics,contentDetails", id=",".join(ids[k:k + 50])).get("items", [])
    chs = list({v["snippet"]["channelId"] for v in vids})
    subs = {}
    for k in range(0, len(chs), 50):
        for ch in _yt("channels", part="statistics,snippet", id=",".join(chs[k:k + 50])).get("items", []):
            subs[ch["id"]] = (int(ch["statistics"].get("subscriberCount", 0) or 0), ch["snippet"]["title"])
    agora_ = datetime.now(timezone.utc)
    out = []
    for v in vids:
        views = int(v["statistics"].get("viewCount", 0) or 0)
        minutos = _dur(v["contentDetails"]["duration"]) / 60
        s, nome = subs.get(v["snippet"]["channelId"], (0, "?"))
        dias_ar = max(1, (agora_ - datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))).days)
        razao = views / max(s, 1)
        if minutos < 8 or views < min_views or s > max_inscritos or razao < min_razao:
            continue
        out.append({"titulo": v["snippet"]["title"], "canal": nome, "inscritos": s, "views": views,
                    "dias": dias_ar, "views_dia": round(views / dias_ar), "razao": round(razao, 1),
                    "min": round(minutos, 1), "url": f"https://www.youtube.com/watch?v={v['id']}",
                    "nota": round(math.log10(views) * min(razao, 50) / math.sqrt(dias_ar), 2)})
    out.sort(key=lambda x: -x["nota"])
    res = {"canal": cid, "quando": agora(), "dias": dias, "buscas": c.get("buscas_en", []), "erros": erros,
           "candidatos": out[:15]}
    grava(PASTA / f"garimpo_{cid}.json", res)
    return res


# ------------------------------------------------------------------ pautas
def propor(itens):
    d, cs = dados(), canais()
    n0 = len(d["pautas"])
    for it in itens:
        if it.get("canal") not in cs or not (it.get("titulo") or "").strip():
            print("ignorada (canal/título):", json.dumps(it, ensure_ascii=False)[:120]); continue
        if len(it["titulo"].strip()) > 100:   # 07/10/2026: regra do usuário — máximo 100 caracteres (nunca cortar)
            print(f"RECUSADA ({len(it['titulo'].strip())} caracteres > 100): {it['titulo'][:110]}"); continue
        ok, motivo = viral_ok(it.get("fonte") or {})
        if not ok:   # 22/10/2026: regra do usuário — modelo tem de ser viral (>= 60 mil views, <= 7 dias)
            print(f"RECUSADA (modelo não viral: {motivo}): {it['titulo'][:90]}"); continue
        pid = time.strftime("%Y%m%d-%H%M%S") + f"-{len(d['pautas']):03d}"
        d["pautas"].append({"id": pid, "canal": it["canal"], "titulo": it["titulo"].strip()[:100],
                            "titulo_pt": (it.get("titulo_pt") or "")[:160], "ideia": (it.get("ideia") or "")[:600],
                            "fonte": it.get("fonte") or {}, "por_que": (it.get("por_que") or "")[:400],
                            "status": "proposta", "criada": agora(), "msg": "", "pedido": None})
    grava(ARQ, d)
    print(f"{len(d['pautas']) - n0} pautas propostas")


def muda(ids, status, msg=None, **extra):
    d = dados()
    for p in d["pautas"]:
        if p["id"] in ids:
            p["status"] = status
            if msg is not None:
                p["msg"] = msg
            p.update(extra)
            p["atualizada"] = agora()
    grava(ARQ, d)


def pauta(pid):
    return next((p for p in dados()["pautas"] if p["id"] == pid), None)


def _dias(v, padrao):
    """09/10/2026 (regra do usuário): quantos dias para trás o vídeo modelado pode ter (7 a 365)."""
    try:
        return max(7, min(365, int(v)))
    except (TypeError, ValueError):
        return padrao


def pedir_pesquisa(ids_canais, por_canal=3, dias=VIRAL_MAX_DIAS):
    d = dados()
    if d["pesquisa"].get("status") in ("pendente", "pesquisando"):
        return {"ok": False, "erro": "já existe uma pesquisa em andamento"}
    cs = canais()
    ids_canais = [c for c in ids_canais if c in cs]
    if not ids_canais:
        return {"ok": False, "erro": "marque pelo menos um canal"}
    d["pesquisa"] = {"status": "pendente", "canais": ids_canais, "por_canal": max(1, min(6, int(por_canal))), "dias": min(_dias(dias, VIRAL_MAX_DIAS), VIRAL_MAX_DIAS),
                     "pedida": agora(), "msg": "na fila — o pesquisador começa em instantes"}
    grava(ARQ, d)
    return {"ok": True}


# ------------------------------------------------------------------ tema próprio (link do vídeo modelado ou título)
def video_id(txt):
    m = RE_YT.search(txt or "")
    return m.group(1) if m else None


def video_info(url):
    """Dados do vídeo modelado: título, canal, inscritos, views, dias no ar, duração, tags e descrição."""
    vid = video_id(url)
    if not vid:
        raise ValueError("não achei o id do vídeo no link")
    it = _yt("videos", part="snippet,statistics,contentDetails", id=vid).get("items") or []
    if not it:
        raise ValueError("vídeo não encontrado (privado ou removido?)")
    v = it[0]
    ch = (_yt("channels", part="statistics,snippet", id=v["snippet"]["channelId"]).get("items") or [{}])[0]
    s = int((ch.get("statistics") or {}).get("subscriberCount", 0) or 0)
    views = int(v["statistics"].get("viewCount", 0) or 0)
    dias = max(1, (datetime.now(timezone.utc) - datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))).days)
    return {"url": f"https://www.youtube.com/watch?v={vid}", "titulo": v["snippet"]["title"],
            "canal": v["snippet"]["channelTitle"], "inscritos": s, "views": views, "dias": dias,
            "views_dia": round(views / dias), "razao": round(views / max(s, 1), 1),
            "min": round(_dur(v["contentDetails"]["duration"]) / 60, 1),
            "likes": int(v["statistics"].get("likeCount", 0) or 0), "comentarios": int(v["statistics"].get("commentCount", 0) or 0),
            "idioma": v["snippet"].get("defaultAudioLanguage") or v["snippet"].get("defaultLanguage"),
            "tags": (v["snippet"].get("tags") or [])[:30], "descricao": (v["snippet"].get("description") or "")[:1500]}


def _videos_com_canal(ids):
    vids = []
    for k in range(0, len(ids), 50):
        vids += _yt("videos", part="snippet,statistics,contentDetails", id=",".join(ids[k:k + 50])).get("items", [])
    chs = list({v["snippet"]["channelId"] for v in vids})
    subs = {}
    for k in range(0, len(chs), 50):
        for c in _yt("channels", part="statistics", id=",".join(chs[k:k + 50])).get("items", []):
            subs[c["id"]] = int(c["statistics"].get("subscriberCount", 0) or 0)
    agora_ = datetime.now(timezone.utc)
    out = []
    for v in vids:
        views, s = int(v["statistics"].get("viewCount", 0) or 0), subs.get(v["snippet"]["channelId"], 0)
        dias = max(1, (agora_ - datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))).days)
        out.append({"titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"], "views": views,
                    "inscritos": s, "razao": round(views / max(s, 1), 1), "dias": dias, "views_dia": round(views / dias),
                    "min": round(_dur(v["contentDetails"]["duration"]) / 60, 1),
                    "url": f"https://www.youtube.com/watch?v={v['id']}"})
    return out


def _busca_ids(q, dias, n=25):
    """ids de vídeo para a busca `q`. 1º a API (search.list, 100 unidades); se a cota diária de BUSCAS acabou (429/403),
    a página de resultados do YouTube pelo yt-dlp (só a lista — 1 página por busca, nada de baixar vídeo). As views e
    os inscritos continuam vindo da API (videos/channels.list, que não gastam a cota de busca)."""
    desde = (datetime.now(timezone.utc) - timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = _yt("search", part="id", q=q, type="video", order="viewCount", publishedAfter=desde, maxResults=n)
        return [i["id"]["videoId"] for i in r.get("items", []) if i.get("id", {}).get("videoId")], "api"
    except urllib.error.HTTPError as e:
        if e.code not in (403, 429):
            raise
    import subprocess
    sp = "EgQIBBAB" if dias <= 31 else "EgQIBRAB"   # filtro do YouTube: vídeos deste mês / deste ano
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "sp": sp})
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "--playlist-end", str(n), "--print", "%(id)s",
                        url], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return [x.strip() for x in r.stdout.splitlines() if re.fullmatch(r"[A-Za-z0-9_-]{11}", x.strip())], "yt-dlp"


def buscar(q, dias=365, n=12):
    """Os vídeos que MAIS deram certo com estes termos (para achar as palavras-chave que funcionam)."""
    ids, _ = _busca_ids(q, dias)
    out = [x for x in _videos_com_canal(ids) if x["min"] >= 4 and x["dias"] <= dias]   # sem Shorts
    return sorted(out, key=lambda x: -x["views"])[:n]


def tema_proprio(b):
    entrada = " ".join(str(b.get("entrada") or "").split())
    cs = canais()
    cid = b.get("canal")
    if not entrada:
        return {"ok": False, "erro": "cole o link do vídeo modelado ou escreva o título"}
    if cid not in cs:
        return {"ok": False, "erro": "escolha o canal (voz, tamanho e estilo do vídeo)"}
    idioma = b.get("idioma") or cs[cid]["idioma"]
    if idioma not in IDIOMAS:
        return {"ok": False, "erro": "idioma inválido"}
    link = video_id(entrada) is not None
    if not link and len(entrada) > 300:
        return {"ok": False, "erro": "título longo demais (cole só o título ou o link)"}
    d = dados()
    pid = time.strftime("%Y%m%d-%H%M%S") + f"-{len(d['pautas']):03d}"
    d["pautas"].append({"id": pid, "canal": cid, "idioma": idioma, "origem": "manual", "entrada": entrada,
                        "tipo": "link" if link else "titulo",
                        "opcoes": {"melhorar": bool(b.get("melhorar")), "clickbait": bool(b.get("clickbait")),
                        "dias": _dias(b.get("dias"), 365)},
                        "titulo": entrada[:100], "titulo_pt": "", "ideia": "", "fonte": {"url": entrada} if link else {},
                        "por_que": "", "status": "analisando", "criada": agora(), "pedido": None,
                        "msg": "na fila — o analista começa em instantes"})
    grava(ARQ, d)
    return {"ok": True, "id": pid}


def analisado(pid, itens):
    """Resultado do ANALISTA. Título e alternativas: máx. 100 caracteres (regra do usuário — nunca cortar)."""
    p = pauta(pid)
    if not p:
        sys.exit(f"pauta {pid} não existe")
    tit = " ".join(str(itens.get("titulo") or "").split())
    if not tit:
        sys.exit("faltou o título")
    if len(tit) > 100:
        sys.exit(f"RECUSADO: título com {len(tit)} caracteres (máx. 100). Reescreva (não corte) e rode de novo.")
    if not (itens.get("titulo_pt") or "").strip():
        sys.exit("faltou a tradução em português (titulo_pt)")
    alts = []
    for a in itens.get("alternativas") or []:
        at = " ".join(str(a.get("titulo") or "").split())
        if at and len(at) <= 100 and at != tit:
            alts.append({"titulo": at, "titulo_pt": (a.get("titulo_pt") or "")[:200]})
        elif len(at) > 100:
            print(f"alternativa ignorada ({len(at)} caracteres > 100): {at[:110]}")
    fonte = dict(p.get("fonte") or {})
    fonte.update({k: v for k, v in (itens.get("fonte") or {}).items() if k not in ("descricao", "tags")})
    muda([pid], "proposta", "analisado — esperando o seu OK", titulo=tit, titulo_pt=itens["titulo_pt"].strip()[:200],
         alternativas=alts[:4], ideia=(itens.get("ideia") or "")[:700], analise=(itens.get("analise") or "")[:1500],
         palavras_chave=[str(x)[:40] for x in (itens.get("palavras_chave") or [])][:15],
         por_que=(itens.get("por_que") or "")[:400], fonte=fonte, analisada=agora())
    print(f"[pautas] {pid} analisada: {tit} ({len(tit)} caracteres) + {len(alts[:4])} alternativas")


def troca_titulo(pid, i):
    p = pauta(pid)
    alts = list((p or {}).get("alternativas") or [])
    if not p or p["status"] != "proposta" or not (0 <= i < len(alts)):
        return {"ok": False, "erro": "alternativa não existe"}
    novo = alts[i]
    alts[i] = {"titulo": p["titulo"], "titulo_pt": p.get("titulo_pt", "")}
    muda([pid], "proposta", None, titulo=novo["titulo"], titulo_pt=novo.get("titulo_pt", ""), alternativas=alts)
    return {"ok": True}


# ------------------------------------------------------------------ modelagem de vídeo (mesmo modelo, canal pequeno)
def modelagem(mid):
    return next((m for m in dados()["modelagens"] if m["id"] == mid), None)


def muda_modelagem(mid, **kw):
    d = dados()
    for m in d["modelagens"]:
        if m["id"] == mid:
            m.update(kw)
            m["atualizada"] = agora()
    grava(ARQ, d)


def nova_modelagem(b):
    entrada = " ".join(str(b.get("entrada") or "").split())
    if not entrada:
        return {"ok": False, "erro": "cole o link ou o título do vídeo que deu certo"}
    if video_id(entrada) is None and len(entrada) > 300:
        return {"ok": False, "erro": "título longo demais (cole só o título ou o link)"}
    d = dados()
    mid = "mod-" + time.strftime("%Y%m%d-%H%M%S")
    d["modelagens"].append({"id": mid, "entrada": entrada, "tipo": "link" if video_id(entrada) else "titulo",
                            "dias": _dias(b.get("dias"), 90),
                            "max_inscritos": max(1000, min(1_000_000, int(b.get("max_inscritos") or 100_000))),
                            "status": "analisando", "criada": agora(), "msg": "na fila — o modelador começa em instantes",
                            "resultados": []})
    d["modelagens"] = d["modelagens"][-40:]
    grava(ARQ, d)
    return {"ok": True, "id": mid}


def outliers_buscas(mid, buscas, dias=None, max_inscritos=None, min_views=VIRAL_MIN_VIEWS, min_razao=3.0):
    """Busca no YouTube (ordem de views) e guarda só canal pequeno + vídeo muito acima dos inscritos."""
    m = modelagem(mid) or {}
    dias = min(int(dias or m.get("dias") or VIRAL_MAX_DIAS), VIRAL_MAX_DIAS)   # 22/10: regra viral (máx. 7 dias)
    min_views = max(int(min_views), VIRAL_MIN_VIEWS)
    max_inscritos = int(max_inscritos or m.get("max_inscritos") or 100_000)
    ids, erros, via = [], [], set()
    for q in buscas[:10]:
        try:
            r, como = _busca_ids(q, dias)
            ids += r
            via.add(como)
        except Exception as e:  # noqa: BLE001
            erros.append(f"{q}: {e}")
    ids = list(dict.fromkeys(ids))
    modelo = video_id(m.get("entrada", ""))
    out = [x for x in _videos_com_canal(ids)
           if x["min"] >= 4 and x["dias"] <= dias and x["views"] >= min_views and x["inscritos"] <= max_inscritos and x["razao"] >= min_razao
           and video_id(x["url"]) != modelo]
    for x in out:
        x["nota"] = round(math.log10(max(x["views"], 10)) * min(x["razao"], 50) / math.sqrt(x["dias"]), 2)
    out.sort(key=lambda x: -x["nota"])
    res = {"modelagem": mid, "quando": agora(), "dias": dias, "max_inscritos": max_inscritos, "buscas": buscas,
           "via": sorted(via),
           "erros": erros, "candidatos": out[:40]}
    grava(PASTA / f"outliers_{mid}.json", res)
    return res


def modelado(mid, itens):
    if not modelagem(mid):
        sys.exit(f"modelagem {mid} não existe")
    res = []
    for r in itens.get("resultados") or []:
        if not video_id(r.get("url", "")) or not viral_ok(r)[0]:   # 22/10: só modelo viral
            continue
        res.append({k: r.get(k) for k in ("url", "titulo", "titulo_pt", "canal", "views", "inscritos", "razao", "dias",
                                          "min", "por_que")})
    muda_modelagem(mid, status="pronta", msg=f"{len(res)} vídeos do mesmo modelo", resultados=res[:25],
                   modelo=itens.get("modelo") or {}, analise=(itens.get("analise") or "")[:1500],
                   buscas=[str(x)[:120] for x in (itens.get("buscas") or [])][:20])
    print(f"[pautas] {mid}: {len(res)} vídeos do mesmo modelo")


def copia_thumbs(pedido, slug):
    """07/10/2026: miniaturas geradas no Google Flow (Nano Banana, estilo da referência do nicho) ficam em
    pautas/<id>/miniaturas_flow/; quando o filme é entregue, vão para entregas/<slug>*/miniaturas/flow_*.jpg."""
    pa = next((x for x in dados()["pautas"] if x.get("pedido") == pedido), None)
    if not pa:
        return 0
    src = sorted((PASTA / pa["id"] / "miniaturas_flow").glob("*.jpg"))
    destinos = sorted((ROOT / "entregas").glob(f"{slug}*"), key=lambda d: d.stat().st_mtime)
    if not src or not destinos:
        return 0
    alvo = destinos[-1] / "miniaturas"
    alvo.mkdir(exist_ok=True)
    for i, f in enumerate(src, 1):
        shutil.copy2(f, alvo / f"flow_{i}.jpg")
    return len(src)


def atualiza_pesquisa(**kw):
    d = dados()
    d["pesquisa"].update(kw)
    grava(ARQ, d)


def _idade_dias(p):
    try:
        return (time.time() - time.mktime(time.strptime(p.get("criada", "")[:19], "%Y-%m-%dT%H:%M:%S"))) / 86400
    except (ValueError, TypeError):
        return 0


def descartar_antigos(dias, msg=None):
    """11/10/2026: descarta os temas ainda PARA APROVAR com mais de `dias` dias (não acumular tema velho)."""
    dias = float(dias or 0)
    if dias <= 0:
        return 0
    alvo = [p["id"] for p in dados()["pautas"] if p["status"] == "proposta" and _idade_dias(p) > dias]
    if alvo:
        muda(alvo, "descartada", msg or f"descartada: tema com mais de {dias:g} dia(s)")
    return len(alvo)


def auto_descarte():
    """Descarte automático (config.auto_descartar_dias; 0 = desligado). Roda quando o painel lê as pautas."""
    dias = float(dados()["config"].get("auto_descartar_dias") or 0)
    return descartar_antigos(dias, f"descartada sozinha: ficou mais de {dias:g} dia(s) sem aprovação") if dias > 0 else 0


def estado_api():
    auto_descarte()
    d = dados()
    return {"canais": list(canais().values()), "pautas": d["pautas"][-200:], "pesquisa": d["pesquisa"],
            "modelagens": d["modelagens"][-20:], "config": d["config"]}


def acao_api(b):
    ids = [str(x) for x in (b.get("ids") or [])]
    if b.get("acao") == "aprovar":
        sel = [p for p in dados()["pautas"] if p["id"] in ids and p["status"] in ("proposta", "erro", "descartada")]
        # tema próprio que falhou ANTES da análise: volta para o analista, não para o roteirista
        reanal = [p["id"] for p in sel if p.get("origem") == "manual" and not p.get("analisada")]
        alvo = [p["id"] for p in sel if p["id"] not in reanal]
        muda(reanal, "analisando", "na fila — o analista começa em instantes", sessao=None)
        muda(alvo, "aprovada", "aprovada — o roteirista pega na ordem")
        return {"ok": True, "n": len(alvo) + len(reanal)}
    if b.get("acao") == "tema_proprio":
        return tema_proprio(b)
    if b.get("acao") == "titulo":
        return troca_titulo(str(b.get("id")), int(b.get("i", -1)))
    if b.get("acao") == "modelar":
        return nova_modelagem(b)
    if b.get("acao") == "modelagem_refazer":
        m = modelagem(str(b.get("id")))
        if not m or m["status"] in ("analisando", "modelando"):
            return {"ok": False, "erro": "nada para refazer"}
        muda_modelagem(m["id"], status="analisando", msg="na fila — o modelador começa em instantes", sessao=None)
        return {"ok": True}
    if b.get("acao") == "modelagem_apagar":
        d = dados()
        d["modelagens"] = [m for m in d["modelagens"] if m["id"] != str(b.get("id")) or m["status"] in ("analisando", "modelando")]
        grava(ARQ, d)
        return {"ok": True}
    if b.get("acao") == "descartar":
        alvo = [p["id"] for p in dados()["pautas"] if p["id"] in ids and p["status"] in ("analisando", "proposta", "aprovada", "erro")]
        muda(alvo, "descartada", "descartada")
        return {"ok": True, "n": len(alvo)}
    if b.get("acao") == "descartar_antigos":
        return {"ok": True, "n": descartar_antigos(b.get("dias") or 0)}
    if b.get("acao") == "config":
        d = dados()
        if "auto_descartar_dias" in b:
            d["config"]["auto_descartar_dias"] = max(0, int(b.get("auto_descartar_dias") or 0))
        grava(ARQ, d)
        return {"ok": True, "n": auto_descarte(), "config": d["config"]}
    if b.get("acao") == "pesquisar":
        return pedir_pesquisa(b.get("canais") or [], b.get("por_canal") or 3, b.get("dias") or 21)
    return {"ok": False, "erro": "ação desconhecida"}


# ------------------------------------------------------------------ produzir: roteiro -> locução -> pedido
def produzir(pid):
    sys.path.insert(0, str(HERE))
    sys.path.insert(0, str(ROOT / "scripts"))
    import fila as F
    import darkplanner
    p = pauta(pid)
    if not p:
        sys.exit(f"pauta {pid} não existe")
    c = canais()[p["canal"]]
    pasta = PASTA / pid
    rot = pasta / "roteiro.txt"
    if not rot.exists() or len(rot.read_text("utf-8").strip()) < 2000:
        sys.exit(f"roteiro ausente ou curto demais em {rot}")
    texto = rot.read_text("utf-8").strip()
    alvo, n = c.get("palavras"), len(texto.split())
    if alvo and abs(n - alvo) > 0.05 * alvo:   # 07/10/2026: regra do usuário — nº de palavras fixo por canal
        sys.exit(f"roteiro com {n} palavras; o canal {c['nome']} pede {alvo} (±5 %). Ajuste o texto e rode de novo.")
    audio = pasta / "audio.mp3"
    if not audio.exists() and not (darkplanner.CHAVE.exists() and darkplanner.CHAVE.read_text("utf-8").strip()):
        # 07/11/2026: sem a chave do DarkPlanner (opcional) a pauta para no roteiro pronto, sem erro
        muda([pid], "roteirizando", f"roteiro pronto ({n} palavras) em painel/pautas/{pid}/roteiro.txt — sem DarkPlanner "
                                    "nesta instalação: grave a narração e mande roteiro + áudio em Novo filme")
        print(f"[pautas] {pid}: sem DarkPlanner — roteiro pronto, falta a narração (o usuário grava)")
        return
    if not audio.exists():
        muda([pid], "roteirizando", "gerando a locução (DarkPlanner, voz " + c["voz_nome"] + ")")
        darkplanner.gerar(texto, audio, darkplanner.voz_por_nome(c["voz_nome"], c.get("voz_id")), 1.0, f"{c['id']}-{pid}")
    # configuração do filme-modelo do canal (estilo, cartões, acabamento, proporção foto/vídeo)
    m = F.jl(F.FILA / c["modelo_pedido"] / "pedido.json") or F.jl(F.ARQUIVO / c["modelo_pedido"] / "pedido.json") or {}
    novo = F.novo({"titulo": p["titulo"], "idioma": p.get("idioma") or c["idioma"], "photo_share": m.get("photo_share", 0.8),
                   "modo": m.get("modo", "padrao"), "estilo": m.get("estilo"), "escolhas": m.get("escolhas") or {},
                   "liga": m.get("liga") or {}, "canal": c["nome"], "auto": True,
                   "observacoes": f"Pauta automática {pid} ({c['nome']}). Fonte: {p.get('fonte', {}).get('url', '')}. "
                                  f"{p.get('ideia', '')}"})
    destino = F.FILA / novo["id"]
    shutil.copy2(rot, destino / "roteiro.txt")
    shutil.copy2(audio, destino / "audio.mp3")
    novo = F.pedido(novo["id"])
    novo["arquivos"] = {"roteiro": "roteiro.txt", "roteiro_nome": f"{p['titulo'][:80]}.txt",
                        "audio": "audio.mp3", "audio_nome": f"{p['titulo'][:80]}.mp3"}
    novo.update(status="na_fila", msg="na fila — pauta automática (" + c["nome"] + ")")
    F.salva(novo)
    F.evento("novo_filme", novo["id"], titulo=novo["titulo"])
    muda([pid], "na_fila", "virou pedido na fila de produção", pedido=novo["id"])
    print(f"[pautas] {pid} -> pedido {novo['id']} na fila ({c['nome']}, {len(texto)} caracteres)")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    a = sys.argv[1:]
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if not a:
        sys.exit(__doc__)
    if a[0] == "garimpar":
        for cid in [x for x in a[1:] if not x.startswith("--") and x != op("--dias")]:
            r = garimpar(cid, int(op("--dias", 21)))
            print(f"== {cid}: {len(r['candidatos'])} outliers" + (f" | erros: {r['erros']}" if r["erros"] else ""))
            for x in r["candidatos"][:8]:
                print(f"   {x['views']:>9} views  {x['inscritos']:>7} insc  x{x['razao']:<6} {x['dias']:>2} d  {x['titulo'][:80]}")
    elif a[0] == "propor":
        propor(json.loads(Path(a[1]).read_text("utf-8")))
    elif a[0] == "lista":
        for p in dados()["pautas"]:
            if not op("--status") or p["status"] == op("--status"):
                print(p["id"], p["status"], p["canal"], "|", p["titulo"])
    elif a[0] == "produzir":
        produzir(a[1])
    elif a[0] == "estado":
        muda([a[1]], a[2], op("--msg"))
    elif a[0] == "video":
        print(json.dumps(video_info(a[1]), ensure_ascii=False, indent=1))
    elif a[0] == "buscar":
        for x in buscar(a[1], int(op("--dias", 365))):
            print(f"{x['views']:>10} views  {x['inscritos']:>8} insc  x{x['razao']:<7} {x['titulo'][:90]}  {x['url']}")
    elif a[0] == "analisado":
        analisado(a[1], json.loads(Path(a[2]).read_text("utf-8")))
    elif a[0] == "outliers":
        qs = [x for i, x in enumerate(a[2:], 2) if not x.startswith("--") and a[i - 1] != "--dias"]
        r = outliers_buscas(a[1], qs, op("--dias"))
        print(f"== {len(r['candidatos'])} outliers ({r['dias']} dias, até {r['max_inscritos']} inscritos) -> "
              f"painel/pautas/outliers_{a[1]}.json" + (f" | erros: {r['erros']}" if r["erros"] else ""))
        for x in r["candidatos"][:25]:
            print(f"   {x['views']:>9} views  {x['inscritos']:>7} insc  x{x['razao']:<6} {x['dias']:>3} d  {x['min']:>5} min  {x['titulo'][:80]}")
    elif a[0] == "modelado":
        modelado(a[1], json.loads(Path(a[2]).read_text("utf-8")))
    elif a[0] == "estado_modelagem":
        muda_modelagem(a[1], status=a[2], msg=op("--msg", ""))
    else:
        sys.exit(__doc__)
