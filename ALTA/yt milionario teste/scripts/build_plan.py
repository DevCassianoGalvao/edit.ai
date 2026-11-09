"""Monta o PLANO e casa os clipes: master_transcript + beats + biblioteca -> data/timeline.json

Biblioteca (data/clips.json, gerada da revisão das folhas de contato):
  {"clips": [{"id": "v0001", "kind": "video"|"photo", "file": "stock/v0001.mp4", "dur": quadros,
              "tags": ["flightdeck", ...], "source": "yt:ID"|"cm:File:...", "era": "modern"|"old"}]}
Travas/rejeições (sobrevivem entre rodadas):
  data/image_locks.json    {cut_id: clip_id}        aprovado na folha -> não volta ao casamento
  data/window_rejects.json [clip_id, ...]           rejeitado para o filme inteiro
  data/segment_rejects.json {cut_id: [clip_id, ...]} rejeitado só naquele corte
Regras:
  - 90 s iniciais: só vídeo (e animação). Nunca duas fotos seguidas (MAXRUN_PHOTO = 1).
  - no máximo MAX_USES aparições por clipe, com REUSE_GAP medido contra TODAS as outras.
  - nunca forçar tag distante: sem vídeo da tag do beat -> ambientação honesta (FALLBACK_TAGS)
    -> foto só como último degrau.
"""
import json, os, sys, unicodedata, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
LEAD_IN = 1 * FPS  # 03/10 (recado: motion graphics curtos, estilo dinâmico) era 3 s; tempo máximo de animação antes do 1º cue dito
MIN_ANIM, MAX_ANIM = 5 * FPS, 14 * FPS  # 03/10 recado: era 6 s / 38 s; teto sobe até incluir o último cue dito (cue_debug: 7 cues a +21..+27 s)
MAX_ANIM_HARD = 14 * FPS  # 03/10 recado: era 50 s; só quando o ÚLTIMO cue é dito depois do teto (A04 +47 s, A08 +46 s, A10 +40 s)
DECLUMP_CAP = 10 ** 6  # a passada que desfaz fila ignora o teto por fonte (as passadas 6 e 8 já o ignoram); quem segura
# a repetição VISUAL é MAX_USES (2 por clipe) + REUSE_GAP (180 s), e trocar 10 cortes do mesmo camarote vale mais
MIN_CUT, TARGET_CUT = 3 * FPS, int(5.5 * FPS)
# MODO ULTRA (PROMPT_v_ULTRA, seção 2): curva de ritmo por bloco, marcada no beat ("modo").
# gancho 3,5-4,5 s | exposição 5-6 s | clímax 2,5-3,0 s (inserts de 1,5-3 s) | fecho 6-8 s
RITMO = {"gancho": (int(4.0 * FPS), int(2.5 * FPS)), "exposicao": (int(5.5 * FPS), 3 * FPS),
         "climax": (int(2.8 * FPS), int(1.6 * FPS)), "fecho": (int(7.0 * FPS), int(4.0 * FPS))}
PHOTO_MAX = int(6.5 * FPS)  # cortes do plano ficam em 4,5–6,5 s; com 4,5 quase nenhuma foto cabia
FADE_ANIM = 12
_CFG = json.loads((Path(__file__).resolve().parent.parent / 'data' / 'pipeline_config.json').read_text('utf-8'))
PHOTO_SHARE = float(_CFG.get('photo_share', 0.5))  # fração de cortes em FOTO (usuário escolhe por filme)
# O gancho e so video. Em filme de 90 % foto isso e o unico trecho em que a foto nao entra, e em
# filme curto 90 s viram 9 % da duracao inteira — mesma regra do qa.py (janela de abertura).
SO_FOTO = PHOTO_SHARE >= 0.999   # filme 100 % imagem (pedido do usuario, 23/09/2026): nenhum video na biblioteca
HOOK = (0 if SO_FOTO else 10 if PHOTO_SHARE >= 0.85 else 30 if PHOTO_SHARE >= 0.75 else 90) * FPS   # 20 % video: gancho de 90 s puxava para 25 %
if SO_FOTO:
    PHOTO_MAX = int(12 * FPS)   # sem video para segurar corte longo: a foto (com o empurrao lento) segura ate 12 s
