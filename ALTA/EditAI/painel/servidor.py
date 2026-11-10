"""PAINEL — Edit.AI by Galvao no navegador para as duas etapas de julgamento do filme.

27/09/2026 (pedido do usuário): o resto do pipeline continua no chat/terminal; o painel cobre só o que é visual:
  1. FOTOS — folha de contato clicável por tag (cota, narração, nota do CLIP, AUTO/DUP). Grava direto em
     data/photo_side.json (a mesma entrada do photo_dl --aprovadas e do make_photos), por TÍTULO do arquivo —
     sem índice #N, então não existe o deslocamento que já rejeitou 81 fotos erradas.
  2. LINHA DO TEMPO — prévia do filme SEM render (narração + cortes de data/timeline.json) e rejeição corte a
     corte: "tirar deste corte" -> data/segment_rejects.json, "tirar do filme" -> data/window_rejects.json (as
     mesmas do review_apply). Depois: python scripts/fechar.py preparar.

Não roda nenhum script do pipeline e não apaga nada. Antes da 1ª gravação de cada arquivo por sessão, guarda uma
cópia em painel/_backup/. Escuta só em 127.0.0.1.
29/09: botão "Limpar concluídos" (GET /api/limpar = prévia; POST /api/limpar = executa, via fila.limpar): arquiva
pedidos entregue/cancelado em painel/fila_arquivo/ e manda as pastas APAGAR_* para a LIXEIRA do Windows (recuperável).

Uso: python painel/servidor.py [--porta 8876] [--sem-navegador]      (ou dois cliques em ABRIR_PAINEL.bat)
"""
import hashlib, json, mimetypes, os, re, shutil, subprocess, sys, threading, time, webbrowser
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
PUB = ROOT / "public"
HERE = ROOT / "painel"
CACHE = HERE / "_cache"
BACKUP = HERE / "_backup"
if "--dados" in sys.argv:   # teste: lê e grava os JSON numa CÓPIA de data/ (o resto do projeto só é lido)
    D = Path(sys.argv[sys.argv.index("--dados") + 1]).resolve()
    BACKUP = D / "_backup"
sys.path.insert(0, str(ROOT / "scripts"))

# 28/09/2026 — BAIAS: cada requisição pode apontar para outra cópia do projeto (?baia=b2); sem isso = b1 (esta pasta)
import threading as _th
_CTX = _th.local()
TESTE = "--dados" in sys.argv


def cd():
    return getattr(_CTX, "d", D)


def cp():
    return getattr(_CTX, "pub", PUB)


def cr():
    return getattr(_CTX, "root", ROOT)


def usar_baia(b):
    _CTX.root, _CTX.d, _CTX.pub = ROOT, D, PUB
    _CTX.baia = b
    if b and b != "b1" and not TESTE:
        import baias
        r = baias.caminho(b)
        if (r / "data").exists():
            _CTX.root, _CTX.d, _CTX.pub = r, r / "data", r / "public"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

LOCK = threading.Lock()          # uma gravação por vez nos JSON do pipeline
FFMPEG = threading.Semaphore(2)  # PC de 16 GB: no máximo 2 quadros extraídos ao mesmo tempo
BACKUP_FEITO = set()

PAPEL = ("cartao", "comparacao", "fichas", "palavra", "quadro", "checklist", "ficha", "manchete", "teletipo", "lupa",
         "antesdepois", "rolo", "revela")
OBRIGATORIOS = [("quadro",), ("checklist",), ("ficha",), ("manchete", "teletipo"), ("lupa",), ("antesdepois",),
                ("rolo",), ("revela",)]
try:
    from photo_sheet import REJ_GLOBAL
except Exception:  # noqa: BLE001
    REJ_GLOBAL = r"scale model|maquette|miniature|diorama|\blego\b|\b3d render|\bcgi\b|diagram|\blogo\b|\bposter\b"


# ---------------------------------------------------------------- arquivos
def jl(p, d=None):
    p = Path(p)
    if not p.exists():
        return d
    try:
        return json.loads(p.read_text("utf-8-sig"))
    except Exception:  # noqa: BLE001
        return d


def grava(p, obj):
    """Cópia de segurança na 1ª gravação da sessão + escrita atômica (tmp -> replace)."""
    p = Path(p)
    if p.exists() and p.name not in BACKUP_FEITO:
        BACKUP.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, BACKUP / f"{p.stem}_{time.strftime('%Y%m%d-%H%M%S')}{p.suffix}")
        BACKUP_FEITO.add(p.name)
    tmp = p.with_suffix(p.suffix + ".painel.tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    for tentativa in range(10):   # Windows: outro processo lendo o arquivo segura o replace por um instante
        try:
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.15 * (tentativa + 1))
    raise RuntimeError(f"não consegui gravar {p.name} (arquivo preso por outro programa)")


def mtime(nome):
    p = cd() / nome
    return p.stat().st_mtime if p.exists() else 0


def dentro(base, p):
    try:
        Path(p).resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------- filme
def filme():
    cfg = jl(cd() / "pipeline_config.json", {})
    meta = jl(cd() / "source_meta.json", {})
    nome = None
    idx = cr() / "src" / "scenes" / "index.ts"
    if idx.exists():
        m = re.search(r"Tema:\s*(.+?)(?:\s*\(|\.\s*$|$)", idx.read_text("utf-8"), re.M)
        nome = m and m.group(1).strip()
    bj = jl(cd() / "beats.json", {})
    if not nome:
        nome = next((b.get("capitulo") for b in bj.get("beats", []) if b.get("capitulo")), "filme atual")
    return {"nome": nome, "idioma": cfg.get("screenLanguage", "?"), "duracao": meta.get("durationSec", 0),
            "photo_share": cfg.get("photo_share", 0.5), "modo": cfg.get("modo", "padrao"),
            "tom": (cfg.get("acabamento") or {}).get("tom")}


def versao():
    return {k: mtime(k) for k in ("photo_side.json", "photo_pool.json", "timeline.json", "window_rejects.json",
                                   "segment_rejects.json", "clips.json")}


