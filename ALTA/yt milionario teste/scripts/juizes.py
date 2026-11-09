"""JUÍZES EM PARALELO — as folhas de FOTOS divididas em lotes para 3-4 agentes julgarem ao mesmo tempo.

25/09/2026 (aprovado pelo usuário para a meta de 1h10-1h30 por filme): julgar ~35 folhas de foto em série levava
25-30 min. Cada agente recebe um lote de TAGS inteiras (a mesma tag nunca é dividida: critério e variedade ficam
com um juiz só), as mesmas regras, a descrição de cada tag, o trecho da narração e a cota. As folhas de VÍDEO, a
folha pré-render e a folha do MP4 continuam comigo. Depois eu confiro TODAS as aprovadas numa folha só
(`conferir`) — é a trava contra critério desigual entre os juízes.

Uso:
  python juizes.py preparar 4 --pais "Brasil" [--extra "critério do filme"]   # lotes em data/juizes/lote_K.md
      -> eu disparo 1 agente por lote (Agent, em paralelo): "Leia data/juizes/lote_K.md e siga à risca."
  python juizes.py juntar            # valida os lote_K.json e grava data/photo_approve.json (-> photo_review.py)
  python juizes.py conferir          # qa/photos/_conferencia_NN.jpg: todas as aprovadas, 40 por folha
  python juizes.py tirar 123,456     # tira aprovações que eu reprovar na conferência (viram reject)
Rodada extra (tag que não fechou a cota): photo_dl --miniaturas --mais tagX ; photo_sheet qa/photos --mais tagX ;
preparar de novo — só as folhas ainda não julgadas entram nos lotes.
"""
import json, math, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
Q = ROOT / "qa" / "photos"
J = D / "juizes"
sys.path.insert(0, str(ROOT / "scripts"))
COLS = 6

REGRAS = """## Regras (as mesmas para todos os juízes)
APROVE só a foto que MOSTRA o que a tag pede (descrição da tag) e combina com o que a narração diz no trecho.
País do filme: **{pais}**. A foto tem de parecer desse país: placa de carro, letreiro, idioma das placas, moeda,
paisagem, arquitetura, uniforme. Vale para CENÁRIO (rua, trânsito, posto, cidade, campo, prédio, porto): cenário
claramente de outro país = rejeitar. Tag de OBJETO/MODELO (um carro, uma máquina, uma bateria, uma peça) vale pelo
objeto certo: placa estrangeira no carro certo pode, desde que a tag não diga "no Brasil"/lugar específico.

REJEITE sempre:
- logotipo de canal, marca d'água, texto/legenda queimada na imagem, captura de tela, cartela, infográfico
  (carimbo de data PEQUENO no canto, de câmera ou panoramio, NÃO conta: aprove se o resto serve);
- youtuber/apresentador falando para a câmera, selfie, rosto em close sem relação com o tema;
- render 3D, CGI, desenho, ilustração, maquete, miniatura, brinquedo, simulador/jogo;
- cerimônia, visita oficial, aperto de mão, palanque, coletiva, entrega de prêmio, pose de político;
- marca que não é do tema (banco, concorrente, outra montadora/empresa em destaque) e modelo errado quando a tag
  pede um modelo específico;
- foto escura demais, borrada, minúscula, torta, colagem, recorte estreito vertical demais para 16:9;
- época errada: preto e branco/antiga numa tag moderna (se a tag aceita época, aprove e ponha em "era_old").
Marcas na folha: **AUTO** = o título caiu na lista de rejeição (só aprove se a imagem estiver claramente certa);
**DUP** = quase igual a outra (não aprove se já aprovou a parecida).
VARIEDADE: não aprove várias fotos do mesmo lugar/ângulo; prefira planos diferentes (geral, médio, detalhe).
A COTA é o MÍNIMO que o filme precisa: aprove TUDO o que serve, até 2x a cota (sobra = variedade e reserva para
a folha final). Se não chegar à cota, diga quantas faltam em "faltam".
Na dúvida, REJEITE — sempre dá para buscar mais.
{extra}
## Como ler cada folha
Abra a folha com Read (imagem). Grade de 6 colunas x 4 linhas, lida da esquerda para a direita, de cima para
baixo. A tabela abaixo dá o #N de cada posição e o título do arquivo (o título ajuda: nome de banco, de país, de
modelo). Confira pelo rótulo amarelo no topo do ladrilho quando der para ler. Se um ladrilho estiver pequeno
demais para decidir, rejeite.

## Resposta
Grave o arquivo `{saida}` (JSON, UTF-8) exatamente assim:
{{"approve": {{"123": ["tag"], "456": ["tag"]}}, "era_old": [789], "faltam": {{"tag": 3}},
 "notas": "1-3 frases sobre o que mais caiu"}}
Só índices #N das SUAS folhas. Não mexa em nenhum outro arquivo. No fim, responda só: aprovadas por tag e faltas.
"""


