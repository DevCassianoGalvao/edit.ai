"""Edit.AI: janela nativa WebView2 para o servidor local existente."""
import os, subprocess, sys, time, urllib.request, json, traceback
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT/'ALTA'/'yt milionario teste'
PANEL=PROJECT/'painel'
LOG=ROOT/'abertura_editai.log'
def registro(msg):
    with LOG.open('a', encoding='utf-8') as log: log.write(f'{datetime.now().isoformat(timespec="seconds")} {msg}\n')
def erro(tipo, valor, tb):
    registro('ERRO: ' + ''.join(traceback.format_exception(tipo, valor, tb)))
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, 'Não foi possível abrir o Edit.AI. Consulte o arquivo abertura_editai.log na pasta do programa.', 'Edit.AI by Galvão', 0x10)
    except Exception: pass
sys.excepthook=erro
registro('Iniciando aplicativo')
sys.path.insert(0,str(ROOT/'.appdeps'))
import webview
registro('WebView carregado')
flags=getattr(subprocess,'CREATE_NO_WINDOW',0)
python_console = str(Path(sys.executable).with_name('python.exe')) if Path(sys.executable).name.lower() == 'pythonw.exe' else sys.executable
subprocess.run([python_console,str(PANEL/'servidor_vivo.py')],cwd=str(PROJECT),check=True,creationflags=flags)
registro('Servidor solicitado')
for _ in range(50):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8876/api/editai',timeout=2) as r:
            if 'presets' in json.load(r):break
    except Exception:time.sleep(.2)
else:raise RuntimeError('O painel local não respondeu na porta 8876.')
registro('Painel respondeu')
if not (PANEL/'.parar_gerente').exists():
    check=subprocess.run([python_console,str(PANEL/'gerente_vivo.py')],cwd=str(PROJECT),creationflags=flags)
    if check.returncode:subprocess.Popen(['wscript.exe',str(PANEL/'gerente_escondido.vbs')],cwd=str(PROJECT),creationflags=flags)
webview.settings['ALLOW_DOWNLOADS']=True
webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER']=True
registro('Criando janela')
webview.create_window('Edit.AI by Galvão','http://127.0.0.1:8876/',width=1440,height=900,min_size=(800,600),background_color='#0b0912',text_select=True)
registro('Abrindo janela')
webview.start(gui='edgechromium',icon=str(PANEL/'app'/'editai.ico'),private_mode=False,storage_path=str(ROOT/'perfil_webview'))
