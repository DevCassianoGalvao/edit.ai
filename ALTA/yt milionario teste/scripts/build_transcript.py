"""whisper_raw.json + input/script.txt -> data/master_transcript.json + data/alignment_report.md

Roteiro = verdade das PALAVRAS; Whisper = verdade do TEMPO.
Parágrafos do roteiro são ancorados às palavras do Whisper por SequenceMatcher.
"""
import difflib, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
raw = json.loads((ROOT / "data/whisper_raw.json").read_text("utf-8"))
meta = json.loads((ROOT / "data/source_meta.json").read_text("utf-8"))
DUR_F = meta["durationInFrames"]
script = (ROOT / "input/script.txt").read_text("utf-8")
import sys as _sys
_sys.path.insert(0, str(ROOT / "scripts"))
LANG = (json.loads((ROOT / "data/pipeline_config.json").read_text("utf-8")).get("screenLanguage") or "en").lower()
if LANG.startswith("pt"):
    from num_pt import num_words_pt
else:
    num_words_pt = None


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", w)


fr = lambda s: max(0, min(DUR_F, round(s * FPS)))

# ---- número do Whisper soletrado como o roteiro escreve ----
# O roteiro escreve por extenso ("one hundred and thirty", "two point two percent") e o Whisper escreve em algarismo
# ("130", "2.2%"): sem isso o casamento caía para 69–84% nos parágrafos cheios de número (filme do trem, 16/09).
UNITS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def num_words(n):
    if n < 20:
        return [UNITS[n]]
    if n < 100:
        t, r = divmod(n, 10)
        return [TENS[t]] + (num_words(r) if r else [])
    if n < 1000:
        h, r = divmod(n, 100)
        return [UNITS[h], "hundred"] + (num_words(r) if r else [])
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            q, r = divmod(n, div)
            return num_words(q) + [name] + (num_words(r) if r else [])
    return [str(n)]


def year_words(n):  # 1909 -> nineteen oh nine; 1928 -> nineteen twenty eight
    hi, lo = divmod(n, 100)
    if lo == 0:
        return num_words(hi) + ["hundred"]
    return num_words(hi) + (["oh"] if lo < 10 else []) + num_words(lo)


NUM_SPOKEN = {str(k): str(v).split() for k, v in
              (json.loads((ROOT / "data/pipeline_config.json").read_text("utf-8")).get("num_spoken") or {}).items()}


def expand(tok):
    """Token do Whisper -> lista de tokens em palavras (números soletrados)."""
    t = tok.strip().lower()
    out, tail = [], []
    if "%" in t:
        tail.append("por" if num_words_pt else "percent")
    if "$" in t:
        tail.append("reais" if num_words_pt else "dollars")
    t = t.replace(",", "").replace("$", "").replace("%", "")
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?(st|nd|rd|th)?", t)
    if not m:
        n = norm(tok)
        return ([n] if n else []) + tail
    whole, dec = int(m.group(1)), m.group(2)
    if dec is None and m.group(1) in NUM_SPOKEN:   # "103" dito "one oh three" (exceção do filme)
        return out + NUM_SPOKEN[m.group(1)] + tail
    fala = num_words_pt if num_words_pt else None
    if fala:                     # portugues le ano como cardinal: 1988 = mil novecentos e oitenta e oito
        out += fala(whole)
    elif dec is None and 2000 <= whole <= 2099 and not m.group(3):
        # 2026 falado neste roteiro e "two thousand and twenty six", nao "twenty twenty six"
        out += num_words(whole)
    elif dec is None and 1100 <= whole <= 1999 and not m.group(3):
        out += year_words(whole)
    else:
        out += num_words(whole)
    if dec:
        sep = ["virgula"] if num_words_pt else ["point"]
        dig = [(num_words_pt(int(d))[0] if num_words_pt else UNITS[int(d)]) for d in dec]
        out += sep + dig
    return out + tail


words = [w for s in raw["segments"] for w in s["words"]]
wtok, w_of = [], []  # w_of: token expandido -> índice da palavra original (o tempo vem dela)
for wi, w in enumerate(words):
    for t in expand(w["w"]):
        wtok.append(t)
        w_of.append(wi)

# ---- sentenças (pontuação do Whisper), contíguas ----
sentences, cur = [], []
for w in words:
    cur.append(w)
    if re.search(r"[.?!]\s*$", w["w"]):
        sentences.append(cur); cur = []
if cur:
    sentences.append(cur)
out_s = []
for i, ws in enumerate(sentences):
    out_s.append({"id": f"s{i + 1:04d}", "text": "".join(w["w"] for w in ws).strip(),
                  "startSec": ws[0]["s"], "endSec": ws[-1]["e"],
                  "words": [{"w": w["w"].strip(), "s": w["s"], "e": w["e"]} for w in ws]})
for i, s in enumerate(out_s):  # contíguo: início = fim da anterior
    s["startFrame"] = 0 if i == 0 else out_s[i - 1]["endFrame"]
    nxt = out_s[i + 1]["startSec"] if i + 1 < len(out_s) else meta["audioDuration"]
    s["endFrame"] = fr((s["endSec"] + nxt) / 2) if i + 1 < len(out_s) else DUR_F
    s["endFrame"] = max(s["endFrame"], s["startFrame"] + 1)

