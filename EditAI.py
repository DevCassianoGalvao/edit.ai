"""Edit.AI: janela nativa WebView2 para o servidor local existente."""
import os, subprocess, sys, time, urllib.request, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT/'ALTA'/'yt milionario teste'
PANEL=PROJECT/'painel'
sys.path.insert(0,str(ROOT/'.appdeps'))
import webview
flags=getattr(subprocess,'CREATE_NO_WINDOW',0)
subprocess.run([sys.executable,str(PANEL/'servidor_vivo.py')],cwd=str(PROJECT),check=True,creationflags=flags)
for _ in range(50):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8876/api/editai',timeout=2) as r:
            if 'presets' in json.load(r):break
    except Exception:time.sleep(.2)
else:raise RuntimeError('O painel local não respondeu na porta 8876.')
if not (PANEL/'.parar_gerente').exists():
    check=subprocess.run([sys.executable,str(PANEL/'gerente_vivo.py')],cwd=str(PROJECT),creationflags=flags)
    if check.returncode:subprocess.Popen(['wscript.exe',str(PANEL/'gerente_escondido.vbs')],cwd=str(PROJECT),creationflags=flags)
webview.settings['ALLOW_DOWNLOADS']=True
webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER']=True
webview.create_window('Edit.AI by Galvão','http://127.0.0.1:8876/',width=1440,height=900,min_size=(800,600),background_color='#0b0912',text_select=True)
webview.start(gui='edgechromium',icon=str(PANEL/'app'/'editai.ico'),private_mode=False,storage_path=str(ROOT/'perfil_webview'))
