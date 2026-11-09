"""PARALAXE 2.5D (REGRA do usuário, 26/09/2026): recorta o sujeito das fotos do plano para o corte em duas camadas.

Para cada corte de FOTO do data/timeline.json (sem gráfico em cima), o rembg (modelo isnet-general-use, CPU) separa o
sujeito do fundo. Fica só a foto em que o recorte é bom para o efeito:
  - sujeito entre 6 % e 55 % da tela (pouco = nada se mexe; muito = a foto inteira vira "recorte")
  - uma mancha principal (mais de 70 % do recorte numa peça só) e sem encostar nas duas laterais (sujeito cortado)
Grava public/stock/<id>_fg.png (RGBA 1920x1080, mesmo enquadramento) e data/paralaxe.json {src: fg}.
O build_overlays.py põe o ov "paralaxe" nas melhores, uma a cada 45 s (src/scenes/arquivo2.tsx -> Paralaxe).

Uso: python scripts/paralaxe.py [--max 40] [--folha]     (--folha: qa/paralaxe.jpg com os recortes aceitos)
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
# 12/10/2026 modo enxuto: o filme usa no máx. 5 fotos em 2.5D — recortar 8 basta (eram 40, ~1 min de CPU cada)
_ENX = json.loads((Path(__file__).resolve().parent.parent / "data" / "pipeline_config.json").read_text("utf-8")).get("enxuto", True) is not False
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else (8 if _ENX else 40)


def main():
    from rembg import new_session, remove
    sess = new_session("isnet-general-use")
    # fotos do plano (timeline) quando já existe; antes do plano, todas as fotos aprovadas da biblioteca (clips.json)
    fotos, vistos, quando = [], set(), {}
    if (D / "timeline.json").exists():
        for it in json.loads((D / "timeline.json").read_text("utf-8"))["items"]:
            if it.get("type") == "cut" and it.get("kind") == "photo" and not it.get("ov") and it["src"] not in vistos:
                vistos.add(it["src"])
                fotos.append(it["src"])
                quando[it["src"]] = it.get("from", 0) / 30
    else:
        c = json.loads((D / "clips.json").read_text("utf-8"))
        for x in (c if isinstance(c, list) else c.get("clips", list(c.values()))):
            f = x.get("file", "")
            if f.startswith("stock/p") and f.endswith(".jpg") and f not in vistos:
                vistos.add(f)
                fotos.append(f)
    antigo = json.loads((D / "paralaxe.json").read_text("utf-8")) if (D / "paralaxe.json").exists() else {}
    aceitos, notas = {}, []
    # 12/10/2026 (Jaguar fr): as 8 recortadas caíam todas nos 3 primeiros min e o build_overlays (1 a cada 45 s) só usava 1
    # -> com timeline, espalhar: no mínimo duração/(MAX+1) entre duas fotos aceitas
    passo = (max(quando.values()) / (MAX + 1)) if quando else 0
    ult = -1e9
    for i, s in enumerate(fotos):
        if len(aceitos) >= MAX:
            break
        if quando and quando.get(s, 0) - ult < passo:
            continue
        fg_rel = s.replace(".jpg", "_fg.png")
        if s in antigo and (ROOT / "public" / fg_rel).exists():
            aceitos[s] = fg_rel
            ult = quando.get(s, 0)
            continue
        im = Image.open(ROOT / "public" / s).convert("RGB")
        m = np.asarray(remove(im, session=sess, only_mask=True)).astype(np.float32) / 255.0
        a = m > 0.5
        cob = a.mean()
        lat = a[:, :8].mean() > 0.25 and a[:, -8:].mean() > 0.25
        # mancha principal: fração do recorte na maior coluna contínua (aproximação barata sem scipy)
        cols = a.any(axis=0)
        maior, run = 0, 0
        for c in cols:
            run = run + 1 if c else 0
            maior = max(maior, run)
        compacto = maior / max(1, cols.sum())
        ok = 0.06 <= cob <= 0.55 and not lat and compacto > 0.7
        notas.append((s, round(float(cob), 3), ok))
        if ok:
            rgba = np.dstack([np.asarray(im), (m * 255).astype(np.uint8)])
            Image.fromarray(rgba, "RGBA").save(ROOT / "public" / fg_rel)
            aceitos[s] = fg_rel
            ult = quando.get(s, 0)
        print(f"[paralaxe] {i + 1}/{len(fotos)} {s} sujeito {cob:.0%} {'OK' if ok else '-'}", flush=True)
    (D / "paralaxe.json").write_text(json.dumps(aceitos, ensure_ascii=False, indent=1), "utf-8")
    print(f"[paralaxe] {len(aceitos)} fotos com recorte bom -> data/paralaxe.json")
    if "--folha" in sys.argv and aceitos:
        th = []
        for s, fg in list(aceitos.items())[:24]:
            bg = Image.open(ROOT / "public" / s).convert("RGB").resize((480, 270))
            f = Image.open(ROOT / "public" / fg).resize((480, 270))
            cx = Image.new("RGB", (480, 270), (255, 0, 255))
            cx.paste(f, (0, 0), f)
            par = Image.new("RGB", (960, 270))
            par.paste(bg, (0, 0))
            par.paste(cx, (480, 0))
            th.append(par)
        folha = Image.new("RGB", (1920, 270 * ((len(th) + 1) // 2)), (20, 20, 20))
        for k, t in enumerate(th):
            folha.paste(t, ((k % 2) * 960, (k // 2) * 270))
        (ROOT / "qa").mkdir(exist_ok=True)
        folha.save(ROOT / "qa" / "paralaxe.jpg", quality=85)
        print("[paralaxe] folha -> qa/paralaxe.jpg")


if __name__ == "__main__":
    from trava import media   # 07/10/2026: render exclusivo (ver trava.py)
    with media("paralaxe"):
        main()
