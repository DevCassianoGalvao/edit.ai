"""PACOTES POR NICHO — 04/10/2026 (meta: filme em 50-60 min).

Os canais repetem nicho (carros na Polônia, agro no Brasil, marinha dos EUA, mar/sobrevivência, Egito...). A cada
filme eu reescrevia as buscas do zero e a 1ª rodada errava (salão de Paris em filme polonês, silo americano em filme
brasileiro). Um pacote guarda o que JÁ FUNCIONOU num filme entregue: descrições das tags, buscas do Commons
(rodadas 1 e 2), categorias, buscas do Pexels (foto e vídeo), buscas do YouTube/DVIDS, mapa BANCO (tags do banco já
gravadas com prefixo de país/nicho), PAIS e as reservas do build_plan.

  python pacote.py listar
  python pacote.py extrair <nome> <pasta com os scripts do tema> [--pais BR] [--banco-prefixo br_] [--yt arquivo.txt]
  python pacote.py aplicar <nome> [tag1,tag2,...]   # grava as buscas do pacote nos fetch_*.py desta baia (só as tags
                                                    # pedidas, ou todas) e mostra o bloco TAGS/BANCO/PAIS para o beats.py
Pasta: <ALTA PRODUÇÃO>/pacotes/<nome>.json (fora das baias, sobrevive à limpeza).
"""
import ast, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT.parent.parent if ROOT.parent.name == "baias" else ROOT.parent
PAC = BASE / "pacotes"
BANCO = BASE / "banco" / "banco.json"


def bloco(src, nome):
    """Lê o dicionário `NOME = {...}` do código pelo AST (vale para chave fechando na mesma linha e para
    constantes simples usadas dentro dele, como F = "USS Gerald R. Ford" no tema do Ford)."""
    try:
        mod = ast.parse(src)
    except SyntaxError:
        return {}
    env = {}
    for no in mod.body:
        if isinstance(no, ast.Assign) and len(no.targets) == 1 and isinstance(no.targets[0], ast.Name):
            alvo = no.targets[0].id
            if isinstance(no.value, ast.Constant) and isinstance(no.value.value, str):
                env[alvo] = no.value.value
            if alvo == nome:
                try:
                    return ast.literal_eval(no.value)
                except Exception:  # noqa: BLE001
                    try:
                        return eval(compile(ast.Expression(no.value), "<pacote>", "eval"), {}, dict(env))  # noqa: S307
                    except Exception:  # noqa: BLE001
                        return {}
    return {}


def junta(a, b):
    out = {k: list(v) if isinstance(v, (list, tuple)) else v for k, v in a.items()}
    for k, v in b.items():
        if isinstance(v, (list, tuple)):
            out[k] = list(dict.fromkeys(list(out.get(k, [])) + list(v)))
        else:
            out.setdefault(k, v)
    return out


def ler(p):
    return p.read_text("utf-8") if p.exists() else ""


def extrair(nome, pasta, pais=None, prefixo=None, yt=None):
    pasta = Path(pasta)
    fi, fc, fa, fs, bp, be = (pasta / n for n in ("fetch_images.py", "fetch_images_cat.py", "fetch_photos_api.py",
                                                  "fetch_stock_api.py", "build_plan.py", "beats.py"))
    commons = {}
    for f in (fi, fi.with_name("fetch_images.py.bak_r1")):
        commons = junta(commons, bloco(ler(f), "QUERIES"))
    api = {}
    for f in (fa, fa.with_name("fetch_photos_api.py.bak_r1")):
        api = junta(api, bloco(ler(f), "QUERIES"))
    tags = bloco(ler(be), "TAGS")
    banco = {t: list(v) for t, v in bloco(ler(be), "BANCO").items()}   # o mapa que o filme já usou
    if prefixo and BANCO.exists():
        tb = {k.split("/")[0] for k in json.loads(BANCO.read_text("utf-8"))}
        for t in tags:
            if prefixo + t in tb:
                banco[t] = list(dict.fromkeys([prefixo + t] + banco.get(t, [])))
    reservas = {}
    src_bp = ler(bp)
    for n in ("FALLBACK_TAGS", "REGIONAL", "INTERIOR_FALLBACK"):
        m = re.search(rf"^{n} = (\[[^\]]*\])", src_bp, re.M)
        if m:
            reservas[n] = ast.literal_eval(m.group(1))
    for n in ("INTERIOR_TAGS", "PHOTO_RUN_TAGS"):
        m = re.search(rf"^{n} = (\{{[^}}]*\}})", src_bp, re.M)
        if m:
            reservas[n] = sorted(ast.literal_eval(m.group(1)))
    pac = {"nome": nome, "pais": pais, "tags": tags, "commons": commons, "categorias": bloco(ler(fc), "CATS"),
           "pexels_foto": api, "pexels_video": bloco(ler(fs), "QUERIES_NAVIO"), "banco": banco, "reservas": reservas,
           "youtube": [l.strip() for l in ler(Path(yt)).splitlines() if l.strip()] if yt else [],
           "rejeita_titulo": bloco(ler(be), "REJEITA") or None}
    m = re.search(r"^REJEITA_TITULO = (\[.*?\])\n", ler(be), re.M | re.S)
    pac["rejeita_titulo"] = ast.literal_eval(m.group(1)) if m else []
    PAC.mkdir(exist_ok=True)
    (PAC / f"{nome}.json").write_text(json.dumps(pac, ensure_ascii=False, indent=1), "utf-8")
    print(f"[pacote] {nome}: {len(tags)} tags, {sum(len(v) for v in commons.values())} buscas Commons, "
          f"{len(pac['categorias'])} categorias, {len(api)} tags Pexels foto, {len(pac['pexels_video'])} tags Pexels vídeo, "
          f"{len(banco)} tags no banco, {len(pac['youtube'])} buscas YouTube -> {PAC / (nome + '.json')}")


