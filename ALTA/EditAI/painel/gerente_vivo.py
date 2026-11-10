"""07/10/2026 — sai com 0 se já existe um gerente vivo (painel/.gerente_pid aponta para um python.exe), 1 se não.
Usado pelo gerente_fundo.bat (tarefa "EditAI Gerente" do Agendador, a cada 5 min) para só religar quando caiu."""
import subprocess, sys
from pathlib import Path

try:
    pid = int((Path(__file__).resolve().parent / ".gerente_pid").read_text().strip())
except Exception:  # noqa: BLE001
    sys.exit(1)
r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True,
                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
vivo = any(l.split()[:2] == ["python.exe", str(pid)] for l in r.stdout.lower().splitlines() if l.strip())
sys.exit(0 if vivo else 1)
