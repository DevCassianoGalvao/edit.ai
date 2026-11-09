"""Amostra o MP4 FINAL (não a timeline): 1 quadro a cada PASSO s, em folhas de 6x8 -> qa/final_mp4.jpg (+ _NN.jpg).
É a última conferência antes da entrega: logos, texto queimado, grade, sobreposições — no arquivo que vai sair.
Uso: python final_mp4_sheet.py [out/final.mp4] [--passo 20]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
mp4 = ROOT / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "out/final.mp4")
passo = float(sys.argv[sys.argv.index("--passo") + 1]) if "--passo" in sys.argv else 20.0
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                           capture_output=True, text=True).stdout.strip())
TW, TH, COLS, ROWS = 320, 180, 6, 8
ts = [t for t in [i * passo + passo / 2 for i in range(int(dur // passo))] if t < dur]
with tempfile.TemporaryDirectory() as td:
    def _um(par):   # 04/10/2026: em paralelo (eram 108 ffmpeg em fila, 114 s)
        i, t = par
        p = Path(td) / f"{i:04d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", f"scale={TW}:{TH}", str(p)], check=True)
        return (t, p)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:
        tiles = [tp for tp in ex.map(_um, enumerate(ts)) if tp[1].exists()]   # 05/11: seek no fim do MP4 pode não gerar quadro
    por_folha = COLS * ROWS
    outs = []
    for k in range(0, len(tiles), por_folha):
        sheet = Image.new("RGB", (TW * COLS, (TH + 18) * ROWS), (16, 16, 16))
        d = ImageDraw.Draw(sheet)
        for j, (t, p) in enumerate(tiles[k:k + por_folha]):
            x, y = (j % COLS) * TW, (j // COLS) * (TH + 18)
            sheet.paste(Image.open(p), (x, y + 18))
            d.text((x + 4, y + 3), f"{int(t // 60):02d}:{int(t % 60):02d}", fill=(255, 220, 0))
        out = ROOT / "qa" / (f"final_mp4_{k // por_folha:02d}.jpg" if len(tiles) > por_folha else "final_mp4.jpg")
        sheet.save(out, quality=85)
        outs.append(out)
    if len(outs) > 1:  # também uma folha única resumida (1 quadro a cada 3 amostras) para o relatório
        sub = tiles[::3][:por_folha]
        sheet = Image.new("RGB", (TW * COLS, (TH + 18) * ROWS), (16, 16, 16))
        d = ImageDraw.Draw(sheet)
        for j, (t, p) in enumerate(sub):
            x, y = (j % COLS) * TW, (j // COLS) * (TH + 18)
            sheet.paste(Image.open(p), (x, y + 18))
            d.text((x + 4, y + 3), f"{int(t // 60):02d}:{int(t % 60):02d}", fill=(255, 220, 0))
        sheet.save(ROOT / "qa" / "final_mp4.jpg", quality=85)
print(f"[final_mp4] {len(ts)} quadros ({passo:.0f} s) de {mp4.name} -> {len(outs)} folha(s) em qa/")
