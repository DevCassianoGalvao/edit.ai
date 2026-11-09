"""CENTRAL — a tela robusta da Sala de Montagem (16/10/2026, pedido do usuário: "crie o app com uma tela mais robusta").

Por que existe: o render do italiano ficou 4 h parado com o painel dizendo "o Claude continua"; devolver fotos do APAGAR,
refazer clipe corrompido, retomar render e trocar trilha viravam conversa no chat. A Central:
  1. junta a SAÚDE de tudo (painel, gerente, funcionários, tarefa do Agendador, disco, lixo APAGAR, limite do Claude,
     render) e acha os filmes PARADOS sem ninguém trabalhando (regra: sem sessão do Diretor, sem arquivo novo na baia);
  2. AVISA na hora: notificação do Windows sempre; no celular pelo ntfy (app grátis) quando ligado na tela;
  3. tem os BOTÕES que rodam o procedimento certo (os mesmos que eu fazia no chat):
       retomar_render, retomar_diretor, devolver_fila, refazer_clipes, trocar_trilha, rerenderizar,
       devolver_material, esvaziar_apagar, reiniciar_gerente, ligar_servicos, funcionarios, autostart,
       notificar, testar_aviso, remoto, thumb_principal
  4. acesso pelo CELULAR: servidor.py escuta na rede só com "remoto" ligado, e só aceita quem tem a chave (token).
Nada aqui apaga arquivo: o que sai do lugar vai para uma pasta APAGAR_* (o usuário esvazia) ou para a Lixeira.
"""
import concurrent.futures as cf
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRINCIPAL = HERE.parent
ALTA = PRINCIPAL.parent
FERR = ALTA / "baias" / "_ferramentas"
CONF = HERE / "central.json"
NOTIFICADOS = HERE / ".central_notificados.json"
ACOES_DIR = HERE / "central_acoes"
CMDLOG = ALTA / "render_comandos.log"
EST_ARQ = HERE / "gerente_estado.json"
NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
DETACH = NOWIN | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
BASH = shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
PY = sys.executable
PARADO_MIN = 20           # min sem sessão e sem arquivo novo na baia = filme parado
DISCO_CRIT, DISCO_AVISO = 8, 15   # GB livres no C:
sys.path.insert(0, str(HERE))
import fila as F  # noqa: E402


def agora():
    return time.time()


def jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def grava(p, obj):
    p = Path(p)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    tmp.replace(p)


def conf():
    c = jl(CONF, {})
    c.setdefault("notificar", {"ntfy": False, "topico": "sala-" + secrets.token_hex(5)})
    c.setdefault("remoto", {"ativo": False, "token": secrets.token_urlsafe(18)})
    if not CONF.exists():
        grava(CONF, c)
    return c


def idade_iso(s):
    try:
        return agora() - datetime.fromisoformat(str(s)[:19]).timestamp()
    except Exception:  # noqa: BLE001
        return None


def baias_lista():
    import baias
    return [(b, baias.caminho(b)) for b in baias.todas()]


def pasta_baia(b):
    import baias
    return baias.caminho(b or "b1")


# ------------------------------------------------------------------------------------------------------- saúde
_CACHE = {}


def cache(chave, seg, fn):
    v = _CACHE.get(chave)
    if v and agora() - v[0] < seg:
        return v[1]
    try:
        r = fn()
    except Exception as ex:  # noqa: BLE001
        r = {"erro": str(ex)[:200]}
    _CACHE[chave] = (agora(), r)
    return r


def processos():
    def ler():
        cmd = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' or Name='ffmpeg.exe' or Name='node.exe' or "
               "Name='bash.exe' or Name='claude.exe' or Name='codex.exe'\" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress")
        r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60, creationflags=NOWIN)
        d = json.loads(r.stdout or "[]")
        return d if isinstance(d, list) else [d]
    return cache("proc", 15, ler)


def vivo_pid(pid, nome="python.exe"):
    if not pid:
        return False
    r = subprocess.run(["tasklist", "/FI", f"PID eq {int(pid)}", "/NH"], capture_output=True, text=True, creationflags=NOWIN)
    return any(l.split()[:2] == [nome, str(pid)] for l in r.stdout.lower().splitlines() if l.strip())


def gerente_saude():
    try:
        pid = int((HERE / ".gerente_pid").read_text().strip())
    except Exception:  # noqa: BLE001
        pid = None
    try:
        visto = agora() - float((HERE / ".gerente_vivo").read_text().strip())
    except Exception:  # noqa: BLE001
        visto = None
    vivo = bool(pid) and vivo_pid(pid) and (visto is None or visto < 120)
    return {"vivo": vivo, "pid": pid, "visto_s": round(visto) if visto is not None else None,
            "ligado": bool(jl(HERE / "config.json", {}).get("gerente")), "parado_de_vez": (HERE / ".parar_gerente").exists()}


def tarefa_agendada():
    def ler():
        out = {}
        for nome in ("Edit.AI by Galvão Gerente", "Edit.AI by Galvão Painel"):
            r = subprocess.run(["schtasks", "/query", "/tn", nome], capture_output=True, text=True, creationflags=NOWIN)
            out[nome] = r.returncode == 0
        return out
    return cache("tarefas", 300, ler)


def disco():
    u = shutil.disk_usage("C:\\")
    return {"livre_gb": round(u.free / 1e9, 1), "total_gb": round(u.total / 1e9), "usado_pct": round(100 * (1 - u.free / u.total))}


def apagar_info():
    def ler():
        pastas = F.pastas_apagar()
        return {"n": len(pastas), "gb": round(sum(F.tamanho(d) for d, _ in pastas) / 1e9, 1)}
    return cache("apagar", 600, ler)


def est():
    return jl(EST_ARQ, {"pedidos": {}, "sessoes": {}, "feed": []})


def claude_limite(e):
    """Feed das últimas 3 h com cara de limite/assinatura do Claude."""
    pad = re.compile(r"(hit your limit|usage limit|limite semanal|limite de uso|disabled claude|subscription access|"
                     r"rate limit|5-hour limit|claude.exe não|sem claude|codex.exe|Codex: .*(limit|quota|log ?in|auth))", re.I)
    for f in reversed(e.get("feed", [])[-60:]):
        if agora() - float(f.get("t") or 0) > 3 * 3600:
            break
        if pad.search(f.get("txt", "")):
            return f.get("txt", "")
    return None


