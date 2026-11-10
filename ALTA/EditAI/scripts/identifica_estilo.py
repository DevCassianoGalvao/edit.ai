"""IDENTIFICADOR DE EDIÇÃO — mede o estilo de um vídeo de referência e grava um estilo para o painel (27/09/2026).

O usuário manda um vídeo que quer imitar; este script mede o que dá para medir e monta as folhas para o Claude olhar:
  ritmo    cortes (detecção de cena do ffmpeg), duração média/mediana de plano, cortes por minuto, mergulhos no preto
  cor      brilho, contraste, saturação, fração P&B, temperatura (R-B), sépia
  textura  grão (resíduo de alta frequência), vinheta (canto/centro), barras de cinema (faixas pretas)
  texto    faixa de baixo com borda densa em muitos quadros = legenda queimada provável; centro = letreiro
  som      loudness (EBU R128) e silêncios: narração sem cama tem pausas; cama contínua = trilha por baixo
Saídas em OUTDIR: analise.json (métricas + sugestão {escolhas, liga} no formato do painel/catalogo.py),
folha_planos.jpg (1 quadro por plano, em ordem — mostra o ritmo), folha_geral.jpg (24 quadros no vídeo inteiro),
ritmo.png (duração de cada plano ao longo do vídeo) e capa.jpg.
Com --gravar SLUG "Nome" grava painel/estilos/SLUG.json já com a sugestão (o Claude revisa olhando as folhas).

Uso: python identifica_estilo.py VIDEO OUTDIR [--gravar slug "Nome do estilo"] [--max-min 12]
"""
import json, math, re, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
F1 = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(v):
    r = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration",
           "-of", "json", str(v))
    j = json.loads(r.stdout)
    s = j["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), s["width"], s["height"], float(n) / float(d or 1)


def cortes_e_pretos(v, ate):
    """Uma passada em 320 px: detecção de cena + blackdetect."""
    r = sh("ffmpeg", "-hide_banner", "-t", f"{ate:.1f}", "-i", str(v), "-an", "-vf",
           "scale=320:-2,blackdetect=d=0.25:pix_th=0.06,select='gt(scene,0.30)',showinfo", "-f", "null", "-")
    cortes = [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    pretos = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)]
    return cortes, pretos


def quadro(v, t, w=480):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-vf", f"scale={w}:-2",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    from io import BytesIO
    try:
        return Image.open(BytesIO(r.stdout)).convert("RGB")
    except Exception:  # noqa: BLE001
        return None


