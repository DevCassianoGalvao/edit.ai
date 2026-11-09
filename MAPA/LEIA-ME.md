# THANOS 3.0

A **2.0 continua intacta** na pasta dela. Esta é uma cópia completa dela com
três camadas novas por cima. Nada do que já funcionava foi removido.

## Novidades (portadas do projeto TESTE)

**Conferência de imagem sem gastar cota — `clipcheck.py` + aba "🖥️ CLIP local"**
Na barra lateral, além de Gemini/Claude, agora tem **CLIP local**: um modelo que
roda na sua máquina (via `onnxruntime`), compara cada foto com o trecho narrado
e descarta o **assunto errado**. Grátis, **sem limite**, offline. Não lê texto
na imagem (não pega marca d'água), mas resolve o caso que mais escapa.
1ª vez: `pip install onnxruntime huggingface_hub tokenizers pillow` (o modelo,
~600 MB, baixa sozinho).

**Wikimedia sem 429 — `bancos.py`**
Com um token OAuth pessoal (grátis) o limite sobe de ~500 → 5000 req/h e o 429
some. Já vem configurado em `wikimedia_token.txt`. Pra trocar: registre em
`meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose/oauth2`
("for use only by você", "Applicable project" = `*`, grant "Basic rights").
Também: freio adaptativo + **cache em disco** (`downloads/_cache_bancos.json`) —
um vídeo re-buscado no dia seguinte reaproveita tudo.

**`visao.py`**: modelo do Gemini corrigido (`gemini-flash-latest` devolvia vazio
→ agora `gemini-2.5-flash`), e provedor `groq` adicionado.

**Trava de assunto único — `buscador-imagens.html`**
Quando o roteiro fala do começo ao fim de UMA coisa só (um veículo, uma pessoa,
um lugar), a ferramenta detecta isso sozinha (`detectAssuntoUnico`) e passa a
tratar TODA parte — inclusive as de apoio — como essa coisa num plano/cenário
diferente. Acaba o caso da metáfora virando busca: *"sempre carregando debaixo
do capô..."* dava a busca `battery charging plug armored vehicle` e enchia a
parte de carregador de bateria da Walmart; agora dá `EE-9 Cascavel motor`. A
frase de busca deixa de ser despejada no "precisa mostrar" (era o que deixava
`battery` sozinho aprovar qualquer coisa), o nome do assunto vira exigência
dura na curadoria, e a checagem de visão (CLIP/Gemini) julga contra o assunto
de verdade, não contra a frase que derivou.

**Guarda de roteiro desatualizado — `buscador-imagens.html`**
Colar um roteiro/áudio novo e buscar imagens **sem clicar em "Analisar"** de novo
usava o contexto (tema, âncora, entidades) e as buscas do vídeo ANTERIOR. Agora:
`startAnalysis` zera todo o estado do vídeo anterior no topo (não só no meio, onde
um erro deixava sobra), e guarda em `textoAnalisado` o texto exato que gerou as
partes. `Rebuscar`, `Olhar`, `Gerar cenas` e o `Sincronizar com áudio` checam
contra isso: se a caixa mudou, bloqueiam com aviso e mostram um banner fixo
"O roteiro mudou — clique em Analisar de novo". Editar a caixa depois de analisar
já acende o banner sozinho.

---

```bash
py servidor.py
```

Abra **http://localhost:8003/**

## O caminho inteiro, do roteiro ao vídeo

1. Cole o roteiro
2. Escolha o áudio → **🎙️ Transcrever e sincronizar**
3. **Analisar e buscar imagens**
4. Use **👁 Olhar** nas partes que quiser conferir, e **✨ Motion** onde couber uma cena
5. **⬇ Baixar TODAS** no rodapé
6. **🎞 Preparar montagem** ← escreve `legenda.srt`, `roteiro.txt` e `partes.json`
7. No cmd, dentro desta pasta:

```bash
py sincronizar.py --capcut
```

```bash
py b.py
```

> **O passo 6 não é opcional.** O `sincronizar.py` procura um `legenda.srt` na
> pasta e não roda sem ele. Antes você teria que gerar essa legenda por fora,
> num site — o que é pedir duas vezes a mesma coisa, já que a transcrição do
> Whisper tem o tempo de **cada palavra**. O botão escreve os três arquivos de
> uma vez.
>
> O `py b.py` monta o projeto do CapCut e precisa de `pip install pycapcut` uma
> vez só. Se você não usa CapCut, pule: o `--capcut` já deixou os clipes
> cortados na pasta `capcut/`, prontos para arrastar para qualquer editor.

> A 3.0 sobe na porta **8003** de propósito — dá pra deixar a 2.0 rodando na
> 8000 ao mesmo tempo e comparar. Para forçar outra porta: `py servidor.py 8010`

---

# Começando um vídeo novo

Use o botão **🆕 Começar um vídeo novo** na lateral. Ele mostra as duas listas
— o que vai apagar e o que vai manter — e só apaga depois que você confirmar.

| apaga | mantém |
|---|---|
| `downloads/paragrafo NN/` (todas) | `cookies.txt` — o acesso ao YouTube |
| `downloads/motion/`, `_motion_tmp/` | `downloads/_transcricoes/` — o cache |
| `downloads/partes.json` | seus áudios (`.mp3`) |
| `capcut/` | `video.mp4` já exportado |
| `legenda.srt`, `roteiro.txt` | os arquivos da ferramenta |
| `linha_do_tempo.json`, `mapa.csv`, `mapa.json`, `concat.txt`, `comando.txt` | |

**Por que isso virou botão em vez de uma lista para decorar:** o pior caso é
silencioso. Se sobram as pastas `paragrafo NN` do vídeo anterior, o
`sincronizar.py` conta 39 pastas contra as 20 partes do roteiro novo, e a imagem
cai no trecho errado da fala. O vídeo sai **inteiro e errado** — que é pior do
que sair quebrado, porque você só descobre assistindo.

O botão também limpa a **memória da página** (sincronia, partes, domínio do
roteiro). Apagar só os arquivos deixaria os tempos do vídeo velho valendo para o
roteiro novo — exatamente o erro que ele existe para evitar.

### Ou: `LIMPAR TUDO.cmd`

Para começar do zero de verdade, dê **dois cliques** em `LIMPAR TUDO.cmd` na
pasta. Ele mostra as duas listas, pede um **S** de confirmação e apaga tudo que
pode atrapalhar o vídeo novo — inclusive a **narração** e o **roteiro**, que o
botão da página preserva.

Apaga: `downloads/paragrafo NN`, `downloads/motion`, `_motion_tmp`,
`_transcricoes`, `partes.json`, `capcut/`, `legenda.srt`, `roteiro.txt`, os
áudios (`.mp3 .wav .m4a .aac .ogg .flac`), `linha_do_tempo.json`, `mapa.csv`,
`mapa.json`, `concat.txt`, `comando.txt`, `video.mp4`.

Mantém: `cookies.txt` e os arquivos da ferramenta.

> Ele pede confirmação de propósito: a narração é material de origem e um duplo
> clique acidental não pode levá-la embora sem aviso. Qualquer tecla que não
> seja **S** cancela sem apagar nada.

### O áudio é perguntado à parte

A narração **não** entra na limpeza junto com o resto — ela é perguntada numa
segunda pergunta, com o nome e o tamanho do arquivo:

```
Apagar também a narração?

   narracao.mp3 (23.8 MB)

OK = apaga (você vai usar uma narração nova)
Cancelar = mantém o arquivo na pasta
```

O motivo: o `.mp3` é o seu **material de origem**, não um subproduto da
ferramenta. Apagar arquivo de origem junto com o resto, sem perguntar, é o tipo
de coisa que não se desfaz.

E tinha uma armadilha nisso: a lista de áudios se escolhe sozinha quando há um
só arquivo na pasta — e depois da limpeza sobrava exatamente um, o **do vídeo
anterior**. Bastava colar o roteiro novo e sincronizar para casar o texto novo
com a narração antiga. Agora, depois de limpar, a lista **não se auto-escolhe**:
a escolha do áudio passa a ser deliberada, e a tela avisa que a narração
anterior continua ali.

> O cache de transcrição fica de propósito: ele é indexado pelo conteúdo do
> áudio, então nunca serve o áudio errado, e poupa minutos se você reaproveitar
> uma narração.

---

# Camada 1 — Vídeo do YouTube, sem API

Vá em **O que buscar → 🎬 Vídeos** (ou **Ambos**).

- **Sem API, sem chave, sem conta.** Roda em cima do `yt-dlp`.
- No modo **🎬 Vídeos** nem a chave da Serper.dev é necessária: o roteiro
  inteiro roda de graça.
- **Nunca baixa o vídeo inteiro.** Pede ao YouTube só uma fatia (padrão 20s,
  ajustável de 5 a 60s), já cortada durante o download (`--download-sections`).
  Um vídeo de 40 minutos vira um arquivo de 20 segundos.

### O filtro — o lixo não chega na tela

Para cada parte, o app pede **40 resultados** e joga fora antes de mostrar:

| descartado | descartado | descartado |
|---|---|---|
| gameplay / jogo | clipe de música / lyrics | react / pegadinha |
| vlog / ASMR / unboxing | podcast / live / stream | tutorial / aula / curso |
| "top 10" / compilado | episódio / filme / desenho | slideshow de foto parada |
| Shorts (url `/shorts/`) | transmissão ao vivo | canal infantil |
| upload sem audiência | curto demais | longo demais |

**Prioriza:** canal de arquivo (Reuters, AP, NASA, bancos de imagem grátis),
material marcado *stock footage* / *no copyright* / *b-roll*, drone, aéreo,
timelapse, câmera lenta, 4K. Vídeo de gente falando pra câmera e preview de
banco pago (Shutterstock, Getty — com marca d'água queimada) levam penalidade
pesada e caem pro fim da fila.

No rodapé de cada parte: **"4 itens · YouTube descartou 12 · yt: port ship
cargo container b-roll no copyright"** — o mouse em cima mostra o motivo de cada
descarte. Em cada card: **★ nota** (com o porquê no tooltip) e o **link do canal
que abre o vídeo no segundo exato** que vai ser recortado.

### O pulo do gato: a frase enviada ao YouTube é outra

Buscar no YouTube a mesma frase do Google Imagens devolve lixo:

| frase | o que volta |
|---|---|
| `supermercado corredor compras` | vlog, câmera escondida, desenho animado |
| `grocery store shopping stock footage` | clipe limpo de banco de imagem |

Quem publica b-roll no YouTube titula **em inglês** com *"stock footage"*,
*"no copyright"*, *"b-roll"*. Então, **só para o YouTube**, a frase é reescrita
numa cadeia de queda: cena de apoio já traduzida (a 2.0 tinha isso em tabela) →
nome próprio da seção → dicionário de b-roll (~200 substantivos) → tema global.
O sufixo alterna entre as partes, pra não vir sempre o mesmo vídeo. Desligável
no toggle *"Procurar b-roll em inglês"*.

### Velocidade do download

Dois ajustes medidos nesta máquina, baixando um trecho:

| | tempo | arquivo |
|---|---|---|
| com `--force-keyframes-at-cuts` | 11,4s | 6,0 MB |
| **sem** (o que a ferramenta usa) | **2,7s** | 2,9 MB |
| vídeo fonte de **11 horas** | 176,8s | **falhou** |

O corte por quadro exato obriga a recodificar o trecho: 4× mais tempo e o dobro
de arquivo, para ganhar uma precisão de fração de segundo que é invisível numa
imagem que fica 5s na tela. Saiu.

Vídeo **fonte** muito longo é o pior caso — o yt-dlp precisa varrer o fluxo até o
ponto do corte. Um de 11 horas gastou quase 3 minutos e nem terminou, e com a
cadeia de estratégias de cookie o mesmo item podia ser tentado 9 vezes: **meia
hora parada num arquivo só**. Era isso que travava o download em massa. Agora:

- teto padrão da fonte: **60 minutos** (era 4 horas)
- fonte acima de 90 min é recusada na entrada, sem tentar
- a cadeia de cookies para na **3ª** tentativa
- cada pedido tem prazo (180s vídeo, 45s imagem) — estourou, aquele item falha e
  a fila anda
- botão **■ Parar**, e a barra mostra o que está baixando e **quanto falta**

### ⚠️ Cookies (a busca não precisa, o download às vezes sim)

A **busca** funciona sempre. O **download da fatia** pode esbarrar no
*"confirme que você não é um robô"* do YouTube. Nesse caso, o arquivo
**`cookies.txt`** na pasta resolve (é o que já está funcionando aqui).

Clique em **"🔍 Testar a camada YouTube"** na lateral — ele diz o que está
funcionando e, se travar, o que fazer:

1. Extensão **"Get cookies.txt LOCALLY"** → abrir o youtube.com logado →
   exportar → salvar como `cookies.txt` nesta pasta.
2. Ou instalar o **Firefox**, logar no YouTube por ele e deixar instalado (o app
   lê o cookie do Firefox sozinho, até com ele aberto).

> Chrome e Edge da versão 127+ criptografam o cookie e não dá pra ler pelo app.

---

# Fidelidade ao roteiro

A busca — de imagem **e** de vídeo — só usa o que o roteiro põe lá. A tabela de
cenas de apoio da 2.0 tinha nascido num canal de carros: 6 das 11 cenas traziam
a palavra "carro" embutida, e o gatilho geográfico "China" devolvia
`carros chineses no Brasil` mesmo num roteiro sobre navio nuclear.

Isso foi corrigido na raiz, em três frentes:

**1. O roteiro diz do que ele fala.** Antes de qualquer busca, o app lê o texto
inteiro e descobre o assunto usando a **palavra que o próprio roteiro usa** —
"navio", "carro", "avião", "míssil", "supermercado". Como a palavra sai do
texto, já vem no idioma e na flexão certos. Precisa aparecer ao menos 3 vezes:
menção solta não é assunto.

**2. As cenas perderam o produto embutido.** Viraram neutras com um encaixe
preenchido pelo roteiro:

| roteiro fala de | cena que sai |
|---|---|
| navio | `fábrica linha de montagem navio` |
| avião | `fábrica linha de montagem avião` |
| míssil | `fábrica linha de montagem mísseis` |
| remédio | `fábrica linha de montagem remédio` |
| *nada dominante* | `fábrica linha de montagem` |

Sem assunto dominante o encaixe some e a cena continua válida — nunca errada.
O gatilho "China" agora devolve `China indústria {coisa}`; a cena de carro só
sai quando o roteiro cita **marca de carro** (BYD, GWM, Chery), que é prova de
verdade. Na versão em inglês (a que vai pro YouTube) o encaixe é traduzido:
`factory assembly line cargo ship`.

**3. Verbo não é assunto.** `localGlobalAnchor` contava palavras Capitalizadas
sem descartar as que só estão em maiúscula por abrirem frase — o comentário dela
assumia que "um nome recorrente sempre vence", o que falha quando nenhum nome se
repete. Num roteiro sobre navio, "Comecemos" (1×) empatava com "Xangai" (1×) e a
âncora saía `Comecemos Xangai`. Agora a abertura de frase é descartada antes da
contagem (como a função vizinha já fazia) e formas de verbo conjugado são
recusadas. A âncora virou `Xangai Jiangnan`.

Verificado nos dois sentidos: roteiro de navio não puxa carro em nenhuma parte,
e roteiro de carro continua com `Dolphin Camaçari na linha de montagem`.

---

# mustShow — o que precisa estar na tela

Vinha do prompt de referência, e é a diferença entre julgar contra **a frase que
se digita** e julgar contra **o que a imagem precisa mostrar**:

| | |
|---|---|
| frase de busca | `turbinas energia` |
| **mustShow** | obrigatório *turbina, turbine* · desejável *navio, vapor, motor* |

A frase de busca é uma string comprimida de palavra-chave — boa para pedir ao
Google, ruim para julgar resultado. Julgar por ela era o que deixava
`"Car Industry Stock Footage"` passar num roteiro de navio: batia em *industry*,
que estava na frase, sem mostrar nada do que a parte precisava.

O saco de palavras plano virou três níveis:

| nível | o que é | efeito |
|---|---|---|
| **obrigatório** | o sujeito da parte, a cena aprovada, o assunto do roteiro | pelo menos um tem que aparecer — senão a imagem não serve, por melhor que seja |
| **desejável** | o cenário em volta, os objetos da mesma cena, o plano | soma pontos |
| **fora do tema** | o vocabulário dos outros setores | desconta, e reprova se não houver nenhum obrigatório |

Cada parte mostra o dela no rodapé — **👁 precisa mostrar: porto, seaport, navio,
cargo, ship** — com a lista completa no tooltip. Assim dá para ver contra o que a
ferramenta está julgando, e discordar se for o caso.

Exemplos do mesmo roteiro:

| parte | precisa mostrar |
|---|---|
| o porto de Xangai | `porto, seaport, navio, cargo, ship` |
| a poluição do óleo pesado | `fumaça, smoke, poluição, pollution, chaminé` |
| o reator de sal fundido | `navio, cargo, ship, reator, nuclear` |

Duas armadilhas tratadas:

- **"drone" é técnica de câmera, não assunto.** Ele é um dos domínios da tabela,
  então caía em "fora do tema" — e penalizava justamente `"Drone Footage of
  Cargo Containers in a Port"`, que é o melhor b-roll possível. Fica de fora da
  lista de setores alheios.
- **A exibição levava o nome da seção na frente**, então toda parte mostrava
  *"xangai, jiangnan"* e parecia que todas pediam a mesma coisa. Agora o que é
  específico do trecho vem primeiro.

Medido num roteiro real: **17 descartes novos** que a curadoria anterior deixava
passar, com os motivos *"não mostra o que a parte pede"* e *"assunto de outro
setor"* — e todas as partes continuaram cheias.

---

# Camada 4 — Curadoria (item por item, como um editor)

Antes desta camada o app confiava na busca. Conferia se a imagem era **grande** e
**limpa**, nunca se ela tinha **alguma coisa a ver** com o que está sendo
narrado. Por isso um roteiro sobre navio nuclear recebia *"Seated Tricep Dips
Muscles Worked"*, um artigo sobre esôfago de cachorro braquicefálico e três
séries chinesas — e chegava tudo na tela com cara de acerto.

Agora cada imagem e cada vídeo passa por uma conferência:

| conferência | o que pega |
|---|---|
| **Relevância** | o título do resultado tem palavra em comum com a narração? Nenhuma, num título com 3+ palavras de conteúdo, é descarte |
| **Repetição** | quatro fotos da mesma matéria, com o mesmo título, são uma imagem ocupando quatro lugares |
| **Nota mínima no YouTube** | a nota já era calculada mas nada era descartado por ela — vídeo com nota **negativa** chegava na tela |
| **Lixo conhecido** | loja online, letra de música, horóscopo, receita |

Tudo que sai aparece no rodapé da parte, com o motivo. Cada card mostra a nota e,
passando o mouse, **quantas palavras do título bateram com aquele trecho**.

### Três detalhes que fazem a conferência funcionar

**Palavra genérica não é prova.** Metade de um título de banco de imagem é
enfeite: *stock*, *footage*, *free*, *royalty*, *4K*. `"Car Industry Stock
Footage"` passava num roteiro sobre navio porque "industry" batia. Essas palavras
continuam contando no total, mas não valem como prova de assunto.

**Nome de lugar muda de língua.** O trecho fala do porto de **Xangai**, o YouTube
devolve **Shanghai** — e a conferência reprovava o vídeo certo. Uma tabela dos
nomes que roteiro de geopolítica realmente cita (Xangai/Shanghai,
Pequim/Beijing, Roterdã/Rotterdam, Moscou/Moscow…) resolve sem inventar tradutor.

**Parte faminta busca de novo.** Se a curadoria reprovou quase tudo, a saída não
é aceitar o lixo de volta: é procurar outro material com a frase ampla do tema e
conferir de novo. Uma parte com 3 mídias certas vale mais que uma com 8, das
quais 5 estão erradas. E se ainda assim nada passar, os dois melhores voltam
**marcados em vermelho com "? confira"** — melhor olhar dois duvidosos do que um
buraco.

---

# Movimento nas imagens

Foto parada num vídeo de 20 minutos é o que faz parecer apresentação de slides.
Agora cada foto entra com um movimento lento de câmera, e a lista roda para que
**duas seguidas nunca façam o mesmo**: aproxima, corre pra direita, afasta,
corre pra esquerda, aproxima subindo, desce devagar.

Vídeo não ganha movimento — ele já se move sozinho, e zoom por cima fica
enjoativo.

Três cuidados que separam movimento bonito de movimento tremido:

1. **Amplia antes de mover.** O `zoompan` do ffmpeg anda de pixel em pixel;
   aplicado direto num 1920×1080 ele pula. Ampliando para 3840 primeiro, cada
   passo vira meio pixel na tela e o movimento fica liso.
2. **Fórmula por quadro, não acumulada.** A forma comum (`zoom+0.0005` a cada
   quadro) acumula erro de arredondamento e acelera sozinha no fim. Aqui a
   posição sai do número do quadro, então começo e fim caem exatamente onde
   deveriam.
3. **Entra e sai devagar.** Movimento linear começa e termina no susto. Uma
   curva *smoothstep* faz a câmera acelerar e frear sozinha.

Medido nos seis movimentos: diferença média entre quadros de 2,4 a 4,5 (há
movimento de verdade) com desvio abaixo de 0,6 da média (é suave, não aos
pulos). Para desligar: `py sincronizar.py --sem-movimento`.

---

# Idioma: buscar em várias línguas, sem texto estrangeiro na tela

São duas coisas diferentes, e elas foram separadas:

**Buscar em inglês é bom** — o acervo é muito maior e a mesma cena volta com
mais opções. O toggle **"Buscar imagens também em inglês"** vem ligado: cada
parte é procurada duas vezes, na língua do roteiro e em inglês, e a curadoria
junta tudo antes de escolher. Não muda o idioma do vídeo — muda só onde a imagem
é procurada.

| busca em português | busca em inglês (automática) |
|---|---|
| `porto navio contêiner importação` | `port ship cargo container` |
| `navio cargueiro fumaça poluição` | `smoke pollution chimney cargo ship` |
| `Jiangnan estaleiro naval` | `Grupo Jiangnan` (nome próprio ganha da cena genérica) |

**Texto estrangeiro na imagem é ruim** — o espectador lê a palavra estranha na
tela. Isso só a curadoria visual resolve, porque só ela vê o que está escrito
*dentro* da imagem. A regra que ela aplica:

- texto grande numa língua que não é a do roteiro **e não é inglês** (espanhol,
  alemão, russo, chinês…) → reprova, e diz qual língua viu
- texto em **inglês** só reprova se for muito e em destaque — palavra solta,
  placa ou nome de empresa passa
- texto na língua do roteiro passa
- imagem **sem texto nenhum** é sempre a melhor

---

# "Isso dá pra filmar?"

Um resultado real que a ferramenta produzia:

> **assunto** Dióxido de carbono supercrítico · **plano** rodando na estrada
> **busca:** `Dióxido de carbono supercrítico rodando na estrada`

Nenhuma busca bem escrita faz existir uma foto disso. São duas falhas somadas,
e as duas do tipo que só um editor percebe:

**O plano vinha do parágrafo, não do assunto.** `kindForQuery` lia
*consulta + texto da parte + tema*. Como o parágrafo mencionava **navio** em
algum ponto, o tipo virou "veículo" e o plano de veículo — *rodando na estrada* —
foi colado num assunto que era dióxido de carbono. O plano descreve a **coisa**,
então tem que sair da coisa. Agora sai.

**O assunto não era filmável.** "Dióxido de carbono supercrítico" é um conceito
de física. Um editor, lendo aquele parágrafo, filmaria a **turbina** — a coisa
visível que está ao redor do conceito. É essa troca que a ferramenta faz agora:

| assunto do roteiro | dá pra filmar? | vira |
|---|---|---|
| Dióxido de carbono supercrítico | não | `turbinas energia` |
| eficiência termodinâmica | não | a coisa visível do parágrafo |
| Reator de sal fundido | sim | (fica) |
| Grupo Jiangnan, Xangai, Sevmorput | sim | (fica) |
| Toyota Hilux | sim | (fica) |

Um termo é filmável quando é **nome próprio** (lugar, marca, navio — sempre há
foto) ou quando alguma palavra dele está no dicionário de b-roll, que é
justamente uma lista do que a câmera consegue apontar. O dicionário ganhou o
vocabulário de engenharia que faltava: turbina, caldeira, tubulação, válvula,
hélice, casco, sala de máquinas, painel de controle, gerador, vapor.

Duas armadilhas que apareceram ao testar isso, e que ficaram tratadas:

- **Maiúscula de início de frase não é nome próprio.** "Dióxido" passou por nome
  próprio na primeira versão só por abrir a frase. Agora a primeira palavra do
  termo não conta como prova — exceto quando o termo tem uma palavra só
  (`Xangai`, `Sevmorput`, aí é nome próprio de verdade).
- **Nome próprio ainda precisa do parágrafo.** "Toyota Hilux" não contém a
  palavra "carro" — é o parágrafo que diz isso. Cortar o parágrafo fora fazia a
  Hilux perder todos os planos de veículo. Agora o parágrafo volta como contexto
  **só quando a âncora é nome próprio de verdade**; com âncora abstrata ele não
  vale, porque foi ele que colou "rodando na estrada" no dióxido de carbono.

---

# Imagem limpa x imagem "vestida"

O prompt de referência é explícito: *"clean footage with **no burned-in text**,
no watermarks, no talking heads, **no logos**"*. Eu tinha implementado marca
d'água e resolução e deixado o resto de fora — e o resto é justamente o que suja
a imagem.

**De onde a imagem veio diz muito sobre ela estar limpa.** Banco de imagem
entrega a foto **crua**, do jeito que foi fotografada. Site de notícia entrega a
foto **já vestida**: manchete atravessada, tarja, logo do canal, crédito
queimado. Numa tela de 1920×1080 isso aparece inteiro.

O ranqueamento agora conhece a diferença:

| fonte | tier | o que costuma vir |
|---|---|---|
| Pexels, Pixabay, Openverse, Wikipédia, NASA | **0** | foto crua |
| site qualquer | 1 | risco médio |
| notícia (Globo, UOL, Correio, portais…) | 2 | manchete/tarja/logo por cima |
| fórum (Reddit, Pinterest, blogspot) e banco pago | 3 | print de post, montagem, marca d'água |

E — esta era a peça que faltava — **os bancos limpos agora são sempre
consultados**, inclusive em trecho de assunto específico. Antes eles só entravam
"se faltasse imagem", e como o Google sempre enchia a cota, nunca eram nem
perguntados.

### Mas o Google é onde mora o assunto

Corrigir a limpeza me fez exagerar, e por um tempo a ferramenta preferia a foto
limpa de um navio **qualquer** à foto do navio **de que o roteiro fala**. Nenhum
banco de imagem tem "Sevmorput", "Grupo Jiangnan" ou "NS Savannah" — isso só
existe no Google, e quase sempre em site de notícia. Medido num trecho sobre o
Sevmorput, antes da correção:

```
ordem só pela limpeza          nota final
  T0 Cargo ship on the sea       236  Cargo ship on the sea      ← navio qualquer
  T0 navio, mar, carga           207  Russian ... Sevmorput      ← o navio certo
  T2 Russian ... Sevmorput
  T3 Navio ... Sevmorput         ← o navio certo, no fim da fila
```

Duas coisas estavam erradas:

1. **A busca cortava candidatos só pela limpeza, antes da curadoria olhar
   relevância.** Um pool de 22 virava 8 escolhidos por fonte — e o assunto
   específico era descartado antes de alguém perguntar se ele era o assunto.
   Agora a busca **não corta**: entrega tudo, e quem decide é a curadoria, que é
   a única com os três sinais na mão.
2. **A nota tratava limpeza quase como relevância.** Agora o **nome próprio da
   seção** é o maior peso da conta (+70 por acerto), e a limpeza virou
   desempate (de −18 para −9 por nível). Imagem limpa do assunto errado é pior
   que imagem com tarja do assunto certo: tarja se corta, assunto errado não tem
   conserto.

Depois da correção, os dois casos se comportam como deviam:

| trecho | vencedor |
|---|---|
| **com nome próprio** (Sevmorput) | `330` naval.com.br · *Russian nuclear container ship Sevmorput* — o Google ganha |
| **de apoio** (portos em geral) | `305` pexels · *Cargo ship at container port* — o banco limpo ganha |

Uma imagem reprovada numa parte também deixou de ficar bloqueada para as outras:
o registro de "já usada" saiu da busca e foi para a curadoria, então só o que
foi **aprovado** fica marcado.

**Banco de imagem é limpo, não é relevante — e eu tinha misturado as duas
coisas.** Pexels, Pixabay e Openverse tinham *passe livre* na curadoria: nenhum
dos vetos de relevância era aplicado neles. A justificativa era que o título
deles é só o nome do autor — o que está errado: o Pexels devolve o texto
alternativo, o Pixabay devolve as tags, o Openverse devolve o título. Todos
descritivos, todos julgáveis.

Enquanto durou o passe livre, uma busca de banco que não achasse nada do assunto
devolvia o que tivesse — e aquilo ia direto pra tela sem conferência. Foi assim
que fotos de maquiagem apareceram num trecho sobre reator nuclear. O passe livre
acabou; o que fica é o bônus de limpeza, que é sobre a foto ser crua, não sobre
ela ter a ver com o trecho. Título curto demais para julgar (só o nome do
fotógrafo) continua passando, com nota baixa.

**A curadoria visual também mudou de alvo.** Ela reprovava "print de tela,
página de site, documento". Mas uma **fotografia de verdade, boa, com uma tarja
de manchete atravessada** passava — e é exatamente essa a imagem suja. Agora ela
recebe a instrução de olhar a imagem inteira, cantos e bordas inclusive, e
reprovar: tarja/faixa de manchete, título ou crédito escrito por cima, logo de
canal em qualquer canto, marca d'água mesmo transparente, tarja de "AO VIVO",
moldura decorativa, foto colada num fundo com espaço para texto ao lado.

Com uma exceção que importa: **palavra que faz parte da cena** — o nome no casco
do navio, uma placa de rua, o letreiro de uma loja — não é sujeira, é a
fotografia. O que reprova é o texto que foi **colocado em cima depois**.

---

# Curadoria visual — a IA olha a imagem

A curadoria por texto compara o **título** com a narração. Ela pega o artigo
veterinário e a série chinesa, mas não tem como saber que aquela "foto de porto"
é um print de tela cheio de letra, uma colagem de quatro fotos ou uma imagem com
marca d'água atravessada. Isso só olhando.

Ligue **👁 Conferir cada imagem OLHANDO** na caixa do Gemini, ou clique em
**👁 Olhar** numa parte específica. A IA recebe as imagens daquela parte **e o
trecho narrado**, e devolve um veredito por imagem. Reprova:

- assunto errado
- print de tela, página de site, documento, slide
- colagem de várias fotos, grade de miniaturas
- marca d'água atravessada, logo grande, legenda queimada
- gráfico ou tabela de outro assunto
- desenho, meme, capa com seta e rosto espantado
- desfocada, escura demais, pequena demais para tela cheia

Uma chamada por parte, com a imagem reduzida a 640px — o que já mostra
composição, texto queimado e montagem. Usa a chave do **provedor escolhido na
aba lá em cima**: Gemini ou **Claude** (`claude-opus-5`, com esforço baixo — é
classificação simples). Sem chave, esta camada não roda e a curadoria por texto
continua valendo.

> **Se você viu um erro `400 temperature` no Claude:** era um parâmetro que os
> modelos atuais não aceitam mais (`temperature`, `top_p` e `top_k` foram
> removidos em Opus 5 / Sonnet 5 / Fable 5 / Opus 4.7-4.8 e devolvem 400). Foi
> corrigido. O custo se controla por `effort`, não por parâmetro de amostragem
> nem rebaixando o modelo.

---

# Camada 2 — Áudio e sincronia real

Caixa **"Áudio da narração"** na lateral.

### O problema que resolve

Até a 2.0 o roteiro era fatiado por **número de caracteres** e toda parte
ganhava o mesmo tanto de imagem. Mas narração não é uniforme: dois parágrafos do
mesmo tamanho podem levar 28s e 45s, por causa de pausa, ênfase e respiração.
Resultado: imagem trocando fora do compasso da voz.

### Como funciona

1. Escolha um MP3 da pasta (ou **📁 Enviar MP3** pela própria página).
2. Cole o roteiro.
3. **🎙️ Transcrever e sincronizar.**

O áudio é transcrito **na sua máquina** pelo `faster-whisper` (nada sobe pra
internet) com o tempo de **cada palavra**. Depois o roteiro é casado com o que
foi falado por comparação de sequência de palavras, e cada parte recebe o
**tempo real** dela.

- **Cache por áudio *e* por modelo:** o mesmo áudio nunca é transcrito duas
  vezes; trocar de modelo refaz (antes devolvia calado o resultado do modelo
  anterior).
- **O padrão é o `tiny`, e é de propósito.** Aqui a transcrição não existe pra
  virar legenda: existe pra dizer *em que segundo* cada palavra foi falada. Se
  o modelo escrever "conteiner" sem acento, nada quebra — o casamento funciona
  igual e o tempo, que é o que interessa, é o mesmo. Medido com 2 minutos da
  narração real:

  | modelo | tempo | resultado |
  |---|---|---|
  | small beam=5 | 123,0s (1,0× tempo real) | referência |
  | small beam=1 | 78,9s (1,5×) | texto **idêntico** |
  | **tiny beam=1** | **18,5s (6,5×)** | 88% de casamento, **desvio mediano de 0,10s** |

  0,10s numa imagem que fica 5s na tela é invisível. Um áudio de 25 min sai em
  ~4 minutos com o tiny, contra ~25 com o small. Suba o modelo só se quiser a
  transcrição boa de *texto*.
- **Duas estratégias de alinhamento:** palavra a palavra (precisa) e, se o
  roteiro colado não bater com o que foi narrado (abaixo de 35% de casamento),
  cai sozinho para o modo proporcional — menos exato, mas nunca sai da ordem.
  A tela mostra qual foi usado e o percentual de casamento.

### O que muda depois de sincronizar

- Cada parte mostra no cabeçalho: **⏱ 0:40,9 → 1:15,9 · 35,0s · 7 mídias ·
  5,0s cada**.
- Uma **barra proporcional** na lateral: bate o olho e vê parte curta x longa.
### Você não precisa mais adivinhar quantas imagens por parte

Com **"Quantidade de mídia pela duração real"** ligado (é o padrão), o campo
*"Imagens por parte"* **para de mandar** — ele apaga na tela e o rótulo passa a
dizer quem decidiu: *"— o áudio decide (3 a 12, 34 no total)"*.

Você regula o **ritmo**, não a quantidade: quantos segundos cada imagem fica na
tela. O resto é conta:

| duração da parte | com 5s por mídia | com 3s por mídia |
|---|---|---|
| 1,2s | 1 | 1 |
| 4,0s | 2 (2,0s cada) | 2 (2,0s cada) |
| 12,9s | 3 (4,3s cada) | 4 (3,2s cada) |
| 36,0s | 7 (5,1s cada) | 12 (3,0s cada) |
| 49,0s | 10 (4,9s cada) | 12 (4,1s cada) |

Dois cuidados que estão no cálculo:

- **O piso não faz imagem piscar.** O mínimo de 2 por parte era aplicado sem
  olhar a duração: numa parte de 1,2 segundo (elas existem — *"Inevitável, ainda
  não."*) isso dava 2 imagens de 0,6s cada, que o olho não lê. Agora o piso cede
  quando a parte é curta.
- **O teto avisa quando muda o seu ritmo.** Se uma parte pedir mais que o *Máx.
  por parte*, o ritmo dela fica mais lento que o pedido — e a tela diz isso em
  vez de deixar você mexer no "segundos por mídia" sem entender por que aquelas
  partes não mudam.

---

# Camada 3 — Motion Graphics

Botão **✨ Motion** no cabeçalho de cada parte (ou **✨ Criar um Motion
Graphic** na lateral, pra cena avulsa).

### Sete tipos de cena

| cena | pra quê |
|---|---|
| 📰 **Título / Abertura** | o gancho dos primeiros 30 segundos |
| 🔢 **Número que conta** | estatística, valor, quantidade — sobe de zero |
| 📊 **Gráfico de barras** | comparação; as barras se desenham e os valores contam junto |
| 📋 **Tópicos** | 3 a 5 itens entrando um de cada vez |
| 💬 **Frase de impacto** | a frase aparece **palavra por palavra** |
| ⚖️ **Comparação (A x B)** | dois lados entrando de direções opostas |
| ⚡ **Passagem curta** | 1,5 a 3s pra separar dois blocos |

Seis paletas, e a identidade visual mora num lugar só — nenhuma cena escreve
código de cor na mão.

### Três regras que valem pra toda cena

1. **Nada aparece nem some sem animação.** Nunca um "pop".
2. **Nada se move em linha reta.** Toda entrada é mola ou expo-out; toda saída é
   ease deliberado, e termina antes do fim da cena.
3. **Nada fica 100% parado.** Existe uma deriva lenta de fundo mesmo em repouso
   — é o que separa motion graphic de slide de PowerPoint.

### O gráfico não é mais chapado

O prompt é direto na Phase 4: *"Multi-layer composition (background treatment +
midground content + foreground accents). **Flat single-layer scenes are not
acceptable**"* e *"charts/diagrams **draw themselves in**"*.

A minha cena de barras era um título, um tracinho e barras crescendo. Uma camada
só, sem eixo, sem grade, sem escala, sem profundidade — exatamente o que o
prompt chama de *default template gallery*. Foi reconstruída nas três camadas:

- **Fundo** — grade de referência que se desenha da esquerda para a direita, com
  as marcas de escala aparecendo uma a uma. A escala sobe até um número redondo
  acima do maior valor: gráfico que termina exatamente no maior parece cortado.
- **Meio** — as barras com gradiente, brilho na borda de cima (luz batendo),
  sombra projetada que tira a barra do plano do fundo, ponta arredondada.
- **Frente** — o eixo vertical descendo, o valor **contando junto com a barra**
  (não aparecendo pronto no fim) e um marcador na barra vencedora.

E o movimento: cada barra entra com **mola**, não com rampa — chega, passa um
triz e assenta. Medido: 20 níveis de tom distintos na faixa do gráfico, contra a
chapa anterior.

### O texto vem da oração, não da frase fatiada

Encurtar o texto resolveu o tamanho e criou outro problema: os textos viravam
pedaços sem sentido — *"Numa embarcação, onde cada metro cúbico ocupado por"*.
Roteiro de narração não tem frase curta; as frases têm 150 a 250 caracteres.
**Cortar o começo de uma frase longa nunca vira manchete, vira fragmento** — e
fragmento na tela é pior que texto cortado.

O que um editor faz é outra coisa: procura, dentro do parágrafo, a **oração que
já se sustenta sozinha**. Ela quase sempre está lá, entre vírgulas.

Agora a busca é por oração, com três filtros: não pode começar com conectivo
(*que, onde, mas, sendo, dando…* — quem começa assim depende do que veio antes),
precisa ter verbo (senão é sintagma solto: *"cada metro cúbico de máquina"*), e
precisa caber. O corte é o último recurso.

O mesmo parágrafo, antes e depois:

| | |
|---|---|
| antes | `Numa embarcação, onde cada metro cúbico ocupado por` |
| **depois** | **`um navio que sai do estaleiro e navega uma década inteira`** |
| antes | `O núcleo do reator foi projetado` |
| **depois** | **`O núcleo do reator foi projetado para operar dez anos sem reabastecimento`** |

E os tamanhos caíram para tamanho de **manchete** — 58 para título, 30 para
passagem, 46 para tópico. Medido nas 6 cenas com texto real: nenhuma encosta na
borda (margem de 176 a 484px em cima, 409 a 602px embaixo).

### Texto nunca é cortado, e a cena sempre termina

Dois defeitos que apareceram usando de verdade:

**A cena não terminava.** Toda cena reserva os últimos 0,45s para sair de tela,
e todo desenho é multiplicado pelo fator de saída — menos um: a função que
revela as linhas de título fazia `ctx.globalAlpha = ...` em vez de `*=`, jogando
fora o fator que o chamador tinha acabado de aplicar. O título nunca sumia.
Medido: a quantidade de pixel claro no último quadro era **1989**, praticamente
igual ao meio da cena (2055) — o vídeo parava em vez de terminar. Valia para o
título das cenas Título, Barras, Tópicos e Comparação. Depois da correção, as
sete cenas terminam em **0**, e no MP4 gerado o último quadro tem brilho máximo
50 (só o fundo) contra 233 no meio.

**Texto sumia calado.** As cenas desenhavam no máximo 2 linhas e jogavam o resto
fora, então frase comprida perdia o final sem avisar; e a cena Título empilhava
chapéu + 3 linhas + subtítulo sem conferir se cabia — com título de 3 linhas o
subtítulo terminava em y=1065 de 1080, encostando na borda. Agora o texto
**encolhe até caber** em vez de ser cortado, e o bloco inteiro é medido antes de
desenhar. Testado com título e subtítulo bem longos: o texto para em y=811.

### Prévia = render

O mesmo código que desenha a prévia desenha os quadros do MP4. Não existe
"quase igual". A prévia tem play e barra de rolagem pra conferir quadro a
quadro antes de gerar.

### ✨ Gerar as cenas sozinho

O botão na lateral escolhe as partes, escolhe o tipo de cada cena e gera todas —
com a duração real vinda do áudio. Precisa do **áudio sincronizado** e do roteiro
já analisado.

**Onde colocar.** Uma cena a cada ~30s / 1min / 1min30 / 2min (você escolhe), mas
**não no relógio**: dentro de cada janela ele fica com a parte que mais *pede*
uma cena. Cena no lugar errado cansa mais do que nenhuma cena. E **nunca duas
seguidas** — precisa de pelo menos uma parte de imagem no meio, senão vira
apresentação de slides animada.

**Qual cena.** Sai do que o texto tem:

| o trecho tem | cena escolhida |
|---|---|
| número grande ("vinte e quatro mil contêineres") | contador subindo de zero |
| enumeração ("o primeiro risco… o segundo…") | tópicos entrando um a um |
| comparação ("em vez de", "no lugar de") | A × B |
| frase curta e fechada | citação palavra por palavra |
| primeira parte | título (o gancho leva o tratamento mais forte) |

Dois cuidados que estão no cálculo:

- **Ano não é estatística.** "dois mil e cinquenta" é 2050 — um contador
  animando até *2.050* não faz sentido. Números entre 1500 e 2200 ficam de fora
  da cena de número.
- **Variedade.** Repetir o tipo da cena anterior perde força no desempate. Sem
  isso o vídeo enchia de cartão de citação seguido, que é o tipo mais fácil de
  detectar — oito deles cansam mais do que ajudam.

**O intervalo real é quase sempre maior que o pedido**, e o diálogo diz isso
antes de começar: como duas cenas nunca ficam coladas, o piso é o tamanho de
duas partes. Num roteiro com partes de ~30s, pedir "a cada 30s" entrega uma a
cada ~62s. Medido no roteiro do navio (19min41):

| pedido | cenas | intervalo real |
|---|---|---|
| 30s | 19 | 62s |
| 1 min | 14 | 84s |
| 1min30 | 9 | 131s |

Leva uns 22 segundos por cena. O botão **■ Parar** interrompe depois da cena
atual.

### Quanto da parte a cena ocupa

Antes a cena virava "mais um arquivo" da pasta e dividia o tempo igual com as
fotos — quem quisesse um título de 4 segundos tinha que contar na mão quantas
fotos tirar. Agora você escolhe, e a tela mostra em números o que a escolha faz:

| escolha | o que acontece (parte de 36s, 7 mídias) |
|---|---|
| **A parte inteira** | a cena ocupa os 36,0s; as 7 mídias saem deste trecho |
| **Só o começo** | a cena abre com 8,0s; sobram 28,0s para as 7 mídias (~4,0s cada) |
| **Mais uma na fila** | entra como uma das 8 mídias, com ~4,5s |

A instrução vai no **próprio nome do arquivo** (`00_motion_parte_titulo.mp4`,
`00_motion_8_0s_titulo.mp4`), e o `sincronizar.py` lê dali e reserva o tempo
antes de dividir o resto. A instrução viaja junto com o arquivo — não existe um
segundo arquivo de configuração para ficar dessincronizado.

### Integração com as outras camadas

- **A duração já vem certa:** abrindo o Motion pelo botão de uma parte com áudio
  sincronizado, a cena nasce com o **tempo real daquele trecho**.
- **💡 Sugerir** lê o texto da parte e preenche sozinho: acha o maior número do
  trecho pra cena de número, as frases pra tópicos, a frase de tamanho certo
  pra citação.
- O MP4 sai em `downloads/paragrafo NN/` com prefixo `00_`, então entra **antes**
  das imagens daquela parte na montagem — e o `sincronizar.py` acha tudo no mesmo
  lugar sem precisar saber que motion graphics existe.

Saída: **1920×1080, H.264, 30fps, yuv420p, CRF 17** — o mesmo formato dos vídeos
do YouTube e do Pexels, pra montagem final não reconverter nada.

---

# Camada 5 — Bancos públicos sem chave

Três acervos novos entram na busca, **sem chave, sem conta, sem cota**:

| banco | pra quê | tier |
|---|---|---|
| **Wikimedia Commons** | o único acervo que guarda **nome próprio** — o navio *Sevmorput*, o estaleiro *Jiangnan*, a usina *X*. Nenhum banco de stock tem isso. | 0 (foto crua) |
| **NASA Image Library** | espaço, Terra vista de cima, foguete, satélite, tecnologia | 0 |
| **Internet Archive** | registro de época, cinejornal, foto histórica de domínio público | 0 |

O Wikimedia é consultado **sempre** (quase não devolve lixo: namespace `File:`,
título descritivo). NASA e Archive entram quando a parte ainda está com pouca
imagem. Todos contam como fonte **limpa** na curadoria — foto crua ganha da
notícia com tarja, mas continua sendo julgada por relevância como qualquer
outra. Rotas: `/api/wikimedia`, `/api/nasa`, `/api/archive` (arquivo `bancos.py`).

### Por que a mesma foto abria três partes seguidas

Um laço fechado, com duas voltas:

**1. O resgate entregava sem registrar.** Quando a curadoria reprova tudo, os
dois melhores voltam marcados `? confira` — é a válvula que evita parte vazia.
Só que esse caminho era o único que não marcava a imagem como *usada*. Então na
parte seguinte o mesmo item voltava na busca, era reprovado de novo, e era
resgatado de novo. Para sempre.

**2. O reforço pedia sempre a mesma coisa.** Parte com pouca mídia buscava de
novo pela palavra do domínio do roteiro — `buque`. Essa palavra é a **mesma para
as 40 partes**, então toda parte faminta fazia a mesma busca e recebia os dois
primeiros resultados do Commons. Os mesmos dois.

O que mudou:

| antes | agora |
|---|---|
| resgate não registrava | registra, e nunca resgata algo que já está noutra parte |
| 1 frase de reforço, global | até 3 frases, todas tiradas **daquela** parte |
| mesma frase → mesma página | deslocamento por parte: a mesma frase devolve material diferente |
| dedup só por URL | dedup por URL **e** por assinatura de título |
| aprovado-mas-cortado ficava queimado | só o que vai para a tela é registrado |

O último item era caro em silêncio: um candidato aprovado que a cota cortava
ficava bloqueado para todas as partes seguintes. A ferramenta gastava material
bom sem nunca mostrá-lo.

### O que passou a ser recusado

| entrava | por quê passava | agora |
|---|---|---|
| página da **Steam**, wiki de jogo | o jogo se chama igual ao assunto (*"Headquarters World War II"*), então batia em **todas** as palavras e ganhava nota alta | veto por domínio + por título (`gameplay`, `War Thunder`, `Hearts of Iron`…) |
| loja de **miniatura/brinquedo** | a peça é catalogada com o nome exato da unidade militar | veto por domínio |
| **miniatura do Google** (`encrypted-tbn`) | é o que sobra quando a página bloqueia o link direto | veto — e a URL do Commons em `1920px-` continua passando |
| prévia da **Alamy/Getty** | antes só era rebaixada | veto: marca d'água atravessada não se usa em vídeo pronto |
| **vídeo** do Commons fora do tema | nome de arquivo curto escapava do piso de 3 palavras | vídeo com lista do que mostrar na mão e zero acerto é recusado |
| brasão, bandeira, mapa, medalha, cartaz, cédula | são JPG grandes e limpos: passam em todo teste automático | filtro de documento plano no `bancos.py` |

### A época do roteiro

Um roteiro de 1941 recebia cerimônia militar de **2024**, ônibus espacial e
cargueiro moderno — com nota alta, porque *military*, *command*, *ship* batem
igual nos dois séculos. Nenhuma trava lexical pega isso: as palavras estão
certas, errada está a década.

E a data está escrita na narração. O app agora lê o roteiro inteiro, tira a
mediana dos anos citados (precisa de 3+, e metade tem que se agrupar) e usa uma
janela de ±30 anos:

- título com data **fora** da janela → recusado (*"de outra época (2024)"*)
- título com data **dentro** → +40 na nota (arquivo é catalogado por ano)
- título **sem** data → julgado como sempre, mas o que só existe depois
  (`STS-129`, `IMO 9919515`, `container terminal`) é recusado

Isso resolveu uma colisão de nome real: o roteiro fala do corsário **Atlantis**
(1941) e o Commons devolvia o **ônibus espacial Atlantis**.

Roteiro sem datas, ou que atravessa séculos, não liga a trava — nada muda.

### "Rogge" não é uma busca

Uma palavra só não é uma busca — é um chute. `Rogge` devolve qualquer pessoa com
esse sobrenome; `Atlantis` devolve o ônibus espacial e um resort.

Normalmente quem monta a frase completa é o briefing da IA (*"Bernhard Rogge,
oficial da Kriegsmarine"*). **Sem chave de IA**, o planejador local entregava o
nome pelado — e a época sumia junto, porque ela vinha só do briefing.

Duas coisas mudaram, as duas sem depender de IA:

1. **A época volta pela porta dos fundos.** O `detectEpoca` já lê os anos do
   próprio roteiro; agora a busca usa isso quando não há briefing.
2. **Nome pelado ganha um qualificador** — um só, escolhido pelo tipo:
   pessoa leva `retrato`; o resto leva o assunto do roteiro.

| antes | agora |
|---|---|
| `Rogge` | `Rogge retrato 1941` |
| `Atlantis` | `Atlantis buque 1941` |
| `Kriegsmarine` | `Kriegsmarine buque 1941` |
| `Bernhard Rogge` | `Bernhard Rogge 1941` (já tinha contexto) |

`Atlantis buque 1941` é o caso que mostra por que vale: é essa frase que separa
o corsário do ônibus espacial de mesmo nome.

> Somar **dois** qualificadores produzia frase que ninguém digitaria — `Rogge
> retrato buque`, `Kriegsmarine sede`. Marinha não tem foto de sede, e capitão
> não é navio. Um qualificador, o certo.

Roteiro sem datas e sem assunto dominante não muda nada.

### O Commons estava recusando a ferramenta, calado

Duas falhas somadas, as duas invisíveis porque a exceção era engolida:

1. **429 — limite de requisições.** A Wikimedia trata User-Agent de navegador
   como tráfego anônimo, e com 40 partes o limite chegava rápido. Agora vai um
   UA que identifica a ferramenta, com nova tentativa e **cache em memória** (a
   mesma consulta feita por duas partes não vai duas vezes à rede).
2. **A busca do Commons é conjuntiva.** `merchant ship cargo ocean smokestack
   1940s` exige as seis palavras no mesmo arquivo — não existe, e o retorno é
   zero. Era a metade silenciosa da "busca fraca": não vinha material errado,
   não vinha material **nenhum**. Agora a consulta encurta em cascata
   (6 palavras → 3 → 2 → 1), como faria quem está pesquisando à mão.

### Vídeo sem o bloqueio do YouTube

O YouTube trava o download com "confirme que você não é um robô". **Wikimedia
Commons** e **NASA** também entregam **vídeo**, com **download direto** — sem
esse bloqueio. Entram na busca de vídeo junto com Pexels/Pixabay/YouTube (rotas
`/api/wikimedia_video`, `/api/nasa_video`). O corte para o trecho continua sendo
feito no `sincronizar.py`. A chave da Serper **não é mais obrigatória** nem para
imagem: sem ela a busca vai por Bing, DuckDuckGo e pelos bancos sem chave.

> Isso ataca na raiz o problema que o resto do LEIA-ME repete: *"o assunto
> específico só existe no Google, e quase sempre em site de notícia"*. Agora,
> para o que tem nome, existe uma fonte limpa.

---

# Montagem: três conferências que a 2.0 não fazia

O `sincronizar.py` ganhou os portões que a reescrita provou necessários:

1. **Loudness.** A narração é medida e levada a **−14 LUFS** (o alvo do
   YouTube) com ganho medido + limitador em −1,5 dBTP. `loudnorm` sozinho
   trava em ~−15,6 em voz de TTS. Vale no `--montar` e no `comando.txt`.
2. **Frame exato.** `-frames:v N` e `-t S` são tetos, não garantias: fonte que
   acaba antes deixa o clipe curto **em silêncio**. Agora cada clipe é conferido
   (`ffprobe nb_frames` da própria saída) e, se faltou, refeito segurando o
   último quadro até a duração exata (acima de 3 s vira defeito, não conserto).
3. **Borda queimada.** Reupload de YouTube vem dentro de uma moldura preta;
   sem recortar, a tela sai não preenchida. `cropdetect` acha o retângulo real
   e corta antes de reampliar.
4. **QA do arquivo pronto** (`qa.py`, roda sozinho depois do `--montar`, ou
   `py sincronizar.py --qa`): duração × áudio, trechos pretos, trechos
   congelados, loudness fora do alvo, e 12 fotos em `qa_fotos/`. Reprovou →
   sai com a lista do que está errado. Desliga com `--sem-qa`.

---

# Modo automático — do roteiro às imagens, sem abrir o navegador

```bash
py auto.py --modelo
```

```bash
py auto.py
```

```bash
py sincronizar.py --capcut
```

Três arquivos na pasta e um plano. O `auto.py` enche `downloads/paragrafo NN/`
sozinho; daí em diante o caminho é o de sempre.

| arquivo | para quê |
|---|---|
| `roteiro.txt` | o texto narrado — o **mesmo** que gerou o áudio |
| `legenda.srt` | a sincronia (é dela que sai a duração real de cada parte) |
| `narracao.mp3` | opcional, só para conferir onde a narração termina |
| `plano.json` | **o contexto e os termos de busca** |

## Por que separar em duas metades

O trabalho tem duas naturezas diferentes, e elas estavam juntas.

A metade **semântica** — ler o roteiro, entender do que ele fala, decidir o que
cada trecho precisa mostrar, escrever a frase de busca — é leitura. Na página
isso é feito por ~3 mil linhas de heurística que adivinha o assunto contando
palavra capitalizada. Funciona, mas é adivinhação: foi ela que produziu `Rogge`
como frase de busca inteira e `Dióxido de carbono supercrítico rodando na
estrada`.

A metade **mecânica** — consultar oito fontes, cruzar o resultado com o que a
parte pede, jogar fora loja/jogo/brasão/miniatura/marca d'água/outra época, não
repetir, e baixar — é execução. Essa a heurística faz bem, porque é verificável.

Aqui elas se separam. A leitura vira `plano.json`, escrito por quem leu o
roteiro de verdade. A execução continua sendo código. **O motor não muda de um
vídeo para o outro; o plano muda.** É o mesmo desenho do `edit_plan.json`:
decisão editorial é *dado*, não código.

## O `plano.json`

O `--modelo` escreve um em branco, **já dividido nas partes certas e com a
duração real de cada uma** — só faltam duas listas por parte:

```json
{
  "idioma": "es",
  "tema": "O cruzador auxiliar alemão Atlantis, corsário disfarçado (1940-41)",
  "assunto": "buque",
  "epoca": { "ano": 1941, "min": 1935, "max": 1946 },
  "fontes": ["wikimedia", "archive", "openverse"],
  "evitar": ["gameplay", "museum model", "replica"],
  "partes": [
    {
      "n": 1, "dur": 24.0, "midias": 4,
      "texto": "En mil novecientos cuarenta el crucero auxiliar Atlantis…",
      "busca":   ["German auxiliary cruiser Atlantis 1940",
                  "Hilfskreuzer Atlantis raider ship",
                  "Bernhard Rogge Kriegsmarine officer"],
      "mostrar": ["atlantis","raider","hilfskreuzer","cruiser","ship","rogge"]
    }
  ]
}
```

`busca` são as frases que vão às fontes. `mostrar` é **contra o que a imagem é
julgada** — e são coisas diferentes de propósito: a frase de busca é uma string
comprimida de palavra-chave, boa para pedir, ruim para julgar. Era isso que
deixava *"Car Industry Stock Footage"* passar num roteiro de navio: batia em
*industry*, que estava na frase, sem mostrar nada do que a parte precisava.

> **A janela de época é sua régua mais afiada — e a mais fácil de errar para o
> lado largo.** Num teste com `min: 1915` entraram fotos da Marinha Real de
> 1914-1918 num roteiro de 1941, e a ferramenta estava certa: eu é que abri
> demais. Aperte para ±5 anos quando o assunto é datado.

## Quantas imagens por parte

Ninguém escolhe: sai da **duração real** de cada parte, lida da legenda.

```bash
py auto.py --seg 6        # cada imagem fica ~6s na tela
```

Uma parte de 45s pede 8 imagens; uma de 12s pede 2. O piso cede quando a parte
é curta — exigir 2 mídias numa parte de 1,2s dá 0,6s cada, que o olho não lê:
vira flash, não imagem.

## Conferir antes de baixar

```bash
py auto.py --so-plano
```

Mostra quantas cada parte achou e **por que** descartou o resto, sem baixar
nada. `--parte 7` roda uma parte só. O relatório completo, com a nota e a fonte
de cada imagem escolhida, fica em `auto_relatorio.json`.

Saída real de um teste (4 partes, 1min26 de narração):

```
 parte 01   24.0s  pede 4  |  German auxiliary cruiser Atlantis 1940 / …
           4 de 24 candidatas | descartou 16  (nada a ver com a parte 10,
                                               de outra época (2018) 2)
 …
 14 imagens de 14 pedidas   (100%)   em 2 min
```

A primeira colocada da parte 1 foi `Hilfskreuzer Atlantis`, nota 150 — o navio
exato de que o trecho fala.

## O que a curadoria recusa

`curadoria.py` é a porta para Python das travas que já existiam na página. Sem
ela o modo automático baixaria tudo que a busca devolvesse — que é exatamente o
problema que a versão com tela já tinha resolvido.

| recusa | exemplo real que passou antes |
|---|---|
| loja, jogo, brinquedo | página da Steam *"Headquarters World War II"* |
| documento plano | *"Kriegsabzeichen für Hilfskreuzer"* (uma insígnia) |
| casco moderno | *"USS Bonhomme Richard (LHD 6)"* num roteiro de 1941 |
| outra época | *"USEUCOM Change of Command 2013"* |
| miniatura | `encrypted-tbn0.gstatic.com/...` |
| prévia com marca d'água | Alamy, Getty |
| repetida | mesma foto, ou mesma matéria, já usada noutra parte |

> Ela **não** adivinha o assunto — isso é trabalho do plano. Portar a
> adivinhação seria duplicar 3 mil linhas de heurística para fazer pior do que
> o plano já faz.

### Três defeitos que só a primeira rodada de verdade mostrou

Rodar em 41 partes e 252 imagens revelou o que 4 partes de teste não revelaram.

**1. A ferramenta mentia sobre o próprio resultado.** Ela dizia
`252 de 252 (100%)` com **200 arquivos na pasta**: contava o que a curadoria
*aprovou*, não o que chegou ao disco. É o pior tipo de erro — silencioso, e só
apareceria na montagem. Agora são dois números, sempre:

```
 Curadoria aprovou : 252 de 252 pedidas   em 16 min
 NO DISCO          : 200 de 252   (79%)
   11 (2/7), 12 (2/8), 13 (2/5), 37 (1/5)
```

**2. O download saía com cara de Chrome.** O `bancos.py` já resolvia isso para
a **busca** — User-Agent que identifica a ferramenta mais o token OAuth — mas o
**download** ia com UA de navegador e sem token, e a Wikimedia trata isso como
tráfego anônimo em massa: 52 das 252 levaram `429 Too many requests` *depois*
de a curadoria já tê-las aprovado. Agora os dois caminhos usam a mesma
credencial, mais um freio por host com recuo progressivo. Medido depois: **0
falhas**.

**3. A pasta virou acumulador.** Rodar de novo escolhe imagens um pouco
diferentes (a memória de "já usada" começa limpa) e, com nomes diferentes, as
antigas ficavam. Sobraram 41 arquivos em 11 partes — a parte 04 terminou com 12
imagens para 34,7 s, ou seja **2,9 s cada em vez dos 6 s pedidos**. O ritmo do
vídeo mudava sem ninguém pedir e sem ninguém ver. A pasta agora é o *resultado*
daquela rodada: o que não foi escolhido desta vez sai.

### O movimento tremido — duas causas, nenhuma óbvia

O movimento lento de câmera nas fotos saía **tremido**. Medindo a diferença
entre quadros consecutivos, o perfil era este:

```
0.06 · 1.15 · 0.07 · 1.15 · 0.08 · 1.16      ← parado, pulo, parado, pulo
```

A imagem ficava **parada 2-3 quadros e pulava um pixel inteiro**.

**Causa 1: a curva.** O `smoothstep` tem velocidade **zero** nas duas pontas —
é a definição dele. E o `zoompan` posiciona o recorte em pixel inteiro. Quando
a velocidade chega perto de zero, a posição não muda: estaciona e salta. A
curva que existia para suavizar era a que causava o tremor.

| curva | tremor | travados | vel. mínima |
|---|---|---|---|
| smoothstep puro | 0,44 | 2 | **0%** |
| **25% ease + 75% linear** | **0,15** | **0** | 60% |
| linear puro | 0,14 | 0 | 84% |

Linear puro é marginalmente mais liso mas começa e para no susto — que foi o
motivo de existir o smoothstep. A mistura mantém o ease visível sem nunca
estacionar.

**Causa 2: a largura de trabalho, e não do jeito que se espera.** Sobravam
"soluços" — um quadro andando 50% mais que os vizinhos. Testando quatro
larguras, o resultado foi contraintuitivo:

| largura | tremor | pico/mediana | custo |
|---|---|---|---|
| 3840 | 0,22 | **1,52** | 0,87 s |
| **5760** | **0,17** | **1,05** | 1,11 s |
| 7680 | 0,14 | 1,23 ← **pior** | 1,43 s |

**O 7680 é pior que o 5760 e mais caro.** O que manda não é o tamanho bruto: é
a **proporção inteira** com 1920. `5760 = 3 × 1920` exato, então cada pixel de
trabalho vale um terço de pixel na tela e os passos caem sempre no mesmo lugar.

Resultado final, medido no clipe que o `sincronizar.py` gera:

| | antes | depois |
|---|---|---|
| tremor | 0,44 | **0,19** |
| pico/mediana | 1,52 | **1,04** |
| quadros travados | 2 | **0** |

> O que restou é inerente ao `zoompan` trabalhar em pixel inteiro. Eliminar de
> vez exigiria outro motor de movimento.

### Geração de clipes em paralelo

Cada clipe é independente — só a numeração do arquivo depende da ordem, e ela
já vem calculada. Com 6 processos simultâneos (o ganho some acima disso, o
gargalo passa a ser disco): **0,61 → 1,18 clipe/s**.

A verificação que importa depois de paralelizar não é "gerou tudo", é a
**soma das durações**: 252 clipes somaram 25:10,900 contra 25:10,949 de áudio —
0,05 s de diferença.

### Quando o acervo de um assunto acaba

Num roteiro sobre **um** assunto (o Ötzi), as partes finais ficavam vazias com
o motivo `já usada em outra parte`: na parte 71, **todas as 36 candidatas** já
tinham ido para partes anteriores.

Não é falha de busca — é o acervo específico ter acabado. A saída não é
afrouxar a trava de repetição (aí a mesma foto abre três partes), é a parte
final buscar o **entorno**: a montanha, o glaciar, a bancada do laboratório —
em vez de mais uma foto da múmia.

### Marca de carro tem três letras

O piso de tamanho para uma palavra de título contar era **4 letras**. Num
roteiro sobre a **BYD** isso apagava o assunto central:

| título real | tokens vistos (antes) |
|---|---|
| `BYD Atto 3 Genf 2022` | `atto, genf, 2022` |
| `BYD Dolphin` | `dolphin` |

A marca sumia, e uma parte inteira sobre a BYD podia aprovar qualquer carro. O
piso caiu para 3 — que é o tamanho de BYD, KIA, BMW, GM — com uma lista curta
de ruído (`the`, `and`, `que`, `der`…) no lugar de um piso que joga fora
justamente o que importa.

---

## Arquivos

| arquivo | o que é |
|---|---|
| **`auto.py`** | do roteiro às imagens, sem navegador |
| **`curadoria.py`** | as travas de qualidade, em Python |
| `buscador-imagens.html` | a ferramenta (2.0 + as três camadas) |
| `servidor.py` | servidor local na porta 8003, com as rotas novas |
| **`youtube.py`** | busca, filtro de qualidade e download de trecho |
| **`bancos.py`** | Wikimedia Commons, NASA e Internet Archive (sem chave) |
| **`audio.py`** | transcrição (faster-whisper) e alinhamento roteiro↔fala |
| **`motion.js`** | o motor de animação (Canvas 2D) — desenho e export |
| **`motion.py`** | recebe os quadros e chama o ffmpeg |
| **`qa.py`** | portões de qualidade sobre o `video.mp4` pronto |
| `sincronizar.py` | montagem + as três conferências novas |
| `estudio.py`, `b.py` | vieram da 2.0, sem alteração |
| `cookies.txt` | seu cookie do YouTube (não compartilhe este arquivo) |

Tudo cai em `downloads/paragrafo NN/`, do jeito que sempre caiu.

---

## Ordem de trabalho sugerida

1. Cole o roteiro
2. Escolha o áudio → **🎙️ Transcrever e sincronizar**
3. **Analisar e buscar imagens** (agora cada parte pede a quantidade certa)
4. Escolha as mídias, use **✨ Motion** nas partes que pedem uma cena
5. **⬇ Baixar TODAS** no rodapé
6. `py sincronizar.py --chars 700` pra montar o vídeo final
