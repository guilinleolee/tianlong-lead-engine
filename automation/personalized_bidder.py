import json
import os
import time

# 配置
AUDIT_DIR = "d:/编程兼职/automation/audit"
BIDS_DIR = "d:/编程兼职/automation/bids"
TEMPLATE_PATH = "d:/投标模板/程序员客栈通用模板.md" # 引用之前创建的模板

if not os.path.exists(BIDS_DIR):
    os.makedirs(BIDS_DIR)

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def log(message):
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")
    except:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] (Encoding error in log message)")

def load_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "您好，我对您的项目 [TITLE] 非常感兴趣。我有丰富的 [TECH] 开发经验..."

def generate_bids():
    log("开始生成投标方案...")
    template_content = load_template()
    
    files = [f for f in os.listdir(AUDIT_DIR) if f.startswith("qualified_") and f.endswith(".json")]
    
    for file in files:
        filepath = os.path.join(AUDIT_DIR, file)
        with open(filepath, "r", encoding="utf-8") as f:
            projects = json.load(f)
            
        for p in projects:
            title = p.get("title", "")
            url = p.get("url", "")
            
            # 生成个性化投标词
            bid_content = template_content.replace("[项目名称]", title)
            # 这里可以进一步根据项目关键词动态调整
            
            bid_data = {
                "project_id": p.get("id"),
                "project_title": title,
                "project_url": url,
                "bid_content": bid_content,
                "status": "pending_approval",
                "timestamp": time.time()
            }
            
            bid_file = os.path.join(BIDS_DIR, f"bid_{p.get('id')}.json")
            with open(bid_file, "w", encoding="utf-8") as f:
                json.dump(bid_data, f, ensure_ascii=False, indent=2)
            log(f"已生成投标预案: {title} -> {bid_file}")

if __name__ == "__main__":
    generate_bids()
