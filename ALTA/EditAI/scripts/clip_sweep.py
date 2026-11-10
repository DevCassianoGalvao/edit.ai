"""Varredura de clipes corrompidos em public/stock: duração do arquivo vs clips.json e teste de decodificação
(quadros contados). Clipe ruim -> data/window_rejects.json (sai da biblioteca) e é apagado.
Uso: python clip_sweep.py"""
import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
lib = json.loads((D / "clips.json").read_text("utf-8"))
rej_p = D / "window_rejects.json"
rej = json.loads(rej_p.read_text("utf-8")) if rej_p.exists() else []
ruins = []
for c in lib["clips"]:
    if c.get("kind") != "video":
        continue
    f = ROOT / "public" / c["file"]
    if not f.exists():
        ruins.append((c["id"], "arquivo ausente")); continue
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=nb_read_frames,width,height,pix_fmt", "-of", "json", str(f)], capture_output=True, text=True)
    st = (json.loads(r.stdout or "{}").get("streams") or [{}])[0]
    n = int(st.get("nb_read_frames") or 0)
    if (st.get("width"), st.get("height")) != (1920, 1080) or st.get("pix_fmt") != "yuv420p" or n < c["dur"]:
        ruins.append((c["id"], f"{st.get('width')}x{st.get('height')} {st.get('pix_fmt')} {n} quadros (precisa {c['dur']})"))
for cid, why in ruins:
    print("[sweep] RUIM", cid, why)
    if cid not in rej:
        rej.append(cid)
rej_p.write_text(json.dumps(rej, indent=1), "utf-8")
print(f"[sweep] {len(ruins)} ruins de {sum(1 for c in lib['clips'] if c.get('kind') == 'video')} vídeos -> window_rejects.json")
