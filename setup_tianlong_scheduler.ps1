# 天龙获客引擎 - 自动化调度设置脚本
# 功能：将静默启动器注册到 Windows 任务计划程序，每小时运行一次

$taskName = "Tianlong_Lead_Engine_Auto"
$taskDescription = "天龙获客引擎全自动全平台监控。每小时自动执行，发现新线索同步 CRM 并生成简报。"

# 1. 定义执行操作：使用 wscript 运行静默启动脚本
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "d:\编程兼职\automation\silent_start.vbs"

# 2. 定义触发器：从现在开始，每 60 分钟重复一次，无限期运行
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Hours 1)

# 3. 设置任务选项：允许在交流电和电池模式下运行（笔记本适用），若失败则每10分钟重试
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# 4. 注册任务 (需以管理员权限运行或确认弹窗)
Write-Host "正在注册任务: $taskName ..." -ForegroundColor Cyan
Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "✅ [天龙引擎] 自动化调度已就绪！" -ForegroundColor Green
Write-Host "系统将每 1 小时静默运行一次获客分析。" -ForegroundColor Yellow
Write-Host "您可以运行 'main.py' 选项 4 查看最新获客简报。" -ForegroundColor Cyan

# 询问是否立即执行第一次测试
$confirm = Read-Host "是否立即进行第一次【静默运行测试】？(Y/N)"
if ($confirm -match "[yY]") {
    Start-ScheduledTask -TaskName $taskName
    Write-Host "已启动后台测试运行..." -ForegroundColor Green
}
