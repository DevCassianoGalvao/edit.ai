"""Monta a pasta de entrega (mesma estrutura do filme da solda): entregas/<slug>-<data>/
  <nome>.mp4 | LEIA-ME.md (escrito à mão antes) | miniaturas/ (+ _teste_210px.jpg + creditos_fotos.json) | relatorios/
Uso: python deliver.py <slug> <nome-do-mp4-sem-extensao> [--mp4 out/final.mp4] [--thumbs PREFIXO] [--thumb-mod make_thumb_x]
"""
import re, json
import shutil
import sys
from datetime import date
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
D, Q = ROOT / "data", ROOT / "qa"


def main():
    slug, nome = sys.argv[1], sys.argv[2]
    mp4 = ROOT / (sys.argv[sys.argv.index("--mp4") + 1] if "--mp4" in sys.argv else "out/final.mp4")
    principal = ROOT.parent.parent / "EditAI" if ROOT.parent.name == "baias" else ROOT   # 28/09: baias entregam na b1
    hoje = date.today().isoformat()
    dest = principal / "entregas" / (slug if slug.endswith(hoje) else f"{slug}-{hoje}")   # slug já com data: não repete
    (dest / "miniaturas").mkdir(parents=True, exist_ok=True)
    (dest / "relatorios").mkdir(parents=True, exist_ok=True)
    arq = re.sub(r'\s*[<>:"/\\|?*]+\s*', ' - ', nome).strip(' .-')   # 30/09: ':' no titulo virava fluxo NTFS oculto (video de 0 bytes)
    alvo = dest / f"{arq}.mp4"   # 14/10/2026: disco cheio -> hard link (mesmo disco, 0 byte a mais); cópia se não der
    if alvo.exists():
        alvo.unlink()
    try:
        import os
        os.link(mp4, alvo)
    except OSError:
        shutil.copy2(mp4, alvo)
    # miniaturas + teste de 210 px + créditos das fotos usadas nelas
    pref = sys.argv[sys.argv.index("--thumbs") + 1] if "--thumbs" in sys.argv else "abismo_"
    thumbs = sorted((ROOT / "out" / "thumbnails").glob(pref + "*.jpg"))
    pool = json.loads((D / "photo_pool.json").read_text("utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib
    # 08/10/2026: o módulo de miniaturas é importado com argv LIMPO — make_thumb_bomba lia sys.argv[1] (o slug) como
    # JSON de escolhas e a entrega quebrava depois de um render inteiro pronto
    _mod = sys.argv[sys.argv.index("--thumb-mod") + 1] if "--thumb-mod" in sys.argv else "make_thumb_abismo"
    _argv, sys.argv = sys.argv, [_mod]
    try:
        SPECS = importlib.import_module(_mod).SPECS
    finally:
        sys.argv = _argv
    pronto = D / "thumb_credits_final.json"  # créditos escritos à mão para este filme têm prioridade
    cred = {}
    for s in SPECS:
        src = Path(s["src"]).name
        e = next((v for v in pool.values() if v.get("file") and Path(v["file"]).name == src), None)
        cred[f"{s['name']}.jpg"] = {"arquivo": src, "titulo": e["title"] if e else None, "licenca": e["license"] if e else None,
                                    "autor": e.get("artist") if e else None, "pagina": e.get("descurl") if e else None}
    if pronto.exists():
        cred = json.loads(pronto.read_text("utf-8"))
    (dest / "miniaturas" / "creditos_fotos.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1), "utf-8")
    folha = Image.new("RGB", (640 + 24 + 210, len(thumbs) * 372), (16, 18, 22))
    for i, t in enumerate(thumbs):
        shutil.copy2(t, dest / "miniaturas" / t.name)
        im = Image.open(t).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(dest / "miniaturas" / "_teste_210px.jpg", quality=90)
    # relatórios
    rel = [D / "alignment_report.md", D / "attribution.md", D / "build_plan_report.md", D / "visual_plan.md", D / "qa_report.md", D / "audio_qa.json",
           D / "music_plan.json", D / "sfx_plan.json", D / "tema_config.json",
           Q / "decisions_log.md", Q / "chapters.md", Q / "music_credits.md", Q / "sfx_credits.md", Q / "risco_content_id.md",
           Q / "grade_sheet.jpg", Q / "final_mp4.jpg", Q / "anim_context.jpg", Q / "review_rounds.md"]
    for p in rel:
        if p.exists():
            shutil.copy2(p, dest / "relatorios" / p.name)
    leia = ROOT / "qa" / "LEIA-ME.md"
    if leia.exists() and leia.stat().st_mtime > mp4.stat().st_mtime - 6 * 3600:   # 30/09: não copiar LEIA-ME de filme antigo
        shutil.copy2(leia, dest / "LEIA-ME.md")
    # 28/09/2026 (painel): legenda do YouTube, Shorts 9:16 e pacote de publicação vão junto sozinhos
    if (ROOT / "out" / "legendas.srt").exists():
        shutil.copy2(ROOT / "out" / "legendas.srt", dest / "legendas-youtube.srt")
    if (ROOT / "out" / "publicacao.md").exists():
        shutil.copy2(ROOT / "out" / "publicacao.md", dest / "publicacao.md")
    shorts = sorted((ROOT / "out" / "shorts").glob("short_*.mp4"))
    if shorts:
        (dest / "shorts").mkdir(exist_ok=True)
        for f in shorts + [ROOT / "out" / "shorts" / "shorts.md"]:
            if f.exists():
                shutil.copy2(f, dest / "shorts" / f.name)
    print(f"[deliver] {dest}  ({(dest / (arq + '.mp4')).stat().st_size / 1e9:.2f} GB, {len(thumbs)} miniaturas, "
          f"{sum(1 for p in rel if p.exists())} relatórios)")


if __name__ == "__main__":
    main()
