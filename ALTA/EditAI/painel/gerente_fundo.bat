@echo off
rem 07/10/2026: VIGIA do gerente — a tarefa "EditAI Gerente" do Agendador roda isto ao entrar no Windows e a cada
rem 5 min. Se já existe um gerente vivo (ex.: ligado pelo chat), sai na hora. Se não, liga e fica no laço: quando o
rem gerente.py muda ele sai sozinho e este laço religa. Para parar de vez: criar painel\.parar_gerente
chcp 65001 >nul
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
set GERENTE_LOOP=1
rem 07/10/2026: o painel (porta 8876) também volta sozinho se cair
python painel\servidor_vivo.py >> painel\gerente_console.log 2>&1
:laco
if exist painel\.parar_gerente goto fim
python painel\gerente_vivo.py && goto fim
echo [%date% %time%] vigia: gerente caido - religando >> painel\gerente_console.log
python -u painel\gerente.py --assumir >> painel\gerente_console.log 2>&1
timeout /t 5 /nobreak >nul
goto laco
:fim
