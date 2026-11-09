"""Baixa SÓ o trecho [start, start+dur] de um vídeo do YouTube por faixa de bytes.

Não usa --download-sections (estrangulado a 10-30 KB/s). Lê o índice `sidx` do
MP4 fragmentado (formato DASH só-vídeo), baixa init + os fragmentos que cobrem a
janela em pedaços de <=9 MB, e recorta/normaliza com ffmpeg:
  - corta 12% da borda (marca de canal) mantendo 16:9, escala para 1920x1080
  - 30 fps, sem áudio, H.264 CRF 18
Uso: python slice_dl.py VIDEO_ID START DUR OUT.mp4 [--nocrop]
"""
import json, struct, subprocess, sys, tempfile, time
from pathlib import Path
import requests

CHUNK = 9 * 1024 * 1024
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0 Safari/537.36"


CACHE = Path(__file__).resolve().parent.parent / "data" / "yt_fmt_cache"


def _extract(vid):
    """1 extração por VÍDEO (não por janela): o JSON fica em cache enquanto as URLs do googlevideo valem."""
    from urllib.parse import parse_qs, urlparse
    import yt_quota
    cp = CACHE / f"{vid}.json"
    if cp.exists():
        j = json.loads(cp.read_text("utf-8"))
        exp = min((int(parse_qs(urlparse(f["url"]).query).get("expire", ["0"])[0])
                   for f in j["formats"] if f.get("url")), default=0)
        if exp - time.time() > 900:
            return j
    yt_quota.acquire(f"slice_dl {vid}")
    p = subprocess.run(yt_quota.ytdlp("-j", "--no-warnings", "--no-playlist", f"https://www.youtube.com/watch?v={vid}"),
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
    yt_quota.report(p.stderr)
    j = json.loads(p.stdout)
    keep = ("id", "title", "channel", "channel_url", "webpage_url", "duration")
    j = {**{k: j.get(k) for k in keep}, "formats": [f for f in j["formats"] if f.get("protocol") == "https"]}
    CACHE.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(j), "utf-8")
    return j


def pick_format(vid):
    j = _extract(vid)
    fmts = [f for f in j["formats"] if f.get("vcodec") not in (None, "none") and f.get("acodec") in (None, "none")
            and f.get("ext") == "mp4" and f.get("protocol") == "https" and (f.get("height") or 0) >= 1080]
    if not fmts:
        raise RuntimeError("sem formato mp4 >=1080p")
    # 1080p primeiro (menor), avc1 antes de av01; 4K só se não houver 1080
    fmts.sort(key=lambda f: (abs((f.get("height") or 0) - 1080) > 0, "avc1" not in (f.get("vcodec") or ""),
                             f.get("height") or 0))
    return j, fmts[0]


def get(url, headers, a, b):
    r = requests.get(url, headers={**headers, "Range": f"bytes={a}-{b}"}, timeout=60)
    r.raise_for_status()
    return r.content


def boxes(buf, off=0):
    while off + 8 <= len(buf):
        size, typ = struct.unpack(">I4s", buf[off:off + 8])
        if size == 1:
            size = struct.unpack(">Q", buf[off + 8:off + 16])[0]
        yield typ.decode("latin1"), off, size
        if size == 0:
            return
        off += size


def parse_sidx(b):
    ver = b[8]
    p = 12 + 4  # header + reference_ID
    timescale = struct.unpack(">I", b[p:p + 4])[0]; p += 4
    if ver == 0:
        ept, first = struct.unpack(">II", b[p:p + 8]); p += 8
    else:
        ept, first = struct.unpack(">QQ", b[p:p + 16]); p += 16
    p += 2
    count = struct.unpack(">H", b[p:p + 2])[0]; p += 2
    refs = []
    for _ in range(count):
        a, dur, _sap = struct.unpack(">III", b[p:p + 12]); p += 12
        refs.append((a & 0x7FFFFFFF, dur))
    return timescale, ept, first, refs


def main():
    # 403 do googlevideo é intermitente (14/09: mesmas fontes alternam janela ok / 403): até 3 novas tentativas,
    # cada uma com extração fresca (a URL do cache pode ter vencido) e espera crescente
    for attempt in range(4):
        try:
            return run()
        except requests.HTTPError as ex:
            if ex.response is None or ex.response.status_code != 403 or attempt == 3:
                raise
            (CACHE / f"{sys.argv[1]}.json").unlink(missing_ok=True)
            time.sleep(15 * (attempt + 1))


def run():
    vid, start, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), Path(sys.argv[4])
    nocrop = "--nocrop" in sys.argv
    j, f = pick_format(vid)
    url, headers = f["url"], {"User-Agent": UA, **(f.get("http_headers") or {})}
    head = get(url, headers, 0, 256 * 1024 - 1)
    init_end, sidx = None, None
    for typ, off, size in boxes(head):
        if typ == "moov":
            init_end = off + size
        if typ == "sidx":
            if off + size > len(head):
                head = get(url, headers, 0, off + size - 1)
            sidx = (off, size, parse_sidx(head[off:off + size]))
            break
    if init_end is None or sidx is None:
        raise RuntimeError("sem moov/sidx")
    soff, ssize, (ts, ept, first, refs) = sidx
    pos, t = soff + ssize + first, ept / ts
    a = b = None
    seg_t0 = None
    for size, d in refs:
        t1 = t + d / ts
        if t1 > start and t < start + dur:
            if a is None:
                a, seg_t0 = pos, t
            b = pos + size - 1
        pos += size
        t = t1
    if a is None:
        raise RuntimeError("janela fora do vídeo")
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.mp4"
        with open(raw, "wb") as fh:
            fh.write(head[:init_end])
            x = a
            while x <= b:
                y = min(b, x + CHUNK - 1)
                fh.write(get(url, headers, x, y))
                x = y + 1
        vf = "fps=30"
        if not nocrop:
            vf = "crop=iw*0.76:ih*0.76,scale=1920:1080:flags=lanczos,setsar=1,fps=30"
        else:
            vf = "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,fps=30"
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start - seg_t0:.3f}", "-i", str(raw),
               "-t", f"{dur:.3f}", "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
    print(json.dumps({"id": vid, "channel": j.get("channel"), "channel_url": j.get("channel_url"),
                      "title": j.get("title"), "url": j.get("webpage_url"), "start": start, "dur": dur,
                      "src_height": f.get("height"), "out": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
