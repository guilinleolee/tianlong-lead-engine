import json
import os
import time

# 配置
DATA_DIR = "d:/编程兼职/automation/data"
AUDIT_DIR = "d:/编程兼职/automation/audit"
KEYWORDS = ["Python", "爬虫", "后端", "数据采集", "自动化", "Scraping", "Crawler"]
EXCLUDE_KEYWORDS = ["UI", "设计", "平面", "美工"]

if not os.path.exists(AUDIT_DIR):
    os.makedirs(AUDIT_DIR)

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def log(message):
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")
    except:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] (Encoding error in log message)")

def audit_projects():
    log("开始项目审核...")
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("projects_") and f.endswith(".json")]
    
    if not files:
        log("没有待审核的项目文件")
        return

    for file in files:
        filepath = os.path.join(DATA_DIR, file)
        with open(filepath, "r", encoding="utf-8") as f:
            projects = json.load(f)
        
        qualified = []
        for p in projects:
            title = p.get("title", "")
            # 简单审核逻辑：关键词匹配 (后续可替换为 LLM API)
            is_match = any(k.lower() in title.lower() for k in KEYWORDS)
            is_exclude = any(k.lower() in title.lower() for k in EXCLUDE_KEYWORDS)
            
            if is_match and not is_exclude:
                p["audit_score"] = 100 # 初始分
                p["status"] = "qualified"
                qualified.append(p)
                log(f"审核通过: {title}")
            else:
                log(f"审核过滤: {title}")
        
        if qualified:
            audit_file = os.path.join(AUDIT_DIR, f"qualified_{file}")
            with open(audit_file, "w", encoding="utf-8") as f:
                json.dump(qualified, f, ensure_ascii=False, indent=2)
            log(f"保存 {len(qualified)} 个合格项目至 {audit_file}")
            
        # 移动已处理的文件
        # os.rename(filepath, os.path.join(DATA_DIR, "processed_" + file))

if __name__ == "__main__":
    audit_projects()
