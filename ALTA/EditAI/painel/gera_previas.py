"""PRÉVIAS VISUAIS das opções do painel -> painel/previas/ — geradas pelos MESMOS filtros do filme.

Cor, textura, barras, nitidez e mergulho: scripts/acabamento.filtros() (a cadeia que o fechar.py render aplica).
Legendas: scripts/legendas.gera_ass() + libass (o mesmo .ass queimado no filme).
Cartões de arquivo e mapa: os renders reais do Remotion em out/demo_arquivo e out/exemplos.
Destaques: Remotion (painel/previas_destaque.mjs, composição DemoDestaques).
Som: trecho de uma faixa do data/music_pool.json e uma sequência de efeitos do data/sfx_pool.json.
Estilos prontos: a combinação inteira (cor + textura + barras + legenda) sobre a mesma imagem.

Uso: python painel/gera_previas.py [--sem-remotion] [--so estilos]   (idempotente; refaz tudo em ~1-2 min)
"""
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "painel"
OUT = HERE / "previas"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
from acabamento import filtros  # noqa: E402
from legendas import gera_ass, demo_words  # noqa: E402
import catalogo  # noqa: E402

BASE = "public/exemplos/trem.jpg"
BASE2 = "public/exemplos/yakutsk.jpg"
FRASE = "O maior navio do mundo deixou o estaleiro em 1979 e nunca mais voltou"
LIMPO = {"grao": 0, "vinheta": "off", "tremor": False}
MP4 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]


def ff(*a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *a], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        print("   ERRO ffmpeg:", r.stderr.strip()[-300:])
    return r.returncode == 0


def rel(p):
    return Path(p).relative_to(ROOT).as_posix()


def still(vf, saida, t=0.0, base=BASE):
    return ff("-loop", "1", "-t", f"{t + 0.5:.2f}", "-i", base, "-vf", f"{vf},scale=960:-2", "-ss", f"{t:.2f}",
              "-frames:v", "1", "-q:v", "3", rel(OUT / saida))


def legenda_ass(estilo, nome="_leg.ass"):
    p = OUT / nome
    p.write_text(gera_ass(demo_words(FRASE), estilo), "utf-8-sig")
    return rel(p)


def momento(estilo):   # instante do quadro: meio de um bloco, com uma palavra acesa no karaokê
    return {"karaoke": 0.2 + 3 * 0.32 + 0.1, "impacto": 0.55}.get(estilo, 1.6)


def legendas():
    still(filtros(LIMPO), "leg_off.jpg")
    for e in ["classica", "documentario", "karaoke", "caixa", "impacto", "minimal", "serifa"]:
        still(filtros(LIMPO, legenda_ass(e)), f"leg_{e}.jpg", momento(e))
        print("  legenda", e)


def cores():
    for tom in ["neutro", "quente", "frio", "cinema", "sepia", "pb"]:
        still(filtros({**LIMPO, "tom": tom}), f"cor_{tom}.jpg")
        print("  cor", tom)


def texturas():
    for o in next(g for g in catalogo.GUIAS if g["id"] == "textura")["opcoes"]:
        a = {"tom": "neutro", **o["config"]["acabamento"]}
        ff("-loop", "1", "-t", "3", "-framerate", "30", "-i", BASE, "-vf", f"{filtros(a)},scale=1280:-2",
           *MP4, rel(OUT / f"tex_{o['id']}.mp4"))
        still(filtros(a), f"tex_{o['id']}.jpg", 1.0)
        print("  textura", o["id"])


def transicoes():
    ff("-loop", "1", "-t", "1.4", "-framerate", "30", "-i", BASE, "-loop", "1", "-t", "1.6", "-framerate", "30", "-i", BASE2,
       "-filter_complex", f"[0:v][1:v]concat=n=2:v=1[c];[c]{filtros({**LIMPO, 'mergulho_capitulo': True}, caps=[1.4])},scale=960:-2[v]",
       "-map", "[v]", *MP4, rel(OUT / "tr_mergulho.mp4"))
    still(filtros({**LIMPO, "tom": "neutro"}), "tr_mergulho.jpg", base=BASE2)
    still(filtros({**LIMPO, "barras": True}, legenda_ass("classica")), "tr_barras.jpg", 1.6)
    ff("-i", BASE, "-filter_complex",
       "[0:v]crop=960:540:560:300,split[a][b];[b]unsharp=5:5:0.8:5:5:0[b2];[a]crop=480:540:0:0[l];[b2]crop=480:540:480:0[r];"
       "[l][r]hstack,drawbox=x=478:y=0:w=4:h=540:color=0xF0B43C:t=fill", "-frames:v", "1", "-q:v", "3", rel(OUT / "tr_nitidez.jpg"))
    print("  transições")


