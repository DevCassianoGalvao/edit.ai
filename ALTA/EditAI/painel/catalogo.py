"""CATÁLOGO de opções de edição do painel — a lista única do que dá para ligar num filme e em que isso vira no
data/pipeline_config.json. O painel desenha as guias a partir daqui; o aplicar.py grava a escolha no config; os
scripts (acabamento, legendas, render_hybrid, render_ranges, build_overlays, music_mix) leem o config.

27/09/2026 (pedido do usuário): guias visuais para escolher legenda, cor, textura, som, cartões, transições, render e
estilos prontos; + "identificador de edição" (painel/estilos/*.json criados a partir de um vídeo de referência).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ESTILOS_DIR = HERE / "estilos"

# cada opção: id, nome, desc, previa (arquivo em painel/previas/), config (mesclado no pipeline_config)
GUIAS = [
    {"id": "legendas", "titulo": "Legendas", "sub": "Texto da narração queimado no vídeo. O .srt para o YouTube sai sempre.",
     "tipo": "escolha", "opcoes": [
        {"id":"turquesa", "nome":"Turquesa", "desc":"Texto turquesa com contorno escuro, para destaques visíveis.", "previa":"leg_turquesa.jpg", "config":{"legendas":{"estilo":"turquesa"}}},
        {"id":"alto_contraste", "nome":"Alto contraste", "desc":"Letras grandes sobre tarja escura, para leitura mais clara.", "previa":"leg_alto_contraste.jpg", "config":{"legendas":{"estilo":"alto_contraste"}}},
        {"id": "off", "nome": "Sem legenda", "desc": "Imagem limpa. O .srt vai junto para subir no YouTube.", "previa": "leg_off.jpg",
         "config": {"legendas": {"estilo": "off"}}},
        {"id": "classica", "nome": "Clássica", "desc": "Branca com contorno, uma linha no rodapé.", "previa": "leg_classica.jpg",
         "config": {"legendas": {"estilo": "classica"}}},
        {"id": "documentario", "nome": "Máquina de escrever", "desc": "Courier em caixa alta sobre fundo escuro. Casa com o arquivo dark.",
         "previa": "leg_documentario.jpg", "config": {"legendas": {"estilo": "documentario"}}},
        {"id": "karaoke", "nome": "Karaokê", "desc": "A palavra falada acende em dourado. Segura atenção.", "previa": "leg_karaoke.jpg",
         "config": {"legendas": {"estilo": "karaoke"}}},
        {"id": "caixa", "nome": "Tarja preta", "desc": "Texto sobre tarja sólida, leitura máxima (estilo TV).", "previa": "leg_caixa.jpg",
         "config": {"legendas": {"estilo": "caixa"}}},
        {"id": "impacto", "nome": "Impacto", "desc": "2–3 palavras por vez, grandes, maiúsculas (true crime / shorts).",
         "previa": "leg_impacto.jpg", "config": {"legendas": {"estilo": "impacto"}}},
        {"id": "minimal", "nome": "Discreta", "desc": "Pequena e clara, quase invisível até você precisar.", "previa": "leg_minimal.jpg",
         "config": {"legendas": {"estilo": "minimal"}}},
        {"id": "serifa", "nome": "Serifa de documentário", "desc": "Garamond pequena e creme, frase inteira no rodapé. Documentário de história (estilo Arquivo Colorizado).",
         "previa": "leg_serifa.jpg", "config": {"legendas": {"estilo": "serifa"}}},
     ]},
    {"id": "cor", "titulo": "Cor", "sub": "A grade de cor aplicada no filme inteiro — vídeo, foto, cartões e animações iguais.",
     "tipo": "escolha", "opcoes": [
        {"id":"editorial", "nome":"Editorial claro", "desc":"Contraste suave e cores moderadas para vídeos explicativos.", "previa":"cor_editorial.jpg", "config":{"acabamento":{"tom":"editorial"}}},
        {"id":"dourado", "nome":"Documentário dourado", "desc":"Tons quentes discretos para história e natureza.", "previa":"cor_dourado.jpg", "config":{"acabamento":{"tom":"dourado"}}},
        {"id":"editai_noite", "nome":"Noite violeta", "desc":"Sombras azuladas e meios-tons violetas para documentários.", "previa":"cor_editai_noite.jpg", "config":{"acabamento":{"tom":"editai_noite"}}},
        {"id":"editai_oceano", "nome":"Oceano turquesa", "desc":"Azul e verde suaves para natureza, ciência e tecnologia.", "previa":"cor_editai_oceano.jpg", "config":{"acabamento":{"tom":"editai_oceano"}}},
        {"id": "neutro", "nome": "Neutro", "desc": "Contraste leve, cor natural um pouco contida.", "previa": "cor_neutro.jpg",
         "config": {"acabamento": {"tom": "neutro"}}},
        {"id": "quente", "nome": "Quente", "desc": "Luz dourada: história, deserto, nostalgia.", "previa": "cor_quente.jpg",
         "config": {"acabamento": {"tom": "quente"}}},
        {"id": "frio", "nome": "Frio", "desc": "Aço e azul: Guerra Fria, indústria, soviético.", "previa": "cor_frio.jpg",
         "config": {"acabamento": {"tom": "frio"}}},
        {"id": "cinema", "nome": "Cinema", "desc": "Sombras azuladas e luz alaranjada, cara de trailer.", "previa": "cor_cinema.jpg",
         "config": {"acabamento": {"tom": "cinema"}}},
        {"id": "sepia", "nome": "Sépia", "desc": "Foto antiga: até os anos 50.", "previa": "cor_sepia.jpg",
         "config": {"acabamento": {"tom": "sepia"}}},
        {"id": "pb", "nome": "Preto e branco", "desc": "Arquivo, guerra, documento.", "previa": "cor_pb.jpg",
         "config": {"acabamento": {"tom": "pb"}}},
     ]},
    {"id": "textura", "titulo": "Textura de filme", "sub": "Grão, vinheta e a tremulação leve de projetor. Passe o mouse para ver em movimento.",
     "tipo": "escolha", "opcoes": [
        {"id":"pelicula_moderna", "nome":"Película moderna", "desc":"Grão médio e vinheta suave, sem tremor.", "previa":"tex_pelicula_moderna.mp4", "config":{"acabamento":{"grao":6,"vinheta":"PI/8","tremor":False}}},
        {"id":"projetor_sutil", "nome":"Projetor sutil", "desc":"Grão discreto com tremulação leve e sem vinheta.", "previa":"tex_projetor_sutil.mp4", "config":{"acabamento":{"grao":2,"vinheta":"off","tremor":True}}},
        {"id":"documental", "nome":"Documental suave", "desc":"Grão discreto com vinheta leve, sem tremor.", "previa":"tex_leve.mp4", "config":{"acabamento":{"grao":2,"vinheta":"PI/8","tremor":False}}},
        {"id": "limpo", "nome": "Limpo", "desc": "Digital, sem grão nem vinheta.", "previa": "tex_limpo.mp4",
         "config": {"acabamento": {"grao": 0, "vinheta": "off", "tremor": False}}},
        {"id": "leve", "nome": "Leve", "desc": "Um toque de película, quase imperceptível.", "previa": "tex_leve.mp4",
         "config": {"acabamento": {"grao": 3, "vinheta": "PI/6", "tremor": False}}},
        {"id": "arquivo", "nome": "Arquivo", "desc": "O padrão atual do canal: grão, vinheta e tremulação.", "previa": "tex_arquivo.mp4",
         "config": {"acabamento": {"grao": 5, "vinheta": "PI/5", "tremor": True}}},
        {"id": "forte", "nome": "Película velha", "desc": "Grão pesado e borda escura, filme de época.", "previa": "tex_forte.mp4",
         "config": {"acabamento": {"grao": 10, "vinheta": "PI/4", "tremor": True}}},
     ]},
    {"id": "som", "titulo": "Som", "sub": "A trilha é pesquisada conforme o tema e o clima do vídeo. Clique para ouvir os exemplos.",
     "tipo": "liga", "opcoes": [
        {"id": "music", "nome": "Trilha automática", "desc": "Busca e escolhe faixas conforme o assunto e o clima de cada trecho; baixa o volume durante a narração.",
         "previa": "som_trilha.mp3", "config_on": {"music": True}, "config_off": {"music": False}},
        {"id": "trilha_baixa", "nome": "Trilha bem baixa", "desc": "A música fica ~20 dB abaixo da voz (-34 LUFS) e sobe pouco nas pausas (-27). Pedido do usuário para o Arquivo Colorizado (04/11/2026).",
         "previa": "", "config_on": {"trilha": {"sob_voz_db": -11, "respiro_db": -4}}, "config_off": {"trilha": {}}},
        {"id": "sfx", "nome": "Efeitos sonoros", "desc": "Golpe grave nas revelações, whoosh nos capítulos, ambiência por lugar.",
         "previa": "som_sfx.mp3", "config_on": {"sfx": True}, "config_off": {"sfx": False}},
        {"id": "voz", "nome": "Voz limpa", "desc": "Tira chiado e o sibilo do “s” da narração antes de tudo. Ouça: 6 s crus, depois os mesmos 6 s limpos.",
         "previa": "som_voz.mp3", "config_on": {"voz_limpa": True}, "config_off": {"voz_limpa": False}},
     ]},
    {"id": "cartoes", "titulo": "Cartões na tela", "sub": "Você pode ativar vários estilos. O Diretor decide onde usá-los; no modo enxuto há limite de cartões e nem todos são garantidos. Passe o mouse para ver em movimento.",
     "tipo": "liga", "opcoes": [
        {"id":"editai_editorial", "nome":"Editorial explicativo", "desc":"Cartão autoral inspirado em vídeos explicativos, com título, texto e fonte.", "previa":"editai_editorial.png", "config_on":{"cartoes_genero":{"editai_editorial":True}}, "config_off":{"cartoes_genero":{"editai_editorial":False}}},
        {"id":"editai_ficha", "nome":"Edit.AI · Dado em destaque", "desc":"Cartão roxo para números, contexto e fonte.", "previa":"editai_ficha.png", "config_on":{"cartoes_genero":{"editai_ficha":True}}, "config_off":{"cartoes_genero":{"editai_ficha":False}}},
        {"id":"editai_linha", "nome":"Edit.AI · Linha do tempo", "desc":"Até quatro marcos em uma cronologia animada.", "previa":"editai_linha.png", "config_on":{"cartoes_genero":{"editai_linha":True}}, "config_off":{"cartoes_genero":{"editai_linha":False}}},
        {"id": "arquivo_dark", "nome": "Família arquivo dark", "desc": "Quadro de provas, checklist, ficha, manchete, lupa, rolo, revela.",
         "previa": "arq_quadrofio.mp4", "config_on": {"arquivo_dark": True}, "config_off": {"arquivo_dark": False}},
        {"id": "paralaxe", "nome": "Fotos em 2.5D", "desc": "O sujeito da foto se descola do fundo (paralaxe).",
         "previa": "arq_paralaxe.mp4", "config_on": {"paralaxe": True}, "config_off": {"paralaxe": False}},
        {"id": "mapa", "nome": "Mapa animado", "desc": "Rota com setas e datas: todo filme tem pelo menos um.",
         "previa": "arq_mapa.mp4", "config_on": {"mapa": True}, "config_off": {"mapa": False}},
        # 04/11/2026 — estilo ARQUIVO COLORIZADO (vídeo de referência de história 1898-1960; scripts/moldura.py +
        # src/scenes/arquivo_colorizado.tsx). Fotos impressas = no make_photos; peças = cenas de tela cheia escritas pelo Diretor.
        {"id": "moldura", "nome": "Fotos impressas na mesa", "desc": "Foto de arquivo vira cópia impressa sobre fundo escuro esfumaçado ou papel quadriculado, com etiqueta laranja (lugar · data), nome+cargo nos retratos e tag de capítulo.",
         "previa": "arq_moldura.jpg", "config_on": {"moldura_fotos": {"ligado": True, "fracao": 0.45}}, "config_off": {"moldura_fotos": {"ligado": False}}},
        {"id": "pecas_colorizado", "nome": "Peças do Arquivo Colorizado", "desc": "Polaroides caindo na mesa, linha do tempo, barras, número grande, citação com tarja laranja e mapa de pergaminho — serifa clássica + laranja.",
         "previa": "ac_polaroids.mp4", "config_on": {"arquivo_colorizado": True}, "config_off": {"arquivo_colorizado": False}},
        # 04/10/2026 — estilos por GÊNERO (src/scenes/estilos5.tsx): ligado = volta 1 vez a cada 3 min, espalhado pelo filme
        {"id": "planta", "temas": ["carros", "militar"], "nome": "Planta técnica", "desc": "Carros, motores, máquinas, navios: a foto vira planta azul com cotas e peças numeradas. Aparece a cada ~3 min.",
         "previa": "arq_planta.mp4", "config_on": {"cartoes_genero": {"planta": True}}, "config_off": {"cartoes_genero": {"planta": False}}},
        {"id": "caderno", "temas": ["arqueologia"], "nome": "Caderno de campo", "desc": "Arqueologia, Egito, pré-história: foto colada no caderno da escavação, notas à mão e etiqueta do achado. Aparece a cada ~3 min.",
         "previa": "arq_caderno.mp4", "config_on": {"cartoes_genero": {"caderno": True}}, "config_off": {"cartoes_genero": {"caderno": False}}},
        {"id": "mercado", "temas": ["carros", "economia"], "nome": "Painel de mercado", "desc": "Economia, mercado de carros, agro, crises: gráfico se desenhando, variação em verde/vermelho e letreiro de cotação. Aparece a cada ~3 min.",
         "previa": "arq_mercado.mp4", "config_on": {"cartoes_genero": {"mercado": True}}, "config_off": {"cartoes_genero": {"mercado": False}}},
        {"id": "radar", "temas": ["militar"], "nome": "Radar tático", "desc": "Guerra, marinha, aviação, resgate: visão noturna com alvos travados e radar varrendo. Aparece a cada ~3 min.",
         "previa": "arq_radar.mp4", "config_on": {"cartoes_genero": {"radar": True}}, "config_off": {"cartoes_genero": {"radar": False}}},
        {"id": "cartao_vhs", "temas": ["nostalgia"], "nome": "Fita VHS retrô", "desc": "Nostalgia, marcas antigas, propaganda dos anos 80-90: PLAY, data na tela e slogan de comercial. Aparece a cada ~3 min.",
         "previa": "arq_vhs.mp4", "config_on": {"cartoes_genero": {"vhs": True}}, "config_off": {"cartoes_genero": {"vhs": False}}},
        # 04/10/2026 (3ª regra): +5 por tema -> cada tema fica com 10 (7 do tema + 3 de todo filme)
        {"id": "velocimetro", "temas": ["carros"], "nome": "Painel de instrumentos", "desc": "Velocímetro de ponteiro sobe até o número (produção, velocidade, vendas) com luzes de alerta piscando. Aparece a cada ~3 min.",
         "previa": "arq_velocimetro.mp4", "config_on": {"cartoes_genero": {"velocimetro": True}}, "config_off": {"cartoes_genero": {"velocimetro": False}}},
        {"id": "raiox", "temas": ["carros"], "nome": "Raio-X do carro", "desc": "A foto vira raio-X e uma linha de varredura revela as peças com nome. Aparece a cada ~3 min.",
         "previa": "arq_raiox.mp4", "config_on": {"cartoes_genero": {"raiox": True}}, "config_off": {"cartoes_genero": {"raiox": False}}},
        {"id": "testecolisao", "temas": ["carros"], "nome": "Teste de colisão", "desc": "Marcadores de crash-test, câmera de alta velocidade e o impacto na tela. Aparece a cada ~3 min.",
         "previa": "arq_testecolisao.mp4", "config_on": {"cartoes_genero": {"testecolisao": True}}, "config_off": {"cartoes_genero": {"testecolisao": False}}},
        {"id": "avisorecall", "temas": ["carros"], "nome": "Aviso de recall", "desc": "Carta oficial com carimbo RECALL, defeito e o número de carros chamados. Aparece a cada ~3 min.",
         "previa": "arq_avisorecall.mp4", "config_on": {"cartoes_genero": {"avisorecall": True}}, "config_off": {"cartoes_genero": {"avisorecall": False}}},
        {"id": "linhamontagem", "temas": ["carros", "economia"], "nome": "Linha de montagem", "desc": "Esteira com carros passando e contador de produção (sobe ou desce quando a fábrica fecha). Aparece a cada ~3 min.",
         "previa": "arq_linhamontagem.mp4", "config_on": {"cartoes_genero": {"linhamontagem": True}}, "config_off": {"cartoes_genero": {"linhamontagem": False}}},
        {"id": "estratigrafia", "temas": ["arqueologia"], "nome": "Camadas do solo", "desc": "Corte do terreno camada por camada com as datas; o achado acende na camada certa. Aparece a cada ~3 min.",
         "previa": "arq_estratigrafia.mp4", "config_on": {"cartoes_genero": {"estratigrafia": True}}, "config_off": {"cartoes_genero": {"estratigrafia": False}}},
        {"id": "papiro", "temas": ["arqueologia"], "nome": "Papiro traduzido", "desc": "Papiro se abre, o texto antigo aparece e a tradução é datilografada embaixo. Aparece a cada ~3 min.",
         "previa": "arq_papiro.mp4", "config_on": {"cartoes_genero": {"papiro": True}}, "config_off": {"cartoes_genero": {"papiro": False}}},
        {"id": "etiquetamuseu", "temas": ["arqueologia"], "nome": "Vitrine de museu", "desc": "A peça iluminada na vitrine com a etiqueta do museu: material, época e número de inventário. Aparece a cada ~3 min.",
         "previa": "arq_etiquetamuseu.mp4", "config_on": {"cartoes_genero": {"etiquetamuseu": True}}, "config_off": {"cartoes_genero": {"etiquetamuseu": False}}},
        {"id": "datacaocarbono", "temas": ["arqueologia"], "nome": "Datação por carbono-14", "desc": "Curva de decaimento se desenhando e o contador de anos do laudo do laboratório. Aparece a cada ~3 min.",
         "previa": "arq_datacaocarbono.mp4", "config_on": {"cartoes_genero": {"datacaocarbono": True}}, "config_off": {"cartoes_genero": {"datacaocarbono": False}}},
        {"id": "escaneamento3d", "temas": ["arqueologia"], "nome": "Escaneamento 3D", "desc": "Malha 3D varre a foto com pontos medidos: reconstrução científica. Aparece a cada ~3 min.",
         "previa": "arq_escaneamento3d.mp4", "config_on": {"cartoes_genero": {"escaneamento3d": True}}, "config_off": {"cartoes_genero": {"escaneamento3d": False}}},
        {"id": "quadriculaescavacao", "temas": ["arqueologia"], "nome": "Quadrícula da escavação", "desc": "Vista de cima do sítio com a grade de barbante; os quadrados dos achados acendem. Aparece a cada ~3 min.",
         "previa": "arq_quadriculaescavacao.mp4", "config_on": {"cartoes_genero": {"quadriculaescavacao": True}}, "config_off": {"cartoes_genero": {"quadriculaescavacao": False}}},
        {"id": "cupomfiscal", "temas": ["economia"], "nome": "Cupom fiscal", "desc": "Cupom sai da impressora linha por linha com os valores e o TOTAL no fim. Aparece a cada ~3 min.",
         "previa": "arq_cupomfiscal.mp4", "config_on": {"cartoes_genero": {"cupomfiscal": True}}, "config_off": {"cartoes_genero": {"cupomfiscal": False}}},
        {"id": "rankingbarras", "temas": ["economia"], "nome": "Ranking em barras", "desc": "Barras horizontais crescendo uma a uma, o item do filme em destaque. Aparece a cada ~3 min.",
         "previa": "arq_rankingbarras.mp4", "config_on": {"cartoes_genero": {"rankingbarras": True}}, "config_off": {"cartoes_genero": {"rankingbarras": False}}},
        {"id": "rosca", "temas": ["economia"], "nome": "Gráfico de rosca", "desc": "Rosca enche até a porcentagem com o número contando no meio. Aparece a cada ~3 min.",
         "previa": "arq_rosca.mp4", "config_on": {"cartoes_genero": {"rosca": True}}, "config_off": {"cartoes_genero": {"rosca": False}}},
        {"id": "pilhadinheiro", "temas": ["economia"], "nome": "Pilha de dinheiro", "desc": "Pilhas de cédulas subindo até o valor, com o contador em cima. Aparece a cada ~3 min.",
         "previa": "arq_pilhadinheiro.mp4", "config_on": {"cartoes_genero": {"pilhadinheiro": True}}, "config_off": {"cartoes_genero": {"pilhadinheiro": False}}},
        {"id": "contratocarimbo", "temas": ["economia", "nostalgia"], "nome": "Contrato carimbado", "desc": "Contrato na mesa, assinatura se desenha e o carimbo bate: INADIMPLENTE, FALÊNCIA, QUITADO. Aparece a cada ~3 min.",
         "previa": "arq_contratocarimbo.mp4", "config_on": {"cartoes_genero": {"contratocarimbo": True}}, "config_off": {"cartoes_genero": {"contratocarimbo": False}}},
        {"id": "dossiesecreto", "temas": ["militar"], "nome": "Dossiê secreto", "desc": "Pasta TOP SECRET: as tarjas pretas saem e revelam as palavras-chave. Aparece a cada ~3 min.",
         "previa": "arq_dossiesecreto.mp4", "config_on": {"cartoes_genero": {"dossiesecreto": True}}, "config_off": {"cartoes_genero": {"dossiesecreto": False}}},
        {"id": "sonar", "temas": ["militar"], "nome": "Sonar de submarino", "desc": "Tela de sonar com pings, contatos aparecendo com rumo e distância e a profundidade. Aparece a cada ~3 min.",
         "previa": "arq_sonar.mp4", "config_on": {"cartoes_genero": {"sonar": True}}, "config_off": {"cartoes_genero": {"sonar": False}}},
        {"id": "comparaforcas", "temas": ["militar"], "nome": "Comparação de forças", "desc": "Os dois lados em colunas, ícones de navios/aviões/tanques contando. Aparece a cada ~3 min.",
         "previa": "arq_comparaforcas.mp4", "config_on": {"cartoes_genero": {"comparaforcas": True}}, "config_off": {"cartoes_genero": {"comparaforcas": False}}},
        {"id": "periscopio", "temas": ["militar"], "nome": "Periscópio / binóculo", "desc": "A foto vista pelo periscópio com retícula, rumo e distância. Aparece a cada ~3 min.",
         "previa": "arq_periscopio.mp4", "config_on": {"cartoes_genero": {"periscopio": True}}, "config_off": {"cartoes_genero": {"periscopio": False}}},
        {"id": "placaidentificacao", "temas": ["militar"], "nome": "Placa de identificação", "desc": "Plaquinha militar de metal gravada, girando na luz. Aparece a cada ~3 min.",
         "previa": "arq_placaidentificacao.mp4", "config_on": {"cartoes_genero": {"placaidentificacao": True}}, "config_off": {"cartoes_genero": {"placaidentificacao": False}}},
        {"id": "tvtubo", "temas": ["nostalgia"], "nome": "TV de tubo", "desc": "Televisão antiga liga com a linha branca e mostra a foto com chuvisco e canal. Aparece a cada ~3 min.",
         "previa": "arq_tvtubo.mp4", "config_on": {"cartoes_genero": {"tvtubo": True}}, "config_off": {"cartoes_genero": {"tvtubo": False}}},
        {"id": "anunciorevista", "temas": ["nostalgia"], "nome": "Anúncio de revista", "desc": "Página de revista antiga: foto retícula, chamada retrô e preço em cruzeiros. Aparece a cada ~3 min.",
         "previa": "arq_anunciorevista.mp4", "config_on": {"cartoes_genero": {"anunciorevista": True}}, "config_off": {"cartoes_genero": {"anunciorevista": False}}},
        {"id": "polaroids", "temas": ["nostalgia"], "nome": "Fotos instantâneas", "desc": "Polaroides caindo na mesa com legenda à caneta. Aparece a cada ~3 min.",
         "previa": "arq_polaroids.mp4", "config_on": {"cartoes_genero": {"polaroids": True}}, "config_off": {"cartoes_genero": {"polaroids": False}}},
        {"id": "evolucaomarca", "temas": ["nostalgia"], "nome": "Evolução da marca", "desc": "Linha do tempo da marca, ano a ano, até o FIM em vermelho. Aparece a cada ~3 min.",
         "previa": "arq_evolucaomarca.mp4", "config_on": {"cartoes_genero": {"evolucaomarca": True}}, "config_off": {"cartoes_genero": {"evolucaomarca": False}}},
        {"id": "etiquetapreco", "temas": ["nostalgia"], "nome": "Etiqueta de preço", "desc": "Etiqueta de mercado: preço antigo riscado, preço novo e quanto subiu. Aparece a cada ~3 min.",
         "previa": "arq_etiquetapreco.mp4", "config_on": {"cartoes_genero": {"etiquetapreco": True}}, "config_off": {"cartoes_genero": {"etiquetapreco": False}}},
     ]},
    {"id": "destaque", "titulo": "Destaques de nome e número", "sub": "Quando a narração cita lugar, data, nome ou número.",
     "tipo": "escolha", "opcoes": [
        {"id":"editorial", "nome":"Editorial explicativo", "desc":"Tarja clara com detalhe dourado para nomes, lugares e dados.", "previa":"dest_editorial.png", "config":{"estilo_destaque":"editorial"}},
        {"id": "documentario", "nome": "Documentário", "desc": "Versalete branco, fio fino, sem caixa. Sóbrio, tipo HISTORY.",
         "previa": "dest_documentario.png", "config": {"estilo_destaque": "documentario"}},
        {"id": "dinamico", "nome": "Dinâmico", "desc": "Barra de cor entrando da esquerda, caixa alta. Mais pop.",
         "previa": "dest_dinamico.png", "config": {"estilo_destaque": "dinamico"}},
        {"id": "tecnico", "nome": "Técnico", "desc": "Moldura com cantos e colchetes, cara de relatório.",
         "previa": "dest_tecnico.png", "config": {"estilo_destaque": "tecnico"}},
     ]},
    {"id": "transicao", "titulo": "Respiro e enquadramento", "sub": "Pausa entre capítulos, formato da tela e definição da imagem.",
     "tipo": "liga", "opcoes": [
        {"id":"barras_sutis", "nome":"Barras discretas", "desc":"Faixas pretas finas. Se barras de cinema também estiverem ligadas, prevalecem as maiores.", "previa":"tr_barras_sutis.jpg", "config_on":{"acabamento":{"barras_sutis":True}}, "config_off":{"acabamento":{"barras_sutis":False}}},
        {"id": "mergulho", "nome": "Mergulho no preto", "desc": "Meio segundo de preto em cada troca de capítulo — respiro.",
         "previa": "tr_mergulho.mp4", "config_on": {"acabamento": {"mergulho_capitulo": True}},
         "config_off": {"acabamento": {"mergulho_capitulo": False}}},
        {"id": "barras", "nome": "Barras de cinema", "desc": "Faixas pretas de cinema em cima e embaixo (~2,18:1, sem cobrir os destaques).", "previa": "tr_barras.jpg",
         "config_on": {"acabamento": {"barras": True}}, "config_off": {"acabamento": {"barras": False}}},
        {"id": "nitidez", "nome": "Nitidez leve", "desc": "Devolve definição ao stock que chegou amaciado.", "previa": "tr_nitidez.jpg",
         "config_on": {"acabamento": {"nitidez": 0.4}}, "config_off": {"acabamento": {"nitidez": 0}}},
     ]},
    {"id": "transicoes", "titulo": "Transições nos cortes", "sub": "O que acontece na troca de uma imagem para a outra. Passe o mouse para ver o corte acontecendo.",
     "tipo": "escolha", "opcoes": [
        {"id":"flash_suave", "nome":"Flash suave", "desc":"Clarão curto e discreto para marcar uma virada.", "previa":"trc_flash_suave.mp4", "config":{"transicao":{"tipo":"flash_suave"}}},
        {"id": "seco", "nome": "Corte seco", "desc": "A troca direta, sem efeito. Clássico de documentário.", "previa": "trc_seco.mp4",
         "config": {"transicao": {"tipo": "seco"}}},
        {"id": "punch", "nome": "Punch-in", "desc": "Zoom seco de 6 % logo depois do corte. Micro-movimento que prende o olho.",
         "previa": "trc_punch.mp4", "config": {"transicao": {"tipo": "punch"}}},
        {"id": "flash", "nome": "Flash", "desc": "Clarão branco rápido no corte. Bom para revelação.", "previa": "trc_flash.mp4",
         "config": {"transicao": {"tipo": "flash"}}},
        {"id": "whip", "nome": "Whip (chicote)", "desc": "Desfoque de movimento lateral atravessando o corte. Energia.",
         "previa": "trc_whip.mp4", "config": {"transicao": {"tipo": "whip"}}},
        {"id": "glitch", "nome": "Glitch", "desc": "Cores separadas e deslocadas por um instante. Digital, tenso.",
         "previa": "trc_glitch.mp4", "config": {"transicao": {"tipo": "glitch"}}},
        {"id": "queima", "nome": "Queima de película", "desc": "Clarão laranja de filme queimando (film burn). Arquivo e nostalgia.",
         "previa": "trc_queima.mp4", "config": {"transicao": {"tipo": "queima"}}},
        {"id": "luz", "nome": "Luz vazada", "desc": "Um vazamento de luz quente e suave passa pelo corte. Cinematográfico.",
         "previa": "trc_luz.mp4", "config": {"transicao": {"tipo": "luz"}}},
        {"id": "fusao", "nome": "Fusão escura", "desc": "A imagem respira para o escuro e volta (~0,6 s). Imita a fusão lenta do documentário de arquivo.",
         "previa": "trc_fusao.mp4", "config": {"transicao": {"tipo": "fusao"}}},
     ]},
    {"id": "ritmo", "titulo": "Quando a transição aparece", "sub": "Pesquisa de retenção: uma quebra de padrão a cada 30–60 s segura o espectador sem cansar.",
     "tipo": "escolha", "opcoes": [
        {"id": "capitulos", "nome": "Só nos capítulos", "desc": "Marca cada virada da história. Mais sóbrio.", "previa": "",
         "barras": {"qualidade": 2, "velocidade": 1}, "config": {"transicao": {"freq": "capitulos"}}},
        {"id": "ritmo", "nome": "Ritmo (~45 s)", "desc": "Capítulos + uma quebra de padrão a cada ~45 s. O recomendado.", "previa": "",
         "barras": {"qualidade": 4, "velocidade": 3}, "config": {"transicao": {"freq": "ritmo"}}},
        {"id": "todos", "nome": "Todos os cortes", "desc": "Em cada troca de imagem. Muito dinâmico — use com punch ou flash.", "previa": "",
         "barras": {"qualidade": 5, "velocidade": 5}, "config": {"transicao": {"freq": "todos"}}},
     ]},
    {"id": "texturas", "titulo": "Texturas por cima", "sub": "Camadas sobre o filme inteiro. Passe o mouse para ver em movimento.",
     "tipo": "liga", "opcoes": [
        {"id":"grao_fino", "nome":"Grão fino contínuo", "desc":"Textura leve sobre a imagem inteira; pode ser combinada com outras camadas.", "previa":"tex_grao_fino.mp4", "config_on":{"texturas":{"grao_fino":True}}, "config_off":{"texturas":{"grao_fino":False}}},
        {"id": "poeira", "nome": "Poeira e riscos", "desc": "Pontos e riscos verticais de película velha.", "previa": "txt_poeira.mp4",
         "config_on": {"texturas": {"poeira": True}}, "config_off": {"texturas": {"poeira": False}}},
        {"id": "vhs", "nome": "VHS", "desc": "Linhas de varredura, cor desalinhada e chiado de fita.", "previa": "txt_vhs.mp4",
         "config_on": {"texturas": {"vhs": True}}, "config_off": {"texturas": {"vhs": False}}},
        {"id": "papel", "nome": "Papel", "desc": "Fibra de papel por cima de tudo, como dossiê impresso.", "previa": "txt_papel.mp4",
         "config_on": {"texturas": {"papel": True}}, "config_off": {"texturas": {"papel": False}}},
        {"id": "luz_vazada", "nome": "Luz vazada contínua", "desc": "Manchas de luz quente passeando pelo quadro.", "previa": "txt_luz_vazada.mp4",
         "config_on": {"texturas": {"luz_vazada": True}}, "config_off": {"texturas": {"luz_vazada": False}}},
     ]},
    {"id": "render", "titulo": "Render", "sub": "Todas em 1080p. A diferença é quanto tempo o PC gasta comprimindo.",
     "tipo": "escolha", "opcoes": [
        {"id": "alta", "nome": "Alta", "desc": "A qualidade de sempre. Para o upload final.", "previa": "",
         "barras": {"qualidade": 5, "velocidade": 2}, "config": {"render": {"qualidade": "alta"}}},
        {"id": "media", "nome": "Média", "desc": "Quase igual no YouTube, um pouco mais rápida.", "previa": "",
         "barras": {"qualidade": 4, "velocidade": 3}, "config": {"render": {"qualidade": "media"}}},
        {"id": "rapida", "nome": "Rápida", "desc": "Compressão mais leve. Boa para testar e para canais de volume.", "previa": "",
         "barras": {"qualidade": 3, "velocidade": 4}, "config": {"render": {"qualidade": "rapida"}}},
     ]},
]

EXTRAS = [  # interruptores fora das guias
    {"id": "rascunho", "nome": "Rascunho 720p antes do render", "desc": "Um MP4 leve em poucos minutos (sem animações) para você assistir no celular antes do render final.",
     "config_on": {"render": {"rascunho": True}}, "config_off": {"render": {"rascunho": False}}},
    {"id": "shorts", "nome": "Shorts 9:16 automáticos", "desc": "3 cortes verticais de ~55 s (gancho + 2 capítulos) com legenda de impacto, prontos para Shorts/Reels/TikTok.",
     "config_on": {"entrega": {"shorts": 3}}, "config_off": {"entrega": {"shorts": 0}}},
    {"id": "publicacao", "nome": "Pacote de publicação", "desc": "5 opções de título, descrição com capítulos e créditos, e tags — num arquivo pronto para colar no YouTube.",
     "config_on": {"entrega": {"publicacao": True}}, "config_off": {"entrega": {"publicacao": False}}},
]

# estilos prontos: combinações das guias (a escolha de cada guia + interruptores)
PRONTOS = [
    {"id": "arquivo-dark", "nome": "Arquivo Dark", "desc": "O padrão do canal: arquivo de investigação, grão e cartões em papel. Sem trilha.",
     "escolhas": {"legendas": "off", "cor": "neutro", "textura": "arquivo", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": False, "sfx": False, "voz": False, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": False}},
    {"id": "guerra-arquivo", "nome": "Guerra — Arquivo P&B", "desc": "Preto e branco, película velha, mergulho entre capítulos, trilha tensa.",
     "escolhas": {"legendas": "documentario", "cor": "pb", "textura": "forte", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": False, "nitidez": False, "radar": True}},
    {"id": "history", "nome": "HISTORY / Nat Geo", "desc": "Trilha por clima, golpe grave nas revelações, cor cinema e textura leve.",
     "escolhas": {"legendas": "off", "cor": "cinema", "textura": "leve", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": False, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": True, "nitidez": True}},
    {"id": "true-crime", "nome": "True crime / Mistério", "desc": "Frio, barras de cinema, legenda de impacto e cartões de investigação.",
     "escolhas": {"legendas": "impacto", "cor": "frio", "textura": "arquivo", "destaque": "tecnico", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": True, "nitidez": False}},
    {"id": "retro", "nome": "Retrô anos 50", "desc": "Sépia com película velha: nostalgia, marcas e indústrias do passado.",
     "escolhas": {"legendas": "off", "cor": "sepia", "textura": "forte", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": False, "voz": True, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": False, "nitidez": False}},
    {"id": "explicativo", "nome": "Explicativo limpo", "desc": "Imagem limpa e nítida, legenda karaokê, destaques técnicos. Engenharia e tecnologia.",
     "escolhas": {"legendas": "karaoke", "cor": "neutro", "textura": "limpo", "destaque": "tecnico", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": False, "voz": True, "arquivo_dark": False, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": True, "planta": True, "mercado": True}},
    # 28/09/2026 — estilos da pesquisa (tendências 2025-26 adaptadas a documentário)
    {"id": "netflix", "nome": "Netflix documental", "desc": "Cor de cinema, barras, legenda discreta e luz vazada só nas viradas de capítulo.",
     "escolhas": {"legendas": "minimal", "cor": "cinema", "textura": "leve", "destaque": "documentario", "render": "alta", "transicoes": "luz", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": False, "voz": True, "arquivo_dark": False, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": True, "nitidez": True}},
    {"id": "vhs90", "nome": "VHS anos 90", "desc": "Fita VHS: linhas de varredura, cor quente, glitch no ritmo. Nostalgia de marcas e TV.",
     "escolhas": {"legendas": "classica", "cor": "quente", "textura": "leve", "destaque": "dinamico", "render": "alta", "transicoes": "glitch", "ritmo": "ritmo"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": False, "paralaxe": False, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": False, "vhs": True, "cartao_vhs": True}},
    {"id": "policial", "nome": "Arquivo policial", "desc": "Dossiê: frio, papel e poeira por cima, flash nas revelações, cartões de investigação.",
     "escolhas": {"legendas": "documentario", "cor": "frio", "textura": "arquivo", "destaque": "tecnico", "render": "alta", "transicoes": "flash", "ritmo": "capitulos"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": False, "nitidez": False, "poeira": True, "papel": True}},
    {"id": "explicativo-dinamico", "nome": "Explicativo dinâmico", "desc": "Quebra de padrão a cada ~45 s com punch-in, legenda karaokê e destaques dinâmicos.",
     "escolhas": {"legendas": "karaoke", "cor": "neutro", "textura": "limpo", "destaque": "dinamico", "render": "alta", "transicoes": "punch", "ritmo": "ritmo"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": False, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": True}},
    # 04/10/2026 — estilos por GÊNERO com os cartões novos
    {"id": "carros", "nome": "Carros e engenharia", "desc": "Planta técnica nas máquinas e painel de mercado nos números. Neutro, limpo, nítido.",
     "escolhas": {"legendas": "off", "cor": "neutro", "textura": "leve", "destaque": "tecnico", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": False, "sfx": False, "voz": False, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": True, "planta": True, "mercado": True}},
    {"id": "arqueologia", "nome": "Arqueologia e história antiga", "desc": "Caderno de campo da escavação, cor quente e película leve. Egito, múmias, pré-história.",
     "escolhas": {"legendas": "off", "cor": "quente", "textura": "arquivo", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": False, "sfx": False, "voz": False, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": False, "caderno": True}},
    {"id": "economia", "nome": "Economia e crise", "desc": "Painel de mercado com gráfico e letreiro, frio e sóbrio. Agro, bancos, mercado de carros.",
     "escolhas": {"legendas": "off", "cor": "frio", "textura": "leve", "destaque": "tecnico", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": False, "sfx": False, "voz": False, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": False, "barras": False, "nitidez": True, "mercado": True}},
    {"id": "militar", "nome": "Militar e naval", "desc": "Radar tático e visão noturna, frio, película leve. Guerra, marinha, aviação, resgate.",
     "escolhas": {"legendas": "off", "cor": "frio", "textura": "leve", "destaque": "documentario", "render": "alta", "transicoes": "seco", "ritmo": "capitulos"},
     "liga": {"music": False, "sfx": False, "voz": False, "arquivo_dark": True, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": False, "nitidez": True, "radar": True}},
    {"id": "epico", "nome": "Épico cinematográfico", "desc": "Cinema com barras, whip no ritmo, luz vazada contínua, trilha e golpes graves.",
     "escolhas": {"legendas": "off", "cor": "cinema", "textura": "leve", "destaque": "documentario", "render": "alta", "transicoes": "whip", "ritmo": "ritmo"},
     "liga": {"music": True, "sfx": True, "voz": True, "arquivo_dark": False, "paralaxe": True, "mapa": True,
              "mergulho": True, "barras": True, "nitidez": True, "luz_vazada": True}},
]


# Novas combinações de componentes já suportados pelo render.
for _id, _nome, _desc, _base, _choices, _switches in [
    ("editorial-explicativo", "Editorial explicativo", "Visual claro inspirado em documentários explicativos, com cartão editorial e flash suave.", "explicativo", {"legendas":"off", "cor":"editorial", "textura":"documental", "destaque":"editorial", "transicoes":"flash_suave", "ritmo":"capitulos"}, {"editai_editorial":True}),
    ("noir-informativo", "Noir informativo", "Tons frios, cartões de arquivo e legendas discretas.", "true-crime", {"legendas":"minimal", "transicoes":"fusao"}, {"mapa":True}),
    ("engenharia-limpa", "Engenharia limpa", "Visual técnico com legendas em caixa e diagramas de peças.", "carros", {"legendas":"caixa", "cor":"neutro"}, {"planta":True,"paralaxe":True}),
    ("historia-sepia", "História em sépia", "Arquivo em sépia, legendas serifadas e documentação visual.", "retro", {"legendas":"serifa","textura":"arquivo"}, {"caderno":True,"mapa":True}),
    ("economia-dinamica", "Economia dinâmica", "Destaques técnicos, painéis de mercado e legendas de impacto.", "economia", {"legendas":"impacto","destaque":"tecnico"}, {"mercado":True})]:
    _orig = next(x for x in PRONTOS if x["id"] == _base)
    PRONTOS.append({"id":_id,"nome":_nome,"desc":_desc,"preview_base":_base,
                    "escolhas":{**_orig["escolhas"],**_choices},"liga":{**_orig["liga"],**_switches}})


def mescla(a, b):
    out = dict(a)
    for k, v in (b or {}).items():
        out[k] = mescla(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def config_de(escolhas, liga):
    """{"legendas": "karaoke", ...} + {"music": True, ...} -> pedaço do pipeline_config."""
    cfg = {"acabamento": {"desligado": False, "leve": False}} if any(k in escolhas for k in ("cor", "textura", "transicoes")) or any(liga.get(k) for k in ("mergulho", "barras", "barras_sutis", "nitidez", "poeira", "vhs", "papel", "luz_vazada", "grao_fino")) else {}
    for g in GUIAS:
        for o in g["opcoes"]:
            if g["tipo"] == "escolha" and escolhas.get(g["id"]) == o["id"]:
                cfg = mescla(cfg, o["config"])
            if g["tipo"] == "liga" and o["id"] in liga:
                cfg = mescla(cfg, o["config_on"] if liga[o["id"]] else o["config_off"])
    for e in EXTRAS:
        if e["id"] in liga:
            cfg = mescla(cfg, e["config_on"] if liga[e["id"]] else e["config_off"])
    return cfg


def meus_estilos():
    out = []
    for p in sorted(ESTILOS_DIR.glob("*.json")):
        try:
            e = json.loads(p.read_text("utf-8"))
            e.setdefault("id", p.stem)
            e["meu"] = True
            out.append(e)
        except Exception:  # noqa: BLE001
            pass
    return out


TEMAS = [  # 04/10/2026: agrupamento dos cartões no painel (cada um = 7 do tema + 3 de todo filme)
    {"id": "carros", "nome": "Carros e engenharia", "desc": "seu canal, crises de montadora, fábricas"},
    {"id": "arqueologia", "nome": "Arqueologia e história antiga", "desc": "Egito, múmias, pré-história"},
    {"id": "economia", "nome": "Economia e crise", "desc": "dívidas, crédito rural, falências, preços"},
    {"id": "militar", "nome": "Militar e naval", "desc": "guerra, porta-aviões, submarinos, resgates"},
    {"id": "nostalgia", "nome": "Nostalgia e marcas", "desc": "TV Nostalgia, marcas que sumiram, propaganda antiga"},
]

# estilo pronto de cada tema liga TODOS os cartões do tema (a cota de 1 a cada 3 min se divide entre eles)
PRONTO_TEMA = {"carros": "carros", "arqueologia": "arqueologia", "economia": "economia", "militar": "militar",
               "guerra-arquivo": "militar", "vhs90": "nostalgia", "retro": "nostalgia"}
for _p in PRONTOS:
    _t = PRONTO_TEMA.get(_p["id"])
    if _t:
        for _o in next(g for g in GUIAS if g["id"] == "cartoes")["opcoes"]:
            if _t in (_o.get("temas") or []):
                _p["liga"][_o["id"]] = True


def catalogo():
    return {"guias": GUIAS, "temas": TEMAS, "extras": EXTRAS, "prontos": [dict(p, previa=f"estilo_{p.get('preview_base', p['id'])}.jpg") for p in PRONTOS],
            "meus": meus_estilos()}
