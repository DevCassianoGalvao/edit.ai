# Edit.AI by Galvão — cópia de trabalho

Esta pasta contém a cópia do pacote completo fornecido pelo proprietário. A pasta original não foi alterada. O painel e o Mapa usam portas próprias para evitar conflito com a instalação anterior.

- **Abrir o aplicativo:** use o atalho Edit.AI by Galvão na área de trabalho ou execute `Abrir Edit.AI by Galvão.bat`. Ele abre uma janela própria usando WebView2 e o painel local. Para aplicar atualizações do servidor já aberto, feche a janela e reinicie o servidor do painel. Painel: http://127.0.0.1:8876/ ; Central: http://127.0.0.1:8876/central .
- **Abrir o Mapa de imagens:** execute `ABRIR_MAPA.bat` (http://127.0.0.1:8877/).
- **Primeiro uso:** abra Chaves no painel e configure as integrações necessárias; cadastre seus canais pelo modelo `ALTA/EditAI/painel/canais.exemplo.json`. Na Central, ligue os funcionários quando estiver pronto. O motor pode ser Claude ou Codex.
- **Dependências:** já foram instaladas para esta cópia neste PC. Para reinstalar em outro ambiente, use `INSTALAR_DEPENDENCIAS.bat`, depois de instalar Python, Node.js, Git Bash e FFmpeg. A primeira utilização de modelos pode exigir internet e bastante espaço em disco.
- **Agentes e memória:** a pasta de trabalho é `MAPA`; as regras copiadas estão em `MEMORIA`. O gerente está configurado para essas pastas. A automação por agentes usa permissões amplas do programa original; ligue os funcionários apenas quando desejar iniciar o trabalho automático.
- **Recuperação automática:** os nomes de tarefas agendadas da cópia são distintos dos da instalação anterior. Não foram criadas tarefas de inicialização automática; a Central e o gerente podem ser iniciados pelo atalho acima.

## Limitações identificadas

O Short 3D foi retirado das novas produções; pedidos antigos continuam preservados. A geração de voz, certas buscas e outras integrações dependem de contas e chaves próprias; a cópia não contém credenciais do pacote original. A existência de uma chave ou CLI não garante que o serviço, o login ou as cotas estejam válidos.

Esta instalação usa o modo do proprietário. O antigo instalador de venda foi separado dos arquivos ativos; use este guia e o instalador de dependências desta cópia.

## Verificações realizadas

A Central, as telas e as APIs principais responderam; uma fila de testes separada criou dois pedidos, enviou roteiro e áudio e confirmou o primeiro. A busca Wikimedia respondeu com resultados reais. Uma transcrição foi executada com Faster-Whisper, um vídeo de teste foi renderizado pelo Remotion principal em 1080p com áudio e um rascunho de teste do CapCut foi gerado em pasta temporária. Esses testes não substituem uma produção real completa com os serviços e contas escolhidos.

## Atualização de 07/11 incorporada

O indicador de conexão distingue monitor, funcionários desligados e gerente sem resposta. As regras de integração aceitam Pexels ou Pixabay e informam ao Diretor quais serviços estão configurados. Sem DarkPlanner, a pauta permanece com o roteiro para receber narração; integrações opcionais sem chave são ignoradas. A escolha de proporção de fotos no painel é preservada. Os arquivos anteriores estão em `backups/antes_atualizacao_20261107`. O atualizador da versão vendida não foi instalado, pois depende do servidor de licença e dos caminhos da instalação anterior.

## Estúdio de canais e miniaturas

Abra Estúdio no painel. Cadastre um canal com idioma, memória editorial, estilo e referência de miniatura. Para guardar opções de um filme, selecione o canal em Novo filme, ajuste as guias e escolha Salvar preset do canal na etapa Revisar. No perfil do canal é possível definir o preset padrão. O cadastro editorial é separado dos canais de Pautas.

Na aba Miniaturas, gere uma imagem com a chave OpenAI cadastrada em Configurações > Chaves; o estilo e a referência de canal são enviados ao serviço. O texto é adicionado na prévia e o PNG final baixado pelo navegador. O botão Salvar estilo no canal guarda cor, tamanho, posição e instruções visuais. As imagens originais ficam em `ALTA/EditAI/painel/editai_data/thumbs`.

As configurações do estúdio permitem definir modelos para novos funcionários e um teto diário ESTIMADO para imagens OpenAI. Você deve informar um preço por imagem; o limite é uma conta local aproximada, não controla a cobrança real do provedor, outros serviços nem despesas prévias. A página Tempo e custos exibe registros locais e o histórico da fila; não é uma fatura.

Em Acervos, Library of Congress, NASA e Openverse podem ser pesquisados; os resultados levam à fonte para conferência da licença. Esta pesquisa não adiciona o arquivo automaticamente ao filme. A Library of Congress pode bloquear requisições com 403.

Existem novos presets de edição, compostos com os componentes já existentes, e dois estilos adicionais de legenda. A geração via API OpenAI foi testada com resposta simulada, sem cobrança; faça uma geração real após configurar sua chave e verifique o resultado. A função de geração pela própria sessão do Codex sem API não foi validada.


## Janela local e novos recursos

A janela do Edit.AI usa WebView2 e se conecta ao painel local; não é uma aba do navegador. O gerente usa as ferramentas de linha de comando locais do Codex ou do Claude conforme configuração e autenticação; isso não significa controlar conversas abertas nos aplicativos gráficos. O Windows precisa de Python, das dependências instaladas e do WebView2. O atalho aponta para esta pasta e deixa de funcionar se ela for movida.

A NASA está disponível em Acervos para busca de imagens e vídeos sem chave. Existe também um campo opcional de chave NASA para futuras integrações com api.nasa.gov. A busca abre a página de origem: ainda não importa automaticamente mídias para a linha do tempo. Confira os direitos de cada item.

Foram adicionados os cartões Dado em destaque e Linha do tempo, os tons Noite violeta e Oceano turquesa e a textura Documental suave. Os cartões dependem da escolha no painel e da criação correspondente pelo Diretor; no modo enxuto podem ser limitados. Os tons e textura dependem do acabamento estar ativado no fluxo. As prévias dos tons são aproximações. Nenhuma produção real completa foi testada após essas alterações.
