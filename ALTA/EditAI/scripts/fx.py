"""EFEITOS de edição do painel (28/09/2026) — TRANSIÇÕES nos cortes e TEXTURAS por cima, tudo no ffmpeg, dentro da
MESMA codificação final do acabamento.py (nada é recodificado duas vezes).

Pesquisa (painel, 28/09): punch-in / whip / glitch / flash / film burn / light leak são as transições de 2025-26;
poeira-e-riscos, VHS, scanlines, papel e luz vazada são as texturas; "pattern interrupt" a cada 30-60 s segura
retenção em documentário — é a frequência "ritmo" (~45 s).

TRANSIÇÕES (pipeline_config "transicao": {"tipo": ..., "freq": "capitulos" | "ritmo" | "todos"})
  seco    corte seco (padrão, nada muda)
  punch   zoom seco de 6 % nos 8 quadros depois do corte (punch-in, micro-movimento)
  flash   clarão branco de 5 quadros no corte
  whip    desfoque horizontal de chicote nos 6 quadros em volta do corte
  glitch  RGB separado e deslocado nos 6 quadros do corte
  queima  queima de película laranja (film burn) atravessando o corte
  luz     luz vazada suave (light leak) atravessando o corte
  fusao   respiro escuro suave de ~0,6 s no corte (imita a fusão lenta do documentário de arquivo, 04/11/2026)
TEXTURAS (pipeline_config "texturas": {"poeira": bool, "vhs": bool, "papel": bool, "luz_vazada": bool})
Os arquivos de textura são gerados uma vez em assets/fx/ (gerar_assets) e ficam em loop durante o filme.

Uso: python fx.py assets        # (re)gera assets/fx
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FX = ROOT / "assets" / "fx"
FPS = 30
TRANSICOES = ["seco", "punch", "flash", "whip", "glitch", "queima", "luz", "fusao", "flash_suave"]
TEXTURAS = ["poeira", "vhs", "papel", "luz_vazada", "grao_fino"]


def _ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *a], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"[fx] ffmpeg: {r.stderr[-400:]}")


def gerar_assets(forcar=False):
    FX.mkdir(parents=True, exist_ok=True)
    x264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p"]
    if forcar or not (FX / "poeira.mp4").exists():   # pontos de poeira + riscos verticais que piscam (5 s em loop)
        _ff("-f", "lavfi", "-i", "color=black:s=480x270:r=30:d=5", "-vf",
            "format=gray,geq=lum='if(gt(random(1)\\,0.9982)\\,255\\,0)',scale=1920:1080:flags=neighbor,gblur=sigma=1.1,"
            "drawbox=x='mod(floor(t*30)*397\\,1880)+20':y=0:w=2:h=ih:color=white@0.5:t=fill:enable='lt(mod(n\\,11)\\,2)',"
            "drawbox=x='mod(floor(t*30)*911\\,1880)+20':y=0:w=1:h=ih:color=white@0.35:t=fill:enable='lt(mod(n\\,17)\\,3)',format=yuv420p",
            *x264, str(FX / "poeira.mp4"))
    if forcar or not (FX / "luz.mp4").exists():      # manchas de luz alaranjada que passeiam (light leak, 8 s)
        blob = lambda cx, cy, s: f"exp(-((X-({cx}))*(X-({cx}))+(Y-({cy}))*(Y-({cy})))/{s})"
        a, b = blob("250+60*sin(T*0.8)", "40+30*cos(T*0.6)", 2600), blob("60+50*cos(T*0.5)", "150-30*sin(T*0.9)", 3600)
        _ff("-f", "lavfi", "-i", "color=black:s=320x180:r=30:d=8", "-vf",
            f"format=gbrp,geq=r='255*min(1\\,{a}+0.6*{b})':g='150*{a}+90*{b}':b='60*{a}+120*{b}',"
            "scale=1920:1080:flags=bicubic,gblur=sigma=30,format=yuv420p", *x264, str(FX / "luz.mp4"))
    if forcar or not (FX / "papel.png").exists():    # fibra de papel (multiplicar)
        _ff("-f", "lavfi", "-i", "color=black:s=480x270:d=1", "-frames:v", "1", "-vf",
            "format=gray,geq=lum='215+40*random(1)',scale=1920:1080:flags=bicubic,gblur=sigma=1.5,format=rgb24,"
            "colorchannelmixer=rr=1:gg=0.97:bb=0.9", str(FX / "papel.png"))
    if forcar or not (FX / "scanlines.png").exists():
        _ff("-f", "lavfi", "-i", "color=white:s=1920x1080:d=1", "-frames:v", "1", "-vf",
            "format=gray,geq=lum='if(mod(Y\\,4)\\,255\\,150)',format=rgb24", str(FX / "scanlines.png"))
    if forcar or not (FX / "queima.png").exists():   # queima de película: clarão laranja vindo do canto
        g = "exp(-((X-1500)*(X-1500)+(Y-260)*(Y-260))/260000)"
        _ff("-f", "lavfi", "-i", "color=black:s=1920x1080:d=1", "-frames:v", "1", "-vf",
            f"format=gbrp,geq=r='255*min(1\\,1.6*{g})':g='255*min(1\\,1.1*{g})*0.55':b='255*{g}*0.12',format=rgb24",
            str(FX / "queima.png"))
    print("[fx] assets ->", FX)


# ------------------------------------------------------------------ onde as transições caem
def cortes(timeline=None):
    p = timeline or (D / "timeline_renderizado.json" if (D / "timeline_renderizado.json").exists() else D / "timeline.json")
    items = json.loads(Path(p).read_text("utf-8"))["items"]
    return [it["from"] / FPS for it in items[1:] if it["from"] > 0]


def tempos(freq, caps, todos_cortes, periodo=45.0):
    """Instantes (s) das transições: nos capítulos, no ritmo (~1 a cada `periodo` s, no corte mais próximo) ou todos."""
    if freq == "todos":
        return list(todos_cortes)
    if freq == "ritmo":
        out, alvo = [], periodo
        for c in todos_cortes:
            if c >= alvo:
                out.append(c)
                alvo = c + periodo
        return sorted(set(out) | set(caps))
    return list(caps)


def _janelas(ts, antes, depois):
    return "+".join(f"between(t\\,{t - antes:.3f}\\,{t + depois:.3f})" for t in ts) or "0"


def flash_brilho(tipo, ts):
    """Termos para somar no eq=brightness do acabamento (o flash é só brilho)."""
    if tipo == "flash_suave":
        return [f"0.20*max(0\\,1-abs(t-{t:.3f})/0.12)" for t in ts]
    if tipo == "fusao":   # 04/11/2026 estilo Arquivo Colorizado: a imagem respira para o escuro e volta (~0,6 s)
        return [f"-0.30*max(0\\,1-abs(t-{t:.3f})/0.30)" for t in ts]
    return [f"0.55*max(0\\,1-abs(t-{t:.3f})/0.09)" for t in ts] if tipo == "flash" else []


DESLOC = 0.0   # 29/09/2026: início (s) do pedaço quando o acabamento roda em paralelo (acabamento.py)
_DUR = {}


def _dur(arq):
    if arq not in _DUR:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq],
                           capture_output=True, text=True, cwd=ROOT)
        try:
            _DUR[arq] = float(r.stdout.strip().rstrip(",")) or 1.0
        except ValueError:
            _DUR[arq] = 1.0
    return _DUR[arq]


def grafo(base, tipo, ts, texturas, final, fundos):
    """Monta o -filter_complex. base/final = cadeias do acabamento (antes e depois); fundos = lista de entradas extras
    que o chamador tem de passar ao ffmpeg (na ordem) como [(args...)]. Devolve (grafo, rotulo_saida)."""
    partes, cur, k = [f"[0:v]{base}[b0]"], "b0", 0
    n_in = 1

    def nxt():
        nonlocal k
        k += 1
        return f"b{k}"

    def entrada(args):
        nonlocal n_in
        fundos.append(args)
        n_in += 1
        if DESLOC > 0 and "-stream_loop" in args:   # 29/09: pedaço do acabamento paralelo — o loop segue de onde parou
            # (NÃO "-ss" na entrada: com -stream_loop o ffmpeg recomeça CADA volta no ponto do -ss e o loop sai de fase)
            off = DESLOC % _dur(args[args.index("-i") + 1])
            partes.append(f"[{n_in - 1}:v]trim=start={off:.4f},setpts=PTS-STARTPTS[lp{n_in - 1}]")
            return f"lp{n_in - 1}"
        return f"{n_in - 1}:v"

    ts = [t for t in ts if t > 0.5]
    if ts and tipo == "punch":
        e = _janelas(ts, 0, 8 / FPS)
        a, z, o = nxt(), nxt(), nxt()
        partes.append(f"[{cur}]split[{a}][{z}p];[{z}p]scale=2036:1146,crop=1920:1080[{z}];[{a}][{z}]overlay=enable='{e}'[{o}]")
        cur = o
    elif ts and tipo == "whip":
        o = nxt()
        partes.append(f"[{cur}]avgblur=sizeX=48:sizeY=1:enable='{_janelas(ts, 3 / FPS, 3 / FPS)}'[{o}]")
        cur = o
    elif ts and tipo == "glitch":
        o = nxt()
        partes.append(f"[{cur}]rgbashift=rh=16:bh=-16:gv=6:edge=wrap:enable='{_janelas(ts, 2 / FPS, 4 / FPS)}'[{o}]")
        cur = o
    elif ts and tipo in ("queima", "luz"):
        src = entrada(["-loop", "1", "-framerate", str(FPS), "-i", "assets/fx/queima.png"]) if tipo == "queima" else \
            entrada(["-stream_loop", "-1", "-i", "assets/fx/luz.mp4"])
        antes, depois, op = (5 / FPS, 8 / FPS, 0.85) if tipo == "queima" else (10 / FPS, 16 / FPS, 0.85)
        o = nxt()
        partes.append(f"[{cur}]format=gbrp[{o}a];[{src}]format=gbrp,scale=1920:1080[{o}b];"
                      f"[{o}a][{o}b]blend=all_mode=screen:all_opacity={op}:shortest=1:enable='{_janelas(ts, antes, depois)}'[{o}]")
        cur = o
    tx = texturas or {}
    if tx.get("grao_fino"):
        o = nxt()
        partes.append(f"[{cur}]noise=alls=3:allf=t[{o}]")
        cur = o
    if tx.get("vhs"):
        sl = entrada(["-loop", "1", "-framerate", str(FPS), "-i", "assets/fx/scanlines.png"])
        o = nxt()
        partes.append(f"[{cur}]rgbashift=rh=5:bh=-5,noise=alls=9:allf=t,format=gbrp[{o}a];[{sl}]format=gbrp[{o}b];"
                      f"[{o}a][{o}b]blend=all_mode=multiply:all_opacity=0.5:shortest=1[{o}]")
        cur = o
    if tx.get("papel"):
        pp = entrada(["-loop", "1", "-framerate", str(FPS), "-i", "assets/fx/papel.png"])
        o = nxt()
        partes.append(f"[{cur}]format=gbrp[{o}a];[{pp}]format=gbrp[{o}b];[{o}a][{o}b]blend=all_mode=multiply:all_opacity=0.45:shortest=1[{o}]")
        cur = o
    if tx.get("luz_vazada"):
        lz = entrada(["-stream_loop", "-1", "-i", "assets/fx/luz.mp4"])
        o = nxt()
        partes.append(f"[{cur}]format=gbrp[{o}a];[{lz}]format=gbrp[{o}b];[{o}a][{o}b]blend=all_mode=screen:all_opacity=0.42:shortest=1[{o}]")
        cur = o
    if tx.get("poeira"):
        po = entrada(["-stream_loop", "-1", "-i", "assets/fx/poeira.mp4"])
        o = nxt()
        partes.append(f"[{cur}]format=gbrp[{o}a];[{po}]format=gbrp[{o}b];[{o}a][{o}b]blend=all_mode=screen:all_opacity=0.5:shortest=1[{o}]")
        cur = o
    partes.append(f"[{cur}]{final}[vout]")
    return ";".join(partes), "vout"


if __name__ == "__main__":
    if sys.argv[1:2] == ["assets"]:
        gerar_assets(forcar=True)
    else:
        print(__doc__)
