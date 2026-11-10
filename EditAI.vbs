Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(WScript.ScriptFullName)
' O Windows inicia a janela fora do processo que chamou o atalho.
Set explorer = CreateObject("Shell.Application")
explorer.ShellExecute "pythonw.exe", """" & root & "\EditAI.py""", root, "open", 1
