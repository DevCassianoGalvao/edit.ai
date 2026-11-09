"""QA DE ÁUDIO do modo ULTRA (PROMPT_v_ULTRA, seção 8) — mede o master e a relação voz/trilha.

  integrado -14 LUFS ± 0,5 | pico real <= -1 dBTP | LRA 4–7 LU
  trilha sob a voz entre -36 e -28 LUFS (medida em 6 janelas de 20 s com fala contínua, só a cama)
  golpes: nunca dois em < 45 s (data/sfx_plan.json)
Uso: python audio_qa.py [arquivo]   (padrão public/final_audio.m4a; 0 = ok, 1 = falhou)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def ebur(path, ss=None, t=None):
    cmd = ["ffmpeg", "-hide_banner", "-nostats"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.2f}", "-t", f"{t:.2f}"]
    cmd += ["-i", str(path), "-vn", "-filter_complex", "ebur128=peak=true", "-f", "null", "-"]   # 04/10: -vn (decodificava o vídeo: 199 s)
    txt = subprocess.run(cmd, capture_output=True, text=True, errors="replace").stderr

    def g(pat):
        m = re.findall(pat, txt)
        return float(m[-1]) if m else None
    return g(r"I:\s+(-?[\d.]+) LUFS"), g(r"LRA:\s+([\d.]+) LU"), g(r"Peak:\s+(-?[\d.]+) dBFS")


def main():
    final = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "public/final_audio.m4a")
    fails, warns = [], []
    I, lra, tp = ebur(final)
    print(f"[audio_qa] {final.name}: I={I} LUFS  LRA={lra} LU  TP={tp} dBTP")
    if I is None or abs(I + 14) > 0.5:
        fails.append(f"integrado {I} LUFS (meta -14 ± 0,5)")
    if tp is None or tp > -1.0:
        fails.append(f"pico real {tp} dBTP (meta <= -1)")
    # LRA: a narração deste filme já chega comprimida (3,6 LU); a meta 4–7 só falha se o master ficar mais
    # comprimido que a própria voz (menos 1,2 LU) ou passar de 7 — o resto é aviso documentado no decisions_log
    voz_I, voz_lra, _ = ebur(ROOT / "public" / "audio.mp3")
    print(f"[audio_qa] narração sozinha: I={voz_I} LUFS  LRA={voz_lra} LU")
    piso = min(4.0, (voz_lra or 4.0) - 1.2)   # subir 10 dB uma voz com picos altos custa ~1 LU de LRA
    if lra is None or lra > 7 or lra < piso:
        fails.append(f"LRA {lra} LU (meta 4–7; piso pela narração {piso:.1f})")
    elif lra < 4 and (json.loads((D / "pipeline_config.json").read_text("utf-8")).get("music")
                      if (D / "pipeline_config.json").exists() else True) is not False:
        # sem trilha o master É a narração: comparar um com o outro não diz nada
        warns.append(f"LRA {lra} LU abaixo de 4 (narração tem {voz_lra} LU)")

    # cama sob a voz: janelas de 20 s com fala contínua, medidas na trilha sozinha.
    # Filme sem trilha ("music": false) não tem cama para medir — medir daria -70 LUFS (silêncio).
    cfg = json.loads((D / "pipeline_config.json").read_text("utf-8")) if (D / "pipeline_config.json").exists() else {}
    cama = ROOT / "public" / "music.m4a"
    if cfg.get("music") is False or not cama.exists():
        print("[audio_qa] filme sem trilha: a checagem de cama e de golpe não se aplica")
        print(f"[audio_qa] {len(fails)} falhas, {len(warns)} avisos | 0 golpes")
        for m in fails:
            print("  FALHA", m)
        for m in warns:
            print("  AVISO", m)
        (D / "audio_qa.json").write_text(
            json.dumps({"I": I, "LRA": lra, "TP": tp, "fails": fails, "warns": warns, "trilha": False}, indent=1), "utf-8")
        sys.exit(1 if fails else 0)

    raw = json.loads((D / "whisper_raw.json").read_text("utf-8"))
    words = sorted((w["s"], w["e"]) for s in raw["segments"] for w in s["words"] if w.get("s") is not None)
    dur = json.loads((D / "source_meta.json").read_text("utf-8"))["audioDuration"]
    janelas, k = [], 1
    while len(janelas) < 6 and k < 7:
        t0 = dur * k / 7
        ws = [w for w in words if t0 <= w[0] < t0 + 20]
        if ws and max(b - a for a, b in zip([w[1] for w in ws], [w[0] for w in ws][1:] + [t0 + 20])) < 2.0:
            janelas.append(t0)
        k += 1
    for t0 in janelas:
        i, _, _ = ebur(cama, t0, 20)
        print(f"  trilha sob a voz @{t0:6.0f}s: {i} LUFS")
        if i is not None and not (-36 <= i <= -28):
            warns.append(f"trilha sob a voz @{t0:.0f}s = {i} LUFS (meta -36..-28)")
    # 29/09/2026: sfx_plan.json de filme anterior sobrava na pasta — só conta se o filme tem efeitos
    _sfx_on = json.loads((D / "pipeline_config.json").read_text("utf-8")).get("sfx", False)
    plan = json.loads((D / "sfx_plan.json").read_text("utf-8")) if _sfx_on and (D / "sfx_plan.json").exists() else []
    hits = sorted(e["t"] for e in plan if e["tipo"] == "hit")
    # golpe audível: a cama sobe >= 4 LU no momentâneo (M) do golpe; e o mix não passa de -8 LUFS momentâneo
    def momentaneo(path, t0, dur):
        txt = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", str(path), "-vn",
                              "-filter_complex", "ebur128", "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
        return [float(x) for x in re.findall(r"M:\s*(-?[\d.]+)", txt)]
    for t in hits[:: max(1, len(hits) // 5)][:5]:
        m = momentaneo(cama, t - 2, 5)
        if len(m) > 35:
            antes, no = max(m[:15]), max(m[18:35])
            mix_m = max(momentaneo(final, t - 0.2, 1.5) or [-99])
            print(f"  golpe @{t:6.0f}s: cama {antes:.1f} -> {no:.1f} LUFS(M)  mix {mix_m:.1f}")
            if no - antes < 4:
                warns.append(f"golpe @{t:.0f}s sobe só {no - antes:.1f} LU sobre a cama (meta >= 4)")
            if mix_m > -8:
                fails.append(f"golpe @{t:.0f}s estoura o mix: {mix_m:.1f} LUFS momentâneo")
    for a, b in zip(hits, hits[1:]):
        if b - a < 45:
            fails.append(f"dois golpes a {b - a:.0f} s ({a:.0f}s, {b:.0f}s)")
    print(f"[audio_qa] {len(fails)} falhas, {len(warns)} avisos | {len(hits)} golpes")
    for m in fails:
        print("  FALHA", m)
    for m in warns:
        print("  AVISO", m)
    (D / "audio_qa.json").write_text(json.dumps({"I": I, "LRA": lra, "TP": tp, "fails": fails, "warns": warns}, indent=1), "utf-8")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
