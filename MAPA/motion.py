# -*- coding: utf-8 -*-
"""
motion.py - lado servidor do MOTION GRAPHICS do THANOS 3.0.

O desenho das cenas acontece no navegador (motion.js, em Canvas 2D). Este
arquivo faz a parte que o navegador nao consegue: receber os quadros um a um,
guardar no disco e chamar o ffmpeg pra virar um MP4 de verdade.

Por que quadro a quadro e nao gravacao de tela: gravar a tela (MediaRecorder)
depende do computador dar conta em tempo real - se engasgar, o video sai com
quadro perdido e movimento tremido. Desenhando quadro a quadro, cada imagem e
gerada com o tempo EXATO dela (0/30s, 1/30s, 2/30s...), entao o resultado e
identico em qualquer maquina, rapida ou lenta.

O MP4 sai em 1920x1080, 30fps, H.264 yuv420p - o mesmo formato dos videos
baixados do YouTube e do Pexels, pra montagem final nao precisar reconverter.
"""

import json
import os
import re
import shutil
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(ROOT, "downloads")
TEMP = os.path.join(DOWNLOADS, "_motion_tmp")

_NOWIN = {}
if os.name == "nt":
    _si = subprocess.STARTUPINFO()
    _si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _NOWIN = {"startupinfo": _si, "creationflags": 0x08000000}


def _seguro(nome, padrao):
    nome = re.sub(r"[^\w\- ]+", "_", str(nome or "")).strip().strip(".")
    return nome or padrao


def _pasta_job(job):
    job = re.sub(r"[^A-Za-z0-9_\-]", "", str(job or ""))[:40]
    if len(job) < 4:
        raise ValueError("id de trabalho invalido")
    return os.path.join(TEMP, job)


def receber_quadro(job, indice, dados):
    """Grava um quadro JPEG vindo do navegador."""
    if not dados or len(dados) < 500:
        raise ValueError("quadro vazio")
    pasta = _pasta_job(job)
    os.makedirs(pasta, exist_ok=True)
    n = max(int(indice), 0)
    with open(os.path.join(pasta, "%06d.jpg" % n), "wb") as f:
        f.write(dados)
    return n


def montar(job, fps=30, folder="", filename="motion"):
    """
    Junta os quadros do trabalho num MP4 e joga na pasta do paragrafo, do lado
    das imagens e videos daquele trecho - assim o sincronizar.py encontra tudo
    no mesmo lugar, sem saber nem que existe motion graphics.
    """
    pasta = _pasta_job(job)
    if not os.path.isdir(pasta):
        return {"ok": False, "message": "nenhum quadro foi recebido"}

    quadros = sorted(x for x in os.listdir(pasta) if x.endswith(".jpg"))
    if len(quadros) < 2:
        return {"ok": False, "message": "quadros de menos (%d)" % len(quadros)}

    destino_dir = os.path.join(DOWNLOADS, _seguro(folder, "motion"))
    os.makedirs(destino_dir, exist_ok=True)
    base = _seguro(filename, "motion")[:55]
    destino = os.path.join(destino_dir, base + ".mp4")

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-framerate", str(int(fps or 30)),
        "-i", os.path.join(pasta, "%06d.jpg"),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "17",                 # praticamente sem perda visivel
        "-pix_fmt", "yuv420p",        # o unico que toca em qualquer lugar
        "-r", str(int(fps or 30)),
        "-movflags", "+faststart",
        destino,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=600, **_NOWIN)
    except subprocess.TimeoutExpired:
        return {"ok": False, "message": "o ffmpeg demorou demais"}
    finally:
        shutil.rmtree(pasta, ignore_errors=True)

    if p.returncode != 0 or not os.path.isfile(destino):
        erro = (p.stderr or b"").decode("utf-8", "ignore").strip().splitlines()
        return {"ok": False, "message": erro[-1][:220] if erro else "o ffmpeg falhou"}

    return {
        "ok": True,
        "path": os.path.relpath(destino, ROOT),
        "quadros": len(quadros),
        "duracao": round(len(quadros) / float(fps or 30), 2),
        "tamanho": os.path.getsize(destino),
    }


def limpar_temporarios(idade_horas=6):
    """Varre restos de exportacao interrompida (fechou a aba no meio)."""
    if not os.path.isdir(TEMP):
        return 0
    limite = time.time() - idade_horas * 3600
    n = 0
    for nome in os.listdir(TEMP):
        caminho = os.path.join(TEMP, nome)
        try:
            if os.path.isdir(caminho) and os.path.getmtime(caminho) < limite:
                shutil.rmtree(caminho, ignore_errors=True)
                n += 1
        except Exception:
            pass
    return n
