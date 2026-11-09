@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 goto erro
python -m pip install --target "%~dp0.deps" --upgrade pycapcut==0.0.4
if errorlevel 1 goto erro
python -m pip install --target "%~dp0.appdeps" --upgrade pywebview==6.2.1
if errorlevel 1 goto erro
cd /d "%~dp0ALTA\yt milionario teste"
call npm.cmd ci --no-audit --no-fund
if errorlevel 1 goto erro
echo Dependencias instaladas.
pause
exit /b 0
:erro
echo A instalacao falhou. Confira internet, Python e Node.js.
pause
exit /b 1
