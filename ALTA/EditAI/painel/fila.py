"""FILA DE FILMES + ponte painel <-> Claude (27/09/2026, pedido do usuário).

O painel cria os pedidos (painel/fila/<id>/pedido.json + roteiro + áudio) e registra cada clique em
painel/eventos.jsonl. O Claude vigia os eventos (painel/vigia.py dentro do Monitor) e produz; a cada etapa ele
atualiza o pedido com `fila.py estado`, e o painel mostra ao vivo.

Comandos (para o Claude):
  python painel/fila.py lista                          # a fila, na ordem
  python painel/fila.py proximo                        # id do próximo "na_fila" (vazio = nada)
  python painel/fila.py preparar ID                    # roteiro/áudio -> input/ (converte p/ mp3; "voz limpa" se pedida)
  python painel/fila.py aplicar ID                     # opções do painel -> data/pipeline_config.json (DEPOIS do novo_filme)
  python painel/fila.py estado ID ETAPA [--status S] [--msg "texto"] [--pct N]
  python painel/fila.py recados ID                     # recados do usuário ainda não lidos (e marca como lidos)
  python painel/fila.py mostrar ID                     # o pedido inteiro
  python painel/fila.py baia ID bN                     # registra a baia do filme (ver painel/baias.py)
  pedido["auto"] = modo automático: o Claude julga fotos e cortes e segue sem esperar o usuário
  python painel/fila.py ref RID [--status analisando|pronto|erro] [--msg "texto"] [--estilo slug]   # vídeo de referência
  python painel/fila.py limpar --simular               # prévia: pedidos entregue/cancelado + pastas APAGAR_* (GB)
  python painel/fila.py limpar [--confirmar]           # arquiva os concluídos em painel/fila_arquivo/ e manda cada
                                                       # APAGAR_* (raiz da b1 e de baias/bN) para a LIXEIRA do Windows
                                                       # (recuperável; esvaziar a Lixeira libera o espaço). = botão
                                                       # "Limpar concluídos" do painel. Evento "limpeza" (só aviso).
  python painel/fila.py arquivados                     # pedidos arquivados
  python painel/fila.py restaurar ID                   # devolve um pedido arquivado para a fila
Referência (identificador de edição): painel/referencias/RID/{ref.json, video.*} -> scripts/identifica_estilo.py
  painel/referencias/RID/video.mp4 painel/referencias/RID --gravar slug "Nome" -> o Claude olha as folhas e revisa
  painel/estilos/slug.json (escolhas, liga, analise, revisado: true).
ETAPAS: preparando roteiro material julgar_fotos montagem julgar_cortes render conferir entregue
STATUS: enviando na_fila produzindo esperando_voce pausado entregue erro cancelado
"""
import json, os, re, shutil, subprocess, sys, time, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent   # a BAIA onde este fila.py está (input/, data/ do filme)
# 28/09: numa baia (<ALTA PRODUÇÃO>/baias/bN/painel) a fila, os eventos e as referências continuam os da b1
CENTRAL = (ROOT.parent.parent / "EditAI" / "painel") if ROOT.parent.name == "baias" else HERE
FILA = CENTRAL / "fila"
EVENTOS = CENTRAL / "eventos.jsonl"
sys.path.insert(0, str(HERE))

ETAPAS = [
    ("preparando", "Preparando", "áudio, duração e transcrição (GPU)"),
    ("roteiro", "Roteiro", "blocos, tags e buscas de imagem"),
    ("material", "Material", "fotos e vídeos baixados e pré-filtrados"),
    ("julgar_fotos", "Julgar fotos", "sua vez: aba Fotos"),
    ("montagem", "Montagem", "cenas, cartões, plano e QA"),
    ("julgar_cortes", "Julgar cortes", "sua vez: aba Linha do tempo"),
    ("render", "Render", "vídeo, acabamento, legendas e áudio"),
    ("conferir", "Conferir", "folha do MP4 final e miniaturas"),
    ("entregue", "Entregue", "pasta em entregas/"),
]
STATUS = ["enviando", "na_fila", "produzindo", "esperando_voce", "pausado", "entregue", "erro", "cancelado"]