# ---------------------------------------------------------------- fotos
def imagem_de(e, cheia=False):
    for k in (("file", "thumb_file") if cheia else ("thumb_file", "file")):
        if e.get(k) and Path(e[k]).exists():
            return e[k]
    return None


def remota(t, e, cheia=False):
    """Endereço da foto na FONTE quando ela não está mais no disco (filme fechado: assets/thumbs vai para APAGAR_)."""
    from urllib.parse import quote
    w = 1920 if cheia else 640
    u = e.get("url") or ""
    if "images.pexels.com" in u:
        return f"{u.split('?')[0]}?auto=compress&w={w}"
    if "pixabay.com" in u:
        return u
    if "wikimedia.org" in u or (e.get("descurl") or "").startswith("https://commons.wikimedia.org"):
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(t.replace('File:', '', 1))}?width={w}"
    return u or None


def fotos():
    pool = jl(cd() / "photo_pool.json", {})
    side = jl(cd() / "photo_side.json", {})
    pre = jl(cd() / "photo_prefilter.json", {})
    bj = jl(cd() / "beats.json", {"tags": {}, "beats": []})
    paras = (jl(cd() / "master_transcript.json", {}) or {}).get("paragraphs", [])
    rej = re.compile("|".join([REJ_GLOBAL] + list(bj.get("rejeita_titulo", []))), re.I)
    try:
        from demanda import cotas
        q = cotas(bruta=True)
    except Exception as ex:  # noqa: BLE001
        print("[painel] demanda indisponível:", ex)
        q = {}
    trechos, ordem = {}, []
    for b in bj.get("beats", []):
        for t in b.get("tags", []):
            if t not in ordem:
                ordem.append(t)
            if len(trechos.setdefault(t, [])) < 3 and b.get("para") is not None and b["para"] < len(paras):
                txt = (paras[b["para"]].get("text") or "").strip()
                if txt and txt not in trechos[t]:
                    trechos[t].append(txt[:420])
    itens, fora_do_disco = [], 0
    for t, e in pool.items():
        sd = side.get(t)
        img = imagem_de(e)
        if not img and not sd:
            continue
        fora_do_disco += not img
        pf = pre.get(t, {})
        itens.append({
            "t": t, "tag": (e.get("tags") or ["?"])[0], "nota": pf.get("nota"), "dup": bool(pf.get("dup")),
            "auto": bool(rej.search(t)), "lic": e.get("license"), "artista": re.sub(r"<[^>]+>", "", e.get("artist") or "")[:80],
            "w": e.get("width"), "h": e.get("height"), "desc": re.sub(r"<[^>]+>", "", e.get("desc") or "")[:400],
            "url": e.get("descurl"), "data": (e.get("date") or "")[:10], "img": bool(img or remota(t, e)), "local": bool(img),
            "cheia": bool(e.get("file") and Path(e["file"]).exists()),
            "v": sd.get("verdict") if sd else None, "tags_ok": sd.get("tags") if sd else None,
            "era": sd.get("era") if sd else None, "focus": sd.get("focus") if sd else None,
            "banco": bool(sd and sd.get("banco")), "nota_juiz": sd.get("note") if sd else None,
        })
    for i in itens:   # mesma ordem da folha: melhor nota do CLIP primeiro, AUTO e duplicata no fim
        i["_k"] = (i["auto"], i["dup"], -float(i["nota"] if i["nota"] is not None else -1))
    itens.sort(key=lambda i: i.pop("_k"))
    banco_por_tag = Counter((v.get("tags") or ["?"])[0] for k, v in side.items()
                            if v.get("verdict") == "ok" and v.get("banco") and k not in pool)
    tags = []
    for t in ordem + sorted({i["tag"] for i in itens} - set(ordem)):
        tags.append({"tag": t, "desc": bj.get("tags", {}).get(t, ""), "cota": q.get(t, 0), "trechos": trechos.get(t, []),
                     "banco_fora": banco_por_tag.get(t, 0)})
    return {"tags": tags, "itens": itens, "fora_do_disco": fora_do_disco, "versao": versao()}


def decidir(body):
    with LOCK:
        p = cd() / "photo_side.json"
        side = jl(p, {})
        pool = jl(cd() / "photo_pool.json", {})
        feitos = 0
        for d in body.get("itens", []):
            t = d.get("t")
            if not t or t not in pool:
                continue
            ant = side.get(t) or {}
            v = d.get("v")
            if v is None:
                if ant.get("banco"):
                    continue   # item do banco não volta a "pendente": só aprova ou tira deste filme
                side.pop(t, None)
            elif v == "ok":
                novo = {k: ant[k] for k in ("banco", "sheet_index", "focus") if k in ant}
                tag = d.get("tag") or (ant.get("tags") or pool[t].get("tags") or ["?"])[0]
                tags = ant.get("tags") if ant.get("tags") and ant["tags"][0] == tag else [tag]
                novo.update({"verdict": "ok", "tags": tags, "era": d.get("era") or ant.get("era") or "modern",
                             "note": "painel"})
                if d.get("focus"):
                    novo["focus"] = [round(float(x), 3) for x in d["focus"]][:2]
                side[t] = novo
            elif v == "reject":
                side[t] = {"verdict": "reject", "note": d.get("note") or "painel", **({"banco": ant["banco"]} if ant.get("banco") else {})}
            else:
                continue
            feitos += 1
        grava(p, side)
    return {"ok": True, "feitos": feitos, "versao": versao()}


# ---------------------------------------------------------------- linha do tempo
def resumo_ov(ov):
    if not ov:
        return None
    for k in ("titulo", "nome", "texto", "manchete", "valor", "legenda", "palavra", "rotulo"):
        if isinstance(ov.get(k), str) and ov[k].strip():
            return {"tipo": ov.get("tipo", "?"), "txt": ov[k][:70]}
    return {"tipo": ov.get("tipo", "?"), "txt": ""}


def tem_mapa():
    idx = cr() / "src" / "scenes" / "index.ts"
    if not idx.exists():
        return None
    cena = next((l.split('"./')[1].split('"')[0] for l in idx.read_text("utf-8").splitlines()
                 if 'from "./' in l and "Scenes" in l), None)
    f = cr() / "src" / "scenes" / f"{cena}.tsx" if cena else None
    if not f or not f.exists():
        return None
    return bool(re.search(r"<(MapaRota|MapaCampanha)\b", f.read_text("utf-8")))