def jl(p, d=None):
    return json.loads(Path(p).read_text("utf-8")) if Path(p).exists() else d


def trechos(bj):
    """Trecho da narração de cada tag (até 3 parágrafos, 280 caracteres cada)."""
    paras = jl(D / "master_transcript.json")["paragraphs"]
    out = {}
    for b in bj["beats"]:
        txt = paras[b["para"]].get("text") or " ".join(w.get("word", "") for w in paras[b["para"]].get("words", []))
        for t in b["tags"]:
            if len(out.setdefault(t, [])) < 3:
                out[t].append(txt.strip()[:280])
    return out


def preparar(n, pais, extra):
    from demanda import cotas
    fidx, index = jl(Q / "folhas_idx.json", {}), jl(Q / "index.json", {})
    J.mkdir(parents=True, exist_ok=True)
    julgadas = set(jl(J / "julgadas.json", []))
    por_tag = {}
    for folha in sorted(fidx):
        if folha not in julgadas and (Q / folha).exists():
            por_tag.setdefault(re.sub(r"_\d\d\.jpg$", "", folha), []).append(folha)
    if not por_tag:
        print("[juizes] nenhuma folha nova para julgar"); return
    lotes = [[] for _ in range(min(n, len(por_tag)))]
    for tag in sorted(por_tag, key=lambda t: -len(por_tag[t])):   # tag inteira no lote mais leve
        min(lotes, key=lambda l: sum(len(por_tag[t]) for t in l)).append(tag)
    bj = jl(D / "beats.json")
    q, tr = cotas(), trechos(bj)
    aprovadas = {}
    for v in jl(D / "photo_side.json", {}).values():
        if v.get("verdict") == "ok" and v.get("tags"):
            aprovadas[v["tags"][0]] = aprovadas.get(v["tags"][0], 0) + 1
    for k, tags in enumerate(lotes, 1):
        saida = (J / f"lote_{k}.json").as_posix()   # absoluto: o agente não roda na pasta do projeto
        md = [f"# Lote {k} de {len(lotes)} — julgar folhas de fotos do filme\n",
              REGRAS.format(pais=pais, extra=(f"\nCritério deste filme: {extra}\n" if extra else ""), saida=saida)]
        folhas = []
        for tag in tags:
            md.append(f"\n## Tag `{tag}` — cota {q.get(tag, 0)} (já aprovadas antes: {aprovadas.get(tag, 0)})")
            md.append(f"Pede: {bj['tags'].get(tag, tag)}")
            for s in tr.get(tag, []):
                md.append(f"> narração: {s}")
            for folha in por_tag[tag]:
                folhas.append(folha)
                md.append(f"\n### Folha `{(Q / folha).as_posix()}`")
                md.append("| linha | col | #N | título |\n|---|---|---|---|")
                for pos, i in enumerate(fidx[folha]):
                    md.append(f"| {pos // COLS + 1} | {pos % COLS + 1} | {i} | {index.get(str(i), '')[5:70]} |")
        (J / f"lote_{k}.md").write_text("\n".join(md) + "\n", "utf-8")
        (J / f"lote_{k}_folhas.json").write_text(json.dumps(folhas), "utf-8")
        print(f"[juizes] lote {k}: {len(folhas)} folhas, tags {', '.join(tags)}")
    print(f"[juizes] {len(lotes)} lotes -> 1 agente por lote (em paralelo), prompt: "
          f"\"Leia {(J / 'lote_K.md').as_posix()} e siga à risca.\"")


