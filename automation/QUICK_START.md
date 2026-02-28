# 自动化获客系统 - 快速开始指南

## 📦 已完成的三个工具

| 工具 | 文件 | 功能 |
|------|------|------|
| 全平台编排 | `lead_orchestrator.py` | 统一运行电鸭+客栈监控，同步 CRM，生成简报 |
| 项目监控 | `eleduck_monitor.py` | 专门监控电鸭社区新项目 |
| 客栈监控 | `proginn_monitor.py` | 专门监控程序员客栈新线索 |
| AI 回复生成 | `ai_responder.py` | 根据项目需求自动生成个性化回复草稿 |
| CRM 客户管理 | `crm_manager.py` | 客户跟进、项目追踪、自动提醒 |

---

## 🚀 快速开始

### 1. 全平台获客流水线
**运行全量任务：**
```bash
python main.py
```
选择选项 1 即可同时扫描电鸭和程序员客栈，并自动更新 CRM。

### 2. 项目监控（按需）
**单次扫描电鸭：**
```bash
python eleduck_monitor.py --once
```
**单次扫描程序员客栈：**
```bash
python proginn_monitor.py
```

**配置推送（可选）：**
- 微信推送：注册 https://sct.ftqq.com/ 获取密钥
- 钉钉推送：创建钉钉机器人获取 Webhook
- 编辑 `eleduck_monitor.py` 顶部配置区

---

### 2. AI 回复生成器

**交互模式：**
```bash
python ai_responder.py
```

**使用流程：**
1. 选择模板（1=标准/2=快速/3=详细）
2. 粘贴项目需求
3. 自动生成回复草稿
4. 保存到 `data/replies/` 目录

**配置文件：**
编辑 `ai_responder.py` 顶部 `PROFILE` 和 `PORTFOLIO`，替换成你的真实信息。

---

### 3. CRM 客户管理

**查看仪表盘：**
```bash
python crm_manager.py
```

**交互模式：**
```bash
python crm_manager.py --cli
```

**数据位置：**
- `crm_data/clients.json` - 客户信息
- `crm_data/projects.json` - 项目信息
- `crm_data/followups.json` - 跟进记录

**导出 Excel：**
在交互模式中选择选项 8，自动生成 CSV 文件。

---

## 📋 完整工作流

```
1. 项目监控自动运行
   ↓ (发现新项目 → 推送通知)
2. 复制项目需求 → AI 回复生成器
   ↓ (生成回复草稿 → 人工确认)
3. 发送回复 → 添加客户到 CRM
   ↓ (设置跟进提醒)
4. 定期查看 CRM 仪表盘
   ↓ (待跟进客户 → 主动联系)
5. 项目成交 → 更新状态 → 完成
```

---

## ⚙️ 个性化配置

### 修改个人资料
编辑 `ai_responder.py`:
```python
PROFILE = {
    'name': '李凌',
    'years': 15,
    'position': '全栈开发者',
    'skills': {...},
    'available_hours': 20,
}
```

### 修改监控关键词
编辑 `eleduck_monitor.py`:
```python
KEYWORDS = ['Vue', 'React', 'Python', '你的技术栈']
MIN_BUDGET = 3000  # 最低预算
```

### 修改检查间隔
```python
CHECK_INTERVAL = 1800  # 秒（30 分钟）
```

---

## 📅 建议的每日流程

| 时间 | 操作 | 工具 |
|------|------|------|
| 早上 10 点 | 查看监控通知 | 微信/钉钉/日志 |
| 中午 14 点 | 生成回复草稿 | AI 回复生成器 |
| 下午 16 点 | 发送回复 + 跟进 | 手动 + CRM |
| 晚上 20 点 | 查看 CRM 仪表盘 | CRM 管理器 |

---

## 🔧 高级功能

### 开机自启（Windows 任务计划）

1. 打开"任务计划程序"
2. 创建基本任务
3. 名称：电鸭项目监控
4. 触发器：每天 9:00
5. 操作：启动程序
   - 程序：`python.exe`
   - 参数：`D:\编程兼职\automation\eleduck_monitor.py`
   - 起始于：`D:\编程兼职\automation`

### 多平台监控

修改 `eleduck_monitor.py` 添加更多来源：
- 程序员客栈
- 码市
- Upwork
- Fiverr

### AI 优化

接入真实 AI API（Claude/DeepSeek）优化回复质量：
```python
# 在 ai_responder.py 中添加
def generate_with_ai(project_text):
    # 调用 AI API 生成更精准的回复
    pass
```

---

## 📞 有问题？

查看日志文件：
- `data/monitor.log` - 监控日志
- `data/replies/` - 回复草稿
- `crm_data/` - CRM 数据

---

**李秘出品，稳扎稳打！** 🔨
