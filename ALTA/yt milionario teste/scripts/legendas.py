"""LEGENDAS queimadas no vídeo (.ass) + arquivo .srt para subir no YouTube — 27/09/2026 (painel, pedido do usuário).

Lê as palavras com tempo do Whisper (data/master_transcript.json -> sentences[].words) e escreve:
  data/legendas.ass   estilo escolhido no pipeline_config "legendas": {"estilo": ..., "posicao": ..., "tamanho": ...}
  out/legendas.srt    sempre (texto limpo, 1-2 linhas, para o upload no YouTube — ajuda busca e retenção)
O acabamento.py queima o .ass na mesma codificação final (sem recodificar o filme duas vezes).

Estilos (as prévias do painel saem deste mesmo arquivo — painel/gera_previas.py):
  classica      branco, contorno preto fino, 1 linha no rodapé (Arial)
  documentario  máquina de escrever (Courier New), caixa alta pequena, fundo escurecido — combina com o arquivo dark
  karaoke       palavra falada acende em amarelo, as outras brancas (Arial Black) — retenção alta
  caixa         texto branco sobre tarja preta sólida (estilo TV/Netflix acessível)
  impacto       2-3 palavras por vez, Anton grande no centro-baixo, maiúsculas (estilo shorts/true crime)
  minimal       pequeno, cinza claro, sem contorno pesado — discreto
  serifa        Garamond pequena creme com sombra suave, frase inteira no rodapé (documentário de história)

Uso: python legendas.py [--estilo X] [--saida data/legendas.ass] [--demo "texto de exemplo"]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
ESTILOS = ["classica", "documentario", "karaoke", "caixa", "impacto", "minimal", "serifa", "turquesa", "alto_contraste"]
AMARELO = "&H0038C8FF"   # BGR do ASS: dourado da casa (#FFC838)


def _cfg():
    p = D / "pipeline_config.json"
    return (json.loads(p.read_text("utf-8")).get("legendas") or {}) if p.exists() else {}


def _familia_serifa():
    """06/11/2026: o nome da família vem de DENTRO de public/fonts/Garamond.ttf — no PC do dono é a Garamond do Windows
    ("Garamond"); no pacote de venda o arquivo é a EB Garamond livre ("EB Garamond"). O libass procura pelo nome."""
    try:
        from PIL import ImageFont
        return ImageFont.truetype(str(ROOT / "public" / "fonts" / "Garamond.ttf"), 20).getname()[0] or "Garamond"
    except Exception:  # noqa: BLE001
        return "Garamond"


def estilo_ass(nome, posicao="baixo", tamanho="m"):
    k = {"p": 0.82, "m": 1.0, "g": 1.2}.get(tamanho, 1.0)
    mv = 70 if posicao == "baixo" else 470
    base = {  # Fontname, Fontsize, Primary, Outline, Back, Bold, BorderStyle, Outline, Shadow, Spacing
        "turquesa": ("Segoe UI Semibold", 52, "&H00CBEA63", "&H00000000", "&H96000000", -1, 1, 3.2, 1.3, 0),
        "alto_contraste": ("Arial", 58, "&H00FFFFFF", "&H00000000", "&H00000000", -1, 3, 14, 0, 0),
        "classica": ("Arial", 54, "&H00FFFFFF", "&H00000000", "&H96000000", -1, 1, 3.2, 1.2, 0),
        "documentario": ("Courier New", 46, "&H00F0F0F0", "&H00101010", "&H78000000", -1, 3, 10, 0, 1.5),
        "karaoke": ("Arial Black", 58, "&H00FFFFFF", "&H00000000", "&H96000000", 0, 1, 4.2, 1.5, 0),
        "caixa": ("Arial", 50, "&H00FFFFFF", "&H00000000", "&H00000000", -1, 3, 12, 0, 0),
        "impacto": ("Anton", 96, "&H00FFFFFF", "&H00000000", "&H96000000", 0, 1, 5.5, 2.5, 1),
        "minimal": ("Segoe UI Semibold", 44, "&H00F4F4F4", "&H50000000", "&H78000000", 0, 1, 1.6, 1.2, 0.5),
        # 04/11/2026 estilo Arquivo Colorizado: Garamond pequena, creme, sombra suave, sem caixa (public/fonts/Garamond.ttf)
        "serifa": (_familia_serifa() if nome == "serifa" else "Garamond", 40, "&H00DCEAF0", "&H64000000", "&H8C000000", 0, 1, 0.9, 1.6, 0.4),
    }[nome]
    f, s, pc, oc, bc, b, bs, o, sh, sp = base
    if nome == "impacto" and posicao == "baixo":
        mv = 150
    return (f"Style: L,{f},{round(s * k)},{pc},{AMARELO},{oc},{bc},{b},0,0,0,100,100,{sp},0,{bs},{o},{sh},2,120,120,{mv},1")


def blocos(words, nome):
    """Agrupa palavras em legendas: quebra em pausa > 0,55 s, fim de frase ou limite de caracteres/palavras."""
    maxc, maxw = {"impacto": (18, 3), "documentario": (40, 8), "minimal": (48, 10), "serifa": (62, 12)}.get(nome, (42, 8))
    out, cur = [], []
    for w in words:
        t = w["w"].strip()
        if not t:
            continue
        if cur and (w["s"] - cur[-1]["e"] > 0.55 or len(" ".join(x["w"] for x in cur + [w])) > maxc or len(cur) >= maxw):
            # não termina a linha num artigo/preposição curta ("deixou o" | "estaleiro"): leva a palavrinha junto
            leva = [cur.pop()] if len(cur) > 2 and len(cur[-1]["w"]) <= 3 and not re.search(r"[.,;:!?]$", cur[-1]["w"]) else []
            out.append(cur)
            cur = leva
        cur.append({"w": t, "s": w["s"], "e": w["e"]})
        if re.search(r"[.!?…]$", t):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def ts_ass(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ts_srt(t):
    t = max(0.0, t)
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"


def esc(s):
    return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def gera_ass(words, nome, posicao="baixo", tamanho="m"):
    linhas = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0",
              "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
              "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
              "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
              "MarginL, MarginR, MarginV, Encoding", estilo_ass(nome, posicao, tamanho), "", "[Events]",
              "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    bl = blocos(words, nome)
    for k, b in enumerate(bl):
        a = b[0]["s"]
        z = min(b[-1]["e"] + 0.25, bl[k + 1][0]["s"] if k + 1 < len(bl) else b[-1]["e"] + 0.25)
        up = nome in ("impacto", "documentario")
        tx = lambda w: esc(w["w"].upper() if up else w["w"])
        if nome == "karaoke":   # um evento por palavra: a palavra falada acende
            for i, w in enumerate(b):
                fim = b[i + 1]["s"] if i + 1 < len(b) else z
                txt = " ".join((f"{{\\c{AMARELO}}}{tx(x)}{{\\c&H00FFFFFF&}}" if j == i else tx(x)) for j, x in enumerate(b))
                linhas.append(f"Dialogue: 0,{ts_ass(w['s'] if i else a)},{ts_ass(fim)},L,,0,0,0,,{txt}")
        else:
            pre = "{\\fad(90,60)}" if nome in ("impacto", "minimal") else ""
            linhas.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(z)},L,,0,0,0,,{pre}{' '.join(tx(w) for w in b)}")
    return "\n".join(linhas) + "\n"


def gera_srt(words):
    out = []
    for k, b in enumerate(blocos(words, "classica"), 1):
        out.append(f"{k}\n{ts_srt(b[0]['s'])} --> {ts_srt(b[-1]['e'] + 0.2)}\n{' '.join(w['w'] for w in b)}\n")
    return "\n".join(out)


def palavras():
    mt = json.loads((D / "master_transcript.json").read_text("utf-8"))
    ws = [{"w": w["w"], "s": w["s"], "e": w["e"]} for s in mt["sentences"] for w in s.get("words", [])]
    # o Whisper parte o milhar ("1" + ".360", "2" + ",000") — na tela tem de sair "1.360" (filme car-pt, 28/09)
    out = []
    for w in ws:
        if out and re.fullmatch(r"\d{1,3}", out[-1]["w"].strip()) and re.match(r"[.,]\d{3}", w["w"].strip()):
            out[-1] = {"w": out[-1]["w"].strip() + w["w"].strip(), "s": out[-1]["s"], "e": w["e"]}
        # 28/09/2026 (T-37): o Whisper separa o hífen de modelo — "T" + "-37", "MiG" + "-25", "tierra" + "-aire"
        elif out and re.match(r"-[\w]", w["w"].strip()) and not out[-1]["w"].strip().endswith((".", ",", ";", ":")):
            out[-1] = {"w": out[-1]["w"].strip() + w["w"].strip(), "s": out[-1]["s"], "e": w["e"]}
        else:
            out.append(w)
    # grafia do ROTEIRO para nomes que o Whisper escreve de ouvido: data/legendas_grafia.json {"Suhoi": "Sujói"}
    gp = D / "legendas_grafia.json"
    if gp.exists():
        g = json.loads(gp.read_text("utf-8"))
        for w in out:
            nu = w["w"].strip()
            core = nu.strip(".,;:!?¿¡")
            if core in g:
                w["w"] = w["w"].replace(core, g[core])
    return out


def demo_words(texto, t0=0.2, passo=0.32):
    return [{"w": w, "s": t0 + i * passo, "e": t0 + (i + 1) * passo - 0.04} for i, w in enumerate(texto.split())]


def main():
    a = sys.argv[1:]
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    cfg = _cfg()
    nome = op("--estilo", cfg.get("estilo", "classica"))
    if nome not in ESTILOS:
        sys.exit(f"estilo desconhecido: {nome} ({', '.join(ESTILOS)})")
    words = demo_words(op("--demo")) if "--demo" in a else palavras()
    saida = ROOT / op("--saida", "data/legendas.ass")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(gera_ass(words, nome, cfg.get("posicao", "baixo"), cfg.get("tamanho", "m")), "utf-8-sig")
    if "--demo" not in a:
        (ROOT / "out").mkdir(exist_ok=True)
        (ROOT / "out" / "legendas.srt").write_text(gera_srt(words), "utf-8")
        print(f"[legendas] {nome}: {saida.name} + out/legendas.srt ({len(words)} palavras)")


if __name__ == "__main__":
    main()
