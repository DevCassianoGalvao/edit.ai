"""REVISÃO ANTES DO RENDER (10/10/2026, pedido do usuário: "vídeo em 2 h" e "fazer uma vez só").

A folha de cortes (qa/pre_render/cortes_*.jpg) mostra os clipes e as fotos, mas NÃO mostra como os cartões, mapas e
animações do Remotion ficam desenhados — foi assim que o rótulo cortado "Corea del S" do Prelude só apareceu depois do
render (2 renders a mais). Este script fotografa cada trecho do Remotion ANTES do render e monta as folhas
qa/pre_render/animacoes_*.jpg, que a revisora confere junto com a folha de cortes.

Quadros: 85 % de cada trecho (o texto já terminou de entrar); trecho longo (> 8 s) também na metade.
Uso: python scripts/stills_animacoes.py      (o fechar.py preparar já chama no fim)
"""
import json, shutil, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "qa" / "pre_render"
TMP = ROOT / "out" / "_stills"
COLS, ROWS, W, H = 4, 4, 480, 270


def fonte(t=22):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, t)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    from trava import media
    with media("fotos das animações (revisão antes do render)"):
        subprocess.run([sys.executable, "scripts/render_hybrid.py", "--plan-only"], cwd=ROOT, check=True,
                       capture_output=True)
        subprocess.run(["node", "scripts/bundle.mjs"], cwd=ROOT, check=True, capture_output=True)
        plan = json.loads((ROOT / "out" / "hybrid" / "plan.json").read_text("utf-8"))
        fps = plan.get("fps", 30)
        quadros = []
        for s in plan["segments"]:
            if s["engine"] != "remotion":
                continue
            a, b = s["start"], s["end"]
            n = b - a
            quadros.append(a + int(n * 0.85))
            if n > 8 * fps:
                quadros.append(a + n // 2)
        quadros = sorted(set(q for q in quadros if q < plan["durationInFrames"]))
        shutil.rmtree(TMP, ignore_errors=True)
        TMP.mkdir(parents=True)
        lista = TMP / "quadros.json"
        lista.write_text(json.dumps(quadros), "utf-8")
        r = subprocess.run(["node", "scripts/stills_animacoes.mjs", str(lista), str(TMP)], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        print("\n".join(l for l in r.stdout.splitlines() if l.strip())[-600:])
    # folhas
    for f in OUT.glob("animacoes_*.jpg"):
        f.unlink()
    fotos = sorted(TMP.glob("f*.jpg"))
    ft = fonte()
    por = COLS * ROWS
    for k in range(0, len(fotos), por):
        folha = Image.new("RGB", (COLS * W, ROWS * (H + 30)), (16, 16, 18))
        d = ImageDraw.Draw(folha)
        for j, f in enumerate(fotos[k:k + por]):
            q = int(f.stem[1:])
            x, y = (j % COLS) * W, (j // COLS) * (H + 30)
            folha.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y + 30))
            seg = q / fps
            d.text((x + 6, y + 4), f"#{k + j + 1}  {int(seg // 60)}:{seg % 60:04.1f}  quadro {q}", fill=(255, 210, 80), font=ft)
        folha.save(OUT / f"animacoes_{k // por:02d}.jpg", quality=85)
    print(f"[stills] {len(fotos)} fotos de animação -> {OUT}/animacoes_*.jpg")


if __name__ == "__main__":
    main()
