"""FECHA o filme em 3 comandos — encadeia o que eu rodava à mão, um passo por vez, esperando cada um.

  python fechar.py preparar
      beats -> build_plan -> cue_debug -> build_overlays -> qa -> folha densa dos cortes de vídeo -> folha corte a corte
      ANTES do render (qa/pre_render). PARA se: ERROS no plano, cue não encontrado, QA com falha ou aviso.
      Depois disso: julgar qa/dense_*.jpg e qa/pre_render/*.jpg; foto/clipe ruim -> data/window_rejects.json e
      rodar preparar de novo.

  python fechar.py render
      re-render INCREMENTAL (só os segmentos que cruzam o que mudou desde o último render — compara com
      data/timeline_renderizado.json) -> bundle NOVO (o Remotion lê o timeline gravado nele) -> render_hybrid
      --workers 2 -> normaliza_audio (filme sem trilha) -> audio_qa -> folha corte a corte do MP4 final
      (qa/final_cortes) + final_mp4_sheet.

  python fechar.py entregar SLUG "nome do mp4" --thumbs PREFIXO --thumb-mod make_thumb_x [--banco tag1,tag2]
      atribuição -> deliver.py -> banco guardar (se --banco) -> material pesado para APAGAR_<SLUG>.

Log completo em data/fechar.log.
"""
import json, os, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
LOG = D / "fechar.log"
PY = sys.executable
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run(*cmd, pega=False):
    t0 = time.time()
    print(f"\n$ {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n$ {' '.join(cmd)}\n{saida}")
    linhas = [l for l in saida.splitlines() if l.strip()]
    for l in linhas[-6:]:
        print("   " + l, flush=True)
    print(f"   ({time.time() - t0:.0f} s)", flush=True)
    if r.returncode:
        sys.exit(f"[fechar] PAROU: {' '.join(cmd)} saiu com {r.returncode} (ver data/fechar.log)")
    return saida if pega else None


def preparar():
    from trava import media   # 07/10/2026: render exclusivo — o preparar não roda junto com o render de outra baia
    with media("preparar"):
        _preparar()


