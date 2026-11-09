"""Escolhe fontes para a folha de sondagem — tema Challenger e o Apendice F (en).

Commons: licença ok, >=1080p (ou >=720p se --allow720), duração >=15s, sem NC/ND; ULTRALEVE (ou o modelo
nomeado no roteiro) no TÍTULO; simulador/aeromodelo/drone/acidente/paramotor nunca entra.
YouTube: passou a regra de classe do fetch_video e o assunto está no título.
Equilíbrio: fontes distribuídas entre os temas (teto por tema), no máximo 3 por canal.
Uso: python select_probe.py N_COMMONS N_YT OUT.json [--skip data/source_side.json] [--focus REGEX] [--allow720]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cm = json.loads((ROOT / "data/commons_video_pool.json").read_text("utf-8")) if (ROOT / "data/commons_video_pool.json").exists() else {}
yt = json.loads((ROOT / "data/yt_pool.json").read_text("utf-8")) if (ROOT / "data/yt_pool.json").exists() else {}
beats = json.loads((ROOT / "data/beats.json").read_text("utf-8"))
side = {}
if "--skip" in sys.argv:
    p = Path(sys.argv[sys.argv.index("--skip") + 1])
    side = json.loads(p.read_text("utf-8")) if p.exists() else {}

B = chr(92) + "b"   # nunca escrever a barra invertida junto do b: vira BACKSPACE em ferramenta que interpreta escape
D = chr(92) + "d"
# ASSUNTO FORTE no TITULO: o onibus espacial, a peca, a investigacao ou a NASA dos anos 80
SUBJ = re.compile(
    r"(space ?shuttle|challenger|columbia|discovery|atlantis|endeavour|\bsts\b|sts-\d|"
    r"\bnasa\b|kennedy space|cape canaveral|marshall space|mission control|"
    r"solid rocket|booster|\bsrb\b|o-?ring|seal|gasket|field joint|"
    r"feynman|rogers commission|presidential commission|hearing|testimony|"
    r"launch|liftoff|lift-off|rollout|countdown|"
    r"astronaut|crew|space suit|"
    r"rocket engine|test stand|test fire|"
    r"1986|1988|archival|archive footage|newsreel|"
    r"engineer|engineering|laboratory|"
    r"icicle|ice|frost|freezing)", re.I)
PLACE_BAN = re.compile(
    r"(spacex|falcon ?9|starship|blue origin|artemis|\bsls\b|electron rocket|"
    r"kerbal|simulator|gameplay|game ?play|\bmod\b|sandbox|minecraft|roblox|"
    r"scale model|1/\d+|model kit|diorama|\brc\b|"
    r"\bcgi\b|3d model|render|blender|unreal|ai generated|midjourney|animation|motion graphics|"
    r"movie clip|film scene|trailer|reenact|re-enact|"
    r"conspiracy|flat earth|hoax|faked)", re.I)
BAD = re.compile(
    r"(top \d+|#shorts|reaction|react|compilation|tier list|facts you|"
    r"podcast|lecture series|debate|"
    r"full documentary|full episode|audiobook|"
    r"asmr|prank|quiz|trivia|"
    r"how much money|salary|exposed)", re.I)
TAG_RE = {
    "lancamento": r"launch|liftoff|lift-off|countdown|rollout|pad \d|crawler",
    "acidente": r"challenger|disaster|explosion|breakup|accident|columbia",
    "peca": r"solid rocket|booster|\bsrb\b|o-?ring|seal|gasket|field joint|engine|test stand",
    "controle": r"mission control|control room|console|flight controller",
    "investigacao": r"feynman|commission|hearing|testimony|report|investigation",
    "nasa": r"\bnasa\b|kennedy space|cape canaveral|marshall|vehicle assembly|facility",
    "gente": r"astronaut|crew|engineer|training|space suit|classroom|press",
    "arquivo": r"1986|1988|archival|archive footage|newsreel|news report",
}
TAG_RE = {k: re.compile(v, re.I) for k, v in TAG_RE.items()}
FOREIGN = re.compile("|".join(re.escape(f.strip()) for f in beats["foreign"]), re.I)
N_CM, N_YT, OUT = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
MINH = 720 if "--allow720" in sys.argv else 1080
FOCUS = re.compile(sys.argv[sys.argv.index("--focus") + 1], re.I) if "--focus" in sys.argv else None


def tag_of(txt):
    return next((k for k, r in TAG_RE.items() if r.search(txt)), "other")


def balanced(cands, n, per_tag, key_group=None):
    pick, by_tag, by_group = [], {}, {}
    for c in cands:
        t = c["tag"]
        g = key_group(c) if key_group else None
        if by_tag.get(t, 0) >= per_tag or (g is not None and by_group.get(g, 0) >= 3):
            continue
        by_tag[t] = by_tag.get(t, 0) + 1
        if g is not None:
            by_group[g] = by_group.get(g, 0) + 1
        pick.append(c)
        if len(pick) >= n:
            break
    return pick


cands = []
for t, e in cm.items():
    if not e.get("pool_ok") or (e.get("height") or 0) < MINH or (e.get("duration") or 0) < 15:
        continue
    desc = e.get("desc", "") or ""
    txt = f"{t} {desc}"
    # assunto no TÍTULO: a descrição do Commons cita "aircraft" em vídeo de qualquer coisa
    if not SUBJ.search(t) or BAD.search(t) or PLACE_BAN.search(t) or BAD.search(desc[:300]) or FOREIGN.search(t) or FOREIGN.search(desc[:400]) or f"cm:{t}" in side:
        continue
    if (e.get("duration") or 0) > 1200 or (FOCUS and not FOCUS.search(txt)):
        continue
    score = (3 if SUBJ.search(t) else 1) + (1 if re.search(r"b-?roll|flight|takeoff|landing|cockpit|build", txt, re.I) else 0) \
        + min(e["duration"], 300) / 300
    cands.append({"score": score, "tag": tag_of(txt), "key": f"cm:{t}", "url": e["url"], "duration": e["duration"],
                  "label": f"CM {e['height']}p {e['duration']:.0f}s {t[5:120]}"})
cands.sort(key=lambda c: -c["score"])
pick_cm = balanced(cands, N_CM, max(3, N_CM // 8 + 1))

ytc = []
for e in yt.values():
    title = e.get("title") or ""
    if e.get("class_reject") or f"yt:{e['id']}" in side or not SUBJ.search(title) or BAD.search(title) or PLACE_BAN.search(title) or FOREIGN.search(title):
        continue
    if FOCUS and not FOCUS.search(title):
        continue
    bonus = bool(re.search(r"b-?roll|4k|no commentary|onboard|pov|raw", title, re.I))
    ytc.append({"score": len(e.get("queries") or []) + bonus, "tag": tag_of(title), "channel": e["channel"], "key": f"yt:{e['id']}",
                "url": e["url"], "duration": e["duration"], "label": f"YT {e['duration']}s [{e['channel']}] {title[:110]}"})
ytc.sort(key=lambda c: -c["score"])
pick_yt = balanced(ytc, N_YT, max(3, N_YT // 10 + 1), key_group=lambda c: c["channel"])

pick = [{k: c[k] for k in ("key", "url", "duration", "label")} for c in pick_cm + pick_yt]
OUT.write_text(json.dumps(pick, ensure_ascii=False, indent=1), "utf-8")
cov = sorted({c["tag"] for c in pick_cm + pick_yt})
print(f"commons candidatos {len(cands)} -> {len(pick_cm)}; yt candidatos {len(ytc)} -> {len(pick_yt)}; temas cobertos {len(cov)}: {cov}")
