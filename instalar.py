"""INSTALADOR do Dark Empire Videos — 07/10/2026 (nome novo 06/11/2026).

Roda no PC NOVO, de dentro da pasta descompactada do pacote:   python instalar.py   (ou dê dois cliques em INSTALAR.bat)

O que faz:
  1. copia a ferramenta para <Área de Trabalho>\\CLAUDE CODE ALTA PRODUÇÃO (painel, scripts, funcionários, regras, chaves)
  2. copia a pasta de trabalho do Claude para <usuário>\\Downloads\\mapa (agentes .claude\\agents + relatórios + prompts)
  3. põe a memória do Claude (as regras aprendidas) no lugar certo deste usuário
  4. põe as chaves pessoais (.pexels_key, .pixabay_key, .dvids_key) na pasta do usuário
  5. troca os caminhos do PC antigo pelos deste PC em todos os arquivos de texto
  6. instala as bibliotecas Python (requirements.txt) e as do vídeo (npm ci)
  7. (opcional) cria as tarefas do Agendador que religam o gerente e o painel sozinhos
  8. cria o atalho do APP (Central) na Área de Trabalho e, se quiser, abre o app junto com o Windows
Nada é apagado. Se a pasta de destino já existir, o instalador para e pergunta.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGEM = json.loads((AQUI / "ORIGEM.json").read_text("utf-8"))
TEXTO = {".py", ".md", ".txt", ".json", ".sh", ".bat", ".vbs", ".html", ".mjs", ".js", ".ts", ".tsx", ".ps1", ".cfg", ".csv", ".jsonl"}


def ps(cmd):
    r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip()


def pergunta(txt, padrao="s"):
    r = input(f"{txt} [{'S/n' if padrao == 's' else 's/N'}] ").strip().lower()
    return (r or padrao).startswith("s")


def tem(cmd):
    return shutil.which(cmd) is not None


def main():
    home = Path(os.environ["USERPROFILE"])
    desktop = Path(os.environ.get("SALA_DESKTOP") or ps("[Environment]::GetFolderPath('Desktop')") or home / "Desktop")
    teste = os.environ.get("SALA_TESTE") == "1"   # teste do instalador: sem pip/npm/Agendador
    alta = desktop / ORIGEM["nome_alta"]
    mapa = home / "Downloads" / "mapa"
    slug = str(mapa).replace(":", "-").replace("\\", "-").replace("/", "-")
    memoria = home / ".claude" / "projects" / slug / "memory"
    print("=" * 70)
    print(" Dark Empire Videos — instalação")
    print("=" * 70)
    print(f" ferramenta  -> {alta}\n pasta Claude -> {mapa}\n memória     -> {memoria}\n chaves      -> {home}")
    print()
    print(" Antes, confira se este PC tem: Python 3.12+, Node.js 20+, Git for Windows (Git Bash), ffmpeg no PATH,")
    print(" o app do Claude (desktop) logado e, para miniaturas no Flow, o Chrome com a extensão do Claude.")
    faltam = [n for n, c in (("Node.js (node)", "node"), ("npm", "npm"), ("ffmpeg", "ffmpeg"), ("Git Bash (bash)", "bash")) if not tem(c)]
    if faltam:
        print(f"\n ATENÇÃO: não achei no PATH: {', '.join(faltam)} — instale antes (ver LEIA-ME_INSTALACAO.md).")
        if not pergunta(" Continuar mesmo assim?", "n"):
            return
    if not pergunta("\n Instalar agora?"):
        return
    for alvo in (alta, mapa / ".claude" / "agents"):
        if alvo.exists() and any(alvo.iterdir()):
            if not pergunta(f"\n {alvo} já existe. Copiar por cima (arquivos com o mesmo nome são substituídos)?", "n"):
                return

    print("\n[1/8] copiando a ferramenta…")
    shutil.copytree(AQUI / "ALTA", alta, dirs_exist_ok=True)
    for d in ("yt milionario teste/entregas", "yt milionario teste/input", "yt milionario teste/out", "yt milionario teste/qa",
              "yt milionario teste/public/stock", "yt milionario teste/painel/fila", "yt milionario teste/painel/pautas",
              "yt milionario teste/painel/gerente_logs", "baias", "banco", "chaves"):
        (alta / d).mkdir(parents=True, exist_ok=True)
    if (AQUI / "CHAVES_COMO_COLOCAR.txt").exists():   # pacote limpo: sem chaves — deixa o passo a passo na pasta certa
        shutil.copy2(AQUI / "CHAVES_COMO_COLOCAR.txt", alta / "chaves" / "LEIA-ME.txt")
    print("[2/8] copiando a pasta de trabalho do Claude (mapa) e os agentes…")
    shutil.copytree(AQUI / "MAPA", mapa, dirs_exist_ok=True)
    print("[3/8] memória do Claude (regras)…")
    memoria.mkdir(parents=True, exist_ok=True)
    for f in (AQUI / "MEMORIA").glob("*.md"):
        shutil.copy2(f, memoria / f.name)
    print("[4/8] chaves pessoais…")
    for f in (AQUI / "HOME").glob(".*"):
        shutil.copy2(f, home / f.name)

    print("[5/8] trocando os caminhos do PC antigo pelos deste…")
    trocas = [
        (ORIGEM["alta"], str(alta)), (ORIGEM["alta"].replace("\\", "/"), str(alta).replace("\\", "/")),
        ("/c/" + ORIGEM["alta"][3:].replace("\\", "/"), "/" + str(alta)[0].lower() + "/" + str(alta)[3:].replace("\\", "/")),
        (ORIGEM["mapa"], str(mapa)), (ORIGEM["mapa"].replace("\\", "/"), str(mapa).replace("\\", "/")),
        (ORIGEM["slug"], slug),
        (ORIGEM["home"], str(home)), (ORIGEM["home"].replace("\\", "/"), str(home).replace("\\", "/")),
        (ORIGEM["home"].replace("\\", "\\\\"), str(home).replace("\\", "\\\\")),
    ]
    trocas = [(a, b) for a, b in trocas if a and a != b]
    n = 0
    if trocas:
        for raiz in (alta, mapa, memoria):
            for f in raiz.rglob("*"):
                if f.is_file() and f.suffix.lower() in TEXTO and "node_modules" not in f.parts:
                    try:
                        t = f.read_text("utf-8")
                    except (UnicodeDecodeError, OSError):
                        continue
                    t2 = t
                    for a, b in trocas:
                        t2 = t2.replace(a, b)
                    if t2 != t:
                        f.write_text(t2, "utf-8"); n += 1
    print(f"      {n} arquivos ajustados" if trocas else "      mesmo usuário e mesma pasta — nada a trocar")

    print("[6/8] bibliotecas Python e do vídeo (pode levar 10-20 min)…")
    if teste:
        print("      (teste: pulado)")
    else:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(AQUI / "requirements.txt")])
    if teste:
        pass
    elif tem("npm"):
        subprocess.run("npm ci", cwd=str(alta / "yt milionario teste"), shell=True)
    else:
        print("      npm não encontrado — depois de instalar o Node.js rode: npm ci  (dentro de 'yt milionario teste')")

    print("[7/8] tarefas do Agendador (gerente e painel voltam sozinhos se caírem)")
    if not teste and pergunta(" Criar as tarefas agora?"):
        painel = alta / "yt milionario teste" / "painel"
        for nome, vbs, repete in (("SalaMontagem Gerente", "gerente_escondido.vbs", True), ("SalaMontagem Painel", "painel_escondido.vbs", True)):
            limite = "([TimeSpan]::Zero)" if nome.endswith("Gerente") else "(New-TimeSpan -Minutes 2)"
            ps(f"""$a = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument '"{painel / vbs}"' -WorkingDirectory '{alta / "yt milionario teste"}'
