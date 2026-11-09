' 07/10/2026: vigia do PAINEL (tarefa "SalaMontagem Painel", a cada 5 min): religa o servidor.py escondido se caiu
Set sh = CreateObject("WScript.Shell")
pasta = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(pasta)
sh.Run "python """ & pasta & "\servidor_vivo.py""", 0, True
