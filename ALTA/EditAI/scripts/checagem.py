"""CHECAGEM AUTOMÁTICA antes do render — o PORTEIRO (05/10/2026, pedido do usuário).

Até aqui quem evitava defeito era a instrução que o Diretor (ou eu) seguia, e em 05/10 passaram 19 clipes corrompidos,
o logo da AngloGold, a marca d'água "SHOT ON VSMART" e açougue da França num filme do Brasil. Agora o programa
BLOQUEIA o render (fechar.py render chama isto e para) quando encontra, na timeline do filme:
  1. CORROMPIDO  — clipe de vídeo que não decodifica inteiro (ffmpeg -v error ... -f null -);
  2. APRESENTADOR/TEXTO no vídeo — o mesmo detector do video_suspeitos.py (CLIP local), agora com trava;
  3. MARCA D'ÁGUA / LEGENDA — OCR do próprio Windows (scripts/ocr_windows.ps1, sem instalar nada) na foto inteira, nos
     4 cantos ampliados e em 3 quadros de cada vídeo: marca d'água conhecida ("shot on", ©, www, Getty, Shutterstock,
     marca de celular...) ou faixa de legenda larga em cima/embaixo. (O CLIP NÃO serve: marca d'água no canto dá a
     mesma nota da foto limpa — medido em 05/10.) Texto natural da cena (placa, letreiro, chip) NÃO conta;
  4. PAÍS ERRADO — foto que veio do banco marcada com país diferente do PAIS do beats.py.
Alarme falso: depois de OLHAR qa/checagem.jpg, ponha o id em data/checagem_aceitos.json
  {"v1234abcd": "é a cientista da história, fica", "p55aa66bb": "placa da própria fábrica"}
e rode de novo. Rejeitar de verdade = window_rejects.json (vídeo) / photo_side.json reject + make_photos (foto).

Saída: data/checagem.json (ok, hash da timeline, falhas) e qa/checagem.jpg (só os problemas, com segundo e motivo).
Uso: python scripts/checagem.py            (sai com 1 se houver problema não aceito)
     python scripts/checagem.py --data DIR --public DIR   (teste com material de outro lugar)
"""
import hashlib, json, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
arg = lambda k, d: Path(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
D = arg("--data", ROOT / "data")
PUB = arg("--public", ROOT / "public")
QA = arg("--qa", ROOT / "qa")
FPS = 30
OCR_PS1 = Path(__file__).resolve().parent / "ocr_windows.ps1"
MARCA = re.compile(r"shot\s*on|©|\(c\)\s*\d|copyright|www\.|\.com\b|getty|shutterstock|alamy|istock|dreamstime|depositphotos|"
                   r"123rf|adobe\s*stock|photo\s*by|foto\s*:|triple\s*camera|ai\s*camera|xiaomi|redmi|vsmart|huawei|oppo|realme|"
                   r"poco\s*f|galaxy\s*s\d|pixabay|pexels|unsplash|subscribe|inscreva|suscr[ií]bete", re.I)
LIM_FALA = 0.012          # o mesmo do video_suspeitos.py


def jl(p, d):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def hash_timeline():
    return hashlib.md5((D / "timeline.json").read_bytes()).hexdigest()


REGRA = "2026-10-07a"   # mudar quando julga_ocr/decodificação mudarem: o cache antigo deixa de valer


def chave(lib, cid):
    f = PUB / lib[cid].get("file", "")
    try:
        st = f.stat()
        return f"{lib[cid].get('file')}|{st.st_size}|{int(st.st_mtime)}|{REGRA}"
    except OSError:
        return None


def decodifica(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(arq), "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    erro = (r.stderr or "").strip()
    return erro.splitlines()[0][:120] if erro else ""


def main():
    tl = jl(D / "timeline.json", {}).get("items", [])
    lib = {c["id"]: c for c in jl(D / "clips.json", {}).get("clips", [])}
    aceitos = jl(D / "checagem_aceitos.json", {})
    pais = jl(D / "beats.json", {}).get("pais")
    side = jl(D / "photo_side.json", {})
    banco = jl(ROOT.parent.parent / "banco" / "banco.json", {}) if ROOT.parent.name == "baias" else jl(ROOT.parent / "banco" / "banco.json", {})
    usos = {}
    for it in tl:
        if it.get("type") == "cut" and it.get("clip") in lib:
            usos.setdefault(it["clip"], it["from"] / FPS)
    falhas = []
    tmp = Path(tempfile.mkdtemp())
    cache = jl(D / "checagem_cache.json", {})   # 07/10/2026: só confere de novo o que entrou/mudou
    novos = {"dec": 0, "ocr": 0}

    # 1) vídeo corrompido
    videos = [c for c in usos if lib[c].get("kind") == "video"]

    def v_ok(cid):
        f = PUB / lib[cid]["file"]
        if not f.exists():
            return cid, "arquivo não existe"
        k = chave(lib, cid)
        if k and "dec" in cache.get(k, {}):
            return cid, cache[k]["dec"]
        erro = decodifica(f)
        if k:
            cache.setdefault(k, {})["dec"] = erro
            novos["dec"] += 1
        return cid, erro
    with ThreadPoolExecutor(4) as ex:
        for cid, erro in ex.map(v_ok, videos):
            if erro:
                falhas.append({"tipo": "corrompido", "id": cid, "t": round(usos[cid]), "motivo": f"vídeo corrompido: {erro}"})
    ruins = {f["id"] for f in falhas}

    # 2) apresentador/texto no vídeo (data/video_suspeitos.json — o fechar.py preparar acabou de gerar)
    for s in jl(D / "video_suspeitos.json", []):
        if s["clip"] in usos and s["clip"] not in ruins:
            motivo = ("apresentador falando para a câmera" if s.get("fala", 0) > LIM_FALA else "") + \
                     (" + " if s.get("fala", 0) > LIM_FALA and s.get("texto") else "") + ("texto na tela" if s.get("texto") else "")
            falhas.append({"tipo": "video_suspeito", "id": s["clip"], "t": s["t"], "motivo": motivo or "suspeito",
                           "quadro": s.get("quadro")})

    # 3) e 4) fotos e quadros de vídeo: OCR (marca d'água / legenda) + país do banco
    fotos = [c for c in usos if lib[c].get("kind") == "photo"]
    por_titulo = {t: v for t, v in side.items() if v.get("verdict") == "ok"}
    for cid in fotos:
        v = por_titulo.get(lib[cid].get("title") or "", {})
        if pais and v.get("banco"):
            p_item = banco.get(v["banco"], {}).get("pais")
            if p_item and p_item != pais:
                falhas.append({"tipo": "pais", "id": cid, "t": round(usos[cid]), "motivo": f"foto do banco de outro país ({p_item}, o filme é {pais})"})
    todos = fotos + [c for c in videos if c not in ruins]
    pend = [c for c in todos if not (chave(lib, c) and "ocr" in cache.get(chave(lib, c), {}))]
    alvos = prepara_ocr([c for c in pend if c in fotos], [c for c in pend if c not in fotos], lib, tmp)
    lidos = ocr([a["arq"] for a in alvos])
    achado, quadro = {}, {}
    for a in alvos:
        r = lidos.get(a["arq"])
        if not r or a["id"] in achado:
            continue
        motivo = julga_ocr(r, a)
        if motivo:
            achado[a["id"]], quadro[a["id"]] = motivo, a.get("quadro")
    lidos_ok = {a["id"] for a in alvos if lidos.get(a["arq"])}
    for c in pend:   # só grava no cache o que o OCR leu de fato (falha do PowerShell = confere de novo da próxima vez)
        k = chave(lib, c)
        if k and c in lidos_ok:
            cache.setdefault(k, {})["ocr"] = achado.get(c, "")
            novos["ocr"] += 1
    for c in todos:
        k = chave(lib, c)
        motivo = achado.get(c) or (cache.get(k, {}).get("ocr") if k else "")
        if motivo:
            falhas.append({"tipo": "texto", "id": c, "t": round(usos[c]), "motivo": motivo, "quadro": quadro.get(c)})
    (D / "checagem_cache.json").write_text(json.dumps(cache, ensure_ascii=False), "utf-8")

    abertas = [f for f in falhas if f["id"] not in aceitos]
    falhas.sort(key=lambda f: f["t"])
    res = {"ok": not abertas, "timeline": hash_timeline() if (D / "timeline.json").exists() else "",
           "falhas": falhas, "abertas": len(abertas), "videos": len(videos), "fotos": len(fotos)}
    (D / "checagem.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), "utf-8")
    folha(abertas, lib, tmp)
    print(f"[checagem] {len(videos)} vídeos e {len(fotos)} fotos conferidos ({novos['dec']} decodificados e "
          f"{novos['ocr']} lidos agora, o resto do cache): {len(abertas)} problema(s)"
          + (f", {len(falhas) - len(abertas)} aceito(s)" if len(falhas) != len(abertas) else ""))
    for f in abertas:
        print(f"   {f['t'] // 60:02d}:{f['t'] % 60:02d}  {f['id']}  {f['motivo']}")
    if abertas:
        print("   -> olhe qa/checagem.jpg; defeito = rejeitar; alarme falso = data/checagem_aceitos.json {id: motivo}")
        sys.exit(1)


def prepara_ocr(fotos, videos, lib, tmp):
    """Foto: imagem inteira (1280 px) + 4 cantos ampliados 2x (marca d'água pequena só aparece assim).
    Vídeo: 3 quadros (25/50/75 %) inteiros."""
    from PIL import Image
    alvos = []
    for cid in fotos:
        f = PUB / lib[cid]["file"]
        if not f.exists():
            continue
        try:
            im = Image.open(f).convert("RGB")
        except Exception:  # noqa: BLE001
            continue
        W, H = im.size
        cheia = tmp / f"{cid}_full.jpg"
        im.resize((1280, max(1, round(H * 1280 / W)))).save(cheia, quality=90)
        alvos.append({"id": cid, "arq": str(cheia), "parte": "inteira", "video": False, "quadro": str(f)})
        for k, b in {"inf. esq.": (0, int(H * .8), int(W * .45), H), "inf. dir.": (int(W * .55), int(H * .8), W, H),
                     "sup. esq.": (0, 0, int(W * .45), int(H * .18)), "sup. dir.": (int(W * .55), 0, W, int(H * .18))}.items():
            c = im.crop(b)
            c = c.resize((c.width * 2, c.height * 2))
            arq = tmp / f"{cid}_{len(alvos)}.png"
            c.save(arq)
            alvos.append({"id": cid, "arq": str(arq), "parte": "canto " + k, "video": False, "quadro": str(f)})
    for cid in videos:
        f = PUB / lib[cid]["file"]
        dur = lib[cid].get("dur", 150) / FPS
        for k, frac in enumerate((0.1, 0.3, 0.5, 0.7, 0.9)):   # 07/10: eram 3 — texto que aparece só no fim passava
            arq = tmp / f"{cid}_q{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-ss", f"{dur * frac:.2f}", "-i", str(f), "-frames:v", "1",
                            "-vf", "scale=1280:-2", str(arq)], check=False)
            if arq.exists():
                alvos.append({"id": cid, "arq": str(arq), "parte": "quadro", "video": True, "quadro": str(arq)})
    return alvos


def ocr(arqs):
    """OCR do Windows em 3 processos em paralelo (≈0,1 s por imagem)."""
    if not arqs or not OCR_PS1.exists():
        return {}
    pedacos = [arqs[i::3] for i in range(3)]
    tmp = Path(tempfile.mkdtemp())

    def roda(i):
        lista = tmp / f"lista_{i}.txt"
        lista.write_text("\n".join(str(Path(a)) for a in pedacos[i]), "utf-8")
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(OCR_PS1), str(lista)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = {}
        for linha in r.stdout.splitlines():
            linha = linha.strip().lstrip("\ufeff")
            if linha.startswith("{"):
                try:
                    e = json.loads(linha)
                    out[str(Path(e["p"]))] = e
                except Exception:  # noqa: BLE001
                    pass
        return out
    res = {}
    with ThreadPoolExecutor(3) as ex:
        for o in ex.map(roda, range(3)):
            res.update(o)
    return {a: res.get(str(Path(a))) for a in arqs}


def julga_ocr(r, a):
    """Marca d'água conhecida em qualquer parte; legenda = faixa larga em cima/embaixo (só na imagem inteira)."""
    W, H = r.get("w") or 1, r.get("h") or 1
    for txt, x, y, w, h in r.get("l") or []:
        if MARCA.search(txt):
            return f"marca d'água/texto de outro canal ({a['parte']}): “{txt[:40]}”"
    if a["parte"] in ("inteira", "quadro"):
        for txt, x, y, w, h in r.get("l") or []:
            letras = sum(ch.isalpha() for ch in txt)
            larga = w / W >= (0.30 if a["video"] else 0.40)
            faixa = y > 0.70 * H or (y + h) < 0.25 * H
            vogais = sum(ch.lower() in "aeiouáéíóúãõâêô" for ch in txt)
            if letras >= 12 and larga and faixa and vogais >= 3 and len(set(txt.lower())) >= 6:
                return f"legenda/título na tela: “{txt[:40]}”"
    # 07/10/2026: BLOCO de texto explicativo do vídeo original (3+ linhas de frase no canto/lado — "Other parts, the DOOR
    # ... are attached ... using ELECTRIC WRENCH" na fábrica da Hilux passou porque não era faixa larga). Só em vídeo:
    # foto de documento/cartaz é material legítimo dos filmes de arquivo.
    if a["parte"] == "quadro":
        frases = [txt for txt, x, y, w, h in r.get("l") or []
                  if sum(ch.isalpha() for ch in txt) >= 5 and sum(ch.lower() in "aeiouáéíóúãõâêô" for ch in txt) >= 2]
        if len(frases) >= 3 and sum(sum(ch.isalpha() for ch in s) for s in frases) >= 30:
            return f"bloco de texto na tela: “{' / '.join(frases)[:60]}”"
    return ""


def folha(abertas, lib, tmp):
    alvo = QA / "checagem.jpg"
    alvo.unlink(missing_ok=True)
    if not abertas:
        return
    from PIL import Image, ImageDraw
    W, H, C = 320, 180, 6
    linhas = (len(abertas) + C - 1) // C
    sh = Image.new("RGB", (W * C, (H + 34) * linhas), (16, 16, 16))
    d = ImageDraw.Draw(sh)
    for j, f in enumerate(abertas):
        x, y = (j % C) * W, (j // C) * (H + 34)
        img = None
        src = PUB / lib.get(f["id"], {}).get("file", "")
        try:
            if f.get("quadro") and Path(f["quadro"]).exists():
                img = Image.open(f["quadro"])
            elif src.suffix.lower() == ".mp4" and src.exists():
                p = tmp / f"{f['id']}.jpg"
                subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-ss", "2", "-i", str(src), "-frames:v", "1", str(p)])
                img = Image.open(p) if p.exists() else None
            elif src.exists():
                img = Image.open(src)
        except Exception:  # noqa: BLE001
            img = None
        if img:
            sh.paste(img.convert("RGB").resize((W, H)), (x, y + 34))
        else:
            d.text((x + 10, y + 100), "ERRO — não abre", fill=(255, 80, 80))
        d.text((x + 4, y + 2), f"{f['id']} @{f['t'] // 60:02d}:{f['t'] % 60:02d}", fill=(255, 210, 0))
        d.text((x + 4, y + 17), f["motivo"][:52], fill=(230, 230, 230))
    QA.mkdir(exist_ok=True)
    sh.save(alvo, quality=85)


if __name__ == "__main__":
    main()
