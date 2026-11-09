' 17/10/2026: o gerente nasce ORFAO (solta.py lanca o laco gerente_fundo.bat e sai). Antes a tarefa esperava o laco e
' toda a arvore descendia do servico do Agendador - e algo matava essa arvore inteira a cada 20-40 min (o servidor do
' painel, orfao, nunca morria). Backup do antigo: gerente_escondido.vbs.bak_solta
Set sh = CreateObject("WScript.Shell")
pasta = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(pasta)
sh.Run "python """ & pasta & "\solta.py"" cmd /c """ & pasta & "\gerente_fundo.bat""", 0, False
