"""Busca vídeo nas APIs OFICIAIS do Pexels e do Pixabay (liberadas pelo usuário em 2026-09-13).

Licenças: Pexels License e Pixabay Content License — uso comercial gratuito, modificação permitida,
sem atribuição obrigatória (registramos autor e link mesmo assim). Não vender o arquivo sem alteração.

Chaves: o USUÁRIO cria as contas e salva cada chave num arquivo de texto (uma linha):
  %USERPROFILE%\\.pexels_key   e   %USERPROFILE%\\.pixabay_key
O script só lê o arquivo e manda no cabeçalho/parâmetro da API — a chave nunca é impressa nem gravada em data/.

Saída: data/stock_api_pool.json {"px:ID"|"pb:ID": {...}} e data/cand_api.json (lista de sondagem por tag).
Uso: python fetch_stock_api.py [N_POR_TAG]
"""
import json, re, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
HOME = Path.home()
N_PER_TAG = int(sys.argv[1]) if len(sys.argv) > 1 else 8
ROUND2 = "--r2" in sys.argv  # usa QUERIES_R2 e grava data/cand_api_r2.json
ROUND3 = "--r3" in sys.argv  # usa QUERIES_R3 e grava data/cand_api_r3.json

QUERIES = {  # tag do beat -> buscas em inglês (assunto real, sem recreativo)
    "ocean_surface": ["rough sea waves", "open ocean aerial", "ocean storm waves"],
    "platform_storm": ["ship in storm waves", "stormy sea night"],
    "platform": ["offshore oil platform", "oil rig at sea", "offshore platform aerial"],
    "darkness": ["deep sea dark underwater", "dark underwater light rays", "underwater darkness particles"],
    "diver_underwater": ["commercial diver underwater", "diver helmet underwater", "diver working underwater"],
    "dsv": ["offshore vessel at sea", "offshore supply ship", "ship crane at sea"],
    "pipeline": ["underwater pipeline", "subsea pipe"],
    "welding": ["underwater welding"],
    "helicopter": ["helicopter flying over sea", "offshore helicopter"],
    "control_room": ["control room monitors operator", "industrial control panel"],
    "medical": ["doctor examining patient", "medical checkup"],
    "family": ["father hugging child", "family at home evening", "man video call family"],
    "crab_fishing": ["crab fishing boat", "fishing boat rough sea"],
    "logging": ["logging trees forest machine", "lumberjack chainsaw"],
    "mining": ["underground mine workers", "coal mine tunnel"],
    "construction": ["construction worker high rise", "steel beam construction height"],
    "decompression": ["hyperbaric chamber"],
}
QUERIES_R3 = {  # rodada 3: ambientação honesta dos trechos de câmara/descompressão/ROV sem vídeo
    "decompression": ["pressure gauge needle", "industrial pressure gauge", "valve wheel turning", "air pressure manometer"],
    "pipeline": ["industrial pipeline valves", "steel pipes factory", "pipe welding pipeline"],
    "rov": ["underwater drone", "underwater robot", "robotic arm industrial"],
    "control_room": ["operator monitoring screens dark room", "ship bridge at night", "radar screen ship"],
    "darkness": ["marine snow deep sea", "dark ocean depth particles", "bioluminescence deep sea"],
}
QUERIES_R2 = {  # rodada 2: tags de ambientação que ainda faltam (cortes vazios em beats de câmara/mergulho)
    "darkness": ["deep blue ocean underwater", "underwater abyss", "underwater light beams deep", "bubbles rising underwater dark"],
    "ocean_surface": ["ocean at night", "underwater view of ocean surface", "grey sea timelapse"],
    "dsv": ["ship deck crew working", "offshore vessel crane lifting", "ship at sea night lights", "rope winch ship deck"],
    "diver_underwater": ["diver descending rope", "underwater hose bubbles", "diver underwater low visibility"],
}
QUERIES_NOR = {  # tema vivir en Noruega (--nor)
    "fjord": ["norway fjord", "geiranger fjord", "fjord norway drone", "norway fjord boat"],
    "mountains_snow": ["norway mountains snow", "norway mountain lake reflection", "norway mountains"],
    "red_houses": ["lofoten red houses", "norway red wooden houses", "reine norway"],
    "fishing_boat": ["norway fishing boat", "lofoten fishing village", "norway harbor boats"],
    "sea_coast": ["norway coast", "norway coastline aerial", "norwegian sea"],
    "aurora": ["aurora borealis norway", "northern lights norway", "northern lights tromso"],
    "polar_night": ["tromso winter night", "norway winter night", "norway polar night"],
    "midnight_sun": ["midnight sun norway", "norway summer sunset"],
    "winter_town": ["norway winter town", "oslo winter snow", "norway snow street"],
    "oslo_city": ["oslo", "oslo city", "oslo opera house", "oslo street"],
    "bergen": ["bergen norway", "bryggen bergen"],
    "tromso_north": ["tromso", "tromso norway"],
    "stavanger": ["stavanger norway", "stavanger"],
    "oil_platform": ["offshore oil platform", "oil rig at sea", "north sea oil platform"],
    "money": ["norwegian krone", "norwegian money", "paying with card", "counting money"],
    "shop_prices": ["supermarket shopping", "grocery store checkout", "supermarket shelves"],
    "cafe_restaurant": ["coffee shop barista", "restaurant dinner friends", "cafe people"],
    "housing": ["oslo apartments", "norway houses neighborhood", "scandinavian apartment building"],
    "hospital": ["hospital corridor", "doctor patient consultation", "nurse hospital"],
    "school": ["classroom students", "university students campus", "kindergarten children playing"],
    "family_kids": ["father pushing stroller", "children playing snow", "family walking park"],
    "office_work": ["scandinavian office", "casual office meeting", "coworkers office"],
    "cabin": ["norway cabin", "cabin fireplace candles", "wooden cabin mountains norway"],
    "hiking_outdoor": ["hiking norway", "camping tent norway", "campfire forest norway"],
    "skiing": ["cross country skiing", "skiing norway", "kids skiing"],
    "sami_reindeer": ["reindeer herd", "reindeer norway", "sami norway"],
    "celebration": ["norway national day", "17 may norway", "christmas candles window", "christmas market"],
    "design_architecture": ["scandinavian interior design", "oslo architecture", "nordic wooden architecture"],
    "safety_prison": ["bicycle city street", "children walking to school"],
    "military": ["norwegian soldiers", "norwegian army"],
    "salmon_farm": ["salmon farm norway", "fish farm fjord", "salmon farming"],
    "hydropower": ["hydroelectric dam", "norway waterfall", "hydropower plant"],
    "electric_car": ["electric car charging", "ev charging station", "electric car driving"],
    "transport": ["norway train", "oslo tram", "norway road", "norway ferry"],
    "people_street": ["people walking street winter", "bus passengers", "oslo people walking"],
    "loneliness": ["lonely man window", "alone winter", "sad woman window"],
    "language_class": ["language class adults", "student studying notebook"],
    "alcohol": ["beer bar", "wine shop shelves", "pouring beer"],
    "mental_health": ["therapy session", "psychologist conversation"],
    "food": ["brown cheese", "sandwich lunch box", "fish dinner plate", "cod fish"],
    "sweden_border": ["car driving country road", "shopping bags car trunk"],
}
# tags de LUGAR: só entram se a descrição/tags do stock nomear a Noruega (paisagem igual à da Islândia/Canadá)
PLACE_TAGS = {"fjord", "mountains_snow", "red_houses", "fishing_boat", "sea_coast", "aurora", "polar_night", "midnight_sun",
              "winter_town", "oslo_city", "bergen", "tromso_north", "stavanger", "housing", "cabin", "hiking_outdoor",
              "sami_reindeer", "military", "salmon_farm", "transport"}
