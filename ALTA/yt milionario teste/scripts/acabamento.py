"""ACABAMENTO de filme de arquivo — passada final sobre out/final.mp4 (REGRA do usuário, 26/09/2026, para TODO filme).

O mesmo tratamento em tudo (foto do ffmpeg, vídeo, cartões e animações do Remotion), para o filme parecer uma peça só:
  - tom por época (pipeline_config "acabamento.tom"): "neutro" (tema atual), "sepia" (até ~1950), "pb" (guerra, arquivo),
    "frio" (Guerra Fria, soviético, industrial); 27/09 (painel): "quente" (pôr do sol, deserto, história) e "cinema"
    (sombras azuladas + luz alaranjada, look de trailer)
  - grão de filme temporal (noise), vinheta e uma respiração leve de brilho (tremulação de projetor)
27/09/2026 — opções do PAINEL (painel/, guias visuais), todas na MESMA codificação final (nada é recodificado 2x):
  - "nitidez": 0 | 0.4 | 0.8     unsharp leve — devolve definição a stock 1080p que chegou amaciado
  - "barras": true               barras de cinema ~2,18:1 (100 px em cima e embaixo; 138 px cobria os destaques do canto)
  - "mergulho_capitulo": true    mergulho curto no preto (0,5 s) em cada troca de capítulo — respiro de documentário
  - "grao": 0 desliga o grão; "vinheta": "off" desliga a vinheta
  - legendas (pipeline_config "legendas.estilo" != "off") queimadas por cima de tudo (scripts/legendas.py);
    o out/legendas.srt para o YouTube sai SEMPRE
  - nível de render (pipeline_config "render.qualidade": alta | media | rapida) escolhe o codificador final
Áudio copiado sem recodificar; confere quadros e duração antes de trocar o arquivo.
A função filtros() é a MESMA que o painel usa para gerar as prévias (painel/gera_previas.py): o que se vê lá é o que sai.

Uso: python scripts/acabamento.py [--in out/final.mp4]
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

# 27/09/2026: com o qp fixo dos segmentos (constqp 18) o grão virava 84 Mbps — 15 GB para 25 min (Tesla, Wi-Fi).
# Aqui é a codificação FINAL: taxa com teto (VBR ~12 Mbps, máx. 18), o grão continua visível e o arquivo fica ~2,3 GB.
_COMUM = ["-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
# 09/10/2026: p4 no lugar do p6 — mesma qualidade medida (SSIM 0,8270 x 0,8269 contra sem perda, mesmo tamanho; o teto de
# 12 Mbps é quem manda) e o NVENC deixa de ser o gargalo do acabamento na placa (134 -> 233 quadros/s com 4 pedaços)
NVENC_Q = {"alta": ("p4", "23"), "media": ("p4", "24"), "rapida": ("p3", "25")}
X264_Q = {"alta": ("medium", "20"), "media": ("fast", "21"), "rapida": ("veryfast", "22")}


def enc(qualidade="alta"):
    from render_hybrid import _tem_nvenc
    q = qualidade if qualidade in NVENC_Q else "alta"
    if _tem_nvenc():
        p, cq = NVENC_Q[q]
        return ["-c:v", "h264_nvenc", "-preset", p, "-tune", "hq", "-rc", "vbr", "-cq", cq, "-b:v", "12M",
                "-maxrate", "18M", "-bufsize", "36M"] + _COMUM
    p, crf = X264_Q[q]
    return ["-c:v", "libx264", "-preset", p, "-crf", crf, "-maxrate", "18M", "-bufsize", "36M"] + _COMUM


TONS = {
    "editai_noite": "eq=contrast=1.12:saturation=0.85,colorbalance=rs=-0.04:gs=0.01:bs=0.08:rm=0.04:bm=0.06",
    "editai_oceano": "eq=contrast=1.08:saturation=0.82,colorbalance=rs=-0.08:gs=0.04:bs=0.08:rh=-0.02:gh=0.03:bh=0.03",
    "editorial": "eq=contrast=1.06:saturation=0.78:brightness=0.02",
    "dourado": "eq=contrast=1.09:saturation=0.82,colorbalance=rs=0.04:bs=-0.04:rm=0.06:gm=0.02:bm=-0.04",
    "neutro": "eq=contrast=1.05:saturation=0.9",
    "sepia": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,eq=contrast=1.06",
    "pb": "hue=s=0,eq=contrast=1.12",
    "frio": "eq=contrast=1.08:saturation=0.72,colorbalance=rs=-0.06:bs=0.08:rh=-0.03:bh=0.04",
    "quente": "eq=contrast=1.07:saturation=0.98,colorbalance=rs=0.07:bs=-0.08:rm=0.07:gm=0.02:bm=-0.07:rh=0.05:bh=-0.06",
    "cinema": "eq=contrast=1.12:saturation=0.92,colorbalance=rs=-0.10:gs=0.02:bs=0.14:rm=0.03:bm=-0.02:rh=0.11:gh=0.03:bh=-0.10",
}
PADRAO = {"tom": "neutro", "grao": 5, "vinheta": "PI/5", "tremor": True, "nitidez": 0, "barras": False,
          "mergulho_capitulo": False}
BARRA = 100   # 28/09: era 138 (2,39:1) e cobria número/destaque do canto (área segura = 10 % = 108 px); 100 px -> ~2,18:1


def config():
    return json.loads((D / "pipeline_config.json").read_text("utf-8")) if (D / "pipeline_config.json").exists() else {}


# 09/10/2026 — ACABAMENTO NA PLACA (OpenCL, NVIDIA): nitidez (unsharp_opencl) e vinheta (kernel data/_vinheta.cl, mesma
# fórmula do vf_vignette) saem do processador. Medido: imagem SSIM 0,997 / PSNR 52,5 dB contra o processador; 4 pedaços
# 129 -> 233 quadros/s (com NVENC p4) e CPU 89 % -> 58 % na mesma velocidade. Cor e grão (baratos) continuam no processador.
# Sem OpenCL ou com pipeline_config "acabamento_gpu": false -> processador, como antes. As prévias do painel não mudam.
HW = ["-init_hw_device", "opencl=gpu:0.0", "-filter_hw_device", "gpu"]
_OPENCL = []


def tem_opencl():
    if not _OPENCL:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", *HW, "-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.2",
                            "-vf", "format=yuv420p,hwupload,unsharp_opencl,hwdownload,format=yuv420p", "-f", "null", "-"],
                           capture_output=True, text=True)
        _OPENCL.append(r.returncode == 0)
    return _OPENCL[0]


KERNEL = r"""
#define W 1920
#define H 1080
#define ANG {ang}f
__constant sampler_t smp = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
__kernel void vinheta(__write_only image2d_t dst, unsigned int index, __read_only image2d_t src)
{{
    int2 p = (int2)(get_global_id(0), get_global_id(1));
    int2 d = get_image_dim(dst);
    if (p.x >= d.x || p.y >= d.y) return;
    int croma = d.x < W;
    int lx = croma ? p.x * 2 : p.x;
    int ly = croma ? p.y * 2 : p.y;
    float xx = (float)(lx - W / 2);
    float yy = (float)(ly - H / 2);
    float dmax = sqrt((float)(W / 2) * (W / 2) + (float)(H / 2) * (H / 2));
    float dn = sqrt(xx * xx + yy * yy) / dmax;
    float f = 0.0f;
    if (dn <= 1.0f) {{ float c = cos(ANG * dn); f = (c * c) * (c * c); }}
    float v = read_imagef(src, smp, p).x * 255.0f;
    float o = croma ? (v - 127.0f) * f + 127.0f : v * f;
    o = clamp(floor(o + 0.5f), 0.0f, 255.0f) / 255.0f;
    write_imagef(dst, p, (float4)(o, 0.0f, 0.0f, 1.0f));
}}
"""


def _angulo(txt):
    import math
    s = str(txt).replace(" ", "")
    if not all(ch in "PI0123456789./*" for ch in s):
        raise ValueError(f"vinheta estranha: {txt}")
    return float(eval(s.replace("PI", repr(math.pi)), {"__builtins__": {}}))   # só número, PI, / e *


def kernel_vinheta(angulo):
    k = D / "_vinheta.cl"
    k.write_text(KERNEL.format(ang=repr(_angulo(angulo))), "utf-8")
    return "data/_vinheta.cl"   # relativo à pasta do filme (o ffmpeg roda com cwd = ROOT)


def capitulos():
    """Segundos de cada troca de capítulo (beats com "capitulo"), menos a abertura."""
    try:
        bj = json.loads((D / "beats.json").read_text("utf-8"))
        paras = json.loads((D / "master_transcript.json").read_text("utf-8"))["paragraphs"]
        return [paras[b["para"]]["startSec"] for b in bj["beats"] if b.get("capitulo") and paras[b["para"]]["startSec"] > 2]
    except Exception:  # noqa: BLE001
        return []


def partes(a, legendas_ass=None, caps=(), extra_brilho=(), desloc=0.0, gpu=False):
    """(base, final) da cadeia: base = cor, nitidez, vinheta, grão e brilho; final = barras, legendas e formato.
    As transições e texturas do fx.py entram ENTRE as duas (28/09/2026).
    desloc (29/09/2026): início do pedaço no acabamento paralelo — o tempo de tremor e legenda continua o do filme."""
    a = {**PADRAO, **(a or {})}
    if a.get("leve"):   # 07/10/2026: "acabamento leve" — sem grão temporal e sem tremor (as partes caras); tom e vinheta ficam
        a["grao"], a["tremor"] = 0, False
    f, g = [], []
    if not a.get("desligado"):
        f.append(TONS.get(a["tom"], TONS["neutro"]))
        nit = float(a.get("nitidez") or 0) > 0
        vin = bool(a.get("vinheta")) and a["vinheta"] != "off"
        if gpu and (nit or vin):   # 09/10/2026: na placa (mesma ordem: nitidez, depois vinheta)
            hw = ["format=yuv420p", "hwupload"]
            if nit:
                hw.append(f"unsharp_opencl=lx=5:ly=5:la={float(a['nitidez']):.2f}:cx=5:cy=5:ca=0")
            if vin:
                hw.append(f"program_opencl=source={kernel_vinheta(a['vinheta'])}:kernel=vinheta")
            f.append(",".join(hw + ["hwdownload", "format=yuv420p"]))
        else:
            if nit:
                f.append(f"unsharp=5:5:{float(a['nitidez']):.2f}:5:5:0")
            if vin:
                f.append(f"vignette=angle={a['vinheta']}")
        if int(a.get("grao") or 0) > 0:
            f.append(f"noise=alls={int(a['grao'])}:allf=t")
        br = list(extra_brilho)
        if a.get("tremor"):
            br.append(f"0.012*sin(2*PI*(t+{desloc:.3f})*0.9)+0.006*sin(2*PI*(t+{desloc:.3f})*3.7)")
        if a.get("mergulho_capitulo") and caps:
            br += [f"-0.9*max(0,1-abs(t-{c:.2f})/0.25)" for c in caps]
        if br:
            f.append(f"eq=brightness='{'+'.join(br)}':eval=frame")
        if a.get("barras"):
            g.append(f"drawbox=x=0:y=0:w=iw:h={BARRA}:color=black:t=fill,drawbox=x=0:y=ih-{BARRA}:w=iw:h={BARRA}:color=black:t=fill")
        elif a.get("barras_sutis"):
            g.append("drawbox=x=0:y=0:w=iw:h=48:color=black:t=fill,drawbox=x=0:y=ih-48:w=iw:h=48:color=black:t=fill")
    if legendas_ass:   # no pedaço, a legenda lê o tempo do filme (desloca e volta)
        g.append((f"setpts=PTS+{desloc:.3f}/TB," if desloc else "") + f"ass={legendas_ass}:fontsdir=public/fonts"
                 + (",setpts=PTS-STARTPTS" if desloc else ""))
    g.append("format=yuv420p")
    return ",".join(f) or "null", ",".join(g)


def filtros(a, legendas_ass=None, caps=()):
    """Cadeia do ffmpeg (-vf) para o dicionário de acabamento `a`. Mesma cadeia no filme e nas prévias do painel."""
    b, g = partes(a, legendas_ass, caps)
    return f"{b},{g}"


def comando(entradas, a, legendas_ass=None, caps=(), transicao=None, texturas=None, cortes=(), ts_fixo=None, desloc=0.0,
            gpu=False):
    """Argumentos do ffmpeg para o acabamento completo (entradas = args da(s) entrada(s) do vídeo, a 1ª é o filme).
    Sem transição nem textura cai no -vf de sempre (mesmo resultado de antes).
    ts_fixo/desloc (29/09/2026): pedaço do acabamento paralelo — instantes já no tempo do pedaço."""
    import fx
    tr = transicao or {}
    tipo = tr.get("tipo", "seco")
    tx = {k: v for k, v in (texturas or {}).items() if v}
    if ts_fixo is not None:
        ts = list(ts_fixo) if tipo != "seco" else []
    else:
        ts = fx.tempos(tr.get("freq", "capitulos"), list(caps) or capitulos(), list(cortes)) if tipo != "seco" else []
    fx.DESLOC = desloc
    b, g = partes(a, legendas_ass, caps if a.get("mergulho_capitulo") else (), fx.flash_brilho(tipo, ts), desloc, gpu=gpu)
    hw = HW if gpu else []
    if tipo in ("seco", "flash", "flash_suave") and not tx:
        return [*hw, *entradas, "-vf", f"{b},{g}"], ts
    extras = []
    graph, out = fx.grafo(b, tipo, ts, tx, g, extras)
    return [*hw, *entradas, *[x for e in extras for x in e], "-filter_complex", graph, "-map", f"[{out}]"], ts


def frames(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(re.sub(r"\D", "", r.stdout) or 0)


# 29/09/2026: o acabamento era 50 min num filme de 33 min (19 q/s) — medido em 60 s: decodificar+codificar sozinho
# faz 436 q/s; o peso é a cadeia de filtros (cor, vinheta, nitidez, textura), que num ffmpeg só usa poucos núcleos.
# Agora o filme é cortado em PEDACOS trechos (fronteira longe de transição e de mergulho) que rodam AO MESMO TEMPO,
# cada um com teto de threads (PC de 12 núcleos: 4 x 3), e são juntados sem recodificar. Mesmo resultado, ~3-4x mais rápido.
PEDACOS = 4
FIO = 3   # threads de filtro por pedaço


def fronteiras(n0, npar, evitar, fps=30):
    """Quadros de corte entre pedaços: perto de n0*k/npar, a >= 1,2 s de qualquer transição/mergulho."""
    out = [0]
    for k in range(1, npar):
        alvo = n0 * k // npar
        for d in range(0, 20 * fps, 15):
            ok = None
            for f in (alvo + d, alvo - d):
                if out[-1] + 30 * fps < f < n0 - 30 * fps and all(abs(f / fps - t) >= 1.2 for t in evitar):
                    ok = f
                    break
            if ok:
                out.append(ok)
                break
    return out + [n0]


def paralelo(src, tmp, a, ass, caps, tr, tx, qual, n0, npar, gpu=False):
    import fx
    from concurrent.futures import ThreadPoolExecutor
    tipo = tr.get("tipo", "seco")
    ts_all = fx.tempos(tr.get("freq", "capitulos"), list(caps), fx.cortes()) if tipo != "seco" else []
    caps_m = list(caps) if a.get("mergulho_capitulo") else []
    bs = fronteiras(n0, npar, ts_all + caps_m)
    pasta = tmp.with_name("_acab_pedacos")
    pasta.mkdir(exist_ok=True)
    print(f"[acabamento] paralelo: {len(bs) - 1} pedaços {[round(b / 30) for b in bs]} s, {FIO} threads de filtro cada", flush=True)

    def um(k):
        f0, f1 = bs[k], bs[k + 1]
        s0, L = f0 / 30, f1 - f0
        dentro = lambda xs: [x - s0 for x in xs if s0 - 1 <= x < f1 / 30 + 1]
        args, _ = comando(["-ss", f"{s0:.4f}", "-i", str(src)], a, ass, dentro(caps_m) if caps_m else [], tr, tx, (),
                          ts_fixo=dentro(ts_all), desloc=s0, gpu=gpu)
        vm = [] if "-filter_complex" in args else ["-map", "0:v:0"]
        if k == len(bs) - 2:   # último pedaço: o seek no fim do arquivo pode render 1 quadro a menos — repete o último
            pos = max(i for i, x in enumerate(args) if x in ("-vf", "-filter_complex")) + 1
            cadeia = args[pos]
            j = cadeia.rfind("format=yuv420p")
            args[pos] = cadeia[:j] + "format=yuv420p,tpad=stop_mode=clone:stop=3" + cadeia[j + len("format=yuv420p"):]
        out = pasta / f"p{k}.mp4"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *args, "-filter_threads", str(FIO),
                            "-filter_complex_threads", str(FIO), *enc(qual), *vm, "-frames:v", str(L), "-an", str(out)],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode != 0:
            raise SystemExit(f"[acabamento] pedaço {k} falhou: {r.stderr[-400:]}")
        got = frames(out)
        if got != L and k == len(bs) - 2 and 0 < L - got <= 3:   # 02/10: completa o último pedaço (seek no fim do arquivo)
            pad = pasta / f"p{k}_pad.mp4"
            r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(out), "-vf",
                                f"tpad=stop_mode=clone:stop={L - got}", *enc(qual), "-frames:v", str(L), "-an", str(pad)],
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode == 0:
                pad.replace(out)
                print(f"[acabamento] pedaço {k}: {got} -> {L} quadros (último quadro repetido)", flush=True)
                got = frames(out)
        if got != L:
            raise SystemExit(f"[acabamento] pedaço {k}: {got} quadros, esperado {L}")
        print(f"[acabamento] pedaço {k + 1}/{len(bs) - 1} ok ({L} quadros)", flush=True)
        return out

    import time
    t = time.time()
    with ThreadPoolExecutor(len(bs) - 1) as ex:
        outs = list(ex.map(um, range(len(bs) - 1)))
    lst = pasta / "lista.txt"
    lst.write_text("\n".join(f"file '{o.as_posix()}'" for o in outs), "utf-8")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-i", str(src), "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", str(tmp)],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"[acabamento] junção falhou: {r.stderr[-400:]}")
    # 02/10/2026: a junção pode sair com as marcas de tempo quebradas (quadros certos, "duração" de 30-48 h)
    dv = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                               "-of", "csv=p=0", str(tmp)], capture_output=True, text=True).stdout.strip().split(",")[0] or 0)
    if abs(dv - n0 / 30) > 2:
        h264, fixo = tmp.with_name("_ts.h264"), tmp.with_name("_ts_fix.mp4")
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(tmp), "-map", "0:v", "-c", "copy",
                        "-bsf:v", "h264_mp4toannexb", "-f", "h264", str(h264)], check=True, cwd=ROOT)
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-fflags", "+genpts", "-r", "30", "-i", str(h264),
                        "-i", str(tmp), "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", str(fixo)],
                       check=True, cwd=ROOT)
        fixo.replace(tmp)
        h264.unlink(missing_ok=True)
        print(f"[acabamento] marcas de tempo quebradas na junção ({dv:.0f} s para {n0 / 30:.0f} s) — regravadas", flush=True)
    for o in outs:
        o.unlink(missing_ok=True)
    print(f"[acabamento] {len(outs)} pedaços em {(time.time() - t) / 60:.1f} min", flush=True)


def main():
    cfg = config()
    a = {**PADRAO, **(cfg.get("acabamento") or {})}
    leg = (cfg.get("legendas") or {}).get("estilo", "off")
    ass = None
    if leg and leg != "off":
        subprocess.run([sys.executable, str(ROOT / "scripts" / "legendas.py")], cwd=ROOT, check=True)
        ass = "data/legendas.ass"
    elif (D / "master_transcript.json").exists():   # sem legenda na tela: o .srt para o YouTube sai do mesmo jeito
        subprocess.run([sys.executable, str(ROOT / "scripts" / "legendas.py"), "--estilo", "classica",
                        "--saida", "out/_sem_uso.ass"], cwd=ROOT)
    if a.get("desligado") and not ass:
        print("[acabamento] desligado no pipeline_config — nada feito")
        return
    src = ROOT / (sys.argv[sys.argv.index("--in") + 1] if "--in" in sys.argv else "out/final.mp4")
    tmp = Path(sys.argv[sys.argv.index("--out") + 1]).resolve() if "--out" in sys.argv else src.with_name(src.stem + "_acab.mp4")
    qual = (cfg.get("render") or {}).get("qualidade", "alta")
    if a.get("leve"):
        qual = "rapida"
    import fx
    tr, tx = cfg.get("transicao") or {}, cfg.get("texturas") or {}
    caps = capitulos()
    if (tr.get("tipo", "seco") != "seco") or any(tx.values()):
        fx.gerar_assets()
    gpu = cfg.get("acabamento_gpu", True) is not False and "--cpu" not in sys.argv and tem_opencl()
    args, ts = comando(["-i", str(src)], a, ass, caps, tr, tx, fx.cortes(), gpu=gpu)
    n0 = frames(src)
    print(f"[acabamento] tom {a['tom']} | grão {a['grao']} | vinheta {a['vinheta']} | tremor {bool(a.get('tremor'))} | "
          f"nitidez {a.get('nitidez')} | barras {bool(a.get('barras'))} | mergulho {bool(a.get('mergulho_capitulo'))} | "
          f"legendas {leg} | render {qual} | {'PLACA (OpenCL)' if gpu else 'processador'} | {n0} quadros")
    vmap = [] if "-filter_complex" in args else ["-map", "0:v:0"]
    print(f"[acabamento] transição {tr.get('tipo', 'seco')} ({tr.get('freq', '-')}, {len(ts)} vezes) | texturas "
          f"{', '.join(k for k, v in tx.items() if v) or '-'}")
    npar = int(cfg.get("acabamento_pedacos") or PEDACOS)
    if npar > 1 and n0 > 120 * 30:
        paralelo(src, tmp, a, ass, caps, tr, tx, qual, n0, npar, gpu=gpu)
    else:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *args, "-filter_threads", "6", "-filter_complex_threads", "6",
                            *enc(qual), *vmap, "-map", "0:a:0", "-c:a", "copy", str(tmp)], capture_output=True, text=True, cwd=ROOT)
        if r.returncode != 0:
            raise SystemExit(f"[acabamento] ffmpeg falhou: {r.stderr[-400:]}")
    n1 = frames(tmp)
    if n1 != n0:
        raise SystemExit(f"[acabamento] {n1} quadros, esperado {n0} — arquivo mantido em {tmp.name}")
    mb = tmp.stat().st_size / 1e6
    if mb / (n1 / 30 / 60) > 160:   # mais de ~21 Mbps: a codificação voltou a inchar (grão x qp fixo)
        raise SystemExit(f"[acabamento] {mb:.0f} MB para {n1 / 1800:.1f} min — taxa alta demais, arquivo mantido em {tmp.name}")
    if "--out" in sys.argv:   # 09/10/2026: teste — grava só no --out, não mexe no filme
        print(f"[acabamento] ok (teste) -> {tmp} ({mb:.0f} MB)")
        return
    if int((cfg.get("entrega") or {}).get("shorts") or 0) > 0:   # 28/09: Shorts 9:16 saem do filme LIMPO (sem barra/legenda)
        src.replace(src.with_name("final_base.mp4"))
    tmp.replace(src)
    print(f"[acabamento] ok -> {src.relative_to(ROOT)} ({mb:.0f} MB)")


if __name__ == "__main__":
    main()
