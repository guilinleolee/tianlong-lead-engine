' 天龙引擎静默启动器 (VBScript)
' 功能：启动获客流水线批处理，不显示黑色控制台窗口
Set objShell = CreateObject("WScript.Shell")
' 0 代表隐藏窗口，True 代表等待脚本运行结束
' 这里我们启动批处理文件，它会自动设置环境变量并执行 Python
objShell.Run "cmd.exe /c ""d:\编程兼职\automation\run_engine.bat""", 0, True
Set objShell = Nothing