MAXRUN_PHOTO = 10 ** 6 if SO_FOTO else (9 if PHOTO_SHARE >= 0.85 else 4) if PHOTO_SHARE >= 0.75 else (3 if PHOTO_SHARE >= 0.65 else 1)
# FILME DA SOLDA: o YouTube só deu 72 clipes de vídeo em 1080p (o resto do assunto existe só em 480/720p).
# Com 2 usos por clipe o plano ficava com 40 cortes VAZIOS no trecho de saturação. Três aparições, com os
# mesmos 180 s de distância, é melhor do que buraco — está registrado no decisions_log.
MAX_USES = 3
IRMA_LIVRE = False
REUSE_GAP = 180 * FPS
# teto de cortes por FONTE (um rolo bom não pode virar o filme inteiro); a última passada afrouxa
SOURCE_CAP = 14
SOURCE_CAP_LAST = 22
FALLBACK_TAGS = ["mar", "barco_pesca", "praia", "icapui"]
# tag de AMBIENTE FECHADO (câmara, painel, sala): ambientação de dentro antes de cair para o mar aberto
INTERIOR_TAGS = {"hospital", "camara", "fabrica", "restaurante"}
INTERIOR_FALLBACK = ["hospital", "camara"]
# ambientação REGIONAL do filme (último degrau antes de ficar sem clipe) — muda por tema
REGIONAL = ["mar", "barco_pesca", "praia"]
SECAO_FB = {}

# Cue = "chave|alternativa|...". A 1ª forma é a chave que a cena lê (cue(p, "trece")).
# O Whisper escreve números em dígitos e parte o milhar ("13", ".300") → alternativas em dígito
# casam por IGUALDADE (para "13" não casar "130"); palavras casam por prefixo (acento é removido pelo norm).
# Tema Austrália: calor solar x carvão (INGLÊS): o Whisper escreve os números em dígito e ainda parte o milhar
# ("10 ,500", "2 .2 %"), por isso os cues são PALAVRAS inteiras ditas no parágrafo, na ordem em que aparecem.
CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; "a|b" = alternativas
    "L01-Rota": ["redonda", "fortaleza"],
    "L04-Ovos": ["300", "150", "milhões"],
    "L05-Queda": ["11", "4"],
    "L06-Portaria": ["1995", "43"],
    "L14-Marambaias": ["100", "icapuí"],
    "L07-Prof": ["40", "esses", "130"],
    "L15-Regras": ["10", "paradas", "dia", "tabelas"],
    "L09-Casos": ["16", "3", "7"],
    "L10-Natal": ["natal", "fogo"],
    "L13-Preco": ["120", "60", "metade"],
}



def cue_hit(spec, word):
    w = norm(word)
    for alt in spec.split("|"):
        a = norm(alt)
        if a.isdigit():
            if w == a:
                return True
        elif w.startswith(a):
            return True
    return False


def seq_hits(specs, ws):
    """Busca os cues NA ORDEM falada: cada um só casa depois do anterior (A07: "one and one half hours"
    vinha antes de "quarter" e roubava o cue "half"). Cue não encontrado não avança o cursor."""
    out, k = {}, 0
    for spec in specs:
        j = next((i for i in range(k, len(ws)) if cue_hit(spec, ws[i]["w"])), None)
        if j is not None:
            out[spec] = ws[j]
            k = j + 1
    return out


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)))


def jload(name, default):
    p = D / name
    return json.loads(p.read_text("utf-8")) if p.exists() else default


ULTRA = jload("pipeline_config.json", {}).get("modo") == "ultra"


tr = jload("master_transcript.json", None)
if tr is None:
    sys.exit("falta data/master_transcript.json")
