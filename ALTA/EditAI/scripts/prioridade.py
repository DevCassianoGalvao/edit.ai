"""Prioridade BAIXA para as etapas leves (download, corte de clipes, recorte 2.5D, pré-filtro) — 04/10/2026.

O render do crédito rural levou 40 min em vez de 33 porque a outra baia baixava fotos, cortava clipes e recortava
paralaxe ao mesmo tempo, disputando a CPU. O render continua em prioridade NORMAL (regra do PC: nada acima de normal);
estas etapas descem para BELOW_NORMAL e os filhos (ffmpeg) herdam. Com o PC livre, a diferença é nenhuma.

Uso no topo do script:  import prioridade  # noqa: F401
"""
import os
import sys

if sys.platform == "win32" and not os.environ.get("SEM_PRIORIDADE_BAIXA"):
    try:
        import ctypes
        BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:  # noqa: BLE001
        pass