def atividade_baia(raiz):
    """segundos desde o arquivo mais novo da baia (data/, out/hybrid/, slices, stock, out/)."""
    mais = 0.0
    for sub in ("data", "out/hybrid", "out", "input/youtube/slices", "public/stock", "qa"):
        p = Path(raiz) / sub
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        mais = max(mais, e.stat().st_mtime)
                    except OSError:
                        pass
        except OSError:
            continue
    return round(agora() - mais) if mais else None


def sessao_ativa(e, pedido):
    for sid, s in e.get("sessoes", {}).items():
        if s.get("pedido") == pedido and not s.get("fim"):
            return {"sid": sid, "papel": s.get("papel"), "inicio": s.get("inicio"), "acao": s.get("acao") or s.get("ultimo")}
    return None


def render_rodando():
    for p in processos() if isinstance(processos(), list) else []:
        c = (p.get("CommandLine") or "")
        if "render_hybrid" in c or "fechar.py render" in c or "render_ranges" in c:
            return True
    return False


BOTOES = {
    "retomar_render": "Retomar render",
    "retomar_diretor": "Diretor continua de onde parou",
    "devolver_fila": "Recomeçar do zero (volta para a fila)",
    "refazer_clipes": "Refazer clipes ruins",
}


def problema_do_pedido(p, e, ativa, ativ_s, rend):
    st, etapa = p.get("status"), p.get("etapa") or ""
    fase = (e.get("pedidos", {}).get(p["id"]) or {}).get("fase")
    renderiza = etapa in ("render", "conferir", "entregue")
    botoes = ["retomar_render", "retomar_diretor"] if renderiza else ["retomar_diretor", "devolver_fila"]
    if st == "esperando_voce":
        return {"codigo": "precisa_voce", "nivel": "alto", "texto": p.get("msg") or "parou e precisa de você", "botoes": botoes}
    if st != "produzindo" or ativa:
        return None
    idade = idade_iso(p.get("atualizado")) or 0
    quieto = (ativ_s is None or ativ_s > PARADO_MIN * 60) and idade > PARADO_MIN * 60
    if renderiza and rend:   # 17/10/2026: na fila de render esperando a outra baia (trava) não mexe em arquivo — não é parado
        return None
    if quieto or (fase == "parado" and (ativ_s is None or ativ_s > 10 * 60)):
        mins = round(min(idade, ativ_s or idade) / 60)
        return {"codigo": "parado", "nivel": "alto",
                "texto": f"ninguém trabalha neste filme há {mins} min (etapa {etapa or '?'}): o painel ainda diz \"{(p.get('msg') or '')[:70]}\"",
                "botoes": botoes}
    return None


def pedidos_info(e):
    rend = render_rodando()
    ativ = {b: atividade_baia(r) for b, r in baias_lista()}
    out = []
    for p in sorted(F.todos(), key=lambda x: x.get("ordem", 0)):
        if p.get("status") in ("entregue", "cancelado") and (idade_iso(p.get("atualizado")) or 1e9) > 6 * 3600:
            continue
        ativa = sessao_ativa(e, p["id"])
        b = p.get("baia") or ""
        info = {k: p.get(k) for k in ("id", "titulo", "status", "etapa", "pct", "msg", "idioma", "atualizado")}
        info.update(baia=b, ativa=ativa, fase=(e.get("pedidos", {}).get(p["id"]) or {}).get("fase"),
                    parado_ha_s=round(idade_iso(p.get("atualizado")) or 0), atividade_s=ativ.get(b))
        info["problema"] = problema_do_pedido(p, e, ativa, ativ.get(b), rend) if p.get("status") not in ("entregue", "cancelado", "na_fila") else None
        out.append(info)
    return out


def pautas_info():
    try:
        import pautas as PA
        d = PA.dados()
    except Exception as ex:  # noqa: BLE001
        return {"erro": str(ex)}
    ps = d.get("pautas", [])
    voz = [p for p in ps if p["status"] == "roteirizando" and (idade_iso(p.get("atualizada")) or 0) > 45 * 60]
    prop = [{k: p.get(k) for k in ("id", "titulo", "titulo_pt", "canal", "status", "msg", "criada")}
            for p in ps if p["status"] in ("proposta", "erro")][-40:]
    cont = {}
    for p in ps:
        cont[p["status"]] = cont.get(p["status"], 0) + 1
    return {"propostas": prop, "contagem": cont, "voz_travada": [p["titulo"][:60] for p in voz]}


def entregas_info(n=14):
    E = PRINCIPAL / "entregas"
    ds = sorted([d for d in E.iterdir() if d.is_dir() and not d.name.startswith("_")], key=lambda d: d.stat().st_mtime, reverse=True)[:n]
    out = []
    for d in ds:
        mp4 = next(iter(sorted(d.glob("*.mp4"))), None)
        minis = sorted([f.name for f in (d / "miniaturas").glob("*.jpg") if not f.name.startswith("_teste")]) if (d / "miniaturas").exists() else []
        out.append({"slug": d.name, "nome": mp4.stem if mp4 else d.name, "pronto": bool(mp4), "mb": round(mp4.stat().st_size / 1e6) if mp4 else 0,
                    "quando": datetime.fromtimestamp((mp4 or d).stat().st_mtime).strftime("%d/%m %H:%M"), "miniaturas": minis,
                    "principal": "_PRINCIPAL.jpg" if (d / "miniaturas" / "_PRINCIPAL.jpg").exists() else None,
                    "material": (PRINCIPAL / f"APAGAR_{d.name}").exists()})
    return out


def a_abrir_pasta_entrega(aid, slug, **_):
    """Abre no Explorador só a pasta final de uma entrega existente."""
    slug = str(slug or "").strip()
    if not slug or Path(slug).name != slug or slug in (".", ".."):
        return False, "identificador de entrega inválido"
    raiz = (PRINCIPAL / "entregas").resolve()
    pasta = (raiz / slug).resolve()
    try:
        pasta.relative_to(raiz)
    except ValueError:
        return False, "a pasta está fora de entregas"
    if not pasta.is_dir() or not any(pasta.glob("*.mp4")):
        return False, "o render ainda não foi concluído nesta pasta"
    os.startfile(str(pasta))
    return True, "Pasta do render aberta no Explorador"


