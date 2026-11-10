"""PACOTE DE TEMA do modo ULTRA (PROMPT_v_ULTRA.txt, seções 1 e 9) -> data/tema_config.json

Tudo que vem depois (trilha, efeitos, grade, cartelas) lê ESSE arquivo. A tabela abaixo reproduz a seção 9 do
prompt para os temas que já usamos; tema novo entra aqui com os 5 campos e fica registrado no decisions_log.
Uso: python theme_pack.py <tema>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"

TEMAS = {
    "oceano_maritimo": {
        "grade": {"quente": "azul_esverdeado", "frio": "cinza_tempestade",
                  # colorbalance do ffmpeg: sombras/realces por lado (-1..1)
                  "quente_sombras": (-0.06, 0.04, 0.10), "quente_realces": (0.06, 0.04, -0.06),
                  "frio_sombras": (-0.10, -0.02, 0.14), "frio_realces": (-0.02, 0.00, 0.02),
                  "saturacao": 0.90, "contraste": 1.12, "vinheta": "PI/4.5"},
        "trilha_termos": ["ocean documentary", "underwater ambient", "deep sea drone", "maritime cinematic",
                          "dark ambient drone", "abyss drone"],
        "trilha_reserva": ["ambient drone cinematic", "dark ambient"],
        "trilha_instrumentos": "cordas graves, piano esparso, pad marinho",
        "sfx_termos": {"hit": ["sub bass hit", "cinematic boom low", "deep impact"],
                       "riser": ["riser cinematic", "tension riser"],
                       "whoosh": ["whoosh cinematic", "deep whoosh"],
                       "ambiencia": ["underwater ambience", "deep sea ambience", "ocean deep rumble"],
                       "diegetico": ["sonar ping", "bubbles underwater", "hull creak", "whale click"]},
        "ambiencia": "underwater ambience",
        "inserts_tipicos": ["olho", "dente", "boca", "isca luminosa", "bolha", "neve marinha", "luz do ROV", "tentáculo"],
        "calibracao": "Nat Geo Drain the Oceans; Discovery Deadliest Catch; BBC Blue Planet II (só ritmo)",
    },
}
# variante do filme dos predadores do abismo: mesmo pacote do oceano, com o lado FRIO mais escuro e slates de
# profundidade em vez de lugar/data (o "lugar" deste filme é a zona do oceano)
TEMAS["abismo_oceano"] = dict(TEMAS["oceano_maritimo"], **{
    "grade": dict(TEMAS["oceano_maritimo"]["grade"], frio="preto_azulado",
                  frio_sombras=(-0.12, -0.04, 0.16), frio_realces=(-0.04, -0.02, 0.04)),
    "trilha_termos": ["deep sea drone", "underwater ambient", "dark ambient drone", "abyss ambient",
                      "ocean documentary", "submarine ambient"],
})


# tema do filme do Challenger (28/01/1986): a referência é a TV americana dos anos 80 + Nat Geo "Challenger:
# The Final Flight". Lado QUENTE = o sol da Flórida e a sala de controle; lado FRIO = o gelo, o mar de busca
# e a comissão Rogers. Slate no formato americano (LUGAR, ESTADO / DATA POR EXTENSO).
TEMAS["espaco_nasa"] = {
    "grade": {"quente": "ambar_flórida", "frio": "azul_aço",
              "quente_sombras": (0.06, 0.02, -0.08), "quente_realces": (0.08, 0.04, -0.04),
              "frio_sombras": (-0.10, -0.02, 0.14), "frio_realces": (-0.04, 0.00, 0.06),
              "saturacao": 0.90, "contraste": 1.12, "vinheta": "PI/4.5"},
    "trilha_termos": ["space documentary", "nasa ambient", "dark ambient drone", "somber piano",
                      "tension strings documentary", "cold war ambient"],
    "trilha_reserva": ["ambient drone cinematic", "dark ambient"],
    "trilha_instrumentos": "cordas tensas, piano esparso, pad grave, sino distante",
    "sfx_termos": {"hit": ["sub bass hit", "cinematic boom low", "deep impact"],
                   "riser": ["riser cinematic", "tension riser"],
                   "whoosh": ["whoosh cinematic", "deep whoosh"],
                   "ambiencia": ["wind cold ambience", "room tone control room", "sea wind ambience"],
                   "diegetico": ["radio static", "morse beep", "typewriter", "telephone ring vintage",
                                 "camera shutter vintage", "rocket launch rumble"]},
    "ambiencia": "wind cold ambience",
    "inserts_tipicos": ["gelo na torre", "anel de vedação", "borracha", "copo de água gelada", "botão do console",
                        "teletipo", "relógio", "insígnia da missão", "cadeira vazia", "fumaça no céu"],
    "calibracao": "Nat Geo Challenger: The Final Flight; HISTORY Engineering Disasters; PBS American Experience",
    "pais": "United States", "epoca": "1986",
    "slate": {"lugar": "KENNEDY SPACE CENTER, FLORIDA", "data": "JANUARY 28, 1986"},
}

# tema do filme de Tutancâmon (es, 28/09/2026, pedido do painel): referência HISTORY The UnXplained "Curse of King
# Tut" + Nat Geo "King Tut in Color". Lado QUENTE = ouro, areia, tocha; lado FRIO = pedra da câmara, laboratório,
# escaneamento. Slate em espanhol (LUGAR, PAÍS / DATA POR EXTENSO).
TEMAS["egito_antiguidade"] = {
    "grade": {"quente": "ouro_ambar", "frio": "azul_petroleo",
              "quente_sombras": (0.06, 0.02, -0.08), "quente_realces": (0.08, 0.05, -0.05),
              "frio_sombras": (-0.08, 0.00, 0.10), "frio_realces": (-0.02, 0.02, 0.04),
              "saturacao": 0.90, "contraste": 1.12, "vinheta": "PI/4.5"},
    "trilha_termos": ["egyptian", "middle eastern", "oud", "duduk", "ney flute", "ancient egypt ambient"],
    "trilha_reserva": ["dark ambient drone", "mystery documentary"],
    "trilha_instrumentos": "oud, ney, duduk, frame drum, cordas graves sustentadas",
    "sfx_termos": {"hit": ["sub bass hit", "cinematic boom low", "deep impact"],
                   "riser": ["riser cinematic", "tension riser"],
                   "whoosh": ["whoosh cinematic", "deep whoosh"],
                   "ambiencia": ["desert wind", "sand wind desert", "cave ambience"],
                   "diegetico": ["stone scrape", "fire crackle", "torch", "camera shutter vintage"]},
    "ambiencia": "desert wind",
    "inserts_tipicos": ["tocha", "areia escorrendo", "mão em pedra", "escaravelho", "papiro", "lamparina", "corda",
                        "selo de argila"],
    "calibracao": "HISTORY The UnXplained; Nat Geo Lost Treasures of Egypt e King Tut in Color; Discovery Expedition Unknown",
    "pais": "Egypt", "epoca": "1922-1925",
    "slate": {"lugar": "VALLE DE LOS REYES, EGIPTO", "data": "4 DE NOVIEMBRE DE 1922"},
}

# tema do filme de El Hierro (es, 29/09/2026, pedido do painel): ilha vulcânica atlântica, vento, água, energia.
# Lado QUENTE = lava, sol, vinhas, festa; lado FRIO = mar profundo, névoa, laurissilva, turbinas. Sem cama de vento
# (recado do usuário em 28/09: trilha tem de ter sentido; nada de "vento soprando").
TEMAS["canarias_ilha"] = {
    "grade": {"quente": "lava_dourada", "frio": "atlantico_azul",
              "quente_sombras": (0.05, 0.02, -0.06), "quente_realces": (0.06, 0.04, -0.03),
              "frio_sombras": (-0.06, 0.00, 0.09), "frio_realces": (-0.02, 0.02, 0.04),
              "saturacao": 0.95, "contraste": 1.10, "vinheta": "PI/4.5"},
    "trilha_termos": ["acoustic guitar", "uplifting documentary", "island", "spanish guitar"],
    "trilha_reserva": ["ambient piano"],
    "trilha_instrumentos": "violão, cordas leves, piano, timple (quando houver)",
    "sfx_termos": {"hit": ["sub bass hit", "cinematic boom low", "deep impact"],
                   "riser": ["riser cinematic", "tension riser"],
                   "whoosh": ["whoosh cinematic", "deep whoosh"],
                   "ambiencia": ["ocean waves rocks", "harbour ambience", "village ambience"],
                   "diegetico": ["water flowing pipe", "wind turbine", "church bell distant", "castanets"]},
    "ambiencia": "ocean waves rocks",
    "inserts_tipicos": ["pá de aerogerador", "água caindo", "lava", "sabina torcida", "névoa", "queijo", "uva", "ondas"],
    "calibracao": "Nat Geo Europe from Above; DW Documentary; ARTE Des îles et des hommes",
    "pais": "Spain (Canary Islands)", "epoca": "hoje",
    "slate": {"lugar": "EL HIERRO, ISLAS CANARIAS", "data": "OCÉANO ATLÁNTICO"},
}


def main():
    tema = sys.argv[1] if len(sys.argv) > 1 else "abismo_oceano"
    if tema not in TEMAS:
        raise SystemExit(f"tema '{tema}' não está na tabela: {sorted(TEMAS)}")
    t = TEMAS[tema]
    cfg = {
        "tema": tema, "pais": t.get("pais", "oceano profundo (global)"), "epoca": t.get("epoca", "hoje"),
        "grade": t["grade"], "trilha_termos": t["trilha_termos"], "trilha_reserva": t["trilha_reserva"],
        "trilha_instrumentos": t["trilha_instrumentos"], "sfx_termos": t["sfx_termos"],
        "ambiencia": t["ambiencia"], "inserts_tipicos": t["inserts_tipicos"], "calibracao": t["calibracao"],
        "slate": t.get("slate", {"lugar": "ZONA BATIPELÁGICA", "data": "1 000 A 4 000 METROS"}),
    }
    (D / "tema_config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), "utf-8")
    escreve_grade_ts(cfg)
    print(f"[tema] {tema} -> data/tema_config.json + src/design/grade.ts")
    print("  trilha:", ", ".join(t["trilha_termos"]))
    print("  sfx:", ", ".join(x for v in t["sfx_termos"].values() for x in v))
    print("  grade:", t["grade"]["quente"], "|", t["grade"]["frio"])



def escreve_grade_ts(cfg):
    """src/design/grade.ts: a mesma grade para o Remotion (fotos e vídeos; animações ficam fora)."""
    g = cfg["grade"]
    NL = chr(10)
    linhas = [
        "// GERADO por scripts/theme_pack.py a partir de data/tema_config.json — não editar à mão.",
        "// Grade de cor do tema (modo ULTRA): os mesmos números que scripts/render_hybrid.py aplica no ffmpeg,",
        "// para foto (Remotion) e vídeo (corte seco) parecerem da mesma câmera.",
        'export type Lado = "quente" | "frio";',
        "export const GRADE = {",
        "  ativo: true,",
        f"  contraste: {g.get('contraste', 1.12)},",
        f"  saturacao: {g.get('saturacao', 0.9)},",
        "  // colorbalance do ffmpeg: [r, g, b] em −1..1 para sombras e realces",
        f"  sombras: {{ quente: {json.dumps(g['quente_sombras'])}, frio: {json.dumps(g['frio_sombras'])} }},",
        f"  realces: {{ quente: {json.dumps(g['quente_realces'])}, frio: {json.dumps(g['frio_realces'])} }},",
        "} as const;",
    ]
    (ROOT / "src" / "design" / "grade.ts").write_text(NL.join(linhas) + NL, "utf-8")


if __name__ == "__main__":
    main()