def cartoes():
    demos = list((ROOT / "out" / "demo_arquivo").glob("*.mp4")) + list((ROOT / "out" / "exemplos").glob("*.mp4"))
    for f in demos:
        nome = ("arq_" + f.stem[3:] if f.stem.startswith("Arq") else "ex_" + f.stem[2:]).lower()
        if (OUT / f"{nome}.mp4").exists():
            continue
        ff("-i", rel(f), "-t", "7", "-vf", "scale=640:-2", *MP4, rel(OUT / f"{nome}.mp4"))
        ff("-ss", "2.5", "-i", rel(f), "-frames:v", "1", "-vf", "scale=640:-2", "-q:v", "4", rel(OUT / f"{nome}.jpg"))
    print(f"  cartões: {len(demos)} demos")


def som():
    pool = json.loads((ROOT / "data" / "music_pool.json").read_text("utf-8"))
    faixa = next((v["file"] for v in pool.values() if v.get("clima") in ("tensao", "cama") and (ROOT / v["file"]).exists()), None)
    if faixa:
        ff("-ss", "8", "-t", "18", "-i", faixa, "-af", "afade=t=in:d=1,afade=t=out:st=15:d=3,loudnorm=I=-18",
           "-c:a", "libmp3lame", "-b:a", "128k", rel(OUT / "som_trilha.mp3"))
    sfx = json.loads((ROOT / "data" / "sfx_pool.json").read_text("utf-8"))
    pega = [next((v["file"] for v in sfx.values() if v["papel"] == p and (ROOT / v["file"]).exists()), None)
            for p in ("whoosh", "riser", "hit", "ambiencia")]
    pega = [p for p in pega if p]
    if pega:
        ins = sum([["-t", "4", "-i", p] for p in pega], [])
        filt = "".join(f"[{i}:a]aresample=44100,apad=pad_dur=0.6,atrim=0:4.6[a{i}];" for i in range(len(pega)))
        filt += "".join(f"[a{i}]" for i in range(len(pega))) + f"concat=n={len(pega)}:v=0:a=1,loudnorm=I=-18[o]"
        ff(*ins, "-filter_complex", filt, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "128k", rel(OUT / "som_sfx.mp3"))
    # voz limpa: 6 s da narração crua + os mesmos 6 s com o filtro do fila.py preparar (antes | depois)
    narr = next((p for p in ("input/audio.mp3", "public/audio.mp3") if (ROOT / p).exists()), None)
    if narr:
        ff("-ss", "20", "-t", "6", "-i", narr, "-ss", "20", "-t", "6", "-i", narr, "-filter_complex",
           "[1:a]highpass=f=70,afftdn=nr=10:nf=-40:tn=1,deesser=i=0.35[b];[0:a]apad=pad_dur=0.7[a];[a][b]concat=n=2:v=0:a=1,loudnorm=I=-18[o]",
           "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "128k", rel(OUT / "som_voz.mp3"))
    for nome, cor in (("som_trilha", "0xF0B43C"), ("som_sfx", "0xB18CFF"), ("som_voz", "0x5EA8FF")):
        if (OUT / f"{nome}.mp3").exists():
            ff("-i", rel(OUT / f"{nome}.mp3"), "-filter_complex",
               f"showwavespic=s=960x540:split_channels=0:colors={cor}:scale=sqrt,format=rgba[w];"
               f"color=c=0x101012:s=960x540[bg];[bg][w]overlay=format=auto", "-frames:v", "1", rel(OUT / f"{nome}.png"))
    print("  som:", "trilha" if faixa else "-", f"{len(pega)} efeitos", "+ voz" if narr else "")


def estilos():
    g = {x["id"]: x for x in catalogo.GUIAS}
    for p in catalogo.PRONTOS:
        cfg = catalogo.config_de(p["escolhas"], p["liga"])
        leg = (cfg.get("legendas") or {}).get("estilo", "off")
        ass = legenda_ass(leg, f"_leg_{p['id']}.ass") if leg != "off" else None
        if any((cfg.get("texturas") or {}).values()):   # com textura: mesma cadeia do filme (acabamento.comando)
            import acabamento, fx
            fx.gerar_assets()
            args, _ = acabamento.comando(["-loop", "1", "-t", "3", "-framerate", "30", "-i", BASE], cfg.get("acabamento"),
                                         ass, (), None, cfg.get("texturas"))
            vmap = [] if "-filter_complex" in args else ["-map", "0:v:0"]
            ff(*args, *vmap, "-ss", f"{momento(leg):.2f}", "-frames:v", "1", "-q:v", "3", rel(OUT / "_est.jpg"))
            ff("-i", rel(OUT / "_est.jpg"), "-vf", "scale=960:-2", "-q:v", "3", rel(OUT / f"estilo_{p['id']}.jpg"))
            (OUT / "_est.jpg").unlink(missing_ok=True)
        else:
            still(filtros(cfg.get("acabamento"), ass), f"estilo_{p['id']}.jpg", momento(leg))
        print("  estilo", p["id"])
    _ = g


def efeitos():
    """Transições (2 fotos com um corte em 2 s) e texturas (3 s) pelo MESMO acabamento.comando() do filme."""
    import acabamento, fx
    fx.gerar_assets()
    tmp = OUT / "_base_corte.mp4"
    ff("-loop", "1", "-t", "2", "-framerate", "30", "-i", BASE, "-loop", "1", "-t", "2", "-framerate", "30", "-i", BASE2,
       "-filter_complex", "[0:v]scale=1920:1080,setsar=1[a];[1:v]scale=1920:1080,setsar=1[b];[a][b]concat=n=2:v=1[v]",
       "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", rel(tmp))
    base3 = OUT / "_base_tex.mp4"
    ff("-loop", "1", "-t", "3", "-framerate", "30", "-i", BASE, "-vf", "scale=1920:1080,setsar=1", "-c:v", "libx264",
       "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", rel(base3))
    def roda(src, saida, tr=None, tx=None, cortes=()):
        args, _ = acabamento.comando(["-i", rel(src)], {**LIMPO}, None, (), tr, tx, cortes)
        grande = OUT / "_fx_tmp.mp4"
        vmap = [] if "-filter_complex" in args else ["-map", "0:v:0"]
        ok = ff(*args, *vmap, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-an", rel(grande))
        if ok:
            ff("-i", rel(grande), "-vf", "scale=960:-2", *MP4, rel(OUT / saida))
            ff("-ss", "2.05" if cortes else "1.5", "-i", rel(grande), "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "3",
               rel(OUT / saida.replace(".mp4", ".jpg")))
        return ok
    for t in fx.TRANSICOES:
        print("  transição", t, "ok" if roda(tmp, f"trc_{t}.mp4", {"tipo": t, "freq": "todos"}, None, [2.0]) else "FALHOU")
    for t in fx.TEXTURAS:
        print("  textura", t, "ok" if roda(base3, f"txt_{t}.mp4", None, {t: True}) else "FALHOU")
    for f in (tmp, base3, OUT / "_fx_tmp.mp4"):
        f.unlink(missing_ok=True)


def destaques():
    demo = ROOT / "public" / "demo"
    demo.mkdir(exist_ok=True)
    if not (demo / "trem.jpg").exists():
        shutil.copy2(ROOT / BASE, demo / "trem.jpg")
    r = subprocess.run(["node", "painel/previas_destaque.mjs"], cwd=ROOT, capture_output=True, text=True)
    print("  destaques:", "ok" if r.returncode == 0 else "FALHOU " + (r.stderr or r.stdout)[-300:])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    so = sys.argv[sys.argv.index("--so") + 1] if "--so" in sys.argv else None
    etapas = {"legendas": legendas, "cores": cores, "texturas": texturas, "transicoes": transicoes, "cartoes": cartoes,
              "som": som, "estilos": estilos, "efeitos": efeitos}
    for k, fn in etapas.items():
        if not so or so == k:
            fn()
    if (not so or so == "destaques") and "--sem-remotion" not in sys.argv:
        destaques()
    for f in OUT.glob("_leg*.ass"):
        f.unlink()
    print("[previas] pronto ->", OUT)


if __name__ == "__main__":
    main()
