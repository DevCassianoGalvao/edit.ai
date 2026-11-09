"""PACOTE DE PUBLICAÇÃO (28/09/2026, painel: extra "Pacote de publicação") -> out/publicacao.md

O Claude escreve data/publicacao.json no fim do filme (ele conhece o roteiro e o que entrou na tela):
  {"titulos": ["...", ... 5 opções, <= 70 caracteres, com o número forte da miniatura],
   "descricao": "2-3 parágrafos: gancho + o que o vídeo mostra (sem spoiler do fim)",
   "tags": ["...", ...], "hashtags": ["#...", "#...", "#..."]}
Este script junta com os capítulos (qa/chapters.md), os créditos das imagens/músicas (data/attribution.md, resumo) e
os Shorts (out/shorts/shorts.md, se houver) num arquivo pronto para colar no YouTube.

Uso: python publicacao.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def main():
    p = D / "publicacao.json"
    if not p.exists():
        raise SystemExit("[publicacao] falta data/publicacao.json (o Claude escreve títulos, descrição e tags)")
    pub = json.loads(p.read_text("utf-8"))
    caps = (ROOT / "qa" / "chapters.md").read_text("utf-8").strip() if (ROOT / "qa" / "chapters.md").exists() else ""
    att = (D / "attribution.md").read_text("utf-8") if (D / "attribution.md").exists() else ""
    autores = sorted(set(re.findall(r"\|\s*([^|]{2,60}?)\s*\|\s*(?:CC|Public|PD|Pexels|Pixabay)", att)))[:40]
    linhas = ["# Pacote de publicação", "", "## Títulos (escolha um)"]
    linhas += [f"{i}. {t}  ({len(t)} caracteres)" for i, t in enumerate(pub.get("titulos", []), 1)]
    linhas += ["", "## Descrição (colar no YouTube)", "", "```", pub.get("descricao", "").strip(), "",
               "CAPÍTULOS", caps, "",
               "Imagens e vídeos: Wikimedia Commons (licenças livres), Pexels, Pixabay e trechos com autorização de uso "
               "justo; créditos completos no arquivo de atribuição." + (f" Autores: {', '.join(autores)}." if autores else ""),
               "", " ".join(pub.get("hashtags", [])), "```", "",
               "## Tags", "", ", ".join(pub.get("tags", []))]
    sh = ROOT / "out" / "shorts" / "shorts.md"
    if sh.exists():
        linhas += ["", sh.read_text("utf-8").replace("# Shorts 9:16", "## Shorts 9:16")]
    out = ROOT / "out" / "publicacao.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(linhas) + "\n", "utf-8")
    print(f"[publicacao] {out.relative_to(ROOT)} — {len(pub.get('titulos', []))} títulos, {len(pub.get('tags', []))} tags")


if __name__ == "__main__":
    main()