# ---- parágrafos do roteiro ancorados ----
paras = [p.strip() for p in script.split("\n") if p.strip()]
ptok, pidx = [], []
SEP = re.compile("[" + chr(45) + chr(0x2013) + chr(0x2014) + chr(47) + "]")  # hífen, travessões e barra
for i, p in enumerate(paras):
    for bruto in p.split():
        for t in SEP.split(bruto):   # "fifty-four" -> "fifty" "four" (o Whisper escreve 54)
            n = norm(t)
            if n:
                ptok.append(n); pidx.append(i)
# sigla soletrada: o roteiro escreve "C G S", "M X", "X E L"; o Whisper escreve "CGS", "MX", "XEL".
# Uma sequencia de 2+ tokens de uma letra vira um token so (o indice do paragrafo e o da primeira letra).
_pt, _pi, k = [], [], 0
while k < len(ptok):
    j = k
    while j < len(ptok) and len(ptok[j]) == 1 and ptok[j].isalpha():
        j += 1
    if j - k >= 2:
        _pt.append("".join(ptok[k:j])); _pi.append(pidx[k]); k = j
    else:
        _pt.append(ptok[k]); _pi.append(pidx[k]); k += 1
ptok, pidx = _pt, _pi

sm = difflib.SequenceMatcher(None, ptok, wtok, autojunk=False)
map_s2w = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        map_s2w[a + k] = b + k
out_p = []
for i, p in enumerate(paras):
    ks = [k for k, pi in enumerate(pidx) if pi == i and k in map_s2w]
    if not ks:
        out_p.append({"id": f"p{i:02d}", "text": p, "startSec": None, "endSec": None}); continue
    out_p.append({"id": f"p{i:02d}", "text": p, "startSec": words[w_of[map_s2w[ks[0]]]]["s"],
                  "endSec": words[w_of[map_s2w[ks[-1]]]]["e"], "matched": len(ks),
                  "tokens": sum(1 for pi in pidx if pi == i)})
# parágrafo curtíssimo pode não casar nenhum token ("The medical." tem 2): em vez de quebrar, ele recebe
# a fresta entre o fim do anterior e o começo do seguinte — o texto continua na ordem e o tiling fecha.
for i, p in enumerate(out_p):
    if p.get("startSec") is None:
        ant = next((out_p[k]["endSec"] for k in range(i - 1, -1, -1) if out_p[k].get("endSec") is not None), 0.0)
        prox = next((out_p[k]["startSec"] for k in range(i + 1, len(out_p)) if out_p[k].get("startSec") is not None), None)
        prox = DUR_F / FPS if prox is None else prox
        p["startSec"], p["endSec"] = ant, max(ant, prox)
        p["semCasamento"] = True
for i, p in enumerate(out_p):  # tiling por parágrafo
    p["startFrame"] = 0 if i == 0 else out_p[i - 1]["endFrame"]
    if i + 1 < len(out_p):
        p["endFrame"] = fr((p["endSec"] + out_p[i + 1]["startSec"]) / 2)
    else:
        p["endFrame"] = DUR_F
    if p["endFrame"] <= p["startFrame"]:      # fresta de zero: garante 1 quadro para o beat existir
        p["endFrame"] = p["startFrame"] + 1

(ROOT / "data/master_transcript.json").write_text(json.dumps(
    {"fps": FPS, "durationInFrames": DUR_F, "sentences": out_s, "paragraphs": out_p}, ensure_ascii=False, indent=1), "utf-8")

# ---- relatório ----
ok = all(s["endFrame"] > s["startFrame"] for s in out_s) and all(
    out_s[i]["startFrame"] == out_s[i - 1]["endFrame"] for i in range(1, len(out_s))) and out_s[-1]["endFrame"] <= DUR_F
okp = all(p["endFrame"] > p["startFrame"] for p in out_p)
div = []
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op != "equal":
        div.append((op, " ".join(ptok[a1:a2])[:80], " ".join(wtok[b1:b2])[:80]))
bad_s = sum(1 for p in out_p if p.get("matched", 0) < 0.85 * p.get("tokens", 1))
lines = ["# alignment_report.md", "",
         f"- Whisper: {raw['model']} ({raw['device']}), {len(words)} palavras, {len(out_s)} sentenças",
         f"- Roteiro: {len(paras)} parágrafos, {len(ptok)} tokens; casados {len(map_s2w)} ({100 * len(map_s2w) / len(ptok):.1f}%)",
         f"- Parágrafos com <85% das palavras casadas: {bad_s}",
         f"- GATE 1 sentenças contíguas/sem sobreposição/<= duração: {'OK' if ok else 'FALHA'}; parágrafos: {'OK' if okp else 'FALHA'}",
         f"- durationInFrames {DUR_F}; última sentença termina em {out_s[-1]['endFrame']}", "",
         "## Parágrafos (início–fim)", ""]
lines += [f"- {p['id']} {p['startFrame'] / FPS:7.1f}s–{p['endFrame'] / FPS:7.1f}s  {p['text'][:70]}" for p in out_p]
lines += ["", "## Amostra de 10 sentenças", ""]
lines += [f"- {s['id']} [{s['startFrame']}–{s['endFrame']}] {s['text'][:110]}" for s in out_s[:: max(1, len(out_s) // 10)][:10]]
lines += ["", f"## Divergências roteiro × falado ({len(div)} trechos; mantido o FALADO com tempo do Whisper)", ""]
lines += [f"- {op}: roteiro «{a}» / falado «{b}»" for op, a, b in div[:200]]
(ROOT / "data/alignment_report.md").write_text("\n".join(lines), "utf-8")
print("\n".join(lines[:8]))
