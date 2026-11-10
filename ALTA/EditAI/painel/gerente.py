"""GERENTE — os funcionários trabalham sozinhos (05/10/2026, pedido do usuário: "faça os funcionários trabalhar sozinhos").

Fica ligado no PC (LIGAR_FUNCIONARIOS.bat). Quando o painel tem pedido "na_fila" e há baia livre (máx. 2), o gerente
reserva a baia e abre um DIRETOR (claude.exe do app, sem janela, -p) que produz o filme do começo ao fim seguindo
PIPELINE.md e a memória, chamando os funcionários fixos (.claude/agents: juiz-fotos, juiz-video, revisora,
pesquisador). O Diretor termina pondo o filme na fila de render+entrega (render_e_entrega.sh, destacado). Quando a
entrega acontece, o gerente abre a REVISORA FINAL, que confere o MP4; se achar defeito, conserta e relança a entrega
(até 3 rodadas).

Tudo o que cada um faz é lido do stream-json do claude.exe e gravado em painel/gerente_estado.json — é isso que a
tela do escritório (/escritorio) mostra ao vivo. Logs completos em painel/gerente_logs/.

Liga/desliga: painel/config.json "gerente": true|false (botão na tela do escritório). Desligado, ele termina o que
já começou mas não pega pedido novo. Enquanto ligado, o Claude do chat NÃO pega pedido do painel.

Uso: python painel/gerente.py            (fica rodando)
     python painel/gerente.py --uma-vez  (um passo, para teste)
"""
import glob, json, os, re, subprocess, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRINCIPAL = HERE.parent
ALTA = PRINCIPAL.parent
FERRAMENTAS = ALTA / "baias" / "_ferramentas"
MAPA = Path(os.environ.get("SALA_MAPA", str(ALTA.parent / "MAPA"))).resolve()   # cópia independente
ESTADO = HERE / "gerente_estado.json"
VIVO = HERE / ".gerente_vivo"
LOGS = HERE / "gerente_logs"
CONFIG = HERE / "config.json"
PROMPTS = HERE / "prompts"
MAX_BAIAS = 2
ESCALONAR = False   # 09/10/2026 (pedido do usuário, velocidade): os 2 filmes começam JUNTOS; só o render é um por vez (trava.py).
                    # True = volta a regra antiga: o 2º só começa quando o 1º passou da busca de material (cota do YouTube).
MAX_RETOMADAS = 4
MAX_CONSERTOS = 2   # 08/10/2026: render/entrega parou -> o próprio Diretor conserta e reenvia (no máx. 2 vezes por filme)
CONSERTO = """O RENDER OU A ENTREGA DESTE FILME PAROU (mensagem: {MSG}). Conserte sozinho e reenvie, sem esperar o usuário.
1. Leia na baia data/fechar_render.log e data/entregar.log (e data/fechar.log) e ache a causa exata.
2. Se out/final.mp4 já está pronto, NÃO renderize de novo:
   - aviso de áudio (audio_qa): ajuste o que o aviso pede (ex.: trilha alta -> music_mix com a cama mais baixa), troque só o
     áudio no MP4 (ffmpeg -map 0:v -map 1:a -c copy), rode audio_qa de novo, depois final_mp4_sheet.py e
     timeline_sheet.py qa/final_cortes --mp4 out/final.mp4, confira as folhas;
   - entrega quebrou (deliver/miniaturas/LEIA-ME): corrija o script e rode só `python scripts/fechar.py entregar ...` com os
     mesmos argumentos do render_e_entrega.sh, depois o guardar_entregue.py (se tinha banco) e
     `fila.py estado <pedido> entregue --status entregue --msg "entregue — <slug> (revisora final conferindo — espere a aprovação para publicar)" --pct 100`
     — exatamente como o render_e_entrega.sh faz no fim (a palavra "revisado" NÃO pode ir na mensagem).
3. Se o defeito exige render novo (corte/foto errada), corrija e ponha de novo na fila com o render_e_entrega.sh (nohup).
4. Não refaça o que já está certo. Se não houver conserto possível, marque esperando_voce com o motivo em 1 frase."""
MAX_RODADAS = 0   # 12/10/2026 meta 1 vídeo/hora: revisão só ANTES do render (cortes + animações); sem rodada depois da entrega
sys.path.insert(0, str(HERE))
import fila as F  # noqa: E402
import motor as MOTOR  # noqa: E402   06/11/2026: Claude ou ChatGPT Codex (config.json "motor")

EXE_NOME = {"claude": "claude.exe", "codex": "codex.exe"}


def exe_da_sessao(s):
    return EXE_NOME.get((s or {}).get("motor") or "claude", "claude.exe")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

LOCK = threading.Lock()
EST = {"sessoes": {}, "pedidos": {}, "feed": []}
PROCS = {}   # sid -> Popen (só nesta execução)

PESQUISA = re.compile(r"busca_openverse|fetch_images|fetch_photos|fetch_video|yt_lista|yt_probe|photo_dl|prefilter|photo_sheet|banco\.py|"
                      r"fetch_stock|fetch_dvids|probe_sheet|yt_win_dl|make_clips|source_review|yt_quando_liberar")
RENDER = re.compile(r"render_e_entrega|fechar\.py render|render_hybrid")


def agora():
    return time.time()


def jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def grava(p, obj):
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")
    # 07/10/2026: no Windows o replace falha (Acesso negado) se alguém está LENDO o arquivo naquele instante (escritório,
    # vigia) — isso derrubou o gerente às 00:34. Tenta de novo; se não der, fica para a próxima gravação (1 s depois).
    for i in range(20):
        try:
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.1 + 0.05 * i)


def ligado():
    return bool(jl(CONFIG, {}).get("gerente"))


