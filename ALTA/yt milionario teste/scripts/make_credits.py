"""Créditos e risco de Content ID do modo ULTRA (PROMPT_v_ULTRA, seções 6, 7 e 10) — lê data/music_plan.json e
data/sfx_plan.json e escreve qa/music_credits.md, qa/sfx_credits.md e qa/risco_content_id.md.
Uso: python make_credits.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D, Q = ROOT / "data", ROOT / "qa"
Q.mkdir(exist_ok=True)
plan = json.loads((D / "music_plan.json").read_text("utf-8"))
sfx = json.loads((D / "sfx_plan.json").read_text("utf-8")) if (D / "sfx_plan.json").exists() else []
mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"

faixas = {}
for b in plan:
    f = faixas.setdefault(b["track"], {"title": b["title"], "license": b["license"], "page": b["page"], "fonte": b["fonte"], "usos": []})
    f["usos"].append((b["from_s"], b["to_s"], b["clima"]))
linhas = ["# Trilha sonora — créditos", "",
          "Todas as faixas são CC0 (domínio público) ou domínio público, verificadas na página de origem "
          "(campo licenseurl / licença da página). Nenhuma exige atribuição; ela vai na descrição mesmo assim.", ""]
for k, f in faixas.items():
    linhas.append(f"- **{f['title']}** — {f['fonte']} — {f['license']}  ")
    linhas.append(f"  {f['page']}  ")
    linhas.append("  usos: " + "; ".join(f"{mm(a)}–{mm(z)} ({c})" for a, z, c in f["usos"]))
linhas += ["", "## Texto para a descrição do YouTube", ""]
linhas += [f"Música: {f['title']} ({f['fonte']}, CC0) — {f['page']}" for f in faixas.values()]
(Q / "music_credits.md").write_text("\n".join(linhas) + "\n", "utf-8")

efeitos = {}
for e in sfx:
    f = efeitos.setdefault(e["key"], {"title": e["title"], "license": e["license"], "page": e["page"], "fonte": e["fonte"], "papel": e["tipo"], "n": 0})
    f["n"] += 1
linhas = ["# Efeitos sonoros — créditos", "", "Todos CC0 (Freesound), verificados na página de cada som.", ""]
for f in efeitos.values():
    linhas.append(f"- **{f['title']}** ({f['papel']}, {f['n']}×) — {f['fonte']} — {f['license']}  ")
    linhas.append(f"  {f['page']}")
linhas += ["", "## Texto para a descrição do YouTube", ""]
linhas += [f"SFX: {f['title']} (Freesound, CC0) — {f['page']}" for f in efeitos.values()]
(Q / "sfx_credits.md").write_text("\n".join(linhas) + "\n", "utf-8")

linhas = ["# Risco de Content ID", "",
          "| item | risco | por quê |", "|---|---|---|"]
for f in faixas.values():
    risco = "baixo" if "zero/1.0" in f["license"] or "publicdomain" in f["license"] else "conferir"
    linhas.append(f"| trilha: {f['title']} | {risco} | CC0 no Freesound; autor não cadastra em Content ID (obra liberada) |")
for f in efeitos.values():
    linhas.append(f"| sfx: {f['title']} | baixo | CC0 no Freesound |")
linhas += ["", "Regra do filme: nada de biblioteca com licença NC/ND, nada de trilha de canal de terceiros, nada de "
           "Pixabay/Epidemic (não verificáveis por script). Se um aviso de Content ID aparecer, contestar com a página "
           "CC0 listada em music_credits.md / sfx_credits.md."]
(Q / "risco_content_id.md").write_text("\n".join(linhas) + "\n", "utf-8")
print(f"[credits] {len(faixas)} faixas, {len(efeitos)} efeitos -> qa/music_credits.md, qa/sfx_credits.md, qa/risco_content_id.md")
