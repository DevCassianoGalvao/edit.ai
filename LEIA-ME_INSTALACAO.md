# Dark Empire Videos — instalação (sem canais, sem chaves)

Este pacote tem a ferramenta inteira, pronta para uso:
- o painel (Central, fila, pautas) e o escritório 3D;
- os funcionários automáticos (gerente, Diretor, juízes de fotos e vídeo, revisora, pesquisador, analista e roteirista);
- os scripts de vídeo, os efeitos e a trilha, as regras (PIPELINE.md e a memória do Claude, só as da ferramenta);
- um modelo para cadastrar os seus canais.

NÃO tem: canais cadastrados, chaves/senhas/cookies, bancos de fotos, filmes antigos, fila ou logs.

## 1. Instale antes (uma vez só)

| Programa | Onde baixar | Observação |
|---|---|---|
| **Python 3.12 ou mais novo** | python.org | marque **"Add python.exe to PATH"** |
| **Node.js 20 ou mais novo** (LTS) | nodejs.org | |
| **Git for Windows** | git-scm.com | traz o **Git Bash**, que os scripts usam |
| **ffmpeg** (versão "full") | gyan.dev/ffmpeg/builds | descompacte e ponha a pasta `bin` no PATH |
| **App do Claude** (desktop) | claude.ai/download | entre na sua conta; a aba **Code** é onde o Claude trabalha |
| Placa NVIDIA (opcional) | | deixa a transcrição e o render bem mais rápidos; sem ela tudo roda, só demora mais |

## 2. Instale a ferramenta

1. Descompacte o .zip em qualquer pasta (por exemplo, Downloads).
2. Dê dois cliques em **INSTALAR.bat** e responda `s` quando perguntar. Ele:
   - copia a ferramenta para a Área de Trabalho, em `CLAUDE CODE ALTA PRODUÇÃO`;
   - copia a pasta de trabalho do Claude para `Downloads\mapa` (com os agentes);
   - põe as regras da memória do Claude no lugar certo;
   - troca os caminhos do PC antigo pelos deste PC;
   - instala as bibliotecas Python e as do vídeo (leva 10–20 min);
   - pergunta se cria as tarefas do Agendador (religam o gerente e o painel sozinhos) e o atalho **Dark Empire Videos**.

## 3. Coloque as suas chaves

Abra `CLAUDE CODE ALTA PRODUÇÃO\chaves\LEIA-ME.txt`: ele lista cada chave, o nome do arquivo e a pasta.
Sem as chaves o painel abre, mas busca de vídeos, voz e fotos não funcionam.

## 4. Cadastre os seus canais

O painel começa **sem canais**. Abra `yt milionario teste\painel\canais.exemplo.json`, copie o item de exemplo para
`canais.json` (dentro de `{"canais": [...]}`), preencha com os dados do seu canal e reinicie o painel.
Se preferir, abra a pasta `Downloads\mapa` no app do Claude e peça: "cadastre este canal no painel".
Sem canal cadastrado você ainda pode mandar filmes pelo botão **Novo filme** (roteiro + áudio).

## 5. Primeiro uso

1. Dê dois cliques em **Dark Empire Videos** na Área de Trabalho (abre a Central com tudo ligado), ou rode
   `yt milionario teste\painel\ABRIR_PAINEL.bat` (http://127.0.0.1:8765).
2. Os funcionários começam **desligados**: ligue no botão da Central/escritório quando quiser que trabalhem sozinhos.
3. Abra o app do Claude, aba **Code**, abra a pasta `Downloads\mapa` e escreva **painel**: o Claude assume o protocolo.

## 6. Se algo travar

- **Antivírus (360 e parecidos):** ponha exceção para a pasta da ferramenta, o `python.exe`, o `claude.exe` e o `codex.exe`.
- **Claude ou ChatGPT Codex:** na aba **Chaves** do painel você escolhe qual IA faz o trabalho (a sua conta do Claude ou a do ChatGPT, logada no app).
- **Disco:** cada filme usa 15–25 GB enquanto é feito; mantenha pelo menos 30 GB livres e esvazie as pastas `APAGAR_*` depois de aprovar os filmes.
- **Memória (16 GB):** feche o Chrome durante o render; faltando memória o render fica 4–5x mais lento.
- **E-mail do Wikimedia:** alguns scripts (`make_clips.py`, `photo_retry.py`, `fetch_fotos_thumb_*.py`) se identificam ao Wikimedia com
  `seu-email@exemplo.com`. Funciona assim, mas a boa prática é trocar pelo seu e-mail real (procure essa frase nos scripts).
- **Qualquer outra coisa:** peça ao Claude na pasta `Downloads\mapa`; ele tem as regras e sabe como tudo funciona
  (veja também `yt milionario teste\PIPELINE.md`).
