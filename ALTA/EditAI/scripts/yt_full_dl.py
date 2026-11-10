"""Baixa vídeos INTEIROS do YouTube (só vídeo, sem áudio) para input/youtube/ID__Canal.mp4 — 1 extração por vídeo,
respeitando a cota compartilhada (yt_quota). Depois disso tudo roda local (local_yt/probe_local/make_clips), sem
gastar cota por janela. Seletor ESTRITO: 1080p (avc1 primeiro); 720p só entra marcado como sub1080.
Uso: python yt_full_dl.py lista.txt   (uma linha por vídeo: ID  prioridade  comentário)"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_quota

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "input" / "youtube"
INFO = ROOT / "data" / "yt_info"
FMT = ("bestvideo[height=1080][vcodec^=avc1][ext=mp4]/bestvideo[height=1080][ext=mp4]/bestvideo[height=1080]/"
       "bestvideo[height>1080][height<=1440][ext=mp4]/bestvideo[height>1080][height<=2160]/"
       "bestvideo[height=720][vcodec^=avc1][ext=mp4]/bestvideo[height=720]")


# --arquivo: imagem de ÉPOCA/amadora do próprio assunto (ex.: o Seawise Giant real só existe em 360–480p). Exceção
# documentada no decisions_log; esses clipes entram marcados como era "old" e em poucos cortes.
FMT_ARQ = "bestvideo[height>=360][height<=1080][ext=mp4]/bestvideo[height>=360][height<=1080]/best[height>=360][height<=1080]"


def main():
    OUT.mkdir(parents=True, exist_ok=True); INFO.mkdir(parents=True, exist_ok=True)
    ids = [l.split()[0] for l in Path(sys.argv[1]).read_text("utf-8").splitlines() if l.strip() and not l.startswith("#")]
    for n, vid in enumerate(ids, 1):
        arq = "--arquivo" in sys.argv
        if arq:
            (INFO / f"{vid}.fail").unlink(missing_ok=True)
        if list(OUT.glob(f"{vid}__*")) or (INFO / f"{vid}.fail").exists():
            print(f"[{n}/{len(ids)}] {vid} já feito", flush=True); continue
        yt_quota.acquire(vid)
        cmd = yt_quota.ytdlp("--no-playlist", "--no-progress", "-f", FMT_ARQ if arq else FMT, "--max-filesize", "2500M",
                             "-o", str(OUT / "%(id)s__%(channel)s.%(ext)s"), "--restrict-filenames",
                             "--write-info-json", "--no-write-comments",
                             "--print", "after_move:[ok] %(id)s %(height)sp %(vcodec)s %(duration)ss %(title)s",
                             f"https://www.youtube.com/watch?v={vid}")
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = r.stdout + r.stderr
        try:
            yt_quota.report(out)
        except yt_quota.Blocked as e:
            print(f"[PARADO] {e}", flush=True); return
        for j in OUT.glob(f"{vid}__*.info.json"):
            j.replace(INFO / f"{vid}.info.json")
        ok = [l for l in r.stdout.splitlines() if l.startswith("[ok]")]
        if ok:
            print(f"[{n}/{len(ids)}] {ok[-1]}", flush=True)
        else:
            (INFO / f"{vid}.fail").write_text(out[-1500:], "utf-8")
            print(f"[{n}/{len(ids)}] {vid} FALHOU: {out.strip().splitlines()[-1][:200] if out.strip() else '?'}", flush=True)
    print("[FIM]", yt_quota.status(), flush=True)


if __name__ == "__main__":
    main()