NOR = re.compile(r"(norway|norwegian|norge|norsk|oslo|bergen|trondheim|troms|stavanger|lofoten|geiranger|senja|alesund|"
                 r"[åa]lesund|bod[øo]|reine|svalbard|preikestolen|trolltunga|hamn[øo]y|fl[åa]m|sognefjord|hardanger|narvik|"
                 r"kirkenes|finnmark|nordkapp|north-cape|\bsami\b|hurtigruten)", re.I)
FOREIGN_PLACE = re.compile(r"(iceland|reykjavik|faroe|greenland|finland|lapland|rovaniemi|canada|alaska|switzerland|swiss|"
                           r"\balps\b|new-zealand|new zealand|patagonia|scotland|denmark|copenhagen|sweden|stockholm|chile|"
                           r"dolomites|austria|italy|germany|russia)", re.I)
NOR_THEME = "--nor" in sys.argv
CN_THEME = "--cn" in sys.argv  # tema Canadian National / pradaria de Manitoba (grava data/cand_api_cn.json)
QUERIES_CN = {
    "cn_train_snow": ["freight train snow canada", "canadian national train", "freight train winter", "train in blizzard"],
    "locomotive_exterior": ["diesel locomotive canada", "freight locomotive winter", "locomotive snow"],
    "cab_interior": ["locomotive cab interior", "train driver cab", "train cab view snow"],
    "control_stand": ["train control panel", "locomotive controls", "train dashboard gauges"],
    "prairie_winter": ["snowy prairie", "flat snow field winter", "canadian prairie winter", "manitoba winter"],
    "blizzard": ["blowing snow road", "snowstorm wind", "whiteout blizzard", "snow drifting wind"],
    "snowplow": ["train snow plow", "railway snow removal"],
    "fuel": ["diesel fuel pump", "refueling diesel tank"],
    "idling_yard": ["locomotives rail yard winter", "train yard snow", "diesel exhaust cold"],
    "rail_yard": ["rail yard winter", "freight cars snow", "train yard aerial"],
    "air_brakes": ["train coupler close up", "railway brake hose", "freight car coupling"],
    "rail_track": ["railway track snow", "train tracks winter", "rail close up frost"],
    "detector": ["railway signal snow", "railroad signal light"],
    "switch": ["railway switch snow", "rail junction winter"],
    "crew_outdoor": ["worker winter gear cold", "railway worker snow", "man walking blizzard"],
    "night_headlight": ["train headlight night snow", "train at night winter", "headlights snowstorm night"],
    "grain_elevator": ["grain elevator prairie", "grain silo canada", "grain elevator winter"],
    "small_town": ["small prairie town winter", "water tower snow town", "chimney smoke winter"],
    "dispatch": ["control room monitors", "dispatcher radio", "operations center screens"],
    "distributed_power": ["long freight train aerial", "freight train drone winter"],
    "crossing": ["railroad crossing lights snow", "level crossing winter"],
    "maintenance": ["locomotive maintenance shop", "train workshop mechanic"],
    "ice_fog": ["ice fog winter", "frost fog cold morning", "hoarfrost trees fog"],
    "winnipeg": ["winnipeg winter", "winnipeg"],
}
PLACE_TAGS_CN = {"cn_train_snow", "locomotive_exterior", "grain_elevator", "small_town", "winnipeg", "distributed_power"}
CAN = re.compile(r"(canada|canadian|manitoba|winnipeg|saskatchewan|alberta|prairie|\bcn\b)", re.I)
FOREIGN_CN = re.compile(r"(bnsf|union-pacific|union pacific|csx|norfolk|amtrak|via-rail|cpkc|canadian-pacific|canadian pacific|"
                        r"russia|siberia|germany|switzerland|swiss|norway|sweden|finland|austria|italy|india|china|japan|"
                        r"australia|uk|england|scotland|poland|czech|toy|model|lego)", re.I)
