"""Reaproveita os segmentos JÁ RENDERIZADOS quando o plano do render híbrido muda de recorte.

Para que serve: o nome do segmento é sNNN_motor_quadro. Basta um corte mudar de motor (por exemplo, ganhar
motion graphic e sair do ffmpeg para o Remotion) para o índice NNN de TODOS os segmentos seguintes andar —
e aí o render acha que está tudo faltando e refaz o filme inteiro. Este passo renomeia o arquivo antigo para
o nome novo quando o trecho é o MESMO (mesmo motor, mesmo início, mesmo fim).

A armadilha (custou um render errado no filme do Mar Morto): trecho com o mesmo recorte pode ter CONTEÚDO
diferente — foi o caso dos rótulos de lugar, que entraram em cortes de foto cujos segmentos não mudaram de
recorte nenhum. Por isso todo segmento que toca um item MUDADO é apagado, nunca reaproveitado.

Uso:
  cp out/hybrid/plan.json out/hybrid/plan_antes.json
  python scripts/render_hybrid.py --plan-only
  python scripts/remap_hybrid.py [timeline_antes.json]
  python scripts/render_hybrid.py --out out/final.mp4
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HY = ROOT / "out" / "hybrid"
D = ROOT / "data"
CHAVES = ("kind", "src", "dur", "trimBefore", "move", "scene", "fadeIn", "tail", "cues", "ov")


def main():
    antes_p, novo_p = HY / "plan_antes.json", HY / "plan.json"
    if not (antes_p.exists() and novo_p.exists()):
        raise SystemExit("faltam out/hybrid/plan_antes.json e plan.json (rode render_hybrid.py --plan-only antes)")
    antes = json.loads(antes_p.read_text("utf-8"))["segments"]
    novo = json.loads(novo_p.read_text("utf-8"))["segments"]

    # quadros dos itens que MUDARAM de conteúdo (comparando com uma timeline anterior, se houver)
    mudados = []
    tl_antes = Path(sys.argv[1]) if len(sys.argv) > 1 else D / "timeline_antes.json"
    itens_novos = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    if tl_antes.exists():
        velhos = {x["id"]: x for x in json.loads(tl_antes.read_text("utf-8"))["items"]}
        for it in itens_novos:
            v = velhos.get(it["id"])
            if v is None or any(v.get(k) != it.get(k) for k in CHAVES):
                mudados.append((it["from"], it["from"] + it["dur"]))
    else:
        print("[remap] sem timeline anterior: só os itens COM sobreposição entram como mudados")
        mudados = [(it["from"], it["from"] + it["dur"]) for it in itens_novos if it.get("ov")]

    por_chave = {(s["engine"], s["start"], s["end"]): s for s in antes}
    reaproveitado = refazer = 0
    for s in novo:
        pn = Path(s["file"])
        toca_mudado = any(s["start"] < b and a < s["end"] for a, b in mudados)
        if toca_mudado:
            if pn.exists():
                pn.unlink()
            v = por_chave.get((s["engine"], s["start"], s["end"]))
            if v and Path(v["file"]).exists():
                Path(v["file"]).unlink()
            refazer += 1
            continue
        if pn.exists():
            reaproveitado += 1
            continue
        v = por_chave.get((s["engine"], s["start"], s["end"]))
        if v and Path(v["file"]).exists():
            Path(v["file"]).rename(pn)
            reaproveitado += 1
        else:
            refazer += 1

    nomes = {Path(s["file"]).name for s in novo}
    sobra = 0
    for p in HY.glob("s*.mp4"):
        if p.name not in nomes:
            p.unlink()
            sobra += 1
    print(f"[remap] {len(novo)} segmentos | reaproveitados {reaproveitado} | a refazer {refazer} | "
          f"apagados por não servirem mais {sobra} | itens mudados {len(mudados)}")


if __name__ == "__main__":
    main()