def travas(items, fps, minutos, cfg, no_plano):
    out = []
    ovs = [it for it in items if (it.get("ov") or {}).get("tipo") in PAPEL]
    n, minp = len(ovs), max(8, round(minutos / 1.5))
    out.append({"ok": n >= minp, "txt": f"Cartões em papel: {n}", "det": f"mínimo {minp} para {minutos:.0f} min"})
    tipos = Counter(it["ov"]["tipo"] for it in ovs)
    if n:
        t, c = tipos.most_common(1)[0]
        out.append({"ok": c <= 0.35 * n, "txt": f"Mescla: “{t}” é {c * 100 // n}% dos cartões", "det": "teto 35% por tipo"})
    faltam = [" ou ".join(g) for g in OBRIGATORIOS if not any(tipos.get(x) for x in g)]
    out.append({"ok": not faltam, "txt": "Família de arquivo " + ("completa" if not faltam else "incompleta"),
                "det": ("8 grupos na tela" if not faltam else "falta: " + ", ".join(faltam))})
    marcos = [0] + sorted(it["from"] / fps for it in ovs) + [minutos * 60]
    gap = max((b - a for a, b in zip(marcos, marcos[1:])), default=0)
    out.append({"ok": gap <= 150, "aviso": True, "txt": f"Maior trecho sem cartão: {int(gap // 60)}:{int(gap % 60):02d}",
                "det": "bom até 2:30"})
    n_anim = sum(1 for it in items if it["type"] == "animation")
    maxa = max(6, round(minutos / 3))
    out.append({"ok": n_anim <= maxa, "txt": f"Animações de tela cheia: {n_anim}", "det": f"teto {maxa}"})
    m = tem_mapa()
    if m is not None:
        out.append({"ok": m, "txt": "Mapa no filme" if m else "Sem mapa", "det": "MapaRota ou MapaCampanha"})
    fo = sum(1 for it in items if it.get("kind") == "photo")
    vi = sum(1 for it in items if it.get("kind") == "video")
    alvo = float(cfg.get("photo_share", 0.5))
    real = fo / (fo + vi) if fo + vi else 0
    out.append({"ok": abs(real - alvo) <= 0.12, "aviso": True, "txt": f"Foto {real:.0%} · vídeo {1 - real:.0%}",
                "det": f"pedido: foto {alvo:.0%}"})
    out.append({"ok": no_plano == 0, "aviso": True,
                "txt": "Nenhuma rejeição pendente" if not no_plano else f"{no_plano} rejeitado(s) ainda no plano",
                "det": "rode fechar.py preparar" if no_plano else "plano em dia"})
    return out


def linha():
    tl = jl(cd() / "timeline.json", {"fps": 30, "items": []})
    fps = tl.get("fps", 30)
    lib = {c["id"]: c for c in jl(cd() / "clips.json", {"clips": []})["clips"]}
    bj = jl(cd() / "beats.json", {"beats": []})
    mt = jl(cd() / "master_transcript.json", {}) or {}
    paras = mt.get("paragraphs", [])
    beat_cap = {b["id"]: b.get("capitulo") for b in bj.get("beats", [])}
    wrej = set(jl(cd() / "window_rejects.json", []) or [])
    srej = jl(cd() / "segment_rejects.json", {}) or {}
    cfg = jl(cd() / "pipeline_config.json", {})
    meta = jl(cd() / "source_meta.json", {})
    minutos = (meta.get("durationSec") or tl.get("durationInFrames", 0) / fps) / 60
    items, no_plano, sem_arquivo = [], 0, 0
    for i, it in enumerate(tl["items"]):
        sem = bool(it.get("src")) and not (cp() / it["src"]).exists()
        sem_arquivo += sem
        c = lib.get(it.get("clip") or "", {})
        rej = "filme" if it.get("clip") in wrej else "corte" if it.get("clip") in srej.get(it["id"], []) else None
        no_plano += bool(rej)
        items.append({"i": i, "id": it.get("id"), "type": it["type"], "kind": it.get("kind"), "from": it["from"],
                      "dur": it["dur"], "src": it.get("src"), "clip": it.get("clip"), "trim": it.get("trimBefore") or 0,
                      "scene": it.get("scene"), "ov": resumo_ov(it.get("ov")), "beat": it.get("beat"),
                      "tag": (c.get("tags") or [""])[0], "title": (c.get("title") or c.get("channel") or "").replace("File:", ""),
                      "lic": c.get("license"), "fonte": (c.get("source") or "")[:3].rstrip(":"), "move": it.get("move"),
                      "rej": rej, "sem": sem})
    caps = []
    for b in bj.get("beats", []):
        if b.get("capitulo") and b.get("para") is not None and b["para"] < len(paras):
            caps.append({"f": paras[b["para"]].get("startFrame", 0), "nome": b["capitulo"], "lugar": b.get("lugar")})
    frases = [{"s": s["startSec"], "e": s["endSec"], "w": [[w["w"], w["s"], w["e"]] for w in s.get("words", [])]}
              for s in mt.get("sentences", [])]
    render_ok = (cd() / "timeline_renderizado.json").exists() and \
        (cd() / "timeline_renderizado.json").read_bytes() == (cd() / "timeline.json").read_bytes()
    return {"fps": fps, "total": tl.get("durationInFrames") or (items[-1]["from"] + items[-1]["dur"] if items else 0),
            "items": items, "caps": caps, "frases": frases, "travas": travas(tl["items"], fps, minutos, cfg, no_plano),
            "render_ok": render_ok, "tem_audio": (cp() / "audio.mp3").exists(), "sem_arquivo": sem_arquivo,
            "versao": versao()}