def agora():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40] or "filme"


def jl(p, d=None):
    p = Path(p)
    try:
        return json.loads(p.read_text("utf-8-sig")) if p.exists() else d
    except Exception:  # noqa: BLE001
        return d


def grava(p, obj):
    p = Path(p)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    for k in range(10):
        try:
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.1 * (k + 1))


def pedido(pid):
    return jl(FILA / pid / "pedido.json")


def salva(p):
    grava(FILA / p["id"] / "pedido.json", p)


def todos():
    ps = [jl(d / "pedido.json") for d in FILA.glob("*") if (d / "pedido.json").exists()] if FILA.exists() else []
    ps = [p for p in ps if p]
    return sorted(ps, key=lambda p: (p.get("ordem", 0), p.get("criado", "")))


def evento(tipo, pid=None, **dados):
    n = sum(1 for _ in EVENTOS.open("r", encoding="utf-8")) if EVENTOS.exists() else 0
    e = {"n": n + 1, "ts": agora(), "tipo": tipo, "id": pid, **dados}
    with EVENTOS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def novo(dados):
    FILA.mkdir(parents=True, exist_ok=True)
    pid = time.strftime("%Y%m%d-%H%M%S-") + slug(dados.get("titulo") or "filme")
    import catalogo
    cfg = catalogo.config_de(dados.get("escolhas") or {}, dados.get("liga") or {})
    # Respeita a proporção escolhida no painel, inclusive 0% e 100%.
    proporcao = float(dados.get("photo_share") if dados.get("photo_share") is not None else 0.8)
    if not 0 <= proporcao <= 1:
        raise ValueError("A proporção de fotos deve estar entre 0 e 1.")
    cfg = catalogo.mescla(cfg, {"screenLanguage": dados.get("idioma") or "pt",
                                "photo_share": proporcao,
                                "modo": dados.get("modo") or "padrao"})
    # 06/11/2026 FORMATO: "longo" (16:9, o de sempre) | "short" (1-2 min, mesmos estilos, sai 9:16 inteiro no fim do
    # render pelo scripts/shorts.py --inteiro) | "short3d" (curta animada 3D na pasta claude-shorts-3d, prompts/short3d.md)
    if dados.get("formato") == "short3d":
        raise ValueError("O Short 3D foi desativado nesta versão.")
    formato = dados.get("formato") if dados.get("formato") == "short" else "longo"
    if formato == "short":
        cfg = catalogo.mescla(cfg, {"legendas": {"estilo": "off"},          # a legenda de impacto vem no 9:16
                                    "entrega": {"shorts": 1, "short_inteiro": True,
                                                "short_titulo": (dados.get("titulo") or "")[:60]}})
    p = {"id": pid, "titulo": dados.get("titulo") or "Filme sem título", "criado": agora(),
         "idioma": dados.get("idioma") or "pt", "photo_share": proporcao,
         "modo": dados.get("modo") or "padrao", "estilo": dados.get("estilo"), "escolhas": dados.get("escolhas") or {},
         "liga": dados.get("liga") or {}, "config": cfg, "observacoes": (dados.get("observacoes") or "")[:4000],
         "canal": dados.get("canal") or "", "arquivos": {}, "formato": formato,
         "auto": bool(dados["auto"]) if "auto" in dados else bool(jl(CENTRAL / "config.json", {}).get("auto")), "baia": None, "status": "enviando", "etapa": None, "msg": "enviando arquivos…",
         "pct": 0, "historico": [], "recados": [], "ordem": max([x.get("ordem", 0) for x in todos()] + [0]) + 1}
    (FILA / pid).mkdir(parents=True, exist_ok=True)
    salva(p)
    return p


