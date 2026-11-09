"""Tema do filme "Berliner Arbeiterfamilien vermieteten Betten stundenweise — warum verschwanden die Schlafgänger?" (de, 29/10/2026, baia b1,
painel 20261029-131224-berliner-arbeiterfamilien-vermieteten-be). Mietskasernen, Schlafgänger, Wohnungsuntersuchungen (Kohn), Ledigenheime, Weimar.
Tema NOVO (sem reuso): Commons (Zille, Berlin 1890-1910, Höfe, Karl-Marx-Hof, Hufeisensiedlung) + arquivo YouTube + Pexels de apoio."""
import json, re, shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent
S = R / "scripts"
D = R / "data"
BK = R / "_bak_tema_berlin"
BK.mkdir(exist_ok=True)
for n in ("beats.py", "build_plan.py", "fetch_images.py", "fetch_images_cat.py", "fetch_photos_api.py",
          "fetch_stock_api.py", "build_overlays.py"):
    if not (BK / n).exists():
        shutil.copy2(S / n, BK / n)

N = 117
s = (BK / "beats.py").read_text("utf-8")
j = s.find("\ndef _extra(i):")
HEAD = '''"""BEATS: "Berliner Arbeiterfamilien vermieteten Betten stundenweise" (de, 117 parágrafos, 40,9 min).
Modo PADRÃO, 20 % VÍDEO / 80 % FOTO, MODO ENXUTO. Pedido do PAINEL 20261029-131224-berliner-arbeiterfamilien-vermieteten-be (baia b1).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = None   # Berlin/Kaiserreich: banco só com tags escolhidas à mão
TAGS_LUGAR = []

TAGS = {
    "bed": "an old bed or bedstead, straw mattress, bedding, a bed in a small cramped room (historic or museum), people sleeping",
    "interior": "interior of a poor working-class room or flat around 1900 in Germany: crowded small room, beds, table, stove, cramped living (Zille, Kohn, Wohnungsuntersuchung)",
    "family": "a working-class family around 1900 in Germany: parents and children in a small room or courtyard, a mother with children, poor household",
    "kitchen": "a historic kitchen with a coal stove or tiled stove (Kachelofen), cooking pots, potatoes, a small tenement kitchen",
    "hinterhof": "a Berlin tenement courtyard (Hinterhof, Hof): narrow courtyard between tall building wings, laundry, children playing, rear building",
    "mietskaserne": "Berlin tenement block (Mietskaserne): tall plain 5-storey residential building facade, Gründerzeit rental housing, Front house and wings",
    "street": "Berlin street scene around 1890-1910: horse carts, passers-by, shop signs, Zille street photographs, market, crowd",
    "city_growth": "Berlin city panorama or skyline in the 19th/early 20th century, rooftops, chimneys, a fast-growing city, aerial or high viewpoint",
    "map": "an old map or city plan of Berlin (19th century), street plan, block layout, Hobrecht plan, district map",
    "hobrecht": "James Hobrecht, the Hobrecht plan, urban planner portrait or planning drawing of Berlin 1862, building blocks",
    "kaiserreich": "German Empire (Kaiserreich) 1871-1914: Kaiser Wilhelm, Berlin palace, imperial parade, Unter den Linden, Berlin as capital",
    "workers": "German industrial workers around 1900: factory hall, machine works (Borsig, AEG), workers leaving the factory, night shift, machinists",
    "stats": "old German documents, census forms, statistics tables, ledgers, handwritten lists, official records, Volkszählung",
    "reformer": "social reformers and scholars of the Kaiserreich: Paul Göhre, social democrats, pastors, medical officers, housing reform meeting, portraits",
    "ledigenheim": "Ledigenheim / Arbeiterwohnheim: Danckelmannstraße 46/47 Charlottenburg (1908), Volkshotel, single rooms of a workers' hostel, hostel facade",
    "doctor": "medicine and health around 1900: tuberculosis, sick children, rickets, hospital ward, doctor, sanatorium, health insurance",
    "wwi": "Germany in the First World War and 1918: home front, soldiers returning, hunger, revolution in Berlin, war end",
    "weimar": "Weimar Republic housing and city: Siedlung, Hufeisensiedlung, Bruno Taut, Karl-Marx-Hof, housing estates of the 1920s, modern flats",
    "housing": "new small flats with kitchen and bathroom: Siedlung, social housing blocks of the 1920s, garden city, apartment blocks with green courtyards",
    "sbahn": "Berlin S-Bahn and Stadtbahn history: station, viaduct, commuter trains of the 1920s, trams, city railway",
    "wien": "Vienna around 1900 and Red Vienna: Gemeindebau, Karl-Marx-Hof, Vienna streets, tenement houses of Vienna",
    "altbau": "Berlin Altbau today: renovated Gründerzeit apartment buildings, Prenzlauer Berg, Kreuzberg facade, courtyards after renewal, 1970s demolition and renewal",
    "student": "a student dormitory room or students in a hostel, a single small room with bed, desk and window (modern)",
    "money": "German Mark coins and banknotes of the Kaiserreich, paying rent, a wallet with coins, pennies and Groschen, household budget",
    "bank": "banks, mortgage and property finance: bank building, stock exchange, property speculation, building contractors, construction site of tenement houses",
    "stairs": "a narrow staircase or stairwell in an old tenement, corridor with doors, shared water tap and toilet on the landing",
    "basement": "basement dwellings and attic rooms: cellar flats, low windows, dark rooms under the roof, Dachboden, Keller",
    "pub": "a Kneipe / working-class pub or soup kitchen around 1900: men eating at long tables, beer hall, canteen, cheap meals",
    "women": "working women of the Kaiserreich: seamstress, washerwoman, maid, Näherin with sewing machine, women at work or in a boarding house",
    "parliament": "parliament and politics of the Kaiserreich: Reichstag, Prussian House of Representatives, town council, city hall (Rotes Rathaus), voting",
    "photographer": "an early photographer with a plate camera around 1900, glass plates, photographic survey of housing, documentary photographs of dwellings",
}

BANCO = {}

REJEITA_TITULO = [r"toy\\b|toys|lego|render|\\b3d\\b|game|poster|clipart|cartoon|model kit|diorama|miniatur|airsoft|costume|"
                  r"ukraine|syria|gaza|wikipedia loves|graffiti|vector|logo"]

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "movie still", "scale model", "diorama"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = [  # 117 parágrafos (master). p13/p25/p43/p50/p82/p98/p108 = pausas do alinhamento
"bed interior G", "street family", "city_growth workers", "kaiserreich street", "hobrecht map",
"hinterhof mietskaserne", "mietskaserne mietskaserne", "mietskaserne hinterhof", "hinterhof mietskaserne", "city_growth map",
"family interior", "reformer workers", "interior kitchen", "bed bed", "family money",
"bed interior", "interior bed", "workers street", "workers street", "stats city_growth",
"stats stats", "street workers", "family interior", "money stats", "reformer stats",
"bed interior", "interior family", "stairs hinterhof", "workers street", "bed interior",
"bed interior", "kitchen family", "pub street", "bed workers", "bed interior",
"reformer interior", "interior family", "doctor interior", "reformer street", "street kaiserreich",
"workers interior", "street workers", "family workers", "interior bed", "interior family",
"mietskaserne family", "stats stats", "reformer mietskaserne", "bank city_growth", "hobrecht hinterhof",
"hinterhof street", "money family", "money bed", "bed kitchen", "family interior",
"reformer family", "stairs street", "stats hinterhof", "workers city_growth", "workers street",
"bank mietskaserne", "mietskaserne bank", "bank stats", "street family", "family money",
"interior family", "women interior", "ledigenheim women", "hinterhof family", "basement hinterhof",
"kitchen interior", "reformer doctor", "mietskaserne city_growth", "doctor reformer", "parliament kaiserreich",
"hobrecht ledigenheim", "photographer interior", "photographer interior", "interior family", "doctor stats",
"parliament photographer", "photographer interior", "interior bed", "reformer workers", "ledigenheim ledigenheim",
"ledigenheim ledigenheim", "ledigenheim workers", "bank ledigenheim", "ledigenheim workers", "ledigenheim interior",
"ledigenheim city_growth", "ledigenheim city_growth", "street interior", "stats street", "reformer stats",
"housing mietskaserne", "kitchen housing", "wwi city_growth", "wwi street", "weimar housing",
"map city_growth", "housing weimar", "sbahn city_growth", "family workers", "wien wien",
"altbau mietskaserne", "ledigenheim student", "student ledigenheim", "student altbau", "stats city_growth",
"workers family", "bank mietskaserne", "photographer reformer", "family kitchen", "housing weimar",
"photographer housing", "bed bed F",
]
assert len(_PT) == 117, len(_PT)
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {37, 38, 39, 40, 41, 76, 77, 78, 79, 80, 81}
_REVEAL = set()
_ANIM = {2: "B01-Wachstum", 9: "B02-Dichte", 20: "B03-Schlafleute", 28: "B04-Karl", 52: "B05-Rechnung",
         77: "B06-Fotos", 85: "B07-Ledigenheim", 104: "B08-Wien"}
_CAP = {0: ("EIN BETT, DAS NIE KALT WIRD", "BERLIN · UM 1900"),
        4: ("DER HOBRECHT-PLAN", "BERLIN · 1862"),
        14: ("DIE SCHLAFGÄNGER", "BERLIN · 1880 – 1900"),
        26: ("EIN TAG IM HINTERHAUS", "BERLIN · KAISERREICH"),
        44: ("DIE RECHNUNG", "BERLIN · KLEINWOHNUNGSFRAGE"),
        60: ("GELD UND MAUERN", "BERLIN · DAS MIETSHAUS ALS ANLAGE"),
        76: ("DIE FOTOGRAFIEN", "BERLIN · 1902 – 1920"),
        83: ("DAS LEDIGENHEIM", "CHARLOTTENBURG · 1. APRIL 1908"),
        92: ("WAS VERSCHWAND", "BERLIN · 1914 – 1932"),
        109: ("DIE ANTWORT", "SCHLAFGÄNGER · EIN BETT")}
_SLATE = {}

'''
s2 = re.sub(r"range\(\d+\)", f"range({N})", s[j:])
(S / "beats.py").write_text(HEAD + s2, "utf-8")

