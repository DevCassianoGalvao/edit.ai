"""SUSPEITOS NOS CLIPES DE VÍDEO antes do render — 04/10/2026.

O apresentador falando ao microfone aos 19:30 do porta-aviões só apareceu na folha do MP4 final e custou um
2º render. Aqui, depois do build_overlays (no fechar.py preparar), cada clipe de VÍDEO usado na timeline é amostrado
em 3 quadros e passa por dois detectores do prefilter.py (CLIP local, sem internet):
  - APRESENTADOR: "pessoa falando para a câmera / entrevista / microfone" ganhando de "imagem de ambiente";
  - TEXTO QUEIMADO: tem_texto() (legenda, ficha técnica, tarja, botão de inscrição).
Saída: qa/suspeitos.jpg (só os marcados, com o id do clipe e o segundo no filme) + data/video_suspeitos.json.
É AVISO, não rejeição: eu olho a folha (1 só) e mando o que for defeito para window_rejects.json.

Uso: python video_suspeitos.py
"""
import json, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prefilter as pf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
FALA = ["a person talking to the camera", "a news presenter or youtuber speaking into a microphone",
        "an interview, a man speaking with a microphone", "a vlogger looking at the camera"]
AMB = ["footage of a place, landscape or machine without anyone facing the camera", "a vehicle, ship or aircraft",
       "workers doing a task, seen from the side", "an aerial drone view"]
LIM_FALA = 0.012  # 04/10: calibrado nos 47 clipes do porta-aviões — pega a entrevista do Ward Carroll (0,017) e os vlogs (0,036-0,045); mediana -0,013


VER = "2026-10-07a"   # mudar quando FALA/AMB/LIM_FALA/tem_texto mudarem: o cache antigo deixa de valer


def chave(c):
    try:
        st = (ROOT / "public" / c["file"]).stat()
        return f"{c['file']}|{st.st_size}|{int(st.st_mtime)}|{VER}"
    except (OSError, KeyError):
        return None


def main():
    tl = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    lib = {c["id"]: c for c in json.loads((D / "clips.json").read_text("utf-8"))["clips"]}
    usos = {}
    for it in tl:
        if it.get("kind") == "video" and it.get("clip") in lib:
            usos.setdefault(it["clip"], it["from"] / FPS)
    tmp = Path(tempfile.mkdtemp())
    # 07/10/2026: memória por clipe — o preparar de novo só avalia clipe que entrou/mudou (antes ~1,4 min a cada rodada)
    cpath, qdir = D / "suspeitos_cache.json", D / "_suspeitos_quadros"
    try:
        cache = json.loads(cpath.read_text("utf-8"))
    except Exception:  # noqa: BLE001
        cache = {}
    pend = {cid: t for cid, t in usos.items() if not (chave(lib[cid]) and chave(lib[cid]) in cache)}
    if pend and not pf.disponivel():
        print("[suspeitos] CLIP indisponível — pulando (conferir a folha densa como antes)"); return

    def avalia(par):
        cid, t_filme = par
        c = lib[cid]
        f = ROOT / "public" / c["file"]
        if not f.exists():
            return None
        dur = c.get("dur", 150) / FPS
        piores = (0.0, False, None)
        for k, frac in enumerate((0.25, 0.5, 0.75)):
            p = tmp / f"{cid}_{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur * frac:.2f}", "-i", str(f), "-frames:v", "1",
                            "-vf", "scale=640:-2", str(p)], check=False)
            if not p.exists():
                continue
            v = pf.emb_img(p)
            fala = max(float(v @ pf.emb_txt(x)) for x in FALA) - max(float(v @ pf.emb_txt(x)) for x in AMB)
            txt, _, _ = pf.tem_texto(p, v)
            if fala > piores[0] or (txt and not piores[1]):
                piores = (max(fala, piores[0]), txt or piores[1], p)
        if piores[0] > LIM_FALA or piores[1]:
            return {"clip": cid, "t": round(t_filme), "fala": round(piores[0], 3), "texto": piores[1],
                    "titulo": (c.get("title") or "")[:60], "quadro": str(piores[2])}
        return None

    with ThreadPoolExecutor(4) as ex:
        novos = dict(zip(pend, ex.map(avalia, pend.items())))
    qdir.mkdir(exist_ok=True)
    for cid, r in novos.items():
        k = chave(lib[cid])
        if not k:
            continue
        if r and r.get("quadro") and Path(r["quadro"]).exists():
            dest = qdir / f"{cid}.jpg"
            shutil.copy2(r["quadro"], dest)
            r = {**r, "quadro": str(dest)}
        cache[k] = r
    cpath.write_text(json.dumps(cache, ensure_ascii=False), "utf-8")
    sus = []
    for cid, t in usos.items():
        r = novos.get(cid) if cid in novos else cache.get(chave(lib[cid]) or "")
        if r:
            sus.append({**r, "t": round(t)})
    sus.sort(key=lambda r: r["t"])
    (D / "video_suspeitos.json").write_text(json.dumps(sus, ensure_ascii=False, indent=1), "utf-8")
    (ROOT / "qa" / "suspeitos.jpg").unlink(missing_ok=True)   # 05/10/2026: folha velha enganava quando a nova dava 0
    if sus:
        W, H, C = 320, 180, 6
        R = (len(sus) + C - 1) // C
        sheet = Image.new("RGB", (W * C, (H + 34) * R), (16, 16, 16))
        d = ImageDraw.Draw(sheet)
        for j, r in enumerate(sus):
            x, y = (j % C) * W, (j // C) * (H + 34)
            sheet.paste(Image.open(r["quadro"]).convert("RGB").resize((W, H)), (x, y + 34))
            motivo = ("FALA " if r["fala"] > LIM_FALA else "") + ("TEXTO" if r["texto"] else "")
            d.text((x + 4, y + 2), f"{r['clip']} @{r['t'] // 60:02d}:{r['t'] % 60:02d} {motivo}", fill=(255, 210, 0))
            d.text((x + 4, y + 17), r["titulo"][:44], fill=(200, 200, 200))
        sheet.save(ROOT / "qa" / "suspeitos.jpg", quality=85)
    print(f"[suspeitos] {len(pend)} avaliados agora, {len(usos) - len(pend)} do cache")
    print(f"[suspeitos] {len(sus)} de {len(usos)} clipes de vídeo marcados" + (" -> qa/suspeitos.jpg (OLHAR antes do render)" if sus else ""))


if __name__ == "__main__":
    main()