BAD = re.compile(r"\b(coral|reef|snorkel|scuba (?:lesson|holiday)|turtle|shark|dolphin|whale|fish tank|aquarium|mermaid|"
                 r"swimming pool|pool|beach|surf|surfing|vacation|holiday|tourist|kayak|freediv\w*|animation|3d|cgi|"
                 r"render|green screen|text|logo|slow motion water drop)\b", re.I)


SUB_THEME = "--sub" in sys.argv  # tema vida dentro de um submarino nuclear (grava data/cand_api_sub.json)
QUERIES_SUB = {
    "submarine_surface": ["submarine", "submarine ocean", "military submarine"],
    "submarine_underwater": ["submarine underwater", "deep ocean underwater", "underwater dark ocean"],
    "ocean_deep": ["deep sea darkness", "underwater light rays", "ocean abyss"],
    "control_room": ["control room red light", "military control panel", "radar screen operator"],
    "sonar": ["sonar screen", "headphones listening operator", "oscilloscope waveform"],
    "reactor_engine": ["engine room pipes valves", "industrial pipes valves", "turbine machinery"],
    "galley": ["industrial kitchen cooking", "baking bread oven", "canned food storage"],
    "mess_deck": ["soldiers eating together", "people eating cafeteria", "playing cards table"],
    "berthing": ["bunk beds", "narrow corridor metal", "locker room"],
    "crew_work": ["sailors cleaning", "worker wrench pipes", "laundry machine"],
    "damage_control": ["firefighter training smoke", "fire extinguisher smoke", "water leak pipe"],
    "pier_departure": ["navy ship leaving port", "family goodbye hug", "harbor pier"],
    "homecoming": ["soldier homecoming family", "family reunion hug", "naval base pier"],
    "gym": ["treadmill running", "weight training dumbbell"],
    "training": ["classroom students technical", "simulator training"],
    "medical": ["medical examination doctor", "doctor stethoscope"],
    "missile": ["missile launch", "rocket launch sea"],
}
DECOY = re.compile(r"(toy|lego|miniature|model|diecast|\brc\b|simulator|game|cartoon|animation|3d-render|cgi|yellow-submarine|"
                   r"tourist-submarine|aquarium|snorkel|scuba-diving-holiday)", re.I)