def estado(pid, etapa=None, status=None, msg=None, pct=None):
    p = pedido(pid)
    if not p:
        sys.exit(f"pedido {pid} não existe")
    if etapa:
        p["etapa"] = etapa
    if status:
        p["status"] = status
    if msg is not None:
        p["msg"] = msg
    if pct is not None:
        p["pct"] = int(pct)
    p["atualizado"] = agora()
    p["historico"].append({"ts": agora(), "etapa": p.get("etapa"), "status": p["status"], "msg": p.get("msg")})
    p["historico"] = p["historico"][-200:]
    salva(p)
    return p


def preparar(pid):
    """Leva roteiro e narração do pedido para input/ (o novo_filme.py lê input/script.txt + input/audio.mp3)."""
    p = pedido(pid)
    d = FILA / pid
    rot = d / p["arquivos"].get("roteiro", "roteiro.txt")
    aud = d / p["arquivos"].get("audio", "")
    if not rot.exists() or not aud.is_file():
        sys.exit(f"faltam arquivos no pedido: roteiro={rot.exists()} audio={aud.is_file()}")
    inp = ROOT / "input"
    inp.mkdir(exist_ok=True)
    shutil.copy2(rot, inp / "script.txt")
    af = []
    if (p.get("config") or {}).get("voz_limpa"):   # tira chiado de fundo e sibilância, sem mexer no volume
        af = ["-af", "highpass=f=70,afftdn=nr=10:nf=-40:tn=1,deesser=i=0.35"]
    if aud.suffix.lower() == ".mp3" and not af:
        shutil.copy2(aud, inp / "audio.mp3")
    else:
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(aud), *af, "-c:a", "libmp3lame",
                        "-b:a", "320k", str(inp / "audio.mp3")], check=True)
    print(f"[fila] {pid}: input/script.txt + input/audio.mp3 prontos"
          + (" (voz limpa)" if af else "") + f" | depois: novo_filme.py --lang {p['idioma']} --foto {p['photo_share']}")


def aplicar(pid):
    """Mescla as opções do pedido no data/pipeline_config.json (rodar DEPOIS do novo_filme.py, que reescreve idioma/foto)."""
    import catalogo
    p = pedido(pid)
    # 05/10/2026: aplicar grava na baia DESTE fila.py; rodar o da b1 para um pedido da b2/b3 sobrescreveu a config do
    # filme da b1 (Subaru renderizando com a trilha do filme anterior). Agora recusa baia diferente da registrada.
    esta = ROOT.name if ROOT.parent.name == "baias" else "b1"
    if p.get("baia") and p["baia"] != esta:
        sys.exit(f"[fila] PAROU: o pedido {pid} é da baia {p['baia']}, mas este fila.py é da {esta} — rode o painel/fila.py "
                 f"de dentro da baia {p['baia']}")
    cp = ROOT / "data" / "pipeline_config.json"
    cfg = catalogo.mescla(jl(cp, {}), p["config"])
    # 26/10/2026: "lang" ficava com o idioma do filme anterior (Recife pt herdou "es" do Catar)
    cfg["lang"] = p.get("idioma") or cfg.get("screenLanguage") or cfg.get("lang")
    grava(cp, cfg)
    print(json.dumps({k: cfg.get(k) for k in ("screenLanguage", "photo_share", "modo", "music", "sfx", "legendas", "acabamento",
                                               "estilo_destaque", "arquivo_dark", "paralaxe", "mapa", "render", "voz_limpa")},
                     ensure_ascii=False, indent=1))


def recados(pid):
    p = pedido(pid)
    novos = [r for r in p.get("recados", []) if not r.get("lido")]
    for r in novos:
        r["lido"] = agora()
        print(f"[{r['ts']}] {r['texto']}")
    if novos:
        salva(p)
    else:
        print("(nenhum recado novo)")


REFS = CENTRAL / "referencias"


