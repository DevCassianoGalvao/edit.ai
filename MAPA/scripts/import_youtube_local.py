# -*- coding: utf-8 -*-
"""Os videos do YouTube que o usuario baixou a mao (input/youtube/) viram
trechos de 6-8 s no manifesto do filme.

Cada arquivo e casado com a lista curada (links_youtube_<tema>.md) pelo ID do
YouTube no nome do arquivo ou, se nao houver, pelo titulo. Cada link da lista
diz para quais partes do roteiro ele serve (PARTES abaixo). De cada video saem
N trechos em pontos espalhados (fugindo de abertura e encerramento, onde ficam
logo, cartela e "inscreva-se"); a folha de contato qa/clipes_yt.jpg mostra um
quadro de cada trecho para a revisao a olho antes de montar.

    py scripts/import_youtube_local.py            corta o que falta
    py scripts/import_youtube_local.py --rejeitar p02_yt6CmK_40,...   tira trechos
"""
import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(AQUI, "input", "youtube")
DEST = os.path.join(AQUI, "downloads", "video")
MANIFESTO = os.path.join(AQUI, "data", "video_manifest.json")
CAND = os.path.join(AQUI, "data", "yt_candidatos.json")

# id -> (partes onde entra, quantos trechos, segundos por trecho)
PARTES = {
    "6CmKyLL9WPU": ([2, 7, 24], 3, 8), "3VWkNbj5NEk": ([49, 50, 5], 3, 8),
    "yZQwwArLR-c": ([7, 24, 43], 3, 8), "tBiOiQ7T_r8": ([2, 49], 2, 7),
    "m2FrX_1WayY": ([3, 21, 42], 3, 8), "EUQOI-4FmDA": ([35, 6, 42], 3, 7),
    "t9oBDb_DZCI": ([43, 45], 2, 8), "c4K-di7CmqQ": ([1, 29, 24], 3, 7),
    "Ju5zuhY302Q": ([50, 4], 2, 7), "g_igODn9Mbs": ([22, 29, 30], 3, 7),
    "AzqjHICxBII": ([22, 34], 2, 7), "vUKaK_BWtWs": ([17, 12, 36], 3, 7),
    "eOl8H4Yj2WI": ([17, 14], 2, 7), "0UjN4XyIt8w": ([19, 44, 40], 3, 7),
    "flZd9yeCBbw": ([44, 19], 2, 7), "gpXX6dS5yy4": ([8, 23, 41], 3, 7),
    "zdF115FFfpU": ([9, 27], 2, 7), "Mviy0wGett4": ([25, 47], 2, 7),
    "pyLQxnra9lM": ([27, 41], 2, 7), "BtIkB2jqggM": ([33, 38], 2, 7),
    "oIGGEHtG6W4": ([10, 31], 2, 7), "puCnWbGvcAU": ([11], 1, 6),
    "G_Y-2_iadUw": ([13, 18], 2, 5), "ldKBKNHd7sc": ([12, 13], 2, 5),
    "whs4CVrTTTo": ([14], 1, 5), "EH5VzoaC8XY": ([15, 36], 2, 5),
    "0yr0alnd9o4": ([32, 34], 2, 5), "22hKrb3qdEU": ([16, 20], 2, 5),
    "XvFw4sobrO4": ([26], 1, 5), "Nj-Nx6mJvlw": ([48, 45], 2, 6),
}

ap = argparse.ArgumentParser()
ap.add_argument("--rejeitar", default="")
args = ap.parse_args()

cands = {}
if os.path.exists(CAND):
    for lista in json.load(open(CAND, encoding="utf-8")).values():
        for v in lista:
            cands[v["ytId"]] = v
os.makedirs(DEST, exist_ok=True)
man = json.load(open(MANIFESTO, encoding="utf-8")) if os.path.exists(MANIFESTO) else {"clipes": []}