DUR = tr["durationInFrames"]
paras = tr["paragraphs"]
beats = jload("beats.json", None)["beats"]
lib = jload("clips.json", {"clips": []})["clips"]
locks = jload("image_locks.json", {})
wrej = set(jload("window_rejects.json", []))
srej = jload("segment_rejects.json", {})
words = [dict(w, f=round(w["s"] * FPS), ef=round(w["e"] * FPS)) for s in tr["sentences"] for w in s["words"]]
sent_ends = sorted({s["endFrame"] for s in tr["sentences"]})
word_starts = sorted({w["f"] for w in words})


def snap(x, lo, hi, radius=20):
    """Prefere fim de sentença, depois início de palavra, dentro do raio e de [lo, hi]."""
    for pool in (sent_ends, word_starts):
        best = min((v for v in pool if lo <= v <= hi and abs(v - x) <= radius), key=lambda v: abs(v - x), default=None)
        if best is not None:
            return best
    return x


def beat_span(b):
    """[a, z) do beat: o parágrafo inteiro, ou a fatia k de n quando o beat tem "part" (parágrafo longo)."""
    p = paras[b["para"]]
    a, z = p["startFrame"], p["endFrame"]
    part = b.get("part")
    if not part:
        return a, z
    k, n = part
    lo = a if k == 0 else snap(a + (z - a) * k // n, a + MIN_CUT, z - MIN_CUT, radius=90)
    hi = z if k == n - 1 else snap(a + (z - a) * (k + 1) // n, lo + MIN_CUT, z - MIN_CUT, radius=90)
    return lo, max(hi, lo + MIN_CUT)


# ---------- 1. regiões: animação x stock ----------
regions = []  # (kind, from, to, beat_index, scene)
anim_cues = {}  # cena -> (1º cue, último cue) em quadros
anim_cue_abs = {}  # cena -> {cue: quadro absoluto} (vira "cues" LOCAL no item da timeline)
for bi, b in enumerate(beats):
    a, z = beat_span(b)
    if not b["anim"]:
        regions.append(["stock", a, z, bi, None]); continue
    ws = [w for w in words if a <= w["f"] < z]
    cue_frames = [h["f"] for h in seq_hits(CUES[b["anim"]], ws).values()]
    if cue_frames:
        # ancora a no máximo LEAD_IN antes do 1º cue, em início de palavra (mesmo no meio da frase):
        # folha de contexto mostrou A13 com 12 s de tela vazia quando a janela começava no início da frase
        first = min(cue_frames)
        target = max(a, first - LEAD_IN)
        start = max((w["f"] for w in words if a <= w["f"] <= target), default=a)
        last = max(cue_frames)
    else:
        start, last = a, a + MIN_ANIM
    if start - a < 2 * FPS:  # sobra curta antes da animação: começa no parágrafo
        start = a
    end_s = next((e for e in sent_ends if e >= last + 6), last + 30)   # 03/10: sai no fim da frase do último cue
    end = min(z, max(start + MIN_ANIM, min(end_s + 15, start + MAX_ANIM)))
    if cue_frames and end < last + 15:  # o número apareceria depois de dito: estica até meio segundo após o último cue
        end = min(z, max(end, min(last + 15, start + MAX_ANIM_HARD)))
    if z - end < 2 * FPS:  # sobra curta depois: a animação absorve (se couber no teto + 2 s)
        end = z if z - start <= MAX_ANIM + 2 * FPS else end
    if start > a:
        regions.append(["stock", a, start, bi, None])
    anim_cues[b["anim"]] = (min(cue_frames), max(cue_frames)) if cue_frames else (start, start + MIN_ANIM)
    # 25/09/2026: o quadro de cada cue vai para a cena (antes as cenas caíam na fração de fallback): chave = cada
    # alternativa do cue ("390|trezentos" -> "390", "trezentos" e o texto inteiro), valor = quadro ABSOLUTO
    anim_cue_abs[b["anim"]] = {k: h["f"] for spec, h in seq_hits(CUES[b["anim"]], ws).items()
                               for k in [spec] + spec.split("|")}
    regions.append(["anim", start, end, bi, b["anim"]])
    if end < z:
        regions.append(["stock", end, z, bi, None])

# respiro entre animações vizinhas: parágrafos seguidos com animação (p01/p02/p03 do filme do trem) deixavam
# A02+A03+A04 coladas, 90 s de gráfico sem imagem real. O respiro sai da folga de cada lado, NUNCA cortando o
# último cue da primeira nem passando do primeiro cue da segunda (1a versão comeu "yard" e "warships").
MIN_STOCK_BETWEEN = 5 * FPS
for i in range(len(regions) - 1):
    a, b = regions[i], regions[i + 1]
    if a[0] != "anim" or b[0] != "anim" or b[1] - a[2] >= MIN_STOCK_BETWEEN:
        continue
    need = MIN_STOCK_BETWEEN - (b[1] - a[2])
    piso_a = max(a[1] + MIN_ANIM, anim_cues.get(a[4], (0, 0))[1] + 15)   # fim mínimo: 0,5 s após o último cue
    corta = max(0, min(need, a[2] - piso_a))
    a[2] -= corta
    need -= corta
    if need > 0:
        teto_b = min(b[2] - MIN_ANIM, anim_cues.get(b[4], (10 ** 9, 0))[0] - 6)  # início máximo: antes do 1º cue
        b[1] += max(0, min(need, teto_b - b[1]))
    if b[1] > a[2]:
        regions.insert(i + 1, ["stock", a[2], b[1], a[3], None])

# funde stock contíguo (beats diferentes continuam marcados por corte)
merged = []
for r in regions:
    if merged and r[0] == "stock" and merged[-1][0] == "stock" and merged[-1][2] == r[1]:
        merged[-1][2] = r[2]
    else:
        merged.append(list(r))

# ---------- 2. cortes de stock ----------
def beat_at(f):
    for bi, b in enumerate(beats):
        a, z = beat_span(b)
        if a <= f < z:
            return bi
    return len(beats) - 1


items = []
for kind, a, z, bi, scene in merged:
    if kind == "anim":
        items.append({"type": "animation", "scene": scene, "from": a, "dur": z - a, "beat": beats[bi]["id"],
                      "modo": beats[bi].get("modo"), "lado": beats[bi].get("lado"),
                      "cues": {k: f - a for k, f in anim_cue_abs.get(scene, {}).items()}})
        continue
    if ULTRA:
        # fatia a região nas fronteiras de beat e aplica a curva de ritmo de cada beat
        fronteiras = sorted({a, z} | {f for b in beats for f in beat_span(b) if a < f < z})
        for ba, bz in zip(fronteiras, fronteiras[1:]):
            b = beats[beat_at((ba + bz) // 2)]
            alvo, minimo = RITMO.get(b.get("modo", "exposicao"), RITMO["exposicao"])
            if bz - ba < minimo:  # sobra curta: gruda no corte anterior
                if items and items[-1]["type"] == "cut" and items[-1]["from"] + items[-1]["dur"] == ba:
                    items[-1]["dur"] += bz - ba
                else:
                    items.append({"type": "cut", "from": ba, "dur": bz - ba, "beat": b["id"], "modo": b.get("modo"), "lado": b.get("lado")})
                continue
            n = max(1, round((bz - ba) / alvo))
            bounds = [ba]
            for k in range(1, n):
                x = ba + (bz - ba) * k // n
                bounds.append(snap(x, bounds[-1] + minimo, bz - minimo, radius=12 if b.get("modo") == "climax" else 20))
            bounds.append(bz)
            for s0, e0 in zip(bounds, bounds[1:]):
                if e0 > s0:
                    items.append({"type": "cut", "from": s0, "dur": e0 - s0, "beat": b["id"], "modo": b.get("modo"), "lado": b.get("lado")})
        continue
    n = max(1, round((z - a) / TARGET_CUT))
    bounds = [a]
    for k in range(1, n):
        x = a + (z - a) * k // n
        bounds.append(snap(x, bounds[-1] + MIN_CUT, z - MIN_CUT))
    bounds.append(z)
    for s, e in zip(bounds, bounds[1:]):
        if e > s:
            items.append({"type": "cut", "from": s, "dur": e - s, "beat": beats[beat_at((s + e) // 2)]["id"]})

for i, it in enumerate(items):
    it["id"] = (f"{it['scene']}" if it["type"] == "animation" else f"c{it['from']:06d}")

# ---------- 3. casamento ----------
clips = {c["id"]: c for c in lib if c["id"] not in wrej}
lib_by_id = {c["id"]: c for c in lib}
# retags da revisão (data/clip_retags.json {clip_id: [tags]}) — sobrevivem a make_clips, que regrava clips.json
for cid, tags in jload("clip_retags.json", {}).items():
    if cid in clips:
        clips[cid] = {**clips[cid], "tags": tags}
SOURCE_CAPS = jload("source_caps.json", {})  # {source: teto} — fontes honestas mas repetitivas
by_source = {}
for c in clips.values():
    by_source.setdefault(c.get("source"), []).append(c["id"])
uses = {}  # clip_id -> [from, ...]
beat_by_id = {b["id"]: b for b in beats}
beat_all_tags = set(jload("beats.json", None)["tags"])
pos_of = {it["id"]: i for i, it in enumerate(items)}  # vizinhança: evitar fila de cortes da MESMA fonte
NEAR_SRC = 3  # quantos itens antes/depois contam como "seguidos"
log = []


def near_sources(it):
    """Fontes já usadas nos itens vizinhos (folha qa/film1: 10 cortes seguidos do mesmo camarote de madeira)."""
    i = pos_of[it["id"]]
    out = []
    for j in range(max(0, i - NEAR_SRC), min(len(items), i + NEAR_SRC + 1)):
        if j == i:
            continue
        cid = items[j].get("clip")
        if cid and cid in lib_by_id:
            out.append(lib_by_id[cid].get("source"))
    return out


# tema agro: sem maquina concorrente; regra de objeto desligada (lista vazia)
MACHINES = []
DESC_CLASS = []
AMBIENT = {m: [] for m in MACHINES}
SCARCE_USES, SCARCE_GAP = 3, 25 * FPS  # máquina com pouco vídeo: o mesmo clipe da PRÓPRIA máquina volta até 3x no seu trecho


def classes_of(c):
    cls = {t for t in c.get("tags", []) if t in MACHINES}
    txt = f"{c.get('title') or ''} {c.get('source') or ''}"
    for rx, k in DESC_CLASS:
        if re.search(rx, txt, re.I):
            cls.add(k)
    return cls


def right_object(c, beat):
    m = beat["tags"][0]
    if m not in MACHINES:
        return True
    cls = classes_of(c)
    if cls:
        return cls <= {m} or (m == "potato_harvester" and cls <= {m, "beet"} and m in cls)
    return bool(set(c.get("tags", [])[:1]) & set(AMBIENT.get(m, [])))


# máquina escassa = menos de 30 clipes de vídeo da própria classe na biblioteca (contado na hora, depois de rejeições/retags)
_mcount = {m: sum(1 for c in clips.values() if c["kind"] == "video" and m in classes_of(c)) for m in MACHINES}
SCARCE_MACHINES = {m for m, n in _mcount.items() if n < 30}


def ok_clip(c, it, need):
    if c["dur"] < need:
        return False
    beat = beat_by_id[it["beat"]]
    if not right_object(c, beat):
        return False
    own = beat["tags"][0] in SCARCE_MACHINES and beat["tags"][0] in classes_of(c)
    if own:  # clipe da própria máquina ESCASSA: teto de repetição do trecho (as fartas seguem MAX_USES/REUSE_GAP)
        prev = uses.get(c["id"], [])
        if len(prev) >= SCARCE_USES or any(abs(it["from"] - f) < SCARCE_GAP for f in prev):
            return False
        if c["id"] in srej.get(it["id"], []):
            return False
        return not (beat["era"] == "modern" and c.get("era") == "old")
    if c["id"] in srej.get(it["id"], []):
        return False
    # corte rejeitado na folha: nenhuma janela irmã da MESMA fonte volta nesse ponto (revisão: carro vermelho/rua de Tromsø voltavam).
    # IRMA_LIVRE: só na última passada. No Mar Morto, 4 janelas rejeitadas num mesmo corte vinham de 4 fontes que juntas
    # tinham 105 dos 152 clipes de vídeo — a regra travava o corte inteiro. O clipe rejeitado continua fora; as irmãs voltam.
    if not IRMA_LIVRE and c.get("source") in {lib_by_id[r]["source"] for r in srej.get(it["id"], []) if r in lib_by_id}:
        return False
    prev = uses.get(c["id"], [])
    if len(prev) >= MAX_USES or any(abs(it["from"] - f) < REUSE_GAP for f in prev):
        return False
    if beat_by_id[it["beat"]]["era"] == "modern" and c.get("era") == "old":
        return False
    return True


def pick(it, tags, kinds, need, cap=None, ban_src=()):
    cap = SOURCE_CAP if cap is None else cap
    best, bs = None, None
    dbg = os.environ.get("DEBUG_PICK") == it.get("id")
    n = {"kind": 0, "okclip": 0, "ban": 0, "cap": 0, "rank": 0, "cand": 0}
    for c in clips.values():
        if c["kind"] not in kinds:
            n["kind"] += 1; continue
        if not ok_clip(c, it, need):
            n["okclip"] += 1; continue
        if c.get("source") in ban_src:
            n["ban"] += 1; continue
        src_cap = min(cap, SOURCE_CAPS.get(c.get("source"), cap))  # teto por fonte decidido na revisão
        if sum(len(uses.get(o, [])) for o in by_source.get(c.get("source"), [])) >= src_cap:
            n["cap"] += 1; continue
        rank = min((tags.index(t) for t in c["tags"] if t in tags), default=None)
        if rank is None:
            n["rank"] += 1; continue
        n["cand"] += 1
        # penalidade forte (não proibição: o plano não pode ficar com corte vazio) para fonte já usada ao lado
        score = rank * 10 + len(uses.get(c["id"], [])) * 4 + 60 * near_sources(it).count(c.get("source"))
        if bs is None or score < bs:
            best, bs = c, score
    if dbg:
        print(f"[pick] {it['id']} tags={tags} kinds={kinds} need={need} cap={cap} -> {n} best={best and best['id']}",
              flush=True)
    return best


for i, it in enumerate(items):
    it["tail"] = FADE_ANIM if i + 1 < len(items) and items[i + 1]["type"] == "animation" else 0
    it["fadeIn"] = FADE_ANIM if i > 0 and (it["type"] == "animation" or items[i - 1]["type"] == "animation") else 0

need_of = lambda it: it["dur"] + it["tail"]


def assign(i, c, how):
    it = items[i]
    b = beat_by_id[it["beat"]]
    k = len(uses.get(c["id"], []))
    uses.setdefault(c["id"], []).append(it["from"])
    trim = 0 if k == 0 else max(0, c["dur"] - need_of(it))
    it.update(kind=c["kind"], src=c["file"], clip=c["id"], trimBefore=trim if c["kind"] == "video" else None,
              move=["in", "left", "out", "right"][it["from"] % 4] if c["kind"] == "photo" else None, how=how)
    if how not in ("tag", "lock"):
        log.append(f"{how}: {it['id']} {it['beat']} {b['tags'][0]} -> {c['id']} {c['tags']}")


cut_idx = [i for i, it in enumerate(items) if it["type"] == "cut"]
pending = lambda: [i for i in cut_idx if not items[i].get("clip")]

# passada 0: travas aprovadas na folha
for i in cut_idx:
    c = clips.get(locks.get(items[i]["id"], ""))
    if c is not None and ok_clip(c, items[i], need_of(items[i])):
        assign(i, c, "lock")

# assunto que SÓ existe em foto de época (o SS France/Norway, 19/09): fotos seguidas valem mais que petroleiro
# moderno de ambientação sob o slate "SS FRANCE". Nesses beats duas fotos podem ficar vizinhas.
PHOTO_RUN_TAGS = {"icapui", "redonda", "falesia", "praia", "jangada", "barco_pesca", "pescador", "vila", "lagosta", "lagosta_pescada", "manzua", "mergulho", "mangueira", "compressor", "botijao", "motor", "fundo", "marambaia", "sucata", "bolhas", "camara", "hospital", "cadeira", "medula", "mar", "amanhecer", "fortaleza", "natal", "rn_costa", "ibama", "policia", "marinha", "guerra", "aviao", "lancha", "fogo", "multidao", "defeso", "restaurante", "fabrica", "porto", "dinheiro", "turismo", "roca", "familia", "eua", "documento"}
# 04/10/2026: tag com MENOS DE 2 VÍDEOS na biblioteca vira PHOTO_RUN sozinha (o porta-aviões precisou de 6 voltas do
# fechar.py preparar acrescentando tag por tag à mão). O qa.py lê o conjunto final em data/photo_run.json.
_vids = {}
for _c in lib:
    if _c.get("kind") == "video" and _c["id"] not in wrej:
        for _t in _c.get("tags", []):
            _vids[_t] = _vids.get(_t, 0) + 1
PHOTO_RUN_AUTO = {b["tags"][0] for b in beats if _vids.get(b["tags"][0], 0) < 2}
PHOTO_RUN_TAGS = set(PHOTO_RUN_TAGS) | PHOTO_RUN_AUTO
(D / "photo_run.json").write_text(json.dumps(sorted(PHOTO_RUN_TAGS), ensure_ascii=False), "utf-8")
# fatia de VÍDEO: com 70 % de foto o vídeo fica em 3 de cada 10 cortes (o resto tenta foto primeiro)
SO_FOTO_BEATS = set()   # 05/11 dresser: nenhum trecho só de foto
VIDEO_SLOTS = set() if SO_FOTO else (({0} if PHOTO_SHARE >= 0.85 else {0, 5}) if PHOTO_SHARE >= 0.75 else {0, 3, 7}) if PHOTO_SHARE >= 0.65 else {1, 3, 5, 7, 9}


def tags_do_beat(it):
    """Ordem de busca do corte: as tags do próprio beat, depois ambientação de dentro (se for beat fechado),
    depois a ambientação geral do filme e a regional."""
    b = beat_by_id[it["beat"]]
    t0 = b["tags"][0]
    fb = (INTERIOR_FALLBACK if t0 in INTERIOR_TAGS else []) + FALLBACK_TAGS + REGIONAL
    _sec = globals().get("SECAO_FB")   # 27/10 (ev): reserva por trecho; só vale se as tags existem neste filme
    if _sec and all(t in beat_all_tags for v in _sec.values() for t in v):
        fb = next(v for (a, z), v in _sec.items() if a <= b["para"] <= z)
    return list(b["tags"]) + [t for t in fb if t not in b["tags"]]


def corre_foto(i):
    """Quantas fotos seguidas ficariam se o corte i virasse foto (conta para os dois lados)."""
    def lado(d):
        n, j = 0, i + d
        while 0 <= j < len(items) and items[j].get("kind") == "photo":
            n += 1
            j += d
        return n
    return lado(-1) + lado(1) + 1


def foto_pode(i):
    it = items[i]
    if it["from"] < HOOK or it["dur"] > PHOTO_MAX:   # gancho é só vídeo; foto não segura corte longo
        return False
    if beat_by_id[it["beat"]]["tags"][0] in PHOTO_RUN_TAGS:
        return True
    return corre_foto(i) <= MAXRUN_PHOTO


def tenta(i, kinds, tags=None, cap=None, need=None):
    it = items[i]
    c = pick(it, tags or tags_do_beat(it), kinds, need or need_of(it), cap)
    if c is None:
        return False
    assign(i, c, "tag" if tags is None else "fallback")
    return True


# passada 1: o slot manda o tipo — vídeo nos slots de vídeo, foto no resto (quando a foto couber)
for k, i in enumerate(cut_idx):
    if items[i].get("clip"):
        continue
    quer_video = (k % 10) in VIDEO_SLOTS or not foto_pode(i)
    if items[i]["beat"] in SO_FOTO_BEATS:
        quer_video = False
    tenta(i, {"video"} if quer_video else {"photo"})

# passada 2: quem não achou do tipo pedido tenta o outro tipo, ainda dentro das tags do beat
for i in pending():
    quer = {"photo"} if foto_pode(i) else {"video"}
    tenta(i, quer)

# passada 3: qualquer tipo, tags do beat + ambientação
for i in pending():
    kinds = {"video", "photo"} if foto_pode(i) else {"video"}
    tenta(i, kinds)

# passada 4: afrouxa o teto por fonte (um rolo bom vale mais que corte vazio)
for i in pending():
    kinds = {"video", "photo"} if foto_pode(i) else {"video"}
    tenta(i, kinds, cap=SOURCE_CAP_LAST)

# passada 5: última chance — aceita foto mesmo quebrando a fila (o qa.py acusa e a revisão decide)
for i in pending():
    tenta(i, {"video", "photo"}, cap=DECLUMP_CAP)

# passada 6: desfaz fila da MESMA fonte em cortes vizinhos (10 cortes seguidos do mesmo rolo)
for k, i in enumerate(cut_idx):
    it = items[i]
    c0 = clips.get(it.get("clip") or "")
    if c0 is None:
        continue
    if near_sources(it).count(c0.get("source")) < 2:
        continue
    uses[c0["id"]].remove(it["from"])
    it.pop("clip", None)
    if not tenta(i, {c0["kind"]}, cap=DECLUMP_CAP):
        uses.setdefault(c0["id"], []).append(it["from"])
        assign(i, c0, "declump-mantido")

# ---------- 4. gravação ----------
for it in items:   # 05/10/2026: corta o que passa do fim do áudio (arredondamento deixava 1 quadro a mais no último corte)
    if it["from"] + it["dur"] > DUR:
        it["dur"] = max(1, DUR - it["from"])
plano = {"fps": FPS, "durationInFrames": DUR, "items": items}
(D / "plan_antes.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), "utf-8")
(D / "timeline.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), "utf-8")

cortes = [items[i] for i in cut_idx]
n_v = sum(1 for c in cortes if c.get("kind") == "video")
n_f = sum(1 for c in cortes if c.get("kind") == "photo")
vazios = [c["id"] for c in cortes if not c.get("clip")]
distintos = len({c["clip"] for c in cortes if c.get("clip")})
abaixo = sum(1 for l in log if l.startswith("fallback"))
rel = ["# build_plan", "",
       f"- itens {len(items)} | animações {sum(1 for i in items if i['type'] == 'animation')} | "
       f"cortes {len(cortes)} | vídeo {n_v} | foto {n_f} | vídeo% {100 * n_v / max(1, len(cortes)):.1f}",
       f"- clipes distintos usados {distintos} de {len(clips)}",
       f"- ERROS {len(vazios)}"] + [f"  - corte sem clipe {c}" for c in vazios[:10]] + ["", "## degraus abaixo da tag", ""] + log
(D / "build_plan_report.md").write_text("\n".join(rel) + "\n", "utf-8")
print("\n".join(rel[:6]))
print(f"(degraus abaixo da tag: {abaixo})")
