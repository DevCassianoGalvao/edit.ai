@echo off
cd /d "%~dp0MAPA"
start "Mapa - servidor" /min python servidor.py 8877
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8877/"
