"""Confere os cues de cada animação (palavras escolhidas à mão nas cenas de src/scenes/AbismoScenes.tsx) contra
o que o Whisper ouviu DENTRO da janela da animação, e troca só os que não batem. Grava a mesma lista nos dois
lugares: CUES do build_plan e as cenas (cue(p, "...") nas cenas próprias; cue: "..." nos painéis).

Janela: item da timeline (from..from+20 s) quando ela existe; senão os primeiros 20 s do parágrafo.
Um cue só vale se a palavra é dita na janela e NÃO foi dita antes no mesmo parágrafo (o casamento sequencial
pegaria a primeira ocorrência e o cue cairia fora da janela).
"""
import json
import re
import unicodedata
from pathlib import Path

R = Path(__file__).resolve().parent.parent
m = json.loads((R / "data/master_transcript.json").read_text("utf-8"))
beats = json.loads((R / "data/beats.json").read_text("utf-8"))["beats"]
paras = {p["id"]: p for p in m["paragraphs"]}
_tl = R / "data/timeline.json"
ANIM = {x["scene"]: x for x in (json.loads(_tl.read_text("utf-8"))["items"] if _tl.exists() else []) if x["type"] == "animation"}
SCENE = R / "src/scenes/MojaveScenes.tsx"
JANELA = 20.0

norm = lambda s: re.sub(r"[^a-z0-9]", "", "".join(
    c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)))

STOP = set("""o a os as um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas com sem para
pra que se e ou mas nem como quando onde porque porque ja ainda tambem so apenas mais menos muito muita muitos
muitas pouco pouca poucos poucas todo toda todos todas cada qualquer quase sempre nunca aqui ali la ele ela eles
elas isso isto aquilo esse essa esses essas este esta estes estas aquele aquela seu sua seus suas dele dela deles
delas meu minha nosso nossa voce voces nos entre sobre ate desde contra depois antes durante dentro fora acima
abaixo ser sao era eram foi foram sera serao seria estar esta estao estava estavam ter tem tinha tinham teve
haver ha havia fazer faz fez feito poder pode podem podia ir vai vao dizer diz disse ver ve viu chamar chamado
chamada chamados existe existem existir parece parecem forma formas coisa coisas vez vezes parte partes tipo
tipos jeito mesmo mesma mesmos mesmas outro outra outros outras algum alguma alguns algumas nenhum nenhuma
primeiro primeira segundo segunda porque enquanto tanto tao bem mal ainda entao agora hoje sempre quase
metros metro centimetros centimetro quilos quilo""".split())


def janela(b):
    it = ANIM.get(b["anim"])
    if it is not None:
        a = it["from"] / 30
        return a, (it["from"] + it["dur"]) / 30  # 19/09: janela = a animação INTEIRA (até 50 s); os 20 s cortavam cues que o plano cobre
    p = paras[f"p{b['para']:03d}"] if f"p{b['para']:03d}" in paras else paras[f"p{b['para']:02d}"]
    return p["startSec"], min(p["endSec"], p["startSec"] + JANELA)


def palavras_entre(a, z):
    return [w for s in m["sentences"] for w in s["words"] if a <= w["s"] < z]


def casa(spec, w):
    """spec "palavra|123": palavra casa por prefixo, algarismo casa exato (o Whisper escreve números em algarismo)."""
    for alt in spec.split("|"):
        a = norm(alt)
        if (w == a) if a.isdigit() else w.startswith(a):
            return True
    return False


def confere(b, cues):
    """devolve (ok, ruins): cue é bom se casa na ordem dentro da janela e não foi dito antes no parágrafo."""
    a, z = janela(b)
    pid = f"p{b['para']:03d}" if f"p{b['para']:03d}" in paras else f"p{b['para']:02d}"
    pp = paras[pid]
    antes = {norm(w["w"]) for w in palavras_entre(pp["startSec"], a)}
    ws = [(norm(w["w"]), w["s"]) for w in palavras_entre(a, z)]
    ruins, pos = [], 0
    for c in cues:
        j = next((i for i in range(pos, len(ws)) if casa(c, ws[i][0])), None)
        if j is None or any(casa(c, x) for x in antes):
            ruins.append(c)
        else:
            pos = j + 1
    return ruins