def ref_estado(rid, status=None, msg=None, estilo=None):
    p = REFS / rid / "ref.json"
    r = jl(p)
    if not r:
        sys.exit(f"referência {rid} não existe")
    if status:
        r["status"] = status
    if msg is not None:
        r["msg"] = msg
    if estilo:
        r["estilo"] = estilo
    r["atualizado"] = agora()
    grava(p, r)
    return r


# ---------------------------------------------------------------- limpeza (29/09/2026, botão "Limpar concluídos")
# Só mexe em duas coisas: (1) pastas painel/fila/<id> com status entregue/cancelado -> MOVIDAS para painel/fila_arquivo/
# (têm roteiro e áudio de origem; nada é apagado) e (2) pastas cujo nome começa com "APAGAR_" no 1º nível da b1 e de
# <ALTA PRODUÇÃO>/baias/bN -> Lixeira do Windows (recuperável). Nunca entregas/, data/, public/, scripts/ nem a baia.
ARQUIVO = CENTRAL / "fila_arquivo"
CONCLUIDOS = ("entregue", "cancelado")
APAGAR_RAIZES = None   # None = b1 + baias/bN; o servidor em modo --dados troca por uma pasta de teste


def raizes_apagar():
    if APAGAR_RAIZES is not None:
        return [Path(r) for r in APAGAR_RAIZES]
    b1 = CENTRAL.parent
    base = b1.parent / "baias"
    bs = sorted((d for d in base.iterdir() if d.is_dir() and re.fullmatch(r"b\d+", d.name)),
                key=lambda d: int(d.name[1:])) if base.is_dir() else []
    return [b1, *bs]


def _nome_raiz(r):
    return r.name if r.parent.name == "baias" else "b1"


def _eh_link(p):
    try:
        return p.is_symlink() or p.is_junction()
    except (OSError, AttributeError):
        return p.is_symlink()


def _apagar_ok(d, raiz):
    """Trava de segurança: pasta de verdade (não atalho/junction), nome começando EXATAMENTE com APAGAR_, e filha
    direta de uma das raízes. Qualquer outra coisa fica de fora."""
    try:
        return (d.name.startswith("APAGAR_") and d.is_dir() and not _eh_link(d)
                and d.resolve().parent == Path(raiz).resolve())
    except OSError:
        return False


def pastas_apagar():
    out = []
    for r in raizes_apagar():
        try:
            filhos = sorted(r.iterdir()) if r.is_dir() else []
        except OSError:
            continue
        out += [(d, r) for d in filhos if d.name.startswith("APAGAR_") and _apagar_ok(d, r)]
    return out


def concluidos():
    out = []
    if not FILA.exists():
        return out
    for d in sorted(FILA.iterdir()):
        p = jl(d / "pedido.json") if d.is_dir() and not _eh_link(d) else None
        if p and p.get("status") in CONCLUIDOS:
            out.append((d, p))
    return out


def tamanho(p):
    """Bytes de uma pasta (sem seguir atalhos/junctions)."""
    tot, pilha = 0, [str(p)]
    while pilha:
        try:
            with os.scandir(pilha.pop()) as it:
                for e in it:
                    try:
                        if e.is_symlink() or (hasattr(e, "is_junction") and e.is_junction()):
                            continue
                        if e.is_dir(follow_symlinks=False):
                            pilha.append(e.path)
                        elif e.is_file(follow_symlinks=False):
                            tot += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return tot


def gb(n):
    return round(n / 1024 ** 3, 2)