def juntar():
    fidx = jl(Q / "folhas_idx.json", {})
    ap_p = D / "photo_approve.json"
    ap = jl(ap_p, {"approve": {}, "ranges": [], "era_old": []})
    julgadas = set(jl(J / "julgadas.json", []))
    from demanda import cotas
    q = cotas()
    faltam, total = {}, 0
    for lf in sorted(J.glob("lote_*_folhas.json")):
        k = lf.name.split("_")[1]
        res_p = J / f"lote_{k}.json"
        folhas = json.loads(lf.read_text("utf-8"))
        if all(f in julgadas for f in folhas):
            continue
        if not res_p.exists():
            print(f"[juizes] lote {k}: SEM resposta ({res_p.name}) — rodar o agente de novo"); continue
        res = json.loads(res_p.read_text("utf-8"))
        vistos = {i for f in folhas for i in fidx.get(f, [])}
        fora = [n for n in res.get("approve", {}) if int(n) not in vistos]
        if fora:
            print(f"[juizes] lote {k}: {len(fora)} índices fora das folhas do lote ignorados ({', '.join(fora[:5])})")
        for n, tags in res.get("approve", {}).items():
            if int(n) in vistos:
                ap["approve"][str(int(n))] = tags if isinstance(tags, list) else [tags]
                total += 1
        ap["era_old"] = sorted(set(ap.get("era_old", [])) | {int(x) for x in res.get("era_old", []) if int(x) in vistos})
        ap["ranges"] += [[i, i] for i in sorted(vistos)]
        faltam.update({t: v for t, v in res.get("faltam", {}).items() if v})
        julgadas |= set(folhas)
        print(f"[juizes] lote {k}: {sum(1 for n in res.get('approve', {}) if int(n) in vistos)} aprovadas | "
              f"{res.get('notas', '')[:160]}")
    ap["ranges"] = [list(r) for r in sorted({tuple(r) for r in ap["ranges"]})]
    ap_p.write_text(json.dumps(ap, ensure_ascii=False, indent=1), "utf-8")
    (J / "julgadas.json").write_text(json.dumps(sorted(julgadas)), "utf-8")
    por_tag = {}
    for tags in ap["approve"].values():
        por_tag[tags[0]] = por_tag.get(tags[0], 0) + 1
    curtas = [t for t, c in q.items() if c and por_tag.get(t, 0) < c * 0.8]
    print(f"[juizes] +{total} aprovadas -> {ap_p.name} (total {len(ap['approve'])}) | depois: photo_review.py")
    if curtas or faltam:
        tags = sorted(set(curtas) | set(faltam))
        print(f"[juizes] abaixo da cota: {', '.join(f'{t} {por_tag.get(t, 0)}/{q.get(t, 0)}' for t in tags)}")
        print(f"          -> photo_dl --miniaturas --mais {','.join(tags)} ; photo_sheet qa/photos --mais {','.join(tags)}")