def baias_info(e, peds):
    out = []
    for b, raiz in baias_lista():
        p = next((x for x in peds if x["baia"] == b and x["status"] in ("produzindo", "esperando_voce", "pausado")), None)
        slug = (raiz / "data" / "gerente_slug.txt")
        out.append({"baia": b, "pedido": p["id"] if p else None, "titulo": p["titulo"] if p else None,
                    "ultimo_slug": slug.read_text("utf-8").strip() if slug.exists() else None,
                    "atividade_s": atividade_baia(raiz), "livre": p is None})
    return out


def alertas(s):
    a = []
    d = s["disco"]
    if d["livre_gb"] < DISCO_CRIT:
        a.append({"id": "disco_crit", "nivel": "alto", "titulo": "Disco C: cheio",
                  "texto": f"só {d['livre_gb']} GB livres — o render precisa de ~10 GB. Esvazie as pastas APAGAR e a Lixeira.",
                  "botoes": ["esvaziar_apagar"]})
    elif d["livre_gb"] < DISCO_AVISO:
        a.append({"id": "disco_aviso", "nivel": "medio", "titulo": "Disco C: ficando cheio",
                  "texto": f"{d['livre_gb']} GB livres. APAGAR soma {s['apagar'].get('gb', '?')} GB.", "botoes": ["esvaziar_apagar"]})
    g = s["gerente"]
    if g["ligado"] and not g["vivo"]:
        a.append({"id": "gerente_morto", "nivel": "alto", "titulo": "O gerente caiu",
                  "texto": "os funcionários estão ligados mas o gerente não responde — nenhum filme anda.", "botoes": ["ligar_servicos"]})
    if s.get("claude_limite"):
        a.append({"id": "claude_limite", "nivel": "alto", "titulo": "Último erro de acesso à IA",
                  "texto": s["claude_limite"][:160] + " — confira o motor e a sessão atual; este aviso pode se referir a uma tentativa anterior.", "botoes": []})
    t = s.get("tarefas") or {}
    if isinstance(t, dict) and t and not all(t.values()):
        falta = ", ".join(k for k, v in t.items() if not v)
        a.append({"id": "tarefa", "nivel": "info", "titulo": "Inicialização automática não configurada",
                  "texto": f"Não encontrei as tarefas do Edit.AI ({falta}). Isso não interrompe o trabalho nesta sessão. Se o Windows reiniciar, abra o Edit.AI pelo atalho; a retomada automática precisa ser configurada no Agendador do Windows.", "botoes": []})
    for v in s["pautas"].get("voz_travada", []):
        a.append({"id": "voz_" + v[:20], "nivel": "medio", "titulo": "Locução demorando", "texto": f"\"{v}\" está no roteirista/voz há mais de 45 min.", "botoes": []})
    for p in s["pedidos"]:
        pr = p.get("problema")
        if pr:
            a.append({"id": f"{pr['codigo']}_{p['id']}", "nivel": pr["nivel"],
                      "titulo": ("Precisa de você: " if pr["codigo"] == "precisa_voce" else "Filme parado: ") + (p.get("titulo") or p["id"])[:60],
                      "texto": pr["texto"], "botoes": pr["botoes"], "pedido": p["id"], "baia": p.get("baia")})
    return a


_SNAP = {"t": 0, "dados": None}
_SNAP_LOCK = threading.Lock()


def coletar():
    e = est()
    peds = pedidos_info(e)
    s = {"t": agora(), "disco": disco(), "gerente": gerente_saude(), "tarefas": tarefa_agendada(), "apagar": apagar_info(),
         "claude_limite": claude_limite(e), "render": render_rodando(), "pedidos": peds, "pautas": pautas_info(),
         "feed": e.get("feed", [])[-25:], "baias": baias_info(e, peds)}
    s["alertas"] = alertas(s)
    return s


def estado(forcar=False):
    with _SNAP_LOCK:
        if forcar or not _SNAP["dados"] or agora() - _SNAP["t"] > 8:
            _SNAP["dados"] = coletar()
            _SNAP["t"] = agora()
        s = dict(_SNAP["dados"])
    c = conf()
    s["acoes"] = acoes_lista()
    s["conf"] = {"ntfy": c["notificar"].get("ntfy"), "topico": c["notificar"].get("topico"),
                 "remoto": c["remoto"].get("ativo"), "link_celular": link_celular(c), "autostart": autostart_ligado()}
    s["entregas"] = cache("entregas", 30, entregas_info)
    return s


# ------------------------------------------------------------------------------------------------------ avisos
def toast(titulo, texto):
    ps = ("[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
          "$t=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);"
          "$x=$t.GetElementsByTagName('text');$x.Item(0).AppendChild($t.CreateTextNode($env:T1))>$null;"
          "$x.Item(1).AppendChild($t.CreateTextNode($env:T2))>$null;"
          "$n=[Windows.UI.Notifications.ToastNotification]::new($t);"
          "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("
          "'{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe').Show($n)")
    try:
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps], env={**os.environ, "T1": titulo[:90], "T2": texto[:220]},
                         creationflags=NOWIN, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:  # noqa: BLE001
        pass


def ntfy(titulo, texto, prioridade=4):
    c = conf()["notificar"]
    if not c.get("ntfy") or not c.get("topico"):
        return False
    corpo = json.dumps({"topic": c["topico"], "title": titulo[:120], "message": texto[:400], "priority": prioridade,
                        "tags": ["rotating_light" if prioridade >= 4 else "information_source"]}).encode("utf-8")
    try:
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/", data=corpo, headers={"Content-Type": "application/json"}), timeout=15)
        return True
    except Exception:  # noqa: BLE001
        return False


def avisar(titulo, texto, prioridade=4):
    toast(titulo, texto)
    threading.Thread(target=ntfy, args=(titulo, texto, prioridade), daemon=True).start()


