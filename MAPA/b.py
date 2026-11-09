#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
projeto_capcut.py — cria um PROJETO DO CAPCUT ja montado.

As imagens e os videos entram na linha do tempo com o tempo exato de cada
um, a narracao entra na trilha de audio e a legenda vem do .srt. Voce abre
o CapCut e esta tudo lá — nao precisa arrastar nada.

Video mais curto que o tempo que sobrou pra ele na linha do tempo nao vira
tela preta nem corta feio: se faltar pouco, ele fica em leve camera lenta
(ate ~2.5x mais devagar); se faltar muito, ele repete (loop) quantas vezes
precisar para preencher o trecho todo, sempre batendo o tempo certinho.

ANTES DE USAR (uma vez so):
    pip install pycapcut

COMO USAR:
    1. Rode o sincronizar.py normalmente (ele gera o linha_do_tempo.json):
           python sincronizar.py --chars 500
       Nao precisa usar --capcut nem --montar.

    2. Descubra a pasta de rascunhos do CapCut:
       CapCut -> Configuracoes globais -> Local do rascunho (ou "Draft location")

    3. Rode:
           python projeto_capcut.py --pasta "C:\\caminho\\da\\pasta\\de\\rascunhos"
           
       Se nao passar --pasta, ele tenta achar sozinho.

    4. Abra o CapCut. O projeto aparece na lista inicial.
       (Pode ser preciso reiniciar o CapCut para a lista atualizar.)
