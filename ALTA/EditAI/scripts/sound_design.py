"""SOUND DESIGN do modo ULTRA (PROMPT_v_ULTRA, seção 7) -> data/sfx_plan.json

Lê data/timeline.json, data/beats.json, data/master_transcript.json, data/sfx_pool.json (+ sfx_probe.json).
Eventos, cada um com o instante em segundos, o arquivo e o ganho em dB (aplicados por music_mix.py):
  hit        golpe grave no PRIMEIRO quadro do primeiro corte de um beat `reveal`; nunca dois em < GAP_HIT s;
             NUNCA sobre um número falado (a batida esconderia o dado) — se cair em número, vai para o corte seguinte
  riser      subida de tensão que termina no hit dos beats de clímax e de 1 em cada 3 reveals (acento <= 30 % do clímax)
  whoosh     leve, junto de cada cartela de capítulo em tela
  ambiencia  cama de ambiente por slate (troca de lugar): começa no corte do slate e vai até o próximo slate
  diegetico  sonar/estalos no bloco do cachalote, bolhas nos trechos de ROV, rangido de casco na pressão
Uso: python sound_design.py
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
FPS = 30
GAP_HIT = 45.0          # s — no máximo um golpe a cada 45 s
# dB RELATIVOS à cama sob a voz (-32 LUFS): golpe -20 LUFS momentâneo (6 dB sob a voz), riser -28, whoosh -30,
# ambiência -38 (camada sob a cama), diegético -26. Com -9/-16/... os golpes ficavam a -41 LUFS: inaudíveis.
HIT_DB, RISER_DB, WHOOSH_DB, AMB_DB, DIEG_DB = +9.0, +4.0, +2.0, -6.0, +6.0
NUM_JANELA = 0.7        # s — número dito a menos disso do golpe = golpe adiado

norm = lambda s: re.sub(r"[^a-z0-9]", "", "".join(
    c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)))
NUMEROS = set("""dois duas tres quatro cinco seis sete oito nove dez onze doze treze quatorze catorze quinze
dezesseis dezessete dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento
duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos mil milhao milhoes
bilhao bilhoes metade dobro triplo""".split())


def escolhe(pool, probe, papel, termos=(), dur=(0, 1e9), usados=None):
    """arquivo do pool com esse papel, preferindo os termos pedidos e a duração na faixa; roda entre os candidatos."""
    cands = []
    for k, v in pool.items():
        if v["papel"] != papel or not (ROOT / v["file"]).exists():
            continue
        d = probe.get(k, {}).get("dur_s", 0)
        if not (dur[0] <= d <= dur[1]):
            continue
        pref = any(t in (v.get("termo", "") + " " + v["title"]).lower() for t in termos)
        cands.append((0 if pref else 1, k))
    cands.sort()
    if not cands:
        return None
    usados = usados if usados is not None else {}
    k = min(cands, key=lambda c: (c[0], usados.get(c[1], 0)))[1]
    usados[k] = usados.get(k, 0) + 1
    return k


def main():
    tl = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    beats = {b["id"]: b for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
    tr = json.loads((D / "master_transcript.json").read_text("utf-8"))
    palavras = [(w["s"], norm(w["w"])) for s in tr["sentences"] for w in s["words"]]
    pool = json.loads((D / "sfx_pool.json").read_text("utf-8"))
    probe = json.loads((D / "sfx_probe.json").read_text("utf-8")) if (D / "sfx_probe.json").exists() else {}
    total = json.loads((D / "source_meta.json").read_text("utf-8"))["audioDuration"]
    cortes = [it for it in tl if it["type"] == "cut"]
    usados = {}
    plano = []

    def numero_perto(t):
        return any(abs(s - t) < NUM_JANELA and (w in NUMEROS or w.isdigit()) for s, w in palavras)

    # --- hits e risers nos reveals
    ultimo_hit, n_reveal = -1e9, 0
    for bid, b in beats.items():
        if not b.get("reveal"):
            continue
        cs = [c for c in cortes if c.get("beat") == bid]
        t = None
        for c in cs:
            t0 = c["from"] / FPS
            if not numero_perto(t0):
                t = t0
                break
        if t is None:
            print(f"[sfx] reveal {bid}: todos os cortes começam em número falado — sem golpe")
            continue
        if t - ultimo_hit < GAP_HIT:
            print(f"[sfx] reveal {bid}: golpe anterior há {t - ultimo_hit:.0f} s — pulado")
            continue
        n_reveal += 1
        k = escolhe(pool, probe, "hit", ("sub bass", "boom", "deep impact"), (0.5, 7), usados)
        plano.append({"t": round(t, 3), "tipo": "hit", "key": k, "db": HIT_DB, "beat": bid})
        ultimo_hit = t
        if b.get("modo") == "climax" or n_reveal % 3 == 0:
            kr = escolhe(pool, probe, "riser", ("riser", "tension"), (2, 9), usados)
            dr = probe.get(kr, {}).get("dur_s", 4)
            plano.append({"t": round(max(0, t - dr), 3), "tipo": "riser", "key": kr, "db": RISER_DB, "beat": bid})

    # --- whoosh nas cartelas de capítulo em tela
    for c in cortes:
        ov = c.get("ov") or {}
        if ov.get("tipo") == "capitulo":
            k = escolhe(pool, probe, "whoosh", ("whoosh",), (0.3, 4), usados)
            plano.append({"t": round((c["from"] + ov.get("entra", 6)) / FPS - 0.15, 3), "tipo": "whoosh", "key": k, "db": WHOOSH_DB})

    # --- ambiência por slate (troca de lugar)
    slates = sorted((c["from"] / FPS for c in cortes if (c.get("ov") or {}).get("tipo") == "slate"))
    if not slates or slates[0] > 5:
        slates = [0.0] + slates
    # 28/09/2026: as palavras vinham fixas do filme do oceano e o Tutancâmon ganhou "Hard Rain Strong Winds" por baixo
    # do filme inteiro (o usuário ouviu "só vento"). Agora: termos do tema_config, sem chuva/tempestade, e
    # pipeline_config "ambiencia": false desliga a cama de ambiente.
    _cfg = json.loads((D / "pipeline_config.json").read_text("utf-8"))
    _tema = json.loads((D / "tema_config.json").read_text("utf-8")) if (D / "tema_config.json").exists() else {}
    _amb = tuple(w for x in (_tema.get("sfx_termos", {}).get("ambiencia") or ["ocean"]) for w in x.lower().split() if len(w) > 3)
    if _cfg.get("ambiencia") is False:
        slates = []
    for i, t in enumerate(slates):
        fim = slates[i + 1] if i + 1 < len(slates) else total
        _seco = {kk: vv for kk, vv in pool.items() if not any(r in str(vv.get("title", "")).lower() for r in ("rain", "storm", "thunder"))}
        k = escolhe(_seco, probe, "ambiencia", _amb, (8, 1e9), usados)
        plano.append({"t": round(t, 3), "tipo": "ambiencia", "key": k, "db": AMB_DB, "ate": round(fim, 3)})

    # --- diegéticos: sonar/estalos (cachalote, p089–p090), casco (pressão, p006), bolhas (trechos de ROV)
    def t_beat(bid):
        cs = [c for c in cortes if c.get("beat") == bid]
        return cs[0]["from"] / FPS if cs else None

    dieg = [("b090", ("sonar", "click", "whale"), 1.0), ("b006", ("hull", "creak"), 2.0), ("b092", ("whale", "click"), 1.0)]
    for bid, termos, atraso in dieg:
        t = t_beat(bid)
        k = escolhe(pool, probe, "diegetico", termos, (0.3, 20), usados)
        if t is not None and k:
            plano.append({"t": round(t + atraso, 3), "tipo": "diegetico", "key": k, "db": DIEG_DB, "beat": bid})
    rov = [c for c in cortes if "rov_lights" in beats.get(c.get("beat"), {}).get("tags", [])[:1]]
    ultimo = -1e9
    for c in rov:
        t = c["from"] / FPS
        if t - ultimo < 240:
            continue
        k = escolhe(pool, probe, "diegetico", ("bubble",), (0.5, 20), usados)
        if k:
            plano.append({"t": round(t + 0.5, 3), "tipo": "diegetico", "key": k, "db": DIEG_DB - 4, "beat": c.get("beat")})
            ultimo = t

    plano.sort(key=lambda e: e["t"])
    for e in plano:
        v = pool[e["key"]]
        e.update({"file": v["file"], "title": v["title"], "page": v["page"], "license": v["license"], "fonte": v["fonte"]})
    (D / "sfx_plan.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), "utf-8")
    conta = {}
    for e in plano:
        conta[e["tipo"]] = conta.get(e["tipo"], 0) + 1
    hits = [e["t"] for e in plano if e["tipo"] == "hit"]
    gaps = [b - a for a, b in zip(hits, hits[1:])]
    print(f"[sfx] {len(plano)} eventos {conta} | menor intervalo entre golpes {min(gaps) if gaps else 0:.0f} s -> data/sfx_plan.json")


if __name__ == "__main__":
    main()
