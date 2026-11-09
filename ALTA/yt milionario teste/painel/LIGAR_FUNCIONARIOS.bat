@echo off
chcp 65001 >nul
title Gerente - funcionarios da Sala de Montagem
cd /d "%~dp0.."
echo Deixe esta janela aberta: o gerente poe os funcionarios para trabalhar sozinhos.
echo Ligue/desligue pelo botao na tela do escritorio: http://127.0.0.1:8876/escritorio
python painel\gerente.py --assumir
pause
