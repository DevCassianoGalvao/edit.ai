"""LICENÇA da Edit.AI by Galvao (06/11/2026 — venda pela Kiwify, mensal ou vitalícia).

Só vale no PACOTE VENDIDO: o empacotar_limpo.py grava painel/licenca_config.json {servidor, chave_publica, suporte}.
Sem esse arquivo (o PC do dono) a licença fica desligada e nada muda.

No PC do cliente:
  - o painel abre a tela /licenca até o cliente ativar com o e-mail da compra (POST /ativar no servidor de licenças);
  - o servidor devolve um PASSE assinado (Ed25519) preso a este PC e com validade de alguns dias; o painel confere a
    assinatura sozinho, com a chave pública embutida, e funciona offline até o passe vencer;
  - 1x a cada 12 h o painel renova o passe (POST /verificar); assinatura cancelada/reembolsada -> o servidor nega, o passe
    vence e o painel e o gerente travam (nada é apagado; reativou na Kiwify, volta a funcionar).
Arquivos: painel/licenca_config.json (vem no pacote) e painel/licenca.json (e-mail + passe deste PC).
  python painel/licenca.py            # mostra a situação
  python painel/licenca.py ativar EMAIL
"""
import base64, hashlib, json, os, platform, sys, threading, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONF = HERE / "licenca_config.json"
LOCAL = HERE / "licenca.json"
VERSAO = "2026.11"
RENOVA_H = 12
_trava = threading.Lock()
_ultimo_bg = [0.0]


def _jl(p, d=None):
    try:
        return json.loads(Path(p).read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return d


def ligada():
    return CONF.exists()


def maquina():
    """Identificador deste PC (não muda ao reinstalar a Sala): MachineGuid do Windows, embaralhado."""
    guid = ""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                            0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as k:
            guid = winreg.QueryValueEx(k, "MachineGuid")[0]
    except Exception:  # noqa: BLE001
        guid = platform.node() + str(os.environ.get("PROCESSOR_IDENTIFIER", ""))
    return hashlib.sha256(("sala-de-montagem|" + guid).encode()).hexdigest()[:40]


def _b64u(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def confere_passe(passe, email=None):
    """-> dict do passe se a assinatura confere, é deste PC e não venceu; senão None."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        dados, sig = passe.split(".")
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(_jl(CONF, {})["chave_publica"]))
        pub.verify(_b64u(sig), _b64u(dados))
        c = json.loads(_b64u(dados))
    except Exception:  # noqa: BLE001
        return None
    if c.get("maquina") != maquina() or (email and c.get("email") != email) or c.get("exp", 0) < time.time():
        return None
    return c


def _post(rota, corpo):
    url = _jl(CONF, {})["servidor"].rstrip("/") + rota
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "SalaDeMontagem/" + VERSAO})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def _grava(d):
    tmp = LOCAL.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf-8")
    os.replace(tmp, LOCAL)


def ativar(email, rota="/ativar"):
    email = (email or "").strip().lower()
    corpo = {"email": email, "maquina": maquina(), "nome_pc": platform.node(), "versao": VERSAO}
    try:
        r = _post(rota, corpo)
    except Exception as ex:  # noqa: BLE001
        return {"ok": False, "offline": True, "motivo": f"Sem conexão com o servidor de licenças ({ex.__class__.__name__}). Confira a internet."}
    if r.get("ok") and confere_passe(r.get("passe", ""), email):
        with _trava:
            _grava({"email": email, "passe": r["passe"], "tipo": r.get("tipo"), "aviso": r.get("aviso"), "renovado": time.time()})
        return {"ok": True, "tipo": r.get("tipo"), "aviso": r.get("aviso")}
    if r.get("ok"):
        return {"ok": False, "motivo": "O servidor respondeu, mas o passe não confere com esta instalação. Fale com o suporte."}
    if rota == "/verificar":      # negado de verdade (cancelou/reembolsou): apaga o passe -> trava já
        with _trava:
            d = _jl(LOCAL, {}) or {}
            d.update(passe="", negado=r.get("motivo"), renovado=time.time())
            _grava(d)
    return {"ok": False, "motivo": r.get("motivo") or "Licença não liberada."}


def _renova_bg(email):
    if time.time() - _ultimo_bg[0] < 600:
        return
    _ultimo_bg[0] = time.time()
    threading.Thread(target=ativar, args=(email, "/verificar"), daemon=True).start()


def estado():
    """{ativa, precisa_ativar, email, tipo, expira, aviso, motivo, suporte}"""
    if not ligada():
        return {"ativa": True, "desligada": True}
    cfg, d = _jl(CONF, {}), _jl(LOCAL, {}) or {}
    base = {"suporte": cfg.get("suporte", ""), "email": d.get("email", "")}
    c = confere_passe(d.get("passe", ""), d.get("email")) if d.get("passe") else None
    if c:
        if time.time() - d.get("renovado", 0) > RENOVA_H * 3600:
            _renova_bg(d["email"])
        return {**base, "ativa": True, "tipo": c.get("tipo"), "expira": c.get("exp"), "aviso": d.get("aviso")}
    if d.get("email") and not d.get("negado"):
        _renova_bg(d["email"])          # passe vencido (PC ficou offline): tenta renovar sozinho
    return {**base, "ativa": False, "precisa_ativar": True,
            "motivo": d.get("negado") or ("Ative o Edit.AI by Galvão com o e-mail usado na compra." if not d.get("email")
                                          else "A licença precisa ser renovada: conecte à internet ou ative de novo.")}


def ativa():
    return estado().get("ativa", False)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    if len(sys.argv) > 2 and sys.argv[1] == "ativar":
        print(json.dumps(ativar(sys.argv[2]), ensure_ascii=False, indent=1))
    else:
        print(json.dumps({**estado(), "maquina": maquina()[:8] + "…"}, ensure_ascii=False, indent=1))