def rejeitar(body):
    cut, clip, escopo, desfazer = body.get("cut"), body.get("clip"), body.get("escopo"), bool(body.get("desfazer"))
    if not cut or not clip or escopo not in ("corte", "filme"):
        return {"ok": False, "erro": "pedido incompleto"}
    with LOCK:
        wp, sp = cd() / "window_rejects.json", cd() / "segment_rejects.json"
        wrej, srej = set(jl(wp, []) or []), jl(sp, {}) or {}
        if escopo == "filme":
            (wrej.discard if desfazer else wrej.add)(clip)
            if desfazer:   # desfazer "do filme" também limpa o do corte (o card volta a limpo)
                srej[cut] = [x for x in srej.get(cut, []) if x != clip]
        else:
            lst = [x for x in srej.get(cut, []) if x != clip]
            if not desfazer:
                lst.append(clip)
            srej[cut] = lst
        srej = {k: v for k, v in srej.items() if v}
        grava(wp, sorted(wrej))
        grava(sp, srej)
    return {"ok": True, "versao": versao()}


# ---------------------------------------------------------------- fila, estilos, catálogo (27/09 — 2ª parte)
sys.path.insert(0, str(HERE))
import catalogo  # noqa: E402
import importlib  # noqa: E402

_CAT_MT = [Path(catalogo.__file__).stat().st_mtime]


def _cat():
    """04/10/2026: catalogo.py editado (estilos novos, regra de trilha) entra sem reiniciar o painel."""
    mt = Path(catalogo.__file__).stat().st_mtime
    if mt != _CAT_MT[0]:
        _CAT_MT[0] = mt
        importlib.reload(catalogo)
    return catalogo
import fila as F  # noqa: E402
import escritorio  # noqa: E402
_ESC_MT = [Path(escritorio.__file__).stat().st_mtime]


import pautas as _PA  # noqa: E402
_PA_MT = [Path(_PA.__file__).stat().st_mtime]


def _pa():
    """07/10/2026: aba Pautas (painel/pautas.py) — editado entra sem reiniciar o painel."""
    global _PA
    mt = Path(_PA.__file__).stat().st_mtime
    if mt != _PA_MT[0]:
        _PA_MT[0] = mt
        _PA = importlib.reload(_PA)
    return _PA


_CEN = None


def _cen():
    """16/10/2026: CENTRAL (painel/central.py) — saúde, avisos e botões de recuperação. Editar central.py pede reiniciar o painel."""
    global _CEN
    if _CEN is None:
        import central as _c
        _CEN = _c
    return _CEN


def _esc():
    """05/10/2026: tela do escritório (funcionários ao vivo) — escritorio.py editado entra sem reiniciar o painel."""
    mt = Path(escritorio.__file__).stat().st_mtime
    if mt != _ESC_MT[0]:
        _ESC_MT[0] = mt
        importlib.reload(escritorio)
    return escritorio
if "--dados" in sys.argv:   # teste: fila, referências e eventos também na cópia (nada aparece no painel de verdade)
    F.FILA, F.REFS, F.EVENTOS = D / "fila", D / "referencias", D / "eventos.jsonl"
    F.ARQUIVO, F.APAGAR_RAIZES = D / "fila_arquivo", [D]   # limpeza de teste: só APAGAR_* dentro da cópia

