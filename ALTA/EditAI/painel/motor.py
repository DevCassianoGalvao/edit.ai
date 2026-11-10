"""MOTOR — qual IA faz o trabalho dos funcionários (06/11/2026, pedido do usuário: "que essa ferramenta possa ser usada
com o ChatGPT Codex também").

painel/config.json "motor": "claude" (padrão) | "codex". O gerente abre cada Diretor/Revisora/Roteirista com o motor
escolhido NA HORA de abrir; a sessão em andamento continua no motor em que nasceu. Ao mudar de motor, uma retomada
inicia uma nova sessão com o contexto e os arquivos do projeto; identificadores de sessão não são compartilhados.

- claude: claude.exe do app do Claude (conta do usuário), `-p --output-format stream-json`.
- codex : codex.exe do app do Codex / `npm i -g @openai/codex` (conta do ChatGPT), `codex exec --json`.
  O Codex não tem a memória automática nem as ferramentas Read/Agent do Claude: o gerente põe ADAPTADOR na frente do
  prompt (onde está a memória, como ver imagem, como chamar os funcionários) e este módulo mantém .codex/agents/*.toml
  iguais aos .claude/agents/*.md (juiz-fotos, juiz-video, revisora, pesquisador).

  python painel/motor.py              # mostra o estado
  python painel/motor.py usar codex   # troca o motor
  python painel/motor.py agentes      # regrava .codex/agents a partir de .claude/agents
"""
import glob, json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.json"
MOTORES = ("claude", "codex")


def _jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def qual():
    m = str(_jl(CONFIG, {}).get("motor") or "claude").lower()
    return m if m in MOTORES else "claude"


def usar(m):
    m = str(m or "").lower()
    if m not in MOTORES:
        return {"ok": False, "erro": "motor desconhecido"}
    cfg = _jl(CONFIG, {})
    cfg["motor"] = m
    tmp = CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), "utf-8")
    os.replace(tmp, CONFIG)
    return {"ok": True, **estado()}


def codex_exe():
    """codex.exe: config.json "codex_exe" > app do Codex (LOCALAPPDATA/OpenAI/Codex/bin/<hash>) > npm global > PATH."""
    cfg = _jl(CONFIG, {}).get("codex_exe")
    if cfg and Path(cfg).exists():
        return cfg
    achados = []
    for b in {os.environ.get("LOCALAPPDATA", ""), str(Path.home() / "AppData" / "Local")}:
        if b:
            achados += glob.glob(os.path.join(b, "OpenAI", "Codex", "bin", "*", "codex.exe"))
    for b in {os.environ.get("APPDATA", ""), str(Path.home() / "AppData" / "Roaming")}:
        if b:
            achados += glob.glob(os.path.join(b, "npm", "node_modules", "@openai", "codex", "**", "codex.exe"), recursive=True)
    if achados:
        return max(set(achados), key=lambda p: os.path.getmtime(p))   # o mais novo (o app se atualiza sozinho)
    w = shutil.which("codex.exe") or shutil.which("codex")
    return w


def codex_logado():
    home = Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
    return (home / "auth.json").exists()


def claude_achado():
    try:
        sys.path.insert(0, str(HERE))
        import gerente as G   # noqa: PLC0415
        return bool(G.claude_exe())
    except Exception:  # noqa: BLE001
        return False


def estado():
    cx = codex_exe()
    return {"motor": qual(), "claude": {"instalado": claude_achado()},
            "codex": {"instalado": bool(cx), "logado": codex_logado(), "exe": Path(cx).name if cx else None}}


# ------------------------------------------------------------------ agentes do Codex (.codex/agents/*.toml)
def _toml_str(s):
    s = s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return '"""\n' + s.strip() + '"""'


