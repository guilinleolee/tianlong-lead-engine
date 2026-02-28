# 🐉 天龙引擎：程序员客栈自动化配置
# © 2026 Tianlong Engine

# ==================== API 配置 ====================
ALIYUN_API_KEY = "sk-203e59e3a79e490a83ed2ec22e72f39d"
ALIYUN_MODEL = "qwen-plus"  # 或 qwen-max

# ==================== 筛选标准 ====================
# 高匹配关键词（命中任意一个即进入候选）
HIGH_MATCH_KEYWORDS = [
    "Excel", "Word", "报表", "自动生成", "爬虫", "数据采集",
    "自动化", "数据处理", "批量", "汇总", "周报", "月报",
    "Python", "FastAPI", "后端", "API", "REST"
]

# 排除关键词（命中任意一个即舍弃）
EXCLUDE_KEYWORDS = [
    "兼职长期", "按月付费", "股份合作", "合伙人"
]

# 最低预算（低于此值舍弃）
MIN_BUDGET = 1000

# ==================== 投标配置 ====================
# 投标时间窗口（避免深夜打扰）
BID_START_HOUR = 9
BID_END_HOUR = 18

# 是否需要人工确认（True=起草后等待确认，False=自动发送）
REQUIRE_MANUAL_APPROVAL = True

# ==================== 持久化配置 ====================
SEEN_PROJECTS_FILE = "d:/工作日志/seen_projects.json"
LEADS_LOG_FILE = "d:/工作日志/leads.md"
BID_TEMPLATE_FILE = "d:/个人笔记/投标模板.md"

# ==================== 推送配置（可选） ====================
# 飞书/钉钉 Webhook URL（留空则不推送）
FEISHU_WEBHOOK = ""
DINGTALK_WEBHOOK = ""
