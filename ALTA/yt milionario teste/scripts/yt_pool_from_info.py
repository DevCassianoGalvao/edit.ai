"""data/yt_info/ID.info.json (gravado pelo yt_full_dl.py) -> data/yt_pool.json (id, title, channel, duration, url, height).
Mescla com o disco."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
p = D / "yt_pool.json"
pool = json.loads(p.read_text("utf-8")) if p.exists() else {}
for f in sorted((D / "yt_info").glob("*.info.json")):
    j = json.loads(f.read_text("utf-8"))
    pool[j["id"]] = {"id": j["id"], "title": j.get("title"), "channel": j.get("channel") or j.get("uploader"),
                     "duration": j.get("duration"), "url": f"https://www.youtube.com/watch?v={j['id']}",
                     "height": j.get("height"), "vcodec": j.get("vcodec"), "license": j.get("license"),
                     "upload_date": j.get("upload_date")}
p.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
print(f"[yt_pool] {len(pool)} vídeos")
