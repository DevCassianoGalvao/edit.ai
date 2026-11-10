"""LEIA-ME da entrega gerado dos DADOS do filme — 04/10/2026 (eu escrevia à mão, ~10 min por filme).

Junta: duração do MP4, áudio (data/audio_qa.json), vídeo/foto (data/build_plan_report.md), animações (CUES do
build_plan + kicker das cenas), cartões e 2.5D (timeline.json), miniaturas da pasta, capítulos (qa/chapters.md com
os nomes do beats.py) e trilha. O que é de JULGAMENTO (o que saiu na conferência, pontos fracos) vem de
data/notas_entrega.md, que eu escrevo durante a conferência; sem ele, a seção fica de fora.

Uso: python leiame.py <pasta de entrega> "<título>"      (o fechar.py entregar chama sozinho)
"""
import json, re, subprocess, sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
dest, titulo = Path(sys.argv[1]), sys.argv[2]
J = lambda p, d=None: json.loads(p.read_text("utf-8")) if p.exists() else d
cfg = J(D / "pipeline_config.json", {})
lang = str(cfg.get("screenLanguage", "pt"))[:2]
mp4 = next(dest.glob("*.mp4"), None)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                           capture_output=True, text=True).stdout or 0) if mp4 else 0
aq = J(D / "audio_qa.json", {})
rep = (D / "build_plan_report.md").read_text("utf-8") if (D / "build_plan_report.md").exists() else ""
vid = re.search(r"vídeo% ([\d.]+)", rep)
vid = float(vid.group(1)) if vid else None
tl = J(D / "timeline.json", {"items": []})["items"]
ovs = Counter(it["ov"]["tipo"] for it in tl if it.get("ov"))
PAPEL = {"cartao", "comparacao", "fichas", "palavra", "quadro", "checklist", "ficha", "manchete", "teletipo", "lupa",
         "antesdepois", "rolo", "revela"}
n_papel = sum(v for k, v in ovs.items() if k in PAPEL)
arq = [k for k in ("quadro", "checklist", "ficha", "manchete", "teletipo", "lupa", "antesdepois", "rolo", "revela") if ovs.get(k)]
# animações: id da cena + kicker do .tsx
anims = [it["scene"] for it in tl if it.get("type") == "animation"]
cena = next((l.split('"./')[1].split('"')[0] for l in (ROOT / "src/scenes/index.ts").read_text("utf-8").splitlines()
             if 'from "./' in l and "Scenes" in l), None)
kick = {}
if cena and (ROOT / "src/scenes" / f"{cena}.tsx").exists():
    src = (ROOT / "src/scenes" / f"{cena}.tsx").read_text("utf-8")
    for bloco in re.split(r"\nexport const ", src)[1:]:
        nome = bloco.split(":")[0].strip()
        k = re.search(r'kicker[=:]\s*["`]([^"`]+)', bloco) or re.search(r'titulo:\s*["`]([^"`]+)', bloco)
        kick[nome] = k.group(1).replace("${NB}", " ") if k else ""
cap = (ROOT / "qa/chapters.md").read_text("utf-8").strip().splitlines() if (ROOT / "qa/chapters.md").exists() else []
beats = J(D / "beats.json", {}).get("beats", [])
nomes = [b["capitulo"].capitalize() for b in beats if b.get("capitulo")]
if cap and len(nomes) == len(cap):   # chapters.md vem em Title Case; o nome do beats.py lê melhor (só 1ª maiúscula)
    cap = [f"{l.split()[0]} {n[0]}{n[1:].lower()}" for l, n in zip(cap, nomes)]
thumbs = sorted(p.stem for p in (dest / "miniaturas").glob("*.jpg") if not p.stem.startswith("_"))
notas = (D / "notas_entrega.md").read_text("utf-8").strip() if (D / "notas_entrega.md").exists() else ""
mm = lambda s: f"{int(s // 60)}:{int(s % 60):02d}"
L = [f"# {titulo} ({lang}) — {date.today().strftime('%d/%m/%Y')}\n",
     f"- **Vídeo:** {mm(dur)}, 1080p, render {cfg.get('render', {}).get('qualidade', 'alta')}, estilo {J(D / 'pipeline_config.json', {}).get('estilo', 'arquivo-dark')}.",
     "- **Som:** " + ("sem trilha e sem efeitos." if cfg.get("music") is False else "trilha e efeitos conforme o pedido.")
     + (f" Áudio a {aq.get('I')} LUFS, pico {aq.get('TP')} dBTP, {len(aq.get('fails', []))} falhas / {len(aq.get('warns', []))} avisos." if aq else ""),
     "- **Motion graphics curtos:** cada animação entra até 1 s antes do número e sai no fim da frase.",
     (f"- **Material:** {vid:.0f} % vídeo / {100 - vid:.0f} % foto." if vid is not None else "")]
if anims:
    L.append(f"- **Animações ({len(anims)}):** " + "; ".join(f"{a.split('-', 1)[1] if '-' in a else a}"
             + (f" ({kick.get(a.replace('-', ''), '')})" if kick.get(a.replace('-', '')) else "") for a in anims) + ".")
L.append(f"- **Cartões:** {n_papel} em papel e de arquivo ({', '.join(arq)}), {ovs.get('paralaxe', 0)} fotos em 2.5D.")
if thumbs:
    L.append(f"- **Miniaturas ({len(thumbs)}):** {', '.join(thumbs)} — todo número delas é dito na narração.")
if notas:
    L += ["", notas]
if cap:
    L += ["", "## Capítulos (colar na descrição)"] + cap
L += ["", "Créditos das fotos e vídeos: relatorios/attribution.md."]
(dest / "LEIA-ME.md").write_text("\n".join(l for l in L if l is not None), "utf-8")
print(f"[leiame] {dest / 'LEIA-ME.md'}")
