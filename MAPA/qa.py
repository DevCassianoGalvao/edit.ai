# -*- coding: utf-8 -*-
"""
qa.py - portoes de qualidade sobre o VIDEO PRONTO.

A 3.0 ja media a soma da duracao dos clipes contra o audio (verificar_clipes).
Isto e o passo que faltava: olhar o arquivo que saiu. Cinco perguntas, todas
sobre o video final:

  1. a duracao bate com o audio? (deriva de sincronia)
  2. tem trecho preto longo? (buraco no acervo, fade que ficou)
  3. tem trecho congelado longo? (imagem parada segurada demais)
  4. o loudness esta no padrao da plataforma (-14 LUFS)?
  5. tira 12 fotos ao longo do video para conferencia rapida

Uso:
    py qa.py video.mp4 narracao.mp3
    (ou automatico no fim de:  py sincronizar.py --montar)

Nao instala nada - so ffmpeg/ffprobe no PATH.
"""

import json
import os
import re
import subprocess
import sys

MAX_PRETO_S = 0.4
# O limiar padrao do blackdetect (0.10) acusa cena escura de proposito. 0.03
# nao da falso positivo e continua pegando preto de verdade.
PRETO_PIX_TH = 0.03
MAX_CONGELADO_S = 3.0
ALVO_LUFS = -14.0
TOLERANCIA_LUFS = 1.5
QTD_FOTOS = 12


def _ffprobe(caminho):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,nb_frames,r_frame_rate:format=duration",
         "-of", "json", caminho],
        capture_output=True, text=True, timeout=60,
    )
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    fmt = d.get("format") or {}
    fr = st.get("r_frame_rate") or "30/1"
    try:
        num, den = fr.split("/")
        fps = float(num) / float(den or 1)
    except Exception:
        fps = 30.0
    return {
        "width": int(st.get("width") or 0),
        "height": int(st.get("height") or 0),
        "fps": round(fps, 3),
        "duration": float(fmt.get("duration") or 0.0),
    }


def _detectar(video, filtro, padrao):
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", video,
         "-vf", filtro, "-an", "-f", "null", "-"],
        capture_output=True, text=True, timeout=3600,
    )
    return [(float(a), float(b)) for a, b in re.findall(padrao, r.stderr or "", re.S)]


def _loudness(video):
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", video,
         "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
        capture_output=True, text=True, timeout=3600,
    )
    m = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", r.stderr or "")
    return float(m[-1]) if m else None


def rodar(video, audio="", silencioso=False):
    """Roda os portoes. Devolve (ok, problemas:list[str])."""
    def p(msg):
        if not silencioso:
            print(msg)

    if not os.path.isfile(video):
        return False, ["o arquivo de video nao existe: %s" % video]
    import shutil
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        return True, []  # sem ffmpeg nao da pra conferir - nao reprova

    info = _ffprobe(video)
    problemas = []

    p(" Conferindo o video pronto (preto / congelado / loudness)...")
    pretos = _detectar(
        video, "blackdetect=d=%g:pic_th=0.98:pix_th=%g" % (MAX_PRETO_S, PRETO_PIX_TH),
        r"black_start:(\d+\.?\d*) black_end:(\d+\.?\d*)")
    congelados = _detectar(
        video, "freezedetect=n=-60dB:d=%g" % MAX_CONGELADO_S,
        r"freeze_start: (\d+\.?\d*).*?freeze_end: (\d+\.?\d*)")
    lufs = _loudness(video)

    dur_audio = None
    if audio and os.path.isfile(audio):
        try:
            ra = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", audio],
                capture_output=True, text=True, timeout=30)
            dur_audio = float((ra.stdout or "").strip())
        except Exception:
            dur_audio = None

    # --- fotos de conferencia ---
    pasta_fotos = os.path.join(os.path.dirname(os.path.abspath(video)) or ".", "qa_fotos")
    os.makedirs(pasta_fotos, exist_ok=True)
    for antigo in os.listdir(pasta_fotos):
        if antigo.endswith(".jpg"):
            try:
                os.remove(os.path.join(pasta_fotos, antigo))
            except OSError:
                pass
    base_dur = info["duration"] or (dur_audio or 0)
    for i in range(QTD_FOTOS):
        em = base_dur * (i + 0.5) / QTD_FOTOS
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-ss", "%.2f" % em, "-i", video, "-frames:v", "1",
             "-vf", "scale=640:-1", os.path.join(pasta_fotos, "t%05d.jpg" % int(em))],
            capture_output=True, timeout=60)

    # --- veredito ---
    if dur_audio and abs(info["duration"] - dur_audio) > 1.0:
        problemas.append("duracao %.1fs contra %.1fs do audio (deriva de %+.1fs)"
                         % (info["duration"], dur_audio, info["duration"] - dur_audio))
    if info["width"] and (info["width"], info["height"]) != (1920, 1080):
        problemas.append("resolucao %dx%d (esperado 1920x1080)"
                         % (info["width"], info["height"]))
    if lufs is None:
        problemas.append("nao consegui medir o loudness")
    elif abs(lufs - ALVO_LUFS) > TOLERANCIA_LUFS:
        problemas.append("loudness %.1f LUFS (alvo %g +/- %g)"
                         % (lufs, ALVO_LUFS, TOLERANCIA_LUFS))
    for a, b in pretos:
        problemas.append("trecho PRETO de %.1fs em t=%.1fs" % (b - a, a))
    for a, b in congelados:
        problemas.append("trecho CONGELADO de %.1fs em t=%.1fs" % (b - a, a))

    relatorio = {
        "duracao": round(info["duration"], 2),
        "duracao_audio": round(dur_audio, 2) if dur_audio else None,
        "largura": info["width"], "altura": info["height"], "fps": info["fps"],
        "loudness_LUFS": lufs,
        "pretos": [[round(a, 2), round(b, 2)] for a, b in pretos],
        "congelados": [[round(a, 2), round(b, 2)] for a, b in congelados],
        "problemas": problemas,
    }
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(video)) or ".",
                               "qa_relatorio.json"), "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
    except OSError:
        pass

    p("")
    p("=" * 60)
    p(" QA do video pronto")
    p("-" * 60)
    p(" Duracao      : %.1fs%s" % (
        info["duration"],
        ("  (audio %.1fs)" % dur_audio) if dur_audio else ""))
    p(" Resolucao    : %dx%d @ %g fps" % (info["width"], info["height"], info["fps"]))
    p(" Loudness     : %s LUFS" % ("?" if lufs is None else "%.1f" % lufs))
    p(" Pretos       : %d" % len(pretos))
    p(" Congelados   : %d" % len(congelados))
    p(" Fotos        : %d em qa_fotos/" % QTD_FOTOS)
    p("-" * 60)
    if problemas:
        p(" REPROVOU:")
        for x in problemas[:15]:
            p("   - " + x)
    else:
        p(" TUDO OK.")
    p("=" * 60)
    return (not problemas), problemas


def main():
    if len(sys.argv) < 2:
        print("uso: py qa.py video.mp4 [narracao.mp3]")
        sys.exit(2)
    video = sys.argv[1]
    audio = sys.argv[2] if len(sys.argv) > 2 else ""
    ok, _ = rodar(video, audio)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
