"""Resumo rápido da timeline: janelas das animações, cues encontrados e estatística dos cortes."""
import json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / "data/timeline.json").read_text("utf-8"))["items"]
for it in items:
    if it["type"] == "animation":
        print(f"{it['scene']:13s} {it['from'] / 30:7.1f}s dur {it['dur'] / 30:5.1f}s cues {it.get('cues')}")
cuts = [i for i in items if i["type"] == "cut"]
d = [c["dur"] / 30 for c in cuts]
print(f"cortes {len(cuts)} | média {statistics.mean(d):.2f}s | min {min(d):.2f}s | max {max(d):.2f}s | <3s: {sum(x < 3 for x in d)}")