def vigia_loop():
    """Thread do servidor: a cada 60 s recalcula e avisa SÓ o alerta novo (o mesmo não repete por 6 h)."""
    time.sleep(20)
    caido = 0
    while True:
        try:
            # 17/10/2026: o gerente cai junto com o laço dele (18:28, 18:50, 19:24) e só voltava pela tarefa de 5 em 5 min.
            # A Central roda em outro processo: 2 checagens seguidas sem gerente (funcionários ligados) -> religa já.
            g = gerente_saude()
            caido = caido + 1 if (g["ligado"] and not g["vivo"] and not g["parado_de_vez"]) else 0
            if caido >= 2:
                ok = roda_tarefa("Edit.AI by Galvão Gerente")
                print(f"[central] gerente caído — religado pela tarefa ({'ok' if ok else 'falhou'})", flush=True)
                avisar("Edit.AI by Galvão — gerente religado", "o gerente tinha caído; a Central religou sozinha e os diretores retomam de onde pararam", 3)
                caido = 0
            s = estado(forcar=True)
            vistos = jl(NOTIFICADOS, {})
            mudou = False
            for al in s["alertas"]:
                if agora() - vistos.get(al["id"], 0) > 6 * 3600:
                    avisar("Edit.AI by Galvão — " + al["titulo"], al["texto"], 5 if al["nivel"] == "alto" else 3)
                    vistos[al["id"]] = agora()
                    mudou = True
            ativos = {al["id"] for al in s["alertas"]}
            for k in list(vistos):   # resolveu: pode avisar de novo se voltar
                if k not in ativos and agora() - vistos[k] > 600:
                    vistos.pop(k)
                    mudou = True
            if mudou:
                grava(NOTIFICADOS, vistos)
        except Exception as ex:  # noqa: BLE001
            print("[central] vigia:", ex, flush=True)
        time.sleep(60)


def iniciar_vigia():
    threading.Thread(target=vigia_loop, daemon=True, name="central-vigia").start()


# ------------------------------------------------------------------------------------------------------- ações
ACOES = {}
_AC_LOCK = threading.Lock()


def acoes_lista():
    with _AC_LOCK:
        return sorted(({"id": k, **{x: v.get(x) for x in ("acao", "rotulo", "inicio", "fim", "ok", "resumo")}} for k, v in ACOES.items()),
                      key=lambda x: x["inicio"], reverse=True)[:12]


def log_acao(aid, txt):
    with _AC_LOCK:
        a = ACOES.get(aid)
    if a:
        with open(a["log"], "a", encoding="utf-8") as fh:
            fh.write(time.strftime("%H:%M:%S ") + txt + "\n")


def roda(aid, cmd, cwd, espera=True):
    log_acao(aid, "$ " + " ".join(str(c) for c in cmd))
    with open(ACOES[aid]["log"], "a", encoding="utf-8") as fh:
        proc = subprocess.Popen([str(c) for c in cmd], cwd=str(cwd), stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                env={**os.environ, "PYTHONIOENCODING": "utf-8"}, creationflags=NOWIN if espera else DETACH)
    if not espera:
        return proc
    return proc.wait()


def comando_render(pedido=None, slug=None):
    """Último comando do render_e_entrega.sh deste filme (render_comandos.log) ou montado da entrega já feita."""
    linhas = CMDLOG.read_text("utf-8").splitlines() if CMDLOG.exists() else []
    for l in reversed(linhas):
        partes = l.split("|")
        if len(partes) >= 8 and ((pedido and partes[2] == pedido) or (slug and partes[3] == slug)):
            return "|".join(partes[1:8])
    if not slug:
        return None
    ent = PRINCIPAL / "entregas" / slug
    mp4 = next(iter(ent.glob("*.mp4")), None)
    minis = [f.name for f in (ent / "miniaturas").glob("*.jpg") if not f.name.startswith(("_", "flow_"))] if ent.exists() else []
    pref = minis[0].split("_")[0] + "_" if minis else ""
    mod = ""
    for b, raiz in baias_lista():
        if (raiz / "data" / "gerente_slug.txt").exists() and (raiz / "data" / "gerente_slug.txt").read_text("utf-8").strip() == slug:
            for m in sorted((raiz / "scripts").glob("make_thumb_*.py"), key=lambda f: f.stat().st_mtime, reverse=True):
                if pref and pref in m.read_text("utf-8", errors="ignore"):
                    mod = m.stem
                    break
            if mp4 and mod:
                if not pedido:   # o gerente guarda o slug do filme entregue em cada pedido
                    pedido = next((k for k, d in est().get("pedidos", {}).items() if d.get("slug") == slug), "")
                if not pedido:   # senão: o último pedido entregue nesta baia
                    ents = [p for p in F.todos() if p.get("baia") == b and p.get("status") == "entregue"]
                    pedido = max(ents, key=lambda p: p.get("atualizado", ""))["id"] if ents else ""
                return "|".join([str(raiz).replace("\\", "/"), pedido or "", slug, mp4.stem, pref, mod, ""])
    return None


def agenda_render(aid, arg):
    """17/10/2026: o render roda numa TAREFA PRÓPRIA do Agendador (job próprio). Processo filho do servidor ou do
    gerente morria junto quando eles caíam (o render da b2 iniciado pela Central sobreviveu à queda das 20:12; o do
    Diretor, não). Mesmo truque do _agenda.ps1 dos Diretores."""
    baia = Path(arg.split("|")[0].replace("/", "\\"))
    nome = "Edit.AI by Galvão_render_" + (baia.name if baia.name.startswith("b") else "b1")
    bat = baia / f"_render_{nome}.bat"
    log = baia / "data" / "_render_tarefa.log"
    bat.write_bytes(("@echo off\r\nchcp 65001 >nul\r\n"
                     f'cd /d "{FERR}"\r\n'
                     f'"{BASH}" render_e_entrega.sh "{arg}" >> "{log}" 2>&1\r\n').encode("utf-8"))
    # 17/10/2026: a tarefa só chama o solta.py, que lança o .bat ÓRFÃO e sai (a árvore do Agendador era morta inteira)
    ps = ("$a = New-ScheduledTaskAction -Execute $env:PYEXE -Argument ('\"' + $env:SOLTA + '\" cmd /c \"' + $env:BAT + '\"');"
          "$s = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 4);"
          "Register-ScheduledTask -TaskName $env:TAREFA -Action $a -Settings $s -Force | Out-Null; Start-ScheduledTask -TaskName $env:TAREFA; 'agendado'")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, creationflags=NOWIN,
                       env={**os.environ, "BAT": str(bat), "TAREFA": nome, "SOLTA": str(HERE / "solta.py"), "PYEXE": PY})
    log_acao(aid, f"tarefa {nome}: {r.stdout.strip() or r.stderr.strip()[:200]}")
    return "agendado" in r.stdout


