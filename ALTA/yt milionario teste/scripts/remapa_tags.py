"""RODADA ÚNICA DE JUÍZES — 04/10/2026 (meta: filme em 50-60 min).

A 2ª rodada de busca + juízes custava 40-60 min por filme, e em tema raro (salão polonês por dentro, balsa inflada,
tribunal brasileiro) ela voltava quase vazia de novo — eu acabava trocando a tag do trecho à mão. Este script faz
isso logo depois da 1ª rodada (`juizes.py juntar`):
  - cobertura de cada tag = fotos aprovadas (juízes + banco) + janelas de vídeo aprovadas (yt_review/api_review);
  - tag com cobertura < LIMIAR da cota vira, nos beats, a tag COBERTA mais parecida (sobra >= 1,2x a cota),
    escolhida pela semelhança das DESCRIÇÕES das tags no CLIP local (texto x texto) — mesmo assunto, outra imagem;
  - troca só os beats necessários (primeiro onde a tag é a 2ª, depois onde é a 1ª) até a demanda caber no que existe;
  - grava backup do beats.py (scripts/beats.py.bak_remapa) e o relatório data/remapa.md.
O texto dos cartões continua dizendo o item exato (ex.: "a faca de ponta arredondada") — a imagem é que muda.

Uso: python remapa_tags.py [--simular] [--limiar 0.5]
"""
import json, math, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))
from demanda import cotas  # noqa: E402

MIN_SIM = 0.78   # abaixo disso a troca vira a ambientação REGIONAL do filme (build_plan.py), não um assunto qualquer
LIMIAR = float(sys.argv[sys.argv.index("--limiar") + 1]) if "--limiar" in sys.argv else 0.5
SIMULAR = "--simular" in sys.argv
J = lambda n, d: json.loads((D / n).read_text("utf-8")) if (D / n).exists() else d


def cobertura():
    cob = {}
    for v in J("photo_side.json", {}).values():
        if v.get("verdict") == "ok" and v.get("tags"):
            cob[v["tags"][0]] = cob.get(v["tags"][0], 0) + 1
    side = J("photo_side.json", {})
    pool = J("photo_pool.json", {})
    for n, tags in J("photo_approve.json", {"approve": {}}).get("approve", {}).items():   # juntar ainda sem photo_review
        if tags:
            cob[tags[0]] = cob.get(tags[0], 0) + 1
    for rev in ("yt_review.json", "api_review.json"):
        for tiles in J(rev, {}).values():
            for ts in tiles.values():
                for t in ts[:1]:
                    cob[t] = cob.get(t, 0) + 1   # cada quadro aprovado ~ 1 corte de vídeo
    return cob


def main():
    beats = J("beats.json", {})
    descr = beats.get("tags", {})
    q = cotas(bruta=True)
    cob = cobertura()
    falta = {t: (cob.get(t, 0), c) for t, c in q.items() if c and cob.get(t, 0) < LIMIAR * c}
    sobra = {t for t, c in q.items() if c and cob.get(t, 0) >= 1.2 * c}
    if not falta:
        print("[remapa] nenhuma tag abaixo de", LIMIAR, "da cota — nada a trocar"); return
    import prefilter as pf
    if not pf.disponivel():
        sys.exit("[remapa] CLIP indisponível — trocar à mão")
    emb = {t: pf.emb_txt(f"{t.replace('_', ' ')}: {descr.get(t, '')}"[:300]) for t in set(falta) | sobra}
    p = ROOT / "scripts" / "beats.py"
    src = p.read_text("utf-8")
    ent = list(re.finditer(r'(\d+): \["([^"]+)", "([^"]+)", (\w)\]', src))
    trocas, rel = {}, []
    for t, (tem, cota) in sorted(falta.items(), key=lambda kv: kv[1][0] / max(1, kv[1][1])):
        cands = sorted(sobra, key=lambda s: -float(emb[t] @ emb[s]))
        if not cands:
            rel.append(f"- {t}: {tem}/{cota} — sem tag coberta para trocar"); continue
        alvo = cands[0]
        sim = float(emb[t] @ emb[alvo])
        if sim < MIN_SIM:   # nada parecido coberto: cai na ambientação regional coberta
            reg = re.search(r"^REGIONAL = (\[[^\]]*\])", (ROOT / "scripts" / "build_plan.py").read_text("utf-8"), re.M)
            reg = [r for r in (eval(reg.group(1)) if reg else []) if r in sobra]
            if reg:
                cands = reg + [c for c in cands if c not in reg]
                alvo, sim = cands[0], float(emb[t] @ emb[cands[0]]) if cands[0] in emb else 0.0
        usos = [m for m in ent if t in (m.group(2), m.group(3))]
        manter = math.floor(len(usos) * tem / cota) if cota else 0   # beats que a cobertura atual ainda segura
        ordem = sorted(usos, key=lambda m: 0 if m.group(3) == t else 1)   # 2ª tag primeiro
        n = 0
        for m in ordem[: max(0, len(usos) - manter)]:
            a, b = m.group(2), m.group(3)
            outra = b if a == t else a
            novo = alvo if alvo != outra else (cands[1] if len(cands) > 1 else alvo)
            a2, b2 = (novo, b) if a == t else (a, novo)
            trocas[m.span()] = f'{m.group(1)}: ["{a2}", "{b2}", {m.group(4)}]'
            n += 1
        rel.append(f"- {t} ({tem}/{cota}) -> {alvo} (semelhança {sim:.2f}) em {n} de {len(usos)} beats")
    novo_src = src
    for (i, j), txt in sorted(trocas.items(), reverse=True):
        novo_src = novo_src[:i] + txt + novo_src[j:]
    print("[remapa] " + ("SIMULAÇÃO — " if SIMULAR else "") + f"{len(trocas)} beats trocados")
    print("\n".join(rel))
    (D / "remapa.md").write_text("# Remapa de tags (rodada única)\n\n" + "\n".join(rel), "utf-8")
    if not SIMULAR and trocas:
        shutil.copy2(p, p.with_name("beats.py.bak_remapa"))
        p.write_text(novo_src, "utf-8")
        print("[remapa] beats.py gravado (backup beats.py.bak_remapa) — rodar scripts/beats.py")


if __name__ == "__main__":
    main()