def candidatos(b, evitar):
    a, z = janela(b)
    pid = f"p{b['para']:03d}" if f"p{b['para']:03d}" in paras else f"p{b['para']:02d}"
    pp = paras[pid]
    antes = {norm(w["w"]) for w in palavras_entre(pp["startSec"], a)}
    ws = [(norm(w["w"]), w["s"]) for w in palavras_entre(a, z)]
    cont = {}
    for t, _ in ws:
        cont[t] = cont.get(t, 0) + 1
    return [(t, s) for t, s in ws if len(t) >= 5 and t not in STOP and cont[t] == 1 and not t.isdigit()
            and t not in antes and not any(casa(e, t) for e in evitar)]


def sincroniza(t, CUES):
    """Reescreve, DENTRO do bloco de cada cena, as strings de cue na ordem de CUES (a palavra sem o "|123")."""
    reg = (R / "src/scenes/index.ts").read_text("utf-8")
    ids = dict(re.findall(r'"(A\d\d-\w+)": \{ C: (A\d\d\w+),', reg))
    for cena, exp in ids.items():
        pals = [c.split("|")[0] for c in CUES.get(cena, [])]
        a = t.index(f"export const {exp}")
        z = t.find(chr(10) + "export const ", a + 1)
        z = len(t) if z < 0 else z
        bloco = t[a:z]
        it = iter(pals)
        pat = r'cue\(p, "[^"]+"' if 'cue(p, "' in bloco else r'cue: "[^"]+"'
        n = len(re.findall(pat, bloco))
        if n != len(pals):
            print(f"!! {cena}: cena tem {n} cues, CUES tem {len(pals)}")
        rep = (lambda m_: f'cue(p, "{next(it, pals[-1])}"') if pat.startswith("cue" + chr(92)) else (lambda m_: f'cue: "{next(it, pals[-1])}"')
        t = t[:a] + re.sub(pat, rep, bloco) + t[z:]
    return t


def main():
    bp = R / "scripts/build_plan.py"
    s = bp.read_text("utf-8")
    i = s.index("CUES = {")
    j = s.index(chr(10) + "}" + chr(10), i) + 3
    ns = {}
    exec(s[i:j], ns)
    CUES = ns["CUES"]
    t = SCENE.read_text("utf-8")
    trocas, problemas = 0, 0
    for b in beats:
        if not b.get("anim"):
            continue
        cues = CUES[b["anim"]]
        ruins = confere(b, cues)
        if not ruins:
            continue
        novos = list(cues)
        cands = candidatos(b, set(cues))
        # cada cue ruim vira a palavra candidata mais próxima da posição relativa dele na lista
        for r in ruins:
            k = cues.index(r)
            if not cands:
                problemas += 1
                print(f"!! {b['anim']}: '{r}' não é dito na janela e não há candidato")
                continue
            alvo = k / max(1, len(cues) - 1)
            best = min(range(len(cands)), key=lambda q: abs(q / max(1, len(cands) - 1) - alvo))
            novo = cands.pop(best)[0]
            novos[k] = novo
            print(f"{b['anim']:22s} '{r}' -> '{novo}'")
            trocas += 1
        # a ordem falada tem de valer: reordena pela posição da palavra na janela
        a, z = janela(b)
        pal = [norm(w["w"]) for w in palavras_entre(a, z)]
        novos.sort(key=lambda c: next((q for q, x in enumerate(pal) if casa(c, x)), 1e9))
        CUES[b["anim"]] = novos
    novo = "CUES = {\n" + "".join(f'    "{k}": {json.dumps(v, ensure_ascii=False)},\n' for k, v in CUES.items()) + "}\n"
    bp.write_text(s[:i] + novo + s[j:], "utf-8")
    SCENE.write_text(sincroniza(t, CUES), "utf-8")
    print(f"[fix_cues] {trocas} trocas, {problemas} sem solução; janela = {'timeline' if ANIM else 'parágrafo'}")


if __name__ == "__main__":
    main()
