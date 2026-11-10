"""Cria uma cama instrumental simples no computador e a cadastra no pool de música.

Uso: python scripts/trilha_local.py --clima calma --duracao 72
Não usa API, amostras de terceiros nem modelos de geração musical.
"""
import argparse
import json
import shutil
import subprocess
import uuid
import wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
POOL = DATA / "music_pool.json"
DIR = ROOT / "assets" / "music" / "geradas"
SR = 22050
HARMONIAS = {
    "calma": ([48, 45, 41, 43], (0, 4, 7)),
    "alegre": ([48, 43, 45, 41], (0, 4, 7)),
    "tensao": ([45, 41, 48, 43], (0, 3, 7)),
    "neutro": ([48, 45, 41, 43], (0, 4, 7)),
}
CLIMAS = {"calma": "alivio", "alegre": "alivio", "tensao": "tensao", "neutro": "cama"}


def sintetizar(clima, duracao):
    """Acordes suaves com notas espaçadas e fades; resultado é uma cama, não uma canção completa."""
    notas, intervalos = HARMONIAS[clima]
    n = int(duracao * SR)
    audio = np.zeros(n, dtype=np.float32)
    passo = int((6 if clima == "alegre" else 8) * SR)
    fade = int(1.4 * SR)
    for i, inicio in enumerate(range(0, n, passo)):
        comprimento = min(passo + fade, n - inicio)
        t = np.arange(comprimento, dtype=np.float32) / SR
        env = np.minimum(np.minimum(t / 1.4, (comprimento / SR - t) / 1.4), 1.0)
        env = np.clip(env, 0, 1)
        bloco = np.zeros(comprimento, dtype=np.float32)
        raiz = notas[i % len(notas)]
        for grau in intervalos:
            freq = 440.0 * 2 ** ((raiz + grau - 69) / 12)
            bloco += np.sin(2 * np.pi * freq * t) * 0.035
            bloco += np.sin(2 * np.pi * freq * 2 * t) * 0.006
        audio[inicio:inicio + comprimento] += bloco * env
        # Nota curta, pouco presente, para dar ritmo sem competir com a voz.
        freq = 440.0 * 2 ** ((raiz + 12 + intervalsafe(i, intervalos) - 69) / 12)
        pulso = np.exp(-t * (1.8 if clima == "alegre" else 1.2))
        ataque = np.minimum(t / 0.04, 1.0)
        audio[inicio:inicio + comprimento] += 0.035 * np.sin(2 * np.pi * freq * t) * pulso * ataque
    # Fades no início e fim para evitar cliques na montagem.
    f = min(int(2 * SR), n // 2)
    audio[:f] *= np.linspace(0, 1, f, dtype=np.float32)
    audio[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
    return np.clip(audio, -0.9, 0.9)


def intervalsafe(i, intervalos):
    return intervalos[i % len(intervalos)]


def criar(clima, duracao):
    if clima not in HARMONIAS or not 45 <= duracao <= 180:
        raise ValueError("Clima inválido ou duração fora de 45 a 180 segundos")
    DATA.mkdir(parents=True, exist_ok=True)
    DIR.mkdir(parents=True, exist_ok=True)
    chave = "local_" + uuid.uuid4().hex[:12]
    arquivo = DIR / (chave + ".wav")
    audio = sintetizar(clima, duracao)
    with wave.open(str(arquivo), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes((audio * 32767).astype("<i2").tobytes())
    registrar(chave, arquivo, clima, duracao, "Composição sintetizada localmente")
    return chave


def registrar(chave, arquivo, clima, duracao, origem):
    try:
        pool = json.loads(POOL.read_text("utf-8")) if POOL.exists() else {}
        pool[chave] = {"file": arquivo.relative_to(ROOT).as_posix(), "title": "Trilha local — " + clima,
            "license": origem, "page": "", "fonte": "Edit.AI local",
            "termo": clima, "dur_s": duracao, "clima": CLIMAS[clima], "clima_fixo": CLIMAS[clima],
            "reserva": False}
        tmp = POOL.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(pool, ensure_ascii=False, indent=1), "utf-8")
        tmp.replace(POOL)
    except Exception:
        arquivo.unlink(missing_ok=True)
        raise


def importar(entrada, clima):
    """Cadastra uma composição original criada no projeto por ferramenta local."""
    entrada = Path(entrada).resolve()
    if clima not in HARMONIAS or not entrada.is_file() or entrada.suffix.lower() not in (".wav", ".mp3", ".m4a", ".ogg", ".flac"):
        raise ValueError("Arquivo ou clima inválido")
    if entrada.stat().st_size > 100 * 1024 * 1024:
        raise ValueError("Arquivo de áudio excede 100 MB")
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                            "format=duration", "-of", "default=nw=1:nk=1", str(entrada)],
                           capture_output=True, text=True, timeout=30, check=True)
    duracao = float(probe.stdout.strip())
    if not 40 <= duracao <= 3600:
        raise ValueError("A composição deve ter entre 40 segundos e uma hora")
    DATA.mkdir(parents=True, exist_ok=True)
    DIR.mkdir(parents=True, exist_ok=True)
    chave = "local_" + uuid.uuid4().hex[:12]
    arquivo = DIR / (chave + entrada.suffix.lower())
    shutil.copy2(entrada, arquivo)
    registrar(chave, arquivo, clima, duracao, "Composição própria informada pelo projeto")
    return chave


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clima", choices=HARMONIAS, default="neutro")
    parser.add_argument("--duracao", type=int, default=72)
    parser.add_argument("--importar", help="arquivo de composição original criado localmente")
    args = parser.parse_args()
    chave = importar(args.importar, args.clima) if args.importar else criar(args.clima, args.duracao)
    print(f"[trilha local] {chave} cadastrada ({args.clima})")


if __name__ == "__main__":
    main()