NAVIO_THEME = "--navio" in sys.argv  # tema por que um navio de aco flutua (grava data/cand_api_navio.json)
QUERIES_NAVIO = {  # 06/11/2026 pescadores de lagosta do Ceará (pt, baia b1)
    "mergulho": ["diver underwater hose", "scuba diver reef rocks"],
    "fundo": ["underwater reef rocks", "coral reef crevice"],
    "lagosta": ["spiny lobster underwater", "lobster reef"],
    "bolhas": ["underwater bubbles rising"],
    "mar": ["sea waves aerial", "boat on green sea"],
    "barco_pesca": ["wooden fishing boat sea", "fishing boat brazil"],
    "praia": ["beach coconut palms brazil", "tropical beach fishing boats"],
    "amanhecer": ["sunrise sea boat"],
    "motor": ["boat engine running"],
    "camara": ["hyperbaric chamber"],
    "hospital": ["hospital emergency"],
    "lancha": ["speedboat sea"],
}
DECOY_NAVIO = re.compile(r"(toy|lego|miniature|model|diecast|\brc\b|simulator|game|cartoon|animation|3d-render|cgi|"
                         r"cruise-cabin|swimming-pool|aquarium|sailing-yacht|regatta|kayak|paddle)", re.I)
CRAB_THEME = "--crab" in sys.argv  # tema pesca de caranguejo no mar de Bering (grava data/cand_api_crab.json)
QUERIES_CRAB = {  # rodada 2: SO clima frio — a rodada 1 trouxe barco tropical do Vietna/Bangladesh
    "crab_boat_sea": ["fishing boat winter sea", "trawler rough sea", "fishing vessel storm", "boat cold ocean"],
    "crab_pot_deck": ["fishing gear deck winter", "rope coil deck boat", "steel deck boat wet", "buoy rope boat"],
    "hauling_gear": ["winch rope pulling boat", "hands pulling rope wet", "fishing net winch", "hydraulic winch boat"],
    "sorting_table": ["hands sorting fish", "fish on conveyor", "seafood on ice hands", "fish catch close up"],
    "king_crab": ["crab close up", "crab on ice", "live crab claws", "crab seafood ice"],
    "dutch_harbor": ["harbor winter snow", "cold harbor boats", "fishing port winter", "harbor fog cold"],
    "processor_plant": ["fish processing plant workers", "seafood factory conveyor", "food factory workers gloves"],
    "storm_sea": ["storm waves ocean", "rough sea grey", "big waves storm", "sea storm wind", "ship storm waves"],
    "icing_ship": ["frozen boat ice", "ice covered rope", "frozen harbor", "icicles cold metal"],
    "deck_crew_work": ["worker rain gear cold", "hands work gloves cold", "man working night deck", "worker cold wind"],
    "immersion_suit": ["rescue training water", "man floating in water rescue", "survival training pool"],
    "coast_guard_rescue": ["rescue helicopter sea", "helicopter hoist water", "helicopter flying over ocean"],
    "wheelhouse": ["boat wheelhouse controls", "ship radar screen", "captain steering ship", "ship bridge night"],
    "engine_room": ["engine room machinery", "marine engine", "industrial engine running"],
    "bunk_galley": ["ship cabin bunk", "small kitchen boat", "crew quarters ship"],
    "aleutian_air": ["small plane snow runway", "propeller plane landing", "airport snow winter"],
    "noaa_survey": ["research vessel science", "scientist measuring sample boat", "marine research ship"],
    "cold_sea_surface": ["cold sea surface", "grey ocean water", "arctic water", "ocean fog cold", "sea ice water"],
    "fishing_fleet_dock": ["fishing boats harbor winter", "boats moored snow", "dock winter boats"],
    "aleutian_landscape": ["snow mountains coast", "arctic coastline", "volcano snow landscape", "cold island coast"],
}
# banco de imagens confunde: brinquedo, render, caranguejo de prato e pesca esportiva/tropical
DECOY_CRAB = re.compile(r"(toy|lego|miniature|model|diecast|\brc\b|simulator|game|cartoon|animation|3d-render|cgi|"
                        r"restaurant|recipe|cooked|cooking|boiled|plate|sushi|market|aquarium|"
                        r"sport-fishing|angler|fly-fishing|charter|tropical|beach-holiday|yacht|sailing-regatta)", re.I)
