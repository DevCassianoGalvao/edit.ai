"""IMAGENS DE CENA GERADAS POR IA (Nano Banana 2 Lite, via fal.ai) — só para canais com "ia_imagens" no painel/canais.json
(02/11/2026, pedido do usuário: seu canal e seu canal). O filme segue o fluxo normal (80 % foto / 20 % vídeo);
além disso, até 10 cortes de foto, espalhados pelo filme, viram uma cena gerada com o PERSONAGEM FIXO do canal
(imagem de referência em painel/personagens/). Zoom lento = o "move" que o build_plan já põe em toda foto.

  python scripts/ia_cenas.py plano --canal seu canal [--n 10]
      escolhe até N parágrafos espalhados (8 % a 94 % do filme, sem animação) -> data/ia_cenas_plano.json
      (cada cena traz o texto da narração e "prompt": ""). O DIRETOR escreve o "prompt" de cada cena (em inglês:
      o que a narração mostra naquele ponto, com o personagem fazendo algo coerente com o assunto) e salva o JSON.
  python scripts/ia_cenas.py gerar [--so N]
      gera as imagens (fal.ai, endpoint /edit com a referência do personagem) -> public/stock/ia_NN.jpg (1920x1080)
      + data/clips.json (kind photo, tag ia_cena). Pula as que já existem. Custo ~US$ 0,05 por imagem.
  python scripts/ia_cenas.py aplicar     (o fechar.py preparar chama sozinho depois do build_plan)
      troca no timeline.json o melhor corte (foto, o mais longo) de cada parágrafo pela imagem de IA, com zoom lento.
  python scripts/ia_cenas.py verificar   confere no timeline.json se todas as imagens foram usadas.
A chave da fal fica em <ALTA>/chaves/fal.txt (nunca imprimir).
"""
import base64, io, json, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
STOCK = ROOT / "public" / "stock"
PLANO = D / "ia_cenas_plano.json"
# a baia (b2, b3) só recebe scripts/ e src/: o painel (canais.json, personagens) e as chaves ficam na pasta principal
ALTA = next((p for p in ROOT.parents if (p / "chaves").is_dir()), ROOT.parent)
PAINEL = next((p for p in (ALTA / "EditAI" / "painel", ROOT / "painel") if (p / "canais.json").exists()), ROOT / "painel")
CANAIS = PAINEL / "canais.json"
CHAVE = ALTA / "chaves" / "fal.txt"
ENDPOINT = "https://fal.run/google/nano-banana-lite/edit"
MAX_PADRAO = 10
FPS = 30


def jload(p, default=None):
    p = Path(p)
    return json.loads(p.read_text("utf-8")) if p.exists() else default


def jsave(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), "utf-8")


def canal_cfg(canal_id):
    for c in jload(CANAIS)["canais"]:
        if c["id"] == canal_id:
            if not c.get("ia_imagens"):
                sys.exit(f"[ia] o canal {canal_id} não tem 'ia_imagens' no canais.json — esta regra é só dos canais que a têm")
            return c
    sys.exit(f"[ia] canal {canal_id} não existe no painel/canais.json")


def arg(nome, padrao=None):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else padrao


