# A Toyota voltou em silêncio ao V8 — o motor V35A da Tundra e os três recalls

Documentário em português, 29 min 38 s, 1920x1080 a 30 quadros por segundo, narração sem trilha.
Versão em português do filme polonês entregue antes ("Toyota po cichu wróciła do V8"): mesmo roteiro
traduzido, mesma curadoria de imagem, texto da tela refeito em português.

## Proporção e regra
Mesma do original: 10 % vídeo e 90 % imagem. O corte final ficou em **11,3 % vídeo e 88,7 % imagem**
(300 cortes: 34 de vídeo e 266 de foto). Com 29,6 min a regra dos cartões pede mais que no polonês:

| Regra | Cálculo | Neste filme |
|---|---|---|
| Cartões em papel | mínimo 1 a cada 2 min | 18 (mínimo 15) |
| Animação de tela cheia | máximo 1 a cada 3 min | 9 (teto 10) |
| Um único tipo de cartão | no máximo metade | 33 % |

## O que foi reaproveitado
A pasta de apagar do filme polonês já tinha sido esvaziada, então os arquivos não existiam mais —
mas as **decisões** estavam intactas em `data/`: as 272 fotos aprovadas, as 57 janelas de vídeo
aprovadas e as rejeições. Nada foi buscado de novo e nenhuma folha de contato foi refeita:
- baixadas de novo só as 272 fotos aprovadas (das 1.655 do pool original);
- baixadas de novo só as 52 janelas de vídeo aprovadas (461 MB);
- as 9 animações, os 18 cartões e os 12 capítulos traduzidos, com as mesmas fotos;
- os 68 parágrafos do português bateram 1 a 1 com os do polonês, então os cartões caíram nos mesmos lugares.

## Números
- 68 parágrafos, 300 cortes, 12 capítulos, 34 sobreposições, 9 animações.
- Todo número na tela é dito na narração, no quadro em que é dito.

## Fontes
- Fotos: Wikimedia Commons, licenças PD/CC0/CC-BY/CC-BY-SA (nunca NC/ND).
  Crédito em `relatorios/attribution.md` (192 clipes: 166 do Commons, 9 do YouTube, 117 com crédito exigido).

## Conferência
- QA de imagem: 0 falhas e 0 avisos.
- QA de áudio: 0 falhas e 0 avisos. Narração normalizada de −24,2 para −14,2 LUFS com limitador.
- Folha do MP4 final revista em três rodadas. Saíram: uma Tundra de salão com o slogan
  "POUR LE TRAVAIL ET LES LOISIRS" na porta, a Tundra FCEV com um gerador **Honda** na caçamba,
  um celular com logotipo de aplicativo e um apresentador falando para a câmera.

## O que mudou no pipeline neste filme
- **Extrator de números em português** (`scripts/build_overlays.py`): "mil" estava na tabela de
  números E na de escalas, e a de números é lida primeiro — "quatrocentos mil" virava 400 + 1.000 =
  **1.400**. Agora "mil" só multiplica. O separador de milhar em português passou a ser o ponto
  ("400.000 km"), e não o espaço.
- **Destaques automáticos**: "NORTE" (de "América do Norte") e "FORCE MAX" (de "i-FORCE MAX")
  saíam como nomes próprios; entraram na lista de exclusão.
- **Re-render incremental**: os segmentos do Remotion leem o timeline que fica gravado no
  **bundle**, não o do disco. Depois de trocar uma foto é preciso refazer o bundle antes de
  re-renderizar — senão o segmento é refeito com a foto velha (foi o que aconteceu com a Tundra
  francesa na segunda rodada).

## Miniaturas
Cinco opções com número dito na narração: 270 mil picapes no recall, 70 mil motores trocados,
os 5,7 L do V8 descartado, os 3,5 L e dois turbos, e os 3 recalls.