ULTRA_THEME = "--ultra" in sys.argv  # tema Part 103 / ultraleves (grava data/cand_api_ultra.json)
QUERIES_ULTRA = {
    "ultralight_flying": ["ultralight aircraft", "small airplane flying sky", "light aircraft in flight",
                          "propeller plane flying"],
    "open_cockpit_ultralight": ["open cockpit airplane", "small plane pilot seat", "vintage small aircraft"],
    "quicksilver_type": ["powered hang glider", "microlight flying", "ultralight sky"],
    "kolb_folding": ["airplane wing folding", "aircraft trailer transport", "small plane garage"],
    "bush_ultralight": ["bush plane landing dirt", "small plane tundra tires", "plane landing field"],
    "enclosed_ultralight": ["small aircraft cabin interior", "light aircraft cockpit window"],
    "trike_weightshift": ["microlight trike flying", "powered paraglider trike", "ultralight trike sky"],
    "ultralight_helicopter": ["small helicopter flying", "helicopter takeoff field", "helicopter rotor start"],
    "kit_build_workshop": ["workshop building metal", "man working workshop tools", "riveting metal workshop",
                           "woodworking workshop hands"],
    "two_stroke_engine": ["small engine running", "propeller spinning close", "engine workshop bench"],
    "cockpit_pov": ["airplane cockpit instruments", "pilot hands controls", "instrument panel small plane"],
    "takeoff_grass": ["small plane takeoff grass", "airplane taking off field", "plane accelerating runway"],
    "landing_approach": ["small plane landing", "airplane approach runway", "plane wheels touchdown"],
    "grass_airfield": ["small airfield hangar", "grass runway airfield", "windsock airfield"],
    "trailer_storage": ["trailer towing vehicle", "garage door open vehicle", "hangar door aircraft"],
    "ballistic_parachute": ["parachute deploy sky", "emergency parachute aircraft"],
    "pilot_gear": ["pilot helmet headset", "pilot preparing flight", "aviation headset close"],
    "sky_clouds": ["sky clouds timelapse", "blue sky clouds", "sunrise clouds sky"],
    "rural_landscape_air": ["aerial farmland fields", "aerial river valley low", "aerial countryside road"],
    "flight_school": ["flight instructor student", "pilot training aircraft", "briefing pilots airfield"],
}
# banco de imagens confunde: aeromodelo, simulador, jato, drone e salto de paraquedas
DECOY_ULTRA = re.compile(r"(toy|lego|miniature|model-plane|rc-plane|diecast|\brc\b|simulator|game|cartoon|"
                         r"animation|3d-render|cgi|airliner|jet|airport-terminal|boarding|skydiv|parachute-jump|"
                         r"drone-quadcopter|fpv-drone|balloon)", re.I)
