"""Miniaturas "Every Job on a Carrier Flight Deck Ranked" (en, 20/10). Todo número é dito: number ten, 134 sailors,
165 mph em ~2 s (catapulta), 150 mph (controlled crash). Fotos Wikimedia Commons (US Navy, domínio público)."""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from make_thumb_solda import make  # noqa: E402

QA = ROOT / "qa" / "thumbs_jobs"
QA.mkdir(parents=True, exist_ok=True)
POOL = json.loads((ROOT / "data" / "photo_pool.json").read_text("utf-8"))
NB = " "


def foto(titulo):
    f = POOL[titulo].get("file")
    p = Path(f) if f else None
    if not p or not p.exists():
        raise SystemExit(f"[thumb] sem arquivo: {titulo}")
    return p


SPECS = [
    {"name": "jobs_10", "src": foto('File:USS Gerald R Ford supports Operation Epic Fury (9542706).jpg'), "num": "10" + NB + "JOBS", "word": "SAFEST TO DEADLIEST", "size": 250},
    {"name": "jobs_red", "src": foto("File:Fighting fires from Forrestal's flight deck (USN 1126632).jpg"), "num": "RED", "word": "THE DEADLIEST JOB", "size": 280},
    {"name": "jobs_134", "src": foto('File:USS Rupertus (DD-851) stands by to assist the burning USS Forrestal (CVA-59), 29 July 1967 (USN 1124775).jpg'), "num": "134", "word": "SAILORS KILLED IN ONE FIRE", "size": 280},
    {"name": "jobs_165", "src": foto('File:US Navy 050413-N-8704K-001 A catapult shooter signals the launch of an F-14D Tomcat.jpg'), "num": "165" + NB + "MPH", "word": "IN 2 SECONDS", "size": 250},
    {"name": "jobs_150", "src": foto('File:US Navy 070127-N-7780S-038 A flight deck director aboard the Nimitz-class aircraft carrier USS John C. Stennis (CVN 74) directs an EA-6B Prowler to the catapult to be launched from the flight deck.jpg'), "num": "150" + NB + "MPH", "word": "A CONTROLLED CRASH", "size": 250},
]


def main():
    for s in SPECS:
        make(s)
    outs = [ROOT / "out" / "thumbnails" / f"{s['name']}.jpg" for s in SPECS]
    folha = Image.new("RGB", (640 + 24 + 210, len(outs) * 372), (16, 18, 22))
    for i, p in enumerate(outs):
        im = Image.open(p).convert("RGB")
        folha.paste(im.resize((640, 360), Image.LANCZOS), (0, i * 372))
        folha.paste(im.resize((210, 118), Image.LANCZOS), (664, i * 372))
    folha.save(QA / "review.jpg", quality=90)
    print("->", QA / "review.jpg")


if __name__ == "__main__":
    main()
