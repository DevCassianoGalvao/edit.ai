# Como buscar e conferir imagens sem trazer coisa fora do tema

Regras aprendidas montando os vídeos do Habib's e das 8 marcas. Duas coisas
diferentes viraram problema em cada um: imagem errada por coincidência de nome
(1º vídeo) e revisão manual demorando tempo/cota demais (2º vídeo — abrir
umas 500 fotos uma por uma esgotou a sessão pra um vídeo só). Este arquivo
existe pra não repetir nenhum dos dois.

**Existem dois modos. Escolha um ANTES de começar, não no meio.**

---

## Modo rápido (padrão) — vídeo em até 30 minutos

Troca "eu olho cada imagem" por "o computador filtra, e eu só confiro uma
amostra pequena". É o modo padrão a menos que o usuário peça explicitamente
"zero erro" ou "confira tudo".

1. **Escrever a busca certa já na primeira tentativa** — regras 1 e 2 abaixo
   (inglês, específica por trecho). Isso sozinho evita a maior parte do lixo,
   sem gastar cota nenhuma.
2. **Se o vídeo é sobre marca específica** (rede, empresa, produto com nome
   próprio) **perguntar logo de cara se o usuário tem as fotos da marca** antes
   de rodar `auto.py`. Banco de imagem grátis não tem foto de marca
   brasileira — tentar buscar mesmo assim é gastar a rodada inteira sabendo que
   vai falhar. Só cair pro banco grátis se o usuário não tiver as fotos ou
   topar imagem genérica (loja de eletrodoméstico qualquer, não a marca X).
3. **Uma rodada de `py auto.py` só.** Não ficar ampliando termo e rodando de
   novo — cada rodada custa tempo real e reabre o problema da regra 5 (abaixo).
4. **Deixar o CLIP local filtrar** (`clipcheck.py`, roda na máquina do
   usuário, grátis, não gasta cota da sessão) em vez de abrir cada imagem.
   Só funciona bem com `mostrar` em inglês (regra 2) — em português ele erra
   pros dois lados.
5. **Eu só abro pessoalmente uma amostra pequena, e só o que tem risco real**
   de colisão de nome: título com nome próprio (pessoa, lugar, marca, evento).
   Título puramente descritivo (`empty store`, `supermarket aisle`,
   `furniture warehouse`) fica por conta do CLIP — não abro um por um.
6. **Aceitar os buracos.** Se uma parte ficar fraca ou vazia, tudo bem — o
   `sincronizar.py` estica o clipe vizinho pra cobrir o tempo, o vídeo não
   quebra. Não vale a pena gastar mais uma rodada de busca por causa de 1-2
   partes fracas.

**A troca que isso implica, pra ficar claro pro usuário se perguntar:** mais
rápido, mas pode passar uma imagem genérica-mas-correta (não a marca exata) e,
raramente, alguma coisa esquisita que só apareceria olhando uma por uma. Isso é
o preço de caber em 30 minutos.

## Modo exaustivo (zero erro) — só quando o usuário pedir

Abrir e olhar **cada imagem baixada, todas, sem amostragem**, incluindo as de
título genérico e as de lote inteiro da mesma fonte. Foi o que gerou a tabela
de colisões de nome abaixo — funciona, mas em ~500 imagens custou a sessão
inteira. Usar só quando o usuário disser algo como "quero zero erro, pode
demorar" ou "confira tudo antes de montar" — não é o padrão.

---

## 1. Busca por trecho específico, não pelo tema geral da parte

Não escrever uma busca genérica de "tema" pra parte inteira (ex: `restaurant
storefront`). Ler o texto exato daquele trecho e tirar dali as entidades, datas
e afirmações concretas que ELE cita — pessoa, marca, cidade, ano, produto — e
buscar exatamente isso.

Exemplo: se o trecho fala "Coca-Cola em 1990", a busca é sobre Coca-Cola nos
anos 90, não "refrigerante" solto. Busca genérica traz qualquer imagem plausível
do assunto amplo, não a cena que está sendo narrada naquele segundo.

## 2. Busca em inglês por padrão

Os bancos gratuitos (Wikimedia, Openverse, DDG, Archive) têm acervo muito maior
em inglês, e a checagem por CLIP (`clipcheck.py`) também julga melhor em inglês
— comparar imagem com texto em português faz ela errar pros dois lados (aprova
lixo, reprova imagem certa).

