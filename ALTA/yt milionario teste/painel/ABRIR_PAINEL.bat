@echo off
chcp 65001 >nul
title Edit.AI by Galvão
cd /d "%~dp0.."
rem 05/10/2026: o gerente dos funcionarios abre junto (so trabalha quando o botao do escritorio esta LIGADO)
start "Gerente - funcionarios" /min python painel\gerente.py --assumir
python painel\servidor.py %*
pause
