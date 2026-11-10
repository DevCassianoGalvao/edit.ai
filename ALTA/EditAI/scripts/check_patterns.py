"""Testa cada padrão de regra contra strings que ele PRECISA casar e que NÃO PODE casar.
Tem que terminar com 0 problemas (inclui auditoria de chr(8) nos próprios padrões).
"""
import importlib.util, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, S / f"{name}.py")
    src = (S / f"{name}.py").read_text("utf-8")
    # carrega só as definições de padrão (sem executar main/efeitos)
    ns = {"re": re, "__name__": "patterns", "B": chr(92) + "b", "D": chr(92) + "d"}  # B: padroes montados sem escrever a barra junto do b
    for m in re.finditer(r"^([A-Z_]+) = re\.compile\((.*?), re\.I\)$", src, re.S | re.M):
        try:
            exec(f"{m.group(1)} = re.compile({m.group(2)}, re.I)", ns)
        except (NameError, SyntaxError):
            pass  # padrão montado a partir de dados (ex.: FOREIGN usa beats.json) — não é testado aqui
    return ns


problems = []
CASES = {
    ("fetch_video", "BAN_TITLE"): (
        ["DCS F/A-18 Carrier Landing", "Aircraft Carrier Survival Gameplay", "How The US Navy Feeds 5000", "Top 10 carriers",
         "Battlefield 6 carrier", "sailors HD Stock Footage", "WWII carrier footage", "Tunnel Boring Machine 3D animation"],
        ["USS Gerald R. Ford (CVN 78) Flight Deck B-Roll", "Night Flight Operations USS Gerald R. Ford", "B-Roll Boat Footage CVN 72",
         "USS Gerald R. Ford Helo Ops", "ICON 3D printed homes printing", "3D-printed house construction timelapse"]),
    ("fetch_video", "BAN_CHANNEL"): (
        ["CriticalPast", "Business Insider", "WAVY TV 10", "13News Now", "USA Military Channel", "airailimages", "AiTelly",
         "Fluctus", "HGA Gaming", "US Military Archive", "Fortress X", "US Aviation", "Ultimate Military Channel"],
        ["U.S. Navy", "U.S. Fleet Forces Command", "Gung Ho Vids", "AIRBOYD", "Sky Eagles", "AiirSource Military", "HII", "Alex Bowman",
         "Will Clark TV", "MiliSource", "Defense & Aerospace Report", "Dave Windell", "m171562"]),
    ("commons_vidcats", "NC_ND"): (
        ["CC BY-NC 4.0", "CC BY-ND 2.0", "CC BY-NC-SA 3.0", "Non-commercial use only"],
        ["CC BY-SA 4.0", "CC BY 2.0", "Public domain", "CC0"]),
    ("commons_vidcats", "OK_LIC"): (
        ["Public domain", "CC BY-SA 4.0", "CC BY 3.0", "CC0", "PD-USGov-Military-Navy"],
        ["All rights reserved", "Fair use", "GFDL"]),
    ("select_probe", "BAD"): (  # tema Mar de Bering / caranguejo
        ["Top 10 deadliest jobs", "crab fishing explained", "Deadliest Catch full episode", "crab boat reaction",
         "Bering Sea podcast interview", "#shorts crab", "Hearing into the loss of the Destination"],
        ["Setting Pots Alaska King Crab Fishery 2017 on F/V Bering Star", "Bering Sea Storm", "Offloading opelio crab in Dutch Harbor",
         "Coast Guard aircrew challenges in Alaska", "Immersion Suit Donning and Water Entry Sequence"]),
    ("select_probe", "SUBJ"): (
        ["Bering Sea crab fishing", "Hauling Pots Alaska King Crab", "Dutch Harbor unloading", "Coast Guard rescue swimmer Kodiak",
         "immersion suit cold water", "Scandies Rose survivor", "freezing spray icing vessel", "NOAA trawl survey snow crab", "St Paul harbor ice"],
        ["underwater welding", "Dead Sea drone 4k", "deep sea anglerfish", "nuclear icebreaker Arktika", "salt crystal timelapse"]),
    ("select_probe", "PLACE_BAN"): (
        ["Deadliest Catch's Roughest Waters | Discovery", "crab fishing game gameplay", "AI generated Bering Sea", "king crab recipe cooking",
         "Ketchikan crab fisherman's tour cruise excursion", "Maine lobster boat", "GIANT ALASKAN KING CRAB eating mukbang"],
        ["Setting Pots Alaska King Crab Fishery 2017 on F/V Bering Star", "Bering Sea Storm", "Coast Guard aircrew challenges in Alaska"]),
}
cache = {}
for (mod, name), (must, mustnot) in CASES.items():
    ns = cache.setdefault(mod, load(mod))
    pat = ns.get(name)
    if pat is None:
        problems.append(f"{mod}.{name}: padrão não encontrado"); continue
    if "\x08" in pat.pattern:
        problems.append(f"{mod}.{name}: contém chr(8) (\\b virou backspace)")
    for s in must:
        if not pat.search(s):
            problems.append(f"{mod}.{name} NÃO casou (devia): {s!r}")
    for s in mustnot:
        if pat.search(s):
            problems.append(f"{mod}.{name} casou (não devia): {s!r} -> {pat.search(s).group(0)!r}")

for f in S.rglob("*.py"):
    if "\x08" in f.read_text("utf-8", errors="replace"):
        problems.append(f"chr(8) em {f.name}")
print(f"check_patterns: {len(problems)} problemas")
for p in problems:
    print("  -", p)
sys.exit(1 if problems else 0)
