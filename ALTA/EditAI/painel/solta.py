"""SOLTA — lança um processo ÓRFÃO e sai na hora (17/10/2026).

Por que: a cada 20-40 min alguma coisa matava de uma vez TODA a árvore de processos que descende do serviço do
Agendador do Windows (gerente + laço + sessões dos diretores + render em tarefa própria + tarefas dos diretores), sempre
40-50 s depois de um Diretor começar um comando com espera (18:28, 18:50, 19:24, 20:12, 20:51). O que sobrevivia sempre
era o servidor do painel — justamente porque o servidor_vivo.py o lança e sai, deixando-o órfão (sem caminho de pais
até o serviço). Este script faz o mesmo para qualquer comando: tarefa -> solta.py (sai) -> comando órfão.

Uso: python solta.py <programa> [args...]
"""
import subprocess
import sys

NOVO_GRUPO = 0x00000200     # CREATE_NEW_PROCESS_GROUP
SEM_JANELA = 0x08000000     # CREATE_NO_WINDOW

if len(sys.argv) < 2:
    sys.exit(__doc__)
flags = NOVO_GRUPO | SEM_JANELA
kwargs = dict(close_fds=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    subprocess.Popen(sys.argv[1:], creationflags=flags | 0x01000000, **kwargs)  # CREATE_BREAKAWAY_FROM_JOB
except OSError:
    subprocess.Popen(sys.argv[1:], creationflags=flags, **kwargs)