def _preparar():
    # 02/10/2026: beats.json é regerado SEMPRE — mudar _T no beats.py sem rodá-lo custou 3 preparar inúteis
    run(PY, "scripts/beats.py")
    s = run(PY, "scripts/build_plan.py", pega=True)
    m = re.search(r"ERROS (\d+)", s)
    if m and int(m.group(1)):
        sys.exit("[fechar] PAROU: build_plan com erros")
    if (D / "ia_cenas_plano.json").exists():   # 02/11/2026: canais com imagens de IA (seu canal, seu canal)
        run(PY, "scripts/ia_cenas.py", "aplicar")
        run(PY, "scripts/ia_cenas.py", "verificar")
    s = run(PY, "scripts/cue_debug.py", pega=True)
    faltam = [l.strip() for l in s.splitlines() if "NÃO ENCONTRADO" in l]
    if faltam:
        sys.exit("[fechar] PAROU: cue não encontrado na narração:\n  " + "\n  ".join(faltam))
    run(PY, "scripts/build_overlays.py")
    s = run(PY, "scripts/qa.py", pega=True)
    if "0 falhas, 0 avisos" not in s:
        sys.exit("[fechar] PAROU: QA com falha ou aviso")
    tl = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    if any(i.get("kind") == "video" for i in tl):
        run(PY, "scripts/dense_cuts.py", "qa/dense.jpg", "--all")
        run(PY, "scripts/video_suspeitos.py")   # 04/10/2026: apresentador/texto nos clipes ANTES do render -> qa/suspeitos.jpg
    run(PY, "scripts/timeline_sheet.py", "qa/pre_render")
    checagem()
    # 10/10/2026 (meta de 2 h, "fazer uma vez só"): foto de cada cartão/mapa/animação do Remotion ANTES do render —
    # a revisora confere animacoes_*.jpg junto com cortes_*.jpg e o filme renderiza uma vez só
    if "--sem-stills" not in sys.argv:
        r = subprocess.run([PY, "scripts/stills_animacoes.py"], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print((r.stdout or "").strip().splitlines()[-1] if r.stdout.strip() else "[stills] sem saída",
              "" if r.returncode == 0 else f"(AVISO: fotos das animações falharam: {(r.stderr or '')[-300:]})")
    print("\n[fechar] PRONTO PARA JULGAR: qa/dense_*.jpg (vídeo), qa/pre_render/cortes_*.jpg (todos os cortes) e "
          "qa/pre_render/animacoes_*.jpg (cartões e animações)")


def checagem():
    """05/10/2026 — PORTEIRO: clipe corrompido, marca d'água/legenda (OCR do Windows), apresentador e foto de outro
    país BLOQUEIAM o filme. Alarme falso: data/checagem_aceitos.json {id: motivo} depois de olhar qa/checagem.jpg."""
    r = subprocess.run([PY, "scripts/checagem.py"], cwd=ROOT, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("\n".join(l for l in r.stdout.splitlines() if "HF Hub" not in l), flush=True)
    if r.returncode:
        sys.exit("[fechar] PAROU na checagem: veja qa/checagem.jpg — defeito: rejeite (window_rejects / photo_side) e rode "
                 "preparar de novo; alarme falso: ponha o id em data/checagem_aceitos.json")


def checagem_em_dia():
    """O render só sai com a checagem aprovada PARA ESTA timeline (hash); senão roda de novo."""
    import hashlib
    c = json.loads((D / "checagem.json").read_text("utf-8")) if (D / "checagem.json").exists() else {}
    atual = hashlib.md5((D / "timeline.json").read_bytes()).hexdigest()
    if c.get("ok") and c.get("timeline") == atual:
        print("[fechar] checagem em dia (timeline aprovada)", flush=True)
        return
    checagem()


def incremental():
    """Apaga só os segmentos do render anterior que cruzam itens que mudaram."""
    plano, velho = ROOT / "out/hybrid/plan.json", D / "timeline_renderizado.json"
    if not (plano.exists() and velho.exists()):
        return
    a = json.loads(velho.read_text("utf-8"))["items"]
    b = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    chave = lambda it: (it["from"], it["dur"], it.get("clip"), it.get("scene"), json.dumps(it.get("ov"), sort_keys=True))
    A = {chave(x) for x in a}
    mud = [(x["from"], x["from"] + x["dur"]) for x in b if chave(x) not in A]
    p = json.loads(plano.read_text("utf-8"))
    segs = p["segments"] if isinstance(p, dict) else p
    apagados = 0
    for s in segs:
        if any(s["start"] < e and a0 < s["end"] for a0, e in mud):
            for ext in (".mp4", ".filter.txt"):
                f = ROOT / "out/hybrid" / (s["name"] + ext)
                if f.exists():
                    f.unlink()
                    apagados += ext == ".mp4"
    print(f"[fechar] incremental: {len(mud)} itens mudaram -> {apagados} segmentos refeitos", flush=True)


def render():
    from trava import pesado   # 28/09: baias — um render por vez no PC inteiro
    with pesado("render"):
        _render()


def _render():
    checagem_em_dia()
    incremental()
    shutil.rmtree(ROOT / "out/bundle", ignore_errors=True)
    run("node", "scripts/bundle.mjs")
    # 04/10/2026: a narração normaliza JUNTO com o render (só áudio, leve); no fim sobra o remux
    import subprocess as _sp
    narr = _sp.Popen([PY, "scripts/normaliza_audio.py", "--so-audio"], cwd=ROOT,
                     env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    run(PY, "scripts/render_hybrid.py", "--workers", "2")
    narr.wait()
    shutil.copy2(D / "timeline.json", D / "timeline_renderizado.json")
    run(PY, "scripts/acabamento.py")   # 26/09/2026: grão + vinheta + tom de época no filme inteiro (regra do usuário)
    run(PY, "scripts/normaliza_audio.py")
    s = run(PY, "scripts/audio_qa.py", "out/final.mp4", pega=True)
    # 04/10/2026: aviso de LRA ACIMA do piso da narração (voz que já chega comprimida) não para o filme — fica no
    # LEIA-ME; qualquer FALHA ou outro aviso continua parando.
    _avisos = [l for l in s.splitlines() if l.strip().startswith("AVISO")]
    if "0 falhas" not in s or any("LRA" not in l for l in _avisos):
        sys.exit("[fechar] PAROU: audio_qa com falha ou aviso")
    if _avisos:
        print("[fechar] aviso aceito (LRA acima do piso da narração):", "; ".join(a.strip() for a in _avisos))
    _ent = (json.loads((ROOT / "data" / "pipeline_config.json").read_text("utf-8")).get("entrega") or {})
    if _ent.get("short_inteiro"):   # 06/11/2026 formato "short": o filme inteiro em 9:16 (out/shorts/short_1.mp4)
        run(PY, "scripts/shorts.py", "1", "--inteiro")
    folha = _sp.Popen([PY, "scripts/final_mp4_sheet.py"], cwd=ROOT, env={**os.environ, "PYTHONIOENCODING": "utf-8"})   # 04/10: as 2 folhas juntas
    run(PY, "scripts/timeline_sheet.py", "qa/final_cortes", "--mp4", "out/final.mp4")
    if folha.wait():
        sys.exit("[fechar] PAROU: final_mp4_sheet.py falhou")
    print("\n[fechar] RENDER PRONTO: julgar qa/final_cortes/cortes_*.jpg; defeito -> window_rejects, preparar, render")


def entregar():
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    ops = {sys.argv[i]: sys.argv[i + 1] for i in range(2, len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    if len(args) < 2 or "--thumbs" not in ops or "--thumb-mod" not in ops:
        sys.exit(__doc__)
    slug, nome = args[0], args[1]
    run(PY, "scripts/make_attribution.py")
    run(PY, "scripts/deliver.py", slug, nome, "--thumbs", ops["--thumbs"], "--thumb-mod", ops["--thumb-mod"])
    if "--banco" in ops:
        run(PY, "scripts/banco.py", "guardar", slug, *ops["--banco"].split(","))
    principal = ROOT.parent.parent / "EditAI" if ROOT.parent.name == "baias" else ROOT   # 28/09: baias
    hoje = time.strftime("%Y-%m-%d")
    dest = principal / "entregas" / (slug if slug.endswith(hoje) else f"{slug}-{hoje}")   # mesma regra do deliver.py
    if dest.exists():   # 04/10/2026: LEIA-ME gerado dos dados (notas de julgamento em data/notas_entrega.md)
        run(PY, "scripts/leiame.py", str(dest), nome)
    lixo = principal / f"APAGAR_{slug}"
    for s in ["out/final.mp4", "out/final_prenorm.mp4", "out/final_base.mp4", "out/shorts", "out/rascunho", "out/rascunho.mp4",
              "out/publicacao.md", "out/legendas.srt", "out/hybrid", "out/bundle", "assets/photos", "assets/thumbs",
              "public/stock", "input/youtube/slices", "qa/photos", "qa/probe1", "qa/pre_render", "qa/final_cortes"]:
        p = ROOT / s
        if p.exists():
            (lixo / s).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), lixo / s)
    tam = sum(f.stat().st_size for f in lixo.rglob("*") if f.is_file()) / 1e9 if lixo.exists() else 0
    print(f"\n[fechar] ENTREGUE. Material pesado ({tam:.1f} GB) em {lixo.name}/ para esvaziar.")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    {"preparar": preparar, "render": render, "entregar": entregar}.get(modo, lambda: sys.exit(__doc__))()