def plano():
    cfg = canal_cfg(arg("--canal") or sys.exit("[ia] use --canal <id>"))
    ia = cfg["ia_imagens"]
    n = min(int(arg("--n", ia.get("max", MAX_PADRAO))), int(ia.get("max", MAX_PADRAO)))
    beats = jload(D / "beats.json")["beats"]
    tr = jload(D / "master_transcript.json")
    paras = {p["id"]: p for p in tr["paragraphs"]}
    dur = tr["durationInFrames"]
    # parágrafos sem animação (mapa/cartão ocupam o corte), entre 8 % e 94 % do filme
    cand = []
    for b in beats:
        p = paras.get("p%02d" % b["para"]) or tr["paragraphs"][min(b["para"], len(tr["paragraphs"]) - 1)]
        pos = p["startFrame"] / dur
        texto = re.sub(r"<[^>]+>", " ", p["text"]).strip()   # tira <break time=...> da voz
        if b.get("anim") or not (0.08 <= pos <= 0.94) or len(texto) < 80:
            continue
        cand.append({"beat": b["id"], "para": b["para"], "pos": round(pos, 3), "inicio_s": round(p["startFrame"] / FPS, 1),
                     "texto": texto, "mustShow": b.get("mustShow"), "tags": b.get("tags")})
    if not cand:
        sys.exit("[ia] nenhum parágrafo candidato (beats.json/master_transcript.json vazios?)")
    n = min(n, len(cand))
    alvo = [0.08 + (0.94 - 0.08) * (i + 0.5) / n for i in range(n)]
    esc, usados = [], set()
    for a in alvo:
        c = min((c for c in cand if c["beat"] not in usados), key=lambda c: abs(c["pos"] - a))
        usados.add(c["beat"])
        esc.append(c)
    esc.sort(key=lambda c: c["pos"])
    cenas = [dict(n=i + 1, prompt="", **c) for i, c in enumerate(esc)]
    jsave(PLANO, {"canal": cfg["id"], "personagem": ia["personagem"], "descricao": ia["descricao"], "max": ia.get("max", MAX_PADRAO),
                  "cenas": cenas})
    print(f"[ia] plano com {len(cenas)} cenas -> {PLANO}")
    for c in cenas:
        print(f"  #{c['n']} {c['beat']} {c['inicio_s']:>6} s  {c['texto'][:90]}")
    print("[ia] AGORA: escrever o \"prompt\" (inglês) de cada cena no JSON e rodar:  python scripts/ia_cenas.py gerar")


def _chave():
    if not CHAVE.exists() or not CHAVE.read_text("utf-8").strip():
        print("[fal.ai] sem chave configurada — etapa opcional ignorada")
        sys.exit(0)
    return CHAVE.read_text("utf-8").strip()