def lixeira_info(p):
    """Tamanho máximo da Lixeira na unidade de p (registro do Windows). Pasta maior que isso o Windows apagaria de vez
    em vez de reciclar — então essa pasta é bloqueada. None = não deu para ler."""
    try:
        import ctypes, winreg
        k32 = ctypes.windll.kernel32
        raiz, vol = ctypes.create_unicode_buffer(300), ctypes.create_unicode_buffer(300)
        if not k32.GetVolumePathNameW(str(p), raiz, 300) or not k32.GetVolumeNameForVolumeMountPointW(raiz.value, vol, 300):
            return None
        guid = re.search(r"\{[0-9A-Fa-f-]+\}", vol.value).group(0)
        chave = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\BitBucket\\Volume\\" + guid
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave) as k:
            cap = int(winreg.QueryValueEx(k, "MaxCapacity")[0])
            try:
                nuke = int(winreg.QueryValueEx(k, "NukeOnDelete")[0])
            except OSError:
                nuke = 0
        return {"unidade": raiz.value, "cap_bytes": cap * 1024 * 1024, "cap_gb": gb(cap * 1024 * 1024), "nuke": bool(nuke)}
    except Exception:  # noqa: BLE001
        return None


def limpeza_contagem():
    """Rápida (sem tamanhos) — o painel pergunta a cada 3 s para ligar/desligar o botão."""
    n_arq = sum(1 for d in ARQUIVO.iterdir() if (d / "pedido.json").exists()) if ARQUIVO.exists() else 0
    return {"pedidos": len(concluidos()), "pastas": len(pastas_apagar()), "arquivados": n_arq}


def limpeza_previa():
    ped = [{"id": d.name, "titulo": p.get("titulo") or d.name, "status": p["status"], "bytes": tamanho(d),
            "gb": 0} for d, p in concluidos()]
    info_cache, pastas, avisos = {}, [], []
    for d, r in pastas_apagar():
        b = tamanho(d)
        dr = d.drive.upper()
        if dr not in info_cache:
            info_cache[dr] = lixeira_info(d)
        li = info_cache[dr]
        bloq = None
        if li and li["nuke"]:
            bloq = "a Lixeira desta unidade está configurada para apagar direto (Propriedades da Lixeira)"
        elif li and b > li["cap_bytes"] * 0.95:
            bloq = f"maior que a Lixeira da unidade ({li['cap_gb']} GB): o Windows apagaria de vez"
        pastas.append({"caminho": str(d), "nome": d.name, "baia": _nome_raiz(r), "bytes": b, "gb": gb(b), "bloqueada": bloq})
    for x in ped:
        x["gb"] = gb(x["bytes"])
    tot = sum(x["bytes"] for x in pastas if not x["bloqueada"])
    for dr, li in info_cache.items():
        if li is None:
            avisos.append(f"não consegui ler o tamanho da Lixeira em {dr}")
        elif tot > li["cap_bytes"]:
            avisos.append(f"o total ({gb(tot)} GB) passa do tamanho da Lixeira ({li['cap_gb']} GB): ao entrar as últimas "
                          "pastas, o Windows descarta da Lixeira os itens mais antigos (inclusive as primeiras pastas desta limpeza)")
    return {"pedidos": ped, "pastas": pastas, "bytes_pedidos": sum(x["bytes"] for x in ped),
            "gb_pedidos": gb(sum(x["bytes"] for x in ped)), "bytes_liberados": tot, "gb_liberados": gb(tot),
            "avisos": avisos, "lixeira": {k: v for k, v in info_cache.items() if v}}


def para_lixeira(p):
    """Manda UMA pasta para a Lixeira do Windows (recuperável). O caminho vai por variável de ambiente, então Ç,
    espaços e aspas não precisam de escape no comando."""
    p = Path(p)
    cmd = ("$ErrorActionPreference='Stop'; Add-Type -AssemblyName Microsoft.VisualBasic; "
           "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($env:PAINEL_LIXEIRA_ALVO, 'OnlyErrorDialogs', "
           "'SendToRecycleBin')")
    try:
        r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                           env={**os.environ, "PAINEL_LIXEIRA_ALVO": str(p)}, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=3600,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except Exception as ex:  # noqa: BLE001
        return str(ex)
    if r.returncode != 0:
        txt = (r.stderr or r.stdout or "").strip()
        return (txt.splitlines()[0][:300] if txt else f"PowerShell saiu com código {r.returncode}")
    if p.exists():
        return "a pasta continua no lugar (algum arquivo em uso?)"
    return None


