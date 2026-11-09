"""
Checagem de relevância LOCAL com CLIP — grátis, offline, sem cota nenhuma.

Ativar com  VISION_CHECK=clip  no .env.

Roda o CLIP (ViT-B/32) via onnxruntime na CPU: ~130 ms por foto. Julga se a
imagem combina com o que o segmento precisa mostrar, comparando o embedding da
imagem com o do texto e com um conjunto de "negativos" (foto genérica, cena
moderna, maquete, mapa, print de videogame). Modelo (~600 MB) baixa uma vez do
Hugging Face e fica em cache.

Não é tão esperto quanto um LLM (não sabe "nação errada"), mas é excelente no
"essa imagem é sobre X ou não" — que é 90% do trabalho.
"""
from __future__ import annotations

import io
import math
import sys

import numpy as np

_REPO = "Xenova/clip-vit-base-patch32"
_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
_STD = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)
_NEG = [
    "an unrelated stock photo",
    "a modern everyday civilian scene",
    "a museum display case with a plaque",
    "a scanned map, chart, diagram or document",
    "a toy, scale model or diorama",
    "a screenshot from a video game",
    "a logo, emblem, flag, stamp or coin",
    "a painting, drawing or illustration",
    "a building, house or piece of architecture",
    "an empty landscape or nature scene with no people or vehicles",
    "a formal studio portrait of a person",
    "a fairground ride, carriage or bicycle",
    "an aircraft, airship or spacecraft",
]

_S: dict = {}


def _load():
    if "vis" in _S:
        return _S["vis"]
    try:
        import onnxruntime as ort
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer

        so = ort.SessionOptions()
        so.log_severity_level = 3
        _S["vis"] = ort.InferenceSession(
            hf_hub_download(_REPO, "onnx/vision_model.onnx"), so, providers=["CPUExecutionProvider"])
        _S["txt"] = ort.InferenceSession(
            hf_hub_download(_REPO, "onnx/text_model.onnx"), so, providers=["CPUExecutionProvider"])
        _S["tok"] = Tokenizer.from_file(hf_hub_download(_REPO, "tokenizer.json"))
        _S["tc"] = {}
        _S["negs"] = np.stack([_emb_txt(n) for n in _NEG])
    except Exception as e:
        print(f"[clip] indisponível ({e!r}). Instale:  pip install onnxruntime huggingface_hub tokenizers",
              file=sys.stderr)
        _S["vis"] = None
    return _S["vis"]


def available() -> bool:
    return _load() is not None


def _emb_txt(s: str) -> np.ndarray:
    cache = _S.setdefault("tc", {})
    if s in cache:
        return cache[s]
    ids = _S["tok"].encode(s).ids[:77]
    ids = ids + [0] * (77 - len(ids))
    o = _S["txt"].run(None, {"input_ids": np.array([ids], dtype=np.int64)})[0][0]
    v = (o / (np.linalg.norm(o) + 1e-8)).astype(np.float32)
    cache[s] = v
    return v


def _emb_img(data: bytes) -> np.ndarray:
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB").resize((224, 224), Image.BICUBIC)
    a = ((np.asarray(im, dtype=np.float32) / 255.0) - _MEAN) / _STD
    o = _S["vis"].run(None, {"pixel_values": a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    return (o / (np.linalg.norm(o) + 1e-8)).astype(np.float32)


def relevant(image_bytes: bytes, must_show: str, strict: bool = False) -> bool:
    """True se a imagem parece pertencer ao segmento.

    CLIP não conhece nomes obscuros ("EE-9 Cascavel"), então pra assunto de
    nicho ele erra fácil. Dois testes têm que passar ao mesmo tempo:
      1. similaridade ABSOLUTA com o texto acima de um piso;
      2. o texto tem que ganhar dos negativos por uma MARGEM (não empatar).
    Com isso ele deixa de aceitar "vítima do V-2 1944" ou "pintura do Papai Noel"
    só porque são "fotos antigas". Erra pro lado de recusar — melhor um buraco
    (que o merge_gaps preenche) do que uma imagem fora do tema.
    """
    if _load() is None or not image_bytes:
        return True
    try:
        v = _emb_img(image_bytes)
    except Exception:
        return True
    # must_show pode vir com várias frases de busca separadas por ";" — testa
    # cada uma e fica com a melhor (a imagem só precisa casar com UMA delas).
    frases = [f.strip() for f in str(must_show or "").replace("\n", ";").split(";") if f.strip()][:4]
    if not frases:
        frases = ["archival documentary photo"]
    pos = 0.0
    for f in frases:
        f = f[:180]
        pos = max(pos,
                  float(v @ _emb_txt(f"a photo of {f}")),
                  float(v @ _emb_txt(f"a documentary archive photo showing {f}")))
    best_neg = float(np.max(_S["negs"] @ v))
    piso = 0.235 if strict else 0.215        # similaridade mínima com o assunto
    margem = 0.045 if strict else 0.025      # tem que ganhar dos negativos
    return pos >= piso and pos >= best_neg + margem