**Exceção:** nome próprio que só existe em português — lugar brasileiro, pessoa
brasileira, marca brasileira (`Habib's`, `São Paulo`, `Alberto Saraiva`) fica
como está, sem traduzir.

## 3. Ao abrir imagem (amostra no modo rápido, todas no modo exaustivo)

Título de banco de imagem é metadado solto, escrito por outra pessoa, sobre
outra coisa, que por acaso tem a mesma palavra do roteiro. Não vale confiar no
nome do arquivo, no domínio de origem, nem na nota de relevância textual da
curadoria — só serve o que está DENTRO da foto.

Colisões de nome que já aconteceram de verdade, nos vídeos anteriores:

| título da imagem | o que era de verdade |
|---|---|
| `Habib Mohebian` | túmulo de um músico iraniano |
| `Habib's Restaurant` (Reino Unido / Malásia) | restaurante homônimo, não a marca brasileira |
| `Sfiha` / `Corniche sfiha` / `Playa sfiha` | uma ilha/praia no Marrocos, não a comida esfirra |
| `Real Gabinete Português de Leitura` | uma biblioteca no Rio, não a moeda Real |
| `Eduarda Samontezze` | uma artista/DJ, não uma foto de "copos de fast-food" |
| `Brazils Farm` | uma fazenda de cavalos no Reino Unido |
| revista `Judge` (1914-1925) | capa de revista satírica, não foto de juiz |
| `Busy Philipps` | uma atriz americana |
| `Surprise, Arizona` | nome de cidade, não a emoção "surpresa" |
| contrato `Nikkah` | casamento islâmico, não empréstimo bancário |
| `Cable Install at Rubin Observatory` | telescópio, não cabo de fibra óptica |
| `Fire Fighting Appliances` | equipamento de bombeiro, não eletrodoméstico |

## 4. Rejeitar por FORMATO, antes mesmo de julgar o assunto

Nunca usar, mesmo que o título bata com a busca:

- capa de livro ou revista
- ilustração, gravura antiga, pintura, cartaz
- print de tela, gráfico, flowchart, mapa/infográfico
- documento manuscrito ou datilografado
- foto vintage/preto-e-branco quando o vídeo é sobre algo atual
- texto estrangeiro pesado (chinês, japonês, coreano, russo, polonês…)
  dominando a imagem — mesmo sendo foto real, distrai e parece lugar errado

Nenhuma dessas é imagem de b-roll de verdade. A curadoria automática julga
texto, não sabe distinguir uma foto real de uma capa de revista chamada
"Judge" — quem pega isso é o olho.

## 5. `auto.py` não lembra rejeições entre execuções

Mover um arquivo rejeitado pra `downloads/_fora_do_tema` só tira ele da pasta;
a memória de curadoria é recriada do zero a cada `py auto.py`. Rodar de novo pra
preencher outras partes pode trazer o MESMO candidato rejeitado de volta — ele
continua no cache (`_cache_bancos.json`) e continua passando na curadoria por
texto. Já aconteceu várias vezes nos dois vídeos, e é a razão principal pra
regra "uma rodada só" do modo rápido: cada rodada extra reabre esse ciclo.

---

## Ordem de trabalho — modo rápido (padrão)

1. Ler o roteiro. Se for vídeo de marca específica, perguntar pelas fotos da
   marca antes de mais nada.
2. Escrever `plano.json` com `busca`/`mostrar` específicos por trecho, em
   inglês (regras 1 e 2).
3. Rodar `py auto.py` — uma vez só.
4. Abrir só a amostra de risco (nomes próprios) — regra 3. Confiar no CLIP pro
   resto.
5. `py sincronizar.py --capcut` e `py b.py`. Aceitar os buracos.

## Ordem de trabalho — modo exaustivo (só se pedido)

1. Ler o roteiro. Escrever `plano.json` (regras 1 e 2).
2. Rodar `py auto.py`.
3. Abrir e olhar **cada imagem baixada, todas, sem amostragem** (regras 3 e 4).
4. Se rodou `auto.py` de novo depois de já ter conferido alguma parte,
   reconferir essa parte também (regra 5).
5. Só depois de 100% conferido: `py sincronizar.py --capcut` e `py b.py`.
