"""ESQUELETO DO TEMA — 04/10/2026 (meta: filme em 50-60 min). Roda logo depois do novo_filme.py.

Antes eu escrevia à mão, a cada filme, scripts avulsos para listar os parágrafos, achar os números na grafia do
Whisper e testar os gatilhos das animações (~30-40 min por filme). Este script entrega tudo pronto:
  data/esqueleto.md    parágrafos (tempo + início do texto), números ditos com o segundo exato, candidatos a capítulo
                       e as ANIMAÇÕES sugeridas: parágrafos com 1-4 números ditos a no máximo JANELA s um do outro
                       (regra do motion curto), espaçados >= ESPACO s, no máximo 1 a cada 3,3 min de filme.
  data/esqueleto.json  o mesmo em dados: {"paragrafos": [...], "anim": [{"para", "cues", "tokens", "t"}], "capitulos": [...]}
Os cues já saem na grafia do Whisper ("10 .000" -> "10", "1 .990" -> "990"), conferidos em ordem como o build_plan faz.
Eu escrevo só o que é de julgamento: tags/buscas, textos das cenas e dos cartões.

Uso: python esqueleto_tema.py [--janela 12] [--espaco 120]
"""
import ast, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
arg = lambda n, d: type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d
JANELA, ESPACO = arg("--janela", 12.0), arg("--espaco", 120.0)

m = json.loads((D / "master_transcript.json").read_text("utf-8"))
P, S = m["paragraphs"], m["sentences"]
dur = P[-1]["endSec"]


def palavras(i):
    a, b = P[i]["startSec"], P[i]["endSec"]
    ws = []
    for s in S:
        if a - 0.1 <= float(s["startSec"]) < b - 0.1:
            ws += ast.literal_eval(s["words"]) if isinstance(s["words"], str) else s["words"]
    return a, b, ws


def token_cue(w):
    """Token do Whisper -> cue: só os dígitos do pedaço ('981,' -> '981'; ',4' é decimal e não serve de gatilho)."""
    t = w.strip()
    if t.startswith((",", ".")):   # pedaço decimal/milhar partido: não é gatilho
        return None
    d = re.sub(r"[^0-9]", "", t)
    return d or None


par, cand, caps = [], [], []
for i in range(len(P)):
    a, b, ws = palavras(i)
    texto = " ".join(w["w"] for w in ws)
    nums = []
    for w in ws:
        c = token_cue(w["w"])
        if c and not re.fullmatch(r"(19|20)\d\d", c):   # ano sozinho raramente vale animação (vira carimbo/cartão)
            nums.append({"cue": c, "t": round(w["s"] - a, 1), "w": w["w"]})
    par.append({"i": i, "ini": round(a), "fim": round(b), "dur": round(b - a), "texto": texto[:160], "nums": nums})
    if (b - a) < 9 or texto.rstrip().endswith("?"):   # parágrafo curto ou pergunta = virada de capítulo
        caps.append(i)
    # melhor grupo de 1-4 números dentro da JANELA, sem repetir o mesmo cue (o build_plan casa em ordem)
    melhor = None
    for x in range(len(nums)):
        grupo, vistos = [], set()
        for y in range(x, len(nums)):
            if nums[y]["t"] - nums[x]["t"] > JANELA or len(grupo) == 4:
                break
            if nums[y]["cue"] in vistos:
                continue
            grupo.append(nums[y]); vistos.add(nums[y]["cue"])
        if grupo and (melhor is None or len(grupo) > len(melhor)):
            melhor = grupo
    if melhor:
        cand.append({"para": i, "t": round(a + melhor[0]["t"]), "cues": [g["cue"] for g in melhor],
                     "tokens": [f"{g['w']}@{g['t']}s" for g in melhor], "n": len(melhor)})

# escolhe as animações: mais números primeiro, espaçadas, até o teto
teto = max(6, round(dur / 60 / 3.3))
escolha = []
for c in sorted(cand, key=lambda c: (-c["n"], c["t"])):
    if len(escolha) >= teto:
        break
    if all(abs(c["t"] - e["t"]) >= ESPACO for e in escolha):
        escolha.append(c)
escolha.sort(key=lambda c: c["t"])

json.dump({"paragrafos": par, "anim": escolha, "capitulos": caps, "dur": dur}, open(D / "esqueleto.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
L = [f"# Esqueleto do tema — {len(P)} parágrafos, {dur / 60:.1f} min\n",
     f"## Animações sugeridas ({len(escolha)} de no máximo {teto}; cues a <= {JANELA:.0f} s, espaço >= {ESPACO:.0f} s)\n"]
for e in escolha:
    L.append(f"- p{e['para']:03d} @{e['t'] // 60:02d}:{e['t'] % 60:02d}  CUES {json.dumps(e['cues'], ensure_ascii=False)}  ({', '.join(e['tokens'])})")
L.append("\n## Viradas de capítulo (parágrafo curto ou pergunta)\n")
L.append(", ".join(f"p{c}" for c in caps))
L.append("\n## Parágrafos\n")
for p in par:
    n = " ".join(f"{x['w']}@{x['t']}" for x in p["nums"])
    L.append(f"- p{p['i']:03d} [{p['ini']}-{p['fim']}s] {p['texto'][:110]}" + (f"\n    números: {n}" if n else ""))
(D / "esqueleto.md").write_text("\n".join(L), "utf-8")
print(f"[esqueleto] {len(P)} parágrafos | {len(escolha)} animações sugeridas | {len(caps)} viradas -> data/esqueleto.md")
for e in escolha:
    print(f"  p{e['para']:03d} @{e['t']}s  {e['cues']}")