TREN_THEME = "--tren" in sys.argv  # tema trem de carga nas Rochosas (grava data/cand_api_tren.json)
QUERIES_TREN = {
    "train_mountain": ["freight train mountains", "cargo train mountain railway", "train mountain landscape"],
    "train_snow": ["freight train snow", "railway snow winter", "train winter mountains"],
    "locomotive_ext": ["diesel locomotive", "freight locomotive close", "train engine passing"],
    "consist_long": ["long freight train aerial", "cargo train drone aerial", "freight train curve aerial"],
    "cab_interior": ["train driver cab", "locomotive cab interior", "train driver controls"],
    "controls_stand": ["train control lever", "industrial control lever hand", "machine throttle lever"],
    "wheels_rail": ["train wheels rail", "railway track close up", "steel rail track detail"],
    "yard": ["freight train yard aerial", "container yard train", "railway yard wagons"],
    "tunnel": ["train tunnel", "railway tunnel entrance", "train entering tunnel"],
    "rockies_landscape": ["rocky mountains landscape", "mountain pass valley", "colorado mountains aerial"],
    "bridge_curve": ["train bridge viaduct", "railway curve train", "train trestle bridge"],
    "freight_cars": ["freight containers train", "tank cars railway", "grain hopper wagons"],
    "signals": ["railway signal light", "train signal night", "railroad crossing lights"],
    "track_work": ["railway track maintenance", "rail welding worker", "railway inspection worker"],
    "snow_plow": ["snow plow machine", "snow removal machine", "snow blower winter road"],
    "dispatcher": ["control room screens operator", "operations center monitors"],
    "crew_change": ["worker climbing ladder machine", "railway worker vest", "train driver walking track"],
}
# maquete/simulador/brinquedo parecem reais no banco de imagens; ferrovia de outro continente também não serve
DECOY_TREN = re.compile(r"(toy|lego|miniature|model|diecast|\brc\b|simulator|game|cartoon|animation|3d-render|cgi|"
                        r"steam-train-tourist|christmas|thomas|subway|metro|tram|monorail|"
                        r"india|china|japan|shinkansen|europe|german|france|italy|spain|switzerland|russia)", re.I)