$t1 = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\\$env:USERNAME"
$t2 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$c = New-ScheduledTaskSettingsSet -ExecutionTimeLimit {limite} -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -StartWhenAvailable
$p = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName '{nome}' -Action $a -Trigger $t1,$t2 -Settings $c -Principal $p -Force | Out-Null""")
            print(f"      tarefa '{nome}' criada")

    print("[8/8] atalho do app (Central: saúde, avisos, botões de recuperação)")
    painel = alta / "yt milionario teste" / "painel"
    vbs, ico = painel / "app" / "SalaMontagem.vbs", painel / "app" / "sala.ico"
    alvos = [desktop / "Dark Empire Videos.lnk"]
    if not teste and pergunta(" Abrir o app sozinho quando o Windows entrar?"):
        alvos.append(Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Dark Empire Videos.lnk")
    for lnk in alvos:
        if teste:
            break
        ps(f"""$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk}');$s.TargetPath='wscript.exe';$s.Arguments='"{vbs}"';
$s.WorkingDirectory='{alta / "yt milionario teste"}';$s.IconLocation='{ico}';$s.Save()""")
        print(f"      atalho: {lnk}")

    print("\n" + "=" * 70)
    print(" PRONTO. Próximos passos (ver LEIA-ME_INSTALACAO.md):")
    print(f"  1. Abra o app do Claude, aba Code, e abra a pasta {mapa}")
    print("  2. Escreva:  painel   — o Claude abre o painel (http://127.0.0.1:8765) e segue o protocolo")
    print("  3. Ou dê dois cliques em 'Dark Empire Videos' na Área de Trabalho (abre a Central com tudo ligado)")
    if (AQUI / "CHAVES_COMO_COLOCAR.txt").exists():
        print(f"  4. FALTAM AS SUAS CHAVES (este pacote não leva chaves): siga {alta / 'chaves' / 'LEIA-ME.txt'}")
        print("  5. Cadastre seus canais: veja 'canais.exemplo.json' em yt milionario teste/painel (o painel começa sem canais)")
    print("  6. Antivírus (360 etc.): ponha exceção para a pasta da ferramenta, o python.exe, o claude.exe e o codex.exe")
    print("  7. Prefere o ChatGPT? Instale o app do Codex, entre na conta e escolha 'ChatGPT Codex' na aba Chaves do painel")
    print("=" * 70)
    if not teste:
        input("\nEnter para fechar…")


if __name__ == "__main__":
    main()