def limpar(pedidos=None, pastas=None, origem="terminal"):
    """Executa. pedidos/pastas = o que a pessoa VIU na prévia (ids / caminhos); None = tudo o que a prévia achar agora.
    Tudo é conferido de novo aqui (status atual e trava APAGAR_) — o que mudou desde a prévia fica de fora."""
    feitos_ped, feitos_pas, erros = [], [], []
    ARQUIVO.mkdir(parents=True, exist_ok=True)
    for d, p in concluidos():
        if pedidos is not None and d.name not in pedidos:
            continue
        p2 = jl(d / "pedido.json")   # relê: o Claude pode ter mexido desde a prévia
        if not p2 or p2.get("status") not in CONCLUIDOS:
            continue
        dest = ARQUIVO / d.name
        k = 2
        while dest.exists():
            dest = ARQUIVO / f"{d.name}-{k}"
            k += 1
        try:
            p2["arquivado"] = agora()
            grava(d / "pedido.json", p2)
            os.rename(d, dest)   # mesma unidade: só troca de pasta (sem cópia, sem apagar nada)
            feitos_ped.append(d.name)
        except OSError as ex:
            p2.pop("arquivado", None)
            try:
                grava(d / "pedido.json", p2)
            except OSError:
                pass
            erros.append({"item": d.name, "erro": f"não arquivou: {ex}"})
    liberado = 0
    prev = {x["caminho"]: x for x in limpeza_previa()["pastas"]} if (pastas is None or pastas) else {}
    for d, r in pastas_apagar():
        if pastas is not None and str(d) not in pastas:
            continue
        x = prev.get(str(d))
        if not x or x["bloqueada"]:
            erros.append({"item": d.name, "erro": (x or {}).get("bloqueada") or "fora da prévia"})
            continue
        if not _apagar_ok(d, r):   # trava de novo, logo antes de mexer
            erros.append({"item": d.name, "erro": "não passou na trava APAGAR_"})
            continue
        e = para_lixeira(d)
        if e:
            erros.append({"item": f"{x['baia']}/{d.name}", "erro": e})
        else:
            feitos_pas.append(f"{x['baia']}/{d.name}")
            liberado += x["bytes"]
    evento("limpeza", None, acao="limpar", origem=origem, arquivados=feitos_ped, lixeira=feitos_pas,
           gb_lixeira=gb(liberado), erros=erros)
    return {"ok": not erros, "arquivados": feitos_ped, "lixeira": feitos_pas, "gb_lixeira": gb(liberado), "erros": erros}


def arquivados():
    out = []
    for d in (ARQUIVO.iterdir() if ARQUIVO.exists() else []):
        p = jl(d / "pedido.json")
        if p:
            out.append({"pasta": d.name, "id": p.get("id"), "titulo": p.get("titulo"), "status": p.get("status"),
                        "idioma": p.get("idioma"), "criado": p.get("criado"), "arquivado": p.get("arquivado"),
                        "msg": p.get("msg"), "pode_voltar": not (FILA / d.name).exists()})
    return sorted(out, key=lambda x: x.get("arquivado") or "", reverse=True)


def restaurar(pasta, origem="terminal"):
    src = ARQUIVO / pasta
    if not pasta or "/" in pasta or "\\" in pasta or pasta.startswith(".") or not (src / "pedido.json").exists():
        return {"ok": False, "erro": "pedido arquivado não encontrado"}
    dest = FILA / pasta
    if dest.exists():
        return {"ok": False, "erro": "já existe um pedido com esse id na fila"}
    FILA.mkdir(parents=True, exist_ok=True)
    os.rename(src, dest)
    p = jl(dest / "pedido.json")
    if p:
        p.pop("arquivado", None)
        grava(dest / "pedido.json", p)
    evento("limpeza", pasta, acao="restaurar", origem=origem, titulo=(p or {}).get("titulo"))
    return {"ok": True, "id": pasta}