"""

import argparse
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".deps"))
from collections import OrderedDict

# Video mais curto que a fatia dele na linha do tempo: ate essa razao
# (fatia / duracao_real_do_video) ele fica em camera lenta; acima disso,
# em vez de ficar lento demais, repete o video (loop) quantas vezes precisar.
LIMITE_LENTIDAO_VIDEO = 2.5


def planejar_segmentos_video(mat_dur_us, alvo_ini_us, alvo_dur_us):
    """Decide como cobrir 'alvo_dur_us' (a fatia da linha do tempo que esse
    video ganhou) usando um material que só tem 'mat_dur_us' de video de
    verdade. Devolve uma lista de (inicio_alvo, duracao_alvo, inicio_fonte,
    fim_fonte, velocidade) - um item da lista por segmento a adicionar na
    trilha (quase sempre so 1; vira mais de 1 quando precisa repetir o
    video em loop). A soma das durações sempre bate exatamente com
    'alvo_dur_us', pra não desalinhar o que vem depois."""
    if mat_dur_us <= 0:
        return []
    if mat_dur_us >= alvo_dur_us:
        # video ja e mais longo (ou igual) que a fatia -> so corta, sem loop
        return [(alvo_ini_us, alvo_dur_us, 0, alvo_dur_us, 1.0)]

    razao = alvo_dur_us / mat_dur_us
    if razao <= LIMITE_LENTIDAO_VIDEO:
        # falta pouco: estica em camera lenta pra cobrir a fatia inteira
        # num unico segmento (sem corte seco no meio)
        return [(alvo_ini_us, alvo_dur_us, 0, mat_dur_us, mat_dur_us / alvo_dur_us)]

    # falta muito: repete o video (loop) ate cobrir o tempo todo. O ultimo
    # pedaco, se sobrar bem pequeno (<0.3s), e absorvido no pedaco anterior
    # como uma leve camera lenta, em vez de virar um cortinho isolado.
    partes = []
    pos = alvo_ini_us
    restante = alvo_dur_us
    while restante > 0:
        pedaco = min(mat_dur_us, restante)
        if restante - pedaco < 300000 and partes:
            ini_alvo, dur_alvo, fsrc_ini, fsrc_fim, _ = partes[-1]
            nova_dur = dur_alvo + restante
            nova_spd = (fsrc_fim - fsrc_ini) / nova_dur
            partes[-1] = (ini_alvo, nova_dur, fsrc_ini, fsrc_fim, nova_spd)
            restante = 0
            break
        partes.append((pos, pedaco, 0, pedaco, 1.0))
        pos += pedaco
        restante -= pedaco
    return partes


CANDIDATOS = [
    r"%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft",
    r"%LOCALAPPDATA%\CapCut Drafts",
    r"%USERPROFILE%\Documents\CapCut Drafts",
    r"%LOCALAPPDATA%\JianyingPro\User Data\Projects\com.lveditor.draft",
    os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft"),
]


def achar_pasta_rascunhos():
    for bruto in CANDIDATOS:
        caminho = os.path.expandvars(bruto)
        if "%" not in caminho and os.path.isdir(caminho):
            return caminho
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", default=None,
                    help="pasta de rascunhos do CapCut")
    ap.add_argument("--nome", default="roteiro_sincronizado",
                    help="nome do projeto que aparecera no CapCut")
    ap.add_argument("--json", default="linha_do_tempo.json")
    ap.add_argument("--sem-legenda", action="store_true",
                    help="nao importar o .srt")
    args = ap.parse_args()

    try:
        import pycapcut as cc
        from pycapcut import trange
    except ImportError:
        print("=" * 60)
        print(" A biblioteca pycapcut nao esta instalada.")
        print(" Rode primeiro:")
        print("     pip install pycapcut")
        print("=" * 60)
        sys.exit(1)

    if not os.path.exists(args.json):
        sys.exit("Nao achei %s. Rode o sincronizar.py primeiro." % args.json)

    with open(args.json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    itens = dados.get("itens") or []
    if not itens:
        sys.exit("O linha_do_tempo.json esta vazio.")

    pasta = args.pasta or achar_pasta_rascunhos()
    if not pasta:
        print(" Nao consegui achar a pasta de rascunhos do CapCut sozinho.")
        print(" Abra o CapCut -> Configuracoes globais -> Local do rascunho,")
        print(" copie o caminho e rode de novo assim:")
        print('     python projeto_capcut.py --pasta "COLE O CAMINHO AQUI"')
        sys.exit(1)
    if not os.path.isdir(pasta):
        sys.exit("Essa pasta nao existe: %s" % pasta)

    print(" Pasta de rascunhos: %s" % pasta)

    # Rede de seguranca: o CapCut recusa o projeto se dois segmentos se
    # tocarem por 1 microssegundo. Aqui a gente garante que cada imagem
    # termina exatamente onde a proxima comeca.
    itens.sort(key=lambda x: int(x["inicio_us"]))
    ajustes = 0
    for i in range(len(itens) - 1):
        atual, proximo = itens[i], itens[i + 1]
        limite = int(proximo["inicio_us"]) - int(atual["inicio_us"])
        if limite <= 0:
            proximo["inicio_us"] = int(atual["inicio_us"]) + max(int(atual["duracao_us"]), 33333)
            ajustes += 1
        elif int(atual["duracao_us"]) != limite:
            atual["duracao_us"] = limite
            ajustes += 1
    if ajustes:
        print(" (%d ajuste(s) de milesimo para evitar sobreposicao)" % ajustes)

    print(" Conferindo se a biblioteca aceita cada imagem/vídeo...")
    materiais = {}
    rejeitados = []
    for i, item in enumerate(itens, 1):
        caminho = item["arquivo"]
        if not os.path.exists(caminho):
            rejeitados.append((caminho, "arquivo nao encontrado"))
            continue
        try:
            materiais[caminho] = cc.VideoMaterial(caminho)
        except Exception as e:
            rejeitados.append((caminho, "%s" % type(e).__name__))
        if i % 50 == 0:
            print("   %d de %d..." % (i, len(itens)))

    # O tempo de uma imagem rejeitada passa para a imagem anterior, para a
    # linha do tempo nao encurtar nem abrir buraco.
    # O tempo de uma imagem rejeitada fica DENTRO do mesmo paragrafo sempre
    # que possivel: e redistribuido soh entre as imagens boas daquele mesmo
    # trecho da narracao (mesmo assunto). Antes, esse tempo era simplesmente
    # jogado para a imagem anterior na lista inteira - se essa imagem
    # anterior fosse de um PARAGRAFO/ASSUNTO diferente (ex: a ultima imagem
    # do paragrafo da Nissan), ela ficava esticada na tela tempo suficiente
    # para "vazar" para dentro da fala do proximo assunto (ex: Chevrolet).
    # E exatamente esse o efeito de imagem trocada/atrasada relatado pelo
    # usuario.
    grupos = OrderedDict()
    for item in itens:
        grupos.setdefault(item.get("paragrafo"), []).append(item)

    paragrafos_ok = []      # [(numero, [item valido, ...]), ...] em ordem
    paragrafos_vazios = []  # paragrafos que perderam TODAS as imagens

    for numero, grupo in grupos.items():
        total_us = sum(int(it["duracao_us"]) for it in grupo)
        validos = [it for it in grupo if it["arquivo"] in materiais]
        if not validos:
            paragrafos_vazios.append((numero, total_us))
            continue
        # mantem o tempo TOTAL do paragrafo igual ao original, so redistribui
        # entre as imagens que sobraram (proporcional ao peso de cada uma)
        soma_validos = sum(int(it["duracao_us"]) for it in validos)
        fator = (total_us / soma_validos) if soma_validos else 1.0
        for it in validos:
            it["duracao_us"] = int(round(int(it["duracao_us"]) * fator))
        paragrafos_ok.append((numero, validos))

    # so quando um paragrafo INTEIRO ficou sem nenhuma imagem valida e que o
    # tempo dele precisa ir para um paragrafo vizinho (nao tem outro jeito,
    # senao o video encurtaria) - prefere o paragrafo seguinte, para nao
    # esticar uma imagem de um assunto ja encerrado.
    for numero, dur in paragrafos_vazios:
        alvo = next((i for i, (n2, _) in enumerate(paragrafos_ok)
                     if n2 is not None and numero is not None and n2 > numero),
                    None)
        if alvo is None and paragrafos_ok:
            alvo = len(paragrafos_ok) - 1
        if alvo is not None:
            _, grupo_alvo = paragrafos_ok[alvo]
            extra = dur / len(grupo_alvo)
            for it in grupo_alvo:
                it["duracao_us"] = int(it["duracao_us"]) + int(extra)

    guardados = [it for _, grupo in paragrafos_ok for it in grupo]

    if not guardados:
        sys.exit("Nenhuma imagem ou vídeo pode ser usado. Nada a fazer.")

    # recalcula os inicios em sequencia, encostados
    posicao = 0
    for item in guardados:
        item["inicio_us"] = posicao
        posicao += int(item["duracao_us"])

    if rejeitados:
        print(" %d arquivo(s) que a biblioteca nao abre (tempo repassado):"
              % len(rejeitados))
        for caminho, motivo in rejeitados[:8]:
            print("   - %s  (%s)" % (os.path.basename(caminho), motivo))
        if len(rejeitados) > 8:
            print("   ... e outras %d" % (len(rejeitados) - 8))

    itens = guardados
    print()
    print(" Montando o projeto '%s' com %d imagem(ns)/vídeo(s)..." % (args.nome, len(itens)))

    draft_folder = cc.DraftFolder(pasta)

    # Se o projeto ja existe (tentativa anterior), substitui.
    script = None
    for tentativa in (
        lambda: draft_folder.create_draft(
            args.nome, dados.get("largura", 1920), dados.get("altura", 1080),
            fps=dados.get("fps", 30), allow_replace=True),
        lambda: draft_folder.create_draft(
            args.nome, dados.get("largura", 1920), dados.get("altura", 1080),
            allow_replace=True),
        lambda: draft_folder.create_draft(
            args.nome, dados.get("largura", 1920), dados.get("altura", 1080)),
    ):
        try:
            script = tentativa()
            break
        except TypeError:
            continue
        except FileExistsError:
            # apaga a pasta do projeto antigo e tenta de novo
            import shutil
            antigo = os.path.join(pasta, args.nome)
            if os.path.isdir(antigo):
                print(" Removendo o projeto anterior '%s'..." % args.nome)
                shutil.rmtree(antigo, ignore_errors=True)
            try:
                script = tentativa()
                break
            except Exception:
                continue

    if script is None:
        print()
        print(" Nao consegui criar o projeto. Duas saidas:")
        print("   1) apague a pasta abaixo na mao e rode de novo:")
        print("      %s" % os.path.join(pasta, args.nome))
        print("   2) use outro nome:")
        print('      python projeto_capcut.py --nome "video2"')
        sys.exit(1)

    # trilha de imagens e vídeos
    script.add_track(cc.TrackType.video, "cenas")
    faltando = []
    postas = 0
    videos_esticados = 0
    videos_repetidos = 0
    for i, item in enumerate(itens, 1):
        caminho = item["arquivo"]
        try:
            mat = materiais[caminho]
            alvo_ini = int(item["inicio_us"])
            alvo_dur = int(item["duracao_us"])

            # vídeo real mais curto que a fatia que ele ganhou na linha do
            # tempo -> em vez de estourar (o pycapcut recusa um corte maior
            # que o material) ele fica em câmera lenta ou repete em loop.
            # Imagem tem duração "infinita" pra essa lógica (nunca cai aqui).
            if mat.material_type == "video" and mat.duration < alvo_dur:
                plano = planejar_segmentos_video(mat.duration, alvo_ini, alvo_dur)
                if len(plano) > 1:
                    videos_repetidos += 1
                elif plano:
                    videos_esticados += 1
                for (t_ini, t_dur, s_ini, s_fim, spd) in plano:
                    seg = cc.VideoSegment(
                        mat, trange(t_ini, t_dur),
                        source_timerange=trange(s_ini, s_fim - s_ini), speed=spd,
                    )
                    script.add_segment(seg, "cenas")
            else:
                seg = cc.VideoSegment(mat, trange(alvo_ini, alvo_dur))
                script.add_segment(seg, "cenas")
            postas += 1
        except Exception as e:
            faltando.append("%s (%s)" % (os.path.basename(caminho), e))
        if i % 25 == 0:
            print("   %d de %d..." % (i, len(itens)))

    if videos_esticados or videos_repetidos:
        print(" %d vídeo(s) mais curto(s) que a fatia deles ficaram em câmera "
              "lenta; %d precisaram repetir (loop) pra preencher o tempo."
              % (videos_esticados, videos_repetidos))

    # trilha da narracao
    audio = dados.get("audio")
    if audio and os.path.exists(audio):
        script.add_track(cc.TrackType.audio, "narracao")
        material = cc.AudioMaterial(audio)
        script.add_segment(
            cc.AudioSegment(material, trange(0, material.duration)),
            "narracao",
        )
        print(" Narracao adicionada: %s" % os.path.basename(audio))
    else:
        print(" ! sem narracao (arquivo nao encontrado)")

    # legendas
    srt = dados.get("srt")
    if srt and os.path.exists(srt) and not args.sem_legenda:
        try:
            script.import_srt(srt, track_name="legenda")
            print(" Legendas importadas: %s" % os.path.basename(srt))
        except Exception as e:
            print(" ! nao consegui importar a legenda: %s" % e)

    script.save()

    print()
    print("=" * 60)
    print(" PRONTO! Projeto '%s' criado." % args.nome)
    print(" %d de %d imagem(ns)/vídeo(s) na linha do tempo." % (postas, len(itens)))
    print(" Duracao: %.1f minutos." % (dados.get("duracao_total_us", 0) / 60000000))
    print("=" * 60)
    print(" Abra o CapCut e procure o projeto na tela inicial.")
    print(" Se nao aparecer, feche e abra o CapCut de novo.")
    print("=" * 60)
    if faltando:
        print(" ! %d arquivo(s) falharam ao entrar:" % len(faltando))
        for aviso in faltando[:5]:
            print("   - %s" % aviso)


if __name__ == "__main__":
    main()