EXT_OK = {"roteiro": {".txt", ".md"}, "audio": {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus"},
          "video": {".mp4", ".mov", ".mkv", ".webm", ".m4v"}}


def vigia_vivo():
    # O gerente mantém o heartbeat mesmo desligado; só conta como conectado
    # quando o usuário ligou os funcionários. O monitor antigo é independente.
    for nome, limite in ((".vigia_vivo", 25), (".gerente_vivo", 60)):
        if nome == ".gerente_vivo" and not cfg_painel().get("gerente"):
            continue
        try:
            if 0 <= time.time() - float((F.EVENTOS.parent / nome).read_text().strip()) < limite:
                return True
        except (OSError, ValueError):
            pass
    return False


def motor_nome():
    try:
        import motor
        return "Codex" if motor.qual() == "codex" else "Claude"
    except Exception:
        return "Claude"


def cfg_painel():
    try:
        return {"paralelo": 1, "auto": False, **json.loads((HERE / "config.json").read_text("utf-8"))}
    except Exception:  # noqa: BLE001
        return {"paralelo": 1, "auto": False}


def baias_estado():
    import baias as B
    oc = {p.get("baia"): p for p in F.todos() if p.get("baia") and p.get("status") in ("produzindo", "esperando_voce", "pausado")}
    lim = int(cfg_painel().get("paralelo", 1))
    trava = None
    try:
        t = json.loads((ROOT.parent / ".trava_pesado").read_text("utf-8"))
        trava = t
    except Exception:  # noqa: BLE001
        pass
    out = []
    for i in range(1, max(2, lim) + 1):
        b = f"b{i}"
        p = oc.get(b)
        out.append({"baia": b, "ativa": i <= lim, "existe": B.caminho(b).exists(),
                    "filme": ({"id": p["id"], "titulo": p["titulo"], "status": p["status"], "etapa": p.get("etapa")} if p else None),
                    "pesado": (trava.get("etapa") if trava and trava.get("baia") == B.caminho(b).name else None)})
    return {"baias": out, "trava": trava}


def config_salvar(b):
    c = cfg_painel()
    if "paralelo" in b:
        c["paralelo"] = max(1, min(2, int(b["paralelo"])))   # 05/10/2026: regra do usuário, no máximo 2 filmes ao mesmo tempo
    if "auto" in b:
        c["auto"] = bool(b["auto"])
    F.grava(HERE / "config.json", c)
    F.evento("config", None, **c)
    return {"ok": True, "config": c, **baias_estado()}


def limpeza_contagem():
    try:
        return F.limpeza_contagem()
    except Exception:  # noqa: BLE001
        return {"pedidos": 0, "pastas": 0, "arquivados": 0}


LIMPANDO = threading.Lock()   # um clique por vez (a Lixeira pode levar um tempo com pastas grandes)


def limpar(body):
    """Botão "Limpar concluídos": executa só o que a pessoa viu na prévia (ids e caminhos), conferido de novo no fila.py."""
    if not LIMPANDO.acquire(blocking=False):
        return {"ok": False, "erro": "uma limpeza já está em andamento"}
    try:
        ped, pas = body.get("pedidos"), body.get("pastas")
        if not isinstance(ped, list) or not isinstance(pas, list):
            return {"ok": False, "erro": "abra a prévia antes de limpar"}
        r = F.limpar([str(x) for x in ped], [str(x) for x in pas], origem="painel")
    finally:
        LIMPANDO.release()
    return {**r, "ok": True, "fila": fila_estado()}   # erros por pasta vão em r["erros"]


def fila_estado():
    return {"pedidos": F.todos(), "vivo": vigia_vivo(), "motor_nome": motor_nome(), "etapas": F.ETAPAS, "config": cfg_painel(), **baias_estado(),
            "limpeza": limpeza_contagem(),
            "aovivo": {p["baia"]: ao_vivo(p["baia"]) for p in F.todos() if p.get("baia") and p.get("status") == "produzindo"},
            "refs": sorted([F.jl(p) for p in F.REFS.glob("*/ref.json")] if F.REFS.exists() else [],
                           key=lambda r: r.get("criado", ""), reverse=True)}


def fila_acao(b):
    pid, ac = b.get("id"), b.get("acao")
    with LOCK:
        p = F.pedido(pid) if pid else None
        if not p:
            return {"ok": False, "erro": "pedido não encontrado"}
        if ac == "confirmar":
            precisa = ("roteiro", "audio")
            if p.get("formato") == "short3d":   # 06/11/2026: short 3D só precisa do tema; roteiro e áudio são opcionais
                precisa = () if _tem_darkplanner() else ("audio",)
            falta = [c for c in precisa if not (F.FILA / pid / p["arquivos"].get(c, "_")).is_file()]
            if falta:
                return {"ok": False, "erro": "falta enviar: " + ", ".join(falta)}
            p.update(status="na_fila", msg="na fila — o Claude começa quando chegar a vez")
            F.salva(p)
            F.evento("novo_filme", pid, titulo=p["titulo"])
        elif ac == "continuar":
            nome = next((e[1] for e in F.ETAPAS if e[0] == p.get("etapa")), p.get("etapa") or "")
            p.update(status="produzindo", msg=f"você liberou “{nome}” — o Claude continua")
            p["historico"].append({"ts": F.agora(), "etapa": p.get("etapa"), "status": "produzindo", "msg": "liberado no painel"})
            F.salva(p)
            F.evento("continuar", pid, etapa=p.get("etapa"), titulo=p["titulo"])
        elif ac == "recado":
            t = (b.get("texto") or "").strip()[:4000]
            if not t:
                return {"ok": False, "erro": "recado vazio"}
            p.setdefault("recados", []).append({"ts": F.agora(), "texto": t})
            F.salva(p)
            F.evento("recado", pid, texto=t, titulo=p["titulo"])
        elif ac == "auto":
            p["auto"] = bool(b.get("valor"))
            p["historico"].append({"ts": F.agora(), "etapa": p.get("etapa"), "status": p["status"],
                                   "msg": "modo automático " + ("ligado" if p["auto"] else "desligado")})
            if p["auto"] and p["status"] == "esperando_voce":
                p.update(status="produzindo", msg="modo automático: o Claude julga e continua sozinho")
            F.salva(p)
            F.evento("auto", pid, valor=p["auto"], etapa=p.get("etapa"), titulo=p["titulo"])
        elif ac in ("pausar", "retomar", "cancelar"):
            p["status"] = {"pausar": "pausado", "retomar": "na_fila" if not p.get("etapa") else "produzindo",
                           "cancelar": "cancelado"}[ac]
            p["msg"] = {"pausar": "pausado por você", "retomar": "retomado", "cancelar": "cancelado por você"}[ac]
            F.salva(p)
            F.evento(ac, pid, titulo=p["titulo"])
        elif ac in ("subir", "descer"):
            ps = F.todos()
            i = next(k for k, x in enumerate(ps) if x["id"] == pid)
            j = i - 1 if ac == "subir" else i + 1
            if 0 <= j < len(ps):
                ps[i]["ordem"], ps[j]["ordem"] = ps[j]["ordem"], ps[i]["ordem"]
                if ps[i]["ordem"] == ps[j]["ordem"]:
                    ps[i]["ordem"] += -1 if ac == "subir" else 1
                F.salva(ps[i]); F.salva(ps[j])
        else:
            return {"ok": False, "erro": "ação desconhecida"}
    return {"ok": True, **fila_estado()}


def ref_nova(b):
    F.REFS.mkdir(parents=True, exist_ok=True)
    rid = time.strftime("%Y%m%d-%H%M%S-") + F.slug(b.get("nome") or "referencia")
    (F.REFS / rid).mkdir(parents=True, exist_ok=True)
    r = {"id": rid, "nome": (b.get("nome") or "Meu estilo")[:60], "link": (b.get("link") or "").strip()[:500],
         "nota": (b.get("nota") or "")[:2000], "criado": F.agora(), "status": "enviando", "msg": "", "video": None}
    F.grava(F.REFS / rid / "ref.json", r)
    return {"ok": True, "ref": r}


def ref_analisar(b):
    rid = b.get("id")
    p = F.REFS / (rid or "_") / "ref.json"
    r = F.jl(p)
    if not r:
        return {"ok": False, "erro": "referência não encontrada"}
    if not r.get("video") and not r.get("link"):
        return {"ok": False, "erro": "mande o vídeo ou cole um link"}
    r.update(status="na_fila", msg="aguardando o Claude analisar")
    F.grava(p, r)
    F.evento("analisar_estilo", rid, nome=r["nome"], link=r.get("link"), video=r.get("video"), nota=r.get("nota"))
    return {"ok": True, **fila_estado()}


def estilo_salvar(b):
    nome = (b.get("nome") or "").strip()[:60]
    if not nome:
        return {"ok": False, "erro": "dê um nome ao estilo"}
    sid = b.get("id") or F.slug(nome)
    catalogo.ESTILOS_DIR.mkdir(parents=True, exist_ok=True)
    p = catalogo.ESTILOS_DIR / f"{sid}.json"
    velho = F.jl(p, {})
    velho.update({"id": sid, "nome": nome, "desc": (b.get("desc") or velho.get("desc") or "")[:300],
                  "escolhas": b.get("escolhas") or {}, "liga": b.get("liga") or {},
                  "origem": velho.get("origem") or "painel", "atualizado": F.agora()})
    F.grava(p, velho)
    return {"ok": True, "catalogo": catalogo.catalogo()}


def estilo_apagar(b):
    p = catalogo.ESTILOS_DIR / f"{F.slug(b.get('id') or '_')}.json"
    if p.exists():   # não apaga de vez: vai para painel/estilos/_removidos
        (catalogo.ESTILOS_DIR / "_removidos").mkdir(exist_ok=True)
        shutil.move(str(p), catalogo.ESTILOS_DIR / "_removidos" / p.name)
    return {"ok": True, "catalogo": catalogo.catalogo()}


def ao_vivo(b=None):
    """02/10/2026 (pedido do usuário: "informações em tempo real na Edit.AI by Galvao"): o log mais recente da baia
    (busca, juízes, transcrição, preparar, render) — a última linha vira a linha "ao vivo" do filme."""
    try:
        import baias as B
        r = ROOT if not b or b == "b1" else B.caminho(b)
        d = r / "data"
        cands = [x for x in d.glob("*.log")] + [r / "out" / "hybrid" / "progress.txt"]
        cands = [x for x in cands if x.exists()]
        if not cands:
            return None
        f = max(cands, key=lambda x: x.stat().st_mtime)
        with open(f, "rb") as fh:
            fh.seek(max(0, f.stat().st_size - 8000))
            txt = fh.read().decode("utf-8", "replace")
        linhas = [l.split("\r")[-1].strip() for l in txt.splitlines()]
        linhas = [l for l in linhas if l and not l.startswith("Warning: You are sending unauthenticated")]
        return {"arq": f.name, "idade": round(time.time() - f.stat().st_mtime), "linha": (linhas[-1] if linhas else "")[:240],
                "ultimas": linhas[-40:]}
    except Exception:  # noqa: BLE001
        return None


def log_producao(n=80):
    p = cd() / "fechar.log"
    linhas = []
    if p.exists():
        with open(p, "rb") as fh:
            fh.seek(max(0, p.stat().st_size - 40000))
            linhas = fh.read().decode("utf-8", "replace").splitlines()[-n:]
    prog = cr() / "out" / "hybrid" / "progress.txt"
    pr = prog.read_text("utf-8", "replace").splitlines()[-6:] if prog.exists() else []
    return {"log": linhas, "render": pr, "atual": ao_vivo(getattr(_CTX, "baia", None))}


# ---------------------------------------------------------------- miniaturas da linha do tempo
def mini(src, t):
    f = (cp() / src)
    if not dentro(cp(), f) or not f.exists():
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.md5(f"{cr()}|{src}|{t:.2f}|{f.stat().st_mtime}".encode()).hexdigest()[:16]
    out = CACHE / f"{h}.jpg"
    if out.exists():
        return out
    with FFMPEG:
        if out.exists():
            return out
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            from PIL import Image
            im = Image.open(f).convert("RGB")
            im.thumbnail((480, 270))
            im.save(out, quality=82)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(f), "-frames:v", "1",
                            "-vf", "scale=480:-2", "-q:v", "4", str(out)], check=False,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return out if out.exists() else None


