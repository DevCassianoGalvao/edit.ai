"""Folha de contato das FOTOS do pool, agrupadas por tag (juiz antes de aprovar qualquer foto).

21/09/2026: se data/photo_prefilter.json existir (scripts/prefilter.py), as fotos de cada tag saem ORDENADAS pela
nota do CLIP e as quase-duplicatas vão para o FIM, marcadas com DUP.

24/09/2026 — FOLHA SÓ ATÉ A COTA (--demanda). O demanda.py calcula quantas fotos cada tag precisa; a folha gera
só as primeiras ceil(cota / (24 x TAXA)) folhas de cada tag (as mais bem avaliadas pelo CLIP). Se a tag não
fechar a cota na folha, `--mais tag1,tag2` gera as folhas seguintes dela (mesma numeração #N).
Título que casa com a lista de rejeição (REJ_GLOBAL + "rejeita_titulo" do beats.json) vai para o fim com AUTO —
maquete, desenho, logotipo, cerimônia, marca concorrente: o que eu rejeitava na folha em todo filme.
A imagem é a miniatura de 500 px (photo_dl --miniaturas) quando ela existe.

Uso: python photo_sheet.py OUTDIR [--demanda] [--mais tag1,tag2] [--skip data/photo_side.json] [--sem-prefiltro]
Saída: OUTDIR/<tag>_NN.jpg (grade 6x4, rótulo = índice global + licença) + OUTDIR/index.json {n: title}
       + OUTDIR/demanda.md (cota, candidatas e folhas por tag) com --demanda
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, math, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))
COLS, ROWS, TW, TH = 6, 4, 440, 248
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
FONT_TAG = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
TAXA = 0.5   # fração aprovada nas primeiras folhas de uma tag boa (motores: 0,3-0,9; agro: 0,4-0,8)
# rejeição pelo TÍTULO do arquivo, em qualquer tema (o que caiu na folha em todos os filmes até 24/09/2026)
REJ_GLOBAL = (r"scale model|ship model|model ship|modellschiff|maquette|miniature|diorama|\blego\b|\btoys?\b|"
              r"\b3d render|\bcgi\b|diagram|schematic|blueprint|coat of arms|\blogo\b|\bflag of\b|\bposter\b|"
              r"postage stamp|visits ?-|visit of|signing ceremony|award ceremony|wedding|\bcosplay\b")


def imagem_de(e):
    for k in ("thumb_file", "file"):
        if e.get(k) and Path(e[k]).exists():
            return e[k]
    return None


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    pool = json.loads((D / "photo_pool.json").read_text("utf-8"))
    side = {}
    if "--skip" in sys.argv:
        p = Path(sys.argv[sys.argv.index("--skip") + 1])
        side = json.loads(p.read_text("utf-8")) if p.exists() else {}
    pre = {}
    if "--sem-prefiltro" not in sys.argv and (D / "photo_prefilter.json").exists():
        pre = json.loads((D / "photo_prefilter.json").read_text("utf-8"))
    bj = json.loads((D / "beats.json").read_text("utf-8")) if (D / "beats.json").exists() else {}
    rej = re.compile("|".join([REJ_GLOBAL] + list(bj.get("rejeita_titulo", []))), re.I)
    by_tag, index, n = {}, {}, 0
    for t, e in pool.items():
        if not imagem_de(e) or t in side:
            continue
        by_tag.setdefault(e["tags"][0], []).append((n, t, e))
        index[n] = t
        n += 1
    auto = {t for rows in by_tag.values() for _, t, _ in rows if rej.search(t)}
    for tag, rows in by_tag.items():   # melhor nota primeiro; AUTO e duplicata no fim
        rows.sort(key=lambda r: (r[1] in auto, bool(pre.get(r[1], {}).get("dup")),
                                 -float(pre.get(r[1], {}).get("nota", -1))))
    per = COLS * ROWS
    limite = {}
    if "--demanda" in sys.argv or "--mais" in sys.argv:
        from demanda import cotas
        q = cotas()
        mais = set(sys.argv[sys.argv.index("--mais") + 1].split(",")) if "--mais" in sys.argv else set()
        prev = json.loads((out / "folhas.json").read_text("utf-8")) if (out / "folhas.json").exists() else {}
        for tag, rows in by_tag.items():
            k = max(1, math.ceil(q[tag] / (per * TAXA))) if q.get(tag, 0) > 0 else 0   # banco cobriu = 0 folhas
            if tag in mais:
                k = prev.get(tag, k) + max(1, k)
            limite[tag] = min(k, math.ceil(len(rows) / per))
        (out / "folhas.json").write_text(json.dumps(limite, indent=1), "utf-8")
    geradas = 0
    # 28/09/2026: a rodada 2 baixa mais miniaturas e a numeração #N MUDA — no filme da Austrália as 150 aprovações
    # da rodada 1 passaram a apontar para a foto vizinha (siderúrgica como helióstato). Antes de gravar a numeração
    # nova, traduz photo_approve.json e folhas_idx.json da numeração antiga para a nova pelo TÍTULO do arquivo.
    velho_p = out / "index.json"
    if velho_p.exists():
        velho = {int(k): v for k, v in json.loads(velho_p.read_text("utf-8")).items()}
        if velho != index:
            novo = {t: k for k, t in index.items()}
            tr = lambda n: novo.get(velho.get(int(n)))
            ap_p = D / "photo_approve.json"
            if ap_p.exists():
                ap = json.loads(ap_p.read_text("utf-8"))
                antes = len(ap.get("approve", {}))
                ap["approve"] = {str(tr(n)): v for n, v in ap.get("approve", {}).items() if tr(n) is not None}
                vistos = {tr(i) for a, b in ap.get("ranges", []) for i in range(a, b + 1)} - {None}
                ap["ranges"] = [[i, i] for i in sorted(vistos)]
                ap["era_old"] = sorted({tr(n) for n in ap.get("era_old", [])} - {None})
                ap_p.write_text(json.dumps(ap, ensure_ascii=False, indent=1), "utf-8")
                print(f"[fotos] numeração nova: photo_approve.json traduzido pelo título ({len(ap['approve'])} de {antes})")
            fpv = out / "folhas_idx.json"
            if fpv.exists():
                fv = json.loads(fpv.read_text("utf-8"))
                fpv.write_text(json.dumps({k: [tr(i) for i in v if tr(i) is not None] for k, v in fv.items()}, indent=0), "utf-8")
    fp = out / "folhas_idx.json"   # {folha: [#N exibidos]} — juizes.py sabe o que cada lote VIU
    folhas_idx = json.loads(fp.read_text("utf-8")) if fp.exists() else {}
    for tag, rows in by_tag.items():
        nf = math.ceil(len(rows) / per)
        faz = range(limite[tag]) if limite else range(nf)
        if "--mais" in sys.argv and tag not in mais:
            faz = range(0)
        for f in faz:
            p = out / f"{tag}_{f:02d}.jpg"
            if "--mais" in sys.argv and p.exists():
                continue
            sheet = Image.new("RGB", (COLS * TW, ROWS * (TH + 22)), (18, 18, 18))
            dr = ImageDraw.Draw(sheet)
            for k, (i, t, e) in enumerate(rows[f * per:(f + 1) * per]):
                x, y = (k % COLS) * TW, (k // COLS) * (TH + 22)
                try:
                    im = Image.open(imagem_de(e)).convert("RGB")
                    im.thumbnail((TW, TH))
                    sheet.paste(im, (x + (TW - im.width) // 2, y + 22 + (TH - im.height) // 2))
                except Exception:  # noqa: BLE001
                    dr.rectangle([x, y + 22, x + TW - 2, y + 22 + TH], fill=(90, 0, 0))
                r = pre.get(t, {})
                nota = f"{r['nota']:+.2f} " if "nota" in r else ""
                dr.text((x + 4, y + 3), f"#{i} {nota}{e['license'][:12]} {t[5:34]}", fill=(255, 220, 0), font=FONT)
                marcas = "AUTO" if t in auto else "DUP" if r.get("dup") else ""
                if marcas:
                    dr.rectangle([x + TW - 92, y + 24, x + TW - 4, y + 50], fill=(140, 0, 0))
                    dr.text((x + TW - 86, y + 27), marcas, fill=(255, 255, 255), font=FONT_TAG)
            sheet.save(p, quality=80)
            folhas_idx[p.name] = [i for i, _, _ in rows[f * per:(f + 1) * per]]
            geradas += 1
            print("[fotos]", p, len(rows[f * per:(f + 1) * per]))
    fp.write_text(json.dumps(folhas_idx, indent=0), "utf-8")
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), "utf-8")
    if limite:
        from demanda import cotas
        q = cotas()
        linhas = ["| tag | cota | candidatas | folhas geradas / total |", "|---|---|---|---|"]
        for tag in sorted(by_tag, key=lambda t: -q.get(t, 0)):
            linhas.append(f"| {tag} | {q.get(tag, 0)} | {len(by_tag[tag])} | {limite.get(tag, 0)} / "
                          f"{math.ceil(len(by_tag[tag]) / per)} |")
        (out / "demanda.md").write_text("\n".join(linhas) + "\n", "utf-8")
        tot = sum(math.ceil(len(r) / per) for r in by_tag.values())
        print(f"[fotos] --demanda: {geradas} folhas geradas (de {tot}) | {len(auto)} títulos AUTO no fim | "
              f"cota total {sum(q.values())} -> {out / 'demanda.md'}")
    elif pre:
        dup = sum(1 for t in index.values() if pre.get(t, {}).get("dup"))
        print(f"[fotos] ordenadas pela nota do CLIP | {dup} quase-duplicatas (DUP) e {len(auto)} AUTO no fim de cada tag")


if __name__ == "__main__":
    main()
