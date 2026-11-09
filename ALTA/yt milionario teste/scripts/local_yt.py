"""Vídeos do YouTube baixados À MÃO pelo usuário em input/youtube/ (YouTube bloqueado para o yt-dlp).
Nomes aceitos:
  - ID.mp4 ou ID__Canal.mp4
  - "Título - Canal (1080p, h264, youtube).mp4" (padrão do baixador do usuário) -> casado com data/yt_pool.json
    por canal + título normalizado (só letras/dígitos; o baixador troca "/" e ":" por "_")."""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_YT = ROOT / "input" / "youtube"
EXTS = (".mp4", ".mkv", ".webm", ".mov")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def local_files():
    return sorted(p for p in LOCAL_YT.glob("*") if p.suffix.lower() in EXTS)


def _pool():
    p = ROOT / "data" / "yt_pool.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def split_name(p, pool=None):
    """-> (id ou None, canal ou None, título ou None)"""
    stem = p.stem
    vid, _, channel = stem.partition("__")
    if ID_RE.match(vid.strip()):
        return vid.strip(), channel.strip() or None, None
    m = re.match(r"^(.*) - (.+?)(?: \([^)]*youtube\))?$", stem)
    title, channel = (m.group(1), m.group(2)) if m else (stem, None)
    pool = _pool() if pool is None else pool
    nt, nc = norm(title), norm(channel)
    hits = [e for e in pool.values() if norm(e.get("channel")) == nc and nt and
            (norm(e.get("title")).startswith(nt) or nt.startswith(norm(e.get("title"))))]
    exact = [e for e in hits if norm(e.get("title")) == nt]  # "DSV Vinnice" é prefixo de outro título do mesmo canal
    if len(exact) == 1:
        return exact[0]["id"], channel, title
    if len(hits) == 1:
        return hits[0]["id"], channel, title
    # 16/09: o usuario baixou 25 videos ANTES de qualquer busca (cota cheia), entao nao ha pool para casar.
    # ID sintetico derivado do nome do arquivo: deterministico, mesmo formato de 11 caracteres, e o make_clips
    # reencontra o arquivo depois. Fica marcado como "manual" no pool (sem link do YouTube).
    return local_id(p), channel, title


def local_id(p):
    return "L" + hashlib.md5(p.stem.encode("utf-8")).hexdigest()[:10]


def local_yt(vid):
    pool = _pool()
    for p in local_files():
        if split_name(p, pool)[0] == vid:
            return str(p)
    return None