def lanca_render(aid, arg, pedido):
    log_acao(aid, "render + entrega: " + arg)
    if not agenda_render(aid, arg):
        log_acao(aid, "não consegui criar a tarefa do Agendador — render roda pela Central")
        roda(aid, [BASH, FERR / "render_e_entrega.sh", arg], FERR)
    else:
        slug = arg.split("|")[2]
        fim = agora() + 4 * 3600
        while agora() < fim:   # acompanha pela fila (ou pelo fila_render.log quando não há pedido)
            time.sleep(30)
            st = (F.pedido(pedido) or {}).get("status") if pedido else None
            ult = (ALTA / "fila_render.log").read_text("utf-8", errors="ignore").splitlines()[-3:] if (ALTA / "fila_render.log").exists() else []
            if st in ("entregue", "esperando_voce") or any(slug in l and ("ENTREGUE" in l or "FALHOU" in l) for l in ult):
                break
    p = F.pedido(pedido) if pedido else None
    if p and p.get("status") == "entregue":
        try:
            import pautas as PA
            n = PA.copia_thumbs(pedido, arg.split("|")[2])
            log_acao(aid, f"{n} miniaturas do Flow copiadas para a entrega")
        except Exception as ex:  # noqa: BLE001
            log_acao(aid, f"miniaturas do Flow: {ex}")
        return True, "entregue"
    return False, "o render parou — veja data/fechar_render.log / entregar.log na baia"


def baia_ocupada(b):
    for p in F.todos():
        if p.get("baia") == b and p.get("status") in ("produzindo", "pausado"):
            e = est()
            if sessao_ativa(e, p["id"]):
                return p["id"]
    return None


def a_retomar_render(aid, pedido, **_):
    p = F.pedido(pedido)
    if not p:
        return False, "pedido não encontrado"
    if disco()["livre_gb"] < 12:
        return False, f"disco com {disco()['livre_gb']} GB — esvazie as pastas APAGAR antes (o render precisa de ~10 GB)"
    raiz = pasta_baia(p.get("baia"))
    arg = None
    for sh in [raiz / "data" / "RETOMAR_RENDER.sh"]:
        if sh.exists() and pedido in sh.read_text("utf-8", errors="ignore"):
            m = re.search(r'render_e_entrega\.sh "([^"]+)"', sh.read_text("utf-8", errors="ignore"))
            arg = m.group(1) if m else None
    arg = arg or comando_render(pedido=pedido)
    if not arg:
        return False, "não achei o comando de render deste filme (nem RETOMAR_RENDER.sh nem render_comandos.log) — use 'Diretor continua'"
    F.estado(pedido, "render", status="produzindo", msg="render retomado pela Central (entrega automática no fim)")
    return lanca_render(aid, arg, pedido)


def roda_tarefa(nome):
    """17/10/2026: gerente e painel SEMPRE nascem pela tarefa do Agendador — filho do servidor morria junto quando o
    servidor era reiniciado e levava as sessões dos funcionários (agentes parando toda hora)."""
    r = subprocess.run(["schtasks", "/run", "/tn", nome], capture_output=True, text=True, creationflags=NOWIN)
    return r.returncode == 0


def liga_gerente(aid):
    (HERE / ".parar_gerente").unlink(missing_ok=True)
    time.sleep(1)
    if not gerente_saude()["vivo"]:
        if roda_tarefa("Edit.AI by Galvão Gerente"):
            log_acao(aid, "gerente religado pela tarefa 'Edit.AI by Galvão Gerente' do Agendador")
        else:
            subprocess.Popen(["wscript.exe", str(HERE / "gerente_escondido.vbs")], cwd=str(PRINCIPAL), creationflags=DETACH)
            log_acao(aid, "tarefa do Agendador não existe — gerente religado pelo gerente_escondido.vbs")


def sessao_do_log(pedido):
    for lg in sorted((HERE / "gerente_logs").glob(f"{pedido}-diretor-*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True):
        with open(lg, encoding="utf-8", errors="replace") as fh:
            for linha in fh:
                m = re.search(r'"session_id":\s*"([0-9a-f-]{36})"', linha)
                if m:
                    return lg.stem, m.group(1)
    return None, None


def a_retomar_diretor(aid, pedido, texto=None, **_):
    """17/10/2026: NÃO para mais o gerente (isso matava os agentes dos outros filmes). Deixa a ordem do usuário em
    fila/<id>/instrucao_gerente.txt e o pedido em .central_retomar.json — o gerente aplica no próximo passo (~10 s)."""
    p = F.pedido(pedido)
    if not p:
        return False, "pedido não encontrado"
    e = est()
    if sessao_ativa(e, pedido):
        return False, "o Diretor deste filme já está trabalhando agora"
    ordem = (texto or "").strip() or ("O filme ficou parado. Confira o estado da baia (fila, logs em data/), descubra onde parou e "
                                      "continue até pôr o filme na fila de render+entrega.")
    sess = [(sid, s) for sid, s in e.get("sessoes", {}).items() if s.get("pedido") == pedido and s.get("claude_session")]
    if sess:
        sid, s = max(sess, key=lambda x: x[1].get("inicio") or 0)
        cs = s["claude_session"]
    else:
        sid, cs = sessao_do_log(pedido)
        if cs:
            log_acao(aid, f"sessão {cs} recuperada do log {sid}")
    if not cs:
        return False, "não há sessão do Diretor para retomar — use 'Recomeçar do zero'"
    (F.FILA / pedido / "instrucao_gerente.txt").write_text(ordem, "utf-8")
    arq = HERE / ".central_retomar.json"
    lista = [x for x in jl(arq, []) if x.get("pedido") != pedido]
    lista.append({"pedido": pedido, "sid": sid, "claude_session": cs, "baia": p.get("baia") or "b1", "titulo": p.get("titulo", "")})
    grava(arq, lista)
    F.estado(pedido, status="produzindo", msg="retomado pela Central — o Diretor continua de onde parou")
    if not gerente_saude()["vivo"]:
        liga_gerente(aid)
    log_acao(aid, f"pedido deixado para o gerente: {pedido} (sessão {sid})")
    return True, "o gerente reabre o Diretor deste filme em até 1 min (os outros filmes continuam trabalhando)"


def a_devolver_fila(aid, pedido, **_):
    F.estado(pedido, status="na_fila", msg="voltou para a fila pela Central — começa de novo quando houver baia livre")
    return True, "voltou para a fila"


def a_refazer_clipes(aid, baia="b1", **_):
    raiz = pasta_baia(baia)
    vs = sorted((raiz / "public" / "stock").glob("v*.mp4"))
    if not vs:
        return False, "a baia não tem clipes de vídeo agora"

    def chk(f):
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "null", "-"], capture_output=True, text=True,
                           timeout=600, creationflags=NOWIN)
        return f, bool(r.stderr.strip())
    log_acao(aid, f"conferindo {len(vs)} clipes…")
    with cf.ThreadPoolExecutor(4) as ex:
        ruins = [f for f, r in ex.map(chk, vs) if r]
    if not ruins:
        return True, f"{len(vs)} clipes conferidos — nenhum corrompido"
    lixo = PRINCIPAL / f"APAGAR_clipes_corrompidos_{baia}_{time.strftime('%Y%m%d_%H%M')}"
    lixo.mkdir(exist_ok=True)
    for f in ruins:
        shutil.move(str(f), lixo / f.name)
    log_acao(aid, f"{len(ruins)} corrompidos movidos para {lixo.name}: " + ", ".join(f.name for f in ruins))
    rc = roda(aid, [PY, "scripts/make_clips.py", "--cpu"], raiz)
    refeitos = sum(1 for f in ruins if f.exists())
    return rc == 0 and refeitos == len(ruins), f"{len(ruins)} corrompidos; {refeitos} refeitos na CPU"


