"""Baixa de novo, em fila, as entradas de data/photo_pool.json que ficaram sem arquivo (429/timeout na colheita).
Uso: python photo_retry.py"""
import json, os, re, time, requests
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "data" / "photo_pool.json"
pool = json.loads(P.read_text("utf-8"))
S = requests.Session(); S.headers["User-Agent"] = "abismo-pipeline/1.0 (seu-email@exemplo.com)"
OUT = ROOT / "assets" / "photos"; OUT.mkdir(parents=True, exist_ok=True)
n_ok = 0
for t, v in pool.items():
    if v.get("file") and os.path.exists(v["file"]):
        continue
    if t.lower().endswith((".tif", ".tiff", ".svg", ".pdf")):
        continue
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", t[5:])[:120]
    if not name.lower().endswith((".jpg", ".jpeg", ".png")):
        name += ".jpg"
    dst = OUT / name
    for k in range(3):
        try:
            r = S.get(v["url"], timeout=120)
            if r.status_code == 429:
                time.sleep(20 * (k + 1)); continue
            if r.ok and len(r.content) > 20000:
                dst.write_bytes(r.content); v["file"] = str(dst); n_ok += 1
                print("[retry] ok", t[5:70], flush=True)
                break
        except Exception as ex:
            print("[retry] erro", t[5:60], ex, flush=True); time.sleep(5)
    time.sleep(1.5)
P.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
print(f"[retry] {n_ok} baixadas")