def claude_exe():
    """claude.exe que vem com o app do Claude (já logado na conta). 05/10/2026: o gerente aberto pelo .bat não achou pelo
    APPDATA — agora procura também pelo caminho do usuário e pelo LOCALAPPDATA, e aceita config.json "claude_exe"."""
    cfg = jl(CONFIG, {}).get("claude_exe")
    if cfg and Path(cfg).exists():
        return cfg
    bases = {os.environ.get("APPDATA", ""), str(Path.home() / "AppData" / "Roaming"),
             os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming"), r"C:\Users\Cassiano\AppData\Roaming"}
    achados = []
    for b in bases:
        if b:
            achados += glob.glob(os.path.join(b, "Claude", "claude-code", "*", "*", "claude.exe"))
    for b in {os.environ.get("LOCALAPPDATA", ""), str(Path.home() / "AppData" / "Local")}:
        if b:
            achados += glob.glob(os.path.join(b, "AnthropicClaude", "**", "claude.exe"), recursive=True)
            # 06/10/2026: o app é pacote MSIX — fora dele (gerente solto via WMI) o AppData\Roaming\Claude NÃO existe;
            # o caminho real fica em Packages\Claude_*\LocalCache\Roaming
            achados += glob.glob(os.path.join(b, "Packages", "Claude_*", "LocalCache", "Roaming", "Claude",
                                              "claude-code", "*", "*", "claude.exe"))
            # 18/10/2026: app novo guarda o claude-code em Local\Claude-Data\claude_<id>\claude-code\<ver>\<hash>
            achados += glob.glob(os.path.join(b, "Claude-Data", "claude_*", "claude-code", "*", "*", "claude.exe"))
    achados = sorted(set(achados))
    if not achados:
        feed("gerente", f"procurei o claude.exe em: {sorted(x for x in bases if x)}")
        return None
    ver = lambda p: [int(x) if x.isdigit() else 0 for x in Path(p).parent.parent.name.split(".")]
    return max(achados, key=ver)


def vivo_pid(pid, nome=None):
    """06/10/2026: com `nome`, confere também o executável — o Windows reaproveita o PID (o Chrome pegou o de um Diretor
    morto e o gerente ficou esperando para sempre)."""
    if not pid:
        return False
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if nome:
        return any(l.split()[:2] == [nome, str(pid)] for l in r.stdout.lower().splitlines() if l.strip())
    return str(pid) in r.stdout


def feed(quem, txt, filme=""):
    with LOCK:
        EST["feed"].append({"t": agora(), "quem": quem, "txt": txt[:160], "filme": filme})
        EST["feed"] = EST["feed"][-60:]


def shorts3d_dir():
    """06/11/2026: projeto Remotion + three.js dos SHORTS 3D (skill cartoon-3d-short). config.json "shorts3d_dir" troca."""
    return Path(jl(CONFIG, {}).get("shorts3d_dir") or Path(os.environ.get("USERPROFILE", "C:/Users/Cassiano")) / "claude-shorts-3d")


def pasta_baia(b):
    if b == "s3d":
        return shorts3d_dir()
    return PRINCIPAL if b == "b1" else ALTA / "baias" / b


# ------------------------------------------------------------------ leitura do stream-json de cada sessão
def resumo_tool(nome, inp):
    if nome == "Bash":
        return (inp.get("description") or inp.get("command", ""))[:120], inp.get("command", "")
    if nome in ("Read", "Write", "Edit"):
        f = str(inp.get("file_path", ""))
        verbo = {"Read": "olhando", "Write": "escrevendo", "Edit": "editando"}[nome]
        return f"{verbo} {Path(f).name}", f
    if nome in ("Agent", "Task"):
        return f"chamou {inp.get('subagent_type', 'ajudante')}: {inp.get('description', '')}"[:120], ""
    return nome, ""


def linhas_do_log(logf, proc=None, pid=None, desde=0, exe_nome="claude.exe"):
    """17/10/2026: segue o log da sessão como um 'tail -f' até o claude.exe terminar. O processo escreve direto no
    arquivo — se o gerente cair, a sessão continua viva e o gerente novo volta a seguir o mesmo arquivo."""
    resto, parado = "", 0
    with open(logf, "r", encoding="utf-8", errors="replace") as fh:
        fh.seek(desde)
        while True:
            pedaco = fh.readline()
            if pedaco:
                parado = 0
                resto += pedaco
                if resto.endswith("\n"):
                    yield resto
                    resto = ""
                continue
            parado += 1
            if proc is None and parado % 10:   # sessão herdada: tasklist só a cada ~5 s
                time.sleep(0.5)
                continue
            vivo = (proc.poll() is None) if proc is not None else vivo_pid(pid, exe_nome)
            if not vivo:
                fim = fh.read()
                for l in (resto + fim).splitlines():
                    yield l + "\n"
                return
            time.sleep(0.5)


def evento_codex(s, e):
    """06/11/2026: eventos do `codex exec --json` (thread.started, item.started/completed, turn.completed, error)."""
    tp = e.get("type", "")
    if tp == "thread.started":
        s["claude_session"] = e.get("thread_id")      # mesmo campo: é o id para retomar (codex exec resume <id>)
        return
    if tp in ("turn.failed", "error"):
        err = e.get("error") if isinstance(e.get("error"), dict) else {}
        s["resultado"] = str(err.get("message") or e.get("message") or tp)[:400]
        # já estamos dentro do LOCK (feed() travaria): anota direto — a Central acha "usage limit" aqui
        EST["feed"].append({"t": agora(), "quem": s.get("papel", "codex"), "txt": ("Codex: " + s["resultado"])[:160],
                            "filme": s.get("pedido", "")})
        EST["feed"] = EST["feed"][-60:]
        return
    if tp == "turn.completed":
        s["resultado"] = s.get("fala", "") or "terminou"
        s["tokens"] = (e.get("usage") or {})
        return
    it = e.get("item") if isinstance(e.get("item"), dict) else {}
    ti = it.get("type", "")
    if ti == "agent_message":
        if tp == "item.completed":
            s["fala"] = str(it.get("text", "")).strip()[:200]
    elif ti == "command_execution" and tp == "item.started":
        cmd = str(it.get("command", ""))
        curto = re.sub(r'^"?[^"]*powershell(\.exe)?"?\s+-Command\s+', "", cmd, flags=re.I).strip("'\" ")
        s["txt"], s["t"], s["cmd"] = curto[:120], agora(), cmd[:300]
        s["area"] = ("pesquisa" if PESQUISA.search(cmd) else "render" if RENDER.search(cmd) else "mesa")
    elif ti == "file_change" and tp == "item.started":
        arqs = [Path(str(c.get("path", ""))).name for c in (it.get("changes") or []) if isinstance(c, dict)]
        s["txt"], s["t"], s["area"] = ("editando " + ", ".join(arqs))[:120], agora(), "mesa"
    elif "image" in ti or (ti == "mcp_tool_call" and "image" in str(it.get("tool", ""))):
        f = str(it.get("path") or (it.get("arguments") or {}).get("path", ""))
        s["txt"], s["t"] = f"olhando {Path(f).name}"[:120], agora()
        s["area"] = "revisao" if "/qa/" in f.replace("\\", "/") else "mesa"
    elif ti == "collab_tool_call":                 # funcionários do Codex (spawn_agent / wait)
        tool = str(it.get("tool", ""))
        if tool.startswith("spawn"):
            aid = it.get("id") or str(agora())
            if tp == "item.started" and aid not in s["ajudantes"]:
                s["ajudantes"][aid] = {"tipo": str(it.get("agent_type") or "funcionário"),
                                       "desc": str(it.get("prompt") or "")[:120], "inicio": agora(), "fim": None,
                                       "txt": "trabalhando", "t": agora()}
        elif tool.startswith("wait"):
            if tp == "item.started":
                s["txt"], s["t"] = "esperando os funcionários terminarem", agora()
            else:                                  # wait terminou: os ajudantes abertos acabaram
                for a in s["ajudantes"].values():
                    a["fim"] = a.get("fim") or agora()
    elif ti == "web_search" and tp == "item.started":
        s["txt"], s["t"], s["area"] = ("pesquisando: " + str(it.get("query", "")))[:120], agora(), "pesquisa"


def ler_stream(sid, proc, logf, pid=None, desde=0):
    if True:
        nome_exe = exe_da_sessao(EST["sessoes"].get(sid))
        for linha in linhas_do_log(logf, proc, pid, desde, nome_exe):
            try:
                e = json.loads(linha)
            except Exception:  # noqa: BLE001
                continue
            with LOCK:
                s = EST["sessoes"].get(sid)
                if not s:
                    continue
                if s.get("motor") == "codex":
                    try:
                        evento_codex(s, e)
                    except Exception:  # noqa: BLE001
                        pass
                    continue
                if e.get("type") == "system" and e.get("subtype") == "init":
                    s["claude_session"] = e.get("session_id")
                if e.get("type") == "system" and e.get("subtype") in ("task_progress", "task_notification"):
                    a = s["ajudantes"].get(e.get("tool_use_id"))
                    if a:
                        if e.get("subtype") == "task_progress":
                            a["txt"] = str(e.get("description") or a.get("txt", ""))[:120]
                            a["t"] = agora()
                        elif not a.get("fim"):
                            a["fim"] = agora()
                msg = e.get("message") if isinstance(e.get("message"), dict) else {}   # 07/10: às vezes vem texto
                cont = [c for c in (msg.get("content") if isinstance(msg.get("content"), list) else []) if isinstance(c, dict)]
                pai = e.get("parent_tool_use_id")
                for c in cont:
                    if c.get("type") == "tool_use":
                        txt, cmd = resumo_tool(c.get("name"), c.get("input") or {})
                        if pai and pai in s["ajudantes"]:                    # um ajudante (juiz etc.) trabalhando
                            s["ajudantes"][pai]["txt"] = txt
                            s["ajudantes"][pai]["t"] = agora()
                        elif c.get("name") in ("Agent", "Task"):
                            inp = c.get("input") or {}
                            s["ajudantes"][c["id"]] = {"tipo": inp.get("subagent_type", "general-purpose"),
                                                       "desc": inp.get("description", ""), "inicio": agora(),
                                                       "fim": None, "txt": "começando", "t": agora()}
                            s["txt"], s["t"] = txt, agora()
                        else:
                            s["txt"], s["t"], s["cmd"] = txt, agora(), cmd[:300]
                            s["area"] = ("pesquisa" if PESQUISA.search(cmd) else "render" if RENDER.search(cmd)
                                         else "revisao" if (c.get("name") == "Read" and "/qa/" in cmd.replace("\\", "/"))
                                         else "mesa")
                    elif c.get("type") == "tool_result":
                        a = s["ajudantes"].get(c.get("tool_use_id"))
                        txt_res = json.dumps(c.get("content"), ensure_ascii=False)[:200]
                        if a and not a["fim"]:
                            if "Async agent launched" in txt_res or "running in the background" in txt_res:
                                a["bg"] = True        # 05/10: juiz em segundo plano — o fim vem no task_notification
                            else:
                                a["fim"] = agora()
                    elif c.get("type") == "text" and not pai and c.get("text", "").strip():
                        s["fala"] = c["text"].strip()[:200]
                if e.get("type") == "result":
                    s["resultado"] = (e.get("result") or "")[:400]
                    s["custo"] = e.get("total_cost_usd")
    with LOCK:
        s = EST["sessoes"].get(sid)
        if s:
            s["fim"] = agora()
            s["rc"] = proc.wait() if proc is not None else None


BREAKAWAY = 0x01000000   # CREATE_BREAKAWAY_FROM_JOB


def popen_solto(cmd, prompt, logf):
    """17/10/2026: a sessão do funcionário nasce SOLTA do gerente: entrada por arquivo, saída direto no log, grupo de
    processo próprio e, se o Windows deixar, fora do 'job' da tarefa do Agendador. Antes ela ficava presa ao pipe do
    gerente e morria junto quando o gerente caía (agentes parando toda hora)."""
    entrada = Path(str(logf) + ".prompt.txt")
    entrada.write_text(prompt, "utf-8")
    # 17/10/2026: console PRÓPRIO e escondido para cada sessão (antes CREATE_NO_WINDOW). Se o claude.exe manda Ctrl+C
    # ao cortar um comando com sleep/timeout, o sinal fica no console da sessão e não derruba o gerente e o laço.
    base = getattr(subprocess, "CREATE_NEW_CONSOLE", 0x10) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0   # SW_HIDE
    with open(entrada, "rb") as fin, open(logf, "ab") as fout:
        try:
            return subprocess.Popen(cmd, cwd=str(MAPA), stdin=fin, stdout=fout, stderr=subprocess.STDOUT,
                                    creationflags=base | BREAKAWAY, startupinfo=si)
        except OSError:
            return subprocess.Popen(cmd, cwd=str(MAPA), stdin=fin, stdout=fout, stderr=subprocess.STDOUT,
                                    creationflags=base, startupinfo=si)


def abrir_sessao(papel, pedido, baia, prompt, resume=None, extra=None):
    # 06/11/2026: motor = o do painel (Claude ou Codex); RETOMAR usa o motor em que a sessão nasceu (id não serve no outro)
    motor = MOTOR.qual()
    if resume:
        motor_anterior = next((s.get("motor") or "claude" for s in EST["sessoes"].values() if s.get("claude_session") == resume), motor)
        if motor_anterior != motor:
            # IDs de sessão não são intercambiáveis: novo Diretor recebe o contexto do projeto.
            if papel != "diretor" or not pedido or not baia:
                feed("gerente", "motor alterado; esta sessão precisa ser iniciada novamente", pedido)
                return None
            prompt = preencher("diretor.md", **ctx(pedido, baia)) + "\n\nRETOMADA: a sessão anterior usava outro motor. Preserve os arquivos existentes e continue da etapa atual; não recomece nem apague dados sem necessidade.\n\n" + prompt
            resume = None
            feed("gerente", f"motor alterado para {motor}; iniciando nova sessão com o contexto do pedido", pedido)
    sid = f"{pedido}-{papel}-{int(agora())}"
    LOGS.mkdir(exist_ok=True)
    logf = LOGS / f"{sid}.jsonl"
    if motor == "codex":
        exe = MOTOR.codex_exe()
        if not exe:
            feed("gerente", "não achei o codex.exe (ChatGPT Codex) — instale o app do Codex ou troque para o Claude na aba Chaves")
            return None
        try:
            MOTOR.sincroniza_agentes(MAPA)
        except Exception as ex:  # noqa: BLE001
            feed("gerente", f"agentes do Codex não atualizados: {ex}")
        base = ["--json", "--dangerously-bypass-approvals-and-sandbox", "--skip-git-repo-check"]
        import editai
        ai_cfg = editai.settings()
        if ai_cfg.get("codex_model"): base += ["--model", ai_cfg["codex_model"]]
        if ai_cfg.get("codex_effort"): base += ["-c", 'model_reasoning_effort="' + ai_cfg["codex_effort"] + '"']
        if resume:
            cmd = [exe, "exec", "resume", resume, *base, "-"]
        else:
            cmd = [exe, "exec", *base, "-C", str(MAPA), "--add-dir", str(ALTA)]
            if baia == "s3d":
                cmd += ["--add-dir", str(shorts3d_dir())]
            cmd += ["-"]
            prompt = MOTOR.adaptador(MAPA) + prompt
    else:
        exe = claude_exe()
        if not exe:
            feed("gerente", "não achei o claude.exe do app — os funcionários não podem trabalhar")
            return None
        cmd = [exe, "-p", "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions",
               "--add-dir", str(ALTA)]
        import editai
        ai_cfg = editai.settings()
        if ai_cfg.get("claude_model"): cmd += ["--model", ai_cfg["claude_model"]]
        if baia == "s3d":
            cmd += ["--add-dir", str(shorts3d_dir())]
        if resume:
            cmd += ["--resume", resume]
    if not resume:
        import editai
        request = F.pedido(pedido) or {}
        perfil = next((c for c in editai.profiles() if c["name"] == request.get("canal")), None)
        if perfil and perfil.get("memory"):
            prompt += "\n\nIDENTIDADE EDITORIAL DO CANAL (orientações do proprietário):\n" + perfil["memory"] + "\n"
    if motor == "claude" and not resume:
        memoria = ALTA.parent / "MEMORIA"
        prompt = f"MEMÓRIA DO PROJETO: leia {memoria / 'MEMORY.md'} e os arquivos relacionados antes de começar.\n\n" + prompt
    try:
        proc = popen_solto(cmd, prompt, logf)
    except OSError as ex:
        feed("gerente", f"Não foi possível iniciar o {motor}: {str(ex)[:180]}", pedido)
        return None
    with LOCK:
        EST["sessoes"][sid] = {"papel": papel, "pedido": pedido, "baia": baia, "pid": proc.pid, "inicio": agora(),
                               "fim": None, "txt": "chegando na mesa", "t": agora(), "area": "mesa", "ajudantes": {},
                               "log": str(logf), "motor": motor, **(extra or {})}
    PROCS[sid] = proc
    threading.Thread(target=ler_stream, args=(sid, proc, logf), daemon=True).start()
    feed(papel, f"começou {pedido} na baia {baia}", pedido)
    return sid


def chaves_txt():
    try:
        import chaves
        return chaves.resumo_para_ia()
    except Exception:
        return ""


def preencher(modelo, **kw):
    t = (PROMPTS / modelo).read_text("utf-8")
    for k, v in kw.items():
        t = t.replace("{" + k + "}", str(v))
    return t


FORMATO_SHORT = """
FORMATO DESTE PEDIDO: SHORT (06/11/2026). Narração de 1 a 2 min; o filme sai normal em 16:9 e o fechar.py render já
monta o 9:16 inteiro (out/shorts/short_1.mp4, título em cima, legenda de impacto embaixo), que o deliver.py põe em
entregas/<slug>/shorts/. Regras: áudio acima de 125 s -> esperando_voce ("short tem no máximo 2 min"). Ritmo de short:
troca de imagem a cada 2-3 s, gancho visual no 1º segundo, no máximo 2 animações de tela cheia e 1-2 sobreposições;
sem busca demorada: 12-20 fotos/vídeos bastam. Nada de texto importante nas bordas laterais do quadro 16:9.
"""


def receita_estilo(pedido):
    """04/11/2026: estilo com "receita" (painel/estilos/<id>.json, ex.: arquivo-colorizado) entra no prompt do Diretor —
    antes só as escolhas/interruptores chegavam ao config e o Diretor não sabia o que o estilo pede na montagem.
    06/11/2026: pedido no formato "short" acrescenta FORMATO_SHORT."""
    try:
        eid = ((F.pedido(pedido) or {}).get("estilo") or "").replace(" (ajustado)", "")   # ajustado no painel = mesma receita
        e = json.loads((HERE / "estilos" / f"{eid}.json").read_text("utf-8")) if eid else {}
        r = ("\n" + e["receita"].strip() + "\n") if e.get("receita") else ""
        if (F.pedido(pedido) or {}).get("formato") == "short":
            r += FORMATO_SHORT
        return r
    except Exception:  # noqa: BLE001
        return ""


def ctx(pedido, baia):
    return dict(PEDIDO=pedido, BAIA=baia, PASTA_BAIA=str(pasta_baia(baia)).replace("\\", "/"),
                PRINCIPAL=str(PRINCIPAL).replace("\\", "/"), FERRAMENTAS=str(FERRAMENTAS).replace("\\", "/"),
                ESTILO_RECEITA=receita_estilo(pedido) + chaves_txt())


# ------------------------------------------------------------------ decisões
def sessao_ativa(pedido):
    for sid, s in EST["sessoes"].items():
        if s["pedido"] == pedido and not s.get("fim"):
            return sid
    return None


def baias_ocupadas():
    oc = {p.get("baia") for p in F.todos() if p.get("baia") and p.get("status") in ("produzindo", "esperando_voce", "pausado")}
    oc |= {d["baia"] for d in EST["pedidos"].values() if d["fase"] in ("diretor", "render", "revisao")}
    return oc


# ------------------------------------------------------------------ pautas automáticas (07/10/2026)
# Aba Pautas do painel: pesquisador (garimpo de outliers -> títulos por canal) e roteirista (roteiro -> locução
# DarkPlanner -> pedido na fila). Estado em painel/pautas/pautas.json (painel/pautas.py).
WPM = {"pt": 151, "pl": 128, "fr": 164, "en": 137, "es": 144}   # medido nos filmes entregues (07/10)
IDIOMA_NOME = {"pt": "português", "en": "inglês", "es": "espanhol", "pl": "polonês", "de": "alemão", "it": "italiano",
               "fr": "francês"}
SKILLS = PROMPTS / "skills"


def _pautas():
    import importlib
    import pautas as PA
    return importlib.reload(PA)


def mata_sessao(sid, motivo=""):
    """07/10/2026: pedido/pauta cancelado -> encerra a sessão do claude.exe e tudo o que ela abriu (árvore de processos)."""
    s = EST["sessoes"].get(sid) or {}
    pid = s.get("pid")
    if pid and vivo_pid(pid, exe_da_sessao(s)):
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    with LOCK:
        s["fim"] = s.get("fim") or agora()
        s["cancelada"] = motivo or True


def render_rodando():
    """09/10/2026 (usuário: menos memória no render): há um render (trava .trava_pesado) com processo vivo?"""
    try:
        e = json.loads((ALTA / ".trava_pesado").read_text("utf-8"))
        return bool(e.get("pid")) and vivo_pid(e["pid"])
    except Exception:  # noqa: BLE001
        return False


def passo_pautas():
    PA = _pautas()
    d = PA.dados()
    for sid, s in list(EST["sessoes"].items()):   # pauta tirada do roteiro (refazer/descartar): para o roteirista
        if s.get("papel") == "roteirista" and not s.get("fim"):
            p = next((x for x in d["pautas"] if "pauta-" + x["id"] == s.get("pedido")), None)
            if p and (p["status"] != "roteirizando" or p.get("sessao") != sid):
                mata_sessao(sid, "pauta mudou para " + p["status"])
                feed("roteirista", "parei o roteiro: " + p["titulo"][:60])
        elif s.get("papel") == "analista" and not s.get("fim"):   # tema próprio descartado no meio da análise
            p = next((x for x in d["pautas"] if "pauta-" + x["id"] == s.get("pedido")), None)
            if p and p["status"] == "descartada":
                mata_sessao(sid, "tema descartado")
        elif s.get("papel") == "modelador" and not s.get("fim"):   # modelagem apagada no painel
            if not any("modelo-" + m["id"] == s.get("pedido") for m in d.get("modelagens", [])):
                mata_sessao(sid, "modelagem apagada")
    pes = d.get("pesquisa") or {}
    ativas = {s.get("papel"): sid for sid, s in EST["sessoes"].items()
              if not s.get("fim") and s.get("papel") in ("pesquisador", "roteirista", "analista", "modelador")}
    princ = str(PRINCIPAL).replace("\\", "/")
    garimpo = str(SKILLS / "garimpo-de-brechas.md").replace("\\", "/")
    # 09/10/2026: durante um render NÃO abre ROTEIRISTA novo (memória do PC); o que já está escrevendo termina normalmente.
    # 10/10/2026: pesquisador, analista e modelador rodam sempre — o usuário fica esperando por eles e gastam pouco
    pausa = render_rodando()
    # 07/10/2026: TEMA PRÓPRIO (link ou título do usuário) -> analista -> título para o OK do usuário
    for p in d["pautas"]:
        if p["status"] == "analisando" and p.get("sessao") and p["sessao"] not in ativas.values():
            if EST["sessoes"].get(p["sessao"], {}).get("fim"):
                PA.muda([p["id"]], "erro", "o analista parou sem terminar — ver painel/gerente_logs", sessao=None)
                feed("pesquisador", "a análise parou sem terminar: " + p.get("entrada", "")[:60])
    if "analista" not in ativas:
        pend = [p for p in d["pautas"] if p["status"] == "analisando" and not p.get("sessao")]
        if pend:
            p = pend[0]
            c = PA.canais().get(p["canal"]) or {}
            op_ = p.get("opcoes") or {}
            (PA.PASTA / p["id"]).mkdir(parents=True, exist_ok=True)
            sid = abrir_sessao("analista", "pauta-" + p["id"], "-",
                               preencher("tema_proprio.md", PAUTA_ID=p["id"], ENTRADA=p.get("entrada", ""),
                                         TIPO="link do vídeo modelado" if p.get("tipo") == "link" else "título",
                                         CANAL_NOME=c.get("nome", p["canal"]), CANAL_ID=p["canal"], NICHO=c.get("nicho", ""),
                                         IDIOMA=p.get("idioma") or c.get("idioma", ""),
                                         IDIOMA_NOME=IDIOMA_NOME.get(p.get("idioma") or c.get("idioma", ""), p.get("idioma", "")),
                                         MELHORAR="SIM" if op_.get("melhorar") else "NÃO",
                                         CLICKBAIT="SIM" if op_.get("clickbait") else "NÃO", DIAS=op_.get("dias", 365),
                                         PRINCIPAL=princ, SKILL_GARIMPO=garimpo),
                               extra={"titulo_pauta": "tema: " + p.get("entrada", "")[:70]})
            if sid:
                PA.muda([p["id"]], "analisando", "o analista está estudando o tema", sessao=sid)
    # 07/10/2026: MODELAGEM DE VÍDEO -> modelador -> vídeos do mesmo modelo com muitas views e poucos inscritos
    for m in d.get("modelagens", []):
        if m["status"] == "modelando" and m.get("sessao") and m["sessao"] not in ativas.values():
            if EST["sessoes"].get(m["sessao"], {}).get("fim"):
                PA.muda_modelagem(m["id"], status="erro", msg="o modelador parou sem terminar — ver painel/gerente_logs")
    if "modelador" not in ativas:
        pend = [m for m in d.get("modelagens", []) if m["status"] == "analisando"]
        if pend:
            m = pend[0]
            sid = abrir_sessao("modelador", "modelo-" + m["id"], "-",
                               preencher("modelagem.md", MID=m["id"], ENTRADA=m["entrada"],
                                         TIPO="link" if m.get("tipo") == "link" else "título",
                                         DIAS=m.get("dias", 90), MAX_INSCRITOS=f"{m.get('max_inscritos', 100000):,}".replace(",", "."),
                                         PRINCIPAL=princ, SKILL_GARIMPO=garimpo),
                               extra={"titulo_pauta": "modelagem: " + m["entrada"][:60]})
            if sid:
                PA.muda_modelagem(m["id"], status="modelando", sessao=sid,
                                  msg="o modelador está estudando o vídeo e buscando parecidos")
    if pes.get("status") == "pendente" and "pesquisador" not in ativas:
        cs = PA.canais()
        nomes = ", ".join(f"{cs[c]['nome']} ({c}, {cs[c]['idioma']})" for c in pes["canais"] if c in cs)
        sid = abrir_sessao("pesquisador", "pesquisa-" + time.strftime("%Y%m%d-%H%M%S"), "-",
                           preencher("pesquisa_pautas.md", CANAIS=nomes, CANAIS_ESPACO=" ".join(pes["canais"]),
                                     POR_CANAL=pes.get("por_canal", 3), DIAS=pes.get("dias", 21), PRINCIPAL=princ,
                                     SKILL_GARIMPO=str(SKILLS / "garimpo-de-brechas.md").replace("\\", "/")),
                           extra={"titulo_pauta": "pautas: " + nomes[:60]})
        if sid:
            PA.atualiza_pesquisa(status="pesquisando", sessao=sid, inicio=PA.agora(),
                                 msg="o Paulo está garimpando os outliers da gringa")
    elif pes.get("status") == "pesquisando" and "pesquisador" not in ativas:
        novas = [p for p in d["pautas"] if p.get("criada", "") >= pes.get("inicio", pes.get("pedida", ""))]
        PA.atualiza_pesquisa(status="pronta" if novas else "erro",
                             msg=(f"{len(novas)} pautas esperando o seu OK" if novas else
                                  "o pesquisador terminou sem propor pautas — ver painel/gerente_logs"))
        feed("pesquisador", f"{len(novas)} pautas propostas — esperando o OK do usuário")
    # roteirista: uma pauta por vez, na ordem em que foram aprovadas
    for p in d["pautas"]:
        if p["status"] == "roteirizando" and p.get("sessao") and p["sessao"] not in ativas.values():
            s = EST["sessoes"].get(p["sessao"], {})
            if s.get("fim"):
                PA.muda([p["id"]], "erro", "o roteirista parou sem terminar — ver painel/gerente_logs")
                feed("roteirista", "parou sem terminar: " + p["titulo"][:60])
    if "roteirista" not in ativas and ligado() and not pausa:
        fila = sorted([p for p in d["pautas"] if p["status"] == "aprovada"], key=lambda p: p.get("atualizada", ""))
        if fila:
            p = fila[0]
            c = PA.canais().get(p["canal"])
            if not c:
                PA.muda([p["id"]], "erro", "canal não existe mais em canais.json")
                return
            f = p.get("fonte") or {}
            fonte = (f"{f.get('titulo', '')} — {f.get('canal', '')}, {f.get('views', '?')} views, "
                     f"{f.get('inscritos', '?')} inscritos, {f.get('dias', '?')} dias ({f.get('url', '')})")
            (PA.PASTA / p["id"]).mkdir(parents=True, exist_ok=True)
            sid = abrir_sessao("roteirista", "pauta-" + p["id"], "-",
                               preencher("roteirista.md", PAUTA_ID=p["id"], CANAL_NOME=c["nome"], CANAL_ID=c["id"],
                                         IDIOMA=p.get("idioma") or c["idioma"], PAIS=c.get("pais", ""), TITULO=p["titulo"],
                                         IDEIA=p.get("ideia", ""), FONTE=fonte,
                                         ANALISE=(p.get("analise") or "—") + (" Palavras-chave: " + ", ".join(p["palavras_chave"])
                                                                              if p.get("palavras_chave") else ""),
                                         # 07/10/2026: nº de palavras FIXO por canal (regra do usuário em canais.json)
                                         PALAVRAS=int(c.get("palavras") or c.get("duracao_min", 25) * WPM.get(c["idioma"], 145)),
                                         DURACAO=round((c.get("palavras") or c.get("duracao_min", 25) * WPM.get(c["idioma"], 145))
                                                       / WPM.get(c["idioma"], 145)),
                                         PRINCIPAL=princ,
                                         SKILL_ROTEIRO=str(SKILLS / "gerar-roteiro.md").replace("\\", "/")),
                               extra={"titulo_pauta": p["titulo"][:80]})
            if sid:
                PA.muda([p["id"]], "roteirizando", "o roteirista está escrevendo", sessao=sid)


CENTRAL_PEDIDOS = HERE / ".central_retomar.json"


def processa_central():
    """17/10/2026: o botão "Diretor continua" da Central NÃO para mais o gerente (parar o gerente matava as sessões dos
    outros filmes, presas aos pipes deste processo). A Central deixa o pedido em .central_retomar.json e o próprio
    gerente põe o filme de volta na fase diretor aqui, sem mexer em ninguém mais."""
    if not CENTRAL_PEDIDOS.exists():
        return
    try:
        lista = json.loads(CENTRAL_PEDIDOS.read_text("utf-8"))
        CENTRAL_PEDIDOS.unlink()
    except Exception:  # noqa: BLE001
        return
    for r in lista if isinstance(lista, list) else []:
        pedido, cs = r.get("pedido"), r.get("claude_session")
        if not pedido or not cs or sessao_ativa(pedido):
            continue
        sid = r.get("sid") or f"{pedido}-diretor-central-{int(agora())}"
        with LOCK:
            if sid not in EST["sessoes"]:
                EST["sessoes"][sid] = {"papel": "diretor", "pedido": pedido, "baia": r.get("baia") or "b1", "pid": 0,
                                       "inicio": agora() - 3600, "fim": agora() - 1, "claude_session": cs}
            d = EST["pedidos"].setdefault(pedido, {"baia": r.get("baia") or "b1", "inicio": agora(), "titulo": r.get("titulo", "")})
            d.update(fase="diretor", retomadas=0, pausou=True, espera_ate=0, ultima=sid)
        feed("gerente", "a Central pediu: o diretor continua de onde parou", pedido)


def passo():
    try:
        dono = int(TRAVA.read_text().strip())
    except Exception:  # noqa: BLE001
        dono = os.getpid()
    if dono != os.getpid() and vivo_pid(dono):
        print("[gerente] outro gerente assumiu — este fecha.", flush=True)
        sys.exit(0)
    with LOCK:
        EST["vivo"] = agora()
    processa_central()
    # sessões que caíram sem o leitor perceber (gerente reiniciado)
    for sid, s in list(EST["sessoes"].items()):
        if not s.get("fim") and sid not in PROCS and not vivo_pid(s.get("pid"), exe_da_sessao(s)):
            s["fim"] = agora()
    for pedido, d in list(EST["pedidos"].items()):
        p = F.pedido(pedido) or {}
        st = p.get("status")
        if st == "cancelado" and d["fase"] != "feito":   # 07/10/2026: cancelado no painel/pelo chat -> para tudo
            sid = sessao_ativa(pedido)
            if sid:
                mata_sessao(sid, "pedido cancelado")
            d["fase"] = "feito"
            feed("gerente", "pedido cancelado — parei o trabalho dele", pedido)
            continue
        ativa = sessao_ativa(pedido)
        if st == "pausado":
            if ativa:
                mata_sessao(ativa, "pedido pausado")
                feed("gerente", "produção pausada; sessão encerrada", pedido)
            continue
        if d["fase"] == "diretor" and not ativa:
            ult = EST["sessoes"].get(d.get("ultima"), {})
            if st in ("entregue",):
                d["fase"] = "render"
            elif p.get("etapa") == "render" and st in ("produzindo",):
                d["fase"] = "render"
                feed("diretor", "filme na fila de render — a entrega é automática", pedido)
            elif st == "esperando_voce":
                d["fase"] = "parado"
                feed("diretor", f"parou e precisa de você: {p.get('msg', '')}", pedido)
            elif st == "produzindo" and ult.get("claude_session") and (ult.get("motor") or "claude") != MOTOR.qual():
                # Uma troca de motor inicia outra sessão; nunca retoma no provedor anterior.
                sid = abrir_sessao("diretor", pedido, d["baia"], "Continue a produção na etapa atual, preservando os dados existentes.", resume=ult["claude_session"])
                if sid:
                    d.update(ultima=sid, retomadas=0, espera_ate=0, pausou=False)
                else:
                    d["fase"] = "parado"
                    F.estado(pedido, p.get("etapa") or "preparando", status="esperando_voce",
                             msg="Não foi possível iniciar o motor de IA selecionado. Confira a Central e tente retomar.")
                    feed("gerente", "Não foi possível iniciar a sessão no motor selecionado.", pedido)
            elif ult.get("claude_session") and agora() < d.get("espera_ate", 0):
                pass   # espera entre retomadas no mesmo motor
            elif d.get("retomadas", 0) < MAX_RETOMADAS and ult.get("claude_session"):
                marca = [p.get("etapa"), p.get("msg"), p.get("pct")]
                if marca != d.get("marca"):   # houve progresso desde a última retomada: não conta como falha
                    d["retomadas"] = 0
                d["marca"] = marca
                curta = (ult.get("fim") or 0) - (ult.get("inicio") or 0) < 300
                if curta and not d.get("pausou"):   # turno curto = "ainda esperando": pausa 8 min antes de retomar
                    d["pausou"] = True
                    d["espera_ate"] = agora() + 480
                    feed("diretor", "esperando os downloads — volta em 8 min", pedido)
                    continue
                d["pausou"] = False
                d["retomadas"] = d.get("retomadas", 0) + 1
                texto = ("Continue de onde parou, seguindo as mesmas instruções, até pôr o filme na fila de "
                         "render+entrega (ou marcar esperando_voce se precisar do usuário).")
                # 06/10/2026: ordem do usuário para ESTE filme (o Claude do chat grava fila/<id>/instrucao_gerente.txt)
                ordem = HERE / "fila" / pedido / "instrucao_gerente.txt"
                if ordem.exists():
                    texto += "\n\nORDEM DO USUÁRIO (vale mais que o plano anterior):\n" + ordem.read_text("utf-8").strip()
                    ordem.replace(ordem.with_suffix(".lida"))
                d["ultima"] = abrir_sessao("diretor", pedido, d["baia"], texto, resume=ult["claude_session"])
                if not d["ultima"]:
                    d["fase"] = "parado"
                    F.estado(pedido, p.get("etapa") or "preparando", status="esperando_voce",
                             msg="Não foi possível retomar a IA. Confira a Central e tente novamente.")
            else:
                d["fase"] = "parado"
                F.estado(pedido, p.get("etapa") or "preparando", status="esperando_voce",
                         msg="O diretor parou antes de terminar. Confira o log na Central para retomar.")
                feed("gerente", "o diretor parou sem terminar — confira o log", pedido)
        if d["fase"] == "parado" and st == "na_fila":     # alguém devolveu o pedido para a fila: pega de novo
            del EST["pedidos"][pedido]
            feed("gerente", "pedido voltou para a fila — vai ser pego de novo", pedido)
            continue
        if d["fase"] == "render" and st == "esperando_voce":
            # 08/10/2026 (pedido do usuário): filme pronto parado 1-5 h esperando alguém ver (Incas: audio_qa 0,1 dB;
            # Chiny: script de miniatura) -> o Diretor do filme reabre a própria sessão, conserta e reenvia
            ult = EST["sessoes"].get(d.get("ultima"), {})
            if d.get("consertos", 0) < MAX_CONSERTOS and ult.get("claude_session") and ligado():
                d["consertos"] = d.get("consertos", 0) + 1
                feed("operador", f"o render parou ({p.get('msg', '')}) — o diretor vai consertar (tentativa {d['consertos']})", pedido)
                sid = abrir_sessao("diretor", pedido, d["baia"], CONSERTO.replace("{MSG}", p.get("msg", "") or "sem mensagem"),
                                   resume=ult["claude_session"])
                if sid:
                    # etapa "conferir" (não "render"): se o Diretor sair sem terminar, a retomada normal o chama de novo
                    F.estado(pedido, "conferir", status="produzindo", msg="o render parou — o diretor está consertando sozinho")
                    d["ultima"] = sid
                    d["fase"] = "diretor"
                    d["retomadas"] = 0
                    d["pausou"] = False
                    continue
            d["fase"] = "parado"
            feed("operador", f"o render parou: {p.get('msg', '')}", pedido)
            continue
        if d["fase"] == "render" and st == "entregue" and "revisado" not in (p.get("msg") or "") and not ativa:
            if d.get("rodada", 0) >= MAX_RODADAS:
                d["fase"] = "feito"
                feed("revisora", "entregue — a revisão foi feita antes do render", pedido)
                try:   # 12/10/2026: sem revisora pós-entrega, as miniaturas do Flow (pautas) são copiadas aqui
                    _sl = pasta_baia(d["baia"]) / "data" / "gerente_slug.txt"
                    _sl = _sl.read_text("utf-8").strip() if _sl.exists() else pedido
                    n_t = _pautas().copia_thumbs(pedido, _sl)
                    if n_t:
                        feed("gerente", f"{n_t} miniaturas do Flow colocadas na entrega", pedido)
                except Exception as ex:  # noqa: BLE001
                    feed("gerente", f"miniaturas do Flow não copiadas: {ex}", pedido)
                continue
            d["rodada"] = d.get("rodada", 0) + 1
            slug = (pasta_baia(d["baia"]) / "data" / "gerente_slug.txt")
            slug = slug.read_text("utf-8").strip() if slug.exists() else pedido
            d["slug"] = slug
            try:   # 07/10/2026: miniaturas do Flow (pautas) entram na pasta da entrega antes da revisora
                n_t = _pautas().copia_thumbs(pedido, slug)
                if n_t:
                    feed("gerente", f"{n_t} miniaturas do Flow colocadas na entrega", pedido)
            except Exception as ex:  # noqa: BLE001
                feed("gerente", f"miniaturas do Flow: {ex}", pedido)
            d["fase"] = "revisao"
            d["ultima"] = abrir_sessao("revisora", pedido, d["baia"],
                                       preencher("revisora_final.md", SLUG=slug, RODADA=d["rodada"], **ctx(pedido, d["baia"])))
            if not d["ultima"]:   # 06/10/2026: sem claude.exe a revisão NÃO aconteceu — não marcar "revisado"
                d["fase"] = "render"
                d["rodada"] -= 1
                continue
            continue   # 06/10/2026: a revisora acabou de abrir — o resultado só é lido no próximo passo, quando ela terminar
        if d["fase"] == "revisao" and not ativa:
            p = F.pedido(pedido) or {}
            if p.get("status") == "entregue":
                d["fase"] = "feito"
                feed("revisora", "entregue e revisado", pedido)
            elif p.get("etapa") == "render":
                d["fase"] = "render"
                feed("revisora", "achou defeito, consertou e mandou de novo para o render", pedido)
            else:
                d["fase"] = "parado"
    try:   # 07/10/2026: pautas automáticas (pesquisador + roteirista) — nunca derruba o gerente
        passo_pautas()
    except Exception as ex:  # noqa: BLE001
        feed("gerente", f"erro nas pautas: {ex}")
    # pedido novo
    if ligado():
        ativos = [d for d in EST["pedidos"].values() if d["fase"] in ("diretor", "render", "revisao") and d.get("baia") != "s3d"]
        # 06/11/2026: SHORT 3D tem mesa própria (pasta claude-shorts-3d, 1 por vez) e não ocupa b1/b2
        s3d = sorted([p for p in F.todos() if p.get("status") == "na_fila" and p.get("formato") == "short3d"
                      and p["id"] not in EST["pedidos"]], key=lambda p: (p.get("ordem", 9999), p["id"]))
        if s3d and "s3d" not in baias_ocupadas():
            p = s3d[0]
            if not (shorts3d_dir() / "package.json").exists():
                F.estado(p["id"], "preparando", status="esperando_voce",
                         msg=f"o projeto dos shorts 3D não está instalado em {shorts3d_dir()}")
            else:
                reg = F.pedido(p["id"])
                reg["baia"] = "s3d"
                F.salva(reg)
                F.estado(p["id"], "preparando", status="produzindo", msg="o Animador pegou o short 3D", pct=2)
                EST["pedidos"][p["id"]] = {"baia": "s3d", "fase": "diretor", "inicio": agora(), "titulo": p.get("titulo", "")}
                EST["pedidos"][p["id"]]["ultima"] = abrir_sessao("diretor", p["id"], "s3d",
                                                                 preencher("short3d.md", **ctx(p["id"], "s3d")))
        if len(ativos) < MAX_BAIAS:
            livres = [b for b in ("b1", "b2") if b not in baias_ocupadas()]
            fila = sorted([p for p in F.todos() if p.get("status") == "na_fila" and p["id"] not in EST["pedidos"]
                           and p.get("formato") != "short3d"],
                          key=lambda p: (p.get("ordem", 9999), p["id"]))
            # 07/10/2026: baias ESCALONADAS — 2 filmes buscando material juntos dividiam a cota do YouTube e os dois
            # ficavam ~2 h baixando 1 vídeo a cada 5 min. O 2º só começa quando o 1º passou da busca (ou após 90 min).
            buscando = [pid for pid, d in EST["pedidos"].items() if d["fase"] == "diretor"
                        and (F.pedido(pid) or {}).get("etapa") in ("preparando", "roteiro", "material", "julgar_fotos")
                        and agora() - d.get("inicio", 0) < 90 * 60]
            if ESCALONAR and livres and fila and buscando:
                if EST.get("_escalonado") != fila[0]["id"]:
                    EST["_escalonado"] = fila[0]["id"]
                    feed("gerente", "próximo filme espera o atual terminar a busca de material (cota do YouTube)", fila[0]["id"])
            elif livres and fila:
                p, b = fila[0], livres[0]
                reg = F.pedido(p["id"])
                reg["baia"] = b
                F.salva(reg)
                F.estado(p["id"], "preparando", status="produzindo", msg=f"o Diretor pegou o filme (baia {b})", pct=2)
                EST["pedidos"][p["id"]] = {"baia": b, "fase": "diretor", "inicio": agora(), "titulo": p.get("titulo", "")}
                sid = abrir_sessao("diretor", p["id"], b, preencher("diretor.md", **ctx(p["id"], b)))
                EST["pedidos"][p["id"]]["ultima"] = sid
                if not sid:
                    EST["pedidos"][p["id"]]["fase"] = "parado"
                    F.estado(p["id"], "preparando", status="esperando_voce",
                             msg="Não foi possível iniciar a IA. Confira o Claude e a Central antes de retomar.")
    with LOCK:
        grava(ESTADO, EST)
    VIVO.write_text(str(agora()))


TRAVA = HERE / ".gerente_pid"


def so_um():
    """05/10/2026: dois gerentes (painel aberto 2x) pegariam o MESMO pedido. Só o primeiro fica; os outros saem."""
    try:
        outro = int(TRAVA.read_text().strip())
    except Exception:  # noqa: BLE001
        outro = 0
    if outro and outro != os.getpid() and vivo_pid(outro) and "--assumir" not in sys.argv:
        print(f"[gerente] já existe um gerente no escritório (pid {outro}) — este aqui fecha.", flush=True)
        time.sleep(4)
        sys.exit(0)
    TRAVA.write_text(str(os.getpid()))


MT0 = Path(__file__).stat().st_mtime


def reinicia_se_mudou():
    """05/10/2026: gerente.py editado entra sozinho — mas só quando NENHUMA sessão está aberta (o leitor do stream é
    este processo; reiniciar no meio cortaria o Diretor)."""
    if Path(__file__).stat().st_mtime == MT0:
        return
    if any(not s.get("fim") for s in EST["sessoes"].values()):
        return
    with LOCK:
        grava(ESTADO, EST)
    feed("gerente", "trocou de turno (gerente atualizado)")
    with LOCK:
        grava(ESTADO, EST)
    if os.environ.get("GERENTE_LOOP"):   # 06/10/2026: rodando pelo Agendador — o laço do gerente_fundo.bat religa
        sys.exit(0)
    # 06/10/2026: SEM janela — a janela preta nova era fechada e levava junto o gerente e os Diretores (5 h perdidas)
    try:   # 17/10/2026: o laço do .bat segura o gerente_console.log (>>) — sem acesso, o novo gerente sobe sem log
        log = open(HERE / "gerente_console.log", "a", encoding="utf-8")
    except OSError:
        log = subprocess.DEVNULL
    subprocess.Popen([sys.executable, "-u", str(Path(__file__)), "--assumir"], cwd=str(PRINCIPAL),
                     stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                     creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    time.sleep(3)
    sys.exit(0)


def ignora_ctrl():
    """17/10/2026: as quedas vinham 20-50 s depois de um Diretor rodar comando com sleep/timeout — suspeita: o Ctrl+C/
    Ctrl+Break que o claude.exe manda ao cortar o comando chega a todo processo do mesmo console (gerente e o laço).
    O gerente passa a ignorar esses dois sinais (fechar a janela/desligar o PC continua encerrando)."""
    import signal
    for nome in ("SIGINT", "SIGBREAK"):
        if hasattr(signal, nome):
            try:
                signal.signal(getattr(signal, nome), signal.SIG_IGN)
            except Exception:  # noqa: BLE001
                pass
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleCtrlHandler(None, True)   # ignora CTRL_C_EVENT no console
    except Exception:  # noqa: BLE001
        pass


_LIC_AVISO = [0.0]


def licenca_ok():
    """06/11/2026: no pacote vendido (painel/licenca_config.json) o gerente não começa nem continua filme sem licença
    ativa. No PC do dono não existe licenca_config.json e isto é sempre True."""
    try:
        import licenca
        e = licenca.estado()
    except Exception as ex:  # noqa: BLE001
        print("[gerente] licença:", ex, flush=True)
        return False
    if e.get("ativa"):
        return True
    if agora() - _LIC_AVISO[0] > 1800:
        _LIC_AVISO[0] = agora()
        feed("gerente", "parado: licença inativa — " + (e.get("motivo") or "ative a Sala no painel"))
    return False


def main():
    ignora_ctrl()
    so_um()
    old = jl(ESTADO, {})
    EST["pedidos"] = old.get("pedidos", {})
    EST["sessoes"] = old.get("sessoes", {})
    EST["feed"] = old.get("feed", [])[-60:]
    for sid, s in EST["sessoes"].items():   # 17/10/2026: sessões soltas que sobreviveram à queda do gerente
        if not s.get("fim") and s.get("log") and Path(s["log"]).exists() and vivo_pid(s.get("pid"), exe_da_sessao(s)):
            threading.Thread(target=ler_stream, args=(sid, None, s["log"], s["pid"], Path(s["log"]).stat().st_size),
                             daemon=True).start()
            print(f"[gerente] voltei a acompanhar a sessão {sid} (pid {s['pid']}) que continuou trabalhando", flush=True)
    exe = MOTOR.codex_exe() if MOTOR.qual() == "codex" else claude_exe()
    print(f"[gerente] ligado em {PRINCIPAL} | motor {MOTOR.qual()}: {exe} | modo automático do painel: {'SIM' if ligado() else 'NÃO'}", flush=True)
    feed("gerente", "chegou no escritório")
    if "--uma-vez" in sys.argv:
        passo()
        return
    while True:
        try:
            if not licenca_ok():
                time.sleep(30)
                continue
            passo()
            reinicia_se_mudou()
        except SystemExit:
            raise
        except Exception as ex:  # noqa: BLE001
            feed("gerente", f"erro no gerente: {ex}")
            print("[gerente] erro:", ex, flush=True)
        for _ in range(10):   # grava o estado a cada 1 s enquanto as sessões trabalham
            time.sleep(1)
            with LOCK:
                grava(ESTADO, EST)
            VIVO.write_text(str(agora()))


if __name__ == "__main__":
    main()
