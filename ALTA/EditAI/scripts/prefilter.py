"""PRÉ-FILTRO automático das folhas de contato — CLIP + pHash + detector de texto na tela.

Não decide nada sozinho no lugar do olho: ele ORDENA e SEPARA, para a folha mostrar primeiro o que tem cara de
certo e para o que é lixo óbvio (quase-duplicata, legenda queimada) sair da frente. O julgamento continua sendo
feito na folha — só que numa pilha 3x menor.

  - CLIP (ViT-B/32 em onnxruntime, o mesmo do pipeline da pasta mapa): nota = quanto a foto combina com a BUSCA
    que a achou, menos o quanto ela combina com os negativos (miniatura, print de jogo, cartaz, salão de carros).
  - pHash (DCT 8x8): quase-duplicata vira "dup" e só a de maior resolução fica na folha.
  - texto na tela (só em QUADRO DE VÍDEO, ver tem_texto): prompts de legenda/tarja + detector morfológico —
    marca com TXT na folha de sondagem e na folha densa a ficha técnica e a legenda queimada que eu rejeitava
    à mão em todo filme. Em FOTO esse sinal não é usado: letreiro de rua dispara o detector.

Uso:
  python prefilter.py fotos                      -> data/photo_prefilter.json
  python prefilter.py quadros ARQ.jpg [ARQ2...]  -> imprime nota de texto por arquivo (calibração)
"""
import sys as _s, pathlib as _pl; _s.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import prioridade  # noqa: E401,F401  04/10: etapa leve em prioridade baixa
import io, json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
REPO = "Xenova/clip-vit-base-patch32"
MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)

NEG = [  # o que nunca deve ganhar da busca (mesma ideia do clipcheck.py da pasta mapa)
    "an unrelated stock photo",
    "a scale model, toy or diorama",
    "a screenshot from a video game",
    "a logo, emblem, flag or coin",
    "a drawing, painting or diagram",
    "a car show stand with crowd and studio lights",
    "a page of a book or a document",
]
TXT_POS = [  # texto QUEIMADO na imagem
    "a video frame with large subtitle text burned in",
    "a screenshot with white caption text over the image",
    "an image with a text banner or specification list on it",
    "a poster with big printed words",
]
TXT_NEG = [
    "a clean photograph with no text",
    "a documentary photo of a scene",
    "a photo of a vehicle on a street",
]
_S = {}


def _load():
    if "vis" in _S:
        return _S["vis"]
    try:
        import onnxruntime as ort
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer
        so = ort.SessionOptions()
        so.log_severity_level = 3
        _S["vis"] = ort.InferenceSession(hf_hub_download(REPO, "onnx/vision_model.onnx"), so,
                                         providers=["CPUExecutionProvider"])
        _S["txt"] = ort.InferenceSession(hf_hub_download(REPO, "onnx/text_model.onnx"), so,
                                         providers=["CPUExecutionProvider"])
        _S["tok"] = Tokenizer.from_file(hf_hub_download(REPO, "tokenizer.json"))
        _S["tc"] = {}
    except Exception as e:  # noqa: BLE001
        print(f"[prefiltro] CLIP indisponível ({e!r}) — a folha sai sem ordenação", file=sys.stderr)
        _S["vis"] = None
    return _S["vis"]


def disponivel():
    return _load() is not None


def emb_txt(s):
    c = _S.setdefault("tc", {})
    if s not in c:
        ids = _S["tok"].encode(s).ids[:77]
        ids = ids + [0] * (77 - len(ids))
        o = _S["txt"].run(None, {"input_ids": np.array([ids], dtype=np.int64)})[0][0]
        c[s] = (o / (np.linalg.norm(o) + 1e-8)).astype(np.float32)
    return c[s]


