"""ESCRITÓRIO — estado ao vivo dos funcionários para a tela /escritorio (05/10/2026, pedido do usuário).

Nada é inventado: tudo sai de arquivos que o trabalho já grava.
  - painel/gerente_estado.json  (o que cada Diretor/Revisora/juiz do gerente está fazendo, lido do stream do claude.exe)
  - painel/fila/*/pedido.json   (etapa e mensagem de cada filme — vale também quando o Claude do chat trabalha à mão)
  - <ALTA>/.trava_pesado + data/fechar_render.log + out/hybrid/plan.json   (render: quem, etapa, progresso)
  - <ALTA>/fila_render.log      (entregas do dia)
  - ~/.yt_quota.json            (cota do YouTube e pausa)
  - espaço livre do disco C:
O servidor do painel recarrega este arquivo sozinho quando ele muda (como o catalogo.py).
"""
import json, shutil, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRINCIPAL = HERE.parent
ALTA = PRINCIPAL.parent
CONFIG = HERE / "config.json"
import fila as F  # noqa: E402

EQUIPE = [   # id, nome, cargo, cor da roupa, cor do cabelo, pele
    ("dora", "Dora", "Diretora · baia 1", "#c0392b", "#3b2314", "#f1c27d"),
    ("davi", "Davi", "Diretor · baia 2", "#2c6fbb", "#1b1b1b", "#c68642"),
    ("paulo", "Paulo", "Pesquisador", "#27ae60", "#6b4423", "#e0ac69"),
    ("julia", "Júlia", "Juíza de fotos", "#8e44ad", "#a0522d", "#ffdbac"),
    ("bia", "Bia", "Pesquisadora de vídeo", "#e84393", "#1b1b1b", "#c68642"),
    ("vitor", "Vitor", "Juiz de vídeo", "#d35400", "#2b1d0e", "#8d5524"),
    ("rita", "Rita", "Revisora", "#16a085", "#111111", "#c68642"),
    ("renato", "Renato", "Operador de render", "#34495e", "#5a3825", "#f1c27d"),
]
DIRETOR_DA_BAIA = {"b1": "dora", "b2": "davi"}
ETAPA_PAPEL = {"preparando": "diretor", "roteiro": "diretor", "material": "paulo", "julgar_fotos": "julia",
               "montagem": "diretor", "julgar_cortes": "vitor", "render": "renato", "conferir": "rita"}
ETAPA_NOME = {"preparando": "preparando", "roteiro": "lendo o roteiro", "material": "buscando material",
              "julgar_fotos": "julgando fotos", "montagem": "montando", "julgar_cortes": "julgando cortes",
              "render": "renderizando", "conferir": "conferindo", "entregue": "entregue"}


AMIGAVEL = [   # comando/arquivo -> o que o funcionário está fazendo, em português
    (r"fetch_images_cat|fetch_images", "buscando fotos no Wikimedia"), (r"fetch_photos_api|fetch_stock_api", "buscando no Pexels"),
    (r"fetch_dvids", "buscando vídeo militar (DVIDS)"), (r"fetch_video|yt_lista", "procurando vídeos no YouTube"),
    (r"yt_probe|probe_sheet", "assistindo os vídeos candidatos"), (r"yt_win_dl|yt_quando_liberar", "baixando trechos do YouTube"),
    (r"photo_dl", "baixando fotos"), (r"prefilter", "filtrando fotos repetidas"), (r"photo_sheet", "montando folhas de contato"),
    (r"juizes\.py preparar", "separando os lotes para os juízes"), (r"juizes\.py juntar", "juntando os votos dos juízes"),
    (r"juizes\.py conferir", "conferindo as fotos aprovadas"), (r"juizes\.py tirar", "tirando fotos ruins"),
    (r"novo_filme", "transcrevendo a narração"), (r"esqueleto_tema", "lendo o roteiro"), (r"_tema_", "escrevendo o tema do filme"),
    (r"beats\.py", "dividindo o filme em cenas"), (r"_dossie", "escrevendo os cartões"), (r"remapa", "remanejando cenas"),
    (r"build_plan|build_overlays", "montando a linha do tempo"), (r"fechar\.py preparar", "montando e checando o filme"),
    (r"paralaxe", "preparando fotos em 3D"), (r"make_photos", "recortando as fotos"), (r"make_clips|source_review", "cortando os clipes"),
    (r"make_thumb", "fazendo as miniaturas"), (r"music_mix|audio_probe", "mixando a trilha"),
    (r"render_e_entrega|fechar\.py render", "mandando para o render"), (r"fila\.py estado", "atualizando o painel"),
    (r"fila\.py (baia|preparar|aplicar)|baias\.py", "arrumando a baia"), (r"ffmpeg|ffprobe", "conferindo um vídeo"),
    (r"PIPELINE\.md|MEMORY\.md|memory", "relendo o manual"), (r"roteiro|script\.txt|master_transcript", "lendo o roteiro"),
    (r"timeline\.json", "olhando a linha do tempo"), (r"_conferencia_|cortes_|final_mp4|suspeitos", "conferindo as folhas"),
    (r"lote_\d+\.md", "lendo as regras do lote"), (r"sheet_\d+", "olhando uma folha de fotos"),
]


