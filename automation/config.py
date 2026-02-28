# 天龙获客引擎 - 全局配置中心
import os
import sys

# 尝试从本地私密配置加载密钥
try:
    from . import config_local
    FEISHU_WEBHOOK = getattr(config_local, 'FEISHU_WEBHOOK', "")
    SCTKEY = getattr(config_local, 'SCTKEY', "")
except (ImportError, ValueError):
    # 如果作为主脚本运行或找不到 local，尝试直接导入
    try:
        import config_local
        FEISHU_WEBHOOK = getattr(config_local, 'FEISHU_WEBHOOK', "")
        SCTKEY = getattr(config_local, 'SCTKEY', "")
    except ImportError:
        # 最后的兜底：尝试从环境变量读取
        FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")
        SCTKEY = os.environ.get("SCTKEY", "")

# GitHub 配置 (已关联: https://github.com/guilinleolee/tianlong-lead-engine)
GITHUB_REPO = "https://github.com/guilinleolee/tianlong-lead-engine"

# 监控关键词（优化版 - 更宽松匹配）
KEYWORDS = [
    # 核心技能
    'Python', '自动化', '脚本', '爬虫', '数据',
    # Web 开发
    '网站', 'Web', '后端', 'API', '系统', '平台',
    # 框架
    'FastAPI', 'Django', 'Flask', 'Vue', 'React',
    # 数据处理
    'Excel', 'Word', 'PDF', '报表', '报告', '生成',
    # 热门技术
    'AI', 'LLM', '大模型', '智能', '机器人',
    # 通用需求
    '开发', '制作', '定制', '外包', '兼职', '远程',
    # 补充关键词
    '办公', '效率', '工具', '管理', '采集', '抓取'
]

# 最低预算线 (元) - 降低门槛
MIN_BUDGET = 1000

# 个人资料配置 (用于 AI 生成投标词)
PROFILE = {
    'name': '李凌',
    'years': 15,
    'position': '全栈开发者',
    'location': '中国（可远程）',
    'available_hours': 20,
}
