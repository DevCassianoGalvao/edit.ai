"""VIGIA dos eventos do painel — o Claude roda isto dentro do Monitor: cada clique no painel (novo filme, continuar,
recado, analisar estilo) vira UMA linha aqui, e cada linha chega ao Claude como notificação, na hora.

Guarda até onde já avisou em painel/.vigia_cursor (não repete evento depois de reiniciar) e grava um sinal de vida
em painel/.vigia_vivo a cada 5 s — o painel mostra "Claude conectado" enquanto ele estiver fresco.

Uso: python painel/vigia.py [--desde-inicio]
"""
import json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE / "eventos.jsonl"
CUR = HERE / ".vigia_cursor"
VIVO = HERE / ".vigia_vivo"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass


def main():
    visto = 0 if "--desde-inicio" in sys.argv else int(CUR.read_text() or 0) if CUR.exists() else 0
    print(f"[vigia] ligado — eventos a partir do nº {visto + 1}", flush=True)
    ult_vivo = 0
    while True:
        if time.time() - ult_vivo > 5:
            VIVO.write_text(str(time.time()))
            ult_vivo = time.time()
        if EV.exists():
            for linha in EV.read_text("utf-8").splitlines():
                try:
                    e = json.loads(linha)
                except Exception:  # noqa: BLE001
                    continue
                if e.get("n", 0) > visto:
                    print("EVENTO " + json.dumps(e, ensure_ascii=False), flush=True)
                    visto = e["n"]
                    CUR.write_text(str(visto))
        time.sleep(1.5)


if __name__ == "__main__":
    main()
