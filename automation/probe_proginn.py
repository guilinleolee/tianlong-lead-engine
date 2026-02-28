# -*- coding: utf-8 -*-
# 天龙引擎：程序员客栈探针
# 使用 Playwright 抓取最新外包项目
# 2026 Tianlong Engine

from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置文件
SEEN_FILE = "d:/工作日志/seen_projects.json"

def load_seen_projects():
    """加载已处理的项目 ID"""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_seen_projects(seen_ids):
    """保存已处理的项目 ID"""
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(seen_ids, f, ensure_ascii=False, indent=2)

def probe_proginn():
    """抓取程序员客栈最新外包项目"""
    url = "https://www.proginn.com/b/outsource"
    print(f"[{datetime.now()}] START: {url}")
    
    seen_projects = load_seen_projects()
    print(f"[INFO] 已记录 {len(seen_projects)} 个历史项目")
    new_projects = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            print("[OK] 页面加载成功")
            
            # 查找项目卡片（根据调试结果调整选择器）
            items = page.query_selector_all("a[href^='/b/p']")
            print(f"[INFO] 找到 {len(items)} 个项目链接")
            
            for i, item in enumerate(items[:30]):
                try:
                    href = item.get_attribute("href")
                    title = item.inner_text().strip()[:100]
                    
                    if not href or not title:
                        continue
                    
                    # 完整 URL
                    full_url = f"https://www.proginn.com{href}"
                    
                    # 去重检查
                    if full_url not in seen_projects:
                        # 尝试提取预算（父元素中查找）
                        budget = "面议"
                        parent = item.query_selector("..")
                        if parent:
                            budget_el = parent.query_selector(".price, .budget, [class*='money'], [class*='price']")
                            if budget_el:
                                budget = budget_el.inner_text().strip()
                        
                        new_projects.append({
                            "id": full_url,
                            "title": title,
                            "budget": budget,
                            "url": full_url,
                            "found_at": datetime.now().isoformat()
                        })
                        print(f"  [NEW] {title} | {budget}")
                    
                except Exception as e:
                    print(f"  [WARN] 解析项目 {i} 失败：{e}")
                    continue
            
            # 更新已见列表
            for proj in new_projects:
                seen_projects.append(proj["id"])
            save_seen_projects(list(dict.fromkeys(seen_projects))[-1000:])
            
            print(f"\n[SUMMARY] 本次发现 {len(new_projects)} 个新项目")
            
            # 输出 JSON
            if new_projects:
                print("\n--- JSON OUTPUT START ---")
                print(json.dumps(new_projects, ensure_ascii=False, indent=2))
                print("--- JSON OUTPUT END ---")
            
        except Exception as e:
            print(f"[ERROR] 抓取失败：{e}")
            
        finally:
            browser.close()
    
    return new_projects

if __name__ == "__main__":
    probe_proginn()