MAQ_THEME = "--maq" in sys.argv  # tema 15 máquinas que substituem 200 trabalhadores (grava data/cand_api_maq.json)
QUERIES_MAQ = {
    "asphalt_milling": ["asphalt milling machine", "road milling", "asphalt removal machine"],
    "potato_harvester": ["potato harvester", "potato harvest machine"],
    "brick_robot": ["bricklaying robot", "construction robot bricks"],
    "pile_driver": ["pile driver", "pile driving construction"],
    "cotton_picker": ["cotton harvester", "cotton picker field"],
    "dredger": ["dredger", "dredging ship", "sand dredging"],
    "feller_buncher": ["forestry harvester", "tree cutting machine", "logging machine"],
    "asphalt_paver": ["asphalt paver", "road paving", "road construction asphalt"],
    "sugarcane_harvester": ["sugarcane harvester", "sugar cane harvest brazil", "sugarcane field"],
    "container_crane": ["container crane port", "container terminal", "port crane ship"],
    "combine_harvester": ["combine harvester", "wheat harvest drone", "grain harvest"],
    "construction_3d_printer": ["3d printed house", "construction 3d printer", "concrete 3d printing"],
    "rock_crusher": ["stone crusher", "rock crusher quarry", "quarry conveyor"],
    "tbm": ["tunnel boring machine", "tunnel construction", "tunnel excavation"],
    "bucket_wheel": ["bucket wheel excavator", "open pit mine", "coal mine excavator"],
    "manual_labor": ["workers digging shovel", "manual labor construction", "farm workers harvesting by hand"],
    "construction_site": ["construction site heavy machinery", "construction site aerial"],
    "road_work": ["road works night", "highway construction"],
    "farm_field": ["harvest field aerial", "farm field drone harvest"],
    "port": ["container port aerial", "cargo ship port"],
    "mine_pit": ["open pit mine aerial", "mining trucks"],
    "forest": ["logging forest", "timber logs pile"],
    "heavy_machinery": ["heavy machinery working", "giant machines"],
}
TOY_GAME = re.compile(r"(toy|lego|miniature|model|diecast|rc\b|simulator|game|cartoon|animation|3d-render|cgi)", re.I)


def key(name):
    p = HOME / name
    if not p.exists():
        return None
    k = p.read_text("utf-8-sig", errors="replace").strip().strip('"')
    return None if (not k or "COLE" in k.upper() or "CHAVE" in k.upper()) else k  # texto de exemplo não é chave


def pexels(q, k):
    r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": k},
                     params={"query": q, "per_page": 40, "orientation": "landscape", "size": "large"}, timeout=60)
    r.raise_for_status()
    for v in r.json().get("videos", []):
        files = [f for f in v.get("video_files", []) if (f.get("width") or 0) >= 1920 and (f.get("height") or 0) >= 1080
                 and f.get("file_type") == "video/mp4"]
        if not files:
            continue
        f = min(files, key=lambda f: f["width"])  # 1080p antes de 4K (menor, basta)
        slug = v.get("url", "")
        yield f"px:{v['id']}", {"site": "Pexels", "page": slug, "desc": slug.rstrip("/").split("/")[-1],
                               "file": f["link"], "width": f["width"], "height": f["height"], "duration": v.get("duration"),
                               "author": (v.get("user") or {}).get("name"), "author_url": (v.get("user") or {}).get("url"),
                               "license": "Pexels License", "license_url": "https://www.pexels.com/license/"}


def pixabay(q, k):
    r = requests.get("https://pixabay.com/api/videos/", params={"key": k, "q": q, "per_page": 50, "video_type": "film",
                                                                "safesearch": "true"}, timeout=60)
    r.raise_for_status()
    for h in r.json().get("hits", []):
        vids = [v for v in (h.get("videos") or {}).values() if (v.get("width") or 0) >= 1920 and (v.get("height") or 0) >= 1080]
        if not vids:
            continue
        v = min(vids, key=lambda v: v["width"])
        yield f"pb:{h['id']}", {"site": "Pixabay", "page": h.get("pageURL"), "desc": h.get("tags"), "file": v["url"],
                               "width": v["width"], "height": v["height"], "duration": h.get("duration"),
                               "author": h.get("user"), "author_url": f"https://pixabay.com/users/{h.get('user')}-{h.get('user_id')}/",
                               "license": "Pixabay Content License", "license_url": "https://pixabay.com/service/license-summary/"}