# ---------------------------------------------------------------- HTTP
def _tem_darkplanner():
    try:
        import chaves as _ch
        return any(c["id"] == "darkplanner" and c["configurada"] for c in _ch.lista()["chaves"])
    except Exception:  # noqa: BLE001
        return False


def _lic():
    import licenca
    return licenca


class H(BaseHTTPRequestHandler):
    server_version = "Painel/1.0"

    def log_message(self, fmt, *args):   # silencioso: só erro
        if args and str(args[1] if len(args) > 1 else "").startswith(("4", "5")):
            sys.stderr.write("[painel] %s\n" % (fmt % args))

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _arquivo(self, p, cache=0):
        p = Path(p)
        if not p.exists() or not p.is_file():
            self.send_error(404)
            return
        tam = p.stat().st_size
        ctype = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
        a, b, parcial = 0, tam - 1, False
        rg = self.headers.get("Range")
        m = re.match(r"bytes=(\d*)-(\d*)", rg or "")
        if m:
            parcial = True
            if m.group(1):
                a = int(m.group(1))
                b = int(m.group(2)) if m.group(2) else tam - 1
            else:
                a, b = max(0, tam - int(m.group(2) or 0)), tam - 1
            b = min(b, tam - 1)
            if a > b:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{tam}")
                self.end_headers()
                return
        self.send_response(206 if parcial else 200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(b - a + 1))
        if parcial:
            self.send_header("Content-Range", f"bytes {a}-{b}/{tam}")
        self.send_header("Cache-Control", f"max-age={cache}" if cache else "no-cache")
        self.end_headers()
        with open(p, "rb") as fh:
            fh.seek(a)
            falta = b - a + 1
            while falta > 0:
                bloco = fh.read(min(262144, falta))
                if not bloco:
                    break
                self.wfile.write(bloco)
                falta -= len(bloco)

    def _permitido(self):
        """16/10/2026: com o acesso pelo celular ligado o servidor escuta na rede — fora deste PC só entra quem tem a chave."""
        ip = self.client_address[0]
        if ip in ("127.0.0.1", "::1") or ip.startswith("::ffff:127."):
            return True
        tok = _cen().conf()["remoto"].get("token") or ""
        if tok and f"sala_k={tok}" in (self.headers.get("Cookie") or ""):
            return True
        u = urlparse(self.path)
        if tok and parse_qs(u.query).get("k", [""])[0] == tok:
            self.send_response(302)
            self.send_header("Set-Cookie", f"sala_k={tok}; Max-Age=31536000; Path=/; HttpOnly; SameSite=Lax")
            self.send_header("Location", u.path or "/central")
            self.end_headers()
            return False
        self.send_error(403, "sem a chave da Edit.AI by Galvao")
        return False

    def do_GET(self):
        if not self._permitido():
            return
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        usar_baia(q.get("baia"))
        try:
            # 06/11/2026 LICENÇA (só no pacote vendido; painel/licenca.py): sem licença ativa só abre a tela de ativação
            if u.path == "/api/licenca":
                return self._json(_lic().estado())
            if u.path == "/licenca":
                return self._arquivo(HERE / "licenca.html")
            if not _lic().ativa() and not u.path.startswith("/app/"):   # o ícone/logo aparece na tela de ativação
                if u.path.startswith("/api/"):
                    return self._json({"ok": False, "erro": "licença inativa", "licenca": True}, 403)
                self.send_response(302)
                self.send_header("Location", "/licenca")
                self.end_headers()
                return
            if u.path == "/estudio":
                return self._arquivo(HERE / "app" / "estudio.html")
            if u.path == "/api/editai/thumb":
                import editai
                return self._arquivo(editai.thumb_path(q.get("id", "")))
            if u.path == "/api/editai":
                import editai
                return self._json({"canais":editai.profiles(), "presets":editai.presets(), "settings":editai.settings(), "uso":editai.ledger(), "fila":F.todos()})
            if u.path == "/api/editai/busca":
                import editai
                try:
                    return self._json({"ok":True,"resultados":editai.sources(q.get("fonte", ""),q.get("q", ""))})
                except Exception as ex:
                    return self._json({"ok":False,"erro":"Não foi possível consultar o acervo: " + str(ex)[:200]}, 502)
            if u.path in ("/", "/index.html"):
                return self._arquivo(HERE / "index.html")
            if u.path in ("/chaves", "/chaves.html"):   # 06/11/2026: aba das chaves de API
                return self._arquivo(HERE / "chaves.html")
            if u.path == "/api/chaves":
                import chaves as _ch
                return self._json(_ch.lista())
            if u.path == "/api/motor":   # 06/11/2026: Claude ou ChatGPT Codex fazendo o trabalho
                import motor as _mo
                return self._json(_mo.estado())
            if u.path in ("/central", "/central.html", "/app"):
                return self._arquivo(HERE / "central.html")
            if u.path == "/api/central":
                return self._json(_cen().estado(forcar=q.get("forcar") == "1"))
            if u.path == "/api/central/faixas":
                return self._json({"ok": True, "faixas": _cen().faixas_disponiveis(q.get("b") or "b1")})
            if u.path == "/api/central/log":
                return self._json(_cen().log_da_acao(q.get("id", "")))
            if u.path == "/central/arquivo":
                f = _cen().arquivo_entrega(q.get("slug", ""), q.get("f", ""))
                return self._arquivo(f, cache=300) if f else self.send_error(404)
            if u.path.startswith("/app/"):
                f = HERE / "app" / unquote(u.path[5:])
                return self._arquivo(f, cache=3600) if dentro(HERE / "app", f) else self.send_error(403)
            if u.path in ("/escritorio", "/escritorio.html"):
                return self._arquivo(HERE / "escritorio.html")
            if u.path == "/api/escritorio":
                return self._json(_esc().estado())
            if u.path == "/api/pautas":
                return self._json(_pa().estado_api())
            if u.path == "/api/filme":
                return self._json(filme())
            if u.path == "/api/versao":
                return self._json(versao())
            if u.path == "/api/fotos":
                return self._json(fotos())
            if u.path == "/api/linha":
                return self._json(linha())
            if u.path == "/foto":
                t = q.get("t", "")
                e = jl(cd() / "photo_pool.json", {}).get(t)
                if not e:
                    return self.send_error(404)
                f = imagem_de(e, cheia=q.get("cheia") == "1")
                if f and dentro(cr(), f):
                    return self._arquivo(f, cache=3600)
                r = remota(t, e, cheia=q.get("cheia") == "1")
                if not r:
                    return self.send_error(404)
                self.send_response(302)
                self.send_header("Location", r)
                self.end_headers()
                return
            if u.path == "/mini":
                f = mini(q.get("src", ""), float(q.get("t", "0") or 0))
                return self._arquivo(f, cache=86400) if f else self.send_error(404)
            if u.path == "/api/catalogo":
                return self._json(_cat().catalogo())
            if u.path == "/api/fila":
                return self._json(fila_estado())
            if u.path == "/api/config":
                return self._json({"config": cfg_painel(), **baias_estado()})
            if u.path == "/api/fila/log":
                return self._json(log_producao())
            if u.path == "/api/limpar":   # só a prévia: GET nunca mexe em nada (?simular=1 ou sem nada)
                return self._json({"ok": True, "simular": True, **F.limpeza_previa()})
            if u.path == "/api/fila/arquivados":
                return self._json({"ok": True, "arquivados": F.arquivados()})
            if u.path.startswith("/previa/"):
                f = HERE / "previas" / unquote(u.path[8:])
                return self._arquivo(f, cache=600) if dentro(HERE / "previas", f) else self.send_error(403)
            if u.path.startswith("/ref/"):
                f = F.REFS / unquote(u.path[5:])
                return self._arquivo(f, cache=60) if dentro(F.REFS, f) else self.send_error(403)
            if u.path.startswith("/pub/"):
                f = cp() / unquote(u.path[5:])
                if not dentro(cp(), f):
                    return self.send_error(403)
                return self._arquivo(f)
            self.send_error(404)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def do_PUT(self):
        if not self._permitido():
            return
        """Envio de arquivo em fluxo: PUT /api/upload?id=PEDIDO&campo=roteiro|audio  ou  ?ref=RID&campo=video."""
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        usar_baia(None)
        try:
            if u.path == "/api/central/thumb":   # 16/10/2026: miniatura nova enviada pelo celular para uma entrega
                n = int(self.headers.get("Content-Length") or 0)
                if n > 25_000_000:
                    return self._json({"ok": False, "erro": "imagem grande demais (máx. 25 MB)"}, 400)
                return self._json(_cen().salva_thumb(q.get("slug", ""), q.get("nome", ""), self.rfile.read(n)))
            if u.path != "/api/upload":
                return self.send_error(404)
            campo, nome = q.get("campo", ""), q.get("nome", "")
            ext = Path(nome).suffix.lower()
            if campo not in EXT_OK or ext not in EXT_OK[campo]:
                return self._json({"ok": False, "erro": f"arquivo não aceito para {campo}: {ext or 'sem extensão'}"}, 400)
            if q.get("ref"):
                pasta = F.REFS / q["ref"]
                reg = F.jl(pasta / "ref.json")
            else:
                pasta = F.FILA / q.get("id", "_")
                reg = F.pedido(q.get("id", "_"))
            if not reg or not (dentro(F.FILA, pasta) or dentro(F.REFS, pasta)):
                return self._json({"ok": False, "erro": "pedido não encontrado"}, 404)
            destino = pasta / f"{campo}{ext}"
            falta = int(self.headers.get("Content-Length") or 0)
            tmp = destino.with_suffix(destino.suffix + ".parte")
            with open(tmp, "wb") as fh:
                while falta > 0:
                    bloco = self.rfile.read(min(1 << 20, falta))
                    if not bloco:
                        break
                    fh.write(bloco)
                    falta -= len(bloco)
            if falta:
                tmp.unlink(missing_ok=True)
                return self._json({"ok": False, "erro": "envio interrompido"}, 400)
            os.replace(tmp, destino)
            with LOCK:
                if q.get("ref"):
                    reg = F.jl(pasta / "ref.json")
                    reg["video"] = destino.name
                    F.grava(pasta / "ref.json", reg)
                else:
                    reg = F.pedido(q["id"])
                    reg["arquivos"][campo] = destino.name
                    reg["arquivos"][campo + "_nome"] = nome[:120]
                    F.salva(reg)
            return self._json({"ok": True, "arquivo": destino.name, "mb": round(destino.stat().st_size / 1e6, 1)})
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        except Exception as ex:  # noqa: BLE001
            self._json({"ok": False, "erro": str(ex)}, 500)

    def do_POST(self):
        if not self._permitido():
            return
        u = urlparse(self.path)
        usar_baia({k: v[0] for k, v in parse_qs(u.query).items()}.get("baia"))
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if u.path.startswith("/api/editai/"):
                origin = self.headers.get("Origin", "")
                host = self.headers.get("Host", "")
                if origin not in ("http://" + host, "https://" + host):
                    return self._json({"ok": False, "erro": "Origem não permitida"}, 403)
                if n > 13_000_000:
                    return self._json({"ok": False, "erro": "Arquivo muito grande"}, 413)
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            if u.path.startswith("/api/editai/"):
                import editai
                handlers = {"/api/editai/canal": editai.save_profile, "/api/editai/preset": editai.save_preset,
                            "/api/editai/config": editai.save_settings, "/api/editai/gerar": editai.generate}
                fn = handlers.get(u.path)
                if not fn: return self._json({"ok": False, "erro": "Ação desconhecida"}, 404)
                with LOCK if u.path != "/api/editai/gerar" else __import__("contextlib").nullcontext():
                    return self._json({"ok": True, "resultado": fn(body)})
            if u.path == "/api/licenca/ativar":
                return self._json(_lic().ativar(body.get("email")))
            if not _lic().ativa():
                return self._json({"ok": False, "erro": "licença inativa", "licenca": True}, 403)
            if u.path == "/api/chaves/salvar":
                import chaves as _ch
                return self._json(_ch.salvar(body))
            if u.path == "/api/motor":
                import motor as _mo
                return self._json(_mo.usar(body.get("motor")))
            if u.path == "/api/gerente":
                return self._json(_esc().gerente(body))
            if u.path == "/api/central/acao":
                return self._json(_cen().executar(body))
            if u.path == "/api/pautas":   # {acao: pesquisar|aprovar|descartar, ...}
                with LOCK:
                    return self._json(_pa().acao_api(body))
            if u.path == "/api/fotos/decidir":
                return self._json(decidir(body))
            if u.path == "/api/linha/rejeitar":
                return self._json(rejeitar(body))
            if u.path == "/api/fila/novo":
                return self._json({"ok": True, "pedido": F.novo(body)})
            if u.path == "/api/fila/roteiro":   # roteiro colado no painel em vez de arquivo
                p = F.pedido(body.get("id") or "_")
                if not p:
                    return self._json({"ok": False, "erro": "pedido não encontrado"})
                (F.FILA / p["id"] / "roteiro.txt").write_text(body.get("texto") or "", "utf-8")
                p["arquivos"]["roteiro"] = "roteiro.txt"
                F.salva(p)
                return self._json({"ok": True})
            if u.path == "/api/config":
                return self._json(config_salvar(body))
            if u.path == "/api/fila/acao":
                return self._json(fila_acao(body))
            if u.path == "/api/limpar":
                return self._json(limpar(body))
            if u.path == "/api/fila/restaurar":
                with LOCK:
                    r = F.restaurar(str(body.get("id") or ""), origem="painel")
                return self._json({**r, **(fila_estado() if r.get("ok") else {})})
            if u.path == "/api/estilos/ref":
                return self._json(ref_nova(body))
            if u.path == "/api/estilos/analisar":
                return self._json(ref_analisar(body))
            if u.path == "/api/estilos/salvar":
                return self._json(estilo_salvar(body))
            if u.path == "/api/estilos/apagar":
                return self._json(estilo_apagar(body))
            self.send_error(404)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass
        except Exception as ex:  # noqa: BLE001
            self._json({"ok": False, "erro": str(ex)}, 500)


def main():
    porta = int(sys.argv[sys.argv.index("--porta") + 1]) if "--porta" in sys.argv else 8876
    # 16/10/2026: "acesso pelo celular" ligado na Central -> escuta na rede (com chave); desligado = só este PC
    try:
        rede = bool(_cen().conf()["remoto"].get("ativo"))
    except Exception:  # noqa: BLE001
        rede = False
    srv = ThreadingHTTPServer(("0.0.0.0" if rede else "127.0.0.1", porta), H)
    if not TESTE:
        try:
            _cen().iniciar_vigia()   # avisos (Windows + celular) quando algo trava
        except Exception as ex:  # noqa: BLE001
            print("[painel] central:", ex)
    srv.daemon_threads = True
    url = f"http://127.0.0.1:{porta}/"
    print(f"[painel] {ROOT.name} -> {url}   (Ctrl+C para fechar)")
    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[painel] fechado")


if __name__ == "__main__":
    main()