def amigavel(txt, cmd=""):
    import re
    alvo = f"{cmd} {txt}"
    m = re.search(r"photos[\\/]+([a-z0-9_]+?)_\d+\.jpg", alvo, re.I)
    if m:
        return f"julgando as fotos de “{m.group(1).replace('_', ' ')}”"
    m = re.search(r"probe(?:1|_api)[\\/]+sheet_(\d+)", alvo, re.I)
    if m:
        return f"assistindo os vídeos da folha {int(m.group(1)) + 1}"
    for pad, frase in AMIGAVEL:
        if re.search(pad, alvo):
            return frase
    txt = (txt or "").strip()
    if not txt or txt.startswith(("cd ", "python", "bash", "ls", "cat ", "grep", "PYTHONIOENCODING")) or "/" in txt[:40] or "\\" in txt[:40]:
        return "trabalhando no terminal"
    return txt


def jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def pasta_baia(b):
    return PRINCIPAL if b == "b1" else ALTA / "baias" / b


def titulo_curto(p):
    t = (p or {}).get("titulo") or (p or {}).get("id", "")
    return t[:40]


def render_info(agora):
    tr = jl(ALTA / ".trava_pesado", None)
    if not tr:
        return None
    baia = tr.get("baia") or "b1"
    b = "b1" if baia in ("EditAI", "b1") else baia
    pasta = pasta_baia(b)
    linhas = []
    try:
        linhas = [l for l in (pasta / "data" / "fechar_render.log").read_text("utf-8", "replace").splitlines() if l.strip()]
    except Exception:  # noqa: BLE001
        pass
    plano = jl(pasta / "out" / "hybrid" / "plan.json", {})
    segs = plano.get("segments", []) if isinstance(plano, dict) else []
    feitos = sum(1 for s in segs if (pasta / "out" / "hybrid" / (s["name"] + ".mp4")).exists())
    fase = "acabamento" if any("acabamento" in l for l in linhas[-3:]) else "render"
    pct = int(100 * feitos / len(segs)) if segs and fase == "render" else None
    filme = next((p for p in F.todos() if p.get("baia") == b and p.get("status") in ("produzindo", "esperando_voce")), None)
    return {"baia": b, "etapa": tr.get("etapa", ""), "fase": fase, "pct": pct, "segs": f"{feitos}/{len(segs)}" if segs else "",
            "linha": (linhas[-1].strip()[:110] if linhas else ""), "filme": titulo_curto(filme),
            "desde": tr.get("desde")}


def yt_info(agora):
    st = jl(Path.home() / ".yt_quota.json", {})
    calls = [t for t in st.get("calls", []) if isinstance(t, (int, float)) and agora - t < 86400]
    pausa = 0
    if agora - st.get("blocked_at", 0) < 3 * 3600:
        pausa = (3 * 3600 - (agora - st["blocked_at"])) / 60
    elif len(calls) >= 160 and calls:
        pausa = (86400 - (agora - min(calls))) / 60
    return {"usadas": len(calls), "teto": 160, "pausa_min": round(pausa)}


def entregues_hoje():
    hoje = []
    try:
        for l in (ALTA / "fila_render.log").read_text("utf-8", "replace").splitlines():
            if l.endswith("ENTREGUE") and len(l) > 6 and l[2] == ":":
                hoje.append({"hora": l[:5], "slug": l[6:-9].strip()})
    except Exception:  # noqa: BLE001
        pass
    return hoje[-8:]


