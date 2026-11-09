"""SHORTS 9:16 automáticos (28/09/2026, painel: extra "Shorts 9:16 automáticos").

Corta N trechos de ~55 s do filme LIMPO (out/final_base.mp4 — o acabamento guarda antes de pôr barras/legenda quando
pipeline_config "entrega.shorts" > 0) e monta cada um em 1080x1920:
  fundo = o próprio vídeo ampliado, desfocado e escurecido; frente = o vídeo 16:9 inteiro no meio;
  título do capítulo em cima (Anton); legenda de IMPACTO (2-3 palavras, grande) no terço de baixo;
  mesma cor/textura do filme (acabamento.partes base); áudio normalizado a -14 LUFS.
Trechos: o GANCHO (começo do filme) + capítulos espalhados; cada corte termina no fim de uma frase (<= 58 s).
Saída: out/shorts/short_1.mp4 ... (+ out/shorts/shorts.md com os títulos e o tempo de origem).

Uso: python shorts.py [N=3] [--src outro.mp4] [--inteiro]   (--inteiro: o filme todo vira 1 short — formato "short", 06/11/2026)
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "out" / "shorts"
sys.path.insert(0, str(ROOT / "scripts"))
import acabamento  # noqa: E402
from legendas import gera_ass, palavras  # noqa: E402

MAX_S = 58.0


def trechos(n):
    mt = json.loads((D / "master_transcript.json").read_text("utf-8"))
    sents = mt["sentences"]
    bj = json.loads((D / "beats.json").read_text("utf-8"))
    paras = mt["paragraphs"]
    caps = [(paras[b["para"]]["startSec"], b["capitulo"]) for b in bj["beats"] if b.get("capitulo")]
    fim_ok = lambda a: max((s["endSec"] for s in sents if a < s["endSec"] <= a + MAX_S), default=a + 45)
    out = [(0.0, fim_ok(0.0), caps[0][1] if caps else "")]
    resto = [c for c in caps[1:] if c[0] > 60]
    for k in range(1, n):
        if not resto:
            break
        a, nome = resto[min(len(resto) - 1, round(k * len(resto) / n))]
        if all(abs(a - x[0]) > 90 for x in out):
            out.append((a, fim_ok(a), nome))
    return out[:n]


def ass_vertical(a, b, caminho):
    ws = [{"w": w["w"], "s": w["s"] - a, "e": w["e"] - a} for w in palavras() if a <= w["s"] < b]
    txt = gera_ass(ws, "impacto")
    txt = txt.replace("PlayResX: 1920", "PlayResX: 1080").replace("PlayResY: 1080", "PlayResY: 1920")
    txt = re.sub(r"^(Style: L,Anton,)\d+(,.*,)\d+(,\d+)$", r"\g<1>110\g<2>560\g<3>", txt, flags=re.M)   # fonte 110, MarginV 560
    Path(caminho).write_text(txt, "utf-8-sig")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
    src = Path(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else ROOT / "out" / "final_base.mp4"
    if not src.exists():
        sys.exit("[shorts] falta out/final_base.mp4 (ligue 'entrega.shorts' antes do fechar.py render)")
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = acabamento.config()
    base, _ = acabamento.partes({**(cfg.get("acabamento") or {}), "barras": False, "mergulho_capitulo": False})
    linhas = ["# Shorts 9:16", ""]
    lista = trechos(n)
    if "--inteiro" in sys.argv:   # 06/11/2026 formato "short" (1-2 min): o filme INTEIRO vira um short 9:16
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                                   capture_output=True, text=True).stdout.strip() or 0)
        lista = [(0.0, dur, ((cfg.get("entrega") or {}).get("short_titulo") or ""))]
    for i, (a, b, nome) in enumerate(lista, 1):
        ass = OUT / f"_short_{i}.ass"
        ass_vertical(a, b, ass)
        titulo = re.sub(r"[^\w\s\-—?!.,]", "", nome or "").upper()[:34].replace(":", " ").replace("'", "")
        fc = (f"[0:v]{base},split[f][b];"
              "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.18[bg];"
              "[f]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-140,"
              f"drawtext=fontfile=public/fonts/Anton.ttf:text='{titulo}':fontsize=76:fontcolor=white:"
              "x=(w-tw)/2:y=250:borderw=4:bordercolor=black@0.7,"
              f"ass={ass.relative_to(ROOT).as_posix()}:fontsdir=public/fonts,format=yuv420p[v]")
        saida = OUT / f"short_{i}.mp4"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", str(src),
                            "-filter_complex", fc, "-map", "[v]", "-map", "0:a:0", "-af", "loudnorm=I=-14:TP=-1.5",
                            *acabamento.enc("alta"), "-c:a", "aac", "-b:a", "192k", str(saida)],
                           cwd=ROOT, capture_output=True, text=True)
        ass.unlink(missing_ok=True)
        if r.returncode:
            print(f"[shorts] {i} FALHOU: {r.stderr[-300:]}")
            continue
        m, s = divmod(int(a), 60)
        linhas.append(f"- short_{i}.mp4 — {b - a:.0f} s — do filme em {m:02d}:{s:02d} — {nome}")
        print(f"[shorts] {saida.relative_to(ROOT)} ({b - a:.0f} s, {nome})")
    (OUT / "shorts.md").write_text("\n".join(linhas) + "\n", "utf-8")


if __name__ == "__main__":
    main()
