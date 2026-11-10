"""Fotos APROVADAS na folha -> public/stock/p<hash>.jpg (1920x1080, recorte cover) + clips.json (kind photo).

Entrada: data/photo_side.json {title: {"verdict": "ok"|"reject", "tags": [...], "focus": [fx, fy] opcional}}
  focus = centro do recorte em fração da imagem (padrão 0.5, 0.5)
Mescla clips.json com o disco. A foto sempre entra com movimento (push/pan) no Remotion.
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import hashlib, json
from pathlib import Path
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True   # 28/09: 1 download truncado derrubou o make_photos

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "public" / "stock"


def cover(im, fx, fy, W=1920, H=1080):
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * fx - W / 2)), im.width - W)
    y = min(max(0, round(im.height * fy - H / 2)), im.height - H)
    return im.crop((x, y, x + W, y + H))


def main():
    pool = json.loads((D / "photo_pool.json").read_text("utf-8"))
    side = json.loads((D / "photo_side.json").read_text("utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    # 24/09/2026: a folha agora é feita com miniatura; a foto cheia só existe depois do photo_dl --aprovadas
    faltam = [t for t, sd in side.items() if sd.get("verdict") == "ok" and t in pool
              and not (pool[t].get("file") and Path(pool[t]["file"]).exists())
              and not (OUT / f"p{hashlib.md5(t.encode()).hexdigest()[:8]}.jpg").exists()]
    if faltam:
        raise SystemExit(f"[fotos] {len(faltam)} aprovadas sem a foto cheia — rodar antes: python scripts/photo_dl.py --aprovadas")
    new = []
    # 04/11/2026 — estilo "Arquivo Colorizado": fotos de arquivo viram cópia impressa sobre fundo escuro/papel, com
    # etiqueta laranja, nome+cargo ou tag de capítulo (scripts/moldura.py; rótulos em data/moldura_rotulos.json)
    cfgp = D / "pipeline_config.json"
    mcfg = (json.loads(cfgp.read_text("utf-8")).get("moldura_fotos") or {}) if cfgp.exists() else {}
    if mcfg.get("ligado"):
        import moldura as MO
        rots = MO.rotulos()
    nm = {"escura": 0, "papel": 0, "capitulo": 0}
    for t, sd in side.items():
        if sd.get("verdict") != "ok":
            continue
        e = pool[t]
        cid = "p" + hashlib.md5(t.encode()).hexdigest()[:8]
        dst = OUT / f"{cid}.jpg"
        if mcfg.get("ligado"):
            rot = rots.get(t) or {}
            fx, fy = sd.get("focus", [0.5, 0.5])
            fonte = e.get("file") if e.get("file") and Path(e["file"]).exists() else None
            src = Image.open(fonte).convert("RGB") if fonte else None
            var = MO.decide(t, src, rot, float(mcfg.get("fracao", 0.45))) if src is not None else None
            if var:
                dm = OUT / f"{cid}{var[0]}.jpg"
                if not dm.exists():
                    MO.emoldura(src, var, rot.get("etiqueta"), rot.get("nome"), rot.get("cargo")).save(dm, quality=92)
                dst, nm[var] = dm, nm[var] + 1
            elif rot.get("capitulo") and src is not None:
                dm = OUT / f"{cid}c.jpg"
                if not dm.exists():
                    MO.capitulo(cover(src, fx, fy), *rot["capitulo"][:2]).save(dm, quality=92)
                dst, nm["capitulo"] = dm, nm["capitulo"] + 1
        if not dst.exists():
            fx, fy = sd.get("focus", [0.5, 0.5])
            cover(Image.open(e["file"]).convert("RGB"), fx, fy).save(dst, quality=92)
        new.append({"id": cid, "kind": "photo", "file": f"stock/{dst.name}", "dur": 10 ** 6, "tags": sd.get("tags", e["tags"]),
                    "source": f"cm:{t}", "era": sd.get("era", "modern"), "title": t, "url": e.get("descurl"),
                    "license": e.get("license"), "artist": e.get("artist"), "credit": e.get("credit")})
    p = D / "clips.json"
    disk = {c["id"]: c for c in json.loads(p.read_text("utf-8"))["clips"]} if p.exists() else {}
    for c in new:
        disk[c["id"]] = c
    # 25/09/2026: foto vetada DEPOIS de entrar na biblioteca (conferência, placa estrangeira) tem de SAIR — antes a
    # mescla só acrescentava e a Chery ucraniana vetada continuou no filme do Dolphin Mini
    fora = [k for k, c in disk.items() if c.get("kind") == "photo" and str(c.get("source", "")).startswith("cm:")
            and side.get(c["source"][3:], {}).get("verdict") == "reject"]
    for k in fora:
        disk.pop(k)
    if fora:
        print(f"[fotos] {len(fora)} vetadas saíram da biblioteca")
    p.write_text(json.dumps({"clips": sorted(disk.values(), key=lambda c: c["id"])}, ensure_ascii=False, indent=1), "utf-8")
    print(f"[fotos] {len(new)} aprovadas na biblioteca; total {len(disk)} clipes")
    if mcfg.get("ligado"):
        print(f"[fotos] moldura: {nm['escura']} em fundo escuro, {nm['papel']} em papel, {nm['capitulo']} com tag de capítulo")


if __name__ == "__main__":
    from trava import media   # 07/10/2026: render exclusivo (ver trava.py)
    with media("make_photos"):
        main()