rej = {x.strip() for x in args.rejeitar.split(",") if x.strip()}
if rej:
    fora = [c for c in man["clipes"] if os.path.splitext(os.path.basename(c["arquivo"]))[0] in rej]
    for c in fora:
        p = os.path.join(AQUI, c["arquivo"])
        if os.path.exists(p):
            os.remove(p)
    man["clipes"] = [c for c in man["clipes"] if c not in fora]
    json.dump(man, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("trechos rejeitados:", len(fora))
    sys.exit(0)


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def casar(arquivo):
    base = os.path.splitext(os.path.basename(arquivo))[0]
    for vid in PARTES:
        if vid in base:
            return vid
    melhor, nota = None, 0.0
    for vid in PARTES:
        t = norm(cands.get(vid, {}).get("title", ""))
        r = difflib.SequenceMatcher(None, norm(base)[:len(t) + 10], t).ratio()
        if r > nota:
            melhor, nota = vid, r
    return melhor if nota >= 0.55 else None


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "default=nw=1:nk=1", p],
                       capture_output=True, text=True)
    v = [x for x in r.stdout.split() if x.strip()]
    try:
        return int(v[0]), int(v[1]), float(v[2])
    except Exception:
        return 0, 0, 0.0


VF = ("scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,"
      "fps=30,format=yuv420p")
ja = {c["arquivo"] for c in man["clipes"]}
novos = semcasar = 0
for arq in sorted(glob.glob(os.path.join(ENTRADA, "*"))):
    if not arq.lower().endswith((".mp4", ".webm", ".mkv", ".mov")):
        continue
    vid = casar(arq)
    if not vid:
        print("  ? nao reconheci:", os.path.basename(arq))
        semcasar += 1
        continue
    partes, n, seg = PARTES[vid]
    w, h, dur = probe(arq)
    if dur < 10:
        continue
    # pontos espalhados entre 15% e 85% do video
    for k in range(n):
        ini = dur * (0.15 + 0.7 * (k + 0.5) / n)
        parte = partes[k % len(partes)]
        nome = "p%02d_yt%s_%d.mp4" % (parte, re.sub(r"[^A-Za-z0-9]", "", vid)[:6], int(ini))
        saida = os.path.join(DEST, nome)
        rel = os.path.relpath(saida, AQUI).replace("\\", "/")
        if rel in ja:
            continue
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % ini, "-i", arq, "-t", str(seg),
                            "-an", "-vf", VF, "-c:v", "libx264", "-crf", "17", "-preset", "medium", saida],
                           capture_output=True, text=True)
        if r.returncode or not os.path.exists(saida):
            print("  ! falhou:", nome, r.stderr[:80])
            continue
        c = cands.get(vid, {})
        man["clipes"].append({"parte": parte, "arquivo": rel, "fonte": "youtube",
                              "canal": c.get("channel", ""), "url": "https://www.youtube.com/watch?v=" + vid,
                              "titulo": c.get("title", os.path.basename(arq)), "inicio": round(ini, 1),
                              "segundos": seg, "largura": w, "altura": h,
                              "licenca": "YouTube (uso de trecho curto, sem audio; ver atribuicao)",
                              "busca": vid})
        novos += 1
        print("  + %s  parte %02d  %.0fs  %dp  %s" % (nome, parte, ini, h, c.get("channel", "")[:30]))

man["clipes"].sort(key=lambda c: (c["parte"], c["arquivo"]))
json.dump(man, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# folha de contato: um quadro do meio de cada trecho do YouTube
yt = [c for c in man["clipes"] if c["fonte"] == "youtube"]
if yt:
    os.makedirs(os.path.join(AQUI, "qa", "clipes_yt"), exist_ok=True)
    for i, c in enumerate(yt):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "3", "-i", os.path.join(AQUI, c["arquivo"]),
                        "-frames:v", "1", "-vf", "scale=384:-2,drawtext=fontfile=C\\\\:/Windows/Fonts/arial.ttf:"
                        "text='%d':x=8:y=8:fontsize=34:fontcolor=yellow:box=1:boxcolor=black" % (i + 1),
                        os.path.join(AQUI, "qa", "clipes_yt", "%03d.jpg" % i)], capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(AQUI, "qa", "clipes_yt", "%03d.jpg"),
                    "-vf", "tile=5x%d" % (-(-len(yt) // 5)), "-frames:v", "1",
                    os.path.join(AQUI, "qa", "clipes_yt.jpg")], capture_output=True)
    with open(os.path.join(AQUI, "qa", "clipes_yt.txt"), "w", encoding="utf-8") as f:
        for i, c in enumerate(yt):
            f.write("%d %s\n" % (i + 1, os.path.splitext(os.path.basename(c["arquivo"]))[0]))
tot = sum(c["segundos"] for c in man["clipes"])
print("novos: %d | sem casar: %d | trechos no manifesto: %d (%d s)" % (novos, semcasar, len(man["clipes"]), tot))
