"""BEATS: "Como Vivem os Pescadores de Lagosta do Ceará que Mergulham com Compressor" (pt, 97 parágrafos, 38,6 min).
Modo PADRÃO, ENXUTO, 20 % VÍDEO / 80 % FOTO. Pedido do PAINEL 20261106-111356 (seu canal, automático, baia b1):
paralaxe, mapa, sem trilha. Gerado por scripts/_tema_lag.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIS = "BR"   # Brasil (Ceará, Rio Grande do Norte)
TAGS_LUGAR = ["icapui", "redonda", "falesia", "praia", "fortaleza", "natal", "rn_costa", "vila", "turismo"]

TAGS = {
    "icapui": "ICAPUÍ, Ceará, Brazil: the coast of Icapuí, red cliffs (falésias), light sand beaches, coconut palms and green sea",
    "redonda": "PRAIA DE REDONDA (Icapuí, Ceará): fishing village under the red cliffs, colourful fishing boats anchored near the sand",
    "falesia": "RED CLIFFS (falésias) on the coast of Ceará, Brazil (Icapuí, Canoa Quebrada, Morro Branco) over the beach",
    "praia": "a beach of CEARÁ / northeast Brazil with coconut palms, fishing boats on the sand and green sea",
    "jangada": "a traditional JANGADA (sail raft of northeast Brazil fishermen) on the sea or on the beach of Ceará",
    "barco_pesca": "a small WOODEN FISHING BOAT of northeast Brazil (lagosteiro) at sea or anchored, painted hull, fishermen on deck",
    "pescador": "a FISHERMAN of northeast Brazil (Ceará, Rio Grande do Norte): a man on a boat or on the beach with nets",
    "vila": "a FISHING VILLAGE of northeast Brazil: simple houses by the beach, fishermen's houses, boats pulled up the sand",
    "lagosta": "a live SPINY LOBSTER (Panulirus argus / Caribbean spiny lobster) with long antennae, no claws, on a reef or in a crevice",
    "lagosta_pescada": "caught SPINY LOBSTERS: lobsters in a box or basket, lobster tails, lobsters on a fish market counter",
    "manzua": "a LOBSTER TRAP / lobster pot (manzuá, covo): wooden or wire trap with funnel entrance, traps stacked on a boat or beach",
    "mergulho": "a DIVER UNDERWATER breathing through an air HOSE (hookah diving / surface-supplied), or a diver on a rocky reef",
    "mangueira": "an AIR HOSE coiled on a boat deck / a diver's breathing hose running from a boat into the water",
    "compressor": "a small AIR COMPRESSOR with belt drive / a compressor on a boat, a hookah diving compressor",
    "botijao": "an LPG GAS CYLINDER (botijão de gás de cozinha, 13 kg): blue or orange steel gas cylinders",
    "motor": "a DIESEL BOAT ENGINE inside a small wooden fishing boat, belt and pulley, engine running",
    "fundo": "the rocky SEA BOTTOM: reef with crevices and holes, rocks, gravel, seen underwater",
    "marambaia": "an ARTIFICIAL REEF made of SCRAP: sunken metal drums, tyres, old fridges on the sea bottom; scrap piled for sinking",
    "sucata": "SCRAP: piles of cut and crushed metal drums, old tyres, scrap metal yard",
    "bolhas": "BUBBLES rising underwater / gas bubbles / soda fizzing in a glass bottle",
    "camara": "a HYPERBARIC CHAMBER: big steel cylinder with a round door and portholes, patients inside a recompression chamber",
    "hospital": "a HOSPITAL: emergency room, ICU bed, doctor examining a patient, naval hospital",
    "cadeira": "a WHEELCHAIR / a man in a wheelchair / physiotherapy and rehabilitation after a spinal cord injury",
    "medula": "SPINE / spinal cord: X-ray or MRI of the spine, nerves, doctor showing a spine scan",
    "mar": "the green SEA off northeast Brazil: waves, open sea, sea seen from a small boat",
    "amanhecer": "DAWN / SUNRISE over the sea with fishing boats leaving, first light on the water",
    "fortaleza": "FORTALEZA, Ceará: city skyline on the sea, Mucuripe port and fishing boats, Beira-Mar",
    "natal": "NATAL, Rio Grande do Norte: city on the sea, Potengi river, naval base, Ponte Newton Navarro",
    "rn_costa": "the coast of RIO GRANDE DO NORTE: Rio do Fogo, São Miguel do Gostoso, beaches, reefs, fishing boats",
    "ibama": "IBAMA environmental agents / inspection of boats / seized fishing gear in Brazil",
    "policia": "BRAZILIAN FEDERAL POLICE (Polícia Federal) operation: agents, vehicles, police boat",
    "marinha": "the BRAZILIAN NAVY (Marinha do Brasil): navy patrol ship, sailors, Natal naval base",
    "guerra": "LOBSTER WAR 1961-63: French destroyer Tartu (T 47 class), Brazilian destroyers Paraná / Pará, warships of the 1960s",
    "aviao": "FAB (Brazilian Air Force) patrol aircraft of the 1960s (B-17, P-15 Neptune) flying over the sea",
    "lancha": "a SPEEDBOAT / patrol launch running fast over the sea",
    "fogo": "a BOAT ON FIRE / a burning wooden boat, flames and smoke on a beach",
    "multidao": "a CROWD of people on a beach in northeast Brazil",
    "defeso": "many FISHING BOATS STOPPED on the beach / anchored and idle in a harbour (closed season)",
    "restaurante": "a LOBSTER DISH in a restaurant: grilled lobster on a plate, seafood restaurant by the sea",
    "fabrica": "a SEAFOOD PROCESSING plant: workers in white packing frozen fish / lobster tails, cold storage",
    "porto": "an EXPORT PORT with containers and reefer containers (Pecém, Mucuripe, Fortaleza)",
    "dinheiro": "BRAZILIAN REAIS banknotes: hands counting reais money",
    "turismo": "TOURISTS on a beach of Ceará (Canoa Quebrada, Ponta Grossa): beach huts, buggies, umbrellas",
    "roca": "a small FARM PLOT (roça) in the northeast Brazil interior: corn, beans, cassava field, farmer with a hoe",
    "familia": "a FAMILY of a fishing village in northeast Brazil / a child going to school in a coastal village",
    "eua": "NORTH AMERICA lobster market: a seafood restaurant in New York / lobster served in the United States",
    "documento": "an official DOCUMENT / law gazette page (Diário Oficial), a stamped decree on a desk"
}

BANCO = {'dinheiro': ['br_dinheiro'], 'hospital': ['navy_hospital', 'enfermaria'], 'mar': ['oceano_superficie', 'mar_mar'], 'motor': ['motor_diesel']}

REJEITA_TITULO = ['toy\\b|toys|lego|diorama|render|\\b3d\\b|game|poster|clipart|cartoon|minecraft|model kit|scale model|aquarium|aquário|aquario|homarus|american lobster|maine|nova scotia|crayfish|crawfish|lagostim|cruise|titanic|yacht|museum|museu|museo|tesla|cybertruck|australia|new zealand|florida keys|bahamas|belize|honduras']

FOREIGN = ["render", "3d model", "cgi", "video game", "cartoon", "illustration", "infographic", "painting"]

G, E, C, F = "gancho", "exposicao", "climax", "fecho"
_PT = ['mergulho mangueira G', 'barco_pesca mar', 'icapui falesia', 'falesia barco_pesca', 'icapui pescador', 'lagosta eua', 'mergulho mar', 'lagosta lagosta_pescada', 'lagosta fundo', 'manzua jangada', 'pescador roca', 'jangada mar', 'mar amanhecer', 'lagosta mar', 'pescador jangada', 'barco_pesca pescador', 'pescador barco_pesca', 'compressor motor', 'mergulho fundo', 'compressor documento', 'compressor botijao', 'botijao compressor', 'mangueira mergulho', 'motor mangueira', 'mangueira pescador', 'barco_pesca pescador', 'praia mar', 'sucata marambaia', 'fundo sucata', 'ibama marambaia', 'sucata ibama', 'mergulho lagosta', 'amanhecer barco_pesca', 'amanhecer barco_pesca', 'mergulho fundo', 'rn_costa mergulho', 'mergulho fundo', 'bolhas mergulho', 'mar bolhas', 'mergulho bolhas', 'mergulho fundo', 'bolhas mergulho', 'bolhas medula', 'mergulho bolhas', 'mergulho barco_pesca', 'medula hospital', 'barco_pesca mar', 'praia', 'pescador vila', 'pescador icapui', 'barco_pesca mar', 'camara hospital', 'pescador familia', 'hospital medula', 'cadeira vila', 'cadeira familia', 'camara', 'camara', 'camara', 'camara medula', 'natal marinha', 'marinha camara', 'barco_pesca cadeira', 'praia mar', 'barco_pesca icapui', 'marinha mar', 'falesia pescador', 'jangada pescador', 'barco_pesca icapui', 'ibama policia', 'lancha mar', 'praia lancha', 'ibama policia', 'mar defeso', 'defeso barco_pesca', 'defeso lagosta', 'dinheiro pescador', 'lagosta defeso', 'porto lagosta', 'lagosta fundo', 'mergulho camara', 'mar', 'policia ibama', 'dinheiro', 'dinheiro lagosta_pescada', 'eua porto', 'familia vila', 'mar', 'lagosta_pescada pescador', 'mar barco_pesca', 'fortaleza pescador', 'defeso turismo', 'mergulho motor', 'bolhas', 'barco_pesca pescador C', 'lagosta icapui', 'praia falesia F']
_M = {"G": G, "C": C, "F": F}
_T = {}
for i, x in enumerate(_PT):
    w = x.split()
    if len(w) == 1 or w[1] in _M:
        w = [w[0], w[0]] + w[1:]
    _T[i] = [w[0], w[1], _M.get(w[2], E) if len(w) > 2 else E]
_FRIO = {0, 32, 64, 6, 39, 74, 13, 48, 17, 82, 88, 57, 27}
_REVEAL = set()
_ANIM = {3: 'L01-Rota', 8: 'L04-Ovos', 14: 'L05-Queda', 19: 'L06-Portaria', 29: 'L14-Marambaias', 34: 'L07-Prof', 43: 'L15-Regras', 53: 'L09-Casos', 60: 'L10-Natal', 84: 'L13-Preco'}
_CAP = {0: ('TERRA DA LAGOSTA', 'ICAPUÍ — CEARÁ'), 6: ('O ANIMAL', 'LAGOSTA ESPINHOSA'), 13: ('A QUEDA', 'MAIS DE 80 % A MENOS'), 17: ('O COMPRESSOR', 'PROIBIDO DESDE 1995'), 27: ('A MARAMBAIA', 'SUCATA NO FUNDO DO MAR'), 32: ('UM DIA NO FUNDO', '46 A 66 METROS'), 39: ('O NITROGÊNIO', 'DOENÇA DESCOMPRESSIVA'), 48: ('QUANTOS MORREM', '7 DE 28'), 57: ('A CÂMARA HIPERBÁRICA', 'NATAL — RIO GRANDE DO NORTE'), 64: ('A GUERRA DA LAGOSTA', 'DE 1961 A 2010'), 74: ('O DEFESO', 'NOVEMBRO A ABRIL'), 82: ('QUEM GANHA', 'DE ICAPUÍ A NOVA IORQUE'), 88: ('SETENTA METROS', 'ICAPUÍ — 2025')}
_SLATE = {}


def _extra(i):
    x = {"modo": _T[i][2], "lado": "frio" if i in _FRIO else "quente", "reveal": i in _REVEAL}
    if i in _CAP:
        x.update(capitulo=_CAP[i][0], lugar=_CAP[i][1])
    if i in _SLATE:
        x["slate"] = _SLATE[i]
    return x


B = [(i, _T[i][:2], _ANIM.get(i), _extra(i)) for i in range(97)]


def main():
    beats = []
    for para, tags, anim, extra in B:
        assert all(t in TAGS for t in tags), (para, tags)
        beats.append({
            "id": f"b{para:03d}", "para": para, "tags": tags, "anim": anim,
            "era": extra.get("era", "any"), "place": None, "part": None,
            "mustShow": TAGS[tags[0]],
            "modo": extra.get("modo", "exposicao"), "lado": extra.get("lado", "quente"),
            "reveal": bool(extra.get("reveal")),
            "slate": list(extra["slate"]) if "slate" in extra else None,
            "capitulo": extra.get("capitulo"),
            "lugar": extra.get("lugar"),   # 26/09/2026: carimbo de lugar/data batido à máquina no capítulo
        })
    assert [b["para"] for b in beats] == list(range(97)), "paragrafos fora de ordem ou faltando"
    (ROOT / "data" / "beats.json").write_text(
        json.dumps({"tags": TAGS, "foreign": FOREIGN, "rejeita_titulo": REJEITA_TITULO,
                    "banco": globals().get("BANCO", {}), "beats": beats,
                    # 04/10/2026: país do roteiro (banco.py só serve item desse país ou genérico) e tags de LUGAR
                    "pais": globals().get("PAIS"), "tags_lugar": list(globals().get("TAGS_LUGAR", []))},
                   ensure_ascii=False, indent=1), "utf-8")
    print(f"[beats] {len(beats)} beats, {sum(1 for b in beats if b['anim'])} animacoes, "
          f"{sum(1 for b in beats if b['capitulo'])} capitulos, {sum(1 for b in beats if b['reveal'])} reveals")


if __name__ == "__main__":
    main()
