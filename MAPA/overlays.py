# -*- coding: utf-8 -*-
"""
overlays.py - texto sobre a imagem: nome, lugar, data, numero.

    py overlays.py                 aplica os overlays declarados no plano.json
    py overlays.py --amostra       gera um clipe de amostra, sem tocar em nada
    py overlays.py --listar        mostra o que seria aplicado, e onde

Roda DEPOIS do `sincronizar.py --capcut`, sobre os clipes ja prontos. Nao
altera o sincronizar.py: os clipes que nao tem overlay ficam intactos, byte
por byte, e a soma das duracoes nao muda.

------------------------------------------------------------------------------
POR QUE PIL + FFMPEG, E NAO UM MOTOR DE VERDADE

A ferramenta irma desenha overlays em React e renderiza com Remotion, que tira
UM SCREENSHOT DO CHROME POR QUADRO. Para os poucos milhares de quadros de umas
poucas cenas isso e aceitavel; foi o que inviabilizou renderizar a timeline
inteira por la.

Aqui o desenho e chapado - retangulo, linha, texto - e nao precisa de motor
nenhum. Medido nesta maquina:

    desenhar quadro com alpha (PIL)  57 quadros/s
    compor sobre o clipe (ffmpeg)    ~2 s por overlay
    -----------------------------------------------
    1 overlay pronto                 ~4,1 s
    60 overlays num video            ~4,1 min

E so os clipes QUE TEM overlay sao reprocessados - num video de 488 clipes com
60 overlays, 428 nem sao abertos.

------------------------------------------------------------------------------
COMO SE DECLARA

No plano.json, dentro da parte:

    { "n": 4, "busca": [...], "mostrar": [...],
      "overlays": [
        {"tipo": "terco", "em": 2.0, "dura": 4.5,
         "titulo": "Helmut e Erika Simon",
         "sub": "Encontraram o corpo - 19 de setembro de 1991"},
        {"tipo": "lugar", "em": 9.0, "dura": 3.5, "titulo": "Alpes de Otztal"}
      ] }

`em` e o segundo DENTRO DA PARTE, nao do video. E o unico jeito que sobrevive a
uma troca de imagens: quem escreve o plano sabe em que ponto da narracao o nome
e dito, nao em que clipe ele vai calhar de cair.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TEMP = os.path.join(AQUI, "downloads", "_overlay_tmp")
FPS = 30
LARG, ALT = 1920, 1080

# O console do Windows e cp1252 e nao escreve "-6 C" com o sinal de menos
# tipografico, nem chines, nem cirilico. Sem isto um `print` derruba o
# programa inteiro com UnicodeEncodeError - ja aconteceu tres vezes neste
# projeto, e uma vez custou a geracao de 252 clipes. Mostrar texto e
# conveniencia; o trabalho e outro. O que nao couber vira "?".
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:                                        # pragma: no cover
    Image = None


# ===========================================================================
# APARENCIA
# ===========================================================================
# Uma paleta so, num lugar so. Nenhum desenho abaixo escreve cor na mao - e o
# que impede o video de virar uma colcha de retalhos quando se acrescenta um
# tipo novo de overlay.
COR = {
    "fundo":    (10, 14, 20),          # a tarja atras do texto
    "titulo":   (255, 255, 255),
    "sub":      (206, 214, 224),
    "destaque": (232, 168, 60),        # a barra lateral, o traco sob a data
    "lugar":    (120, 190, 240),
}
OPACIDADE_FUNDO = 210                  # de 255

_FONTES = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
_ALT_FONTES = ["/usr/share/fonts/truetype/dejavu", "/Library/Fonts"]


def _fonte(tamanho, negrito=False):
    nomes = (["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"] if negrito
             else ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"])
    for pasta in [_FONTES] + _ALT_FONTES:
        for n in nomes:
            p = os.path.join(pasta, n)
            if os.path.isfile(p):
                return ImageFont.truetype(p, tamanho)
    return ImageFont.load_default()


def _largura(dr, texto, fonte):
    try:
        return dr.textbbox((0, 0), texto, font=fonte)[2]
    except Exception:
        return len(texto) * fonte.size // 2


# ===========================================================================
# A CURVA DE ENTRADA E SAIDA
# ===========================================================================
def _fase(i, total, entrada=0.35, saida=0.35):
    """Devolve (visibilidade 0..1, deslocamento 0..1) para o quadro `i`.

    A mesma licao do movimento das fotos: nada aparece nem some no susto, mas a
    animacao tambem nao pode ESTACIONAR - aqui isso importa menos porque o
    texto e chapado e nao ha reamostragem de pixel, entao da para usar uma
    curva suave de verdade nas pontas.

    `entrada` e `saida` sao em SEGUNDOS, nao em fracao: um overlay de 3s e um
    de 8s tem que entrar no mesmo ritmo, senao o de 8s parece lento.
    """
    t = i / max(total - 1, 1)
    dur = total / FPS
    fe = min(max(entrada / max(dur, 0.01), 0.05), 0.45)
    fs = min(max(saida / max(dur, 0.01), 0.05), 0.45)
    if t < fe:
        p = t / fe
    elif t > 1 - fs:
        p = (1 - t) / fs
    else:
        p = 1.0
    p = max(0.0, min(1.0, p))
    suave = p * p * (3 - 2 * p)        # smoothstep: aqui pode, e so opacidade
    return suave, 1 - suave


# ===========================================================================
# OS TIPOS
# ===========================================================================
def _tarja(dr, x, y, w, h, alpha, barra=None):
    """A tarja escura atras do texto, com a barra colorida na lateral."""
    dr.rectangle([x, y, x + w, y + h], fill=COR["fundo"] + (int(OPACIDADE_FUNDO * alpha),))
    if barra:
        dr.rectangle([x, y, x + 8, y + h], fill=barra + (int(255 * alpha),))


def _sombra(dr, x, y, texto, fonte, vis, raio=3):
    """Contorno escuro atras do texto, para ele nao sumir sobre fundo claro.

    Desenhado como oito copias deslocadas em volta - e mais barato que um
    desfoque de verdade e, num texto grande, indistinguivel dele.
    """
    a = int(150 * vis)
    if a <= 0:
        return
    for dx in (-raio, 0, raio):
        for dy in (-raio, 0, raio):
            if dx or dy:
                dr.text((x + dx, y + dy), texto, font=fonte, fill=(0, 0, 0, a))


def _desenhar(tipo, dados, i, total):
    vis, desl = _fase(i, total)
    if vis <= 0.01:
        return None
    img = Image.new("RGBA", (LARG, ALT), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    a = int(255 * vis)
    titulo = str(dados.get("titulo") or "")
    sub = str(dados.get("sub") or "")

    if tipo == "terco":
        # Terco inferior: nome de pessoa + o que ela e. Entra deslizando da
        # esquerda - o olho ja esta desse lado, porque e onde a leitura comeca.
        f1, f2 = _fonte(52, True), _fonte(30)
        x = int(110 - 70 * desl)
        y = 790
        w = max(_largura(dr, titulo, f1), _largura(dr, sub, f2)) + 70
        _tarja(dr, x - 22, y - 20, w, 124 if sub else 84, vis, COR["destaque"])
        dr.text((x, y), titulo, font=f1, fill=COR["titulo"] + (a,))
        if sub:
            dr.text((x, y + 64), sub, font=f2, fill=COR["sub"] + (a,))

    elif tipo == "lugar":
        # Selo de lugar: canto de cima, curto, em caixa alta. Nao compete com o
        # terco inferior porque nunca ocupa a mesma faixa da tela.
        f = _fonte(34, True)
        txt = titulo.upper()
        x = int(90 - 50 * desl)
        y = 80
        _tarja(dr, x, y, _largura(dr, txt, f) + 56, 66, vis, COR["lugar"])
        dr.text((x + 28, y + 16), txt, font=f, fill=(236, 242, 248, a))

    elif tipo == "data":
        # Data grande, canto direito. O numero manda; o rotulo explica.
        #
        # ALINHADO A DIREITA, e nao posicionado num x fixo. Com x fixo, "1991"
        # cabia mas o rotulo "A DESCOBERTA" vazava pela borda e saia cortado -
        # e o texto vazado so aparece depois de renderizar, nunca no codigo.
        # Ancorando na margem direita, qualquer tamanho de texto cabe.
        f1, f2 = _fonte(96, True), _fonte(28)
        y = int(150 - 40 * desl)
        direita = LARG - 110
        st = sub.upper() if sub else ""
        w1 = _largura(dr, titulo, f1)
        w2 = _largura(dr, st, f2) if st else 0
        # SOMBRA. Este e o unico tipo sem tarja atras - a tarja pesaria demais
        # num numero grande. Sem nada atras, porem, texto branco sobre neve
        # branca simplesmente some, e foi o que aconteceu no clipe do glaciar:
        # o "1991" ficou ilegivel sobre o campo de neve. A sombra resolve sem
        # sujar o desenho.
        _sombra(dr, direita - w1, y, titulo, f1, vis)
        if st:
            _sombra(dr, direita - w2, y + 136, st, f2, vis)
        dr.text((direita - w1, y), titulo, font=f1, fill=COR["titulo"] + (a,))
        traco = max(w1, w2)
        dr.rectangle([direita - traco, y + 112, direita, y + 118],
                     fill=COR["destaque"] + (a,))
        if st:
            dr.text((direita - w2, y + 136), st, font=f2, fill=COR["sub"] + (a,))

    elif tipo == "nota":
        # Cartao de apoio: um numero com uma explicacao ("5.300 anos").
        f1, f2 = _fonte(64, True), _fonte(28)
        x = int(110 - 60 * desl)
        y = 250
        w = max(_largura(dr, titulo, f1), _largura(dr, sub, f2)) + 70
        _tarja(dr, x - 22, y - 20, w, 136 if sub else 96, vis, COR["destaque"])
        dr.text((x, y), titulo, font=f1, fill=COR["titulo"] + (a,))
        if sub:
            dr.text((x, y + 76), sub, font=f2, fill=COR["sub"] + (a,))
    else:
        return None
    return img


TIPOS = ("terco", "lugar", "data", "nota")


def gerar(tipo, dados, dura, pasta):
    """Escreve a sequencia de PNG com alpha. Devolve o numero de quadros."""
    if Image is None:
        raise SystemExit("falta a Pillow:  py -m pip install pillow")
    if os.path.isdir(pasta):
        shutil.rmtree(pasta, ignore_errors=True)
    os.makedirs(pasta, exist_ok=True)
    total = max(int(round(float(dura) * FPS)), 2)
    for i in range(total):
        img = _desenhar(tipo, dados, i, total)
        if img is None:
            img = Image.new("RGBA", (LARG, ALT), (0, 0, 0, 0))
        img.save(os.path.join(pasta, "f%05d.png" % i))
    return total


# ===========================================================================
# ONDE CADA OVERLAY CAI
# ===========================================================================
def duracao(caminho):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", caminho],
            capture_output=True, text=True, timeout=30)
        return float((r.stdout or "").strip())
    except Exception:
        return 0.0


def mapa_dos_clipes(pasta="capcut"):
    """Instante inicial e final de CADA clipe na linha do tempo.

    Mede os arquivos, nao confia no plano: o `sincronizar.py` arredonda a
    duracao de cada clipe para quadro inteiro, e um erro de 30 ms por clipe
    viraria segundos de deriva ao longo de 488 deles - o overlay apareceria
    numa imagem e o nome estaria sendo dito noutra.
    """
    arq = sorted(glob.glob(os.path.join(AQUI, pasta, "*.mp4")))
    fora, t = [], 0.0
    for f in arq:
        d = duracao(f)
        fora.append({"arquivo": f, "ini": t, "fim": t + d, "dur": d})
        t += d
    return fora


def alvos(clipes, inicio, dura):
    """Quais clipes o overlay atravessa, e em que ponto de cada um.

    Um overlay de 4,5s sobre clipes de 6s cruza a fronteira quase sempre. Em
    vez de encurta-lo ou empurra-lo (as duas coisas mudariam o que foi
    escrito no plano), ele e RECORTADO e aplicado em cada clipe que toca -
    na tela isso e um overlay so, continuo.
    """
    fim = inicio + dura
    fora = []
    for c in clipes:
        a, b = max(c["ini"], inicio), min(c["fim"], fim)
        if b - a < 0.08:                 # encostou de raspao: nao vale reencodar
            continue
        fora.append({
            "clipe": c["arquivo"],
            "atraso": a - c["ini"],          # segundo dentro do clipe
            "quadro0": int(round((a - inicio) * FPS)),   # 1o quadro do overlay
            "quadros": max(int(round((b - a) * FPS)), 1),
        })
    return fora


def _preservar(clipe):
    """Guarda o clipe LIMPO antes da primeira queima, e devolve o limpo nas
    vezes seguintes.

    Overlay se queima no pixel: nao da para desfazer. E ajustar texto e uma
    coisa que se faz varias vezes - trocar uma data, encurtar um nome. Sem esta
    copia, a segunda rodada escrevia por cima da primeira e o clipe ficava com
    dois textos sobrepostos, um deles impossivel de remover sem refazer os 488
    clipes do zero.
    """
    limpo = clipe + ".limpo"
    if os.path.isfile(limpo):
        # SEGUNDA TRAVA: so restaura se a copia for do MESMO clipe. Uma copia
        # de um render anterior tem outra duracao, e restaura-la tira segundos
        # da linha do tempo sem que nada mais acuse. O sincronizar.py ja apaga
        # as copias ao refazer os clipes; isto aqui e a rede de seguranca para
        # quando alguem gera clipe por fora.
        if abs((duracao(limpo) or 0) - (duracao(clipe) or 0)) > 0.05:
            os.remove(limpo)
            shutil.copy2(clipe, limpo)
            return limpo
        shutil.copy2(limpo, clipe)      # volta ao original antes de queimar
    else:
        shutil.copy2(clipe, limpo)      # primeira vez: guarda o original
    return limpo


def limpar_preservados(pasta="capcut"):
    """Apaga as copias limpas. So depois de o video estar aprovado."""
    n = 0
    for f in glob.glob(os.path.join(AQUI, pasta, "*.limpo")):
        os.remove(f)
        n += 1
    return n


def compor(clipe, pasta_png, quadro0, quadros, atraso, log):
    """Queima a fatia do overlay no clipe. Substitui o arquivo no fim."""
    tmp = clipe + ".ov.mp4"
    filtro = (
        "[1:v]setpts=PTS-STARTPTS+%.4f/TB[ov];"
        "[0:v][ov]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]"
        % atraso
    )
    cmd = [
        "ffmpeg", "-y", "-nostdin", "-loglevel", "error",
        "-i", clipe,
        "-framerate", str(FPS), "-start_number", str(quadro0),
        "-i", os.path.join(pasta_png, "f%05d.png"),
        "-filter_complex", filtro, "-map", "[v]",
        "-frames:v", str(int(round(duracao(clipe) * FPS))),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-an", tmp,
    ]
    r = subprocess.run(cmd, capture_output=True, timeout=300)
    if r.returncode != 0:
        log("      ! nao compos em %s: %s"
            % (os.path.basename(clipe), r.stderr.decode("utf-8", "replace")[-90:]))
        if os.path.exists(tmp):
            os.remove(tmp)
        return False
    os.replace(tmp, clipe)
    return True


# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="texto sobre a imagem")
    ap.add_argument("--plano", default="plano.json")
    ap.add_argument("--relatorio", default="auto_relatorio.json")
    ap.add_argument("--capcut", default="capcut")
    ap.add_argument("--listar", action="store_true",
                    help="mostra o que seria aplicado, sem tocar em nada")
    ap.add_argument("--limpar", action="store_true",
                    help="apaga as copias .limpo (so depois de aprovar o video)")
    ap.add_argument("--amostra", action="store_true",
                    help="gera amostra_overlay.mp4 com os quatro tipos")
    args = ap.parse_args()

    def log(m):
        print(m)
        sys.stdout.flush()

    if args.limpar:
        n = limpar_preservados(args.capcut)
        log(" %d copia(s) limpa(s) apagada(s)." % n)
        if n:
            log(" A partir de agora, rodar o overlays.py de novo empilha texto:")
            log(" refaca os clipes com  py sincronizar.py --capcut  antes.")
        return

    if args.amostra:
        return amostra(log)

    cam_plano = os.path.join(AQUI, args.plano)
    cam_rel = os.path.join(AQUI, args.relatorio)
    if not os.path.isfile(cam_plano):
        sys.exit("nao achei %s" % args.plano)
    if not os.path.isfile(cam_rel):
        sys.exit("nao achei %s - rode o auto.py antes" % args.relatorio)

    plano = json.load(open(cam_plano, encoding="utf-8"))
    rel = json.load(open(cam_rel, encoding="utf-8"))
    tempos = rel.get("tempos") or []
    if not tempos:
        sys.exit("o relatorio nao tem os tempos das partes")

    clipes = mapa_dos_clipes(args.capcut)
    if not clipes:
        sys.exit("nao achei clipes em %s/ - rode o sincronizar.py --capcut antes" % args.capcut)

    # Junta tudo: overlay declarado na parte -> instante absoluto no video.
    trabalho = []
    for parte in plano.get("partes", []):
        i = int(parte.get("n", 0)) - 1
        if i < 0 or i >= len(tempos):
            continue
        base = float(tempos[i]["inicio"])
        limite = float(tempos[i]["fim"])
        for ov in (parte.get("overlays") or []):
            tipo = str(ov.get("tipo") or "terco")
            if tipo not in TIPOS:
                log(" ! parte %s: tipo de overlay desconhecido %r (use %s)"
                    % (parte.get("n"), tipo, ", ".join(TIPOS)))
                continue
            em = base + float(ov.get("em") or 0)
            dura = float(ov.get("dura") or 4.0)
            # Um overlay nao pode vazar para a parte seguinte: la a narracao ja
            # esta falando de outra coisa, e o nome na tela contradiz o audio.
            if em + dura > limite:
                dura = max(limite - em, 1.0)
            trabalho.append({"parte": parte.get("n"), "tipo": tipo, "ov": ov,
                             "em": em, "dura": dura})

    if not trabalho:
        log(" Nenhum overlay declarado no plano.")
        log(" Acrescente uma lista \"overlays\" nas partes que pedem nome, lugar ou data.")
        return

    total_clipes = sum(len(alvos(clipes, t["em"], t["dura"])) for t in trabalho)
    log("=" * 62)
    log(" %d overlay(s) declarados, tocando %d clipe(s) de %d"
        % (len(trabalho), total_clipes, len(clipes)))
    log("=" * 62)

    if args.listar:
        for t in trabalho:
            al = alvos(clipes, t["em"], t["dura"])
            log(" parte %-3s %-6s %6.1fs +%.1fs  %-34s -> %d clipe(s)"
                % (t["parte"], t["tipo"], t["em"], t["dura"],
                   str(t["ov"].get("titulo"))[:34], len(al)))
        return

    os.makedirs(TEMP, exist_ok=True)

    # Devolve ao estado limpo TODO clipe que vai ser tocado, antes de queimar
    # qualquer coisa. Tem que ser ANTES do laco: um clipe pode receber dois
    # overlays (um terco e um selo de lugar), e restaurar dentro do laco
    # apagaria o primeiro ao aplicar o segundo.
    tocados = set()
    for t in trabalho:
        for a in alvos(clipes, t["em"], t["dura"]):
            tocados.add(a["clipe"])
    restaurados = sum(1 for c in sorted(tocados) if os.path.isfile(_preservar(c)))
    log(" %d clipe(s) preparados (copia limpa guardada)" % restaurados)

    feitos, falhas = 0, 0
    for k, t in enumerate(trabalho, 1):
        pasta = os.path.join(TEMP, "ov%03d" % k)
        gerar(t["tipo"], t["ov"], t["dura"], pasta)
        al = alvos(clipes, t["em"], t["dura"])
        ok_aqui = 0
        for a in al:
            if compor(a["clipe"], pasta, a["quadro0"], a["quadros"], a["atraso"], log):
                ok_aqui += 1
            else:
                falhas += 1
        shutil.rmtree(pasta, ignore_errors=True)
        feitos += 1
        log("  %2d/%d  %-6s %-32s %d clipe(s)"
            % (k, len(trabalho), t["tipo"], str(t["ov"].get("titulo"))[:32], ok_aqui))

    shutil.rmtree(TEMP, ignore_errors=True)
    log("")
    log("=" * 62)
    log(" %d overlay(s) aplicados%s" % (feitos, (", %d falha(s)" % falhas) if falhas else ""))
    log("=" * 62)

    # A conferencia que importa: compor NAO pode ter mudado a duracao de nada.
    depois = mapa_dos_clipes(args.capcut)
    antes_t = sum(c["dur"] for c in clipes)
    depois_t = sum(c["dur"] for c in depois)
    log(" soma dos clipes: %.2fs antes, %.2fs depois  (%+.2fs)"
        % (antes_t, depois_t, depois_t - antes_t))
    if abs(depois_t - antes_t) > 0.5:
        log(" ! ATENCAO: a duracao mudou. A sincronia com o audio saiu do lugar.")
    log("")
    log(" Pode rodar de novo a vontade: os clipes tocados tem uma copia limpa")
    log(" ao lado (.limpo), entao ajustar um texto nao empilha em cima do")
    log(" anterior. Depois de aprovar o video:  py overlays.py --limpar")


def amostra(log):
    """Um clipe com os quatro tipos, para olhar antes de escrever 60 deles."""
    base = sorted(glob.glob(os.path.join(AQUI, "capcut", "*.mp4")))
    if not base:
        sys.exit("nao achei nenhum clipe em capcut/ para usar de fundo")
    fundo = base[2] if len(base) > 2 else base[0]
    os.makedirs(TEMP, exist_ok=True)
    demo = [
        ("terco", {"titulo": "Helmut e Erika Simon",
                   "sub": "Encontraram o corpo \u00b7 19 de setembro de 1991"}, 0.4, 4.0),
        ("lugar", {"titulo": "Alpes de \u00d6tztal"}, 1.0, 3.4),
        ("data",  {"titulo": "1991", "sub": "a descoberta"}, 1.6, 3.2),
        ("nota",  {"titulo": "5.300 anos", "sub": "a idade do corpo"}, 5.2, 3.4),
    ]
    shutil.copy(fundo, os.path.join(AQUI, "amostra_overlay.mp4"))
    alvo = os.path.join(AQUI, "amostra_overlay.mp4")
    for k, (tipo, dados, em, dura) in enumerate(demo, 1):
        pasta = os.path.join(TEMP, "am%d" % k)
        gerar(tipo, dados, dura, pasta)
        compor(alvo, pasta, 0, int(dura * FPS), em, log)
        shutil.rmtree(pasta, ignore_errors=True)
        log("  %s aplicado" % tipo)
    shutil.rmtree(TEMP, ignore_errors=True)
    log("")
    log(" amostra_overlay.mp4 pronto (%.1fs) - os quatro tipos, um apos o outro."
        % duracao(alvo))


if __name__ == "__main__":
    main()
