"""data/attribution.md a partir da timeline final + clips.json.
- YouTube: canal + URL + janela usada (para contestar Content ID)
- Commons: título, página, licença, autor; destaca quais exigem crédito (BY/BY-SA) e quantas estão "unverified"
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
clips = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
used = {}
for it in items:
    if it["type"] == "cut" and it.get("clip"):
        used.setdefault(it["clip"], []).append(it["from"] / 30)

by_src = {}
for cid, times in used.items():
    c = clips[cid]
    by_src.setdefault(c["source"], []).append((c, times))

yt = {k: v for k, v in by_src.items() if k.startswith("yt:")}
api = {k: v for k, v in by_src.items() if k.startswith(("px:", "pb:"))}
cm = {k: v for k, v in by_src.items() if not k.startswith(("yt:", "px:", "pb:"))}


def lic_class(lic):
    l = (lic or "").lower()
    if not l:
        return "unverified"
    if "public domain" in l or l.startswith("pd") or "cc0" in l:
        return "pd"
    if "by" in l:
        return "credit"
    return "unverified"


unver = [k for k, v in cm.items() if lic_class(v[0][0].get("license")) == "unverified"]
credit = [k for k, v in cm.items() if lic_class(v[0][0].get("license")) == "credit"]
mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
L = ["# attribution.md", "",
     f"> **Fontes Commons com licença UNVERIFIED: {len(unver)}**  ",
     f"> **Fontes que EXIGEM crédito (CC BY / BY-SA): {len(credit)}** — texto pronto abaixo.", "",
     f"- Clipes usados: {len(used)} | fontes YouTube: {len(yt)} | fontes Commons: {len(cm)} | fontes Pexels/Pixabay: {len(api)}", "",
     "## Crédito para a descrição do vídeo (obrigatório)", ""]
for k in credit:
    c = cm[k][0][0]
    L.append(f"- \"{c.get('title', '')[5:]}\" — {c.get('artist') or c.get('credit') or 'autor não informado'}, {c.get('license')}, via Wikimedia Commons ({c.get('url')})")
if not credit:
    L.append("- (nenhuma)")
L += ["", "## YouTube — trechos curtos, mudos (canal e URL para contestar reivindicação)", ""]
for k, v in sorted(yt.items()):
    c = v[0][0]
    wins = "; ".join((f"fonte {mm(cc['window'][0])}–{mm(cc['window'][1])}" if cc.get('window') else "quadro parado") + f" → filme {', '.join(mm(t) for t in ts)}" for cc, ts in v)
    L.append(f"- **{c.get('channel')}** — {c.get('title')} — {c.get('url')}  \n  {wins}")
L += ["", "## Wikimedia Commons / DVIDS", ""]
for k, v in sorted(cm.items()):
    c = v[0][0]
    L.append(f"- {c.get('title', '')[5:]} — licença: {c.get('license') or 'UNVERIFIED'} — autor: {c.get('artist') or '-'} — {c.get('url')}  \n  "
             f"usado em: {', '.join(mm(t) for _, ts in v for t in ts)}")
L += ["", "## Pexels / Pixabay (licença própria do site: uso comercial grátis, crédito opcional)", ""]
for k, v in sorted(api.items()):
    c = v[0][0]
    L.append(f"- {c.get('credit')} — {c.get('license')} — {c.get('url')}  \n  usado em: {', '.join(mm(t) for _, ts in v for t in ts)}")
if not api:
    L.append("- (nenhuma)")
mp = D / "music_plan.json"  # trilha sonora (scripts/music_mix.py)
if mp.exists():
    plan = json.loads(mp.read_text("utf-8"))
    pool = {v["title"]: v for v in json.loads((D / "music_pool.json").read_text("utf-8")).values()}
    seen = {}
    for seg in plan:
        seen.setdefault(seg["title"], {"license": seg["license"], "page": seg["page"], "spans": []})["spans"].append(
            f"{mm(seg['from_s'])}–{mm(seg['to_s'])}")
    strip = lambda t: t[5:] if t.startswith("File:") else t  # pool antigo guardava "File:..."
    by = [t for t, m in seen.items() if lic_class(m["license"]) == "credit"]
    L += ["", f"## Crédito da trilha sonora (obrigatório: {len(by)} faixas CC BY)", ""]
    for t in by:
        L.append(f"- Music: \"{strip(t)}\" by {(pool.get(t) or {}).get('artist') or 'autor não informado'} — {seen[t]['license']} — {seen[t]['page']}")
    if not by:
        L.append("- (nenhuma)")
    L += ["", "## Trilha sonora (Wikimedia Commons) — onde cada faixa toca", ""]
    for title, m in seen.items():
        L.append(f"- \"{strip(title)}\" — {m['license']} — {m['page']}  \n  toca em: {', '.join(m['spans'])}")
    L.append("- Se o YouTube reivindicar direitos sobre a música, contestar com a página do Commons acima (licença livre com crédito na descrição).")
if unver:
    L += ["", "## UNVERIFIED (revisar antes de publicar)", ""] + [f"- {k}" for k in unver]
(D / "attribution.md").write_text("\n".join(L), "utf-8")
print(f"attribution.md: {len(used)} clipes, yt {len(yt)}, commons {len(cm)}, pexels/pixabay {len(api)}, crédito {len(credit)}, unverified {len(unver)}")