def faixas_disponiveis(baia="b1"):
    raiz = pasta_baia(baia)
    out = []
    for pasta, origem in ((raiz / "assets" / "music" / "manual", "biblioteca"), (raiz / "assets" / "music" / "yt_studio", "biblioteca"),
                          (Path(os.environ.get("USERPROFILE", "C:/Users/Cassiano")) / "Downloads", "Downloads")):
        if not pasta.exists():
            continue
        for f in sorted(pasta.glob("*.mp3"), key=lambda f: f.stat().st_mtime, reverse=True):
            if origem == "Downloads" and (agora() - f.stat().st_mtime > 30 * 86400 or f.stat().st_size < 1_000_000):
                continue
            out.append({"arquivo": str(f), "nome": f.stem, "origem": origem})
    pool = jl(raiz / "data" / "music_pool.json", {})
    atuais = {Path(v.get("file", "")).name for v in pool.values()}
    for x in out:
        x["no_filme"] = Path(x["arquivo"]).name in atuais
    return out[:80]


def a_trocar_trilha(aid, baia="b1", faixas=(), remux=True, **_):
    raiz = pasta_baia(baia)
    faixas = [Path(f) for f in faixas if Path(f).exists()]
    if not faixas:
        return False, "escolha pelo menos 1 faixa"
    man = raiz / "assets" / "music" / "manual"
    man.mkdir(parents=True, exist_ok=True)
    pool = {}
    for i, f in enumerate(faixas):
        dst = man / f.name
        if f.resolve() != dst.resolve():
            shutil.copy2(f, dst)
        k = "yt_" + re.sub(r"[^a-z0-9]+", "_", f.stem.lower()).strip("_")[:40]
        clima = "tensao" if i == 0 and len(faixas) > 1 else "cama"
        pool[k] = {"file": f"assets/music/manual/{f.name}", "title": f"{f.stem} (YouTube Audio Library)",
                   "license": f"YouTube Audio Library — \"{f.stem}\" (escolhida na Central)", "page": "https://studio.youtube.com/ (Biblioteca de Áudio)",
                   "fonte": "YouTube Audio Library", "termo": "escolhida pelo usuário", "clima": clima, "clima_fixo": clima, "reserva": False}
    mp = raiz / "data" / "music_pool.json"
    if mp.exists():
        shutil.copy2(mp, mp.with_name(f"music_pool.json.bak_central_{time.strftime('%H%M%S')}"))
    grava(mp, pool)
    log_acao(aid, f"music_pool com {len(pool)} faixas: " + ", ".join(f.stem for f in faixas))
    if roda(aid, [PY, "scripts/audio_probe_pool.py"], raiz) != 0 or roda(aid, [PY, "scripts/music_mix.py"], raiz) != 0:
        return False, "a mixagem falhou — veja o log da ação"
    if not remux:
        return True, "trilha nova mixada (entra no próximo render)"
    slug = (raiz / "data" / "gerente_slug.txt").read_text("utf-8").strip() if (raiz / "data" / "gerente_slug.txt").exists() else ""
    ent = PRINCIPAL / "entregas" / slug
    mp4 = next(iter(ent.glob("*.mp4")), None) if slug else None
    if not mp4:
        return True, "trilha nova mixada; não há entrega desta baia para trocar o áudio (entra no próximo render)"
    if baia_ocupada(baia):
        return False, "a baia já está em outro filme — o áudio do filme entregue não bate mais com os dados dela"
    novo = mp4.with_name(mp4.stem + ".trilha_nova.mp4")
    rc = roda(aid, ["ffmpeg", "-v", "error", "-y", "-i", mp4, "-i", raiz / "public" / "final_audio.m4a", "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-shortest", "-movflags", "+faststart", novo], raiz)
    if rc != 0 or not novo.exists():
        return False, "ffmpeg não trocou o áudio"
    velho = PRINCIPAL / f"APAGAR_{slug}"
    velho.mkdir(exist_ok=True)
    shutil.move(str(mp4), velho / f"trilha_antiga_{time.strftime('%H%M%S')}.mp4")
    novo.replace(mp4)
    return True, f"áudio trocado na entrega {slug} (o vídeo antigo foi para {velho.name})"


def devolve_material(aid, slug, raiz):
    lixo = PRINCIPAL / f"APAGAR_{slug}"
    if not lixo.exists():
        return 0
    n = 0
    for s in ("out/hybrid", "out/bundle", "public/stock", "assets/photos", "assets/thumbs", "input/youtube/slices"):
        src, dst = lixo / s, raiz / s
        if src.exists():
            if dst.exists() and any(dst.iterdir()):
                log_acao(aid, f"{s}: a baia já tem conteúdo — não mexi")
                continue
            if dst.exists():
                dst.rmdir()
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), dst)
            n += 1
            log_acao(aid, f"{s} devolvido para a baia")
    return n


def baia_do_slug(slug):
    for b, raiz in baias_lista():
        f = raiz / "data" / "gerente_slug.txt"
        if f.exists() and f.read_text("utf-8").strip() == slug:
            return b, raiz
    return None, None


def a_devolver_material(aid, slug, **_):
    b, raiz = baia_do_slug(slug)
    if not raiz:
        return False, "nenhuma baia tem os dados deste filme (ela já começou outro)"
    if baia_ocupada(b):
        return False, f"a {b} está trabalhando em outro filme agora"
    n = devolve_material(aid, slug, raiz)
    return True, f"{n} pastas devolvidas para a {b}"