def _imprime_previa(pv):
    print(f"Filmes concluídos (arquivar em painel/fila_arquivo/): {len(pv['pedidos'])} · {pv['gb_pedidos']} GB (só muda de pasta)")
    for x in pv["pedidos"]:
        print(f"  {x['gb']:>7.2f} GB  {x['status']:<10} {x['id']}  {x['titulo']}")
    print(f"Material pesado para a Lixeira (APAGAR_*): {len(pv['pastas'])} · {pv['gb_liberados']} GB liberados")
    for x in pv["pastas"]:
        print(f"  {x['gb']:>7.2f} GB  {x['baia']:<3} {x['nome']}" + (f"   BLOQUEADA: {x['bloqueada']}" if x["bloqueada"] else ""))
    for a in pv["avisos"]:
        print("AVISO:", a)
    print("As pastas vão para a Lixeira do Windows; esvazie a Lixeira para liberar o espaço.")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    c = a[0]
    if c == "lista":
        for p in todos():
            print(f"{p['ordem']:>3} {p['id']:<45} {p['status']:<15} {p.get('etapa') or '-':<14} {p['titulo']}")
    elif c == "proximo":
        print(next((p["id"] for p in todos() if p["status"] == "na_fila"), ""))
    elif c == "preparar":
        preparar(a[1])
    elif c == "aplicar":
        aplicar(a[1])
    elif c == "estado":
        p = estado(a[1], a[2] if len(a) > 2 and not a[2].startswith("--") else None, op("--status"), op("--msg"), op("--pct"))
        print(f"[fila] {p['id']}: {p['status']} / {p.get('etapa')} — {p.get('msg')}")
    elif c == "recados":
        recados(a[1])
    elif c == "baia":   # fila.py baia ID bN — o filme ocupa a baia (o painel mostra; Fotos/Linha do tempo leem de lá)
        p = pedido(a[1]); p["baia"] = a[2]; salva(p)
        print(f"[fila] {p['id']} -> baia {a[2]}")
    elif c == "ref":
        r = ref_estado(a[1], op("--status"), op("--msg"), op("--estilo"))
        print(f"[fila] referência {r['id']}: {r['status']} — {r.get('msg')}")
    elif c == "mostrar":
        print(json.dumps(pedido(a[1]), ensure_ascii=False, indent=1))
    elif c == "limpar":
        pv = limpeza_previa()
        _imprime_previa(pv)
        if "--simular" in a:
            print("(simulação: nada foi mexido)")
            return
        if not pv["pedidos"] and not any(not x["bloqueada"] for x in pv["pastas"]):
            print("Nada para limpar.")
            return
        if "--confirmar" not in a:
            try:
                ok = input("Arquivar e mandar para a Lixeira? [s/N] ").strip().lower() in ("s", "sim", "y")
            except EOFError:
                ok = False
            if not ok:
                print("Cancelado (sem terminal interativo, use --confirmar).")
                return
        r = limpar([x["id"] for x in pv["pedidos"]], [x["caminho"] for x in pv["pastas"]], origem="terminal")
        print(f"[fila] arquivados: {len(r['arquivados'])} · na Lixeira: {len(r['lixeira'])} ({r['gb_lixeira']} GB)")
        for e in r["erros"]:
            print(f"  ERRO {e['item']}: {e['erro']}")
    elif c == "arquivados":
        for x in arquivados():
            print(f"{(x.get('arquivado') or '')[:16]:<17} {x['status'] or '-':<10} {x['pasta']:<45} {x['titulo']}")
    elif c == "restaurar":
        r = restaurar(a[1] if len(a) > 1 else "")
        print(f"[fila] {r['id']} voltou para a fila" if r["ok"] else f"[fila] {r['erro']}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
