@echo off
chcp 65001 >nul
title Dark Empire Videos - instalação
cd /d "%~dp0"
where python >nul 2>nul || (echo Python não encontrado. Instale o Python 3.12+ marcando "Add python.exe to PATH" e rode de novo. & pause & exit /b 1)
python instalar.py
