"""BANCO DE AMBIENTAÇÃO — o material genérico que se repete em todo filme fica guardado e pronto para usar.

O assunto do filme NUNCA entra no banco (Jimny, Saveiro, sino de mergulho, locomotiva do Cajon são buscados de
novo a cada vídeo). Só entra ambientação: trânsito, fábrica, escapamento, concessionária, oficina, pátio de
usados, recarga elétrica, tempestade no mar, porto, casa vazia, empregos perigosos...

No filme dos carros isso foi 664 das 2.148 fotos baixadas (30 % da coleta) para 23 cortes no filme final.

Pasta: ..\\banco  (fora da pasta do filme, sobrevive à limpeza)
  banco/<tag>/<arquivo>          foto 1920x1080 ou clipe já normalizado
  banco/banco.json               ficha de cada item (fonte, licença, autor, url, tags, phash)
  banco/uso.json                 {item: [{"filme": slug, "data": "AAAA-MM-DD"}]}

Uso:
  python banco.py guardar <slug-do-filme> tag1 tag2 ...   # depois da entrega: guarda o que foi aprovado
  python banco.py servir  <slug-do-filme> tag1 tag2 ...   # no começo: injeta o banco no pool/side do filme
  python banco.py listar
  python banco.py sugerir                                 # tags do banco parecidas com as tags do beats.json
  python banco.py paises                                  # 04/10: anota o país de cada item (filtro do servir)
  python banco.py servir-beats <slug> [--simular]          # BANCO PRIMEIRO (25/09/2026): serve o mapa BANCO do
                                                           # beats.py {tag_do_filme: [tags_do_banco]} até a cota
Banco primeiro (25/09/2026): depois do beats.py e ANTES do photo_dl --miniaturas. O que o banco serve entra
aprovado com a TAG DO FILME e sai da cota (demanda.py) — tag coberta não baixa nem gera folha. O mapa é escolhido
por mim filme a filme, olhando o `sugerir`: só ambientação do PAÍS do roteiro (warszawa não serve em filme
brasileiro; linha de montagem, bateria, laboratório servem em qualquer um).
Regras de reuso (o servir respeita):
  - item não volta nos próximos REPOUSO filmes (padrão 3);
  - no máximo 1 aparição do mesmo item por filme (o build_plan já evita repetir clipe seguido).
"""
import json, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
BANCO = (ROOT.parent.parent if ROOT.parent.name == "baias" else ROOT.parent) / "banco"   # 28/09: baia usa o banco da ALTA PRODUÇÃO
FICHA = BANCO / "banco.json"
USO = BANCO / "uso.json"
REPOUSO = 3  # filmes que o item tem de ficar de molho antes de voltar


