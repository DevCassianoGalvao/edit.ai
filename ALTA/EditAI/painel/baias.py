"""BAIAS — vários filmes ao mesmo tempo (28/09/2026, pedido do usuário).

Cada filme em produção ocupa uma BAIA = uma cópia de trabalho do projeto (data/, public/, out/, qa/, input/ próprios).
  b1 = a pasta principal (EditAI)
  b2, b3... = <pasta ALTA PRODUÇÃO>/baias/bN  (criadas na hora; ~1,2 GB cada: código + node_modules + música/efeitos)
Etapas leves correm juntas; render e transcrição passam pela trava (scripts/trava.py): um por vez.
O código (scripts/, src/, painel/*.py) é copiado da b1 para a baia quando um filme NOVO começa nela (`preparar`);
durante o filme a baia não é sincronizada (os arquivos do tema — beats, buscas, cenas, cartões — são daquele filme).

Uso (para o Claude):
  python painel/baias.py lista              # baias, caminho e qual filme ocupa cada uma
  python painel/baias.py livre              # nome da primeira baia livre (respeitando o limite "paralelo" do painel)
  python painel/baias.py preparar bN        # cria (se preciso) e copia o código atual da b1
  python painel/baias.py caminho bN
"""
import json, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRINCIPAL = HERE.parent
BASE = PRINCIPAL.parent / "baias"
CONFIG = HERE / "config.json"
sys.path.insert(0, str(HERE))

COPIA_FIXA = ["package.json", "package-lock.json", "tsconfig.json", "remotion.config.ts", "banned_videos.json", "cookies.txt"]
DIR_FIXOS = ["node_modules", "assets/music", "assets/sfx", "assets/fx", "public/fonts", "public/exemplos", "public/demo"]
DADOS_FIXOS = ["pipeline_config.json", "music_pool.json", "sfx_pool.json", "source_caps.json"]
CODIGO = ["scripts", "src"]
MAX_BAIAS = 2   # 05/10/2026: regra do usuário — 2 filmes ao mesmo tempo (um monta, o outro renderiza); 3 só gerou erro e disco cheio


def config():
    try:
        return {"paralelo": 1, "auto": False, **json.loads(CONFIG.read_text("utf-8"))}
    except Exception:  # noqa: BLE001
        return {"paralelo": 1, "auto": False}


def caminho(b):
    return PRINCIPAL if b == "b1" else BASE / b


def todas():
    n = max(2, min(MAX_BAIAS, config().get("paralelo", 1)))
    return [f"b{i}" for i in range(1, n + 1)]


def ocupacao():
    import fila
    oc = {}
    for p in fila.todos():
        if p.get("baia") and p.get("status") in ("produzindo", "esperando_voce", "pausado"):
            oc[p["baia"]] = p
    return oc


def livre():
    lim = max(1, min(MAX_BAIAS, int(config().get("paralelo", 1))))
    oc = ocupacao()
    return next((b for b in [f"b{i}" for i in range(1, lim + 1)] if b not in oc), "")


def _robocopy(src, dst, *extra):
    r = subprocess.run(["robocopy", str(src), str(dst), "/E", "/NFL", "/NDL", "/NJH", "/NJS", "/NP", "/R:1", "/W:1", *extra],
                       capture_output=True, text=True)
    if r.returncode >= 8:
        raise SystemExit(f"[baias] robocopy falhou ({r.returncode}) {src} -> {dst}")


def preparar(b):
    dst = caminho(b)
    if b == "b1":
        print(f"[baias] b1 = pasta principal ({dst})"); return dst
    nova = not dst.exists()
    dst.mkdir(parents=True, exist_ok=True)
    if nova:
        print(f"[baias] criando {b} em {dst} (~1,2 GB, uma vez só)…", flush=True)
        for d in DIR_FIXOS:
            if (PRINCIPAL / d).exists():
                _robocopy(PRINCIPAL / d, dst / d)
        for f in COPIA_FIXA:
            if (PRINCIPAL / f).exists():
                shutil.copy2(PRINCIPAL / f, dst / f)
        (dst / "data").mkdir(exist_ok=True)
        for f in DADOS_FIXOS:
            if (PRINCIPAL / "data" / f).exists():
                shutil.copy2(PRINCIPAL / "data" / f, dst / "data" / f)
        for d in ("input", "out", "qa", "entregas", "public/stock"):
            (dst / d).mkdir(parents=True, exist_ok=True)
    # 03/10/2026: o espelho abaixo APAGA o tema do filme anterior da baia (beats, CUES, cenas) antes de o novo_filme.py
    # guardá-lo em _decisoes_*; por isso o tema vai antes para _tema_<filme>/ (o novo_filme não sobrescreve o que já existe)
    if not nova and (dst / "scripts" / "beats.py").exists():
        import time as _t
        tema = dst / ("_tema_" + _t.strftime("%Y%m%d-%H%M%S"))
        (tema / "scripts").mkdir(parents=True, exist_ok=True)
        for f in list((dst / "scripts").glob("*.py")) + list((dst / "scripts").glob("*.bak*")):
            shutil.copy2(f, tema / "scripts" / f.name)
        for f in (dst / "src" / "scenes").glob("*.ts*"):
            shutil.copy2(f, tema / "scripts" / (f.name + ".txt"))
        print(f"[baias] tema anterior de {b} guardado em {tema.name}/")
    for d in CODIGO:   # código atual da b1 (espelho: o que foi apagado na b1 some aqui também)
        _robocopy(PRINCIPAL / d, dst / d, "/MIR", "/XD", "__pycache__")
    (dst / "painel").mkdir(exist_ok=True)
    for f in ("fila.py", "catalogo.py"):   # o fila.py da baia fala com a fila da b1 (painel/fila é uma só)
        shutil.copy2(HERE / f, dst / "painel" / f)
    print(f"[baias] {b} pronta: {dst}")
    return dst


def main():
    a = sys.argv[1:]
    if not a or a[0] == "lista":
        oc = ocupacao()
        lim = config().get("paralelo", 1)
        for b in todas():
            p = oc.get(b)
            print(f"{b}{' *' if int(b[1:]) <= lim else '  '} {'existe' if caminho(b).exists() else 'ainda não criada':16s} "
                  f"{(p['id'] + ' · ' + p['status']) if p else 'livre':50s} {caminho(b)}")
        print(f"(paralelo = {lim}; * = baias em uso pelo limite do painel)")
    elif a[0] == "livre":
        print(livre())
    elif a[0] == "preparar":
        preparar(a[1])
    elif a[0] == "caminho":
        print(caminho(a[1]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