def estado():
    agora = time.time()
    cfg = jl(CONFIG, {})
    ger = jl(HERE / "gerente_estado.json", {})
    try:
        ger_vivo = agora - float((HERE / ".gerente_vivo").read_text()) < 30
    except Exception:  # noqa: BLE001
        ger_vivo = False
    pedidos = F.todos()
    por_id = {p["id"]: p for p in pedidos}
    pess = {i: {"id": i, "nome": n, "cargo": c, "roupa": r, "cabelo": h, "pele": k, "estado": "livre",
                "txt": "", "filme": "", "desde": None} for i, n, c, r, h, k in EQUIPE}
    ajud = []

    def poe(pid, estado_, txt, filme="", prior=1):
        cur = pess[pid]
        if cur.get("_prior", 0) > prior:
            return
        cur.update(estado=estado_, txt=txt[:140], filme=filme, _prior=prior)

    # 1) o que o gerente está vendo nas sessões do claude.exe (o mais preciso)
    for sid, s in (ger.get("sessoes") or {}).items():
        if s.get("fim"):
            continue
        p = por_id.get(s.get("pedido"), {})
        filme = titulo_curto(p)
        if s.get("papel") == "diretor":
            dono = DIRETOR_DA_BAIA.get(s.get("baia"), "dora")
            area = s.get("area", "mesa")
            if area == "pesquisa" and agora - s.get("t", 0) < 300:
                poe("paulo", "trabalhando", amigavel(s.get("txt", ""), s.get("cmd", "")), filme, 3)
                poe(dono, "esperando", "esperando o Paulo trazer o material", filme, 3)
            else:
                poe(dono, "trabalhando", amigavel(s.get("txt", ""), s.get("cmd", "")) if s.get("txt") else "pensando", filme, 3)
        elif s.get("papel") == "revisora":
            poe("rita", "trabalhando", amigavel(s.get("txt", ""), s.get("cmd", "")) if s.get("txt") else "conferindo o MP4", filme, 3)
        elif s.get("papel") in ("pesquisador", "roteirista", "analista", "modelador"):   # 07/10/2026: pautas (painel/pautas.py)
            base = {"pesquisador": "garimpando pautas na gringa", "roteirista": "escrevendo o roteiro",
                    "analista": "analisando o tema do usuário",
                    "modelador": "buscando vídeos do mesmo modelo"}[s["papel"]]
            poe("paulo", "trabalhando", amigavel(s.get("txt", ""), s.get("cmd", "")) if s.get("txt") else base,
                s.get("titulo_pauta", ""), 3)
        for aid, a in (s.get("ajudantes") or {}).items():
            if a.get("fim"):
                continue
            tipo = a.get("tipo", "")
            quem = {"juiz-fotos": "julia", "juiz-video": "vitor", "revisora": "rita", "pesquisador": "paulo"}.get(tipo)
            if tipo == "juiz-fotos":
                ajud.append({"cargo": "Juiz de fotos", "txt": amigavel(a.get("txt") or a.get("desc", "")), "filme": filme})
            if quem:
                poe(quem, "trabalhando", amigavel(a.get("txt") or a.get("desc", "")), filme, 3)
    # 2) fila do painel (vale para o trabalho feito à mão pelo Claude do chat)
    for p in pedidos:
        st, et, b = p.get("status"), p.get("etapa") or "", p.get("baia")
        if st not in ("produzindo", "esperando_voce", "pausado") or not b:
            continue
        dono = DIRETOR_DA_BAIA.get(b, "dora")
        filme = titulo_curto(p)
        if st == "esperando_voce":
            poe(dono, "travado", p.get("msg") or "precisa de você", filme, 4)
            continue
        papel = ETAPA_PAPEL.get(et, "diretor")
        if papel == "diretor":
            poe(dono, "trabalhando", p.get("msg") or ETAPA_NOME.get(et, et), filme, 2)
        else:
            poe(papel, "trabalhando", p.get("msg") or ETAPA_NOME.get(et, et), filme, 2)
            poe(dono, "esperando", f"esperando: {ETAPA_NOME.get(et, et)}", filme, 2)
    # juízes à mão (lote_K.md sem resposta numa baia em julgar_fotos)
    for b in ("b1", "b2"):
        j = pasta_baia(b) / "data" / "juizes"
        if j.exists():
            for md in j.glob("lote_*.md"):
                k = md.stem.split("_")[1]
                if not (j / f"lote_{k}.json").exists() and agora - md.stat().st_mtime < 3600:
                    ajud.append({"cargo": "Juiz de fotos", "txt": f"julgando o lote {k}", "filme": ""})
                    poe("julia", "trabalhando", "coordenando os juízes", "", 2)
    # 2b) Bia — busca de vídeo em paralelo (baias/_ferramentas/busca_video.sh grava data/busca_video.estado)
    for b in ("b1", "b2"):
        est_b = jl(pasta_baia(b) / "data" / "busca_video.estado", None)
        if not est_b:
            continue
        idade = agora - est_b.get("t", 0)
        filme = titulo_curto(next((p for p in pedidos if p.get("baia") == b and p.get("status") in ("produzindo", "esperando_voce")), None))
        pronto = (pasta_baia(b) / "data" / "busca_video.ok").exists()
        if not pronto and idade < 2700:
            yt = yt_info(agora)
            if yt["pausa_min"] and "YouTube" in est_b.get("etapa", ""):
                poe("bia", "esperando", f"YouTube em pausa ({yt['pausa_min']} min)", filme, 4)
            else:
                poe("bia", "trabalhando", est_b.get("etapa", "buscando vídeos"), filme, 4)
        elif pronto and idade < 1200:
            poe("bia", "esperando", "folhas de vídeo prontas para o Vitor", filme, 3)
    # 3) render
    ren = render_info(agora)
    if ren:
        txt = f"{ren['fase']} {ren['segs']}" + (f" ({ren['pct']}%)" if ren["pct"] is not None else "")
        poe("renato", "trabalhando", txt, ren["filme"], 5)
    ent = entregues_hoje()
    log_mt = (ALTA / "fila_render.log").stat().st_mtime if (ALTA / "fila_render.log").exists() else 0
    if not ren and ent and agora - log_mt < 240:
        poe("renato", "entregando", f"levando {ent[-1]['slug']} para ENTREGAS", "", 5)
    # 4) recursos que travam o trabalho
    yt = yt_info(agora)
    try:
        livre = shutil.disk_usage("C:/").free / 1e9
    except Exception:  # noqa: BLE001
        livre = 999
    if livre < 15:
        poe("renato", "travado", f"disco quase cheio: {livre:.0f} GB livres", "", 9)
    if yt["pausa_min"] and pess["paulo"]["estado"] == "trabalhando" and "youtube" in pess["paulo"]["txt"].lower():
        poe("paulo", "esperando", f"YouTube em pausa ({yt['pausa_min']} min)", pess["paulo"]["filme"], 9)
    for v in pess.values():
        v.pop("_prior", None)
        if v["estado"] == "livre":
            v["txt"] = "tomando café"
    fila_vis = [{"titulo": titulo_curto(p), "status": p.get("status"), "etapa": ETAPA_NOME.get(p.get("etapa") or "", p.get("etapa") or ""),
                 "baia": p.get("baia"), "pct": p.get("pct", 0)}
                for p in sorted(pedidos, key=lambda p: p.get("criado", ""), reverse=True)
                if p.get("status") in ("na_fila", "produzindo", "esperando_voce", "pausado", "enviando")][:8]
    return {"agora": agora, "gerente": {"ligado": bool(cfg.get("gerente")), "vivo": ger_vivo},
            "funcionarios": list(pess.values()), "ajudantes": ajud[:4], "fila": fila_vis, "entregues": ent,
            "render": ren, "recursos": {"disco_gb": round(livre), "yt": yt},
            "feed": list(reversed((ger.get("feed") or [])[-14:]))}


def gerente(body):
    cfg = jl(CONFIG, {})
    cfg["gerente"] = bool(body.get("ligado"))
    tmp = CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), "utf-8")
    tmp.replace(CONFIG)
    F.evento("gerente", None, ligado=cfg["gerente"])
    return {"ok": True, "ligado": cfg["gerente"]}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(estado(), ensure_ascii=False, indent=1)[:3000])
