"""RASCUNHO 720p do filme em poucos minutos — direto do data/timeline.json, sem Remotion (27/09/2026, painel).

Serve para assistir o ritmo e as imagens (no celular, inclusive) ANTES de gastar o render final:
  vídeo  = o trecho certo do clipe (public/stock), foto = a foto parada, animação = cartela roxa com o nome da cena,
  cartão = etiqueta no rodapé com o tipo ("[quadro]", "[ficha]"...), + a narração (ou o master com trilha, se houver).
Cada item é cortado com o número exato de quadros (-frames:v), então o tempo bate com o filme final.
Saída: out/rascunho.mp4 (+ out/rascunho/ com os pedaços, refeitos só se o item mudar).

Uso: python rascunho.py [--workers 3]
"""
import hashlib, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
OUT = ROOT / "out" / "rascunho"
FPS = 30
W, H = 1280, 720
ENC = ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
FONTE = "public/fonts/Anton.ttf"


def txt(s):
    return re.sub(r"[^A-Za-z0-9 \-]", "", s or "")[:40]


def pedaco(par):
    i, it = par
    chave = hashlib.md5(json.dumps(it, sort_keys=True).encode()).hexdigest()[:10]
    f = OUT / f"{i:04d}_{chave}.mp4"
    if f.exists():
        return f
    n = it["dur"]
    etq = ""
    if (it.get("ov") or {}).get("tipo"):
        etq = (f",drawbox=x=40:y=ih-92:w=360:h=52:color=0xECE3CF@0.92:t=fill,"
               f"drawtext=fontfile={FONTE}:text='[{txt(it['ov']['tipo'])}]':fontcolor=0x2B2418:fontsize=34:x=56:y=h-84")
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    if it["type"] == "animation":
        cmd = ["-f", "lavfi", "-i", f"color=c=0x1d1530:s={W}x{H}:r={FPS}", "-vf",
               f"drawtext=fontfile={FONTE}:text='{txt(it.get('scene') or 'animacao')}':fontcolor=0xD9CDFA:fontsize=78:"
               f"x=(w-tw)/2:y=(h-th)/2,drawtext=fontfile={FONTE}:text='ANIMACAO REMOTION':fontcolor=0xB18CFF:fontsize=26:"
               f"x=(w-tw)/2:y=(h-th)/2-90{etq}"]
    elif it.get("kind") == "photo":
        cmd = ["-loop", "1", "-framerate", str(FPS), "-i", str(ROOT / "public" / it["src"]), "-vf", base + etq]
    else:
        cmd = ["-ss", f"{(it.get('trimBefore') or 0) / FPS:.3f}", "-i", str(ROOT / "public" / it["src"]), "-vf", f"fps={FPS}," + base + etq]
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *cmd, "-frames:v", str(n), *ENC, str(f)],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode or not f.exists():   # arquivo sumiu/corrompido: tela cinza com o aviso, o tempo continua certo
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x333333:s={W}x{H}:r={FPS}",
                        "-vf", f"drawtext=fontfile={FONTE}:text='FALTA {txt(it.get('src'))}':fontcolor=white:fontsize=40:x=40:y=40",
                        "-frames:v", str(n), *ENC, str(f)], cwd=ROOT)
    return f


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    nw = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 3
    with ThreadPoolExecutor(nw) as ex:
        feitos = list(ex.map(pedaco, enumerate(items)))
    validos = {p.name for p in feitos}
    for p in OUT.glob("*.mp4"):
        if p.name not in validos:
            p.unlink()
    lst = OUT / "lista.txt"
    lst.write_text("\n".join(f"file '{p.as_posix()}'" for p in feitos), "utf-8")
    master = ROOT / "public" / "final_audio.m4a"
    narr = ROOT / "public" / "audio.mp3"
    audio = master if master.exists() and master.stat().st_mtime > narr.stat().st_mtime else narr
    saida = ROOT / "out" / "rascunho.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
                    "-movflags", "+faststart", str(saida)], check=True)
    mb = saida.stat().st_size / 1e6
    print(f"[rascunho] {len(items)} itens -> out/rascunho.mp4 ({mb:.0f} MB, áudio: {audio.name})")


if __name__ == "__main__":
    main()
