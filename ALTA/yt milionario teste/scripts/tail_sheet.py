"""Confere o FIM de clipes do YouTube recortados perto do final do vídeo de origem (cartão final,
"thanks for watching", inscreva-se). 3 quadros por clipe: 40%, 75% e último segundo.
Uso: python tail_sheet.py qa/decisions/yt_tail_clips.json qa/tail.jpg"""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ids = json.loads(Path(sys.argv[1]).read_text("utf-8"))
clips = {c["id"]: c for c in json.loads((ROOT / "data/clips.json").read_text("utf-8"))["clips"]}
TW, TH = 480, 270
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
sheet = Image.new("RGB", (TW * 3, (TH + 24) * len(ids)), (18, 18, 18))
dr = ImageDraw.Draw(sheet)
with tempfile.TemporaryDirectory() as td:
    for r, cid in enumerate(ids):
        c = clips[cid]
        src = ROOT / "public" / c["file"]
        dur = c["dur"] / 30
        y = r * (TH + 24)
        dr.text((4, y + 3), f"{cid} {c.get('channel')} {c.get('source')}", fill=(255, 220, 0), font=font)
        for k, t in enumerate((dur * 0.4, dur * 0.75, max(0, dur - 0.5))):
            out = Path(td) / f"{cid}_{k}.jpg"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src),
                            "-frames:v", "1", "-vf", f"scale={TW}:{TH},format=yuvj420p", "-strict", "unofficial", str(out)])
            if out.exists():
                sheet.paste(Image.open(out), (k * TW, y + 24))
sheet.save(sys.argv[2], quality=80)
print("[tail]", sys.argv[2], len(ids))
