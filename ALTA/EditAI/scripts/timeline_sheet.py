"""Folha CORTE A CORTE do timeline ANTES do render — 1 quadro por item, com a tag e o título do arquivo.

24/09/2026: a folha que pegava o Itaú no filme do Banco do Brasil, o carro antigo no museu e a pedra com inscrição
em alemão era a do MP4 FINAL — cada achado custava um re-render. O plano já diz qual foto/clipe entra em cada
corte: dá para ver tudo antes de renderizar. Foto = o JPG 1920x1080 já recortado (public/stock); vídeo = o quadro
do meio do trecho usado; animação = cartela com o nome. O título do arquivo vai no rótulo (marca concorrente e
país errado costumam estar no nome).

A folha do MP4 final continua existindo como última conferência — mas passa a ser confirmação, não caça.

Com --mp4 out/final.mp4 a mesma folha sai do MP4 RENDERIZADO (quadro a 60 % de cada item, cartões e animações
por cima) — é a conferência final corte a corte.

Uso: python timeline_sheet.py [OUTDIR=qa/pre_render] [--stock public] [--mp4 out/final.mp4]
"""
import json, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
TW, TH, COLS, ROWS, LAB = 320, 180, 6, 8, 34
F1 = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
F2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
FA = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = ROOT / (args[0] if args else "qa/pre_render")
    stock = Path(sys.argv[sys.argv.index("--stock") + 1]) if "--stock" in sys.argv else ROOT / "public"
    out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("cortes_*.jpg"):
        p.unlink()
    items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    lib = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
    tmp = Path(tempfile.mkdtemp())
    mp4 = ROOT / sys.argv[sys.argv.index("--mp4") + 1] if "--mp4" in sys.argv else None

    def quadro(par):
        i, it = par
        im = Image.new("RGB", (TW, TH), (24, 26, 30))
        try:
            if mp4 is not None:
                p = tmp / f"{i:04d}.jpg"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(it['from'] + it['dur'] * 0.6) / FPS:.2f}",
                                "-i", str(mp4), "-frames:v", "1", "-vf", f"scale={TW}:{TH}", str(p)], check=True)
                im = Image.open(p).convert("RGB")
            elif it["type"] == "animation":
                d = ImageDraw.Draw(im)
                d.text((12, TH // 2 - 14), it.get("scene", "animação"), fill=(240, 200, 80), font=FA)
            elif it.get("kind") == "photo":
                im = Image.open(stock / it["src"]).convert("RGB").resize((TW, TH), Image.BILINEAR)
            else:
                t = (it.get("trimBefore") or 0) / FPS + it["dur"] * 0.5 / FPS
                p = tmp / f"{i:04d}.jpg"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(stock / it["src"]),
                                "-frames:v", "1", "-vf", f"scale={TW}:{TH}", str(p)], check=True)
                im = Image.open(p).convert("RGB")
        except Exception as ex:  # noqa: BLE001
            ImageDraw.Draw(im).text((8, 8), f"ERRO {ex!r}"[:40], fill=(255, 80, 80), font=F2)
        c = lib.get(it.get("clip") or "", {})
        tag = (c.get("tags") or [""])[0]
        ov = (it.get("ov") or {}).get("tipo", "")
        l1 = f"#{i} {it['from'] / FPS:.0f}s {it.get('kind') or 'anim'} {tag}" + (f" [{ov}]" if ov else "")
        titulo = (c.get("title") or c.get("channel") or "").replace("File:", "")
        return im, l1, titulo[:52]

    with ThreadPoolExecutor(4) as ex:
        tiles = list(ex.map(quadro, enumerate(items)))
    per = COLS * ROWS
    for k in range(0, len(tiles), per):
        sh = Image.new("RGB", (TW * COLS, (TH + LAB) * ROWS), (14, 14, 14))
        d = ImageDraw.Draw(sh)
        for j, (im, l1, l2) in enumerate(tiles[k:k + per]):
            x, y = (j % COLS) * TW, (j // COLS) * (TH + LAB)
            d.text((x + 3, y + 2), l1, fill=(255, 220, 60), font=F1)
            d.text((x + 3, y + 18), l2, fill=(200, 200, 200), font=F2)
            sh.paste(im, (x, y + LAB))
        p = out / f"cortes_{k // per:02d}.jpg"
        sh.save(p, quality=85)
        print("[pre_render]", p)
    print(f"[pre_render] {len(tiles)} itens em {(len(tiles) + per - 1) // per} folhas -> {out}")


if __name__ == "__main__":
    main()