def _ref_uri(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((1024, 1024))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _cover_1080(im):
    from PIL import Image
    W, H = 1920, 1080
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def gerar():
    from PIL import Image
    pl = jload(PLANO) or sys.exit("[ia] rode antes: ia_cenas.py plano --canal <id>")
    if len(pl["cenas"]) > pl.get("max", MAX_PADRAO):
        sys.exit(f"[ia] mais de {pl.get('max', MAX_PADRAO)} cenas — a regra do canal é no máximo {pl.get('max', MAX_PADRAO)}")
    so = arg("--so")
    pers = PAINEL / pl["personagem"]
    ref = _ref_uri(pers)
    key = _chave()
    STOCK.mkdir(parents=True, exist_ok=True)
    clips_p = D / "clips.json"
    disk = {c["id"]: c for c in (jload(clips_p, {"clips": []})["clips"])}
    gastas = 0
    for c in pl["cenas"]:
        if so and str(c["n"]) != so:
            continue
        cid = "ia_%02d" % c["n"]
        dst = STOCK / f"{cid}.jpg"
        if dst.exists() and cid in disk:
            print(f"[ia] #{c['n']} já existe"); continue
        if not c.get("prompt", "").strip():
            print(f"[ia] #{c['n']} SEM prompt — escreva em data/ia_cenas_plano.json"); continue
        texto = (c["prompt"].strip().rstrip(".") + ". The man in the picture is exactly the same person as in the reference image "
                 "(same face, hair, beard, eye color and age), wearing " + pl["descricao"].split("wearing ")[-1] + ". "
                 "Photorealistic documentary photograph, natural light, 16:9 landscape, no text, no captions, no logos, no watermark.")
        req = urllib.request.Request(ENDPOINT, data=json.dumps({"prompt": texto, "image_urls": [ref], "aspect_ratio": "16:9",
                                                               "num_images": 1}).encode(),
                                     headers={"Authorization": "Key " + key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=240))
            img = Image.open(io.BytesIO(urllib.request.urlopen(r["images"][0]["url"], timeout=120).read())).convert("RGB")
        except urllib.error.HTTPError as e:
            print(f"[ia] #{c['n']} HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}"); continue
        except Exception as e:   # rede, JSON, imagem corrompida
            print(f"[ia] #{c['n']} falhou: {e}"); continue
        _cover_1080(img).save(dst, quality=92)
        disk[cid] = {"id": cid, "kind": "photo", "file": f"stock/{cid}.jpg", "dur": 10 ** 6, "tags": ["ia_cena"],
                     "source": "ia:nano-banana-2-lite", "era": "modern", "title": f"IA cena {c['n']} ({c['beat']})", "url": "https://fal.ai",
                     "license": "AI generated (Nano Banana 2 Lite)", "artist": None,
                     "credit": "Imagem gerada por IA (Nano Banana 2 Lite)", "prompt": c["prompt"]}
        gastas += 1
        print(f"[ia] #{c['n']} ok -> {dst.name}", flush=True)
        jsave(clips_p, {"clips": list(disk.values())})
    log = jload(D / "ia_cenas_log.json", {"geradas": 0})
    log["geradas"] += gastas
    jsave(D / "ia_cenas_log.json", log)
    print(f"[ia] {gastas} imagem(ns) gerada(s) agora (~US$ {gastas * 0.05:.2f}); total no filme: {log['geradas']}")


def _cortes_da_cena(items, beat):
    cuts = [it for it in items if it.get("type") == "cut" and it.get("beat") == beat]
    # prefere corte que JÁ é foto (não derruba vídeo) e mais longo; senão, o mais longo do parágrafo
    fotos = [c for c in cuts if c.get("kind") == "photo"]
    pool = fotos or cuts
    return sorted(pool, key=lambda c: -c["dur"])


def aplicar():
    """Troca, no timeline.json (logo depois do build_plan), o melhor corte de cada parágrafo pela imagem de IA.
    Idempotente: o build_plan regera o timeline a cada rodada e o fechar.py chama isto de novo."""
    pl = jload(PLANO)
    if not pl:
        print("[ia] sem plano — nada a aplicar"); return
    tp = D / "timeline.json"
    tl = jload(tp, {"items": []})
    items = tl["items"]
    clips = {c["id"] for c in jload(D / "clips.json", {"clips": []})["clips"]}
    ocupados = {it.get("clip") for it in items if it.get("type") == "cut"}
    novos = 0
    for c in pl["cenas"]:
        cid = "ia_%02d" % c["n"]
        if cid not in clips or cid in ocupados:
            continue
        cortes = _cortes_da_cena(items, c["beat"])
        cortes = [x for x in cortes if not str(x.get("clip", "")).startswith("ia_")]
        if not cortes:   # beat sem corte (cartão/animação ocupou): usa o corte de foto mais próximo da fala
            f0 = int(c.get("inicio_s", 0) * FPS)
            cortes = sorted((x for x in items if x.get("type") == "cut" and not str(x.get("clip", "")).startswith("ia_")
                             and f0 - 300 <= x["from"] <= f0 + 900),
                            key=lambda x: (x.get("kind") != "photo", abs(x["from"] - f0)))
        if not cortes:
            print(f"[ia] #{c['n']} sem corte livre no beat {c['beat']}"); continue
        it = cortes[0]
        it.update(kind="photo", src=f"stock/{cid}.jpg", clip=cid, trimBefore=None,
                  move=["in", "left", "out", "right"][it["from"] % 4], how="ia")
        ocupados.add(cid)
        novos += 1
    if novos:
        jsave(tp, tl)
    print(f"[ia] cenas aplicadas: {novos}")


def verificar():
    pl = jload(PLANO)
    if not pl:
        print("[ia] sem plano"); return
    clips = {c["id"] for c in jload(D / "clips.json", {"clips": []})["clips"]}
    tl = jload(D / "timeline.json", {"items": []})["items"]
    usadas = {it.get("clip") for it in tl if it.get("type") == "cut"}
    esperadas = ["ia_%02d" % c["n"] for c in pl["cenas"] if "ia_%02d" % c["n"] in clips]
    faltam = [e for e in esperadas if e not in usadas]
    print(f"[ia] {len(esperadas) - len(faltam)}/{len(esperadas)} imagens de IA no filme" + (f" — FALTAM: {', '.join(faltam)}" if faltam else ""))
    if len(esperadas) < len(pl["cenas"]):
        print(f"[ia] AVISO: {len(pl['cenas']) - len(esperadas)} cena(s) sem imagem gerada (rode: ia_cenas.py gerar)")
    if faltam:
        sys.exit(1)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    {"plano": plano, "gerar": gerar, "aplicar": aplicar, "verificar": verificar}.get(modo, lambda: print(__doc__))()