def medidas(ims):
    L, C, S, G, W, V, GR, BAR, TXB, TXC = [], [], [], [], [], [], [], [], [], []
    for im in ims:
        a = np.asarray(im).astype(np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        y = 0.299 * r + 0.587 * g + 0.114 * b
        mx, mn = a.max(-1), a.min(-1)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
        h, w = y.shape
        L.append(y.mean()); C.append(y.std()); S.append(sat.mean())
        G.append(float(np.abs(r - g).mean() + np.abs(g - b).mean()) < 6)
        W.append(float((r - b).mean()))
        c = y[h // 3:2 * h // 3, w // 3:2 * w // 3].mean()
        k = np.concatenate([y[:h // 6, :w // 6].ravel(), y[:h // 6, -w // 6:].ravel(), y[-h // 6:, :w // 6].ravel(), y[-h // 6:, -w // 6:].ravel()]).mean()
        V.append(k / max(c, 1))
        blur = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)
        res = np.abs(np.asarray(im.convert("L")).astype(np.float32) - blur)
        GR.append(float(np.median(res)))
        topo, base = y[:int(h * 0.1)], y[-int(h * 0.1):]
        BAR.append(topo.mean() < 14 and base.mean() < 14 and y[int(h * 0.3):int(h * 0.7)].mean() > 30)
        ed = np.abs(np.diff(np.asarray(im.convert("L")).astype(np.float32), axis=1))
        faixa = ed[int(h * 0.78):int(h * 0.93)]
        meio = ed[int(h * 0.35):int(h * 0.65)]
        TXB.append(float((faixa > 60).mean()) > 0.035 and float((faixa > 60).mean()) > 1.8 * float((meio > 60).mean()))
        TXC.append(float((meio > 60).mean()) > 0.06)
    return {"brilho": round(float(np.mean(L)), 1), "contraste": round(float(np.mean(C)), 1),
            "saturacao": round(float(np.mean(S)), 3), "fracao_pb": round(float(np.mean(G)), 2),
            "temperatura": round(float(np.mean(W)), 1), "vinheta": round(float(np.median(V)), 2),
            "grao": round(float(np.median(GR)), 2), "fracao_barras": round(float(np.mean(BAR)), 2),
            "fracao_legenda": round(float(np.mean(TXB)), 2), "fracao_letreiro": round(float(np.mean(TXC)), 2)}


def som(v, ate):
    r = sh("ffmpeg", "-hide_banner", "-t", f"{ate:.1f}", "-i", str(v), "-vn", "-af",
           "ebur128=framelog=quiet,silencedetect=n=-45dB:d=0.12", "-f", "null", "-")
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    lra = re.findall(r"LRA:\s+([\d.]+) LU", r.stderr)
    sil = sum(float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r.stderr))
    return {"lufs": float(i[-1]) if i else None, "lra": float(lra[-1]) if lra else None,
            "fracao_silencio": round(sil / max(ate, 1), 3)}


def folha(ims, rotulos, cols, saida, tw=320):
    th = int(tw * 9 / 16)
    rows = math.ceil(len(ims) / cols)
    s = Image.new("RGB", (cols * tw, rows * (th + 20)), (14, 14, 14))
    d = ImageDraw.Draw(s)
    for k, (im, rot) in enumerate(zip(ims, rotulos)):
        x, y = (k % cols) * tw, (k // cols) * (th + 20)
        if im:
            t = im.copy(); t.thumbnail((tw, th)); s.paste(t, (x + (tw - t.width) // 2, y + 20))
        d.text((x + 4, y + 3), rot, fill=(255, 210, 60), font=F1)
    s.save(saida, quality=84)


def grafico_ritmo(planos, dur, saida):
    W, H = 1200, 220
    im = Image.new("RGB", (W, H), (16, 16, 18))
    d = ImageDraw.Draw(im)
    mx = max(10.0, max((b for _, b in planos), default=10))
    for a, b in planos:
        x = int(a / dur * W)
        h = int(min(b, mx) / mx * (H - 30))
        d.rectangle([x, H - 10 - h, x + max(1, int(b / dur * W) - 1), H - 10], fill=(240, 180, 60))
    d.text((8, 6), f"duração de cada plano (altura) ao longo do vídeo — teto {mx:.0f} s", fill=(200, 200, 200), font=F1)
    im.save(saida)


def sugestao(m, ritmo, s):
    e = {"legendas": "off", "cor": "neutro", "textura": "leve", "destaque": "documentario", "render": "alta"}
    if m["fracao_pb"] > 0.6:
        e["cor"] = "pb"
    elif m["fracao_pb"] > 0.3 and m["temperatura"] > 8:
        e["cor"] = "sepia"
    elif m["temperatura"] > 14:
        e["cor"] = "quente"
    elif m["temperatura"] < -6:
        e["cor"] = "frio" if m["saturacao"] < 0.32 else "cinema"
    e["textura"] = "limpo" if m["grao"] < 1.2 and m["vinheta"] > 0.8 else "leve" if m["grao"] < 2.2 else "arquivo" if m["grao"] < 3.5 else "forte"
    if m["fracao_legenda"] > 0.35:
        e["legendas"] = "impacto" if ritmo["plano_mediano"] < 2.2 else "classica"
    liga = {"music": s["lufs"] is not None and s["fracao_silencio"] < 0.008, "sfx": ritmo["cortes_por_min"] > 18, "voz": True,
            "arquivo_dark": m["fracao_letreiro"] > 0.25, "paralaxe": True, "mapa": True,
            "mergulho": ritmo["pretos_por_10min"] >= 2, "barras": m["fracao_barras"] > 0.5, "nitidez": m["grao"] < 1.5}
    return e, liga


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    v, out = Path(a[0]), Path(a[1])
    out.mkdir(parents=True, exist_ok=True)
    dur, w, h, fps = probe(v)
    ate = min(dur, float(a[a.index("--max-min") + 1]) * 60 if "--max-min" in a else dur)
    print(f"[estilo] {v.name}: {dur / 60:.1f} min {w}x{h} {fps:.0f} fps — analisando {ate / 60:.1f} min")
    cortes, pretos = cortes_e_pretos(v, ate)
    marcos = [0.0] + cortes + [ate]
    planos = [(a0, b0 - a0) for a0, b0 in zip(marcos, marcos[1:]) if b0 - a0 > 0.05]
    dur_pl = sorted(p for _, p in planos)
    ritmo = {"cortes": len(cortes), "cortes_por_min": round(len(cortes) / (ate / 60), 1),
             "plano_medio": round(float(np.mean(dur_pl)), 2), "plano_mediano": round(float(np.median(dur_pl)), 2),
             "plano_p90": round(float(np.percentile(dur_pl, 90)), 2), "pretos": len(pretos),
             "pretos_por_10min": round(len(pretos) / (ate / 600), 1)}
    print(f"[estilo] ritmo: {ritmo}")
    amostra = [quadro(v, t) for t in np.linspace(ate * 0.03, ate * 0.97, 36)]
    amostra = [x for x in amostra if x]
    m = medidas(amostra)
    print(f"[estilo] imagem: {m}")
    s = som(v, ate)
    print(f"[estilo] som: {s}")
    esc, liga = sugestao(m, ritmo, s)
    pl = planos[:48]
    ims = [quadro(v, a0 + d0 / 2, 320) for a0, d0 in pl]
    folha(ims, [f"{int(a0 // 60)}:{a0 % 60:04.1f}  {d0:.1f}s" for a0, d0 in pl], 8, out / "folha_planos.jpg")
    tg = list(np.linspace(ate * 0.02, ate * 0.98, 24))
    folha([quadro(v, t, 400) for t in tg], [f"{int(t // 60)}:{int(t % 60):02d}" for t in tg], 6, out / "folha_geral.jpg", 400)
    grafico_ritmo(planos, ate, out / "ritmo.png")
    capa = quadro(v, ate * 0.35, 960)
    if capa:
        capa.save(out / "capa.jpg", quality=86)
    analise = {"video": v.name, "duracao_min": round(dur / 60, 2), "resolucao": f"{w}x{h}", "fps": round(fps, 2),
               "ritmo": ritmo, "imagem": m, "som": s, "sugestao": {"escolhas": esc, "liga": liga}}
    (out / "analise.json").write_text(json.dumps(analise, ensure_ascii=False, indent=1), "utf-8")
    print(f"[estilo] sugestão: {esc} | {liga}")
    if "--gravar" in a:
        i = a.index("--gravar")
        slug, nome = a[i + 1], a[i + 2]
        pasta = ROOT / "painel" / "estilos"
        pasta.mkdir(parents=True, exist_ok=True)
        rel = out.resolve().relative_to((ROOT / "painel").resolve()).as_posix() if str(out.resolve()).startswith(str((ROOT / "painel").resolve())) else None
        est = {"id": slug, "nome": nome, "origem": "referencia", "video": v.name, "escolhas": esc, "liga": liga,
               "desc": f"Do vídeo de referência: {ritmo['plano_mediano']:.1f} s por plano, {ritmo['cortes_por_min']:.0f} cortes/min.",
               "analise": "", "revisado": False, "metricas": {"ritmo": ritmo, "imagem": m, "som": s},
               "capa": f"{rel}/capa.jpg" if rel else None, "pasta": rel}
        (pasta / f"{slug}.json").write_text(json.dumps(est, ensure_ascii=False, indent=1), "utf-8")
        print(f"[estilo] gravado painel/estilos/{slug}.json")


if __name__ == "__main__":
    main()
