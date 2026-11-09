"""Folha DENSA dos cortes de VÍDEO: N quadros da parte do clipe que o corte realmente usa (trimBefore..+dur),
direto pelo ffmpeg (não usa o Remotion — pode rodar durante o render). Pega entrevista/legenda queimada que a
folha de 1 quadro por corte não mostra.
29/09/2026: era 1 ffmpeg por quadro, em fila, refeito do zero a cada `fechar.py preparar` (Tibete: 30 min). Agora os
quadros saem em paralelo (8 de cada vez) e ficam em cache (qa/_dense_cache, chave = clipe + quadro): na 2ª volta
só o que mudou é extraído. Mesmos quadros, mesma folha.
Uso: python dense_cuts.py OUT.jpg [ids.json | --all] [--n 6]"""
import hashlib, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prefilter
ROOT = Path(__file__).resolve().parent.parent
TXT = "--sem-aviso-texto" not in sys.argv and prefilter.disponivel()
t = json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"]
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 6
ids = None if "--all" in sys.argv else set(json.loads(Path(sys.argv[2]).read_text("utf-8")))
cuts = [i for i in t if i["type"] == "cut" and i.get("kind") == "video" and (ids is None or i["id"] in ids)]
F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
TW, TH, PER = 320, 180, 30
out = Path(sys.argv[1])
CACHE = ROOT / "qa" / "_dense_cache"
CACHE.mkdir(parents=True, exist_ok=True)
IDX = CACHE / "texto.json"
flags = json.loads(IDX.read_text("utf-8")) if IDX.exists() else {}


def extrai(src, fr):
    """Miniatura do quadro `fr` do clipe (do cache se já extraída). Devolve (arquivo, chave)."""
    arq = ROOT / "public" / src
    chave = hashlib.md5(f"{src}|{arq.stat().st_mtime_ns if arq.exists() else 0}|{fr:.2f}|{TW}".encode()).hexdigest()
    jpg = CACHE / f"{chave}.jpg"
    if not jpg.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{fr / 30:.3f}", "-i", str(arq),
                        "-frames:v", "1", "-vf", f"scale={TW}:{TH}", str(jpg)])
    return jpg, chave


pedidos = [(it["src"], (it.get("trimBefore") or 0) + (it["dur"] - 1) * k / (N - 1)) for it in cuts for k in range(N)]
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda p: extrai(*p), pedidos))
for jpg, chave in res:   # aviso de texto: o CLIP roda aqui, em série, e só no que ainda não foi visto
    if TXT and chave not in flags and jpg.exists():
        flags[chave] = bool(prefilter.tem_texto(str(jpg))[0])
IDX.write_text(json.dumps(flags), "utf-8")
for pg in range(0, len(cuts), PER):
    ch = cuts[pg:pg + PER]
    W = Image.new("RGB", (TW * N, TH * len(ch)), "black"); d = ImageDraw.Draw(W)
    for r, it in enumerate(ch):
        for k in range(N):
            jpg, chave = res[(pg + r) * N + k]
            if jpg.exists():
                W.paste(Image.open(jpg), (k * TW, r * TH))
            if flags.get(chave):  # aviso de texto queimado no quadro
                d.rectangle([k * TW + TW - 46, r * TH + 4, k * TW + TW - 6, r * TH + 26], fill=(150, 0, 0))
                d.text((k * TW + TW - 42, r * TH + 5), "TXT", fill="white", font=F)
        d.text((4, r * TH + 2), f"{it['id']} {it['clip']} {it['from'] // 30}s", fill="yellow", font=F, stroke_width=2, stroke_fill="black")
    p = out.with_name(f"{out.stem}_{pg // PER:02d}.jpg"); W.save(p, quality=80); print(p)