def conferir():
    ap = jl(D / "photo_approve.json", {"approve": {}})
    index, pool = jl(Q / "index.json", {}), jl(D / "photo_pool.json", {})
    itens = sorted(((v[0], int(n)) for n, v in ap["approve"].items()), key=lambda x: (x[0], x[1]))
    # fotos servidas pelo BANCO entram aprovadas, mas foram julgadas para OUTRO filme: vão para a conferência
    # também, rotuladas B<k> (submarino da 2ª Guerra servido como "praça de máquinas" no filme dos piratas)
    side = jl(D / "photo_side.json", {})
    bmap = {}
    for t, v in sorted(side.items(), key=lambda kv: ((kv[1].get("tags") or [""])[0], kv[0])):
        if v.get("banco") and v.get("verdict") == "ok":
            k = f"B{len(bmap)}"
            bmap[k] = t
            itens.append(((v.get("tags") or ["?"])[0], k))
    (Q / "_conferencia_banco.json").write_text(json.dumps(bmap, ensure_ascii=False, indent=0), "utf-8")
    TW, TH, C, R = 330, 186, 8, 5
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    for old in Q.glob("_conferencia_*.jpg"):
        old.unlink()
    for f in range(math.ceil(len(itens) / (C * R))):
        sheet = Image.new("RGB", (C * TW, R * (TH + 20)), (18, 18, 18))
        dr = ImageDraw.Draw(sheet)
        for k, (tag, n) in enumerate(itens[f * C * R:(f + 1) * C * R]):
            x, y = (k % C) * TW, (k // C) * (TH + 20)
            e = pool.get(bmap[n] if isinstance(n, str) else index.get(str(n), ""), {})
            src = next((e[c] for c in ("thumb_file", "file") if e.get(c) and Path(e[c]).exists()), None)
            try:   # miniatura corrompida (Commons devolveu HTML): tenta a foto cheia
                im = Image.open(src).convert("RGB")
            except Exception:  # noqa: BLE001
                im = Image.open(e["file"]).convert("RGB") if e.get("file") and Path(e["file"]).exists() else None
            if im:
                im.thumbnail((TW - 4, TH))
                sheet.paste(im, (x + (TW - im.width) // 2, y + 20 + (TH - im.height) // 2))
            dr.text((x + 4, y + 2), f"#{n} {tag}"[:40], fill=(120, 200, 255) if isinstance(n, str) else (255, 220, 0), font=font)
        p = Q / f"_conferencia_{f:02d}.jpg"
        sheet.save(p, quality=82)
        print("[juizes] conferência:", p)
    print(f"[juizes] {len(itens)} aprovadas em {math.ceil(len(itens) / (C * R))} folhas — reprovar: juizes.py tirar N,N")


def tirar(ns):
    bmap = jl(Q / "_conferencia_banco.json", {})
    side_p = D / "photo_side.json"
    side = jl(side_p, {})
    for b in [n for n in ns if n.upper().startswith("B")]:     # item do banco: só sai deste filme
        t = bmap.get(b.upper())
        if t in side:
            side[t] = {"verdict": "reject", "note": "conferência: banco não serve neste tema", "banco": side[t].get("banco")}
    side_p.write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    ns = [n for n in ns if not n.upper().startswith("B")]
    p = D / "photo_approve.json"
    ap = jl(p, {"approve": {}, "ranges": [], "era_old": []})
    for n in ns:
        ap["approve"].pop(str(int(n)), None)
        ap["ranges"].append([int(n), int(n)])
    p.write_text(json.dumps(ap, ensure_ascii=False, indent=1), "utf-8")
    index = jl(Q / "index.json", {})   # se o photo_review já rodou, a foto volta a reject agora
    for n in ns:
        t = index.get(str(int(n)))
        if t in side and not side[t].get("banco"):
            side[t] = {"verdict": "reject", "note": "conferência dos juízes"}
    side_p.write_text(json.dumps(side, ensure_ascii=False, indent=1), "utf-8")
    print(f"[juizes] {len(ns)} tiradas")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if a[0] == "preparar":
        if "--pais" not in a:
            print("informe --pais (as fotos têm de ser do país do roteiro)"); return
        preparar(int(a[1]) if len(a) > 1 and a[1].isdigit() else 4, op("--pais"), op("--extra", ""))
    elif a[0] == "juntar":
        juntar()
    elif a[0] == "conferir":
        conferir()
    elif a[0] == "tirar":
        tirar([x for x in a[1].split(",") if x])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
