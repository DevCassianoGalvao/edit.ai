"""COMEÇA um filme novo a partir de input/ (script.txt + audio.mp3) — um comando no lugar de 8 passos à mão.

24/09/2026: na troca agro -> motores o public/audio.mp3 e o data/source_meta.json ainda eram do filme anterior
(o QA pegou o áudio; o alinhamento rodou com a duração errada), e as decisões do agro (photo_pool, clips,
window_rejects...) ficaram misturadas em data/ até eu mover à mão. Este script faz, nesta ordem:
  1. guarda as DECISÕES do filme anterior em _decisoes_<anterior>/ (JSON de data/ + cópia dos scripts do tema:
     beats, buscas, tabelas do plano, DOSSIE, cenas) — é o que permite refazer o mesmo tema em outro idioma;
  2. manda o material PESADO que sobrou para APAGAR_<anterior>/ (o usuário esvazia);
  3. copia a narração para public/audio.mp3, grava data/source_meta.json pela duração do ffprobe,
     gera data/audio16k.wav e acerta idioma/proporção no pipeline_config;
  4. transcreve (GPU) e alinha com o roteiro; imprime o GATE 1.

Uso: python novo_filme.py --lang it|pt|en|es|pl|de [--foto 0.8] [--anterior slug] [--simular]
     (--simular: só lista o que seria movido/gravado, sem tocar em nada)
     (--anterior: nome da pasta de decisões; sem ele, usa a entrega mais recente em entregas/)
"""
import json, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
DECISOES = ["beats.json", "clips.json", "photo_pool.json", "photo_prefilter.json", "photo_side.json",
            "photo_approve.json", "timeline.json", "timeline_antes_rej1.json", "timeline_renderizado.json",
            "window_rejects.json", "yt_pool.json", "yt_review.json", "source_side.json", "yt_slices.json",
            "extra_windows.json", "api_review.json", "cm_review.json", "cm_crop.json", "audio_qa.json",
            "mudados.json", "plan_antes.json", "burned_text.json", "commons_files.json", "commons_video_pool.json",
            "stock_api_pool.json", "sheets_map.json", "probe_cm.json", "probe_cm_curada.json", "probe_yt_big.json",
            "master_transcript.json", "whisper_raw.json", "source_meta.json", "photo_dl_limite.json", "fechar.log",
            "segment_rejects.json", "image_locks.json", "yt_crop.json", "ia_cenas_plano.json", "ia_cenas_log.json"]   # 03/10: travas por corte do filme anterior vazavam
SCRIPTS_TEMA = ["scripts/beats.py", "scripts/fetch_images.py", "scripts/fetch_images_cat.py", "scripts/build_plan.py",
                "scripts/build_overlays.py", "src/scenes/index.ts"]
PESADO = ["assets/photos", "assets/thumbs", "assets/banco", "public/stock", "out/hybrid", "out/bundle", "out/final.mp4",
          "out/final_prenorm.mp4", "out/final_v1.mp4", "input/youtube/slices", "qa/photos", "qa/probe1",
          "qa/cortes_final", "qa/final_cortes", "qa/pre_render", "qa/final_mp4", "qa/dense", "painel/_cache"]


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def run(*cmd):
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode:
        sys.exit(f"[novo_filme] falhou: {' '.join(cmd)}")