# 04/10/2026 — PAÍS de cada item. O banco serviu 64 fotos de agro dos EUA/Inglaterra/Alemanha num filme brasileiro
# (os juízes não veem item do banco). Cada item ganha "pais" (detectado no título/crédito/consulta, ou o país do filme
# que o aprovou quando a tag era de lugar) e o servir PULA item de outro país quando o beats.py declara PAIS = "BR".
import re as _re, unicodedata as _ud
PAISES = [  # ordem importa: o primeiro que casar vence
    ("BR", r"brasil|brazil|sao paulo|rio grande do sul|rio de janeiro|parana|mato grosso|goias|minas gerais|bahia|"
           r"pernambuco|ceara|santa catarina|brasilia|porto alegre|curitiba|recife|fortaleza|pelotas|paranagua|"
           r"banco do brasil|embrapa|conab|agencia brasil|faria lima|esplanada dos ministerios|real banknote"),
    ("PL", r"poland|polska|polish|warszaw|warsaw|krakow|cracow|poznan|wroclaw|gdansk|gdynia|lodz|katowice|zloty"),
    ("UK", r"geograph\.org\.uk|geograph|england|scotland|wales|london|united kingdom|\buk\b|britain"),
    ("US", r"united states|uss |usns |coast guard|\busa\b|usda|nrcs|fpac|u\.s\.|us navy|texas|iowa|illinois|indiana|nebraska|kansas|ohio|"
           r"minnesota|dakota|missouri|kentucky|california|florida|wisconsin|michigan|arkansas|tennessee|alabama|"
           r"oklahoma|colorado|oregon|montana|idaho|pennsylvania|new york|virginia|carolina|gettysburg|albany"),
    ("DE", r"germany|deutschland|german|berlin|munchen|munich|hamburg|thuringia|bavaria|bayern|sachsen|wolfsburg"),
    ("ES", r"spain|espana|madrid|barcelona|mallorca|sineu|andaluc|ebro|valencia|sevilla"),
    ("FR", r"france|paris|lyon|marseille|bretagne|normandie"),
    ("IT", r"italy|italia|roma|milano|napoli|sicilia|torino"),
    ("AR", r"argentina|buenos aires|cordoba arg"), ("PE", r"\bperu\b|juliaca|lima peru"), ("VE", r"venezuela|margarita island"),
    ("CN", r"china|chinese|beijing|shanghai|guangzhou|shenzhen|pla type"), ("IN", r"\bindia\b|mumbai|delhi"),
    ("AU", r"australia|csiro|sydney|melbourne|queensland"), ("CA", r"canada|ontario|alberta|quebec|halifax|manitoba"),
    ("UY", r"uruguay|montevideo"), ("LT", r"lithuania|vilnius|kaunas"), ("NO", r"norway|norge|oslo|bergen"), ("BD", r"bangladesh"),
]


def _sem_acento(t):
    return "".join(ch for ch in _ud.normalize("NFD", str(t or "")) if _ud.category(ch) != "Mn").lower()


def pais_de(item):
    """País pelo título, crédito, consulta e url do item (None = genérico/sem pista)."""
    texto = _sem_acento(" ".join(str(item.get(k) or "") for k in ("titulo", "title", "credito", "credit", "query", "url", "descurl")))
    for cod, pad in PAISES:
        if _re.search(pad, texto):
            return cod
    return None


def jload(p, d):
    return json.loads(p.read_text("utf-8")) if p.exists() else d


def jsave(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=1), "utf-8")


def usadas_no_filme():
    """Títulos que realmente APARECERAM no filme (timeline -> clips.json). Aprovada na folha mas não usada não
    conta como uso: senão o item nasceria de molho e o banco nunca serviria no filme seguinte."""
    tl = jload(D / "timeline.json", {"items": []})["items"]
    lib = {c["id"]: c for c in jload(D / "clips.json", {"clips": []})["clips"]}
    return {lib[i["clip"]].get("title") for i in tl if i.get("clip") in lib and lib[i["clip"]].get("title")}


def guardar(slug, tags):
    """Copia para o banco as fotos APROVADAS das tags de ambientação (com a ficha de crédito)."""
    side = jload(D / "photo_side.json", {})
    pool = jload(D / "photo_pool.json", {})
    usadas = usadas_no_filme()
    bj = jload(D / "beats.json", {})
    pais_filme, lugar = bj.get("pais"), set(bj.get("tags_lugar") or [])   # 04/10: país do roteiro e tags de lugar
    ficha, uso = jload(FICHA, {}), jload(USO, {})
    novos = 0
    for titulo, v in side.items():
        if v.get("verdict") != "ok":
            continue
        tag = (v.get("tags") or [""])[0]
        if tag not in tags or v.get("banco"):   # veio do banco: já está lá (sem cópia duplicada em outra tag)
            continue
        e = pool.get(titulo)
        if not e or not e.get("file") or not Path(e["file"]).exists():
            continue
        dst_dir = BANCO / tag
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / Path(e["file"]).name
        chave = f"{tag}/{dst.name}"
        if chave in ficha:
            continue
        shutil.copy2(e["file"], dst)
        ficha[chave] = {"titulo": titulo, "tags": v.get("tags", [tag]), "licenca": e.get("license"),
                        "autor": e.get("artist"), "credito": e.get("credit"), "url": e.get("descurl"),
                        "width": e.get("width"), "height": e.get("height"), "query": e.get("query"),
                        "de": slug, "em": date.today().isoformat(),
                        "pais": pais_de({"titulo": titulo, "credito": e.get("credit"), "query": e.get("query"),
                                         "url": e.get("descurl")}) or (pais_filme if tag in lugar else None)}
        if titulo in usadas:  # só conta repouso quem foi ao ar neste filme
            uso.setdefault(chave, []).append({"filme": slug, "data": date.today().isoformat()})
        novos += 1
    jsave(FICHA, ficha); jsave(USO, uso)
    mb = sum(f.stat().st_size for f in BANCO.rglob("*.jpg")) / 1048576
    print(f"[banco] +{novos} itens | total {len(ficha)} ({mb:.0f} MB) em {BANCO}")