TAGS_ALL = re.findall(r'^    "(\w+)": "', HEAD, re.M)
bp = S / "build_plan.py"
b = bp.read_text("utf-8")
b = re.sub(r'^FALLBACK_TAGS = .*$', 'FALLBACK_TAGS = ["street", "city_growth", "mietskaserne", "interior", "family"]', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_TAGS = .*$', 'INTERIOR_TAGS = {"interior", "bed", "kitchen", "stairs", "basement"}', b, count=1, flags=re.M)
b = re.sub(r'^INTERIOR_FALLBACK = .*$', 'INTERIOR_FALLBACK = ["interior", "bed"]', b, count=1, flags=re.M)
b = re.sub(r'^REGIONAL = .*$', 'REGIONAL = ["street", "mietskaserne", "hinterhof", "city_growth"]', b, count=1, flags=re.M)
b = re.sub(r'^PHOTO_RUN_TAGS = \{.*\}$', 'PHOTO_RUN_TAGS = {' + ", ".join(f'"{k}"' for k in TAGS_ALL) + '}', b, count=1, flags=re.M)
CUES = {"B01-Wachstum": ["500", "Millionen", "60"],
        "B02-Dichte": ["berlin", "Schöneberg", "Charlottenburg"],
        "B03-Schlafleute": ["72", "114", "84"],
        "B04-Karl": ["5", "6", "4"],
        "B05-Rechnung": ["2", "17"],
        "B06-Fotos": ["175", "112"],
        "B07-Ledigenheim": ["Charlottenburg", "370"],
        "B08-Wien": ["Berliner", "Wien"]}
(D / "_berlin_cues.json").write_text(json.dumps(CUES), "utf-8")
i = b.index("CUES = {")
k = b.index("\n}\n", i) + 3
b = b[:i] + "CUES = {  # UMA palavra por gatilho: algarismo casa exato, palavra por prefixo; \"a|b\" = alternativas\n" + "".join(
    f"    {json.dumps(a, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for a, v in CUES.items()) + "}\n" + b[k:]
bp.write_text(b, "utf-8")

Q = {
    "bed": ["Bettgestell historisch", "bedstead 19th century", "Strohsack Bett", "iron bed historic", "Schlafstelle Bett Arbeiterwohnung"],
    "interior": ["Wohnung Arbeiter Berlin 1900 Stube", "Zille Wohnung Stube Berlin", "Wohnungsuntersuchung Berlin Wohnung", "Berlin tenement interior 1900", "Arbeiterwohnung Küche Stube Kinder", "Notwohnung Berlin 1910"],
    "family": ["Arbeiterfamilie Berlin 1900", "Zille Familie Berlin", "working class family Germany 1900", "Arbeiterfamilie Wohnung Kinder 1910"],
    "kitchen": ["Küche Kohleherd historisch", "Arbeiterküche 1900", "Kachelofen Stube historisch", "kitchen coal stove 19th century"],
    "hinterhof": ["Berliner Hinterhof", "Hinterhof Mietskaserne Berlin", "Berlin courtyard tenement", "Hof Wäsche Berlin 1900", "Zille Hinterhof", "Berlin Hinterhof historisch Foto"],
    "mietskaserne": ["Mietskaserne Berlin", "Mietskaserne Fassade", "Berlin tenement building 19th century", "Gründerzeit Mietshaus Berlin Fassade", "Berlin Wedding Mietskaserne", "Mietskasernen Berlin Luftbild"],
    "street": ["Berlin Straßenszene 1900", "Zille Straße Berlin", "Berlin street life 1900 photograph", "Berlin Pferdefuhrwerk 1900", "Berlin Markt 1900", "Berlin Kaiserreich Straße historisch"],
    "city_growth": ["Berlin Panorama 1900", "Berlin Dächer Schornsteine 1900", "Berlin skyline 19th century", "Berlin 1890 Luftaufnahme", "Berlin Stadtansicht 1880", "Berlin Stadtbahn Viadukt 1900"],
    "map": ["Hobrecht-Plan Berlin 1862", "Stadtplan Berlin 1890", "map of Berlin 1880", "Berlin Plan 1900 Karte", "Bebauungsplan Berlin Hobrecht"],
    "hobrecht": ["James Hobrecht", "Hobrecht Bebauungsplan Berlin", "Hobrecht portrait"],
    "kaiserreich": ["Kaiser Wilhelm I Berlin", "Unter den Linden 1900", "Berliner Stadtschloss 1900", "Kaiserreich Parade Berlin", "Wilhelm II Berlin"],
    "workers": ["Borsig Maschinenbau Berlin", "Fabrikarbeiter Berlin 1900", "AEG Fabrik Berlin Arbeiter", "Arbeiter verlassen Fabrik Berlin", "Maschinenfabrik Arbeiter 1900", "Berlin Fabrik 1890"],
    "stats": ["Volkszählung Berlin 1900", "census form Germany 1900", "handwritten ledger 19th century", "Statistisches Jahrbuch Berlin 1905", "Mietvertrag historisch"],
    "reformer": ["Paul Göhre", "Sozialreform Kaiserreich", "Wohnungsreform Berlin 1900", "Arbeiterbewegung Berlin 1900", "SPD Kaiserreich Versammlung"],
    "ledigenheim": ["Ledigenheim Danckelmannstraße", "Danckelmannstraße Charlottenburg", "Ledigenheim Berlin", "Volkshotel Charlottenburg", "Arbeiterwohnheim 1908", "Lindenhof Schöneberg Taut"],
    "doctor": ["Tuberkulose Kinder 1900", "Rachitis Kind historisch", "Krankenhaus Berlin 1900 Station", "tuberculosis ward 1900", "Krankenkasse Berlin 1900"],
    "wwi": ["Berlin 1918 Revolution", "Berlin Erster Weltkrieg Heimatfront", "German soldiers return 1918", "Berlin 1919 hunger", "Berlin Weltkrieg 1916 Straße"],
    "weimar": ["Hufeisensiedlung Britz", "Bruno Taut Siedlung", "Karl-Marx-Hof", "Siedlung 1920er Berlin", "Weimarer Republik Wohnungsbau", "Onkel-Toms-Hütte Siedlung"],
    "housing": ["Siedlung 1920er Wohnungsbau", "Sozialer Wohnungsbau 1920er Berlin", "Gartenstadt Siedlung Berlin", "Wohnblock 1920er Grünhof", "Siedlung Berlin Weimarer Republik"],
    "sbahn": ["Berlin S-Bahn 1920er", "Stadtbahn Berlin historisch", "Berlin Hochbahn 1900", "Berlin Bahnhof Alexanderplatz 1900", "Berlin Straßenbahn 1910"],
    "wien": ["Wien um 1900", "Wien Gemeindebau", "Rotes Wien Gemeindebau", "Karl-Marx-Hof Wien", "Wien Zinshaus Hof 1900"],
    "altbau": ["Berlin Altbau Fassade", "Prenzlauer Berg Altbau", "Kreuzberg Altbau Hinterhof", "Berlin Mietshaus saniert", "Berlin Kahlschlagsanierung 1970"],
    "student": ["Studentenwohnheim Zimmer", "student dormitory room", "Studentenwohnheim Berlin Charlottenburg"],
    "money": ["Reichsmark Münzen Kaiserreich", "German Mark coins 1900", "Kaiserreich Banknoten", "Groschen Münzen", "Mietquittung historisch"],
    "bank": ["Berliner Börse 1900", "Bank Berlin Gründerzeit", "Baustelle Berlin 1900 Mietshaus", "Hypothekenbank 1900", "Bauunternehmer Berlin 1890"],
    "stairs": ["Treppenhaus Mietshaus Altbau", "Hausflur Berlin Mietskaserne", "Treppenhaus Berlin historisch"],
    "basement": ["Kellerwohnung Berlin", "Kellerwohnung 1900", "Dachboden Wohnung historisch", "Dachkammer Berlin"],
    "pub": ["Berliner Kneipe 1900", "Suppenküche 1900", "Volksküche Berlin", "Arbeiter Kneipe historisch", "Speisehalle Arbeiter 1900"],
    "women": ["Näherin 1900 Nähmaschine", "Waschfrau Berlin 1900", "Arbeiterin Berlin 1900", "Dienstmädchen 1900", "Schlafmädchen"],
    "parliament": ["Reichstag Kaiserreich Sitzung", "Rotes Rathaus Berlin 1900", "Preußisches Abgeordnetenhaus", "Berliner Stadtverordnetenversammlung", "Wahl Dreiklassenwahlrecht"],
    "photographer": ["Fotograf Plattenkamera 1900", "Heinrich Lichte Fotograf", "photographer plate camera 1900", "Wohnungsenquete Fotografie Berlin"],
}
CATS = {"Category:Photographs by Heinrich Zille": "street",
        "Category:Heinrich Zille": "street",
        "Category:Courtyards in Berlin": "hinterhof",
        "Category:Berlin in the 1890s": "street",
        "Category:Berlin in the 1900s": "street",
        "Category:Berlin in the 19th century": "city_growth",
        "Category:James Hobrecht": "hobrecht",
        "Category:Paul Göhre": "reformer",
        "Category:Danckelmannstraße (Berlin-Charlottenburg)": "ledigenheim",
        "Category:Borsig": "workers",
        "Category:Poverty in Germany": "family",
        "Category:Tuberculosis in Germany": "doctor",
        "Category:Rickets": "doctor",
        "Category:Seamstresses": "women",
        "Category:Straw mattresses": "bed",
        "Category:Kitchens in the 19th century": "kitchen",
        "Category:Soup kitchens": "pub",
        "Category:Hufeisensiedlung": "weimar",
        "Category:Bruno Taut": "weimar",
        "Category:Karl-Marx-Hof": "wien",
        "Category:Prussian House of Representatives": "parliament",
        "Category:German Empire": "kaiserreich",
        "Category:Weimar Republic": "wwi",
        "Category:Berlin-Moabit": "mietskaserne",
        "Category:Berlin-Weißensee": "mietskaserne",
        "Category:Berlin-Wedding": "mietskaserne",
        "Category:Chemnitz in the 19th century": "city_growth",
        "Category:Sewing machines": "women"}
SMALL = {  # arquivo >= 780 px (scripts/_fetch_small_berlin.py)
    "street": ["Berlin 1900 Photochrom", "Zille Photographie Berlin Straße", "Berlin 1895 photograph street", "Alexanderplatz 1900 photograph"],
    "hinterhof": ["Zille Hinterhof Photographie", "Berlin Hinterhof 1900 photograph", "Berlin courtyard 1910 photograph"],
    "interior": ["Wohnungsuntersuchung Berlin 1904 photograph", "Berlin tenement interior 1910 photograph", "Zille Interieur Arbeiterwohnung"],
    "family": ["Arbeiterfamilie Berlin 1900 photograph", "Zille Kinder Berlin Hof", "working class family 1900 photograph Berlin"],
    "kaiserreich": ["Kaiser Wilhelm I photograph", "Wilhelm II photograph 1900", "Bismarck photograph 1890"],
    "hobrecht": ["James Hobrecht photograph", "Hobrecht Plan 1862 map"],
    "workers": ["Borsig Arbeiter 1900 photograph", "Fabrikarbeiter 1900 photograph Berlin"],
    "reformer": ["Paul Göhre photograph", "Sozialdemokraten Kaiserreich photograph"],
    "women": ["Näherin 1900 photograph", "Arbeiterin 1900 photograph Berlin"],
    "pub": ["Suppenküche Berlin 1900 photograph", "Berlin Kneipe 1900 photograph"],
}
PEX = {"altbau": ["berlin altbau facade", "old apartment building courtyard"], "student": ["student dorm room", "small student room bed"],
       "money": ["old coins", "vintage coins"], "bed": ["old iron bed", "vintage bed bedroom"], "kitchen": ["old kitchen stove", "vintage kitchen"],
       "stairs": ["old staircase building", "stairwell apartment old"], "bank": ["bank building facade"], "housing": ["apartment blocks green courtyard"],
       "basement": ["old cellar", "attic room"], "women": ["vintage sewing machine"]}
NAVIO = {  # 29/10 slot Pexels: poucos assuntos têm vídeo de apoio
    "bed": ["old iron bed", "bed sheets morning"],
    "kitchen": ["old kitchen stove", "cooking potatoes pot"],
    "stairs": ["old staircase", "apartment stairwell"],
    "hinterhof": ["apartment courtyard", "old courtyard building"],
    "mietskaserne": ["berlin apartment buildings", "old apartment building facade"],
    "street": ["berlin street", "old european street"],
    "workers": ["factory workers machinery", "old factory"],
    "women": ["sewing machine", "seamstress sewing"],
    "money": ["coins counting", "old coins"],
    "student": ["student dorm room"],
    "altbau": ["berlin altbau", "berlin apartment building"],
    "housing": ["apartment block green courtyard"],
    "sbahn": ["berlin s-bahn train"],
}
YT = """Berlin um 1900 historische Filmaufnahmen Straßenleben
Berlin Kaiserreich Originalaufnahmen 1900 Film
Mietskaserne Berlin Dokumentation Geschichte
Berliner Hinterhof Geschichte Dokumentation
Schlafgänger Schlafburschen Berlin Geschichte
Heinrich Zille Berlin Milieu Dokumentation
Wohnungsnot Kaiserreich Arbeiterwohnung Doku
Berlin 1910 historic footage tenement street life
Berlin 1920s documentary footage housing Siedlung
Weimarer Republik Wohnungsbau Siedlungen Dokumentation
Berlin Arbeiterleben Kaiserreich Fabrik Doku"""
(D / "yt_queries_berlin.txt").write_text(YT + "\n", "utf-8")


def troca(path, nome, novo):
    t = path.read_text("utf-8")
    a = t.index(nome + " = {")
    z = t.index("\n}\n", a) + 3
    body = nome + " = {  # 29/10/2026 Berlin (de, baia b1)\n" + "".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},\n" for k, v in novo.items()) + "}\n"
    path.write_text(t[:a] + body + t[z:], "utf-8")


troca(S / "fetch_images.py", "QUERIES", Q)
troca(S / "fetch_images_cat.py", "CATS", CATS)
troca(S / "fetch_photos_api.py", "QUERIES", PEX)
troca(S / "fetch_stock_api.py", "QUERIES_NAVIO", NAVIO)
fs = S / "_fetch_small_berlin.py"
shutil.copy2(S / "_fetch_small_uhr.py", fs)
troca(fs, "QUERIES", SMALL)
cc = S / "_cat_berlin.py"
t = (S / "fetch_images_cat.py").read_text("utf-8").replace("w < 1600 or w < 1.3 * h", "w < 780 or w < 1.25 * h")
cc.write_text(t, "utf-8")
print("tema Berlin de gravado;", len(TAGS_ALL), "tags")
