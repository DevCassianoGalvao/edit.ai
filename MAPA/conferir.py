# -*- coding: utf-8 -*-
"""conferir.py - audita as pastas de downloads e aponta SO o que esta errado.

    py conferir.py

Existe para cortar o laco caro: em vez de ler as 40 listagens inteiras a cada
rodada, olho so as partes sinalizadas. Sinaliza tres coisas, em ordem de
gravidade:

  FALTA    a pasta tem menos arquivo do que a parte pede
  REPETE   quase tudo na pasta e a mesma materia (mesmo titulo-base)
  SOLTA    o titulo nao divide nenhuma palavra com o 'mostrar' da parte

'SOLTA' e o unico heuristico, e ele erra para os dois lados - por isso mostra a
lista, nao decide nada. A regra de uso e a que custou caro para aprender: so
vale mexer numa parte com FALTA, com REPETE, ou com mais da metade SOLTA. Uma
imagem estranha em seis e invisivel no video e nao paga uma rodada de busca.
"""
from __future__ import annotations

import glob
import io
import json
import os
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))

RUIDO = set("""de da do das dos e a o as os um uma no na nos nas em por para com
que se sua seu the of and in on at for with from a an is are was to by geograph
org uk jpg jpeg png img dsc foto photo view front rear side interior exterior
cropped""".split())


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def palavras(texto):
    toks = re.split(r"[^\wÀ-ɏ]+", sem_acento(texto))
    return {t for t in toks if len(t) > 2 and not t.isdigit() and t not in RUIDO}


def base(nome):
    """Titulo sem o numero de ordem, sem extensao e sem sufixo de serie.
    'IBPA 23711 - Fiscalizacao do PROCON nos postos' e 'IBPA 23712 - ...' viram
    a mesma materia."""
    n = re.sub(r"^\d+_", "", os.path.splitext(nome)[0])
    n = re.sub(r"[\d_\-\(\)]+$", "", n)
    n = re.sub(r"\d+", "", n)
    return " ".join(sem_acento(n).split())[:38]


def main():
    caminho = os.path.join(AQUI, "plano.json")
    if not os.path.exists(caminho):
        print("nao achei plano.json")
        return 1
    plano = json.load(io.open(caminho, encoding="utf-8"))

    # Usa a MESMA validacao do sincronizar.py, nao uma parecida. O PIL abre sem
    # reclamar um JPEG que nao termina com o marcador FFD9, e o ffmpeg tambem -
    # mas o sincronizar.py descarta, e a imagem nao vira clipe. Quando eu
    # dupliquei a checagem com PIL, cinco arquivos passaram aqui e cairam la,
    # custando um render inteiro.
    quebrados = []
    try:
        import sincronizar as S
        for f in sorted(glob.glob(os.path.join(AQUI, "downloads", "paragrafo *", "*"))):
            ok, motivo = S.validar_imagem(f)
            if not ok:
                quebrados.append((os.path.relpath(f, AQUI), motivo))
    except Exception:
        print(" (PIL nao instalado - nao da para checar JPEG truncado)\n")

    problemas = 0
    for parte in plano.get("partes", []):
        n = parte["n"]
        pasta = os.path.join(AQUI, "downloads", "paragrafo %02d" % n)
        arquivos = sorted(os.listdir(pasta)) if os.path.isdir(pasta) else []
        pede = int(parte.get("midias") or 0)

        avisos = []
        if len(arquivos) < pede:
            avisos.append(("FALTA", "%d de %d" % (len(arquivos), pede)))

        bases = {}
        for a in arquivos:
            bases.setdefault(base(a), []).append(a)
        maior = max((len(v) for v in bases.values()), default=0)
        if arquivos and maior >= max(3, len(arquivos) - 1):
            materia = [k for k, v in bases.items() if len(v) == maior][0]
            avisos.append(("REPETE", "%d de %d sao '%s'" % (maior, len(arquivos), materia)))

        vocab = set()
        for frase in (parte.get("mostrar") or []):
            vocab |= palavras(frase)
        for g in (parte.get("busca") or []):
            vocab |= palavras(g)
        soltas = []
        if vocab:
            for a in arquivos:
                if not (palavras(a) & vocab):
                    soltas.append(a)
        if len(soltas) > len(arquivos) / 2.0 and soltas:
            avisos.append(("SOLTA", "%d de %d" % (len(soltas), len(arquivos))))

        if not avisos:
            continue
        problemas += 1
        print("parte %02d  %s" % (n, "   ".join("%s: %s" % a for a in avisos)))
        for a in arquivos:
            marca = "  ?" if a in soltas else "   "
            print("   %s %s" % (marca, os.path.splitext(a)[0][:70]))
        print()

    if quebrados:
        print("ARQUIVOS QUEBRADOS (conserte antes de renderizar):")
        for q, motivo in quebrados:
            print("   %-58s %s" % (q[:58], motivo))
        print()
        print('   ffmpeg -y -v error -i "ARQ" -q:v 2 _fix.jpg && mv -f _fix.jpg "ARQ"')
        print()

    if not problemas and not quebrados:
        print("Nenhuma parte com problema. Pode renderizar.")
    else:
        print("%d parte(s) sinalizada(s). So mexa em FALTA, REPETE, ou "
              "maioria SOLTA." % problemas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