def servir(slug, tags, limite=14, tag_filme=None, simular=False):
    """Injeta no filme atual o que o banco já tem dessas tags: entra no photo_pool e já APROVADO no photo_side,
    então não passa pela folha de contato de novo (já foi julgado quando entrou no banco)."""
    ficha, uso = jload(FICHA, {}), jload(USO, {})
    if not ficha:
        print("[banco] vazio — nada a servir"); return
    pool, side = jload(D / "photo_pool.json", {}), jload(D / "photo_side.json", {})
    filmes = []                                   # ordem dos filmes que já usaram o banco (para o repouso)
    for us in uso.values():
        for u in us:
            if u["filme"] not in filmes:
                filmes.append(u["filme"])
    recentes = set(filmes[-REPOUSO:])
    dest = ROOT / "assets" / "banco"
    dest.mkdir(parents=True, exist_ok=True)
    postos = 0
    molho = 0
    pais = jload(D / "beats.json", {}).get("pais")   # 04/10: PAIS do beats.py — item de outro país não entra
    fora = 0
    for tag in tags:
        cand = [(k, v) for k, v in ficha.items() if k.split("/")[0] == tag]
        if pais:
            antes = len(cand)
            cand = [(k, v) for k, v in cand if (v.get("pais") or pais_de(v)) in (None, pais)]
            fora += antes - len(cand)
        molho += sum(1 for k, _ in cand if any(u["filme"] in recentes for u in uso.get(k, [])))
        cand = [(k, v) for k, v in cand if not any(u["filme"] in recentes for u in uso.get(k, []))]
        cand.sort(key=lambda kv: len(uso.get(kv[0], [])))   # menos usado primeiro
        for k, v in cand:
            src = BANCO / k
            if not src.exists():
                continue
            loc = dest / Path(k).name
            titulo = v.get("titulo") or f"File:{Path(k).name}"
            if titulo in side and side[titulo].get("verdict") == "ok":
                continue                                  # já servido/aprovado por outra tag neste filme
            if postos >= limite:
                break
            if simular:
                postos += 1; continue
            if not loc.exists():
                shutil.copy2(src, loc)
            tg = ([tag_filme] if tag_filme else []) + [t for t in v.get("tags", [tag]) if t != tag_filme]
            pool[titulo] = {"title": titulo, "tags": tg, "query": v.get("query", tag),
                            "url": v.get("url"), "descurl": v.get("url"), "width": v.get("width"),
                            "height": v.get("height"), "license": v.get("licenca"), "artist": v.get("autor"),
                            "credit": v.get("credito"), "file": str(loc), "banco": k}
            side[titulo] = {"verdict": "ok", "tags": tg, "era": "modern", "banco": k}
            uso.setdefault(k, []).append({"filme": slug, "data": date.today().isoformat()})
            postos += 1
    if not simular:
        jsave(D / "photo_pool.json", pool); jsave(D / "photo_side.json", side); jsave(USO, uso)
    print(f"[banco]{' (simulação)' if simular else ''}{' ' + tag_filme + ' <-' if tag_filme else ''} {postos} itens servidos ({', '.join(tags)}) — já aprovados, fora da folha de contato"
          + (f" | {molho} em repouso (saíram num dos últimos {REPOUSO} filmes)" if molho else "")
          + (f" | {fora} fora por serem de outro país (PAIS={pais})" if fora else ""))


