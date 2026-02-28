# 🐉 Tianlong Lead Engine (天龙获客引擎) v2.0

> **天龙获客引擎**：一套基于 AI 驱动的多平台（电鸭、程序员客栈）自动化线索获取与营销系统。通过 7x24h 自动化监控与 AI 个性化回复，帮助开发者从海量众包市场中精准锁定并转化高价值订单。

---

## 🏗️ 核心矩阵 (Core Matrix)

| 组件 | 功能 | 状态 |
| :--- | :--- | :--- |
| **Orchestrator** | 协调全引擎：从监控扫描到 CRM 同步与简报生成。 | 🟢 就绪 |
| **Monitors** | **电鸭监控** (BS4) + **客栈探针** (BS4/Playwright)。 | 🟢 运行中 |
| **AI Responder** | 语义分析需求并自动草拟极具竞争力的投标方案。 | 🟢 进阶 |
| **SimpleCRM** | 轻量级客户、项目、跟进记录与收入统计管理。 | 🟢 在线 |
| **Auto-Scheduler** | 利用 Windows 任务计划程序实现的隐形后台运行。 | 🟢 已部署 |

---

## 🚀 快速启动

### 方式一：控制台操作（推荐）
在根目录下运行：
```powershell
python main.py
```
- **选项 1**：立即运行一次全平台扫描与 CRM 同步。
- **选项 2**：查看您的 CRM 业务看板。
- **选项 4**：查看最新生成的 Markdown 获客简报。

### 方式二：后台静默运行
若需引擎在后台 24 小时运行，请运行以下设置脚本：
```powershell
powershell -ExecutionPolicy Bypass -File setup_tianlong_scheduler.ps1
```

---

## 📂 目录结构
- `/automation`: 核心业务逻辑（监控、AI、CRM）。
- `/automation/reports`: 自动生成的每日获客简报。
- `/automation/tests`: 核心组件单元测试（pytest）。
- `/crm_data`: CRM 数据库（JSON）。
- `main.py`: 根目录统一入口。

---

## 🛠️ 配置与定制
您可以根据自身技术栈在以下文件中调整关键词与报价逻辑：
- `automation/eleduck_monitor.py` (KEYWORDS, MIN_BUDGET)
- `automation/ai_responder.py` (PROFILE, RATE_CARD)

---
*© 2026 Tianlong Engine | 系统自动化，价值最大化。*
