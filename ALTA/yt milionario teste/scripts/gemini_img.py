"""FUNDO DE MINIATURA com o Gemini ("Nano Banana") — 07/10/2026, pedido do usuário.

Chave em <ALTA PRODUÇÃO>/chaves/gemini.txt (NUNCA imprimir). A IA gera SÓ a imagem (sem texto); o texto da miniatura
continua sendo aplicado pelo make_thumb (número dourado + palavra branca, Anton) — IA erra letra/número.
Regras de prompt: sem texto/letras/logos/marcas d'água, sem rosto de pessoa real, sem logo de montadora em destaque.

  python gemini_img.py "descrição da cena" saida.png [--modelo gemini-2.5-flash-image] [--n 3] [--formato 16:9]
  python gemini_img.py --teste      # 1 imagem pequena para medir se a cota grátis gera imagem
"""
import base64, json, sys, time, urllib.error, urllib.request
from pathlib import Path

CHAVE = Path(__file__).resolve().parents[2] / "chaves" / "gemini.txt"
if not CHAVE.exists():
    CHAVE = Path(__file__).resolve().parents[3] / "chaves" / "gemini.txt"
BASE = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
REGRAS = ("Photorealistic YouTube documentary thumbnail background, 16:9, dramatic cinematic lighting, high contrast, "
          "sharp focus on ONE clear subject, uncluttered composition with empty space on the left third for big text. "
          "ABSOLUTELY NO text, letters, numbers, captions, logos, brand badges, watermarks or signatures anywhere. "
          "No real identifiable person's face. Scene: ")


def gera(cena, saida, modelo="gemini-2.5-flash-image", formato="16:9", tentativas=4):
    k = CHAVE.read_text("utf-8").strip()
    corpo = {"contents": [{"parts": [{"text": REGRAS + cena}]}],
             "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": formato}}}
    for i in range(tentativas):
        req = urllib.request.Request(BASE.format(m=modelo), data=json.dumps(corpo).encode("utf-8"),
                                     headers={"x-goog-api-key": k, "Content-Type": "application/json"})
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code == 429 and i < tentativas - 1:
                espera = 20 * (i + 1)
                print(f"[gemini] 429 (cota) — esperando {espera} s", flush=True)
                time.sleep(espera)
                continue
            raise SystemExit(f"[gemini] ERRO {e.code}: {msg[:500]}")
        for c in d.get("candidates", []):
            for p in c.get("content", {}).get("parts", []):
                dado = p.get("inlineData") or p.get("inline_data")
                if dado and dado.get("data"):
                    Path(saida).parent.mkdir(parents=True, exist_ok=True)
                    Path(saida).write_bytes(base64.b64decode(dado["data"]))
                    return Path(saida)
        raise SystemExit(f"[gemini] sem imagem na resposta: {json.dumps(d)[:400]}")


if __name__ == "__main__":
    a = sys.argv[1:]
    op = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    if "--teste" in a:
        t0 = time.time()
        f = gera("an empty Polish car dealership lot at dusk full of unsold electric cars, rain on the asphalt",
                 Path(__file__).resolve().parent.parent / "data" / "_teste_gemini.png", op("--modelo", "gemini-2.5-flash-image"))
        print(f"[gemini] ok em {time.time() - t0:.0f} s -> {f} ({f.stat().st_size // 1024} KB)")
    elif len(a) >= 2:
        n = int(op("--n", 1))
        saida = Path(a[1])
        for i in range(n):
            alvo = saida if n == 1 else saida.with_name(f"{saida.stem}_{i + 1}{saida.suffix}")
            gera(a[0], alvo, op("--modelo", "gemini-2.5-flash-image"), op("--formato", "16:9"))
            print(f"[gemini] {alvo}")
    else:
        sys.exit(__doc__)
