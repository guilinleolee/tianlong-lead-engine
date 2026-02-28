@echo off
:: 设置工作目录
cd /d "d:\编程兼职\automation"

:: 设置 Python 路径确保模块导入正常
set PYTHONPATH=d:\编程兼职\automation

:: 运行流水线
"D:\Python310\python.exe" lead_orchestrator.py

:: 记录运行完成时间（可选）
echo Last run: %date% %time% >> run_history.log
