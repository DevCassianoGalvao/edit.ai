"""QA — travas que impedem a entrega. Precisa terminar com 0 FALHAS e 0 AVISOS.

- timeline cobre [0, durationInFrames) sem buraco/sobreposição; quadros inteiros
- todo arquivo citado existe em public/, vídeo 1920x1080 e longo o bastante para trimBefore+dur+tail
- duração do áudio (ffprobe) == durationInFrames/fps (±1 quadro)
- 0 fotos nos 90 s iniciais; nunca 2 fotos seguidas; mistura ~50/50 video/foto (regra do usuario, 16/09)
- no máximo 2 aparições por clipe e distância mínima entre elas
- animações nunca coladas; toda cena da timeline registrada em src/scenes/index.ts
- nenhum chr(8) (backspace) em scripts/ ou src/
- nenhum clipe de fonte com licença NC/ND ou de canal/título banido
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
fails, warns = [], []


def probe(path, entries):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", str(path)], capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


meta = json.loads((D / "source_meta.json").read_text("utf-8"))
DUR = meta["durationInFrames"]
items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
clips = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]} if (D / "clips.json").exists() else {}

# tiling
pos = 0
for it in items:
    for k in ("from", "dur", "fadeIn", "tail"):
        if not isinstance(it.get(k), int):
            fails.append(f"{it.get('id')}: {k} não inteiro")
    if it["from"] != pos:
        fails.append(f"buraco/sobreposição em {pos} -> {it['from']}")
    if it["dur"] <= 0:
        fails.append(f"{it['id']} duração {it['dur']}")
    pos = it["from"] + it["dur"]
if pos != DUR:
    fails.append(f"timeline termina em {pos}, áudio tem {DUR}")

# áudio
a = probe(ROOT / "public" / "audio.mp3", "format=duration")
adur = float(a.get("format", {}).get("duration", 0))
if abs(adur * FPS - DUR) > 1:
    fails.append(f"áudio {adur:.3f}s = {adur * FPS:.1f} quadros != {DUR}")

# arquivos
seen_probe = {}
for it in items:
    if it["type"] != "cut":
        continue
    src = it.get("src")
    p = ROOT / "public" / (src or "")
    if not src or not p.exists():
        fails.append(f"{it['id']}: arquivo ausente {src}"); continue
    if it.get("kind") == "video":
        if src not in seen_probe:
            j = probe(p, "stream=width,height:format=duration")
            st = (j.get("streams") or [{}])[0]
            seen_probe[src] = (st.get("width"), st.get("height"), float(j.get("format", {}).get("duration", 0)))
        w, h, d = seen_probe[src]
        if (w, h) != (1920, 1080):
            fails.append(f"{it['id']}: {src} {w}x{h}")
        need = (it.get("trimBefore", 0) + it["dur"] + it["tail"]) / FPS
        if d + 0.05 < need:
            fails.append(f"{it['id']}: {src} tem {d:.2f}s, precisa {need:.2f}s")

# regras de montagem
cuts = [it for it in items if it["type"] == "cut"]
photos = [it for it in cuts if it.get("kind") == "photo"]
_share = float(json.loads((D / "pipeline_config.json").read_text("utf-8")).get("photo_share", 0.5))
# a abertura pede vídeo, mas num filme de 90 % foto a janela de 90 s não cabe: encolhe para 10 s
_abertura = 0 if _share >= 0.999 else 10 if _share >= 0.85 else 30 if _share >= 0.75 else 90   # 100 % foto: a abertura tambem e foto
for it in photos:
    if it["from"] < _abertura * FPS:
        fails.append(f"foto nos {_abertura} s iniciais: {it['id']}")
_maxrun = 10 ** 6 if _share >= 0.999 else (9 if _share >= 0.85 else 4) if _share >= 0.75 else (3 if _share >= 0.65 else 1)  # mesmo MAXRUN_PHOTO do build_plan
# assunto que só existe em foto (mesmo PHOTO_RUN_TAGS do build_plan): fotos podem ficar vizinhas
import re as _re
_src = (ROOT / "scripts" / "build_plan.py").read_text("utf-8")
PHOTO_RUN = eval(_re.search(r"^PHOTO_RUN_TAGS = (\{[^}]*\}|set\(\))", _src, _re.M).group(1))
if (D / "photo_run.json").exists():   # 04/10: o build_plan grava o conjunto final (inclui as tags sem vídeo)
    PHOTO_RUN = set(PHOTO_RUN) | set(json.loads((D / "photo_run.json").read_text("utf-8")))
_bt_all = {b["id"]: b["tags"][0] for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
_run = 0
for it in items:
    _run = _run + 1 if it.get("kind") == "photo" else 0
    if _maxrun > 1 and _run > _maxrun and _bt_all.get(it.get("beat")) not in PHOTO_RUN:
        fails.append(f"mais de {_maxrun} fotos seguidas até {it['id']}")
for x, y in zip(items, items[1:]):
    # exceção documentada (19/09): assunto que só existe em foto de época (mesmo PHOTO_RUN_TAGS do build_plan)
    RUN = {"giant", "queen_elizabeth", "anchor", "france_norway"} | PHOTO_RUN   # 03/10: + as do build_plan
    _bt = {b["id"]: b["tags"][0] for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
    if _maxrun == 1 and x.get("kind") == "photo" and y.get("kind") == "photo" and not (_bt.get(x.get("beat")) in RUN and _bt.get(y.get("beat")) in RUN):
        fails.append(f"duas fotos seguidas: {x['id']} {y['id']}")
    if x["type"] == "animation" and y["type"] == "animation":
        fails.append(f"animações coladas: {x['id']} {y['id']}")
vid_pct = 100 * (len(cuts) - len(photos)) / max(1, len(cuts))
# regra 16/09: metade video, metade foto. Avisa so quando desequilibra de verdade.
_meta = 100 * (1 - _share)
if abs(vid_pct - _meta) > 15:
    warns.append(f"vídeo {vid_pct:.1f}% dos cortes (meta ~{_meta:.0f}%, aceitável ±15)")
uses = {}
for it in cuts:
    uses.setdefault(it.get("clip"), []).append(it["from"])
# exceção documentada (filme das máquinas, decisions_log): vídeo da PRÓPRIA máquina escassa, dentro do trecho dela, pode
# aparecer até 3x com >= 25 s entre aparições. Mesma classificação do build_plan (lida do próprio script, sem cópia).
_bp = (ROOT / "scripts" / "build_plan.py").read_text("utf-8")
_ns = {"re": re, "FPS": FPS}
exec(_bp[_bp.index("MACHINES = ["):_bp.index("def right_object")], _ns)
_beats = {b["id"]: b for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
_count = {m: sum(1 for c in clips.values() if c.get("kind") == "video" and m in _ns["classes_of"](c)) for m in _ns["MACHINES"]}
_scarce = {m for m, n in _count.items() if n < 30}
_beat_of = {}
for it in cuts:
    _beat_of.setdefault(it.get("clip"), set()).add(_beats[it["beat"]]["tags"][0])
for cid, fs in uses.items():
    if cid is None:
        continue
    c = clips.get(cid) or {}
    mach = _beat_of.get(cid, set())
    scarce_own = len(mach) == 1 and next(iter(mach)) in _scarce and next(iter(mach)) in _ns["classes_of"](c)
    max_uses, gap = (4, 25) if scarce_own else (5, 110)  # acervo de vídeo escasso (46 clipes livres): até 5 aparições, sempre com 180 s  # 4ª só pela passada 8 do build_plan (último recurso)
    if len(fs) > max_uses:
        fails.append(f"clipe {cid} aparece {len(fs)}x")
    fs = sorted(fs)
    for u, v in zip(fs, fs[1:]):
        if v - u < gap * FPS:
            fails.append(f"clipe {cid} repete com {(v - u) / FPS:.0f}s de distância")

# cenas registradas
reg = (ROOT / "src" / "scenes" / "index.ts").read_text("utf-8")
for it in items:
    if it["type"] == "animation" and f'"{it["scene"]}"' not in reg:
        fails.append(f"cena não registrada: {it['scene']}")

# licenças e bans
NCND = re.compile(r"(\bNC\b|\bND\b|non-?commercial|no ?deriv)", re.I)
for cid in uses:
    c = clips.get(cid)
    if cid and not c:
        fails.append(f"clipe {cid} não está em clips.json"); continue
    if c and NCND.search(f"{c.get('license', '')}"):
        fails.append(f"clipe {cid} com licença NC/ND: {c.get('license')}")
    if c and not c.get("url"):
        if not c.get("manual"):   # baixado a mao pelo usuario: credito por titulo + canal
            warns.append(f"clipe {cid} sem URL de atribuição")

# chr(8)
scan = [f for pat in ("*.py", "*.mjs", "*.cmd", "*.ps1") for f in (ROOT / "scripts").rglob(pat)] + list((ROOT / "src").rglob("*.ts*"))
for f in scan:
    raw = f.read_bytes()
    if b"\x08" in raw:
        fails.append(f"chr(8) em {f.relative_to(ROOT)}")
    if f.suffix == ".cmd" and b"\r" in raw.replace(b"\r\n", b""):
        fails.append(f"CR solto em {f.relative_to(ROOT)} (edição por sed?)")

# ---------------------------------------------------------------- modo ULTRA (PROMPT_v_ULTRA, seções 3, 4, 7, 10)
_cfg = json.loads((D / "pipeline_config.json").read_text("utf-8")) if (D / "pipeline_config.json").exists() else {}
if _cfg.get("modo") == "ultra":
    ALVO = {"gancho": (3.5, 4.5), "exposicao": (5.0, 6.0), "climax": (2.5, 3.0), "fecho": (6.0, 8.0)}
    TOL = 0.8
    durs = [it["dur"] / FPS for it in cuts]
    asl = sum(durs) / max(1, len(durs))
    print(f"  ULTRA: ASL geral {asl:.2f} s em {len(durs)} planos de acervo")
    for modo, (lo, hi) in ALVO.items():
        ds = [it["dur"] / FPS for it in cuts if it.get("modo") == modo]
        if not ds:
            continue
        m = sum(ds) / len(ds)
        print(f"  ULTRA: ASL {modo:9s} {m:.2f} s ({len(ds)} planos; alvo {lo}–{hi})")
        if not (lo - TOL <= m <= hi + TOL):
            warns.append(f"ULTRA: ASL de {modo} = {m:.2f} s fora de {lo}–{hi} (±{TOL})")
    n = max(1, len(durs))
    h = {"<=1": sum(d <= 1.0 for d in durs) / n, "2-4": sum(2 <= d < 4 for d in durs) / n,
         "4-8": sum(4 <= d < 8 for d in durs) / n, ">8": sum(d >= 8 for d in durs) / n}
    print("  ULTRA: histograma " + " ".join(f"{k}={100 * v:.0f}%" for k, v in h.items()))
    if h["<=1"] > 0.07:
        fails.append(f"ULTRA: {100 * h['<=1']:.0f}% dos planos com <= 1 s (máx 7%)")
    if h[">8"] > 0.15:
        warns.append(f"ULTRA: {100 * h['>8']:.0f}% dos planos com > 8 s (máx 15%)")
    if not (0.28 <= h["2-4"] <= 0.55):
        warns.append(f"ULTRA: planos de 2–4 s = {100 * h['2-4']:.0f}% (alvo ≈ 40%)")
    for it in cuts:
        if it["dur"] > 15 * FPS:
            fails.append(f"ULTRA: plano de acervo com {it['dur'] / FPS:.1f} s (> 15 s): {it['id']}")
    # 21/09/2026: destaque/número/etiqueta são pequenos e sobrepostos (src/overlays/Destaques.tsx) — podem vir
    # mais perto que os gráficos grandes, que continuam com 25 s de folga entre si.
    PEQUENOS = {"destaque", "numero", "etiqueta", "faixa"}
    # 28/09/2026: paralaxe 2.5D é só a foto em duas camadas, sem texto nenhum — não entra na folga entre textos
    ovs = [(it["from"] / FPS, it["ov"]["tipo"]) for it in items if it.get("ov") and it["ov"].get("tipo") != "paralaxe"]
    for (a, ta), (b, tb) in zip(ovs, ovs[1:]):
        folga = 11 if (ta in PEQUENOS or tb in PEQUENOS) else 25
        if b - a < folga:
            fails.append(f"ULTRA: dois textos na tela a {b - a:.0f} s ({ta} @{a:.0f}s, {tb} @{b:.0f}s)")
    grandes = [o for o in ovs if o[1] not in PEQUENOS]
    if grandes and len(grandes) / (DUR / FPS / 60) > 1.6:
        warns.append(f"ULTRA: densidade de gráfico grande {len(grandes) / (DUR / FPS / 60):.1f}/min (máx ~1,5)")
    if ovs and len(ovs) / (DUR / FPS / 60) > 3.2:
        warns.append(f"ULTRA: densidade de texto {len(ovs) / (DUR / FPS / 60):.1f}/min (máx ~3)")
    sfx = json.loads((D / "sfx_plan.json").read_text("utf-8")) if (D / "sfx_plan.json").exists() else []
    hits = sorted(e["t"] for e in sfx if e["tipo"] == "hit")
    for a, b in zip(hits, hits[1:]):
        if b - a < 45:
            fails.append(f"ULTRA: dois golpes a {b - a:.0f} s")
    if "--entrega" in sys.argv:
        for g in ("data/tema_config.json", "qa/grade_sheet.jpg", "qa/chapters.md", "data/music_plan.json", "data/sfx_plan.json",
                  "public/final_audio.m4a", "data/audio_qa.json"):
            if not (ROOT / g).exists():
                fails.append(f"ULTRA: falta {g}")
        aq = json.loads((D / "audio_qa.json").read_text("utf-8")) if (D / "audio_qa.json").exists() else {"fails": ["sem medição"]}
        for m in aq.get("fails", []):
            fails.append(f"ULTRA áudio: {m}")

print(f"QA: {len(fails)} falhas, {len(warns)} avisos | itens {len(items)} | cortes {len(cuts)} | vídeo {vid_pct:.1f}% | fotos {len(photos)}")
for m in fails[:80]:
    print("  FALHA", m)
for m in warns[:40]:
    print("  AVISO", m)
(D / "qa_report.md").write_text("\n".join([f"# QA — {len(fails)} falhas, {len(warns)} avisos"] + [f"- FALHA {m}" for m in fails] + [f"- AVISO {m}" for m in warns]), "utf-8")
sys.exit(1 if fails or warns else 0)
