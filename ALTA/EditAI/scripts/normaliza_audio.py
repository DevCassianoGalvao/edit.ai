"""Narração do filme SEM TRILHA a -14 LUFS / pico <= -1 dBTP, sem mexer no vídeo (remux com -c:v copy).

24/09/2026: em todo filme sem música eu acertava o volume à mão, 2-6 tentativas (agro: -24 -> -14 com +11 dB e
limitador; motores: narração a -31 LUFS com pico em -1,8 dBTP — o limitador comum achatava a fala e a LRA caía
abaixo do piso do audio_qa). Aqui:
  1. mede a narração (public/audio.mp3): integrado e pico;
  2. escolhe a cadeia — ganho + limitador suave quando os picos cabem; ganho + limitador RÁPIDO só nos
     transientes (0,1 ms / 2 ms) + limitador suave quando precisa tirar muitos dB de pico (preserva a LRA);
  3. ajusta o ganho em até 4 rodadas (só áudio, ~10 s cada) até -14 +- 0,3 e pico <= -1,1 dBTP no AAC;
  4. remux: out/final.mp4 -> out/final_prenorm.mp4 (guardado) e o novo out/final.mp4.
Filme COM trilha (music != false) não passa por aqui — o music_mix já entrega o master.

Uso: python normaliza_audio.py [out/final.mp4]
     python normaliza_audio.py --so-audio     # 04/10: só prepara data/narracao_norm.m4a (roda junto com o render)
"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
ALVO, TOL, TP_MAX = -14.0, 0.3, -1.1


def mede(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(arq), "-vn", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    resumo = r[r.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, resumo).group(1))
    return g(r"I:\s+(-?[\d.]+) LUFS"), g(r"LRA:\s+([\d.]+) LU"), g(r"Peak:\s+(-?[\d.]+) dBFS")


def cadeia(ganho, rapido, aperto=1.0):
    # 20/10/2026: `aperto` (<1) baixa o teto dos limitadores quando o AAC estoura o pico mesmo com o limitador rápido
    # (voz Alicia, seu canal: pico -0,2/-0,3 dBTP nas 4 rodadas -> render parado 2 filmes seguidos)
    if rapido:
        return (f"volume={ganho:.2f}dB,alimiter=limit={0.7 * aperto:.3f}:attack=0.1:release=2:level=disabled,"
                f"alimiter=limit={0.78 * aperto:.3f}:attack=1:release=50:level=disabled")
    return f"volume={ganho:.2f}dB,alimiter=limit={0.84 * aperto:.3f}:attack=5:release=50:level=disabled"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mp4 = ROOT / (args[0] if args else "out/final.mp4")
    cfg = json.loads((D / "pipeline_config.json").read_text("utf-8"))
    if cfg.get("music") is not False:
        print("[audio] filme com trilha: o master vem do music_mix — nada a fazer")
        return
    meta = json.loads((D / "source_meta.json").read_text("utf-8"))
    dur = meta["durationInFrames"] / meta.get("fps", 30)
    # 04/10/2026: a narração é conhecida desde o começo — o fechar.py roda `--so-audio` JUNTO com o render e grava o
    # AAC pronto em data/narracao_norm.m4a; no fim do render sobra só o remux (segundos, eram 5,5 min).
    cache, cache_j = D / "narracao_norm.m4a", D / "narracao_norm.json"
    narr = ROOT / "public" / "audio.mp3"
    chave = {"mtime": narr.stat().st_mtime, "size": narr.stat().st_size, "dur": round(dur, 3)}
    if "--so-audio" not in sys.argv and cache.exists() and cache_j.exists() and json.loads(cache_j.read_text("utf-8")) == chave:
        print("[audio] narração já normalizada (data/narracao_norm.m4a) — só o remux")
        return remux(mp4, cache, dur, meta)
    I0, lra0, pk0 = mede(narr)
    rapido = pk0 + (ALVO - I0) > -2.0    # o pico passaria do teto: precisa do limitador de transiente
    # o limitador come volume: ~1,1 dB no de transiente, ~0,3 dB no suave (motores: +16,9 dB deram -15,1 LUFS)
    ganho = ALVO - I0 + (1.1 if rapido else 0.3)
    piso_lra = min(4.0, lra0 - 1.2)      # mesmo piso do audio_qa
    print(f"[audio] narração {I0} LUFS, LRA {lra0}, pico {pk0} dBFS -> ganho {ganho:+.1f} dB "
          f"({'limitador de transiente' if rapido else 'limitador suave'})")
    tmp = Path(tempfile.mkdtemp())
    melhor = None                        # (erro, arquivo) da melhor tentativa que passa pico e LRA
    aperto = 1.0
    for rodada in range(7):
        aac = tmp / f"narr{rodada}.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "public" / "audio.mp3"),
                        "-af", cadeia(ganho, rapido, aperto), "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
                        "-t", f"{dur:.3f}", str(aac)], check=True)
        I, lra, pk = mede(aac)
        valido = pk <= TP_MAX and lra >= piso_lra
        print(f"[audio] rodada {rodada + 1}: ganho {ganho:+.2f} dB -> {I} LUFS, LRA {lra}, pico {pk}"
              f"{'' if valido else '  (fora: pico ou LRA)'}")
        if valido and (melhor is None or abs(I - ALVO) < melhor[0]):
            melhor = (abs(I - ALVO), aac)
        if valido and abs(I - ALVO) <= TOL + 1e-6:
            break
        if pk > TP_MAX and not rapido:
            rapido = True
            continue
        if pk > TP_MAX:                  # já no limitador rápido e o pico ainda passa: aperta o teto e compensa o ganho
            corte = TP_MAX - 0.3 - pk    # dB a tirar do pico (negativo)
            aperto *= 10 ** (corte / 20)
            ganho += -corte * 0.5        # o teto mais baixo come volume; recupera metade no ganho
            print(f"[audio] pico acima de {TP_MAX} dBTP: teto do limitador x{aperto:.2f}")
            continue
        ganho += (ALVO - I) if abs(I - ALVO) > TOL else -0.3   # dentro do volume mas pico/LRA fora: recua
    if melhor is None or melhor[0] > 0.5:
        print("[audio] nenhuma tentativa dentro de -14 +- 0,5 com pico e LRA na regra — conferir a narração à mão")
        sys.exit(1)
    aac = melhor[1]
    shutil.copy2(aac, cache)
    cache_j.write_text(json.dumps(chave), "utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    if "--so-audio" in sys.argv:
        print(f"[audio] narração normalizada guardada em {cache.name} (remux no fim do render)")
        return
    remux(mp4, cache, dur, meta)


def remux(mp4, aac, dur, meta):
    prenorm = mp4.with_name("final_prenorm.mp4")
    if not prenorm.exists() or prenorm.stat().st_mtime < mp4.stat().st_mtime:
        shutil.move(str(mp4), prenorm)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(prenorm), "-i", str(aac), "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-t", f"{dur:.3f}", str(mp4)], check=True)
    # 29/09/2026: -count_packets (lê só o contêiner) no lugar de -count_frames, que DECODIFICAVA o filme inteiro (11 min)
    n = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(mp4)],
                       capture_output=True, text=True).stdout.strip().strip(",")
    ok = int(n) == meta["durationInFrames"]
    print(f"[audio] {mp4.name}: {n} quadros ({'confere' if ok else 'DIFERENTE de ' + str(meta['durationInFrames'])})")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
