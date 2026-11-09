"""Transcreve input/audio16k.wav com faster-whisper (timestamps por palavra).
Tenta GPU (large-v3 int8_float16); se falhar, cai para CPU (medium int8).
Saída: data/whisper_raw.json

21/09/2026: a GPU caía sempre com "cublas64_12.dll is not found". As DLLs do CUDA vêm nos pacotes
nvidia-cublas-cu12 / nvidia-cudnn-cu12, mas no Windows elas ficam em site-packages/nvidia/*/bin, que NÃO está
no PATH. cuda_dlls() registra essas pastas antes de importar o faster-whisper — sem isso o filme inteiro
transcreve em CPU (35-50 min em vez de 3-6 min)."""
import glob, json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAV = ROOT / "data" / "audio16k.wav"
OUT = ROOT / "data" / "whisper_raw.json"
LANG = sys.argv[1] if len(sys.argv) > 1 else "en"  # idioma da narração: python transcribe.py en|es|pt


def cuda_dlls():
    """Põe as pastas bin/ dos pacotes nvidia-* no caminho de DLL do processo (Windows)."""
    try:
        import nvidia  # noqa: PLC0415
    except ImportError:
        return []
    achadas = []
    for b in sorted(glob.glob(os.path.join(list(nvidia.__path__)[0], "*", "bin"))):
        if not any(f.lower().endswith(".dll") for f in os.listdir(b)):
            continue
        achadas.append(b)
        os.environ["PATH"] = b + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):  # Windows + Python >= 3.8
            os.add_dll_directory(b)
    return achadas


_dirs = cuda_dlls()
print(f"[transcribe] CUDA dlls: {len(_dirs)} pasta(s)" + (f" ({os.path.basename(os.path.dirname(_dirs[0]))}...)" if _dirs else " — só CPU"), flush=True)


def run(model_name, device, compute):
    from faster_whisper import WhisperModel
    print(f"[transcribe] {model_name} {device} {compute}", flush=True)
    model = WhisperModel(model_name, device=device, compute_type=compute)
    # Decodifica no FFmpeg para evitar incompatibilidade do faster-whisper com PyAV 19.
    import numpy as np, subprocess
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", str(WAV), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True)
    segs, info = model.transcribe(np.frombuffer(decoded.stdout, dtype=np.float32), language=LANG, word_timestamps=True,
                                  beam_size=5, vad_filter=False,
                                  condition_on_previous_text=False)  # 26/09: com contexto alucinou 4 paragrafos (SunCable)
    out, t0 = [], time.time()
    for s in segs:
        out.append({"start": s.start, "end": s.end, "text": s.text,
                    "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability}
                              for w in (s.words or [])]})
        print(f"[transcribe] {s.end:8.1f}s / {info.duration:.0f}s  ({time.time()-t0:.0f}s elapsed)", flush=True)
    return {"model": model_name, "device": device, "duration": info.duration, "segments": out}


# A RTX 2050 tem 4 GB: large-v3 em int8_float16 cabe (~2,5 GB). Se faltar VRAM, tenta large-v3 int8 e
# depois medium na GPU; a CPU fica como último recurso.
CFGS = [("large-v3", "cuda", "int8_float16"), ("large-v3", "cuda", "int8"),
        ("medium", "cuda", "int8_float16"), ("medium", "cpu", "int8")]
if os.environ.get("TRANSCRIBE_SEM_CPU"):   # 04/10: rodando junto com um render — CPU derrubaria o render
    CFGS = [c for c in CFGS if c[1] != "cpu"]
for cfg in CFGS:
    try:
        res = run(*cfg)
        OUT.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
        print("[transcribe] DONE", OUT, flush=True)
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"[transcribe] falhou {cfg}: {e!r}", flush=True)
sys.exit(3 if os.environ.get("TRANSCRIBE_SEM_CPU") else 1)
