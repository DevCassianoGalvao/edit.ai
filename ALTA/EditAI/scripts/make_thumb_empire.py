"""Five thumbnails for "Inside the Empire Builder — Surviving a Polar Vortex" (en). Every number is spoken:
minus 50 degrees; 2,200 miles; minus 70 at Rogers Pass; a 100-degree fall at Browning; minus 40 stranded.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

P = ROOT / "assets" / "photos"
B = ROOT / "assets" / "banco"
QA = ROOT / "qa" / "thumbs_empire"
QA.mkdir(parents=True, exist_ok=True)

SPECS = [
    {"name": "eb_minus50", "src": P / "Amtrak_s_Eastbound_Empire_Builder_crosses_the_bridge_marking_the_park_boundary_on_US-2_550_bf6902.jpg", "num": "-50°", "word": "NEVER STOP", "size": 260},
    {"name": "eb_2200", "src": P / "Fargo_Empire_Builder_4c5797.jpg", "num": "2,200 MILES", "word": "OF ICE", "size": 215},
    {"name": "eb_minus70", "src": P / "Hille_Winter_View_53437973569__9def36.jpg", "num": "-70°F", "word": "MONTANA", "size": 250},
    {"name": "eb_100deg", "src": P / "Wolf_Point_Montana_Depot_12e8b2.jpg", "num": "100°", "word": "IN 24 HOURS", "size": 240},
    {"name": "eb_minus40", "src": P / "Empire_Builder_at_West_Glacier_station_55087339376__594993.jpg", "num": "-40°", "word": "STRANDED", "size": 260},
]


def main():
    outs = [make(s) for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
