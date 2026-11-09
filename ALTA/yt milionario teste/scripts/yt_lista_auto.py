"""Lista de SONDA do YouTube montada sozinha a partir do data/yt_pool.json (depois do fetch_video.py).

24/09/2026: no filme dos motores eu escolhi 56 vídeos à mão, a sonda levou ~45 min (1 extração a cada 45 s, regra
da cota) e 21 caíram na folha — 7 só por serem verticais/4:3/abaixo de 720p, quase todos Shorts. Esta lista:
  - tira o que a regra de classe já recusou, Short (< 60 s) e vídeo longo demais (> 60 min);
  - pontua o título: footage (drone, 4K, tour, walkaround, timelapse, running) sobe; aula/tutorial/entrevista/
    webinar/review (cabeça falante, slide, texto na tela) desce;
  - pega as N melhores de CADA busca (variedade de assunto) até o teto.
Com a lista pronta logo depois da transcrição, a sonda roda em segundo plano enquanto eu escrevo beats/cenas/cartões.

Uso: python yt_lista_auto.py SLUG [--por-busca 2] [--teto 20]

25/09/2026: teto 36 -> 20. Para 20 % de vídeo (~50 cortes) 20 fontes boas bastam; a sonda (1 extração a cada
45 s, regra da cota) cai de ~30 para ~15 min.  -> data/yt_lista_SLUG.txt (ID prio comentário)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
BOM = re.compile(r"\b(4k|8k|uhd|drone|aerial|footage|tour|walk ?around|walkaround|timelapse|time-lapse|running|"
                 r"start ?up|launch|inside|onboard|on board|working|operation|b-?roll|cinematic)\b", re.I)
RUIM = re.compile(r"\b(how to|tutorial|explained|class|lecture|lesson|webinar|interview|review|podcast|reaction|"
                  r"animation|3d|simulation|simulator|cartoon|facts|quiz|top \d+|compilation|news|update|"
                  r"procedure|familiari[sz]ation|diy|mix|guide)\b", re.I)


def arg(n, d):
    return type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d


def pontua(e):
    t, dur = e["title"], e.get("duration") or 0
    s = 2.0 * len(BOM.findall(t)) - 3.0 * len(RUIM.findall(t))
    s += 1.0 if 120 <= dur <= 1800 else 0.0          # 2-30 min: filmagem de verdade, não compilado de 2 h
    s -= 1.0 if t.count("#") >= 3 else 0.0            # título de Short/reel reaproveitado
    return s


def main():
    slug = sys.argv[1]
    por, teto = arg("--por-busca", 2), arg("--teto", 15)   # 29/09/2026: 20 -> 15 (3 baias somadas levaram aviso de robô)
    pool = json.loads((D / "yt_pool.json").read_text("utf-8"))
    cands = [e for e in pool.values() if e.get("queries") and not e.get("class_reject")
             and 60 <= (e.get("duration") or 0) <= 3600]   # sem "queries" = entrou pela sonda, não pela busca
    por_busca = {}
    for e in cands:
        por_busca.setdefault(e["queries"][0], []).append(e)
    escolhidos, vistos = [], set()
    rodada = 0
    while len(escolhidos) < teto and rodada < por:
        for q, es in por_busca.items():
            es_ord = sorted((x for x in es if x["id"] not in vistos), key=lambda x: -pontua(x))
            if es_ord and pontua(es_ord[0]) > -2 and len(escolhidos) < teto:
                e = es_ord[0]
                escolhidos.append((e, q))
                vistos.add(e["id"])
        rodada += 1
    out = D / f"yt_lista_{slug}.txt"
    linhas = [f"{e['id']} {1 if pontua(e) > 0 else 2} {q[:40]} | {e['title'][:70]}" for e, q in escolhidos]
    out.write_text("\n".join(linhas) + "\n", "utf-8")
    for l in linhas:
        print(l)
    print(f"[yt_lista] {len(escolhidos)} vídeos de {len(por_busca)} buscas ({len(cands)} candidatos) -> {out}")


if __name__ == "__main__":
    main()