def a_rerenderizar(aid, slug, modo="ffmpeg", **_):
    b, raiz = baia_do_slug(slug)
    if not raiz:
        return False, "nenhuma baia tem mais os dados deste filme — não dá para re-renderizar sem montar de novo"
    if baia_ocupada(b):
        return False, f"a {b} está trabalhando em outro filme agora — espere ela terminar"
    if disco()["livre_gb"] < 12:
        return False, f"disco com {disco()['livre_gb']} GB — esvazie as pastas APAGAR antes"
    arg = comando_render(slug=slug)
    if not arg:
        return False, "não achei o comando de render deste filme"
    devolve_material(aid, slug, raiz)
    hy = raiz / "out" / "hybrid"
    if not (hy / "plan.json").exists():
        return False, "out/hybrid/plan.json não voltou do APAGAR — o material deste filme não está completo"
    apag = 0
    for f in hy.glob("*.mp4"):
        if modo == "tudo" or "_f_" in f.name:
            f.unlink()
            apag += 1
    log_acao(aid, f"{apag} segmentos apagados para refazer ({'tudo' if modo == 'tudo' else 'fotos e vídeos'})")
    pedido = arg.split("|")[1]
    if pedido and F.pedido(pedido):
        F.estado(pedido, "render", status="produzindo", msg="re-render pela Central")
    return lanca_render(aid, arg, pedido if pedido and F.pedido(pedido) else None)


def a_esvaziar_apagar(aid, **_):
    r = F.limpar(pedidos=[], pastas=None, origem="central")
    _CACHE.pop("apagar", None)
    erros = r.get("erros") or []
    txt = f"{len(r.get('lixeira') or [])} pastas foram para a Lixeira ({r.get('gb_lixeira', 0)} GB) — esvazie a Lixeira para liberar o disco"
    if erros:
        txt += "; ficaram: " + "; ".join(f"{e['item']} ({e['erro'][:60]})" for e in erros[:4])
    return not erros, txt


def a_reiniciar_gerente(aid, **_):
    abertas = [s for s in est().get("sessoes", {}).values() if not s.get("fim")]
    if abertas:
        return False, (f"{len(abertas)} funcionário(s) trabalhando agora — reiniciar o gerente mataria o trabalho deles. "
                       "Espere terminarem (ou use 'Diretor continua' no filme parado).")
    g = gerente_saude()
    if g["pid"] and vivo_pid(g["pid"]):
        subprocess.run(["taskkill", "/F", "/PID", str(g["pid"])], capture_output=True, creationflags=NOWIN)
    time.sleep(8)
    liga_gerente(aid)
    return True, "gerente reiniciado"


def a_ligar_servicos(aid, **_):
    liga_gerente(aid)
    return True, "gerente ligado (o painel já está no ar)"


def a_funcionarios(aid, ligado=True, **_):
    c = jl(HERE / "config.json", {})
    c["gerente"] = bool(ligado)
    grava(HERE / "config.json", c)
    F.evento("gerente", None, ligado=c["gerente"])
    return True, "funcionários " + ("ligados" if ligado else "desligados (terminam o que começaram)")


def atalho_inicio():
    return Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Edit.AI by Galvão.lnk"


def autostart_ligado():
    return atalho_inicio().exists()


def cria_atalho(lnk, alvo_vbs):
    ico = HERE / "app" / "editai.ico"
    ps = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut($env:LNK);$s.TargetPath='wscript.exe';"
          "$s.Arguments='\"'+$env:VBS+'\"';$s.WorkingDirectory=$env:WD;"
          + ("$s.IconLocation=$env:ICO;" if ico.exists() else "") + "$s.Save()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, creationflags=NOWIN,
                   env={**os.environ, "LNK": str(lnk), "VBS": str(alvo_vbs), "WD": str(PRINCIPAL), "ICO": str(ico)})
    return Path(lnk).exists()


def a_autostart(aid, ligado=True, **_):
    lnk = atalho_inicio()
    if ligado:
        ok = cria_atalho(lnk, HERE / "app" / "SalaMontagem.vbs")
        return ok, "o app abre sozinho quando o Windows entrar" if ok else "não consegui criar o atalho de inicialização"
    lnk.unlink(missing_ok=True)
    return True, "o app não abre mais sozinho com o Windows (painel e gerente continuam voltando pela tarefa agendada)"


def a_notificar(aid, ligado=True, topico=None, **_):
    c = conf()
    c["notificar"]["ntfy"] = bool(ligado)
    if topico:
        c["notificar"]["topico"] = re.sub(r"[^A-Za-z0-9_-]", "", topico)[:60] or c["notificar"]["topico"]
    grava(CONF, c)
    return True, ("avisos no celular LIGADOS — instale o app ntfy e assine o tópico " + c["notificar"]["topico"]) if ligado else "avisos no celular desligados"


def a_testar_aviso(aid, **_):
    toast("Edit.AI by Galvão", "teste de aviso — se você está vendo isto, os avisos do Windows funcionam")
    ok = ntfy("Edit.AI by Galvão", "teste de aviso no celular — está funcionando", 3)
    return True, "aviso de teste enviado ao Windows" + (" e ao celular" if ok else " (celular desligado ou sem internet)")


def ip_rede():
    ts = shutil.which("tailscale") or r"C:\Program Files\Tailscale\tailscale.exe"
    if Path(ts).exists():
        try:
            r = subprocess.run([ts, "ip", "-4"], capture_output=True, text=True, timeout=5, creationflags=NOWIN)
            ip = r.stdout.strip().splitlines()[0] if r.stdout.strip() else ""
            if ip:
                return ip, "tailscale"
        except Exception:  # noqa: BLE001
            pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip, "wifi"
    except Exception:  # noqa: BLE001
        return "", ""


def link_celular(c=None):
    c = c or conf()
    if not c["remoto"].get("ativo"):
        return None
    ip, tipo = cache("ip", 120, ip_rede) if True else ("", "")
    if not ip:
        return None
    return {"url": f"http://{ip}:8876/central?k={c['remoto']['token']}", "tipo": tipo}


def a_remoto(aid, ligado=True, **_):
    c = conf()
    c["remoto"]["ativo"] = bool(ligado)
    grava(CONF, c)
    log_acao(aid, "reiniciando o servidor do painel para aplicar…")
    reinicia_servidor()
    return True, ("acesso pelo celular LIGADO — o servidor reinicia em 3 s (aceite o aviso do Firewall do Windows se aparecer)"
                  if ligado else "acesso pelo celular desligado — o painel volta a responder só neste PC")