def main():
    kp, kb = key(".pexels_key"), key(".pixabay_key")
    if not (kp or kb):
        print("[api] sem chave Pexels ou Pixabay — banco pulado; as outras fontes continuam")
    pool_p = D / "stock_api_pool.json"
    pool = json.loads(pool_p.read_text("utf-8")) if pool_p.exists() else {}
    side = json.loads((D / "source_side.json").read_text("utf-8")) if (D / "source_side.json").exists() else {}
    cand, seen = [], set(side)
    for p in D.glob("probe_round*.json"):  # já sondados (aprovados ou não) não voltam
        seen |= {s["key"] for s in json.loads(p.read_text("utf-8"))}
    for tag, qs in (QUERIES_ULTRA if ULTRA_THEME else QUERIES_CRAB if CRAB_THEME else QUERIES_NAVIO if NAVIO_THEME else QUERIES_TREN if TREN_THEME else QUERIES_SUB if SUB_THEME else QUERIES_MAQ if MAQ_THEME else QUERIES_CN if CN_THEME else QUERIES_NOR if NOR_THEME else QUERIES_R3 if ROUND3 else QUERIES_R2 if ROUND2 else QUERIES).items():
        got = []
        for q in qs:
            for api, k in (("px", kp), ("pb", kb)):
                if not k:
                    continue
                try:
                    it = list(pexels(q, k) if api == "px" else pixabay(q, k))
                except requests.HTTPError as ex:
                    print(f"[{api}] {q}: HTTP {ex.response.status_code}", flush=True)
                    continue
                time.sleep(1.2)  # Pexels 200/h, Pixabay 100/min
                for sk, e in it:
                    if BAD.search(e["desc"] or "") or not (6 <= (e["duration"] or 0) <= 300):
                        continue
                    if MAQ_THEME and TOY_GAME.search(e["desc"] or ""):
                        continue
                    if SUB_THEME and DECOY.search(e["desc"] or ""):
                        continue
                    if TREN_THEME and DECOY_TREN.search(e["desc"] or ""):
                        continue
                    if NAVIO_THEME and DECOY_NAVIO.search(e["desc"] or ""):
                        continue
                    if CRAB_THEME and DECOY_CRAB.search(e["desc"] or ""):
                        continue
                    if ULTRA_THEME and DECOY_ULTRA.search(e["desc"] or ""):
                        continue
                    if CN_THEME and (FOREIGN_CN.search(e["desc"] or "") or
                                     (tag in PLACE_TAGS_CN and not CAN.search(e["desc"] or ""))):
                        continue
                    if NOR_THEME and (FOREIGN_PLACE.search(e["desc"] or "") or
                                      (tag in PLACE_TAGS and not NOR.search(e["desc"] or ""))):
                        continue
                    e.setdefault("queries", [])
                    pool.setdefault(sk, e)
                    if q not in pool[sk].setdefault("queries", []):
                        pool[sk]["queries"].append(q)
                    if sk not in seen:
                        got.append(sk); seen.add(sk)
        for sk in got[:N_PER_TAG]:
            e = pool[sk]
            cand.append({"key": sk, "url": e["file"], "duration": e["duration"], "tag": tag,
                         "label": f"[{tag}] {e['site']} {e['author']} | {(e['desc'] or '')[:70]} [{e['width']}x{e['height']}]"})
        print(f"[api] {tag}: {len(got)} novos, {min(len(got), N_PER_TAG)} para sondar", flush=True)
    pool_p.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
    name = "cand_api_ultra.json" if ULTRA_THEME else "cand_api_crab.json" if CRAB_THEME else "cand_api_navio.json" if NAVIO_THEME else "cand_api_tren.json" if TREN_THEME else "cand_api_sub.json" if SUB_THEME else "cand_api_maq.json" if MAQ_THEME else "cand_api_cn.json" if CN_THEME else "cand_api_nor.json" if NOR_THEME else "cand_api_r3.json" if ROUND3 else "cand_api_r2.json" if ROUND2 else "cand_api.json"
    (D / name).write_text(json.dumps(cand, ensure_ascii=False, indent=1), "utf-8")
    print(f"[api] pool {len(pool)} | candidatos {len(cand)} -> data/{name}")


if __name__ == "__main__":
    main()