def sincroniza_agentes(mapa):
    """.claude/agents/<nome>.md (frontmatter name/description + corpo) -> .codex/agents/<nome>.toml. Só regrava o que mudou."""
    mapa = Path(mapa)
    origem, destino = mapa / ".claude" / "agents", mapa / ".codex" / "agents"
    if not origem.exists():
        return []
    destino.mkdir(parents=True, exist_ok=True)
    feitos = []
    for md in sorted(origem.glob("*.md")):
        t = md.read_text("utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", t, re.S)
        if not m:
            continue
        cab, corpo = m.group(1), m.group(2)
        campo = lambda k: (re.search(rf"^{k}:\s*(.+)$", cab, re.M) or [None, ""])[1].strip()
        nome = campo("name") or md.stem
        corpo = corpo.replace("com Read (imagem)", "com view_image (imagem)").replace("com Read", "com view_image")
        toml = (f'name = {json.dumps(nome, ensure_ascii=False)}\n'
                f'description = {json.dumps(campo("description"), ensure_ascii=False)}\n'
                f'developer_instructions = {_toml_str(corpo)}\n')
        alvo = destino / f"{nome}.toml"
        if not alvo.exists() or alvo.read_text("utf-8") != toml:
            alvo.write_text(toml, "utf-8")
            feitos.append(nome)
    return feitos


def memoria_dir(mapa):
    return Path(mapa).resolve().parent / "MEMORIA"


def bash_exe():
    for c in (r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files (x86)\Git\bin\bash.exe", shutil.which("bash.exe")):
        if c and Path(c).exists() and "system32" not in c.lower():
            return c
    return "bash"


def adaptador(mapa):
    """Vai NA FRENTE de todo prompt quando o motor é o Codex: traduz o que os prompts (escritos para o Claude) pressupõem."""
    mem = str(memoria_dir(mapa)).replace("\\", "/")
    ag = str(Path(mapa) / ".claude" / "agents").replace("\\", "/")
    bash = bash_exe().replace("\\", "/")
    return f"""[ADAPTADOR CODEX — Edit.AI by Galvão]
As instruções abaixo foram escritas para o Claude Code; você é o Codex fazendo o MESMO trabalho, sozinho, sem ninguém
no chat. Traduza assim:
- MEMÓRIA: "a sua memória" / MEMORY.md = `{mem}/MEMORY.md` e os arquivos .md citados nele (mesma pasta). Leia o
  MEMORY.md logo no começo; abra os arquivos citados quando o assunto bater. Lições novas que o prompt mandar anotar:
  grave lá, no mesmo formato.
- COMANDOS: os comandos das instruções são de BASH (nohup, &&, $(...), timeout, sleep). Rode-os pelo Git Bash:
  `& "{bash}" -lc '<comando>'` (o seu shell padrão é PowerShell). Comando "destacado" (nohup ... &) que precisa
  sobreviver a você: `Start-Process -WindowStyle Hidden -FilePath "{bash}" -ArgumentList '-lc','<comando sem o & final>'`.
- IMAGENS: "abra/olhe/Read" uma imagem (folhas de contato .jpg/.png, qa/*.jpg) = ferramenta view_image. Olhe de
  verdade cada folha que as instruções mandam conferir.
- FUNCIONÁRIOS (ferramenta Agent / subagent_type "juiz-fotos", "juiz-video", "revisora", "pesquisador"): use
  spawn_agent com o agente de mesmo nome (definidos em .codex/agents; o texto original está em `{ag}/<nome>.md`),
  vários em paralelo quando as instruções pedirem, e espere com wait_agent. Se spawn_agent não existir, faça você
  mesmo o trabalho de cada funcionário seguindo `{ag}/<nome>.md`.
- WebSearch/WebFetch = a sua ferramenta de busca/leitura na web. Skills citadas por caminho (~/.claude/skills/...,
  painel/prompts/skills/...) = leia o arquivo e siga.
- Nunca imprima chaves; nunca apague de vez (Lixeira/APAGAR_*); não peça confirmação a ninguém — decida e siga.
[FIM DO ADAPTADOR]

"""


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    a = sys.argv[1:]
    if a[:1] == ["usar"] and len(a) > 1:
        print(json.dumps(usar(a[1]), ensure_ascii=False, indent=1))
    elif a[:1] == ["agentes"]:
        mapa = Path(a[1]) if len(a) > 1 else HERE.parent.parent.parent / "MAPA"
        print("regravados:", sincroniza_agentes(mapa) or "nenhum (já iguais)")
    else:
        print(json.dumps(estado(), ensure_ascii=False, indent=1))
