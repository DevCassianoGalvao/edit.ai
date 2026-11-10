"""DOSSIE + NOMES_FORA do filme MSC Irina (pt, 31/10) — grava em build_overlays.py (backup em _bak_tema_roadster/).
`para` dos cartões = índice do parágrafo do MASTER (90, pausas incluídas).
`src`/`foto`/`fundo` = "@tag" -> foto APROVADA dessa tag (data/clips.json, sem repetir). Uso: python scripts/_dossie_msc.py"""
import json, re, shutil, sys
from pathlib import Path

S = Path(__file__).resolve().parent
R = S.parent
sys.path.insert(0, str(S))
from _dossie_msc_cards import DOSSIE, PROPRIOS
_txt = chr(10).join(x.get("text", "") for x in json.loads((R / "data" / "master_transcript.json").read_text("utf-8"))["paragraphs"])  # fr: o script.txt tem a grafia fonética (Bé-Igrec-Dé)
_TOK = re.compile(r"^[A-ZÀ-ÖØ-Þ][a-zà-ÿ'’]+(?:[-'’][A-Za-zà-ÿ]+)?$")
NOMES_FORA = set()
for _fr in re.split(r"[.!?:;]\s+|\n+", _txt):
    _cru = _fr.split()
    _ws = [re.sub(r"^[^\w']+|[^\w']+$", "", x) for x in _cru]
    _corta = [bool(re.search(r"[,;:!?—–)]$", x)) for x in _cru]
    for i in range(len(_ws)):
        run = []
        for j in range(i, len(_ws)):
            if not (_TOK.match(_ws[j]) or re.match(r"^[A-Z]{2,5}$", _ws[j])):
                break
            run.append(_ws[j].upper())
            nome = " ".join(run)
            if nome not in PROPRIOS:
                NOMES_FORA.add(nome)
            if _corta[j]:
                break
NOMES_FORA = sorted(NOMES_FORA)

clips = json.loads((R / "data" / "clips.json").read_text("utf-8"))["clips"]
fotos = {}
for c in clips:
    f = c.get("file", "")
    if c.get("kind", "photo") in ("photo", "image") or f.endswith((".jpg", ".png")):
        for t in c.get("tags", [])[:1]:
            fotos.setdefault(t, []).append(f)
_wr = set(json.loads((R / "data" / "window_rejects.json").read_text("utf-8"))) if (R / "data" / "window_rejects.json").exists() else set()
usado = {f for fs in fotos.values() for f in fs if Path(f).stem in _wr}


def pega(tag):
    for f in fotos.get(tag, []) + [g for r in ("irina", "megaship", "boxes", "mar") for g in fotos.get(r, [])]:
        if f not in usado:
            usado.add(f)
            return f
    raise SystemExit(f"[dossie] sem foto livre da tag {tag}")


def resolve(x):
    if isinstance(x, str) and x.startswith("@"):
        return pega(x[1:])
    if isinstance(x, list):
        return [resolve(v) for v in x]
    if isinstance(x, dict):
        return {k: resolve(v) for k, v in x.items()}
    return x


out = [resolve(d) for d in DOSSIE]
bo = S / "build_overlays.py"
bk = R / "_bak_tema_msc" / "build_overlays.py"
if not bk.exists():
    shutil.copy2(bo, bk)
t = bo.read_text("utf-8")
a = t.index("DOSSIE = [")
z = t.index("\n]\n", a) + 3
t = t[:a] + "DOSSIE = [  # 21/10/2026 MSC Irina porta-contêineres (pt)\n" + "".join(f"    {d!r},\n" for d in out) + "]\n" + t[z:]
a = t.index("NOMES_FORA = {")
z = t.index("\n}\n", a) + 3
t = t[:a] + "NOMES_FORA = {  # 31/10/2026 pt (msc): todo token maiúsculo que não é nome próprio (_dossie_msc.py)\n    " + ", ".join(repr(n) for n in NOMES_FORA) + ",\n}\n" + t[z:]
bo.write_text(t, "utf-8")
print(f"[dossie] {len(out)} cartões gravados; fotos usadas {len(usado)}")
