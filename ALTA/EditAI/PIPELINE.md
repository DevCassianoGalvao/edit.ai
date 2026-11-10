# Prioridades atuais do Edit.AI

As escolhas do pedido e os ajustes do painel têm prioridade sobre regras históricas abaixo. Respeite a proporção de
fotos, o estilo, o acabamento e as opções de áudio escolhidas para cada filme. Use o roteiro e a narração fornecidos.
Não gere imagens por IA automaticamente. As metas de tempo antigas são apenas referências, não garantias.

## ESTILO "ARQUIVO COLORIZADO" (04/11/2026 — pedido do usuário; referência youtu.be/hnQj4e3U8OM, história de Cuba 1898)
- Selecionável no painel (Estilos > Meus estilos > "Arquivo Colorizado (história)"); a receita completa para o Diretor está
  em painel/estilos/arquivo-colorizado.json ("receita") e entra no prompt dele (gerente.receita_estilo + diretor.md).
- Peças novas: scripts/moldura.py (foto de arquivo impressa na mesa escura/papel, etiqueta laranja LUGAR · DATA, nome+cargo,
  tag ANO | CAPÍTULO; ligado por pipeline_config "moldura_fotos" no make_photos; rótulos em data/moldura_rotulos.json),
  src/scenes/arquivo_colorizado.tsx (Polaroids, LinhaDoTempoAC, BarrasAC, DadoAC, CitacaoAC, MapaPergaminho; exemplos em
  src/exemplos/ArquivoColorizadoEx.tsx, prévias `node scripts/render_exemplos_ac.mjs [--mp4]`), legenda "serifa"
  (Garamond, public/fonts/Garamond*.ttf) e transição "fusao" (respiro escuro de ~0,6 s em todo corte, scripts/fx.py).
- Não tem: fusão cruzada de verdade entre dois planos (o acabamento só vê o filme pronto) e as recriações fotorrealistas
  coloridas por IA do original (~35 % dos planos) — aqui entram fotos colorizadas/autocromos do Commons em tela cheia.

## GERAÇÃO DE IMAGENS
- Geração automática de imagens está pausada a pedido do proprietário. Não execute serviços de geração durante a produção.

## MODO ENXUTO — 1 VÍDEO SAINDO POR HORA (12/10/2026 — regra permanente do usuário)
- **Proporção de imagens e vídeos escolhida no pedido** (photo_share; padrão 0,8); YouTube no máx. 15 por filme.
- Medido nos quebra-gelos de 12/10: o Remotion desenhava ~30 % do filme e segurava o render (42/63/77 min); 84 % disso
  eram sobreposições (paralaxe 21x, palavra, teletipo, revela, radar...). Agora (`"enxuto": true` no pipeline_config, padrão):
  cartões explicativos e estilos selecionados têm limite para manter o render leve; paralaxe máx. 5. Os destaques de
  nomes e números escolhidos no painel podem aparecer com limite moderado; estilos de gênero não são exigidos. Teste no francês: sobreposições 552 s -> 135 s no Remotion.
- Animações de tela cheia (mapa etc.) ficam. Revisão só ANTES do render; o gerente não chama mais a revisora depois da entrega.
- `"enxuto": false` no pipeline_config volta ao modo antigo (arquivo dark completo).

## META DE 2 H POR VÍDEO (10/10/2026 — regra permanente do usuário)
- Acabamento DESLIGADO (grão, vinheta, textura, tom): só cartões e motion graphics. Não religar sem o usuário pedir.
- Revisão COMPLETA ANTES do render: `fechar.py preparar` fotografa cada cartão/mapa/animação (scripts/stills_animacoes.py ->
  qa/pre_render/animacoes_*.jpg); a revisora confere cortes_*.jpg + animacoes_*.jpg; corrigir tudo; renderizar UMA vez.
  A revisora final depois da entrega só reabre por defeito GRAVE.
- Material: a Bia (busca_video.sh) faz Pexels/Pixabay + DVIDS em paralelo ao YouTube; YouTube 25 extrações/filme (35 se < 70 % foto).
- Render: NVENC p4 nos segmentos (era p7; mesma imagem, 3x mais rápido).
- Orçamento: preparar+tema ~20 min, material ~30, juízes ~15, montagem+cortes ~30, render ~30.

# Ordem do pipeline (atualizada em 24/09/2026 — fluxo RÁPIDO)

## OTIMIZAÇÃO MEDIDA (07/10/2026 — pedido do usuário: "otimização real, rápido e sem erro")
Medido no filme da Toyota (APAGAR_toyota-desmontou-byd-pt, banco de teste: scripts/bench_render.py e
scripts/bench_remotion.mjs). O render real levou 40 min e o acabamento 15-28 min; SOZINHO no PC o mesmo filme fez
ffmpeg 35 mil quadros em 5,5 min + Remotion 9,5 mil em 9,8 min (juntos ~10 min) e acabamento em 6,9 min.
Causa: a outra baia trabalhando ao lado (CLIP, checagem, cortes, Whisper) + PC parado já em ~8 de 16 GB -> memória
estourava e TUDO ficava 4-5x mais lento (uniforme, até o Remotion sozinho no fim do render).
- RENDER EXCLUSIVO (trava.py `media`): preparar, make_clips, prefilter, paralaxe e make_photos esperam o render de
  outra baia; o render espera eles acabarem (até 40 min). Download (rede) roda junto.
- PORTEIRO COM MEMÓRIA: checagem.py guarda decodificação+OCR por arquivo (data/checagem_cache.json, versão REGRA);
  rodada repetida 129 s -> 1 s. video_suspeitos.py idem (data/suspeitos_cache.json + _suspeitos_quadros/): 37 s -> 1 s.
  Mudou a regra do OCR/CLIP? subir REGRA/VER no script.
- NÃO compensou: GPU no Chrome do Remotion (gl=angle) +45-65 % mas SSIM 0,987-0,997 contra o entregue (muda a
  imagem) e o Remotion sozinho já leva ~6-10 min; "acabamento leve" só 6 %; mais abas no Remotion só +10 %.
