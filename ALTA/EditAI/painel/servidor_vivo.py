"""07/10/2026 — o painel (servidor.py, porta 8876) caiu quando a janela "Edit.AI by Galvao" foi fechada. O vigia do
Agendador (gerente_fundo.bat, a cada 5 min) chama isto: se a porta não responde, liga o servidor escondido, sem
janela (log em painel/servidor_console.log). Assim o painel pode ser aberto em qualquer navegador, inclusive o do Claude."""
import socket, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
try:
    socket.create_connection(("127.0.0.1", 8876), timeout=3).close()
    sys.exit(0)
except OSError:
    pass
log = open(HERE / "servidor_console.log", "a", encoding="utf-8")
subprocess.Popen([sys.executable, "-u", str(HERE / "servidor.py"), "--sem-navegador"], cwd=str(HERE.parent), stdout=log,
                 stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
print("servidor do painel religado")