def servir_beats(slug, simular=False):
    """BANCO PRIMEIRO: para cada tag do filme mapeada no beats.py (BANCO = {tag: [tags do banco]}), serve até a
    cota BRUTA da tag (demanda.py). O resto da cota sai do Commons como sempre."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from demanda import cotas
    mapa = jload(D / "beats.json", {}).get("banco", {})
    if not mapa:
        print("[banco] beats.json sem mapa BANCO — nada a servir (ver `banco.py sugerir`)"); return
    q = cotas(bruta=True)
    total = 0
    for tag_filme, tags_banco in mapa.items():
        if tag_filme not in q:
            print(f"[banco] {tag_filme}: não está em nenhum beat — pulada"); continue
        side = jload(D / "photo_side.json", {})
        ja = sum(1 for v in side.values() if v.get("banco") and v.get("verdict") == "ok" and (v.get("tags") or [""])[0] == tag_filme)
        falta = q[tag_filme] - ja
        if falta > 0:
            servir(slug, tags_banco, limite=falta, tag_filme=tag_filme, simular=simular)
            total += 1
    rest = cotas()
    print(f"[banco] cota que sobra para o Commons: {sum(rest.values())} de {sum(q.values())} fotos"
          + (" (simulação: nada gravado)" if simular else ""))


def sugerir():
    """Tags do banco com palavra parecida com o nome/descrição de cada tag do filme (primeiras 4 letras)."""
    import re
    ficha = jload(FICHA, {})
    por_tag = {}
    for k in ficha:
        por_tag[k.split("/")[0]] = por_tag.get(k.split("/")[0], 0) + 1
    tags = jload(D / "beats.json", {}).get("tags", {})
    raiz = lambda txt: {w[:4] for w in re.findall(r"[a-z]{4,}", txt.lower())} - {"with", "from", "that", "this", "their"}
    for t, desc in tags.items():
        r = raiz(t.replace("_", " ") + " " + desc)
        hits = [f"{bt}({n})" for bt, n in sorted(por_tag.items(), key=lambda kv: -kv[1]) if raiz(bt.replace("_", " ")) & r]
        if hits:
            print(f"  {t:20s} -> {', '.join(hits[:8])}")


def listar():
    ficha, uso = jload(FICHA, {}), jload(USO, {})
    por_tag = {}
    for k in ficha:
        por_tag.setdefault(k.split("/")[0], []).append(k)
    mb = sum(f.stat().st_size for f in BANCO.rglob("*") if f.is_file()) / 1048576
    print(f"[banco] {len(ficha)} itens, {mb:.0f} MB em {BANCO}")
    for tag, ks in sorted(por_tag.items(), key=lambda kv: -len(kv[1])):
        usos = sum(len(uso.get(k, [])) for k in ks)
        print(f"  {tag:18s} {len(ks):3d} itens  {usos:3d} usos")


def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd = sys.argv[1]
    if cmd == "listar":
        listar()
    elif cmd == "servir-beats":
        servir_beats(sys.argv[2], simular="--simular" in sys.argv)
    elif cmd == "sugerir":
        sugerir()
    elif cmd == "paises":   # 04/10: anota o país detectado em todos os itens e mostra a contagem
        ficha = jload(FICHA, {})
        from collections import Counter
        for v in ficha.values():
            if not v.get("pais"):
                v["pais"] = pais_de(v)
        jsave(FICHA, ficha)
        print("[banco] países:", dict(Counter(v.get("pais") or "?" for v in ficha.values()).most_common()))
    elif cmd in ("guardar", "servir"):
        slug, tags = sys.argv[2], sys.argv[3:]
        if not tags:
            print("informe as tags de ambientação (o assunto do filme NÃO entra no banco)"); return
        (guardar if cmd == "guardar" else servir)(slug, tags)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