- Revisora ANTES do render recebe marca/modelo/país (deixou passar volante Peugeot); entrega diz "espere a aprovação"
  até a revisora final (a palavra "revisado" é a marca do gerente — não usar na mensagem da entrega).
Esperado por filme de 40 min sem queda: Diretor ~1h20-1h40 (era ~1h55) + render+acabamento ~20 min (era 55-70).

## MENOS DEMORA (07/10/2026 — pedido do usuário: "tá demorando muito, me mostre as causas e as soluções")
Medido em 06/10: ~70 % da demora foram QUEDAS (15 h parado em ~25 h), ~2 h por filme esperando a cota do YouTube,
~1 h de retrabalho (preparar 3-4 vezes) e o render em fila (~1h20 por filme de 40 min, limite do PC).
- QUEDAS: tarefa do Agendador "EditAI Gerente" (ao entrar no Windows + a cada 5 min) roda painel\gerente_fundo.bat:
  se painel\gerente_vivo.py diz que há gerente vivo, sai; senão religa (laço com GERENTE_LOOP=1). Parar de vez:
  painel\.parar_gerente. Suspeito das mortes em massa: 360 Total Security — exceção para a pasta ALTA PRODUÇÃO, o
  python.exe e o claude.exe é do USUÁRIO (eu não mexo em antivírus). Ordem para um filme em andamento:
  painelila\<id>\instrucao_gerente.txt (o gerente anexa na próxima retomada).
- YOUTUBE: orçamento POR FILME em scripts/yt_quota.py (data/yt_orcamento.json, zerado pelo novo_filme.py): 40
  extrações (60 se < 70 % foto; pipeline_config "yt_max" muda). Esgotou = SemOrcamento/ORCAMENTO_ESGOTADO: Pexels,
  Commons ou foto, sem esperar (yt_quando_liberar.sh não insiste). `python scripts/yt_quota.py` mostra "este filme: N/40".
- BAIAS ESCALONADAS: o gerente só começa o 2º filme quando o 1º passou da busca de material (ou após 90 min).
- ASSUNTO CERTO NO JUIZ: juiz-fotos/juiz-video rejeitam outra marca/modelo/empresa/país (o Diretor passa
  `juizes.py preparar ... --extra "MARCA/MODELO..."`); 1 preparar para julgar + 1 para conferir, nada de 3-4.
- ACABAMENTO LEVE (opção): pipeline_config "acabamento": {"leve": true} = sem grão temporal e sem tremor, codificação
  "rapida". MEDIDO 07/10 (60 s, PC livre): forte 68 q/s x leve 72 q/s — só ~6 % (1 min num filme de 40 min). NÃO
  compensa: o custo do acabamento é decodificar o final.mp4 intermediário (~3,5 GB) e recodificar, não o grão.
  Ganho de verdade seria fundir o acabamento no render (sem a 2ª passada) — ainda não feito.

## PORTEIRO ANTES DO RENDER (05/10/2026 — pedido do usuário)
- scripts/checagem.py roda no fim do `fechar.py preparar` e de novo no começo do `fechar.py render` (se a timeline mudou).
  BLOQUEIA: clipe que não decodifica inteiro; marca d'água conhecida ou legenda larga (OCR do Windows,
  scripts/ocr_windows.ps1: foto inteira + 4 cantos ampliados 2x + 3 quadros por vídeo); apresentador/texto do
  video_suspeitos; foto do banco de outro país. O CLIP NÃO serve para foto (marca no canto = nota da foto limpa).
- Saída: data/checagem.json + qa/checagem.jpg. Alarme falso: data/checagem_aceitos.json {id: motivo}.
- Medido: BYD pt (41 vídeos + 193 fotos) 0 problemas em ~3 min; teste com clipe corrompido + VSMART + legenda: 3/3.

## FUNCIONÁRIOS SOZINHOS + ESCRITÓRIO (05/10/2026 — pedido do usuário)
- Tela ao vivo: http://127.0.0.1:8765/escritorio (botão 🏢 Escritório no painel). Dados: painel/escritorio.py (recarrega
  sozinho), lidos de gerente_estado.json, fila, .trava_pesado, fila_render.log, ~/.yt_quota.json, disco.