def troca(p, head, body):
    s = p.read_text("utf-8")
    i = s.index(head)
    j = s.index("\n}\n", i) + 3
    if not p.with_name(p.name + ".bak_pacote").exists():
        shutil.copy2(p, p.with_name(p.name + ".bak_pacote"))
    p.write_text(s[:i] + body + s[j:], "utf-8")


def aplicar(nome, so=None):
    pac = json.loads((PAC / f"{nome}.json").read_text("utf-8"))
    f = lambda d: {k: v for k, v in d.items() if not so or k in so}
    lit = lambda nomevar, d, nota: f"{nomevar} = {{  # pacote {nome} — {nota}\n" + "".join(f"    {k!r}: {v!r},\n" for k, v in d.items()) + "}\n"
    S = ROOT / "scripts"
    troca(S / "fetch_images.py", "QUERIES = {", lit("QUERIES", f(pac["commons"]), "Commons"))
    troca(S / "fetch_images_cat.py", "CATS = {", lit("CATS", {k: v for k, v in pac["categorias"].items() if not so or v in so}, "categorias"))
    troca(S / "fetch_photos_api.py", "QUERIES = {", lit("QUERIES", f(pac["pexels_foto"]), "Pexels/Pixabay foto"))
    if pac.get("pexels_video"):
        troca(S / "fetch_stock_api.py", "QUERIES_NAVIO = {", lit("QUERIES_NAVIO", f(pac["pexels_video"]), "Pexels vídeo (--navio)"))
    if pac.get("youtube"):
        (ROOT / "data" / f"yt_queries_{nome}.txt").write_text("\n".join(pac["youtube"]), "utf-8")
    print(f"[pacote] {nome} aplicado nos fetch_*.py" + (f" (tags {', '.join(so)})" if so else ""))
    print("\n# --- para o beats.py (ajustar ao roteiro) ---")
    print(f"PAIS = {pac.get('pais')!r}")
    print("TAGS = {\n" + "".join(f"    {k!r}: {v!r},\n" for k, v in f(pac["tags"]).items()) + "}")
    print(f"BANCO = {f(pac['banco'])!r}")
    print(f"# reservas do build_plan: {json.dumps(pac['reservas'], ensure_ascii=False)}")


def main():
    a = sys.argv[1:]
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if not a or a[0] == "listar":
        for p in sorted(PAC.glob("*.json")) if PAC.exists() else []:
            d = json.loads(p.read_text("utf-8"))
            print(f"  {p.stem:22s} país {d.get('pais') or '-':3s} {len(d['tags']):3d} tags  {len(d['banco']):3d} no banco")
        return
    if a[0] == "extrair":
        extrair(a[1], a[2], op("--pais"), op("--banco-prefixo"), op("--yt"))
    elif a[0] == "aplicar":
        aplicar(a[1], set(a[2].split(",")) if len(a) > 2 and not a[2].startswith("--") else None)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
