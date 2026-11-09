"""Folha de contato do FILME montado (juiz único antes de exportar).

Amostra 1 quadro por item da timeline, empurrado para o MIOLO do plano (margem de 20 quadros),
nunca dentro de fade/transição. Renderiza pelo Remotion (stills.mjs) — o mesmo caminho do render.
Modo --changed: compara o hash de cada item com a rodada anterior (qa/sheet_state.json) e só
monta folha do que mudou (o renderizador é determinístico).

Uso: python clip_sheet.py OUTDIR [--changed] [--from F --to F]
Saída: OUTDIR/film_NN.jpg (grade 6x5 = 30 itens por folha, rótulo = id, clipe, tag do beat)
"""
import hashlib, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
MARGIN = 20
COLS, ROWS, TW, TH = 6, 5, 480, 270
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)


def item_hash(it):
    keys = ("type", "from", "dur", "src", "trimBefore", "move", "scene", "fadeIn", "tail", "cues")
    return hashlib.md5(json.dumps({k: it.get(k) for k in keys}, sort_keys=True).encode()).hexdigest()


def sample_frame(it):
    lo = it["from"] + max(MARGIN, it.get("fadeIn", 0) + 4)
    hi = it["from"] + it["dur"] - MARGIN
    if hi <= lo:
        return it["from"] + it["dur"] // 2
    return (lo + hi) // 2


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    items = json.loads((D / "timeline.json").read_text("utf-8"))["items"]
    beats = {b["id"]: b for b in json.loads((D / "beats.json").read_text("utf-8"))["beats"]}
    state_p = ROOT / "qa" / "sheet_state.json"
    prev = json.loads(state_p.read_text("utf-8")) if state_p.exists() else {}
    f0 = int(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0
    f1 = int(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else 10 ** 9
    sel = [it for it in items if f0 <= it["from"] < f1]
    if "--changed" in sys.argv:
        sel = [it for it in sel if prev.get(it["id"]) != item_hash(it)]
    if "--unlocked" in sys.argv:  # todo corte ainda não travado (independe do estado da rodada anterior)
        locks = json.loads((D / "image_locks.json").read_text("utf-8")) if (D / "image_locks.json").exists() else {}
        sel = [it for it in sel if it["type"] == "cut" and locks.get(it["id"]) != it.get("clip")]
    print(f"[sheet] {len(sel)} itens", flush=True)
    if not sel:
        return
    jobs = [{"comp": "Main", "frame": sample_frame(it), "out": f"qa/_frames/{it['id']}.jpg", "scale": 0.25} for it in sel]
    # --resume: reaproveita qa/_frames da MESMA rodada interrompida (nunca entre rodadas: o quadro pode ter mudado)
    (ROOT / "qa" / "jobs_sheet.json").write_text(json.dumps({"jobs": jobs, "resume": "--resume" in sys.argv}), "utf-8")
    r = subprocess.run(["node", str(ROOT / "scripts" / "stills.mjs"), str(ROOT / "qa" / "jobs_sheet.json")], cwd=ROOT)
    if r.returncode != 0:
        sys.exit("stills.mjs falhou")
    per = COLS * ROWS
    for si in range(0, len(sel), per):
        sheet = Image.new("RGB", (COLS * TW, ROWS * (TH + 26)), (18, 18, 18))
        dr = ImageDraw.Draw(sheet)
        for k, it in enumerate(sel[si:si + per]):
            x, y = (k % COLS) * TW, (k // COLS) * (TH + 26)
            fp = ROOT / "qa" / "_frames" / f"{it['id']}.jpg"
            if fp.exists():
                sheet.paste(Image.open(fp).resize((TW, TH)), (x, y + 26))
            tag = beats[it["beat"]]["tags"][0] if it.get("beat") in beats else ""
            label = f"{it['id']} {it.get('clip') or it.get('scene', '')} {'FOTO ' if it.get('kind') == 'photo' else ''}[{tag}] {sample_frame(it) / 30:.0f}s"
            dr.text((x + 4, y + 4), label[:52], fill=(255, 220, 0), font=FONT)
        p = out / f"film_{si // per:02d}.jpg"
        sheet.save(p, quality=80)
        print("[sheet]", p, flush=True)
    for it in sel:
        prev[it["id"]] = item_hash(it)
    state_p.write_text(json.dumps(prev), "utf-8")


if __name__ == "__main__":
    main()