def main():
    lang = arg("--lang")
    if not lang:
        sys.exit(__doc__)
    for f in ("input/script.txt", "input/audio.mp3"):
        if not (ROOT / f).exists():
            sys.exit(f"[novo_filme] falta {f}")
    ant = arg("--anterior")
    if not ant:
        ents = sorted((ROOT / "entregas").glob("*"), key=lambda p: p.stat().st_mtime)
        ant = ents[-1].name.rsplit("-20", 1)[0] if ents else time.strftime("anterior-%Y%m%d-%H%M")
    fin = ROOT / "out" / "final.mp4"
    ents = sorted((ROOT / "entregas").glob("*"), key=lambda p: p.stat().st_mtime)
    if fin.exists() and (not ents or fin.stat().st_mtime > ents[-1].stat().st_mtime + 60):
        print(f"[novo_filme] AVISO: out/final.mp4 é mais novo que a última entrega — vai para APAGAR_{ant}")

    if "--simular" in sys.argv:
        print(f"[simular] anterior = {ant}")
        print("[simular] decisões ->", f"_decisoes_{ant}/:",
              [n for n in DECISOES + [p.name for p in D.glob("probe_round*.json")] if (D / n).exists()])
        print("[simular] pesado ->", f"APAGAR_{ant}/:",
              [s for s in PESADO if (ROOT / s).exists() and ((ROOT / s).is_file() or any((ROOT / s).iterdir()))])
        return

    # 1. decisões do filme anterior
    dec = ROOT / f"_decisoes_{ant}"
    movidos = 0
    for n in DECISOES + [p.name for p in D.glob("probe_round*.json")]:
        p = D / n
        if p.exists():
            dec.mkdir(exist_ok=True)
            shutil.move(str(p), dec / n)
            movidos += 1
    if (D / "juizes").exists():            # lotes e respostas dos juízes em paralelo (juizes.py)
        dec.mkdir(exist_ok=True)
        shutil.move(str(D / "juizes"), dec / "juizes")
        movidos += 1
    if movidos:
        (dec / "scripts").mkdir(parents=True, exist_ok=True)
        for s in SCRIPTS_TEMA + [str(p.relative_to(ROOT)) for p in (ROOT / "src/scenes").glob("*Scenes.tsx")]:
            if (ROOT / s).exists():
                nome = Path(s).name + (".txt" if Path(s).suffix in (".ts", ".tsx") else "")   # o tsc não compila a cópia
                if not (dec / "scripts" / nome).exists():   # 03/10: baias.py preparar já guardou o tema ANTES do espelho
                    shutil.copy2(ROOT / s, dec / "scripts" / nome)
        print(f"[novo_filme] {movidos} arquivos de decisão + scripts do tema -> {dec.name}/")

    # 2. material pesado que sobrou
    lixo = ROOT / f"APAGAR_{ant}"
    for s in PESADO:
        p = ROOT / s
        if p.exists() and (p.is_file() or any(p.iterdir())):
            (lixo / s).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), lixo / s)
            print(f"[novo_filme] {s} -> {lixo.name}/")

    # 3. narração, duração, configuração
    shutil.copy2(ROOT / "input/audio.mp3", ROOT / "public/audio.mp3")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(ROOT / "input/audio.mp3")], capture_output=True, text=True).stdout)
    meta = {"durationInFrames": round(dur * 30), "durationSec": round(dur, 2), "audioDuration": round(dur, 2), "fps": 30}
    (D / "source_meta.json").write_text(json.dumps(meta, indent=1), "utf-8")
    cfgp = D / "pipeline_config.json"
    cfg = json.loads(cfgp.read_text("utf-8"))
    cfg["screenLanguage"] = lang
    if arg("--foto"):
        cfg["photo_share"] = float(arg("--foto"))
    cfgp.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), "utf-8")
    # 07/10/2026: orçamento do YouTube zera a cada filme (yt_quota.orcamento)
    (D / "yt_orcamento.json").write_text(json.dumps({"inicio": __import__("time").time()}), "utf-8")
    print(f"[novo_filme] narração {dur / 60:.2f} min = {meta['durationInFrames']} quadros | idioma {lang} | "
          f"foto {cfg.get('photo_share')} | música {cfg.get('music')}")
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "input/audio.mp3", "-ac", "1", "-ar", "16000",
        "data/audio16k.wav")

    # 4. transcrição + alinhamento
    # 04/10: trava SÓ da GPU — roda junto com o render de outra baia se houver VRAM (trava.py); sem GPU, espera a vez
    from trava import pesado, gpu
    with gpu("transcrição") as junto:
        env = {**__import__("os").environ, "PYTHONIOENCODING": "utf-8"}
        if junto:
            env["TRANSCRIBE_SEM_CPU"] = "1"
        print("$ python scripts/transcribe.py", lang, "(junto com render)" if junto else "", flush=True)
        rc = subprocess.run([sys.executable, "scripts/transcribe.py", lang], cwd=ROOT, env=env).returncode
    if rc == 3:   # a GPU não deu ao lado do render: espera o render acabar e transcreve do jeito antigo
        print("[novo_filme] GPU ocupada demais — esperando o render para transcrever", flush=True)
        with pesado("transcrição"):
            run(sys.executable, "scripts/transcribe.py", lang)
    elif rc:
        sys.exit("[novo_filme] falhou: scripts/transcribe.py")
    run(sys.executable, "scripts/build_transcript.py")
    rel = (D / "alignment_report.md").read_text("utf-8").splitlines()
    print("\n".join(l for l in rel[:8] if l.startswith("-")))


if __name__ == "__main__":
    main()