def emb_img(src):
    from PIL import Image
    im = (Image.open(io.BytesIO(src)) if isinstance(src, bytes) else Image.open(src)).convert("RGB")
    a = ((np.asarray(im.resize((224, 224), Image.BICUBIC), dtype=np.float32) / 255.0) - MEAN) / STD
    o = _S["vis"].run(None, {"pixel_values": a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    return (o / (np.linalg.norm(o) + 1e-8)).astype(np.float32)


def nota(v, busca):
    """Quanto a imagem combina com a busca, descontando os negativos (margem, não similaridade crua)."""
    pos = max(float(v @ emb_txt(f"a photo of {busca[:180]}")), float(v @ emb_txt(busca[:180])))
    neg = max(float(v @ emb_txt(n)) for n in NEG)
    return round(pos - neg, 4)


def nota_texto(v):
    """> 0 = tem cara de imagem com texto queimado (legenda, ficha técnica, tarja)."""
    return round(max(float(v @ emb_txt(p)) for p in TXT_POS) - max(float(v @ emb_txt(p)) for p in TXT_NEG), 4)


def _dct2(a):
    """DCT-II 2D sem scipy (matriz de cossenos 32x32 é barata e evita mais uma dependência)."""
    n = a.shape[0]
    k = np.arange(n)
    c = np.cos(np.pi * (2 * k[:, None] + 1) * k[None, :] / (2 * n)) * np.sqrt(2 / n)
    c[:, 0] /= np.sqrt(2)
    return c.T @ a @ c


def phash_np(path, hash_size=8):
    from PIL import Image
    a = np.asarray(Image.open(path).convert("L").resize((32, 32), Image.LANCZOS), dtype=np.float32)
    d = _dct2(a)[:hash_size, :hash_size]
    bits = (d > np.median(d.flatten()[1:])).flatten()
    return int("".join("1" if b else "0" for b in bits), 2)


def dist(a, b):
    return bin(a ^ b).count("1")


def texto_morf(path, W=960):
    """Texto QUEIMADO sem OCR: banda horizontal com muitas transições de borda forte (as hastes das letras).
    Calibrado contra legenda/ficha técnica/marca d'água desenhadas em foto limpa: legenda e ficha dão 0,10-0,19;
    foto limpa dá 0 (grade de locomotiva e vitrine cheia de reflexo são os falsos positivos conhecidos)."""
    from PIL import Image
    im = Image.open(path).convert("L")
    im = im.resize((W, max(1, round(im.height * W / im.width))), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32)
    b = np.abs(np.diff(a, axis=1)) > max(28.0, float(np.percentile(np.abs(np.diff(a, axis=1)), 97)))
    dens = b.mean(axis=1)
    linhas = dens > max(0.055, 3.5 * (float(np.median(dens)) + 1e-6))
    bandas, ini, melhor = [], None, 0.0
    for i, v in enumerate(linhas):
        if v and ini is None:
            ini = i
        if (not v or i == len(linhas) - 1) and ini is not None:
            if 4 <= i - ini <= 90:
                bandas.append((ini, i))
            ini = None
    for i0, i1 in bandas:
        faixa = b[i0:i1 + 1]
        tpl = (np.diff(faixa.astype(np.int8), axis=1) != 0).sum(axis=1).mean() / faixa.shape[1]
        melhor = max(melhor, float(tpl * min(1.0, faixa.any(axis=0).mean() / 0.25)))
    return round(melhor, 4)


def tem_texto(path, v=None):
    """AVISO de texto queimado em QUADRO DE VÍDEO (legenda, ficha técnica, tarja de canal).

    Calibrado em legendas/fichas/marcas desenhadas sobre foto limpa: pega ficha técnica (3/3), legenda (2/3) e
    marca d'água grande (2/3), sem marcar quadro limpo (3/3). É um aviso na folha, não rejeição automática — o
    olho continua decidindo, e o que ele deixa passar eu ainda pego na folha densa.

    NÃO serve para FOTO de cena urbana: placa de loja, letreiro e vitrine disparam o detector morfológico
    (a foto da Avenida Paulista sem legenda nenhuma marcou 0,173, mais que a mesma foto com legenda queimada).
    Por isso o pré-filtro das fotos não usa este sinal — lá quem cuida de cartaz/documento é o negativo do CLIP.
    """
    morf = texto_morf(path)
    clip = nota_texto(v if v is not None else emb_img(path)) if disponivel() else 0.0
    return ((morf > 0.10 and clip > 0.015) or clip > 0.045), morf, clip


def imagem_de(e):
    """24/09/2026: a miniatura de 500 px (photo_dl --miniaturas) basta — o CLIP reduz para 224 e o pHash para 32.
    Sem miniatura, usa a foto cheia (fluxo antigo)."""
    for k in ("thumb_file", "file"):
        if e.get(k) and Path(e[k]).exists():
            return e[k]
    return None


def fotos():
    pool = json.loads((D / "photo_pool.json").read_text("utf-8"))
    itens = [(t, e) for t, e in pool.items() if imagem_de(e)]
    # 24/09/2026: nota já calculada é reaproveitada (rodar de novo depois de uma busca extra só avalia as novas)
    velho = json.loads((D / "photo_prefilter.json").read_text("utf-8")) if (D / "photo_prefilter.json").exists() else {}
    out = {t: {k: v for k, v in r.items() if k != "dup"} for t, r in velho.items()
           if t in pool and r.get("tag") == pool[t]["tags"][0] and r.get("nota", -1) != -1}
    itens = [(t, e) for t, e in itens if t not in out]
    print(f"[prefiltro] {len(itens)} fotos novas ({len(out)} já avaliadas)", flush=True)
    if not disponivel():
        return

    def uma(par):
        t, e = par
        try:
            img = imagem_de(e)
            v = emb_img(img)
            return t, {"nota": nota(v, e.get("query") or e["tags"][0]),
                       "ph": phash_np(img), "tag": e["tags"][0]}
        except Exception as ex:  # noqa: BLE001
            return t, {"nota": -1, "ph": 0, "tag": e["tags"][0], "erro": repr(ex)[:80]}

    with ThreadPoolExecutor(4) as ex:
        for i, (t, r) in enumerate(ex.map(uma, itens), 1):
            out[t] = r
            if i % 200 == 0:
                print(f"[prefiltro] {i}/{len(itens)}", flush=True)
    # quase-duplicatas: dentro da mesma tag, a de MAIOR área fica; as outras viram dup
    por_tag = {}
    for t, r in out.items():
        por_tag.setdefault(r["tag"], []).append(t)
    for tag, ts in por_tag.items():
        ts.sort(key=lambda t: -(pool[t].get("width", 0) * pool[t].get("height", 0)))
        vistos = []
        for t in ts:
            h = out[t]["ph"]
            d = next((u for u, hu in vistos if dist(h, hu) <= 6), None)
            if d:
                out[t]["dup"] = d
            else:
                vistos.append((t, h))
    (D / "photo_prefilter.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), "utf-8")
    dups = sum(1 for r in out.values() if r.get("dup"))
    print(f"[prefiltro] {len(out)} avaliadas | {dups} quase-duplicatas (as maiores ficam) "
          f"-> data/photo_prefilter.json", flush=True)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "fotos":
        fotos()
    elif sys.argv[1] == "quadros":
        if not disponivel():
            return
        for p in sys.argv[2:]:
            flag, morf, clip = tem_texto(p)
            print(f"{Path(p).name:28s} texto={'SIM' if flag else 'nao':4s} morf {morf:.4f}  clip {clip:+.4f}")


if __name__ == "__main__":
    from trava import media   # 07/10/2026: render exclusivo (ver trava.py)
    with media("prefilter"):
        main()
