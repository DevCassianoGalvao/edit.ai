"""Sobe a fatia de VÍDEO de uma timeline já montada até o alvo (pipeline_config.photo_share).

Por que existe: o casamento do build_plan enche o slot de vídeo com FOTO quando o beat não tinha vídeo da
própria tag na hora. Depois que a colheita de vídeo termina, dá para trocar essas fotos por vídeo sem
remontar o filme — e sem reembaralhar o que já foi aprovado na folha.

Troca só o que pode: corte de FOTO em posição de slot de vídeo, com clipe de vídeo da MESMA tag do beat
(ou da lista de ambientação do próprio beat), respeitando as mesmas travas do build_plan:
  - clipe longo o bastante (dur >= corte + cauda)
  - no máximo MAX_USES aparições do mesmo clipe, com REUSE_GAP de distância
  - nunca dois cortes vizinhos da mesma fonte
  - nunca em corte travado na folha (data/image_locks.json)
Uso: python rebalance_video.py [--alvo 0.30] [--seco]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
MAX_USES, REUSE_GAP = 3, 180 * FPS
SOURCE_CAP = 5   # um rolo genérico (trânsito holandês) tomava 16 dos 67 cortes de vídeo

cfg = json.loads((D / "pipeline_config.json").read_text("utf-8"))
ALVO = float(sys.argv[sys.argv.index("--alvo") + 1]) if "--alvo" in sys.argv else 1 - float(cfg.get("photo_share", 0.5))
tl = json.loads((D / "timeline.json").read_text("utf-8"))
items = tl["items"]
clips = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
beats = {b["id"]: b for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
locks = json.loads((D / "image_locks.json").read_text("utf-8")) if (D / "image_locks.json").exists() else {}
# ambientação POR REGIÃO do beat: rua europeia não entra em trecho do Brasil e vice-versa
EUROPA = {"bruxelas", "madri", "londres", "stuttgart", "paris", "oxford", "euro7", "eu_2035", "noruega",
          "citroen_c3", "porsche_macan", "porsche_718", "renault_zoe", "suzuki_jimny", "trabant",
          "transito_europa", "lez_placa", "ev_carregando"}
BRASIL = {"diesel_brasil", "proconve", "modificado", "transito_brasil", "importados"}
FB_EUROPA = ["transito_europa", "madri", "londres", "paris", "bruxelas", "stuttgart", "oxford", "poluicao", "sucata"]
FB_BRASIL = ["transito_brasil", "oficina", "concessionaria", "poluicao", "sucata"]
FB_GERAL = ["poluicao", "sucata", "transito_europa"]

cortes = [i for i, it in enumerate(items) if it["type"] == "cut"]
usos, fontes = {}, {}
for it in items:
    if it.get("clip"):
        usos.setdefault(it["clip"], []).append(it["from"])
        fontes[clips.get(it["clip"], {}).get("source")] = fontes.get(clips.get(it["clip"], {}).get("source"), 0) + 1

vid = lambda: sum(1 for i in cortes if items[i].get("kind") == "video")
alvo_n = round(ALVO * len(cortes))
print(f"[rebalance] {vid()}/{len(cortes)} cortes em vídeo ({100 * vid() / len(cortes):.1f}%); alvo {alvo_n} ({100 * ALVO:.0f}%)")


def vizinho_mesma_fonte(i, src):
    for j in (i - 2, i - 1, i + 1, i + 2):
        if 0 <= j < len(items) and items[j].get("clip"):
            if clips.get(items[j]["clip"], {}).get("source") == src:
                return True
    return False


def candidato(i):
    it = items[i]
    b = beats[it["beat"]]
    need = it["dur"] + it.get("tail", 0)
    t0 = b["tags"][0]
    fb = FB_EUROPA if t0 in EUROPA else FB_BRASIL if t0 in BRASIL else FB_GERAL
    ordem = list(b["tags"]) + [t for t in fb if t not in b["tags"]]
    for grau, tag in enumerate(ordem):
        melhor, nota = None, None
        for c in clips.values():
            if c["kind"] != "video" or tag not in c.get("tags", []) or c["dur"] < need:
                continue
            prev = usos.get(c["id"], [])
            if len(prev) >= MAX_USES or any(abs(it["from"] - f) < REUSE_GAP for f in prev):
                continue
            if fontes.get(c.get("source"), 0) >= SOURCE_CAP or vizinho_mesma_fonte(i, c.get("source")):
                continue
            s = grau * 10 + len(prev) * 4
            if nota is None or s < nota:
                melhor, nota = c, s
        if melhor is not None:
            return melhor, grau
    return None, None


trocados, por_grau = 0, {}
for k, i in enumerate(cortes):
    if vid() >= alvo_n:
        break
    it = items[i]
    if it.get("kind") != "photo" or it["id"] in locks or it.get("how") == "lock":
        continue
    if (k % 10) not in (0, 3, 7):   # mesmos slots de vídeo do build_plan
        continue
    c, grau = candidato(i)
    if c is None:
        continue
    antigo = it.get("clip")
    if antigo:
        usos[antigo].remove(it["from"])
        src0 = clips.get(antigo, {}).get("source")
        fontes[src0] = max(0, fontes.get(src0, 1) - 1)
    usos.setdefault(c["id"], []).append(it["from"])
    fontes[c.get("source")] = fontes.get(c.get("source"), 0) + 1
    k0 = len(usos[c["id"]]) - 1
    it.update(kind="video", src=c["file"], clip=c["id"], move=None, how="rebalance",
              trimBefore=0 if k0 == 0 else max(0, c["dur"] - (it["dur"] + it.get("tail", 0))))
    trocados += 1
    por_grau[grau] = por_grau.get(grau, 0) + 1

# 2ª passada: quebra fila de mais de 3 fotos seguidas (trava do qa.py) em beat que TEM vídeo próprio
import re as _re
PR = eval(_re.search(r"^PHOTO_RUN_TAGS = (\{[^}]*\})", (ROOT / "scripts" / "build_plan.py").read_text("utf-8"), _re.M).group(1))
tag0 = lambda it: beats.get(it.get("beat"), {}).get("tags", [None])[0]
for _ in range(6):
    run, quebrou = 0, False
    for i in cortes:
        it = items[i]
        run = run + 1 if it.get("kind") == "photo" else 0
        if run <= 3 or tag0(it) in PR or it["id"] in locks:
            continue
        c, grau = candidato(i)
        if c is None:
            continue
        antigo = it.get("clip")
        if antigo:
            usos[antigo].remove(it["from"])
            s0 = clips.get(antigo, {}).get("source")
            fontes[s0] = max(0, fontes.get(s0, 1) - 1)
        usos.setdefault(c["id"], []).append(it["from"])
        fontes[c.get("source")] = fontes.get(c.get("source"), 0) + 1
        k0 = len(usos[c["id"]]) - 1
        it.update(kind="video", src=c["file"], clip=c["id"], move=None, how="rebalance-fila",
                  trimBefore=0 if k0 == 0 else max(0, c["dur"] - (it["dur"] + it.get("tail", 0))))
        trocados += 1
        por_grau[grau] = por_grau.get(grau, 0) + 1
        run, quebrou = 0, True
    if not quebrou:
        break

print(f"[rebalance] {trocados} fotos viraram vídeo | graus {por_grau} -> {vid()}/{len(cortes)} "
      f"({100 * vid() / len(cortes):.1f}% vídeo)")
if "--seco" not in sys.argv:
    (D / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), "utf-8")
    print("[rebalance] data/timeline.json gravada")
