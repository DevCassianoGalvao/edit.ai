"""12/10 (Jaguar pl): paralaxe.py pega as 8 PRIMEIRAS fotos do timeline -> todas nos 2 primeiros minutos e o build só usa 1
(gap de 45 s). Este recorta fotos ESPALHADAS (1 por janela de 5 min) com o mesmo critério e soma ao data/paralaxe.json."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
ALVOS = [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "200,480,760,1040,1320").split(",")]


def main():
    from rembg import new_session, remove
    sess = new_session("isnet-general-use")
    items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    fotos = [it for it in items if it.get("type") == "cut" and it.get("kind") == "photo" and not it.get("ov")]
    plx = json.loads((D / "paralaxe.json").read_text("utf-8"))
    for t0 in ALVOS:
        cands = [it for it in fotos if t0 <= it["from"] / 30 < t0 + 150 and it["src"] not in plx][:5]
        for it in cands:
            s = it["src"]
            im = Image.open(ROOT / "public" / s).convert("RGB")
            m = np.asarray(remove(im, session=sess, only_mask=True)).astype(np.float32) / 255.0
            a = m > 0.5
            cob = a.mean()
            lat = a[:, :8].mean() > 0.25 and a[:, -8:].mean() > 0.25
            cols = a.any(axis=0)
            maior, run = 0, 0
            for c in cols:
                run = run + 1 if c else 0
                maior = max(maior, run)
            ok = 0.06 <= cob <= 0.55 and not lat and maior / max(1, cols.sum()) > 0.7
            print(f"[plx] {t0}s {s} {cob:.0%} {'OK' if ok else '-'}", flush=True)
            if ok:
                fg = s.replace(".jpg", "_fg.png")
                Image.fromarray(np.dstack([np.asarray(im), (m * 255).astype(np.uint8)]), "RGBA").save(ROOT / "public" / fg)
                plx[s] = fg
                break
    (D / "paralaxe.json").write_text(json.dumps(plx, ensure_ascii=False, indent=1), "utf-8")
    th = []
    for s, fg in plx.items():
        a = Image.open(ROOT / "public" / s).convert("RGB").resize((480, 270))
        b = Image.new("RGB", (480, 270), (255, 0, 255))
        f = Image.open(ROOT / "public" / fg).resize((480, 270))
        b.paste(f, (0, 0), f)
        th += [a, b]
    W = Image.new("RGB", (1920, 270 * ((len(th) + 3) // 4)))
    for i, x in enumerate(th):
        W.paste(x, ((i % 4) * 480, (i // 4) * 270))
    W.save(ROOT / "qa" / "paralaxe.jpg", quality=85)
    print(f"[plx] {len(plx)} no paralaxe.json -> qa/paralaxe.jpg")


if __name__ == "__main__":
    main()
