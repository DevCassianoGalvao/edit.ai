# -*- coding: utf-8 -*-
"""Os 20% de VIDEO deste filme, cortados de filmes em dominio publico do
Internet Archive (o Commons nao tem video de Egito e o YouTube esta bloqueado).

Cada trecho foi escolhido a mao numa folha de contato (qa/arquivo/*.jpg): nada
de cartelas de texto, mapas, animacao, reconstituicao ou cena de arquivo com
gente identificavel em situacao delicada. O corte e feito no servidor
(-ss antes do -i), entao so trafega o pedaco usado.

    py scripts/fetch_archive_video.py            baixa o que falta
    py scripts/fetch_archive_video.py --refazer  refaz tudo
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(AQUI, "downloads", "video")
MANIFESTO = os.path.join(AQUI, "data", "video_manifest.json")

# filmes-fonte: id do item, arquivo, duracao e a licenca que o item declara
FILMES = {
    "aw1": ("AncientWorldEgypt_Pt1", "AncientWorldEgypt_Pt1.mp4",
            "The Ancient World: Egypt, Part 1 (Harmon Foundation / Metropolitan Museum of Art)",
            "Public domain (Harmon Foundation collection, Internet Archive)"),
    "aw2": ("AncientWorldEgypt_Pt2", "AncientWorldEgypt_Pt2.mp4",
            "The Ancient World: Egypt, Part 2 (Harmon Foundation / Metropolitan Museum of Art)",
            "Public domain (Harmon Foundation collection, Internet Archive)"),
    "dig": ("0998_Digging_Into_the_Past_Egyptian_Excavations_of_the_Metropolitan_01_00_44_21",
            "0998_Digging_Into_the_Past_Egyptian_Excavations_of_the_Metropolitan_01_00_44_21_3mb.mp4",
            "Digging Into the Past: Egyptian Excavations of the Metropolitan Museum (Prelinger Archives)",
            "Public domain (Prelinger Archives, Internet Archive)"),
}

# (parte, filme, segundo inicial, duracao, o que aparece)
TRECHOS = [
    (1, "aw1", 1340, 8, "cabeca de estatua real em granito, museu"),
    (2, "aw2", 900, 8, "portal e colunas de Karnak"),
    (2, "aw2", 920, 8, "colunata com sombras, templo de Luxor"),
    (3, "aw2", 500, 8, "relevo de Akenaton em talhe fundo"),
    (4, "aw1", 500, 8, "colossos sentados escavados na rocha"),
    (5, "aw2", 160, 8, "corredor interno de templo"),
    (6, "aw2", 320, 8, "Colossos de Memnon, Amenhotep III"),
    (6, "aw2", 360, 7, "Colossos de Memnon, plano aberto"),
    (7, "aw2", 480, 8, "busto pintado de rainha do Reino Novo"),
    (8, "aw2", 400, 8, "relevo do disco solar com raios em maos"),
    (9, "aw2", 80, 8, "falesias tebanas sobre o deserto"),
    (9, "aw1", 580, 7, "escarpa de deserto ao amanhecer"),
    (10, "aw1", 940, 8, "estatuas reais pintadas, par sentado"),
    (11, "aw1", 1500, 8, "relevo de perfil em calcario"),
    (12, "dig", 164, 8, "fila de trabalhadores subindo a encosta da escavacao"),
    (16, "aw1", 1600, 8, "cartucho hieroglifico em pedra"),
    (17, "aw1", 1520, 8, "relevo com o signo da vida"),
    (18, "aw1", 1640, 8, "portal inscrito de tumba"),
    (19, "dig", 955, 8, "caixoes dentro da cripta, como foram deixados"),
    (19, "dig", 987, 8, "retirada de material da boca da tumba"),
    (20, "aw1", 1120, 8, "mobiliario funerario dourado"),
    (21, "aw2", 580, 8, "sarcofago dourado em close"),
    (24, "aw1", 660, 8, "relevo de faraó em pedra escura"),
    (30, "aw1", 1300, 8, "cabeca de reserva em gesso, museu"),
    (31, "aw1", 1320, 7, "rosto de gesso em close"),
    (32, "aw1", 1100, 8, "camara funeraria com objetos"),
    (32, "aw1", 1160, 7, "arca funeraria fechada"),
    (33, "aw1", 1620, 8, "coluna com cartuchos"),
    (34, "aw1", 960, 8, "relevo de oficiais e servidores"),
    (35, "aw2", 880, 8, "avenida de esfinges de Karnak"),
    (36, "aw2", 720, 8, "par de estatuas reais em pedra"),
    (37, "aw2", 489, 7, "busto pintado de Nefertiti, perfil"),
    (38, "aw1", 1400, 8, "modelos de madeira de oficina"),
    (38, "aw1", 1460, 8, "maquetes de oficina em tumba"),
    (39, "dig", 274, 8, "escavacao no deserto plano"),
    (39, "dig", 439, 8, "trabalhadores com cestos na encosta"),
    (40, "dig", 918, 8, "escavacao dentro de uma vala"),
    (40, "dig", 1151, 8, "caixotes sendo carregados na carroca"),
    (41, "dig", 329, 8, "canteiro de escavacao visto de cima"),
    (41, "dig", 603, 8, "terraco do templo com os trabalhadores"),
    (42, "aw2", 1000, 8, "colunas de Karnak contra o ceu"),
    (43, "aw1", 1240, 8, "Esfinge de Gize de lado"),
    (44, "aw1", 620, 8, "dunas do deserto"),
    (44, "aw1", 520, 8, "por do sol sobre o Nilo"),
]

ap = argparse.ArgumentParser()
ap.add_argument("--refazer", action="store_true")
args = ap.parse_args()

os.makedirs(DEST, exist_ok=True)
os.makedirs(os.path.dirname(MANIFESTO), exist_ok=True)
manifesto = json.load(open(MANIFESTO, encoding="utf-8")) if os.path.exists(MANIFESTO) else {"clipes": []}
manifesto["clipes"] = [c for c in manifesto["clipes"] if c.get("fonte") == "archive"]
ja = {c["arquivo"] for c in manifesto["clipes"]}

# 4:3 -> 16:9 cortando mais do rodape do que do topo (cabeca de estatua no alto)
VF = ("crop=iw:iw*9/16:0:(ih-iw*9/16)*0.35,scale=1920:1080:flags=lanczos,"
      "fps=30,format=yuv420p")

novos = falhas = 0
for parte, tag, ini, dur, oque in TRECHOS:
    ident, nome, titulo, licenca = FILMES[tag]
    saida = os.path.join(DEST, "p%02d_%s_%d.mp4" % (parte, tag, ini))
    rel = os.path.relpath(saida, AQUI).replace("\\", "/")
    if os.path.exists(saida) and not args.refazer:
        if rel not in ja:
            manifesto["clipes"].append({"parte": parte, "arquivo": rel, "fonte": "archive",
                                        "canal": titulo, "url": "https://archive.org/details/" + ident,
                                        "titulo": oque, "inicio": ini, "segundos": dur,
                                        "largura": 1920, "altura": 1080, "licenca": licenca, "busca": tag})
        print("   = %s (ja estava)" % os.path.basename(saida))
        continue
    url = "https://archive.org/download/%s/%s" % (ident, urllib.parse.quote(nome))
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(ini), "-i", url, "-t", str(dur),
                        "-an", "-vf", VF, "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        saida], capture_output=True, text=True)
    if r.returncode or not os.path.exists(saida) or os.path.getsize(saida) < 50000:
        print("   ! parte %02d %s %ds: %s" % (parte, tag, ini, (r.stderr or "")[:90]))
        falhas += 1
        continue
    manifesto["clipes"] = [c for c in manifesto["clipes"] if c["arquivo"] != rel]
    manifesto["clipes"].append({"parte": parte, "arquivo": rel, "fonte": "archive",
                                "canal": titulo, "url": "https://archive.org/details/" + ident,
                                "titulo": oque, "inicio": ini, "segundos": dur,
                                "largura": 1920, "altura": 1080, "licenca": licenca, "busca": tag})
    novos += 1
    print("   + parte %02d  %s  %ds  %s" % (parte, tag, ini, oque), flush=True)

manifesto["clipes"].sort(key=lambda c: (c["parte"], c["arquivo"]))
json.dump(manifesto, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("clipes no manifesto: %d (novos %d, falhas %d) | %d s de video"
      % (len(manifesto["clipes"]), novos, falhas, sum(c["segundos"] for c in manifesto["clipes"])))
sys.exit(1 if falhas else 0)