- Gerente: painel/gerente.py (abre junto com ABRIR_PAINEL.bat, ou LIGAR_FUNCIONARIOS.bat). Só pega pedido com
  config.json "gerente": true (botão no escritório). Abre o claude.exe do app (sem janela, -p, stream-json,
  --dangerously-skip-permissions, cwd = Downloads\mapa para ter a memória) com painel/prompts/diretor.md; o Diretor
  chama os funcionários de .claude/agents (juiz-fotos, juiz-video, revisora, pesquisador) e termina pondo o filme em
  render_e_entrega.sh. Depois da entrega o gerente abre painel/prompts/revisora_final.md (até 3 rodadas).
  Logs: painel/gerente_logs/*.jsonl.
- COM O GERENTE LIGADO o Claude do chat NÃO pega pedido do painel (só acompanha/conserta quando pedido).

## TRILHA E CARTÕES POR GÊNERO (04/10/2026 — regra do painel)
- TRILHA AUTOMÁTICA: quando ligada, o Diretor extrai do roteiro termos de assunto e clima, pesquisa faixas no
  Internet Archive e Freesound com `scripts/fetch_music.py`, mede com `scripts/audio_probe_pool.py music`, escolhe
  faixas por capítulo em `data/music_por_bloco.json` e roda `scripts/music_mix.py`. Use também o acervo local da
  Biblioteca de Áudio do YouTube. Se a busca falhar, use faixas válidas já disponíveis; sem nenhuma, desligue música
  e registre a falta na entrega. Registre fonte e licença das faixas utilizadas no plano de áudio.
- CARTÕES POR GÊNERO (src/scenes/estilos5.tsx, tipos no DOSSIE com as props de OvArquivo em src/overlays/Arquivo.tsx):
  planta (carros/motores/navios: src, titulo, cotas[{x1,y1,x2,y2,rotulo}], chamadas[{x,y,rotulo}]) ·
  caderno (arqueologia: src, titulo, local, data, notas, achado, circulo{x,y,r}) ·
  mercado (economia/agro: titulo, serie[], rotulos, valor, variacao, sobe, ticker, unidade) ·
  radar (guerra/marinha/resgate: src, titulo, coord, hora, alvos[{x,y,rotulo}]) ·
  vhs (nostalgia/marcas: src, data, slogan, marca, hora).
  Ligado no painel -> pipeline_config "cartoes_genero" -> build_overlays exige 1 a cada 3 min (36 min = 12; 2+ estilos
  ligados dividem a cota, cada um >= 3), ESPALHADOS (buraco máx = 2x o intervalo) — ERRO se faltar ou amontoar.
  Gênero fica fora do teto de 35 % por tipo; somados, até 50 % dos cartões em papel.
  Prontos novos: Carros e engenharia, Arqueologia e história antiga, Economia e crise, Militar e naval.
- 10 ESTILOS POR TEMA (04/10/2026, 3ª regra): +26 cartões em src/scenes/estilos_<tema>.tsx, registrados em
  src/overlays/temas.ts (tipo minúsculo no DOSSIE -> componente; as props do DOSSIE vão direto). Painel agrupa por tema
  (7 do tema + 3 de todo filme) com botão "ligar todos do tema"; prontos de tema ligam o tema inteiro (cota 1/3 min
  dividida: 7 ligados = 2 de cada). Demos: src/demo_<tema>/ (entrada própria, renderiza da b1 sem timeline).
  carros: velocimetro {titulo, valor, max, unidade, rotulo?, luzes?[]} · raiox {src, titulo, pecas[{x,y,rotulo}]}
    · testecolisao {src, titulo, velocidade, resultado?, nota?, marcas?[{x,y}] da TELA} · avisorecall {marca, modelo,
    defeito, unidades:number, data, carimbo?, rotulos?} · linhamontagem {titulo, total, unidade, sub?, descendo?, fim?, status?}
  arqueologia: estratigrafia {titulo, camadas[{rotulo,data}], achado, nivel} · papiro {original, traducao, fonte?}
    · etiquetamuseu {src, nome, material, data, inventario?, museu?} · datacaocarbono {titulo, anos, margem?, amostra,
    laboratorio?, unidade?} · escaneamento3d {src, titulo, pontos?[{x,y,rotulo}], hud?} · quadriculaescavacao {src,
    titulo, achados[{celula "A1".."F6", rotulo}], sitio?, escala?}
  economia: cupomfiscal {titulo, linhas[{rotulo,valor}], total, rodape?} · rankingbarras {titulo, itens[{rotulo,valor,
    destaque?}], unidade, fonte?} · rosca {titulo, pct, rotulo, sub?, cor?} · pilhadinheiro {valor "4,7 bilhões", moeda,
    rotulo, sub?, pilhas?} · contratocarimbo {titulo, partes[], valor, carimbo, data, clausula?}
  militar: dossiesecreto {titulo, linhas[] com [[palavra]] sob tarja, classificacao, data, origem?} · sonar {titulo,
    contatos[{ang,dist 0-1,rotulo,distancia?}], profundidade?} · comparaforcas {titulo, lados[{nome, cor?, itens[{rotulo,
    n, icone navio|aviao|tanque|soldado|submarino}]}]} · periscopio {src, titulo, distancia?, rumo?, modo?} ·
    placaidentificacao {linhas[] (<=5, ~22 car.), legenda?}
  nostalgia: tvtubo {src, canal?, legenda?} · anunciorevista {src, chamada, marca, preco?, ano, rodape?} · polaroids
    {fotos[{src,legenda}] (<=4), titulo?} · evolucaomarca {titulo, itens[{ano,rotulo,src?,fim?}] (<=6)} · etiquetapreco
    {produto, antigo, novo, ano_antigo, ano_novo, multiplicador?}
  Atenção: textos fixos em PT em alguns (TOTAL, FIM, ANOS) — no filme em outra língua passar os rótulos opcionais.
  Todo número no cartão (valor, cotas, ticker) é dito na narração.

## PIPELINE 50-60 MIN (04/10/2026 — pedido do usuário: "filme em 50 min a 1 h sem perder qualidade")
Medido no lote de 03-04/10 (balsa, 36 min de narração): ~3h30-4h por filme; o render sozinho dava 62 min.
Ordem nova (o que mudou está em **negrito**):
```
baias.py preparar bN          # **guarda o tema anterior em _tema_<data>/ ANTES do espelho** (antes ele se perdia)
novo_filme.py --lang L --foto F --anterior SLUG   # **transcrição com trava SÓ da GPU (.trava_gpu): roda junto com o
                              #   render de outra baia se houver >= 2400 MiB de VRAM; sem VRAM, espera** (trava.py)
python scripts/esqueleto_tema.py      # **parágrafos, números na grafia do Whisper e ANIMAÇÕES sugeridas com CUES prontos**
python scripts/pacote.py listar ; python scripts/pacote.py aplicar <nicho>   # **buscas/categorias/banco já testados**
# beats.py: PAIS = "BR"|"PL"|"US"|None e TAGS_LUGAR = [...]  -> **banco.py só serve foto desse país ou genérica**
banco.py servir-beats <slug> ; buscas ; juízes (1 rodada; **juízes com model "sonnet" no Agent**, eu confiro todas)
juizes.py juntar ; **python scripts/remapa_tags.py** (tag abaixo de 50 % da cota vira a tag coberta mais parecida —
                              #   CLIP texto x texto, mínimo 0,78, senão a REGIONAL; SEM 2ª rodada de busca)
vídeo: YouTube só dentro da cota (**DAY_MAX 160/24 h: o robô bloqueou com 169**) ; **DVIDS** (fetch_dvids.py, chave em
       %USERPROFILE%\.dvids_key) e Pexels (slot --navio) no mesmo trilho ("dv:"/"px:" -> api_review.json)
fechar.py preparar            # **build_overlays se corrige: cartão sem lugar vai p/ parágrafo vizinho (±2, arquivo ±3)
                              #   ou sai com AVISO; tipo > 35 % vira outro (fichas->palavra, palavra->cartão com a foto
                              #   do corte); tag com < 2 vídeos vira PHOTO_RUN sozinha (data/photo_run.json)**
                              # **+ video_suspeitos.py -> qa/suspeitos.jpg (apresentador/texto) — olhar ANTES do render**
fechar.py render              # **narração normaliza JUNTO com o render (remux 15 s, eram 5,5 min); audio_qa com -vn
                              #   (10 s, eram 199 s); folhas finais em paralelo**
fechar.py entregar SLUG "nome" --thumbs P --thumb-mod M **--banco tag1,tag2**   # **LEIA-ME gerado sozinho (leiame.py);
                              #   julgamento em data/notas_entrega.md**; SEMPRE guardar o aprovado no banco
```
- Etapas leves (photo_dl, make_clips, paralaxe, prefilter, fetch_*, photo_sheet, make_photos, yt_win_dl) rodam em
  prioridade BAIXA (scripts/prioridade.py): o render do crédito rural foi de 33 para 40 min com a outra baia baixando.
- Filme ENTREGUE sem --banco: `python ../baias/_ferramentas/guardar_entregue.py <data|_decisoes> <slug> <PAIS|-> <prefixo> tags...`
  (pega a foto em APAGAR_<slug>/assets/photos ou public/stock 1920 px). Em 04/10: +952 itens (pl_, navy_, br_, mar_, gen_).
- NÃO feito (precisa de validação SSIM num render real): juntar o acabamento (16 min) ao render dos segmentos e
  pré-renderizar as animações. Foto do Commons em 1920 px também não: o limite deles é nº de pedidos (~52/min), não tamanho.
- Meta: nicho conhecido (pacote + banco) ~50-60 min do pedido à entrega; tema novo ~1h30. Com 3 baias a fila entrega
  1 filme a cada ~35-60 min.

## 0. Resumo: 3 comandos meus + 3 momentos de julgamento
25/09/2026: sonda com 20 fontes (bastam para 20 % de vídeo; ~15 min em vez de ~30) e destaque automático só
quando o nome CASA com a imagem do corte (título/canal/tags; em polonês a palavra exata, no nominativo) —
acabou o re-render por "VOLKSWAGEN" sobre o BMW Welt e "WARSZAWIE" declinado.

```
python scripts/novo_filme.py --lang it --foto 0.8        # guarda o filme anterior, áudio, duração, transcreve
# escrever beats.py (com BANCO = {tag_do_filme: [tags_do_banco]}, escolhido pelo `banco.py sugerir`) + buscas
python scripts/banco.py servir-beats <slug>                # BANCO PRIMEIRO: aprovado já, sai da cota
python scripts/fetch_video.py data/yt_queries_<tema>.txt   # API do YouTube, 0 extração
python scripts/yt_lista_auto.py <tema>                     # lista de ~20 vídeos (25/09: era 36), sem escolher à mão
python scripts/yt_probe_stream.py data/yt_lista_<tema>.txt data/probe_round1.json   # ~30 min em SEGUNDO PLANO
python scripts/fetch_images.py 30 --sem-download && python scripts/fetch_images_cat.py --sem-download
python scripts/photo_dl.py --miniaturas                    # 500 px, SÓ até 3x a cota que sobrou do banco
python scripts/prefilter.py fotos
python scripts/photo_sheet.py qa/photos --demanda          # ~25-35 folhas
python scripts/juizes.py preparar 4 --pais "<país>"        # JULGAR (1) EM PARALELO: 1 agente por lote
#   (Agent x4 na mesma mensagem: "Leia .../data/juizes/lote_K.md e siga à risca.")
python scripts/juizes.py juntar                            # -> data/photo_approve.json + o que ficou abaixo da cota
#   tag abaixo da cota: photo_dl --miniaturas --mais tagX ; photo_sheet qa/photos --mais tagX ; preparar/juntar
python scripts/juizes.py conferir                          # EU confiro todas as aprovadas (_conferencia_NN.jpg)
#   reprovada na conferência: juizes.py tirar N,N
python scripts/photo_review.py
python scripts/photo_dl.py --aprovadas                     # resolução cheia só das aprovadas
python scripts/make_photos.py
# probe_sheet -> JULGAR (2) -> yt_review.json -> source_review -> yt_win_dl -> make_clips -> clip_sweep
# escrever cenas, CUES, DOSSIE
python scripts/fechar.py preparar      # plano, cues, cartões, QA, folha densa, folha corte a corte PRÉ-RENDER
#   JULGAR (3) qa/dense_*.jpg e qa/pre_render/*.jpg; ruim -> window_rejects.json -> preparar de novo
python scripts/fechar.py render        # incremental + bundle + render + áudio automático + QA + folha do MP4
python scripts/fechar.py entregar SLUG "nome" --thumbs PREF --thumb-mod make_thumb_x --banco tag1,tag2
```
O que mudou em 25/09/2026 (meta 1h10-1h30, aprovado pelo usuário):
- **Banco primeiro** (`banco.py servir-beats`): o mapa BANCO do beats.py serve fotos já aprovadas com a TAG DO
  FILME; o `demanda.py` desconta, e tag coberta não baixa nem gera folha. Só ambientação do país do roteiro.
  Repouso de 3 filmes por item continua. Item vindo do banco não é guardado de novo em outra tag.
- **Cota 3x** (era 4x, piso 18 em vez de 24): ~30 % menos pedidos ao Commons.
- **Juízes em paralelo** (`juizes.py`): tags inteiras por lote, mesmas regras, descrição da tag, trecho da
  narração, cota e tabela posição -> #N; eu confiro TODAS as aprovadas numa folha de conferência. Folhas de
  vídeo, pré-render e do MP4 continuam comigo.

O que mudou em 24/09/2026 e por quê (filme dos motores levou 6h30; meta ~2h30):
- **Miniatura primeiro** (`photo_dl --miniaturas/--aprovadas`): folha e pré-filtro com 500 px; foto cheia só
  das aprovadas. O Commons limita por NÚMERO de pedidos (~52/min com 429 e Retry-After), não por tamanho — o
  ganho vem de pedir só até a cota: 1.045 em vez de 2.234 no filme dos motores; 185 MB em vez de 7,5 GB.
- **Cota por tag** (`demanda.py`): segundos de foto de cada beat / 5,6 s por corte x 1,2 + 2. A folha só gera
  as folhas que a cota pede; título na lista de rejeição (`REJ_GLOBAL` + `rejeita_titulo` do beats) vai pro fim
  com AUTO e nem é baixado.
- **Folha corte a corte ANTES do render** (`timeline_sheet.py`): o Itaú, o carro no museu e a pedra alemã eram
  achados no MP4 final e custavam re-render. A folha do MP4 (`--mp4`) continua como confirmação.
- **Lista do YouTube automática** (`yt_lista_auto.py`): 36 vídeos por pontuação do título, sem Short e sem
  aula; a sonda roda em segundo plano enquanto escrevo cenas e cartões. A sonda passou a MESCLAR com a entrada
  da busca (antes apagava `queries`).
- **Um comando de início e um de fim** (`novo_filme.py`, `fechar.py`): acabou a troca de filme com áudio e
  duração do anterior; o volume da narração sai sozinho (`normaliza_audio.py`: acertou os motores em 1 rodada,
  -14,3 LUFS / LRA 3,9 / pico -1,2).

## PIPELINE RÁPIDO v3 (29/09/2026 — pedido do usuário: "capacidade máxima sem perder qualidade")
Medido nos 3 filmes de 29/09 (30 min cada): render 52-55 min (Remotion 26-34 + ffmpeg 21-25, EM FILA) + acabamento
50 min + normaliza 11 min. O que mudou (todas as saídas conferidas com SSIM contra o método antigo):
- `render_hybrid.py`: Remotion e ffmpeg rodam AO MESMO TEMPO (trechos diferentes do filme). `--em-fila` = modo antigo.
- `render_ranges.mjs`: UM Chrome para o filme inteiro (`openBrowser` + `puppeteerInstance`), não um por trecho.
- `acabamento.py`: o filme é cortado em 4 pedaços (fronteira a >= 1,2 s de transição/mergulho) que rodam juntos
  com 3 threads de filtro cada e são juntados sem recodificar. 19 -> 50 q/s (CPU no teto; 6x2, 6x3 e 8x2 foram piores).
  SSIM sem perda = 1,000 (a vinheta tem dither aleatório: difere até entre duas rodadas do método antigo).
  `fx.py`: textura em loop entra com `trim` no ponto do pedaço — `-ss` com `-stream_loop` recomeça CADA volta no -ss.
  pipeline_config `"acabamento_pedacos": 1` volta ao ffmpeg único.
- `normaliza_audio.py`: conta quadros por pacote (`-count_packets`); o `-count_frames` decodificava o filme (11 min).
- `dense_cuts.py`: quadros em paralelo (8) + cache em qa/_dense_cache (2ª volta do preparar só extrai o que mudou).
- `yt_lista_auto.py`: teto 20 -> 15 fontes (3 baias somadas levaram aviso de robô); tema genérico (campo, oficina,
  colheita, mar) já sai com Pexels na 1ª rodada (slot `--navio` do fetch_stock_api + data/api_review.json).
- Fotos na 1ª rodada: categoria EXATA do Commons + termo no idioma do lugar ("Josephinum", "那曲", "Hoya del Morcillo");
  tag sabidamente rara (usina, instituto, peça) com cota baixa e coberta por vídeo — evita a 2ª rodada de juízes.
- Fila de render entre baias: esperar "RENDER PRONTO|PAROU|Traceback" no log da baia anterior.
- Painel: botão "Limpar concluídos" (arquiva pedidos entregues em painel/fila_arquivo e manda APAGAR_* para a Lixeira).

## PAINEL 27/09/2026 — julgar no navegador (pedido do usuário)
`painel/ABRIR_PAINEL.bat` (ou `python painel/servidor.py`) abre http://127.0.0.1:8765. Duas abas, lendo e gravando
os MESMOS JSON do pipeline (nenhum script roda pelo painel):
- **Fotos** = JULGAR (1) sem índice #N: grava direto em `data/photo_side.json` por título (`note: "painel"`).
  Pode substituir os juízes ou servir de conferência depois do `juizes.py juntar` + `photo_review.py` (as aprovadas
  dos juízes aparecem carimbadas). Depois: `photo_dl.py --aprovadas` -> `make_photos.py`. O `photo_review.py` NÃO
  sobrescreve decisão com `note: "painel"`. Clique na foto ampliada = ponto de foco (`focus`) do recorte 16:9.
- **Linha do tempo** = JULGAR (3) com prévia sem render (narração + cortes do `timeline.json`, legenda do Whisper,
  cartões marcados, travas do build). C = `segment_rejects.json` (só aquele corte), F = `window_rejects.json` (o clipe
  sai do filme). Depois: `fechar.py preparar`; o painel avisa quando o `timeline.json` muda e pede para recarregar.
- Cópia de cada JSON antes da 1ª gravação da sessão em `painel/_backup/`; miniaturas em `painel/_cache/` (pode apagar).
- Não usar o painel enquanto `juizes.py juntar`/`photo_review.py`/`fechar.py preparar` gravam os mesmos arquivos.

### PAINEL 2ª parte (27/09/2026): fila, guias de edição, identificador de estilo
Abas novas: **Produção** (fila ao vivo), **Novo filme** (guias com prévias REAIS: legendas, cor, textura, som, cartões,
destaques, transições, render + estilos prontos), **Estilos** (identificador de edição + galeria).
Catálogo único das opções: `painel/catalogo.py` (guia -> chave do pipeline_config). Prévias: `python painel/gera_previas.py`
(mesmos filtros do filme: `acabamento.filtros()` e `legendas.gera_ass()`).

**Protocolo do Claude** (quando o usuário disser "painel" ou houver pedido na fila):
1. `Monitor` com `python painel/vigia.py` (persistente) — cada clique vira uma linha `EVENTO {...}`:
   `novo_filme`, `continuar` (etapa liberada), `recado` (texto do usuário: LER e obedecer), `pausar/retomar/cancelar`,
   `analisar_estilo`. O painel mostra "Claude conectado" enquanto o vigia estiver vivo.
2. Filme novo (um por vez, na ordem de `fila.py lista`): `fila.py estado ID preparando --status produzindo --msg ...` ->
   `fila.py preparar ID` (input/, voz limpa) -> `novo_filme.py --lang L --foto F` -> `fila.py aplicar ID` (opções -> config)
   -> pipeline normal, atualizando `fila.py estado` a cada etapa (roteiro, material...). Observações do pedido = instruções.
3. Momentos de julgar: `fila.py estado ID julgar_fotos --status esperando_voce --msg "..."` e ESPERAR o evento `continuar`
   (as decisões já estão no photo_side.json). Idem `julgar_cortes` depois do `fechar.py preparar`.
4. Antes do render: trilha/efeitos ligados -> `sound_design.py` (se sfx) + `music_mix.py` (gera public/final_audio.m4a,
   que o render_hybrid usa se for mais novo que a narração); `render.rascunho` -> `rascunho.py` (out/rascunho.mp4) e avisar.
   `fechar.py render` já aplica legendas, cor, textura, barras, nitidez, mergulho e o nível de render (acabamento.py).
5. Entregar -> `fila.py estado ID entregue --status entregue --msg "entregas/..."`, `out/legendas.srt` vai junto. Próximo da fila.
6. Estilo: `identifica_estilo.py painel/referencias/RID/video.* painel/referencias/RID --gravar slug "Nome"` (link: baixar
   com yt-dlp respeitando a cota) -> OLHAR folha_planos/folha_geral -> revisar painel/estilos/slug.json (escolhas, liga,
   "analise" em 2-3 frases, "revisado": true) -> `fila.py ref RID --status pronto --estilo slug --msg "..."`.
### PAINEL 3ª parte (28/09/2026): baias, modo automático, transições/texturas, Shorts e publicação
- **REGRA 05/10/2026 (usuário): no MÁXIMO 2 baias (b1 + b2).** Um filme montando enquanto o outro renderiza; o resto da
  fila espera a vez. Com 3 baias o render (1 por vez) virava fila, o Claude se dividia e vieram os erros de baia trocada,
  id digitado errado e disco cheio. b3 fica desligada (painel, servidor.py e baias.py `MAX_BAIAS = 2`).
- **Baias** (vários filmes ao mesmo tempo, limite no painel: "Filmes ao mesmo tempo" 1–2 = painel/config.json `paralelo`):
  b1 = esta pasta; b2/b3 = `<ALTA PRODUÇÃO>/baias/bN` (cópia de trabalho, ~1 GB). Para cada filme novo:
  `python painel/baias.py livre` -> bN -> `python painel/baias.py preparar bN` (copia o código ATUAL da b1) ->
  `python painel/fila.py baia ID bN` -> daí em diante TODOS os comandos do filme rodam com cwd na baia (o fila.py da baia
  fala com a fila central). Render (`fechar.py render`) e transcrição (`novo_filme.py`) pegam a trava `scripts/trava.py`
  (<ALTA PRODUÇÃO>/.trava_pesado): um por vez no PC; as etapas leves correm juntas. Entrega e APAGAR_ de qualquer baia
  vão para a b1 (entregas/ e APAGAR_*). Tema de filme (beats, buscas, cenas, DOSSIE) é escrito DENTRO da baia do filme.
  Filme sem baia livre fica "na fila" até outro terminar.
- **Modo automático** (config.json `auto` = padrão dos filmes novos; pedido["auto"] por filme; eventos `config` e `auto`):
  com auto, NÃO usar `--status esperando_voce`: rodar juízes + `juizes.py conferir` (EU olho todas) + tirar, e no fim da
  montagem EU julgo `qa/dense_*` e `qa/pre_render/*`; o painel mostra a mensagem mas não para. Recado "pode julgar você
  mesmo" = auto naquele filme.
- **Transições nos cortes** (`transicao.tipo`: seco|punch|flash|whip|glitch|queima|luz; `transicao.freq`: capitulos|ritmo
  (~45 s, pattern interrupt)|todos) e **texturas** (`texturas`: poeira|vhs|papel|luz_vazada): scripts/fx.py, aplicadas
  pelo `acabamento.py` na MESMA codificação final (assets em assets/fx, gerados sozinhos). Prévias: `gera_previas.py --so efeitos`.
- **Shorts 9:16** (`entrega.shorts` = N): o acabamento guarda `out/final_base.mp4` (limpo) e, depois do render,
  `python scripts/shorts.py N` -> out/shorts/ (gancho + capítulos, legenda de impacto, fundo desfocado).
- **Pacote de publicação** (`entrega.publicacao`): EU escrevo `data/publicacao.json` (5 títulos <= 70 caracteres com o
  número forte da miniatura, descrição 2–3 parágrafos, tags, 3 hashtags) -> `python scripts/publicacao.py` -> out/publicacao.md.
- `deliver.py` leva sozinho legendas-youtube.srt, publicacao.md e shorts/ para a entrega; `render.rascunho` -> `rascunho.py`.
- **Limpar concluídos** (29/09, botão na barra da fila = `python painel/fila.py limpar [--simular]`): pedidos entregue/cancelado
  -> painel/fila_arquivo/ (restaurável: "ver arquivados" ou `fila.py restaurar ID`) e cada `APAGAR_*` da raiz da b1 e de
  baias/bN -> Lixeira do Windows (nunca exclusão definitiva). Evento `limpeza` no vigia = só aviso, nada a fazer.

Chaves novas do pipeline_config: `legendas.estilo`, `acabamento.{tom: +quente|cinema, nitidez, barras, mergulho_capitulo}`,
`render.{qualidade: alta|media|rapida, rascunho}`, `arquivo_dark`, `paralaxe`, `mapa`, `sfx`, `voz_limpa`.

## REGRA 26/09/2026 — ARQUIVO DARK em TODO filme (pedido do usuário)
- DOSSIE: além de cartao/comparacao/fichas/palavra/faixa, usar os cartões de arquivo `quadro`, `checklist`, `ficha`,
  `manchete` ou `teletipo`, `lupa`, `antesdepois`, `rolo`, `revela` (todos obrigatórios; nenhum tipo > 35 %; piso 1 a
  cada 1,5 min). Espalhar pelo filme inteiro.
- Antes do `fechar.py preparar`: `python scripts/paralaxe.py --folha` (recorte do sujeito para as fotos em 2.5D).
- beats: todo capítulo com `"lugar": "LUGAR — MÊS DE ANO"` (carimbo batido à máquina na cartela).
- Scenes: pelo menos um `MapaCampanha` (src/scenes/arquivo2.tsx) ou `MapaRota`.
- pipeline_config `"acabamento": {"tom": "neutro"|"sepia"|"pb"|"frio"}` — o `fechar.py render` aplica grão, vinheta e
  tom no filme inteiro (scripts/acabamento.py).

---

# Detalhes das etapas (21/09/2026)

Seis mudanças de velocidade entraram hoje — **GPU na transcrição, NVENC no corte/render, sondar o YouTube por
streaming e baixar só as janelas aprovadas, foto renderizada pelo ffmpeg, pré-filtro das folhas e banco de
ambientação**. Nada mudou no resultado: a folha de contato continua sendo o juiz e o QA continua fechando com
0 falhas — o pré-filtro só ORDENA a folha, não aprova nem rejeita nada sozinho.

## 1. Material novo
```
ffmpeg -i input/audio.mp3 -ac 1 -ar 16000 data/audio16k.wav     # transcribe.py lê SEMPRE data/audio16k.wav
python scripts/transcribe.py pt|en|es                            # GPU: large-v3 em ~4 min para 25 min de áudio
python scripts/build_transcript.py
python scripts/beats.py                                          # reescrito por filme (tags, animações, capítulos)
```
`transcribe.py` registra as DLLs do CUDA (pacotes `nvidia-cublas-cu12` / `nvidia-cudnn-cu12`) antes de importar o
faster-whisper. Se a primeira linha do log disser "CUDA dlls: 0 pasta(s) — só CPU", a transcrição vai levar 25-50 min
em vez de 4: reinstale os dois pacotes.

## 2. Fotos (Commons)
```
python scripts/banco.py servir <slug> <tags de ambientação>   # o que o banco já tem entra APROVADO
python scripts/fetch_images.py 30 --sem-download
python scripts/fetch_images_cat.py --sem-download
python scripts/photo_dl.py                     # 3 conexões
python scripts/prefilter.py fotos              # CLIP + pHash -> data/photo_prefilter.json (~1 s por 2 fotos)
python scripts/photo_sheet.py qa/photos        # folha JÁ ORDENADA -> julgar
# data/photo_approve.json -> photo_review.py -> make_photos.py
```
O `prefilter` põe a nota do CLIP no rótulo de cada foto, ordena cada tag da melhor para a pior e joga as
quase-duplicatas (pHash) para o fim com a marca **DUP**. Continua tendo tudo na folha: o que muda é que as
primeiras folhas de cada tag são as que valem — na prática dá para parar de olhar quando a nota cai.

## 3. Vídeo do YouTube — fluxo novo (sem baixar vídeo inteiro)
```
python scripts/yt_probe_stream.py data/yt_lista_<tema>.txt data/probe_round1.json   # 1 extração/vídeo, 0 download
python scripts/probe_sheet.py data/probe_round1.json qa/probe1                      # quadros por faixa HTTP
# julgar as folhas (ladrilho com TXT = suspeita de legenda/ficha queimada) -> data/yt_review.json
python scripts/source_review.py
python scripts/yt_win_dl.py            # baixa SÓ as janelas aprovadas (--force-keyframes-at-cuts)
python scripts/make_clips.py           # corta das janelas (data/yt_slices.json) ou do vídeo inteiro, se houver
python scripts/clip_sweep.py
```
Antes: 35 vídeos inteiros = 10-15 GB e 50-70 min. Agora: ~300 MB e ~15 min.
A URL do stream expira em poucas horas — rodar a folha logo depois da sonda (para re-sondar, apague o campo
`stream` do `data/yt_pool.json`). Vídeo baixado à mão em `input/youtube/` continua funcionando como antes.

## 4. Montagem
```
python scripts/build_plan.py     # CUES/FALLBACK_TAGS/REGIONAL/PHOTO_RUN_TAGS são do tema
python scripts/fix_cues.py       # conferir o que ele troca: ele muda o CUES e as cenas
python scripts/build_plan.py && python scripts/cue_debug.py
python scripts/build_overlays.py && python scripts/qa.py       # 0 falhas e 0 avisos
python scripts/dense_cuts.py qa/dense.jpg --all                # 6 quadros por corte de vídeo -> rejeições
```

## 5. Render
```
node scripts/bundle.mjs
python scripts/render_hybrid.py --workers 2        # NVENC + fotos no ffmpeg
```
- **Fotos agora são cortes secos do ffmpeg** (`photo_filter`): no filme dos carros o Remotion caiu de 85,7 % para
  58,5 % dos quadros (o que sobra é animação, que tem de ficar no Remotion); em filme com mais foto a queda é maior.
  Validado contra o render 100 % Remotion: SSIM médio 0,978 / mínimo 0,965 / PSNR 39,8 dB (`compare_render.py`).
  `--fotos-remotion` volta ao caminho antigo.
- **NVENC** (`h264_nvenc p7 qp18`) nos segmentos e nos clipes; `--cpu` volta para o x264.
  Mesmo tamanho e mesma qualidade do x264 crf16, ~2,4x mais rápido, e não ocupa os 12 núcleos.
- A junção continua SEM RECODIFICAR: os segmentos do NVENC e os do Remotion (x264) são ambos H.264 High@4.0.

## 6. Entrega
```
python scripts/final_mp4_sheet.py        # conferir o MP4 final na folha
python scripts/make_thumb_<tema>.py      # 5 miniaturas (foto do Commons em alta, Anton, número dito na narração)
python scripts/make_attribution.py
python scripts/deliver.py <slug> "<nome do mp4>" --thumbs <prefixo> --thumb-mod make_thumb_<tema>
python scripts/banco.py guardar <slug> <tags de ambientação>   # antes de apagar o material pesado
```
O `banco guardar` copia para `..anco` as fotos de AMBIENTAÇÃO aprovadas (com licença e autor na ficha) e
anota quais foram ao ar. O `banco servir` do próximo filme pula as que saíram nos últimos 3 filmes, então o
mesmo plano de fundo não aparece em vídeos seguidos. O ASSUNTO do filme nunca entra no banco.

## Armadilha corrigida em 21/09/2026
`src/design/grade.ts` fica com `ativo: true` depois de um filme ULTRA e não é regerado no modo padrão. O Remotion
aplicava a grade (contraste/saturação/tinte/vinheta) nas FOTOS e o ffmpeg deixava os VÍDEOS crus — dois visuais no
mesmo filme. Agora os dois lados olham para `pipeline_config.modo == "ultra"`.

## Animações = JavaScript/Remotion (REGRA FIXA do usuário, 25/09/2026)

Toda animação é código (React + Remotion); After Effects só para peça-assinatura única do canal (abertura,
transição fixa), que entra como vídeo pronto. Ordem: usar a biblioteca antes de escrever cena nova.
- `src/scenes/biblioteca.tsx`: **MapaRota** (lugares lat/lon, rota cresce até cada lugar NO CUE dele, contador
  opcional, `linhas` para rio/fronteira, `marca` para destino fora da rota; projeção se encaixa sozinha),
  **Odometro** (valor rola no cue, `prefixo/sufixo`, `nota`, até 4 `barras`, `foto` de fundo),
  **Documento** (`linhas`, `chave` = linha com marca-texto, `carimbo` no cue), **FotoMedidor** (foto aprovada,
  `de/ate/unidade`, `efeito` gelo | calor | fundo | nenhum).
- `blocos.tsx`/`Painel.tsx`: Painel, Barras, LinhaDoTempo, Lista, Colunas.
- Por filme: pelo menos 2 tipos; nenhum tipo em mais da metade das animações. Lugar -> MapaRota;
  número-recorde -> Odometro; relatório/processo/carta -> Documento; medida extrema com foto -> FotoMedidor.
- Separador de milhar pelo idioma com `sep` ("," en; "." pt/it/es/de; " " pl/fr) — sem toLocaleString.
- Continua: teto de 1 animação de tela cheia a cada 3 min; número dito; cue = palavra dentro da janela.
- Uso na cena do filme: `export const A03Rota: React.FC<SceneProps> = (p) => <MapaRota {...p} kicker=... lugares={[...]} />`
  e a palavra de cada `cue` vai no CUES do build_plan.py. Modelo completo: `src/exemplos/Exemplos.tsx`;
  vitrine/teste: `node scripts/render_exemplos.mjs` -> `out/exemplos` (~40 s).

## Destaques e cartões sobrepostos (21/09/2026)

`src/overlays/Destaques.tsx` (destaque, etiqueta, numero, faixa, comparativo) e `src/overlays/Cartoes.tsx`
(cartao, comparacao, fichas, palavra) entram pelo campo `ov` do corte, igual aos gráficos ULTRA. Estilo do filme
em `data/pipeline_config.json` -> `estilo_destaque` (documentario | dinamico | tecnico).
Prévia sem render do filme: `node scripts/demo_destaques.mjs` -> `out/demo/*.png`.

`destaque` (nome próprio/ano) e `numero` (valor + unidade) saem SOZINHOS do roteiro — `build_overlays.py` lê
`data/master_transcript.json`, usa a grafia do ROTEIRO (o Whisper escreve "Sema Hill" para "Cima Hill") e o
instante das palavras. Ajuste por filme: `NOMES_FORA`, `DESTAQUE_FIXO`, `NUMEROS_FORA`, `NUMEROS_ROTULO`.
Os cartões em papel vêm da tabela `DOSSIE` (uma linha por cartão, com `para` e `src` de public/).
Travas: nada por cima de animação; 12 s de um gráfico grande; 14 s entre dois pequenos; teto de 26 destaques
e 14 números. No filme do Mojave: 23 gráficos -> 28, sendo 8 destaques e 3 números automáticos.

## Cota do YouTube (22/09/2026)

A trava de 280 extracoes/24 h e minha (`yt_quota.py`), nao do YouTube: e o volume em que o aviso de robo apareceu.
Um filme custava ~140 extracoes (45 de busca + 52 de sonda + 40 de download). Agora:
- **busca pela YouTube Data API v3** (`fetch_video.py`, chave em `data/youtube_api_key.txt`): 0 extracoes; a API tem
  cota propria de 10.000 unidades/dia (~95 consultas de 30 resultados). Sem chave ou com a cota da API cheia, cai no yt-dlp.
- **download sem extrair de novo**: a sonda guarda o JSON completo em `data/yt_info/<id>.json` e o `yt_win_dl.py` baixa
  as janelas com `--load-info-json` (URL do stream vale ~6 h; passado isso ele extrai normalmente).
Resultado esperado: ~52 extracoes por filme, so as da sonda.

**22/09/2026: o usuario subiu DAY_MAX de 280 para 400** (a cota da API de busca continua sendo o outro
teto: 10.000 unidades/dia = ~95 consultas). Com ~52 extracoes por filme, 400 da ~7 filmes/dia pelo lado
do yt-dlp. MIN_GAP de 45 s e a pausa de 3 h no aviso de robo NAO mudaram — se o aviso aparecer, voltar
DAY_MAX para 280 e anotar quantas extracoes tinham sido feitas.

### ACABAMENTO NA PLACA (09/10/2026)
- scripts/acabamento.py: nitidez (unsharp_opencl) e vinheta (kernel OpenCL data/_vinheta.cl, fórmula do vf_vignette) rodam na
  NVIDIA; cor e grão no processador; gravação NVENC p4 (mesma qualidade do p6 medida, o teto de 12 Mbps manda).
  Medido (3 min de filme, 4 pedaços, baias trabalhando): processador 169 s x placa 22 s; SSIM 0,987 entre os dois.
  Desligar: pipeline_config "acabamento_gpu": false, ou `python scripts/acabamento.py --cpu`. Sem OpenCL cai no processador sozinho.
- Luz vazada desligada por padrão (texturas.luz_vazada=false) — era a parte mais cara (blend em RGB).
- Testado e NÃO adotado: Remotion com gl=angle/vulkan (mais lento e muda a imagem); 2 renders juntos (1,68x o tempo, memória
  livre mín. 0,9 GB num PC de 16 GB); juntar acabamento ao render (ler+gravar custa só ~3 min).
