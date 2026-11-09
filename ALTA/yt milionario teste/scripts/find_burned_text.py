"""Caça LEGENDA QUEIMADA nos clipes que estão no filme (regra: nada de texto na tela).

A folha do filme amostra 1 quadro por corte e a legenda do vlog aparece só em parte do clipe
(qa/thumbs2: v878552a9 com "Average patrol is around 2-3 months" no rodapé). Aqui cada clipe é
amostrado em N quadros e recebe uma nota de "faixa de texto": bordas concentradas numa faixa
horizontal do rodapé/topo, com contraste forte, muito acima do resto do quadro.

Saída: data/burned_text.json {clip: nota} + qa/burned/sheet_NN.jpg com os piores para conferência.
Uso: python find_burned_text.py [N_quadros] [quantos_suspeitos]
"""
import json, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "qa" / "burned"
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 60


def band_score(im):
    """Nota = (densidade de bordas na faixa) / (densidade no resto) x contraste da faixa."""
    g = np.asarray(im.convert("L").resize((480, 270)), dtype=float)
    e = np.asarray(Image.fromarray(g.astype("uint8")).filter(ImageFilter.FIND_EDGES), dtype=float)
    best = 0.0
    for y0, y1 in ((200, 262), (8, 70)):  # rodapé e topo (onde legenda/cartela ficam)
        band = e[y0:y1, 48:432]
        rest = np.concatenate([e[:y0, :].ravel(), e[y1:, :].ravel()])
        if rest.mean() <= 0.01:
            continue
        gb = g[y0:y1, 48:432]
        contrast = (np.percentile(gb, 97) - np.percentile(gb, 40)) / 255.0
        rows = band.mean(axis=1)
        rowiness = rows.max() / (rows.mean() + 1e-6)  # legenda = poucas linhas muito "cheias"
        best = max(best, (band.mean() / rest.mean()) * contrast * min(rowiness, 6.0))
    return float(best)


def main():
    clips = {c["id"]: c for c in json.loads((ROOT / "data/clips.json").read_text("utf-8"))["clips"]}
    used = {it["clip"] for it in json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"] if it.get("clip")}
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_frames"
    tmp.mkdir(exist_ok=True)
    notes, worst = {}, []
    for n, cid in enumerate(sorted(used)):
        c = clips.get(cid)
        if not c or c["kind"] != "video":
            continue
        src = ROOT / "public" / c["file"]
        dur = c["dur"] / 30
        best, bestf = 0.0, None
        for k in range(N):
            f = tmp / f"{cid}_{k}.jpg"
            if not f.exists():
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss",
                                f"{dur * (0.05 + 0.9 * k / max(1, N - 1)):.2f}", "-i", str(src),
                                "-frames:v", "1", "-vf", "scale=640:360", str(f)], check=False)
            if not f.exists():
                continue
            s = band_score(Image.open(f))
            if s > best:
                best, bestf = s, f
        notes[cid] = round(best, 2)
        if bestf:
            worst.append((best, bestf, cid, c.get("source", "")))
        if (n + 1) % 50 == 0:
            print(f"[texto] {n + 1} clipes", flush=True)
    (ROOT / "data" / "burned_text.json").write_text(json.dumps(notes, indent=1), "utf-8")
    worst.sort(key=lambda r: -r[0])
    COLS, ROWS, TW, TH = 4, 3, 640, 360
    for i in range(0, min(TOP, len(worst)), COLS * ROWS):
        sheet = Image.new("RGB", (COLS * TW, ROWS * (TH + 22)), (12, 12, 12))
        d = ImageDraw.Draw(sheet)
        for j, (s, f, cid, srcname) in enumerate(worst[i:i + COLS * ROWS]):
            x, y = (j % COLS) * TW, (j // COLS) * (TH + 22)
            sheet.paste(Image.open(f).resize((TW, TH)), (x, y + 22))
            d.text((x + 6, y + 3), f"{cid} nota {s:.1f} {str(srcname)[:40]}", font=FONT, fill=(255, 220, 0))
        p = OUT / f"sheet_{i // (COLS * ROWS):02d}.jpg"
        sheet.save(p, quality=88)
        print("[texto]", p, flush=True)
    print(f"[texto] {len(notes)} clipes; piores: " + ", ".join(f"{c}={n}" for n, _, c, _ in worst[:8]))


if __name__ == "__main__":
    main()
