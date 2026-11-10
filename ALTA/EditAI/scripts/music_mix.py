"""TRILHA + SOUND DESIGN + MASTER do modo ULTRA (PROMPT_v_ULTRA, seções 6–8)

Tudo é medido na ESCALA FINAL (voz a -14 LUFS):
1) a narração (public/audio.mp3, ≈ -24 LUFS) é levada a -14 LUFS com ganho linear + limitador de pico
   (-2,5 dB, sobra ~1 dB para o AAC) — só a voz passa pelo limitador, a cama nunca é esmagada junto;
2) cama musical por CLIMA do bloco (beats.json: gancho/exposição/clímax/fecho -> tensão/cama/tensão/alívio),
   trocando de faixa a cada capítulo; faixa curta entra em loop com crossfade; XFADE entre faixas.
   Cada faixa é levada a LUFS_FAIXA e depois:
     sob a voz ..... GAIN_VOZ  (≈ -32 LUFS)      respiro (pausa >= RESPIRO s) ..... GAIN_PAUSA (≈ -21 LUFS)
   com ataque rápido (a música desce antes da palavra) e soltura lenta;
3) efeitos de data/sfx_plan.json (sound_design.py) somados por cima, ganho de cada evento relativo à cama;
4) master = voz normalizada + cama + efeitos -> limitador de segurança -> public/final_audio.m4a
   (render_hybrid usa este arquivo no modo ULTRA). Também grava public/music.m4a (cama + efeitos, na escala
   final, para o Remotion Studio e para o audio_qa) e data/music_plan.json (créditos).
Uso: python music_mix.py [--sem-master]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
SR = 44100
ALVO_I, ALVO_TP = -14.0, -1.5
LIMITE = ALVO_TP - 1.0          # o AAC devolve até ~1 dB de pico por cima
LUFS_FAIXA = -23.0
GAIN_VOZ = 10 ** (-7 / 20)      # -23 - 7 = -30 LUFS sob a voz (28/09: com -32 a trilha temática sumia e o usuário só ouvia "vento")
GAIN_PAUSA = 10 ** (+2 / 20)    # -23 + 2 = -21 LUFS no respiro
RESPIRO = 2.5                   # s de silêncio para a música subir
MERGE_GAP = 0.45
PRE_ROLL = 0.25
ATTACK, RELEASE = 0.12, 1.2     # s
XFADE = 4.0
TROCA_MIN = 150.0               # s — não troca de faixa antes disso
CLIMA = {"gancho": "tensao", "exposicao": "cama", "climax": "tensao", "fecho": "alivio"}
RUIM = ("kitten", "interweb", "insects", "hospital")   # títulos que não prometem cama de documentário


def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, **k)


def medir(path):
    """(I LUFS, LRA LU, pico real dBTP) de um arquivo."""
    txt = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    g = lambda pat: float(re.findall(pat, txt)[-1])
    return g(r"I:\s+(-?[\d.]+) LUFS"), g(r"LRA:\s+([\d.]+) LU"), g(r"Peak:\s+(-?[\d.]+) dBFS")


def decode(path, lufs):
    p = sh("ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-")
    a = np.frombuffer(p.stdout, dtype=np.float32).reshape(-1, 2)
    g = 10 ** ((LUFS_FAIXA - (lufs if lufs is not None else -20.0)) / 20)
    a = np.clip(a * g, -0.98, 0.98).astype(np.float32)
    # intro quase muda (fade-in longo de drone): pula o que passar de 0,5 s abaixo de -40 dBFS, senão o bloco
    # começa em silêncio (aconteceu aos 2282 s: -57 LUFS sob a voz)
    alto = np.flatnonzero(np.max(np.abs(a), axis=1) > 0.01)
    if len(alto) and alto[0] > SR // 2:
        a = a[alto[0] - SR // 2:]
    return a


def fade(n, up=True):
    x = np.linspace(0, 1, n, dtype=np.float32)
    x = np.sin(x * np.pi / 2) ** 2
    return x if up else x[::-1]


def looped(track, n):
    xf = int(XFADE * SR)
    if len(track) <= xf * 2:
        track = np.tile(track, int(xf * 3 / max(1, len(track))) + 1)
    out = track.copy()
    while len(out) < n:
        out[-xf:] = out[-xf:] * fade(xf, False)[:, None] + track[:xf] * fade(xf, True)[:, None]
        out = np.concatenate([out, track[xf:]])
    return out[:n]


def speech_gain(total):
    raw = json.loads((D / "whisper_raw.json").read_text("utf-8"))
    words = sorted((w["s"], w["e"]) for s in raw["segments"] for w in s["words"] if w.get("s") is not None)
    spans = []
    for s, e in words:
        s = max(0.0, s - PRE_ROLL)
        if spans and s - spans[-1][1] < MERGE_GAP:
            spans[-1][1] = max(spans[-1][1], e)
        else:
            spans.append([s, e])
    hop = 0.01
    steps = int(total / SR / hop) + 2
    target = np.full(steps, GAIN_VOZ, dtype=np.float32)
    # respiro: só pausas longas sobem para GAIN_PAUSA; pausas curtas ficam no nível da voz
    for (s1, e1), (s2, e2) in zip(spans, spans[1:]):
        if s2 - e1 >= RESPIRO:
            target[int(e1 / hop):int(s2 / hop)] = GAIN_PAUSA
    if spans:
        target[: int(spans[0][0] / hop)] = GAIN_PAUSA
        target[int(spans[-1][1] / hop):] = GAIN_PAUSA
    g = np.empty_like(target)
    cur = GAIN_PAUSA
    a_att, a_rel = 1 - np.exp(-hop / ATTACK), 1 - np.exp(-hop / RELEASE)
    for i, t in enumerate(target):
        cur += (t - cur) * (a_att if t < cur else a_rel)
        g[i] = cur
    return np.interp(np.arange(total) / SR, np.arange(steps) * hop, g).astype(np.float32), spans


def eh_yt_studio(v):
    """faixa da Biblioteca de Áudio do YouTube Studio: marcada no music_pool ("fonte") ou guardada em assets/music/yt_studio."""
    marca = " ".join(str(v.get(c, "")) for c in ("fonte", "license", "title"))
    return any(x in marca.lower() for x in ("youtube audio library", "biblioteca de áudio do youtube", "biblioteca de audio de youtube")) or "/yt_studio/" in str(v.get("file", "")).replace("\\", "/")


def classifica(pool, probe):
    """clima de cada faixa a partir do título e da medição (LRA alto = tensão)."""
    faixas = {}
    for k, v in pool.items():
        # Permite também faixas obtidas pelo coletor com licença livre identificada.
        fonte = str(v.get("fonte", ""))
        licenca = str(v.get("license", "")).lower()
        livre = fonte in ("Internet Archive", "Freesound (CC0)") and any(
            x in licenca for x in ("creativecommons.org/publicdomain/zero/", "creativecommons.org/publicdomain/mark/", "creativecommons.org/licenses/by/", "creativecommons.org/licenses/by-sa/")) and not any(x in licenca for x in ("/by-nc", "/by-nd", "nc-sa", "nc-nd"))
        # Aceita a composição local somente quando está na pasta prevista do projeto.
        try:
            arquivo = (ROOT / str(v.get("file", ""))).resolve()
            gerada = fonte == "Edit.AI local" and arquivo.is_relative_to((ROOT / "assets/music/geradas").resolve()) and arquivo.is_file()
        except (OSError, ValueError):
            gerada = False
        if not eh_yt_studio(v) and not livre and not gerada:
            continue
        pr = probe.get(k)
        if not pr or pr["dur_s"] < 40 or any(r in v["title"].lower() for r in RUIM):
            continue
        t = v["title"].lower()
        if v.get("clima_fixo"):   # 28/09/2026: faixa escolhida por mim para o tema (ex.: trilha egípcia) — clima já decidido
            faixas[k] = {"clima": v["clima_fixo"], "dur": pr["dur_s"], "lufs": pr["lufs"]}
            continue
        if any(x in t for x in ("horror", "nasty", "doomed", "thriller", "monolith", "obsidian", "heavy", "noisy")) or (pr["lra"] or 0) > 9:
            clima = "tensao"
        elif any(x in t for x in ("journey", "world", "underwater", "undersea", "submerged", "lake", "warm")):
            clima = "alivio"
        else:
            clima = "cama"
        faixas[k] = {"clima": clima, "dur": pr["dur_s"], "lufs": pr["lufs"]}
    return faixas


def jload_mb():
    p = D / "music_por_bloco.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def blocos(beats, paras, total):
    """[(t_ini, t_fim, clima)] — junta beats vizinhos do mesmo clima; corta em capítulos para trocar de faixa."""
    out = []
    for b in beats:
        t = paras[b["para"]]["startFrame"] / 30
        clima = CLIMA.get(b.get("modo"), "cama")
        novo = bool(b.get("capitulo"))
        if out and out[-1][2] == clima and not novo:
            continue
        out.append([t, None, clima])
    for i in range(len(out)):
        out[i][1] = out[i + 1][0] if i + 1 < len(out) else total
    # blocos curtos demais grudam no anterior (uma troca de faixa a menos de TROCA_MIN cansa)
    fund = []
    for a, z, c in out:
        if fund and (fund[-1][1] - fund[-1][0]) < TROCA_MIN and fund[-1][2] == c:
            fund[-1][1] = z
        elif fund and z - a < 60:   # bloco de menos de 1 min: fica na faixa anterior (troca curta demais cansa)
            fund[-1][1] = z
        else:
            fund.append([a, z, c])
    return fund


def voz_normalizada(voz, total):
    """narração a ALVO_I LUFS com pico <= LIMITE: ganho linear; limitador só no que sobra. Volta como numpy."""
    I, lra, tp = medir(voz)
    ganho = ALVO_I - I
    tmp = ROOT / "public" / "voice_norm.wav"
    for k in range(3):
        sh("ffmpeg", "-v", "error", "-y", "-i", str(voz), "-af",
           f"volume={ganho:.2f}dB,alimiter=limit={LIMITE:.1f}dB:attack=3:release=60:level=false",
           "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", str(tmp))
        I2, lra2, tp2 = medir(tmp)
        print(f"[voz] {I:.1f} LUFS / {tp:.1f} dBTP / LRA {lra:.1f}  ->  ganho {ganho:+.2f} dB: I={I2} LRA={lra2} TP={tp2}")
        if abs(I2 - ALVO_I) <= 0.2:
            break
        ganho += ALVO_I - I2
    a = np.frombuffer(sh("ffmpeg", "-v", "error", "-i", str(tmp), "-f", "f32le", "-").stdout, dtype=np.float32).reshape(-1, 2)
    out = np.zeros((total, 2), dtype=np.float32)
    n = min(total, len(a))
    out[:n] = a[:n]
    return out


def nivel_da_trilha():
    """04/11/2026 (usuário: "não deixe a trilha muito alta" no estilo Arquivo Colorizado): pipeline_config
    "trilha": {"sob_voz_db": -11, "respiro_db": -4} troca os níveis padrão (-7 / +2 em relação a LUFS_FAIXA)."""
    global GAIN_VOZ, GAIN_PAUSA
    try:
        t = json.loads((D / "pipeline_config.json").read_text("utf-8")).get("trilha") or {}
    except Exception:  # noqa: BLE001
        t = {}
    if "sob_voz_db" in t:
        GAIN_VOZ = 10 ** (float(t["sob_voz_db"]) / 20)
    if "respiro_db" in t:
        GAIN_PAUSA = 10 ** (float(t["respiro_db"]) / 20)
    print(f"[trilha] sob a voz {LUFS_FAIXA + 20 * np.log10(GAIN_VOZ):.0f} LUFS | respiro {LUFS_FAIXA + 20 * np.log10(GAIN_PAUSA):.0f} LUFS")


def main():
    nivel_da_trilha()
    meta = json.loads((D / "source_meta.json").read_text("utf-8"))
    total = int(meta["audioDuration"] * SR)
    paras = json.loads((D / "master_transcript.json").read_text("utf-8"))["paragraphs"]
    beats = json.loads((D / "beats.json").read_text("utf-8"))["beats"]
    pool = json.loads((D / "music_pool.json").read_text("utf-8"))
    probe = json.loads((D / "music_probe.json").read_text("utf-8"))
    faixas = classifica(pool, probe)
    if not faixas:
        sys.exit("[music] nenhuma faixa válida e medida disponível; confira as fontes ou desligue a trilha.")
    print(f"[music] {len(faixas)} faixas úteis: " + ", ".join(f"{c}={sum(1 for f in faixas.values() if f['clima'] == c)}" for c in ("cama", "tensao", "alivio")))
    bl = blocos(beats, paras, meta["audioDuration"])
    # 29/09/2026: capítulos escolhidos por mim em music_por_bloco.json viram os blocos, exatos (faixa pelo que o
    # capítulo FALA); sem o arquivo, segue a curva de clima de sempre
    _mb = sorted((float(t), k) for t, k in jload_mb().items() if k in faixas)
    if _mb:
        bl = [(t, (_mb[i + 1][0] if i + 1 < len(_mb) else meta["audioDuration"]), faixas[k]["clima"])
              for i, (t, k) in enumerate(_mb)]
        if bl[0][0] > 0:
            bl[0] = (0.0, bl[0][1], bl[0][2])
    usos, cache, plan = {}, {}, []
    mix = np.zeros((total, 2), dtype=np.float32)
    xf = int(XFADE * SR)
    ultima = None
    for i, (a_s, z_s, clima) in enumerate(bl):
        cands = [k for k, f in faixas.items() if f["clima"] == clima] or [k for k, f in faixas.items() if f["clima"] == "cama"]
        cands = cands or list(faixas)
        cands = [k for k in cands if k != ultima] or cands
        key = min(cands, key=lambda k: (usos.get(k, 0), -faixas[k]["dur"]))
        # 28/09/2026: data/music_por_bloco.json {"segundo_do_inicio_do_bloco": "chave"} — eu escolho a faixa pelo que o
        # capítulo FALA (luto -> Heartbreaking, museu -> Long Note Four...), em vez do rodízio por clima
        _forca = {int(float(t)): k for t, k in jload_mb().items()}
        if _mb:
            key = _mb[i][1]
        elif int(a_s) in _forca and _forca[int(a_s)] in faixas:
            key = _forca[int(a_s)]
        usos[key] = usos.get(key, 0) + 1
        ultima = key
        a, b = int(a_s * SR), min(total, int(z_s * SR))
        a0, b0 = max(0, a - xf // 2), min(total, b + xf // 2)
        if key not in cache:
            cache[key] = decode(ROOT / pool[key]["file"], faixas[key]["lufs"])
        seg = looped(cache[key], b0 - a0)
        if i > 0:
            seg[:xf] *= fade(xf, True)[:, None]
        if i < len(bl) - 1:
            seg[-xf:] *= fade(xf, False)[:, None]
        mix[a0:b0] += seg
        plan.append({"from_s": round(a_s, 2), "to_s": round(z_s, 2), "clima": clima, "track": key, "title": pool[key]["title"],
                     "license": pool[key]["license"], "page": pool[key]["page"], "fonte": pool[key]["fonte"]})
    mix[: 3 * SR] *= fade(3 * SR, True)[:, None]
    mix[-6 * SR:] *= fade(6 * SR, False)[:, None]
    gain, spans = speech_gain(total)
    mix *= gain[:, None]

    # --- efeitos (sound_design.py): db de cada evento é relativo à cama sob a voz (-32 LUFS)
    _sfx_on = json.loads((D / "pipeline_config.json").read_text("utf-8")).get("sfx", False)
    sfx = json.loads((D / "sfx_plan.json").read_text("utf-8")) if _sfx_on and (D / "sfx_plan.json").exists() else []
    sprobe = json.loads((D / "sfx_probe.json").read_text("utf-8")) if (D / "sfx_probe.json").exists() else {}
    for e in sfx:
        lufs = sprobe.get(e["key"], {}).get("lufs")
        a = decode(ROOT / e["file"], lufs)          # todo efeito referenciado a -23 LUFS
        a = a * (GAIN_VOZ * 10 ** (e["db"] / 20))   # e depois posto em relação à cama sob a voz
        i0 = int(e["t"] * SR)
        if e["tipo"] == "ambiencia":
            n = max(0, min(total, int(e["ate"] * SR)) - i0)
            a = looped(a, n)
            a[: min(n, 2 * SR)] *= fade(min(n, 2 * SR), True)[:, None]
            a[-min(n, 3 * SR):] *= fade(min(n, 3 * SR), False)[:, None]
        n = min(len(a), total - i0)
        if n > 0:
            mix[i0:i0 + n] += a[:n]
    mix = np.clip(mix, -0.98, 0.98)
    (D / "music_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), "utf-8")
    out = ROOT / "public" / "music.m4a"
    sh("ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
       "-c:a", "aac", "-b:a", "256k", str(out), input=mix.tobytes())
    print(f"[music] {len(plan)} blocos, {len(cache)} faixas, {len(sfx)} efeitos, fala {sum(e - s for s, e in spans) / 60:.1f} min -> {out.name}")
    if "--sem-master" in sys.argv:
        return

    # --- master: voz normalizada + cama -> limitador de segurança -> AAC
    voz = voz_normalizada(ROOT / "public" / "audio.mp3", total)
    final = ROOT / "public" / "final_audio.m4a"
    master = voz + mix
    for k in range(2):
        sh("ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af",
           f"alimiter=limit={LIMITE:.1f}dB:attack=3:release=60:level=false", "-ar", "48000",
           "-c:a", "aac", "-b:a", "320k", str(final), input=master.astype(np.float32).tobytes())
        I, lra, tp = medir(final)
        print(f"[master] I={I} LUFS  LRA={lra} LU  TP={tp} dBTP -> {final.name}")
        if abs(I - ALVO_I) <= 0.3 or k == 1:
            break
        master = master * 10 ** ((ALVO_I - I) / 20)   # ajuste fino (a cama muda a soma em décimos de dB)
    # prévias de 30 s: abertura, um reveal, o fecho
    (ROOT / "qa").mkdir(exist_ok=True)
    hits = [e["t"] for e in sfx if e["tipo"] == "hit"]
    for name, t in (("abertura", 5), ("reveal", (hits[len(hits) // 2] - 12) if hits else 600), ("fecho", meta["audioDuration"] - 75)):
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t):.2f}", "-t", "30", "-i", str(final), "-b:a", "192k",
           str(ROOT / "qa" / f"music_preview_{name}.mp3"))


if __name__ == "__main__":
    main()
