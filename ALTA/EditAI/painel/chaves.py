"""CHAVES DE API no painel (06/11/2026, pedido do usuário: aba com as chaves por ordem de prioridade, o que cada uma
faz e onde conseguir). O painel NUNCA devolve a chave inteira: só se está configurada e os 4 últimos caracteres.
Cada chave é gravada no MESMO arquivo que os scripts já leem (não muda nada no pipeline)."""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # EditAI
ALTA = ROOT.parent                       # CLAUDE CODE ALTA PRODUÇÃO
HOME = Path.home()

# nivel: 1 = obrigatória, 2 = recomendada, 3 = opcional
CHAVES = [
    {"id": "serpapi", "nome": "Busca Google Imagens (SerpAPI)", "nivel": 3,
     "arquivo": ALTA / "chaves" / "serpapi.txt",
     "faz": "Pesquisa imagens de sites na web durante a produção. Sem chave, usa os outros acervos.",
     "links": [["Criar conta e chave SerpAPI", "https://serpapi.com/manage-api-key"]],
     "como": "Crie uma conta SerpAPI e cole a chave. Até seis buscas por produção; cada busca pode consumir sua cota.",
     "custo": "Cota gratuita limitada; planos pagos disponíveis"},
    {"id":"nasa", "nome":"NASA API (opcional)", "nivel":3, "arquivo":ALTA / "chaves" / "nasa.txt",
     "faz":"Chave para serviços api.nasa.gov. A busca da biblioteca de imagens e vídeos usa images-api.nasa.gov e não exige esta chave.",
     "links":[["Obter chave NASA", "https://api.nasa.gov/"]],
     "como":"Cadastre sua chave para futuros serviços NASA que a exijam.", "custo":"Grátis, sujeito a limites"},
    {"id":"openai", "nome":"OpenAI API (imagens)", "nivel":2, "arquivo":ALTA / "chaves" / "openai.txt",
     "faz":"Gera imagens e miniaturas a partir de texto e referências. Cobrança da API separada da assinatura ChatGPT.",
     "links":[["Criar chave da OpenAI", "https://platform.openai.com/api-keys"]],
     "como":"Crie sua chave e configure o faturamento da API; não compartilhe a chave.", "custo":"Pago por uso"},
    {"id": "youtube", "nome": "YouTube Data API v3", "nivel": 1, "arquivo": ROOT / "data" / "youtube_api_key.txt",
     "faz": "Busca vídeos virais, analisa canais (inscritos, views, idade) e acha as pautas e os vídeos de referência.",
     "links": [["1. Ativar a YouTube Data API v3", "https://console.cloud.google.com/apis/library/youtube.googleapis.com"],
               ["2. Criar a chave (Credenciais → Criar credenciais → Chave de API)", "https://console.cloud.google.com/apis/credentials"]],
     "como": "Entre com a sua conta Google, crie um projeto se ele pedir, ative a API no link 1 e crie a chave no link 2.",
     "custo": "Grátis (cota diária)"},
    {"id": "pexels", "nome": "Pexels", "nivel": 1, "grupo": "banco", "arquivo": HOME / ".pexels_key",
     "faz": "Banco grátis de fotos e vídeos em alta qualidade para cobrir os trechos do roteiro. Basta ele OU o Pixabay.",
     "links": [["Pedir a chave da API do Pexels", "https://www.pexels.com/api/new/"]],
     "como": "Crie a conta grátis, preencha o formulário (pode pôr 'uso pessoal em vídeos') e copie a chave que aparece.",
     "custo": "Grátis"},
    {"id": "darkplanner", "nome": "DarkPlanner (narração automática)", "nivel": 2, "arquivo": ALTA / "chaves" / "darkplanner.txt",
     "faz": "Só se você quiser a NARRAÇÃO AUTOMÁTICA: quando o Claude escreve o roteiro das pautas, a voz de IA já é gerada "
            "sozinha. Sem ela você manda o seu próprio roteiro e a sua narração (MP3) em Novo filme e a Sala monta igual.",
     "links": [["Entrar no DarkPlanner e pegar a chave da API", "https://app.darkplanner.com.br"]],
     "como": "Crie a conta, assine um plano com API e copie a chave da API no seu perfil.", "custo": "Pago (plano mensal)"},
    {"id": "fal", "nome": "fal.ai (Nano Banana)", "nivel": 2, "arquivo": ALTA / "chaves" / "fal.txt",
     "faz": "Gera imagens com IA: miniaturas com o seu rosto e cenas com o personagem do canal quando não existe foto real.",
     "links": [["Criar a chave do fal.ai", "https://fal.ai/dashboard/keys"], ["Colocar créditos", "https://fal.ai/dashboard/billing"]],
     "como": "Crie a conta, coloque créditos (a partir de US$ 10) e clique em 'Add key'.",
     "custo": "Pago por imagem (~US$ 0,04 a 0,15)"},
    {"id": "pixabay", "nome": "Pixabay", "nivel": 1, "grupo": "banco", "arquivo": HOME / ".pixabay_key",
     "faz": "Banco grátis de fotos e vídeos. Basta ele OU o Pexels (com os dois o filme tem mais opções).",
     "links": [["Ver a sua chave do Pixabay (faça login antes)", "https://pixabay.com/api/docs/#api_search_images"]],
     "como": "Crie a conta grátis, entre e abra o link: a sua chave aparece em destaque na seção 'Parameters' (key).",
     "custo": "Grátis"},
    {"id": "gemini", "nome": "Google Gemini", "nivel": 3, "arquivo": ALTA / "chaves" / "gemini.txt",
     "faz": "Alternativa para gerar a imagem das miniaturas. Use se não tiver o fal.ai.",
     "links": [["Criar a chave do Gemini", "https://aistudio.google.com/apikey"]],
     "como": "Entre com a conta Google e clique em 'Criar chave de API'. Para gerar imagens é preciso ativar o faturamento.",
     "custo": "Pago para imagens"},
    {"id": "dvids", "nome": "DVIDS (acervo militar dos EUA)", "nivel": 3, "arquivo": HOME / ".dvids_key",
     "faz": "Vídeos e fotos oficiais e gratuitos das Forças Armadas dos EUA. Só ajuda em canais de navios, aviões e guerra.",
     "links": [["Pedir a chave da API do DVIDS", "https://api.dvidshub.net/"]],
     "como": "Abra o link, crie a conta grátis e peça a chave (API key) na página.", "custo": "Grátis"},
]
NIVEL = {1: "Obrigatória", 2: "Recomendada", 3: "Opcional"}


