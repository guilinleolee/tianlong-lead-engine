# 天龙获客引擎 - 全局配置中心
import os

# 飞书群机器人 Webhook 地址
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

# ServerChan (微信推送) SendKey
SCTKEY = "SCT317350TYHO9tkL2HC9UbEG7AiFUPa8v"

# GitHub 配置 (已关联: https://github.com/guilinleolee/tianlong-lead-engine)
GITHUB_REPO = "https://github.com/guilinleolee/tianlong-lead-engine"

# 监控关键词
KEYWORDS = [
    'Python', '后端', '爬虫', '数据', '自动化', 'FastAPI', 'Django', 'Flask',
    'AI', 'LLM', '大模型', 'Web3', 'Node.js'
]

# 最低预算线 (元)
MIN_BUDGET = 3000

# 个人资料配置 (用于 AI 生成投标词)
PROFILE = {
    'name': '李凌',
    'years': 15,
    'position': '全栈开发者',
    'location': '中国（可远程）',
    'available_hours': 20,
}
