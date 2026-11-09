' SALA DE MONTAGEM — o app (16/10/2026). Um clique: liga o painel e o gerente se estiverem parados e abre a Central
' numa janela própria (Edge em modo app; sem Edge, Chrome; sem os dois, o navegador padrão).
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
painel = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
raiz = fso.GetParentFolderName(painel)
sh.CurrentDirectory = raiz
sh.Environment("PROCESS")("PYTHONIOENCODING") = "utf-8"
sh.Run "python """ & painel & "\servidor_vivo.py""", 0, True
If Not fso.FileExists(painel & "\.parar_gerente") Then
  If sh.Run("python """ & painel & "\gerente_vivo.py""", 0, True) <> 0 Then
    sh.Run "wscript.exe """ & painel & "\gerente_escondido.vbs""", 0, False
  End If
End If
url = "http://127.0.0.1:8876/central"
For i = 1 To 20
  ok = sh.Run("powershell -NoProfile -Command ""try{(Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 " & url & ")|Out-Null;exit 0}catch{exit 1}""", 0, True)
  If ok = 0 Then Exit For
  WScript.Sleep 1000
Next
edge = sh.ExpandEnvironmentStrings("%ProgramFiles(x86)%") & "\Microsoft\Edge\Application\msedge.exe"
chrome = sh.ExpandEnvironmentStrings("%ProgramFiles%") & "\Google\Chrome\Application\chrome.exe"
If fso.FileExists(edge) Then
  sh.Run """" & edge & """ --app=" & url & " --window-size=1300,900", 1, False
ElseIf fso.FileExists(chrome) Then
  sh.Run """" & chrome & """ --app=" & url & " --window-size=1300,900", 1, False
Else
  sh.Run url, 1, False
End If