def _le(p):
    try:
        return Path(p).read_text("utf-8-sig").strip()
    except Exception:  # noqa: BLE001
        return ""


def lista():
    out = []
    for c in CHAVES:
        v = _le(c["arquivo"])
        nn = "Obrigatória: esta OU a outra" if c.get("grupo") == "banco" else NIVEL[c["nivel"]]
        out.append({k: c[k] for k in ("id", "nome", "nivel", "faz", "links", "como", "custo")} |
                   {"nivel_nome": nn, "configurada": bool(v), "final": v[-4:] if len(v) >= 8 else ""})
    # 07/11/2026: obrigatório = YouTube + pelo menos UM banco (Pexels ou Pixabay). O resto é opcional.
    falta = [c["nome"] for c, o in zip(CHAVES, out) if c["nivel"] == 1 and not c.get("grupo") and not o["configurada"]]
    if not any(o["configurada"] for c, o in zip(CHAVES, out) if c.get("grupo") == "banco"):
        falta.append("Pexels ou Pixabay (pelo menos um)")
    return {"ok": True, "chaves": out, "faltam_obrigatorias": falta}


def resumo_para_ia():
    """07/11/2026: texto que entra no prompt do Diretor — ele usa SÓ as fontes com chave nesta instalação."""
    tem = {c["id"]: bool(_le(c["arquivo"])) for c in CHAVES}
    ok = [c["nome"] for c in CHAVES if tem[c["id"]]]
    nao = [c["nome"] for c in CHAVES if not tem[c["id"]]]
    regras = []
    if not tem["pexels"] and not tem["pixabay"]:
        regras.append("sem Pexels e sem Pixabay: use Wikimedia Commons, Openverse e outras fontes disponíveis")
    elif not tem["pexels"]:
        regras.append("sem Pexels: o banco de fotos/vídeos é só o Pixabay (os scripts fetch_* já usam só ele)")
    elif not tem["pixabay"]:
        regras.append("sem Pixabay: o banco de fotos/vídeos é só o Pexels")
    if not tem["dvids"]:
        regras.append("sem DVIDS: NÃO escreva data/dvids_queries_*.txt e não rode fetch_dvids")
    if not tem["youtube"]:
        regras.append("sem chave do YouTube: a busca de vídeo usa o yt-dlp sozinha (fetch_video já cai nele)")
    return ("\nCHAVES DE API DESTA INSTALAÇÃO (configuração atual): Wikimedia Commons e Openverse podem ser usados sem chave. Com chave: "
            + (", ".join(ok) or "nenhuma") + ". SEM chave (não existem aqui; não tente, não pare nem peça por elas): "
            + (", ".join(nao) or "nenhuma") + "." + "".join("\n- " + r for r in regras) + "\n")


def salvar(b):
    c = next((x for x in CHAVES if x["id"] == b.get("id")), None)
    if not c:
        return {"ok": False, "erro": "chave desconhecida"}
    v = "".join(str(b.get("valor") or "").split())          # sem espaços nem quebras de linha
    if len(v) < 8:
        return {"ok": False, "erro": "a chave parece curta demais — copie de novo do site"}
    p = Path(c["arquivo"])
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and _le(p):
        p.replace(p.with_name(p.name + ".anterior"))          # guarda a anterior (nada é apagado de vez)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(v, "utf-8")
    os.replace(tmp, p)
    return lista()