def reinicia_servidor():
    # 17/10/2026: o servidor novo nasce pela tarefa "Edit.AI by Galvão Painel" (fora da árvore de processos de quem pediu)
    cod = ("import time,subprocess,sys;time.sleep(3);"
           "r=subprocess.run(['schtasks','/run','/tn','Edit.AI by Galvão Painel'],capture_output=True);"
           f"r.returncode==0 or subprocess.Popen([sys.executable,'-u',r'{HERE / 'servidor.py'}','--sem-navegador'],cwd=r'{PRINCIPAL}',"
           f"stdout=open(r'{HERE / 'servidor_console.log'}','a'),stderr=subprocess.STDOUT,creationflags={DETACH})")
    subprocess.Popen([PY, "-c", cod], creationflags=DETACH, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    threading.Timer(1.0, lambda: os._exit(0)).start()


def a_thumb_principal(aid, slug, arquivo, **_):
    m = PRINCIPAL / "entregas" / slug / "miniaturas"
    f = m / Path(arquivo).name
    if not f.exists():
        return False, "miniatura não encontrada"
    shutil.copy2(f, m / "_PRINCIPAL.jpg")
    _CACHE.pop("entregas", None)
    return True, f"{f.name} marcada como principal (_PRINCIPAL.jpg)"


ACAO_FN = {"retomar_render": a_retomar_render, "retomar_diretor": a_retomar_diretor, "devolver_fila": a_devolver_fila,
           "refazer_clipes": a_refazer_clipes, "trocar_trilha": a_trocar_trilha, "rerenderizar": a_rerenderizar,
           "devolver_material": a_devolver_material, "esvaziar_apagar": a_esvaziar_apagar, "reiniciar_gerente": a_reiniciar_gerente,
           "ligar_servicos": a_ligar_servicos, "funcionarios": a_funcionarios, "autostart": a_autostart, "notificar": a_notificar,
           "testar_aviso": a_testar_aviso, "remoto": a_remoto, "thumb_principal": a_thumb_principal,
           "abrir_pasta_entrega": a_abrir_pasta_entrega}
LONGAS = {"retomar_render", "refazer_clipes", "trocar_trilha", "rerenderizar", "esvaziar_apagar"}
ROTULOS = {"retomar_render": "Retomar render", "retomar_diretor": "Diretor continua", "devolver_fila": "Recomeçar do zero",
           "refazer_clipes": "Refazer clipes ruins", "trocar_trilha": "Trocar trilha", "rerenderizar": "Re-renderizar",
           "devolver_material": "Devolver material do APAGAR", "esvaziar_apagar": "Esvaziar pastas APAGAR",
           "reiniciar_gerente": "Reiniciar gerente", "ligar_servicos": "Ligar serviços", "funcionarios": "Funcionários",
           "autostart": "Abrir com o Windows", "notificar": "Avisos no celular", "testar_aviso": "Testar aviso",
           "remoto": "Acesso pelo celular", "thumb_principal": "Miniatura principal",
           "abrir_pasta_entrega": "Abrir pasta do render"}


def executar(body):
    nome = body.get("acao")
    fn = ACAO_FN.get(nome)
    if not fn:
        return {"ok": False, "erro": "ação desconhecida"}
    with _AC_LOCK:
        chave = str(body.get("pedido") or body.get("slug") or body.get("baia") or "")
        if nome in LONGAS and any(a["acao"] == nome and a.get("chave") == chave and not a.get("fim") for a in ACOES.values()):
            return {"ok": False, "erro": "essa ação já está rodando para este filme — espere terminar"}
        ACOES_DIR.mkdir(exist_ok=True)
        aid = f"{time.strftime('%Y%m%d-%H%M%S')}-{nome}"
        ACOES[aid] = {"acao": nome, "chave": chave, "rotulo": ROTULOS.get(nome, nome), "inicio": agora(), "fim": None, "ok": None, "resumo": "rodando…",
                      "log": str(ACOES_DIR / f"{aid}.log")}
    args = {k: v for k, v in body.items() if k != "acao"}
    log_acao(aid, f"ação {nome} {json.dumps(args, ensure_ascii=False)}")

    def corre():
        try:
            ok, resumo = fn(aid, **args)
        except Exception as ex:  # noqa: BLE001
            ok, resumo = False, f"erro: {ex}"
        log_acao(aid, ("OK: " if ok else "FALHOU: ") + resumo)
        with _AC_LOCK:
            ACOES[aid].update(fim=agora(), ok=ok, resumo=resumo)
        _SNAP["t"] = 0
        try:
            if nome in LONGAS:
                avisar("Edit.AI by Galvão — " + ROTULOS.get(nome, nome) + (" terminou" if ok else " falhou"), resumo, 3 if ok else 4)
        except Exception:  # noqa: BLE001
            pass
    if nome in ("remoto", "abrir_pasta_entrega"):
        corre()
        return {"ok": ACOES[aid]["ok"], "id": aid, "resumo": ACOES[aid]["resumo"],
                **({"erro": ACOES[aid]["resumo"]} if not ACOES[aid]["ok"] else {})}
    threading.Thread(target=corre, daemon=True, name=f"acao-{nome}").start()
    return {"ok": True, "id": aid}


def log_da_acao(aid):
    a = ACOES.get(aid)
    if not a:
        return {"ok": False}
    try:
        t = Path(a["log"]).read_text("utf-8", errors="replace")
    except OSError:
        t = ""
    return {"ok": True, "log": t[-6000:], **{k: a.get(k) for k in ("acao", "fim", "ok", "resumo")}}


def salva_thumb(slug, nome, dados):
    m = PRINCIPAL / "entregas" / slug / "miniaturas"
    if not m.exists() or not dados:
        return {"ok": False, "erro": "entrega não encontrada"}
    ext = ".png" if dados[:4] == b"\x89PNG" else ".jpg"
    f = m / (f"celular_{time.strftime('%Y%m%d_%H%M%S')}" + ext)
    f.write_bytes(dados)
    _CACHE.pop("entregas", None)
    return {"ok": True, "arquivo": f.name}


def arquivo_entrega(slug, rel):
    base = (PRINCIPAL / "entregas" / slug).resolve()
    f = (base / rel).resolve()
    return f if str(f).startswith(str(base)) and f.exists() else None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    s = estado(forcar=True)
    print(json.dumps({k: s[k] for k in ("disco", "gerente", "tarefas", "apagar", "claude_limite", "render", "alertas", "baias")},
                     ensure_ascii=False, indent=1)[:4000])
