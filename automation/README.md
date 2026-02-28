# 电鸭项目监控自动化

## 快速开始

### 1. 安装依赖

```bash
cd D:\编程兼职\automation
pip install -r requirements.txt
```

### 2. 运行脚本

**测试运行（只扫描一次）：**
```bash
python eleduck_monitor.py --once
```

**持续监控（每 30 分钟扫描）：**
```bash
python eleduck_monitor.py
```

### 3. 查看结果

- 新项目通知：控制台输出 + `data/monitor.log`
- 项目缓存：`data/projects.json`
- 已看项目：`data/seen_projects.txt`

---

## 配置说明

编辑 `eleduck_monitor.py` 顶部的配置区：

### 关键词过滤
```python
KEYWORDS = ['Vue', 'React', 'Python', '全栈', 'AI', ...]
```

### 最低预算
```python
MIN_BUDGET = 3000  # 低于 3000 元的项目不提醒
```

### 推送通知

**微信推送（ServerChan）：**
1. 访问 https://sct.ftqq.com/ 获取密钥
2. 配置 `SERVER_CHAN_KEY = "你的密钥"`
3. 设置 `PUSH_CONFIG['wechat'] = True`

**钉钉推送：**
1. 创建钉钉机器人获取 Webhook
2. 配置 `DINGTALK_WEBHOOK = "你的 webhook"`
3. 设置 `PUSH_CONFIG['dingtalk'] = True`

---

## 高级用法

### 修改扫描间隔
```python
CHECK_INTERVAL = 1800  # 秒（30 分钟）
```

### 添加监控关键词
```python
KEYWORDS.append('你的技术栈')
```

### 设置为开机自启

**Windows 任务计划程序：**
1. 打开"任务计划程序"
2. 创建基本任务
3. 程序：`python.exe`
4. 参数：`D:\编程兼职\automation\eleduck_monitor.py`
5. 起始于：`D:\编程兼职\automation`

---

## 注意事项

1. **页面结构变化**：如果电鸭社区改版，需要调整 `_parse_item` 方法中的 CSS 选择器
2. **请求频率**：建议间隔≥30 分钟，避免被封 IP
3. **Cookie 登录**：如需查看登录后查看的项目，需要在 `session.headers` 中添加 Cookie

---

## 下一步优化

- [ ] 添加 Cookie 登录支持
- [ ] 增加更多项目源（程序员客栈、码市）
- [ ] AI 自动生成回复草稿
- [ ] 简易 CRM 客户管理

---

**有问题随时找李秘！** 🔨
